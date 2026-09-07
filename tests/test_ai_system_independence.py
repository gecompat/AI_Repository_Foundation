from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AT = datetime(2026, 9, 7, 18, 0, tzinfo=timezone.utc)
sys.path.insert(0, str(ROOT / "tools"))


def load_module(name: str, relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ai_work = load_module("foundation_ai_work_independence", "foundation/capabilities/ai-work/ai_work.py")
installer = load_module("foundation_installer_independence", "tools/install_foundation.py")


def work_request(
    task_class: str = "software.change",
    functions: list[str] | None = None,
    *,
    data_class: str = "INTERNAL",
    effects: list[str] | None = None,
    authorities: list[str] | None = None,
    boundaries: list[str] | None = None,
    validation_functions: list[str] | None = None,
    allow_human: bool = True,
    max_cost_usd: float = 1,
) -> dict[str, object]:
    return {
        "schema_version": 1,
        "contract": "foundation-ai-work/v1",
        "work_id": "acceptance-work",
        "task_class": task_class,
        "data_class": data_class,
        "risk": "LOW",
        "effects": effects if effects is not None else ["LOCAL_READ"],
        "input_handles": [{"handle_id": "input", "kind": "EPHEMERAL", "content_sha256": "sha256:" + "a" * 64}],
        "output": {"format": "application/json", "handle": {"handle_id": "output", "kind": "EPHEMERAL"}},
        "required_capabilities": functions if functions is not None else ["repository.inspect", "repository.edit"],
        "allowed_execution_boundaries": boundaries if boundaries is not None else ["PROCESS", "HOST"],
        "authorization": {
            "granted_authorities": authorities if authorities is not None else ["filesystem:read"],
            "remote_data_classes": [],
            "allow_local_adapter_synthesis": False,
        },
        "quality": {"minimum_success_probability": 0.5},
        "limits": {"max_cost_usd": max_cost_usd, "max_network_mb": 0, "max_ram_mb": 1024},
        "validation": {
            "required_capabilities": validation_functions if validation_functions is not None else [],
            "independent_required": bool(validation_functions),
            "allow_human": allow_human,
        },
    }


def capability(
    capability_id: str,
    functions: list[str],
    *,
    kind: str = "DETERMINISTIC_TOOL",
    boundary: str = "PROCESS",
    health: str = "HEALTHY",
    expires_at: datetime | None = None,
    required_authorities: list[str] | None = None,
    cost: float = 0,
) -> dict[str, object]:
    expiry = expires_at if expires_at is not None else AT + timedelta(minutes=5)
    return {
        "schema_version": 1,
        "contract": "foundation-ai-work/v1",
        "capability_id": capability_id,
        "kind": kind,
        "protocol": "foundation-ai-adapter-jsonl/v1",
        "execution_boundary": boundary,
        "required_authorities": required_authorities if required_authorities is not None else ["filesystem:read"],
        "health": {
            "state": health,
            "checked_at": ai_work.isoformat(AT - timedelta(minutes=1)),
            "expires_at": ai_work.isoformat(expiry),
            "reason_code": "SYNTHETIC_ACCEPTANCE_STATE",
        },
        "functions": functions,
        "data_classes_allowed": ["PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"],
        "deterministic": kind != "MODEL",
        "provenance": {"source": "synthetic-acceptance-fixture", "observed_at": ai_work.isoformat(AT - timedelta(minutes=1))},
        "quality": {"provenance": "CONFIGURED", "predicted_success": 1, "observations": 0},
        "resources": {"network_mb": 0, "ram_mb": 32},
        "cost_model": {"provenance": "CONFIGURED", "currency": "USD", "estimated_cost": cost},
    }


class AISystemIndependenceTests(unittest.TestCase):
    def test_default_transfer_contains_no_executable_ai_runtime(self) -> None:
        manifest = json.loads((ROOT / "foundation/manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["default_capabilities"], [])
        executable_suffixes = {".py", ".ps1", ".exe", ".dll", ".so", ".dylib"}
        self.assertFalse([row["source"] for row in manifest["core"] if Path(row["source"]).suffix.lower() in executable_suffixes])
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            with redirect_stdout(StringIO()):
                self.assertEqual(installer.main([str(target), "--adapters", "none", "--apply"]), 0)
            self.assertEqual(list(target.rglob("*.py")), [])
            rules = (target / ".ai/foundation/AI_WORK_ORCHESTRATION_POLICY.md").read_text(encoding="utf-8")
            self.assertIn("Foundation rules, installation, upgrade assessment", rules)
            self.assertIn("every optional capability is unavailable", rules)

    def test_component_failure_matrix_isolated_or_degrades_truthfully(self) -> None:
        required = ["repository.inspect", "repository.edit"]
        healthy = capability("healthy", required)
        scenarios = {
            "no_runtime": ([], "MANUAL_REQUIRED"),
            "missing_process": ([capability("missing", required, health="UNAVAILABLE")], "MANUAL_REQUIRED"),
            "dead_endpoint_with_healthy_alternative": ([capability("dead-endpoint", required, health="UNAVAILABLE"), healthy], "EXECUTABLE"),
            "timeout_with_healthy_alternative": ([capability("timeout", required, health="UNAVAILABLE"), healthy], "EXECUTABLE"),
            "invalid_response_with_healthy_alternative": ([{"capability_id": "invalid-response"}, healthy], "EXECUTABLE"),
            "expired_fragment_with_healthy_alternative": ([capability("expired", required, expires_at=AT), healthy], "EXECUTABLE"),
            "missing_credentials_with_healthy_alternative": ([capability("credentialed", required, required_authorities=["credential:runtime"]), healthy], "EXECUTABLE"),
            "exhausted_budget": ([capability("expensive", required, cost=2)], "MANUAL_REQUIRED"),
        }
        for scenario, (catalog, expected) in scenarios.items():
            with self.subTest(scenario=scenario):
                result = ai_work.plan(work_request(), catalog, at=AT)
                self.assertEqual(result["status"], expected)
                if expected == "EXECUTABLE":
                    self.assertEqual(result["steps"][0]["capability_id"], "healthy")

        unavailable = ai_work.plan(work_request(allow_human=False), [], at=AT)
        self.assertEqual(unavailable["status"], "UNAVAILABLE")
        no_validator = ai_work.plan(
            work_request(validation_functions=["foundation.validate"]),
            [healthy],
            at=AT,
        )
        self.assertEqual(no_validator["status"], "MANUAL_REQUIRED")

    def test_no_network_or_mcp_does_not_block_healthy_process_tool(self) -> None:
        required = ["repository.inspect", "repository.edit"]
        request = work_request(boundaries=["PROCESS", "REMOTE"])
        remote = capability("remote-provider", required, kind="MODEL", boundary="REMOTE")
        local = capability("process-tool", required)
        result = ai_work.plan(request, [remote, local], at=AT)
        self.assertEqual(result["status"], "EXECUTABLE")
        self.assertEqual(result["steps"][0]["capability_id"], "process-tool")
        self.assertNotIn("MCP", json.dumps(result))

    def test_nonpublic_remote_processing_requires_explicit_data_authority(self) -> None:
        request = work_request(data_class="CONFIDENTIAL", boundaries=["REMOTE"])
        remote = capability("remote-model", ["repository.inspect", "repository.edit"], kind="MODEL", boundary="REMOTE")
        blocked = ai_work.plan(request, [remote], at=AT)
        self.assertEqual(blocked["status"], "BLOCKED")
        self.assertIn("REMOTE_DATA_NOT_AUTHORIZED", blocked["reason_codes"])

        request["authorization"]["remote_data_classes"] = ["CONFIDENTIAL"]
        authorized = ai_work.plan(request, [remote], at=AT)
        self.assertEqual(authorized["status"], "EXECUTABLE")

    def test_rights_matrix_requires_exact_capability_and_effect_authority(self) -> None:
        read = ai_work.plan(
            work_request(functions=["repository.inspect"]),
            [capability("reader", ["repository.inspect"])],
            at=AT,
        )
        self.assertEqual(read["status"], "EXECUTABLE")

        local_write_request = work_request(
            effects=["LOCAL_READ", "LOCAL_WRITE"],
            authorities=["filesystem:read", "filesystem:write"],
        )
        local_only = capability(
            "local-writer",
            ["repository.inspect", "repository.edit"],
            required_authorities=["filesystem:read", "filesystem:write"],
        )
        self.assertEqual(ai_work.plan(local_write_request, [local_only], at=AT)["status"], "EXECUTABLE")

        push_capability = capability(
            "branch-pr",
            ["repository.inspect", "repository.edit"],
            required_authorities=["filesystem:read", "filesystem:write", "git:push", "github:pull_request"],
        )
        without_push = ai_work.plan(local_write_request, [push_capability], at=AT)
        self.assertEqual(without_push["status"], "BLOCKED")
        self.assertIn("CAPABILITY_AUTHORITY_MISSING", without_push["reason_codes"])

        branch_pr_request = work_request(
            effects=["LOCAL_READ", "LOCAL_WRITE", "EXTERNAL_WRITE"],
            authorities=["filesystem:read", "filesystem:write", "external:write", "git:push", "github:pull_request", "approve:risk-boundary"],
        )
        self.assertEqual(ai_work.plan(branch_pr_request, [push_capability], at=AT)["status"], "EXECUTABLE")

        forbidden_publish = work_request(effects=["PUBLISH"], authorities=["filesystem:read"])
        blocked = ai_work.plan(forbidden_publish, [capability("publisher", ["repository.inspect", "repository.edit"])], at=AT)
        self.assertEqual(blocked["status"], "BLOCKED")
        self.assertIn("AUTHORITY_MISSING:publish", blocked["reason_codes"])

    def test_representative_workflows_have_safe_plans_and_independent_validation(self) -> None:
        workflows = [
            ("software.change", ["repository.inspect", "repository.edit"], "foundation.validate", "DETERMINISTIC_TOOL"),
            ("research.sourced", ["research.retrieve", "research.synthesize"], "sources.verify", "RETRIEVAL"),
            ("documentation.author", ["documentation.author"], "documentation.check", "RENDERER"),
            ("data.structured", ["structured-data.transform"], "structured-data.validate", "DETERMINISTIC_TOOL"),
            ("project.custom", ["project.declared"], "project.validate", "DETERMINISTIC_TOOL"),
        ]
        for task_class, functions, validation_function, kind in workflows:
            with self.subTest(task_class=task_class):
                request = work_request(task_class, functions, validation_functions=[validation_function])
                worker = capability("worker", functions, kind=kind)
                validator = capability("validator", [validation_function], kind="VALIDATOR")
                result = ai_work.plan(request, [worker, validator], at=AT)
                self.assertEqual(result["status"], "EXECUTABLE")
                self.assertEqual([step["step_id"] for step in result["steps"]], ["work", "validate"])
                self.assertEqual(result["steps"][1]["depends_on"], ["work"])

    def test_ci_contract_keeps_linux_gate_and_adds_windows_macos_matrix(self) -> None:
        workflow = (ROOT / ".github/workflows/foundation-ci.yml").read_text(encoding="utf-8")
        self.assertIn("os: [windows-latest, macos-latest]", workflow)
        self.assertIn("runs-on: ubuntu-latest", workflow)
        self.assertIn("needs: platform-contracts", workflow)
        self.assertIn("tests.test_ai_system_independence", workflow)


if __name__ == "__main__":
    unittest.main()
