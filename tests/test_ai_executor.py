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
    spec.loader.exec_module(module)
    return module


ai_work = load_module("foundation_ai_work_for_executor_tests", ROOT / "foundation" / "capabilities" / "ai-work" / "ai_work.py")
executor = load_module("foundation_ai_executor_tests", ROOT / "foundation" / "capabilities" / "ai-executor" / "ai_executor.py")
AT = datetime(2026, 9, 7, 12, 0, tzinfo=timezone.utc)
HASH_A = "sha256:" + "a" * 64
RESULT_BODY = b"result"
EVIDENCE_BODY = b"evidence"
HASH_B = "sha256:" + hashlib.sha256(RESULT_BODY).hexdigest()
HASH_C = "sha256:" + hashlib.sha256(EVIDENCE_BODY).hexdigest()


def request(**updates: object) -> dict[str, object]:
    value: dict[str, object] = {
        "schema_version": 1,
        "contract": "foundation-ai-work/v1",
        "work_id": "executor-work",
        "task_class": "software.transform",
        "data_class": "INTERNAL",
        "risk": "LOW",
        "effects": ["LOCAL_READ"],
        "input_handles": [{"handle_id": "source", "kind": "FILE", "content_sha256": HASH_A}],
        "output": {"format": "application/json", "handle": {"handle_id": "result", "kind": "EPHEMERAL"}},
        "quality": {},
        "required_capabilities": ["source.transform"],
        "allowed_execution_boundaries": ["PROCESS"],
        "authorization": {
            "granted_authorities": ["filesystem:read"],
            "remote_data_classes": [],
            "allow_local_adapter_synthesis": False,
        },
        "limits": {"max_cost_usd": 1, "max_network_mb": 0, "max_ram_mb": 100, "max_attempts": 4},
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
        "functions": ["source.transform"],
        "data_classes_allowed": ["INTERNAL"],
        "deterministic": True,
        "provenance": {"source": "test-fixture", "observed_at": "2026-09-07T11:59:00Z"},
        "quality": {"provenance": "CONFIGURED", "predicted_success": 1, "observations": 0},
        "resources": {"network_mb": 0, "ram_mb": 40},
        "cost_model": {"provenance": "CONFIGURED", "currency": "USD", "estimated_cost": 0.1},
    }
    value.update(updates)
    return value


def bindings(*ids: str) -> dict[str, object]:
    return {
        "bindings": {
            capability_id: {
                "argv": [str(Path(sys.executable).resolve())],
                "environment_allowlist": [],
                "timeout_seconds": 10,
                "model": capability_id,
            }
            for capability_id in ids
        }
    }


class AIExecutorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.state = executor.CheckpointStore(self.root / "state")
        self.handles = {
            "handles": {
                "source": str(self.root / "source.json"),
                "result": str(self.root / "result.json"),
                "executor-work:validation-evidence": str(self.root / "evidence.json"),
            }
        }

    def make_executor(self, request_value, capabilities, invoke, *, approvals=None):
        plan = ai_work.plan(request_value, capabilities, at=AT)
        return executor.Executor(
            request_value,
            plan,
            capabilities,
            bindings(*(item["capability_id"] for item in capabilities)),
            self.handles,
            store=self.state,
            approvals_raw=approvals,
            clock=lambda: AT,
            invoke=invoke,
        ), plan

    @staticmethod
    def success(_binding, frame):
        Path(frame["arguments"]["output_path"]).write_bytes(RESULT_BODY)
        return {"output_sha256": HASH_B, "actual_cost_usd": 0.1, "resource_usage": {"network_mb": 0, "ram_mb": 40}}

    def approval(self, plan, *, authority="approve:risk-boundary"):
        point = plan["approval_points"][0]
        return {
            "approvals": [{
                "schema_version": 1,
                "contract": "foundation-ai-approval/v1",
                "receipt_id": "approval-1",
                "plan_id": plan["plan_id"],
                "approval_key": executor.digest(point),
                "scope_sha256": executor.digest(plan),
                "authority": authority,
                "approved_at": executor.isoformat(AT - timedelta(minutes=1)),
                "expires_at": executor.isoformat(AT + timedelta(minutes=2)),
            }]
        }

    def test_executes_once_and_resume_returns_completed_report(self) -> None:
        calls = []

        def invoke(binding, frame):
            calls.append((binding, frame))
            return self.success(binding, frame)

        instance, plan = self.make_executor(request(), [capability("worker")], invoke)
        self.assertEqual(instance.execute()["status"], "COMPLETED")
        resumed, _ = self.make_executor(request(), [capability("worker")], invoke)
        self.assertEqual(resumed.execute()["status"], "COMPLETED")
        self.assertEqual(len(calls), 1)
        checkpoint = self.state.path(plan["plan_id"]).read_text(encoding="utf-8")
        self.assertNotIn(str(self.root), checkpoint)
        self.assertNotIn("prompt", checkpoint.lower())

    def test_failed_primary_uses_distinct_fallback_once(self) -> None:
        calls = []

        def invoke(binding, frame):
            calls.append(binding["model"])
            if binding["model"] == "a-primary":
                raise executor.ExecutionError("FAILED", "bounded", error_class="AVAILABILITY")
            return self.success(binding, frame)

        capabilities = [capability("a-primary"), capability("b-fallback")]
        instance, _ = self.make_executor(request(), capabilities, invoke)
        report = instance.execute()
        self.assertEqual(report["status"], "COMPLETED")
        self.assertEqual(calls, ["a-primary", "b-fallback"])

    def test_grouped_approval_is_exact_scoped_and_authority_bound(self) -> None:
        request_value = request(
            effects=["EXTERNAL_WRITE"],
            authorization={
                "granted_authorities": ["filesystem:read", "external:write"],
                "remote_data_classes": [],
                "allow_local_adapter_synthesis": False,
            },
        )
        capabilities = [capability("worker")]
        denied, plan = self.make_executor(request_value, capabilities, self.success)
        self.assertEqual(denied.execute()["status"], "MANUAL_REQUIRED")
        with self.assertRaisesRegex(executor.ExecutionError, "authority"):
            self.make_executor(request_value, capabilities, self.success, approvals=self.approval(plan, authority="someone-else"))
        allowed, _ = self.make_executor(request_value, capabilities, self.success, approvals=self.approval(plan))
        self.assertEqual(allowed.execute()["status"], "COMPLETED")

    def test_ambiguous_external_operation_is_not_blindly_repeated(self) -> None:
        request_value = request(
            effects=["EXTERNAL_WRITE"],
            authorization={
                "granted_authorities": ["filesystem:read", "external:write"],
                "remote_data_classes": [],
                "allow_local_adapter_synthesis": False,
            },
        )
        calls = []
        capabilities = [capability("worker"), capability("fallback")]
        instance, plan = self.make_executor(request_value, capabilities, lambda binding, frame: calls.append(frame))
        state = instance._initial_state(AT)
        attempt = instance._new_attempt(plan["steps"][0], "worker", 1, AT)
        attempt["status"] = "IN_PROGRESS"
        state["attempts"].append(attempt)
        self.state.save(state)
        report = instance.execute()
        self.assertEqual(report["status"], "MANUAL_REQUIRED")
        self.assertIn("AMBIGUOUS_EXTERNAL_OUTCOME", report["reason_codes"])
        self.assertEqual(calls, [])
        resumed, _ = self.make_executor(request_value, capabilities, lambda binding, frame: calls.append(frame))
        self.assertEqual(resumed.execute()["status"], "MANUAL_REQUIRED")
        self.assertEqual(calls, [])

    def test_idempotent_external_operation_replays_same_operation_key(self) -> None:
        request_value = request(
            effects=["EXTERNAL_WRITE"],
            authorization={
                "granted_authorities": ["filesystem:read", "external:write"],
                "remote_data_classes": [],
                "allow_local_adapter_synthesis": False,
            },
        )
        cap = capability("worker", execution={"idempotency": "IDEMPOTENT_REPLAY", "resume": "RESTART"})
        plan = ai_work.plan(request_value, [cap], at=AT)
        calls = []

        def invoke(binding, frame):
            calls.append(frame["arguments"]["operation_id"])
            return self.success(binding, frame)

        instance, _ = self.make_executor(request_value, [cap], invoke, approvals=self.approval(plan))
        state = instance._initial_state(AT)
        attempt = instance._new_attempt(plan["steps"][0], "worker", 1, AT)
        attempt["status"] = "IN_PROGRESS"
        state["attempts"].append(attempt)
        self.state.save(state)
        self.assertEqual(instance.execute()["status"], "COMPLETED")
        self.assertEqual(calls, [attempt["operation_key"]])

    def test_validation_evidence_is_required_and_peak_memory_is_not_summed(self) -> None:
        request_value = request(
            validation={"required_capabilities": ["tests.run"], "independent_required": True, "allow_human": False}
        )
        validator = capability("validator", kind="VALIDATOR", functions=["tests.run"], resources={"network_mb": 0, "ram_mb": 80})
        worker = capability("worker", resources={"network_mb": 0, "ram_mb": 80})

        def invoke(binding, frame):
            if binding["model"] == "worker":
                Path(frame["arguments"]["output_path"]).write_bytes(RESULT_BODY)
                return {"output_sha256": HASH_B, "actual_cost_usd": 0.1, "resource_usage": {"network_mb": 0, "ram_mb": 80}}
            Path(frame["arguments"]["output_path"]).write_bytes(EVIDENCE_BODY)
            return {
                "output_sha256": HASH_C,
                "actual_cost_usd": 0.1,
                "resource_usage": {"network_mb": 0, "ram_mb": 80},
                "validation_evidence": {
                    "schema_version": 1,
                    "contract": "foundation-ai-work/v1",
                    "evidence_id": "evidence-1",
                    "subject_sha256": HASH_B,
                    "scope": "tests.run",
                    "method": "DETERMINISTIC",
                    "producer_capability_id": "validator",
                    "independent": True,
                    "result": "PASSED",
                    "provenance": ["test-fixture"],
                    "observed_at": executor.isoformat(AT),
                },
            }

        instance, _ = self.make_executor(request_value, [worker, validator], invoke)
        report = instance.execute()
        self.assertEqual(report["status"], "COMPLETED")
        self.assertEqual(report["validation_status"], "PASSED")
        self.assertEqual(report["resource_usage"]["ram_mb"], 80)

    def test_actual_spend_overrun_is_reported(self) -> None:
        def expensive(_binding, _frame):
            Path(_frame["arguments"]["output_path"]).write_bytes(RESULT_BODY)
            return {"output_sha256": HASH_B, "actual_cost_usd": 2, "resource_usage": {"network_mb": 0, "ram_mb": 40}}

        instance, _ = self.make_executor(request(), [capability("worker")], expensive)
        report = instance.execute()
        self.assertEqual(report["status"], "BLOCKED")
        self.assertIn("ACTUAL_COST_LIMIT_EXCEEDED", report["reason_codes"])
        self.assertEqual(report["resource_usage"]["cost_usd"], 2)
        resumed, _ = self.make_executor(request(), [capability("worker")], expensive)
        self.assertEqual(resumed.execute()["status"], "BLOCKED")

    def test_payload_or_secret_fields_from_adapter_are_rejected(self) -> None:
        calls = []

        def leaking(_binding, frame):
            calls.append(frame)
            return {"output_sha256": HASH_B, "raw_response": "must-not-enter-control-plane"}

        instance, _ = self.make_executor(request(), [capability("worker")], leaking)
        report = instance.execute()
        self.assertEqual(report["status"], "UNAVAILABLE")
        self.assertEqual(report["attempts"][0]["error_class"], "PROTOCOL")
        self.assertNotIn("must-not-enter-control-plane", json.dumps(report))

    def test_corrupt_checkpoint_and_repository_state_path_fail_closed(self) -> None:
        instance, plan = self.make_executor(request(), [capability("worker")], self.success)
        state = instance._initial_state(AT)
        self.state.save(state)
        path = self.state.path(plan["plan_id"])
        value = json.loads(path.read_text(encoding="utf-8"))
        value["state"] = "COMPLETED"
        path.write_text(json.dumps(value), encoding="utf-8")
        with self.assertRaises(executor.ExecutionError) as raised:
            instance.execute()
        self.assertEqual(raised.exception.code, "CHECKPOINT_INTEGRITY_FAILURE")
        with self.assertRaises(executor.ExecutionError) as repository_state:
            executor.CheckpointStore(ROOT / ".runtime")
        self.assertEqual(repository_state.exception.code, "RUNTIME_STATE_IN_VERSION_CONTROL")

    def test_scoped_cancellation_stops_before_invocation(self) -> None:
        calls = []
        instance, plan = self.make_executor(request(), [capability("worker")], lambda binding, frame: calls.append(frame))
        self.state.request_cancel(plan, AT)
        report = instance.execute()
        self.assertEqual(report["status"], "CANCELLED")
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
