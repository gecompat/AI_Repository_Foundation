from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


executor = load_module(
    "foundation_ai_executor_self_hosting",
    ROOT / "foundation" / "capabilities" / "ai-executor" / "ai_executor.py",
)


class AIWorkSelfHostingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.profile = json.loads((ROOT / ".ai" / "ai-work" / "profile.json").read_text(encoding="utf-8"))

    def test_source_profile_is_provider_free_and_runtime_external(self) -> None:
        self.assertEqual(self.profile["contract"], "foundation-ai-work/v1")
        self.assertEqual(self.profile["provider_requirements"], [])
        self.assertEqual(self.profile["runtime_inventory_location"], "OUTSIDE_REPOSITORY")
        self.assertEqual(self.profile["client_dispatch"]["client_requirements"], [])
        self.assertEqual(self.profile["client_dispatch"]["runtime_state_location"], "OUTSIDE_REPOSITORY")
        text = json.dumps(self.profile).lower()
        for forbidden in ("ollama", "openai", "lm studio", "c:\\", "d:\\", "token", "credential"):
            self.assertNotIn(forbidden, text)

    def test_source_profile_covers_representative_open_work_classes(self) -> None:
        profiles = self.profile["task_profiles"]
        self.assertEqual(
            set(profiles),
            {"software.change", "research.sourced", "documentation.author", "data.structured", "project.custom"},
        )
        self.assertEqual(self.profile["degradation"]["no_capability"], "MANUAL_REQUIRED")
        self.assertEqual(self.profile["degradation"]["provider_failure"], "EXCLUDE_PROVIDER_FRAGMENT_ONLY")
        dispatch = self.profile["client_dispatch"]
        self.assertEqual(dispatch["requested_without_actual_evidence"], "REQUESTED_NOT_ATTESTED")
        self.assertEqual(dispatch["manual_fallback"], "MANUAL_DISPATCH_REQUIRED")
        self.assertEqual(dispatch["actual_model_evidence"], ["HOST_EXECUTION", "HOST_RESPONSE_METADATA"])
        self.assertEqual(dispatch["trusted_dispatch_issuers"], [])

    def test_source_profile_without_optional_capabilities_degrades_truthfully(self) -> None:
        at = datetime.now(timezone.utc).replace(microsecond=0)
        source = ROOT / ".ai" / "ai-work" / "profile.json"
        selected = self.profile["task_profiles"]["project.custom"]
        request = {
            "schema_version": 1,
            "contract": "foundation-ai-work/v1",
            "work_id": "foundation-self-host-no-runtime",
            "task_class": "project.custom",
            "data_class": self.profile["data_defaults"]["data_class"],
            "risk": selected["risk"],
            "effects": selected["effects"],
            "input_handles": [{
                "handle_id": "profile",
                "kind": "FILE",
                "content_sha256": "sha256:" + hashlib.sha256(source.read_bytes()).hexdigest(),
            }],
            "output": {"format": "application/json", "handle": {"handle_id": "result", "kind": "EPHEMERAL"}},
            "required_capabilities": selected["required_capabilities"],
            "allowed_execution_boundaries": ["PROCESS"],
            "authorization": {
                "granted_authorities": ["filesystem:read"],
                "remote_data_classes": self.profile["data_defaults"]["remote_data_classes"],
                "allow_local_adapter_synthesis": False,
            },
            "quality": {},
            "limits": {"max_cost_usd": 0, "max_network_mb": 0, "max_ram_mb": 64, "max_attempts": 1},
            "validation": {
                "required_capabilities": selected["validation_capabilities"],
                "independent_required": False,
                "allow_human": True,
            },
        }
        result = executor.ai_work.plan(request, [], at=at)
        self.assertEqual(result["status"], self.profile["degradation"]["no_capability"])
        self.assertEqual(result["reason_codes"], ["REQUIRED_CAPABILITY_UNAVAILABLE"])

    def test_foundation_validation_is_shell_free_and_maps_existing_gates(self) -> None:
        validation = self.profile["validation_capabilities"]["foundation.validate"]
        self.assertFalse(validation["shell_evaluation"])
        commands = validation["commands"]
        self.assertTrue(all(isinstance(command, list) and command for command in commands))
        flat = [item for command in commands for item in command]
        for required in (
            "tools/transfer_manifest_guard.py",
            "tools/feature_catalog_guard.py",
            "foundation/capabilities/artifact-registry-github/registry_semantic.py",
            "tools/foundation_validator.py",
            "unittest",
        ):
            self.assertIn(required, flat)

    def test_source_profile_is_not_transfer_payload(self) -> None:
        manifest = json.loads((ROOT / "foundation" / "manifest.json").read_text(encoding="utf-8"))
        sources = {item["source"] for item in manifest["core"]}
        for rows in manifest["adapters"].values():
            sources.update(item["source"] for item in rows)
        for rows in manifest["capabilities"].values():
            sources.update(item["source"] for item in rows)
        self.assertNotIn(".ai/AI_WORK_PROFILE.md", sources)
        self.assertNotIn(".ai/ai-work/profile.json", sources)

    def test_reference_planner_adapter_and_executor_use_profile_without_expanding_authority(self) -> None:
        at = datetime.now(timezone.utc).replace(microsecond=0)
        source = ROOT / ".ai" / "ai-work" / "profile.json"
        source_body = source.read_bytes()
        selected = self.profile["task_profiles"]["project.custom"]
        request = {
            "schema_version": 1,
            "contract": "foundation-ai-work/v1",
            "work_id": "foundation-self-host-profile-check",
            "task_class": "project.custom",
            "data_class": self.profile["data_defaults"]["data_class"],
            "risk": selected["risk"],
            "effects": selected["effects"],
            "input_handles": [{
                "handle_id": "profile",
                "kind": "FILE",
                "content_sha256": "sha256:" + hashlib.sha256(source_body).hexdigest(),
            }],
            "output": {"format": "application/json", "handle": {"handle_id": "verified-copy", "kind": "EPHEMERAL"}},
            "required_capabilities": selected["required_capabilities"],
            "allowed_execution_boundaries": ["PROCESS"],
            "authorization": {
                "granted_authorities": ["filesystem:read"],
                "remote_data_classes": self.profile["data_defaults"]["remote_data_classes"],
                "allow_local_adapter_synthesis": False,
            },
            "quality": {},
            "limits": {"max_cost_usd": 0, "max_network_mb": 0, "max_ram_mb": 64, "max_attempts": 1},
            "validation": {
                "required_capabilities": selected["validation_capabilities"],
                "independent_required": False,
                "allow_human": True,
            },
        }
        capability = {
            "schema_version": 1,
            "contract": "foundation-ai-work/v1",
            "capability_id": "foundation-self-host-command",
            "kind": "DETERMINISTIC_TOOL",
            "protocol": "foundation-ai-adapter-jsonl/v1",
            "execution_boundary": "PROCESS",
            "required_authorities": ["filesystem:read"],
            "health": {
                "state": "HEALTHY",
                "checked_at": executor.isoformat(at - timedelta(minutes=1)),
                "expires_at": executor.isoformat(at + timedelta(minutes=5)),
                "reason_code": "SELF_HOST_TEST_PROBE",
            },
            "functions": selected["required_capabilities"],
            "data_classes_allowed": [request["data_class"]],
            "deterministic": True,
            "provenance": {
                "source": "foundation-source-profile",
                "observed_at": executor.isoformat(at - timedelta(minutes=1)),
            },
            "quality": {"provenance": "CONFIGURED", "predicted_success": 1, "observations": 0},
            "resources": {"network_mb": 0, "ram_mb": 16},
            "cost_model": {"provenance": "CONFIGURED", "currency": "USD", "estimated_cost": 0},
            "execution": {"idempotency": "IDEMPOTENT_REPLAY", "resume": "RESTART"},
        }
        plan = executor.ai_work.plan(request, [capability], at=at)
        self.assertEqual(plan["status"], "EXECUTABLE")

        with tempfile.TemporaryDirectory() as tmp:
            external = Path(tmp).resolve()
            output = external / "verified-copy.json"
            config = external / "command-adapter.json"
            config.write_text(json.dumps({
                "provider": "foundation-self-host",
                "execution_boundary": "PROCESS",
                "probe_argv": [str(Path(sys.executable).resolve()), "-c", "raise SystemExit(0)"],
                "catalog_argv": [str(Path(sys.executable).resolve()), "-c", "print('{\"fragments\":[]}')"],
                "invoke_argv": [str(Path(sys.executable).resolve()), "-c", "import sys;sys.stdout.buffer.write(sys.stdin.buffer.read())"],
                "environment_allowlist": [],
                "timeout_seconds": 10,
                "allowed_data_classes": [request["data_class"]],
                "read_roots": [str(ROOT)],
                "write_roots": [str(external)],
                "cwd": str(ROOT),
            }, sort_keys=True), encoding="utf-8")
            bindings = {"bindings": {capability["capability_id"]: {
                "argv": [
                    str(Path(sys.executable).resolve()),
                    str((ROOT / "foundation" / "capabilities" / "ai-runtime-adapters" / "reference_adapters.py").resolve()),
                    "command",
                    "--config",
                    str(config),
                ],
                "environment_allowlist": [],
                "timeout_seconds": 15,
            }}}
            handles = {"handles": {"profile": str(source), "verified-copy": str(output)}}
            store = executor.CheckpointStore(external / "state")
            runner = executor.Executor(
                request,
                plan,
                [capability],
                bindings,
                handles,
                store=store,
                clock=lambda: at,
            )
            report = runner.execute()
            self.assertEqual(report["status"], "COMPLETED", report)
            self.assertEqual(output.read_bytes(), source_body)
            self.assertEqual(report["resource_usage"]["cost_usd"], 0)
            self.assertEqual(report["resource_usage"]["network_mb"], 0)
            self.assertEqual(report["validation_status"], "NOT_REQUIRED")
            self.assertEqual(len(report["attempts"]), 1)

            checkpoint = store.path(plan["plan_id"]).read_text(encoding="utf-8")
            control_plane = json.dumps({"plan": plan, "report": report, "checkpoint": json.loads(checkpoint)}).lower()
            for forbidden in (
                str(ROOT).lower(), str(external).lower(), "prompt", "response", "credential", "token",
                "git:push", "github:pull_request", "publish", "external:write", "data:transfer", "spend",
                "requested_model", "actual_model",
            ):
                self.assertNotIn(forbidden, control_plane)

            resumed = executor.Executor(
                request,
                plan,
                [capability],
                bindings,
                handles,
                store=store,
                clock=lambda: at,
            ).execute()
            self.assertEqual(resumed["status"], "COMPLETED")
            self.assertEqual(len(resumed["attempts"]), 1)


if __name__ == "__main__":
    unittest.main()
