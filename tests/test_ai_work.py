from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "foundation" / "capabilities" / "ai-work" / "ai_work.py"
SPEC = importlib.util.spec_from_file_location("foundation_ai_work", MODULE_PATH)
assert SPEC and SPEC.loader
ai_work = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ai_work)

AT = datetime(2026, 9, 7, 12, 0, tzinfo=timezone.utc)


def request(**updates: object) -> dict[str, object]:
    value: dict[str, object] = {
        "schema_version": 1,
        "contract": "foundation-ai-work/v1",
        "work_id": "work-1",
        "task_class": "software.validate",
        "data_class": "INTERNAL",
        "risk": "LOW",
        "effects": ["LOCAL_READ"],
        "input_handles": [{"handle_id": "source", "kind": "FILE", "content_sha256": "sha256:" + "a" * 64}],
        "output": {"format": "application/json", "handle": {"handle_id": "result", "kind": "EPHEMERAL"}},
        "quality": {"minimum_success_probability": 0.5},
        "required_capabilities": ["source.validate"],
        "allowed_execution_boundaries": ["PROCESS", "HOST"],
        "authorization": {
            "granted_authorities": ["filesystem:read"],
            "remote_data_classes": [],
            "allow_local_adapter_synthesis": False,
        },
        "limits": {"max_cost_usd": 1, "max_network_mb": 0, "max_ram_mb": 1024},
        "validation": {"required_capabilities": [], "independent_required": False, "allow_human": True},
    }
    value.update(updates)
    return value


def capability(capability_id: str, **updates: object) -> dict[str, object]:
    value: dict[str, object] = {
        "schema_version": 1,
        "contract": "foundation-ai-work/v1",
        "capability_id": capability_id,
        "kind": "DETERMINISTIC_TOOL",
        "protocol": "foundation-ai-adapter-jsonl/v1",
        "execution_boundary": "PROCESS",
        "required_authorities": ["filesystem:read"],
        "health": {"state": "HEALTHY", "checked_at": "2026-09-07T11:59:00Z", "expires_at": "2026-09-07T12:05:00Z"},
        "functions": ["source.validate"],
        "data_classes_allowed": ["PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"],
        "deterministic": True,
        "provenance": {"source": "test-fixture", "observed_at": "2026-09-07T11:59:00Z"},
        "quality": {"provenance": "CONFIGURED", "predicted_success": 1, "observations": 0},
        "resources": {"network_mb": 0, "ram_mb": 32},
        "cost_model": {"provenance": "CONFIGURED", "currency": "USD", "estimated_cost": 0},
    }
    value.update(updates)
    return value


