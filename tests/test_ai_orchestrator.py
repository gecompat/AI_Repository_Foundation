from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
CAPABILITY = ROOT / "foundation" / "capabilities" / "ai-orchestrator"
ROUTER = ROOT / "foundation" / "capabilities" / "model-router"
sys.path.insert(0, str(ROUTER))
sys.path.insert(0, str(CAPABILITY))
SPEC = importlib.util.spec_from_file_location("ai_orchestrator", CAPABILITY / "ai_orchestrator.py")
ai_orchestrator = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules["ai_orchestrator"] = ai_orchestrator
SPEC.loader.exec_module(ai_orchestrator)
import router_v2  # noqa: E402
import orchestrator_mcp  # noqa: E402


AT = datetime(2026, 9, 8, 12, 0, tzinfo=timezone.utc)


def profile(cost: float = 0.0) -> dict:
    return {
        "availability": "AVAILABLE",
        "assessment": "ASSESSED",
        "capabilities": ["text"],
        "context_window": 8192,
        "quality_prior": {"*": 0.9},
        "quality_provenance": "CONFIGURED",
        "supported_tiers": ["ECONOMICAL", "BALANCED", "FRONTIER"],
        "reasoning_efforts": ["low", "medium", "high"],
        "latency_seconds_prior": 0.1,
        "resource_estimate": {},
        "resource_provenance": "CONFIGURED",
        "pricing": {"currency": "USD", "unit_tokens": 1000000, "base": {"input": cost, "cached_input": cost, "output": cost}, "schedules": []},
    }


def evidence(root: Path, *, aliases: list[dict] | None = None, records: list[dict] | None = None) -> Path:
    source = {"kind": "PROJECT_CONFIGURATION", "locator": "test:evidence", "content_sha256": "sha256:" + "a" * 64}
    value = {
        "schema_version": 1,
        "contract": "foundation-model-runtime-evidence/v1",
        "updated_at": "2026-09-08T11:00:00Z",
        "records": records if records is not None else [
            {"connection_id": "one", "model_id": "alpha", "profile": profile(), "source": source, "observed_at": "2026-09-08T11:00:00Z", "valid_until": "2026-09-09T11:00:00Z"}
        ],
        "aliases": aliases or [],
    }
    path = root / "evidence.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def request(root: Path, **updates: object) -> dict:
    router = {
        "schema_version": 2,
        "contract": "foundation-model-router/v2",
        "tier": "BALANCED",
        "task_class": "test",
        "data_class": "PUBLIC",
        "context_tokens": 100,
        "expected_output_tokens": 20,
        "required_capabilities": ["text"],
        "allow_remote": False,
        "allowed_execution_boundaries": ["HOST"],
        "remote_data_classes": [],
        "resource_limits": {},
        "max_fallbacks": 2,
        "failure_cost_usd": 10,
        "at": "2026-09-08T12:00:00Z",
    }
    value = {
        "schema_version": 1,
        "contract": "foundation-ai-orchestration/v1",
        "orchestration_id": "test-run",
        "router_request": router,
        "input_handle": str(root / "input" / "prompt.txt"),
        "output_handle": str(root / "output" / "result.json"),
        "remote_authorized": False,
        "max_attempts": 3,
        "validation": {"mode": "JSON_DOCUMENT"},
    }
    value.update(updates)
    return value


class FakeRuntime:
    failures: set[str] = set()
    actual_models: dict[str, str | None] = {}
    connections = ["one"]
    calls = 0
    catalog_calls = 0
    failure_classes: dict[str, str] = {}

    class ConfigurationStore:
        def __init__(self, path: Path | None = None) -> None:
            self.path = path

        def connection_statuses(self) -> list[dict]:
            return [{"connection_id": item, "status": "CONFIGURED", "reason_code": None} for item in FakeRuntime.connections]

        def load_connection(self, connection_id: str) -> dict:
            return {"connection_id": connection_id}

    @staticmethod
    def execute_adapter(connection: dict, operation: str, arguments: dict) -> dict:
        connection_id = connection["connection_id"]
        if operation == "catalog":
            FakeRuntime.catalog_calls += 1
            model = "alpha" if connection_id == "one" else "beta"
            return {"fragments": [{
                "schema_version": 2, "contract": "foundation-model-router/v2", "provider": connection_id + "-provider",
                "adapter": "test/v1", "execution_boundary": "HOST", "generated_at": "2026-09-08T11:59:00Z",
                "valid_until": "2026-09-08T13:00:00Z", "pricing_epoch": "test", "health": {
                    "state": "HEALTHY", "checked_at": "2026-09-08T11:59:00Z", "expires_at": "2026-09-08T12:30:00Z"
                }, "provenance": {"source": "test", "observed_at": "2026-09-08T11:59:00Z"}, "models": {
                    model: {"model_id": model, "availability": "AVAILABLE", "assessment": "UNASSESSED", "capabilities": ["text"],
                            "context_window": None, "quality_prior": {"*": 0.5}, "quality_provenance": "UNKNOWN",
                            "supported_tiers": ["ECONOMICAL", "BALANCED", "FRONTIER"], "reasoning_efforts": ["low"],
                            "resource_estimate": {}, "resource_provenance": "UNKNOWN", "pricing": None}
                }
            }]}
        if connection_id in FakeRuntime.failures:
            error = RuntimeError("synthetic failure")
            error.code = "ENDPOINT_UNAVAILABLE"
            error.error_class = FakeRuntime.failure_classes.get(connection_id, "AVAILABILITY")
            raise error
        FakeRuntime.calls += 1
        output = Path(arguments["output_path"])
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text('{"message":"kept outside report"}\n', encoding="utf-8")
        model = arguments["model"]
        actual = FakeRuntime.actual_models.get(connection_id, model)
        return {"status": "COMPLETED", "requested_model": model, "actual_model": actual,
                "dispatch_status": "ACTUAL_MODEL_ATTESTED" if actual == model else "ACTUAL_MODEL_DIFFERS",
                "output_sha256": "sha256:" + "b" * 64, "output_bytes": output.stat().st_size}


class AIOrchestratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "input").mkdir()
        (self.root / "input" / "prompt.txt").write_text("secret payload marker", encoding="utf-8")
        FakeRuntime.failures = set()
        FakeRuntime.actual_models = {}
        FakeRuntime.connections = ["one"]
        FakeRuntime.calls = 0
        FakeRuntime.catalog_calls = 0
        FakeRuntime.failure_classes = {}

    def tearDown(self) -> None:
        self.temp.cleanup()

    def orchestrate(self, *, execute: bool, evidence_path: Path | None = None, value: dict | None = None) -> dict:
        with patch.object(ai_orchestrator, "_dependencies", return_value=(router_v2, FakeRuntime)):
            return ai_orchestrator.plan_or_execute(
                value or request(self.root), execute=execute, state_root=self.root / "state",
                evidence_path=evidence_path or evidence(self.root), at=AT,
            )

    def test_plan_and_execute_complete_without_payload_in_report(self) -> None:
        planned = self.orchestrate(execute=False)
        self.assertEqual(planned["status"], "PLANNED")
        self.assertEqual(planned["route"]["connection_id"], "one")
        completed = self.orchestrate(execute=True)
        self.assertEqual(completed["status"], "COMPLETED")
        self.assertEqual(completed["validation_status"], "PASSED")
        self.assertNotIn("secret payload marker", json.dumps(completed))
        self.assertNotIn("kept outside report", json.dumps(completed))
        repeated = self.orchestrate(execute=True)
        self.assertEqual(repeated, completed)
        self.assertEqual(FakeRuntime.calls, 1)
        self.assertEqual(FakeRuntime.catalog_calls, 2)

    def test_missing_evidence_is_truthful_manual_status(self) -> None:
        result = self.orchestrate(execute=True, evidence_path=self.root / "missing.json")
        self.assertEqual(result["status"], "MANUAL_REQUIRED")
        self.assertEqual(result["router_status"], "NO_ROUTE")
        self.assertIn("ADD_FRESH_SOURCE_BACKED_MODEL_EVIDENCE", result["remaining_actions"])

    def test_one_invalid_evidence_record_does_not_hide_a_valid_record(self) -> None:
        valid = json.loads(evidence(self.root).read_text(encoding="utf-8"))["records"][0]
        invalid = {**valid, "connection_id": "broken", "profile": {"quality_prior": "invented"}}
        result = self.orchestrate(execute=False, evidence_path=evidence(self.root, records=[invalid, valid]))
        self.assertEqual(result["status"], "PLANNED")

    def test_actual_model_mismatch_needs_strong_fresh_alias(self) -> None:
        FakeRuntime.actual_models = {"one": "alpha-real"}
        denied = self.orchestrate(execute=True)
        self.assertEqual(denied["status"], "MANUAL_REQUIRED")
        source = {"kind": "PROVIDER_DOCUMENTATION", "locator": "https://provider.invalid/models", "content_sha256": "sha256:" + "c" * 64}
        alias = {"connection_id": "one", "requested_model": "alpha", "actual_model": "alpha-real", "evidence_kind": "PROVIDER_DOCUMENTATION", "source": source, "observed_at": "2026-09-08T11:00:00Z", "valid_until": "2026-09-09T11:00:00Z"}
        accepted_request = request(self.root, orchestration_id="alias-accepted")
        accepted = self.orchestrate(execute=True, evidence_path=evidence(self.root, aliases=[alias]), value=accepted_request)
        self.assertEqual(accepted["status"], "COMPLETED")
        self.assertEqual(accepted["attempts"][0]["dispatch_status"], "ALIAS_ATTESTED")

    def test_failed_primary_uses_distinct_router_fallback(self) -> None:
        FakeRuntime.connections = ["one", "two"]
        FakeRuntime.failures = {"one"}
        source = {"kind": "PROJECT_CONFIGURATION", "locator": "test:evidence", "content_sha256": "sha256:" + "d" * 64}
        records = [
            {"connection_id": "one", "model_id": "alpha", "profile": profile(0), "source": source, "observed_at": "2026-09-08T11:00:00Z", "valid_until": "2026-09-09T11:00:00Z"},
            {"connection_id": "two", "model_id": "beta", "profile": profile(1), "source": source, "observed_at": "2026-09-08T11:00:00Z", "valid_until": "2026-09-09T11:00:00Z"},
        ]
        result = self.orchestrate(execute=True, evidence_path=evidence(self.root, records=records))
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual([row["connection_id"] for row in result["attempts"]], ["one", "two"])

    def test_timeout_is_ambiguous_and_is_not_retried_or_replayed(self) -> None:
        FakeRuntime.connections = ["one", "two"]
        FakeRuntime.failures = {"one"}
        FakeRuntime.failure_classes = {"one": "TIMEOUT"}
        source = {"kind": "PROJECT_CONFIGURATION", "locator": "test:evidence", "content_sha256": "sha256:" + "e" * 64}
        records = [
            {"connection_id": "one", "model_id": "alpha", "profile": profile(0), "source": source, "observed_at": "2026-09-08T11:00:00Z", "valid_until": "2026-09-09T11:00:00Z"},
            {"connection_id": "two", "model_id": "beta", "profile": profile(1), "source": source, "observed_at": "2026-09-08T11:00:00Z", "valid_until": "2026-09-09T11:00:00Z"},
        ]
        evidence_path = evidence(self.root, records=records)
        first = self.orchestrate(execute=True, evidence_path=evidence_path)
        self.assertEqual(first["status"], "MANUAL_REQUIRED")
        self.assertEqual([row["connection_id"] for row in first["attempts"]], ["one"])
        second = self.orchestrate(execute=True, evidence_path=evidence_path)
        self.assertIn("AMBIGUOUS_PRIOR_INVOCATION", second["reason_codes"])

    def test_local_tier_never_invokes_model(self) -> None:
        value = request(self.root)
        value["router_request"]["tier"] = "LOCAL"
        result = self.orchestrate(execute=True, value=value)
        self.assertEqual(result["router_status"], "LOCAL_ONLY")
        self.assertEqual(result["attempts"], [])

    def test_refresh_attempts_at_most_daily_and_preserves_last_known_good(self) -> None:
        producer = self.root / "producer.py"
        evidence_value = json.loads(evidence(self.root).read_text(encoding="utf-8"))
        producer.write_text("import json\nprint(" + repr(json.dumps(evidence_value)) + ")\n", encoding="utf-8")
        sources = self.root / "sources.json"
        sources.write_text(json.dumps({"schema_version": 1, "contract": "foundation-model-evidence-sources/v1", "sources": [{
            "source_id": "daily", "argv": [sys.executable, str(producer)], "environment_allowlist": [],
            "timeout_seconds": 5, "minimum_refresh_seconds": 86400
        }]}), encoding="utf-8")
        first = ai_orchestrator.refresh_evidence(sources, self.root / "refresh", at=AT)
        self.assertEqual(first["records"][0]["status"], "REFRESHED")
        producer.unlink()
        second = ai_orchestrator.refresh_evidence(sources, self.root / "refresh", at=AT)
        self.assertEqual(second["records"][0]["reason_code"], "REFRESH_RATE_LIMIT")
        self.assertTrue(Path(first["evidence_path"]).is_file())

    def test_public_contract_schemas_validate_reports_and_reject_payload_fields(self) -> None:
        schemas = ROOT / "foundation" / "schemas"
        report_schema = json.loads((schemas / "ai-orchestration-report.schema.json").read_text(encoding="utf-8"))
        report = self.orchestrate(execute=True)
        self.assertEqual(set(report), set(report_schema["required"]))
        self.assertFalse(report_schema["additionalProperties"])
        self.assertNotIn("prompt", report_schema["properties"])
        self.assertNotIn("response", report_schema["properties"])
        for name in ("ai-orchestration-request.schema.json", "model-runtime-evidence.schema.json", "model-evidence-sources.schema.json"):
            schema = json.loads((schemas / name).read_text(encoding="utf-8"))
            self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")

    def test_mcp_starts_unconfigured_and_exposes_end_to_end_tools(self) -> None:
        server = orchestrator_mcp.Server(config=self.root / "missing-config.json", state_root=self.root / "mcp-state", evidence=None, evidence_sources=None)
        initialized = orchestrator_mcp.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}}, server)
        self.assertEqual(initialized["result"]["serverInfo"]["name"], "foundation-ai-orchestrator")
        listed = orchestrator_mcp.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, server)
        self.assertEqual({item["name"] for item in listed["result"]["tools"]}, {"orchestration_status", "orchestration_plan", "orchestration_execute", "orchestration_refresh_evidence"})
        status = server.call("orchestration_status", {})["structuredContent"]
        self.assertEqual(status["status"], "CONFIGURATION_REQUIRED")


if __name__ == "__main__":
    unittest.main()
