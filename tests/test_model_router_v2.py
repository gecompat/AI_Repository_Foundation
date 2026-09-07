from __future__ import annotations

import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITY = ROOT / "foundation" / "capabilities" / "model-router"
sys.path.insert(0, str(CAPABILITY))
import model_router  # noqa: E402
import router_v2  # noqa: E402

AT = datetime(2026, 9, 7, 12, 0, tzinfo=timezone.utc)


def rates() -> dict:
    return {"currency": "USD", "unit_tokens": 1_000_000, "base": {"input": 0, "cached_input": 0, "output": 0}, "schedules": []}


def model(model_id: str, *, quality: float = 0.9, ram_mb: int = 256) -> dict:
    return {
        "model_id": model_id,
        "availability": "AVAILABLE",
        "assessment": "ASSESSED",
        "capabilities": ["text", "tools"],
        "context_window": 16_000,
        "quality_prior": {"*": quality},
        "quality_provenance": "CONFIGURED",
        "supported_tiers": ["ECONOMICAL", "BALANCED", "FRONTIER"],
        "reasoning_efforts": ["low", "medium", "high"],
        "latency_seconds_prior": 0.1,
        "resource_estimate": {"ram_mb": ram_mb, "network_mb": 0, "cpu_seconds": 1},
        "resource_provenance": "CONFIGURED",
        "pricing": rates(),
    }


def with_resource_cost(value: dict, amount: float, source: str = "project-meter") -> dict:
    value["resource_cost"] = {
        "currency": "USD",
        "estimated_cost": amount,
        "provenance": "CONFIGURED",
        "evidence_id": "resource-cost-test",
        "source": source,
        "observed_at": "2026-09-07T00:00:00Z",
        "valid_until": "2026-09-08T00:00:00Z",
    }
    return value


def fragment(provider: str, boundary: str, **updates: object) -> dict:
    value: dict[str, object] = {
        "schema_version": 2,
        "contract": "foundation-model-router/v2",
        "provider": provider,
        "adapter": "synthetic/v1",
        "execution_boundary": boundary,
        "generated_at": "2026-09-07T11:55:00Z",
        "valid_until": "2026-09-07T13:00:00Z",
        "pricing_epoch": f"sha256:{provider}",
        "health": {"state": "HEALTHY", "checked_at": "2026-09-07T11:55:00Z", "expires_at": "2026-09-07T12:10:00Z"},
        "provenance": {"source": "test-fixture", "observed_at": "2026-09-07T11:55:00Z"},
        "models": {"model": model("model")},
    }
    value.update(updates)
    return value


def request(**updates: object) -> dict:
    value: dict[str, object] = {
        "schema_version": 2,
        "contract": "foundation-model-router/v2",
        "tier": "BALANCED",
        "task_class": "coding.repository",
        "data_class": "INTERNAL",
        "context_tokens": 1000,
        "expected_output_tokens": 100,
        "required_capabilities": ["tools"],
        "allow_remote": False,
        "allowed_execution_boundaries": ["PROCESS", "HOST"],
        "remote_data_classes": [],
        "resource_limits": {"max_ram_mb": 1024, "max_network_mb": 0},
        "at": "2026-09-07T12:00:00Z",
    }
    value.update(updates)
    return value