class AIWorkPlannerTests(unittest.TestCase):
    def test_deterministic_capability_is_preferred_to_a_model(self) -> None:
        model = capability(
            "model",
            kind="MODEL",
            deterministic=False,
            execution_boundary="HOST",
            cost_model={"provenance": "CONFIGURED", "currency": "USD", "estimated_cost": 0},
        )
        result = ai_work.plan(request(), [model, capability("deterministic")], at=AT)
        self.assertEqual(result["status"], "EXECUTABLE")
        self.assertEqual(result["steps"][0]["capability_id"], "deterministic")
        self.assertEqual(result["steps"][0]["alternatives"], ["model"])

    def test_omitted_execution_extension_preserves_v1_descriptor_shape(self) -> None:
        normalized = ai_work.validate_capability(capability("legacy"))
        self.assertNotIn("execution", normalized)
        extended = capability("extended", execution={})
        self.assertEqual(
            ai_work.validate_capability(extended)["execution"],
            {"idempotency": "NONE", "resume": "RESTART"},
        )

    def test_expired_and_failed_entries_are_isolated(self) -> None:
        expired = capability("expired")
        expired["health"] = {"state": "HEALTHY", "checked_at": "2026-09-07T11:00:00Z", "expires_at": "2026-09-07T11:30:00Z"}
        unavailable = capability("down")
        unavailable["health"] = {"state": "UNAVAILABLE", "checked_at": "2026-09-07T11:59:00Z", "expires_at": "2026-09-07T12:05:00Z"}
        result = ai_work.plan(request(), [expired, unavailable, capability("healthy")], at=AT)
        self.assertEqual(result["status"], "EXECUTABLE")
        self.assertEqual(result["steps"][0]["capability_id"], "healthy")

    def test_malformed_and_duplicate_descriptors_are_isolated(self) -> None:
        result = ai_work.plan(request(), [{"capability_id": "broken"}, capability("duplicate"), capability("duplicate"), capability("healthy")], at=AT)
        self.assertEqual(result["status"], "EXECUTABLE")
        self.assertEqual(result["steps"][0]["capability_id"], "healthy")
        excluded = result["constraints"]["excluded_descriptors"]
        self.assertIn({"capability_id": "broken", "reason_code": "INVALID_DESCRIPTOR"}, excluded)
        self.assertIn({"capability_id": "duplicate", "reason_code": "DUPLICATE_CAPABILITY_ID"}, excluded)

    def test_no_runtime_yields_truthful_manual_status(self) -> None:
        result = ai_work.plan(request(), [], at=AT)
        self.assertEqual(result["status"], "MANUAL_REQUIRED")
        self.assertEqual(result["steps"], [])
        self.assertIn("REQUIRED_CAPABILITY_UNAVAILABLE", result["reason_codes"])

    def test_no_runtime_without_human_fallback_is_unavailable(self) -> None:
        validation = {"required_capabilities": [], "independent_required": False, "allow_human": False}
        result = ai_work.plan(request(validation=validation), [], at=AT)
        self.assertEqual(result["status"], "UNAVAILABLE")

    def test_remote_nonpublic_processing_fails_closed(self) -> None:
        remote = capability("remote", execution_boundary="REMOTE", resources={"network_mb": 0, "ram_mb": 32})
        result = ai_work.plan(request(allowed_execution_boundaries=["REMOTE"]), [remote], at=AT)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("REMOTE_DATA_NOT_AUTHORIZED", result["reason_codes"])

    def test_component_does_not_grant_missing_effect_authority(self) -> None:
        result = ai_work.plan(request(effects=["LOCAL_WRITE"]), [capability("writer")], at=AT)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("AUTHORITY_MISSING:filesystem:write", result["reason_codes"])

    def test_unknown_resource_or_cost_cannot_cross_hard_limit(self) -> None:
        unknown = capability("unknown", resources={"network_mb": 0}, cost_model={"provenance": "UNKNOWN"})
        result = ai_work.plan(request(), [unknown], at=AT)
        self.assertEqual(result["status"], "MANUAL_REQUIRED")

    def test_validator_becomes_a_dependent_step(self) -> None:
        validator = capability("validator", kind="VALIDATOR", functions=["tests.run"])
        validation = {"required_capabilities": ["tests.run"], "independent_required": True, "allow_human": False}
        result = ai_work.plan(request(validation=validation), [capability("worker"), validator], at=AT)
        self.assertEqual(result["status"], "EXECUTABLE")
        self.assertEqual([step["step_id"] for step in result["steps"]], ["work", "validate"])
        self.assertEqual(result["steps"][1]["depends_on"], ["work"])

    def test_independent_validation_cannot_reuse_the_work_capability(self) -> None:
        both = capability("same", kind="VALIDATOR", functions=["source.validate", "tests.run"])
        validation = {"required_capabilities": ["tests.run"], "independent_required": True, "allow_human": False}
        result = ai_work.plan(request(validation=validation), [both], at=AT)
        self.assertEqual(result["status"], "UNAVAILABLE")
        self.assertIn("INDEPENDENT_VALIDATION_UNAVAILABLE", result["reason_codes"])

    def test_risk_effects_create_one_grouped_checkpoint(self) -> None:
        auth = {
            "granted_authorities": ["filesystem:read", "publish"],
            "remote_data_classes": [],
            "allow_local_adapter_synthesis": False,
        }
        result = ai_work.plan(request(risk="HIGH", effects=["PUBLISH"], authorization=auth), [capability("worker")], at=AT)
        self.assertEqual(result["status"], "MANUAL_REQUIRED")
        self.assertEqual(len(result["approval_points"]), 1)
        self.assertEqual(set(result["approval_points"][0]["reasons"]), {"HIGH_IMPACT", "PUBLISH"})

    def test_gap_synthesis_is_authority_gated_and_external(self) -> None:
        denied = ai_work.gap_report(request(), [], at=AT)
        self.assertIsNone(denied["local_remedy"])
        allowed_request = copy.deepcopy(request())
        allowed_request["authorization"]["allow_local_adapter_synthesis"] = True
        allowed = ai_work.gap_report(allowed_request, [], at=AT)
        self.assertEqual(allowed["local_remedy"]["network_default"], "DENY")
        self.assertEqual(allowed["local_remedy"]["repository_write_default"], "DENY")
        self.assertTrue(allowed["local_remedy"]["conformance_required"])

    def test_control_plane_contains_handles_not_payload_content(self) -> None:
        result = ai_work.plan(request(), [capability("worker")], at=AT)
        serialized = json.dumps(result)
        self.assertIn("source", serialized)
        self.assertNotIn("prompt", serialized.lower())
        self.assertNotIn("response", serialized.lower())
        self.assertNotIn(str(ROOT), serialized)

    def test_cli_emits_structured_plan_and_invalid_input_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            request_path = root / "request.json"
            catalog_path = root / "catalog.json"
            request_path.write_text(json.dumps(request()), encoding="utf-8")
            catalog_path.write_text(json.dumps({"capabilities": [capability("worker")]}), encoding="utf-8")
            success = subprocess.run(
                [sys.executable, str(MODULE_PATH), "plan", "--request", str(request_path), "--capabilities", str(catalog_path), "--at", "2026-09-07T12:00:00Z"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(success.returncode, 0, success.stderr)
            self.assertEqual(json.loads(success.stdout)["status"], "EXECUTABLE")
            request_path.write_text("{}", encoding="utf-8")
            failure = subprocess.run(
                [sys.executable, str(MODULE_PATH), "plan", "--request", str(request_path), "--capabilities", str(catalog_path)],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(failure.returncode, 2)
            self.assertEqual(json.loads(failure.stderr)["status"], "BLOCKED")

    def test_public_schemas_are_runtime_neutral_and_strict(self) -> None:
        names = [
            "ai-work-request.schema.json", "capability-descriptor.schema.json", "execution-plan.schema.json",
            "execution-report.schema.json", "validation-evidence.schema.json", "gap-report.schema.json",
            "provision-plan.schema.json", "execution-checkpoint.schema.json", "approval-receipt.schema.json",
        ]
        for name in names:
            schema = json.loads((ROOT / "foundation" / "schemas" / name).read_text(encoding="utf-8"))
            self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
            self.assertFalse(schema["additionalProperties"])
            self.assertNotIn("ollama", json.dumps(schema).lower())
            self.assertNotIn("openai", json.dumps(schema).lower())


if __name__ == "__main__":
    unittest.main()