class RouterV2Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.runtime = model_router.RuntimeStore(self.root / "runtime")
        self.fragments = router_v2.ProviderFragmentStore(self.root / "runtime")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def route(self, request_value: dict, fragments: list[dict]) -> dict:
        return router_v2.route_v2(
            request_value, fragments, runtime_store=self.runtime, fragment_store=self.fragments, at=AT
        )

    def test_host_model_keeps_model_tier_and_local_remains_deterministic(self) -> None:
        routed = self.route(request(), [fragment("host-models", "HOST")])
        self.assertEqual(routed["status"], "ROUTED")
        self.assertEqual(routed["execution_boundary"], "HOST")
        self.assertEqual(routed["v1_decision"]["route"]["model"], "model")
        local = self.route(request(tier="LOCAL"), [fragment("host-models", "HOST")])
        self.assertEqual(local["status"], "LOCAL_ONLY")
        self.assertIsNone(local["v1_decision"]["route"])

    def test_invalid_and_unavailable_fragments_do_not_block_healthy_provider(self) -> None:
        down = fragment("down", "HOST")
        down["health"] = {"state": "UNAVAILABLE", "checked_at": "2026-09-07T11:55:00Z", "expires_at": "2026-09-07T12:10:00Z"}
        result = self.route(request(), [{"provider": "broken"}, down, fragment("healthy", "HOST")])
        self.assertEqual(result["status"], "ROUTED")
        self.assertEqual(result["v1_decision"]["route"]["provider"], "healthy")
        reasons = {item["reason_code"] for item in result["catalog_fragments"]}
        self.assertIn("INVALID_FRAGMENT", reasons)
        self.assertIn("HEALTH_UNAVAILABLE", reasons)

    def test_unexpired_last_known_good_is_per_provider(self) -> None:
        first = self.route(request(), [fragment("saved", "HOST")])
        self.assertEqual(first["status"], "ROUTED")
        failed_refresh = {"provider": "saved", "bad": True}
        second = self.route(request(), [failed_refresh])
        self.assertEqual(second["status"], "ROUTED")
        self.assertTrue(any(item["source"] == "LAST_KNOWN_GOOD" for item in second["catalog_fragments"]))

    def test_privacy_boundary_and_resource_limits_fail_closed(self) -> None:
        remote_request = request(
            allow_remote=True,
            allowed_execution_boundaries=["REMOTE"],
            remote_data_classes=[],
        )
        denied = self.route(remote_request, [fragment("remote", "REMOTE")])
        self.assertEqual(denied["status"], "NO_ROUTE")
        self.assertIn("REMOTE_DATA_NOT_AUTHORIZED", denied["reason_codes"])
        oversized = fragment("large", "HOST", models={"model": model("model", ram_mb=2048)})
        limited = self.route(request(), [oversized])
        self.assertEqual(limited["status"], "NO_ROUTE")
        self.assertTrue(any("RAM_MB_LIMIT_EXCEEDED" in code for code in limited["reason_codes"]))

    def test_unknown_quality_provenance_is_not_treated_as_evidence(self) -> None:
        unknown = fragment("unknown", "HOST")
        unknown["models"]["model"]["quality_provenance"] = "UNKNOWN"
        result = self.route(request(), [unknown])
        self.assertEqual(result["status"], "NO_ROUTE")
        self.assertTrue(any("QUALITY_PROVENANCE_UNKNOWN" in code for code in result["reason_codes"]))

    def test_evidenced_resource_cost_participates_in_total_cost(self) -> None:
        expensive = fragment("a-expensive", "HOST", models={"model": with_resource_cost(model("model"), 0.2)})
        economical = fragment("z-economical", "HOST", models={"model": with_resource_cost(model("model"), 0.05)})
        result = self.route(request(), [expensive, economical])
        self.assertEqual(result["v1_decision"]["route"]["provider"], "z-economical")
        self.assertEqual(result["v1_decision"]["route"]["resource_cost_usd"], 0.05)
        self.assertEqual(result["v1_decision"]["economics"]["expected_resource_cost_usd"], 0.05)

    def test_resource_pressure_is_only_a_tie_breaker_without_money_conversion(self) -> None:
        heavy = fragment("a-heavy", "HOST", models={"model": model("model", ram_mb=900)})
        light = fragment("z-light", "HOST", models={"model": model("model", ram_mb=100)})
        result = self.route(request(), [heavy, light])
        route = result["v1_decision"]["route"]
        self.assertEqual(route["provider"], "z-light")
        self.assertEqual(route["resource_cost_usd"], 0)
        self.assertGreater(result["v1_decision"]["candidates_considered"][1]["resource_pressure"], route["resource_pressure"])

    def test_resource_limits_require_provenance(self) -> None:
        unproven = fragment("unproven", "HOST")
        unproven["models"]["model"]["resource_provenance"] = "UNKNOWN"
        result = self.route(request(), [unproven])
        self.assertEqual(result["status"], "NO_ROUTE")
        self.assertTrue(any("RESOURCE_PROVENANCE_UNKNOWN" in code for code in result["reason_codes"]))

    def test_hard_latency_limit_excludes_slow_or_unknown_models(self) -> None:
        slow = fragment("slow", "HOST")
        slow["models"]["model"]["latency_seconds_prior"] = 4
        fast = fragment("fast", "HOST")
        fast["models"]["model"]["latency_seconds_prior"] = 0.2
        result = self.route(request(max_latency_seconds=1), [slow, fast])
        self.assertEqual(result["v1_decision"]["route"]["provider"], "fast")
        self.assertTrue(any("LATENCY_LIMIT_EXCEEDED" in code for code in result["reason_codes"]))

    def test_invalid_resource_money_is_excluded_instead_of_invented(self) -> None:
        invalid = fragment("invalid-cost", "HOST")
        invalid["models"]["model"]["resource_cost"] = {"currency": "USD", "estimated_cost": 1}
        result = self.route(request(), [invalid])
        self.assertEqual(result["status"], "NO_ROUTE")
        self.assertTrue(any("RESOURCE_COST_INVALID" in code for code in result["reason_codes"]))

    def test_expired_resource_money_is_not_reused(self) -> None:
        expired = fragment("expired-cost", "HOST", models={"model": with_resource_cost(model("model"), 0.01)})
        expired["models"]["model"]["resource_cost"]["valid_until"] = "2026-09-07T11:00:00Z"
        result = self.route(request(), [expired])
        self.assertEqual(result["status"], "NO_ROUTE")
        self.assertTrue(any("RESOURCE_COST_EXPIRED" in code for code in result["reason_codes"]))

    def test_fragment_store_rejects_repository_location(self) -> None:
        with self.assertRaisesRegex(model_router.RouterError, "outside version control"):
            router_v2.ProviderFragmentStore(ROOT / ".ai" / "runtime")

    def test_v2_schemas_and_v1_contract_are_both_present(self) -> None:
        for name in (
            "model-router-catalog-fragment-v2.schema.json",
            "model-routing-request-v2.schema.json",
            "model-routing-decision-v2.schema.json",
        ):
            schema = json.loads((ROOT / "foundation" / "schemas" / name).read_text(encoding="utf-8"))
            self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        decision = self.route(request(), [fragment("host", "HOST")])
        self.assertEqual(decision["contract"], "foundation-model-router/v2")
        self.assertEqual(decision["v1_decision"]["contract"], "foundation-model-router/v1")


if __name__ == "__main__":
    unittest.main()
