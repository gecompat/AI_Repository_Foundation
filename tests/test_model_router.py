from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
CAPABILITY = ROOT / "foundation" / "capabilities" / "model-router"
sys.path.insert(0, str(CAPABILITY))

import mcp_stdio  # noqa: E402
import model_router  # noqa: E402
import ollama_cloud  # noqa: E402


def rates(input_price: float, cached_price: float | None, output_price: float, schedules: list | None = None) -> dict:
    return {
        "currency": "USD",
        "unit_tokens": 1_000_000,
        "base": {"input": input_price, "cached_input": cached_price, "output": output_price},
        "schedules": schedules or [],
    }


def model(
    model_id: str,
    *,
    quality: float,
    pricing: dict | None,
    assessment: str = "ASSESSED",
    availability: str = "AVAILABLE",
    capabilities: list[str] | None = None,
    context_window: int | None = 200_000,
) -> dict:
    return {
        "model_id": model_id,
        "availability": availability,
        "assessment": assessment,
        "capabilities": capabilities or ["text", "tools"],
        "context_window": context_window,
        "quality_prior": {"*": quality, "coding": quality},
        "supported_tiers": ["ECONOMICAL", "BALANCED", "FRONTIER"],
        "reasoning_efforts": ["low", "medium", "high"],
        "latency_seconds_prior": 1.0,
        "pricing": pricing,
    }


def catalog(*, valid_until: str = "2026-09-09T00:00:00Z") -> dict:
    peak = {
        "id": "weekday-peak",
        "priority": 10,
        "days_utc": [0, 1, 2, 3, 4],
        "start_utc": "12:00",
        "end_utc": "18:00",
        "rates": {"input": 2.0, "cached_input": 0.2, "output": 4.0},
    }
    providers = {
        "cloud-a": {
            "adapter": "synthetic/v1",
            "remote": True,
            "models": {
                "cheap": model("cheap", quality=0.70, pricing=rates(0.10, 0.01, 0.40, [peak])),
                "reliable": model("reliable", quality=0.90, pricing=rates(0.50, 0.10, 1.00)),
                "new": model("new", quality=0.80, pricing=rates(0.05, 0.01, 0.20), assessment="UNASSESSED"),
                "unpriced": model("unpriced", quality=0.95, pricing=None, availability="MISSING_PRICE"),
            },
        }
    }
    value = {
        "schema_version": 1,
        "contract": model_router.CONTRACT,
        "generated_at": "2026-09-06T00:00:00Z",
        "valid_until": valid_until,
        "pricing_epoch": "sha256:prices",
        "catalog_epoch": "sha256:catalog",
        "router_defaults": {
            "tier_quality_floors": {"ECONOMICAL": 0.45, "BALANCED": 0.65, "FRONTIER": 0.82},
            "quality_prior_strength": 4,
            "minimum_evaluation_trials": 3,
            "daily_evaluation_budget_usd": 0.5,
            "failure_cost_usd": 0,
            "latency_value_usd_per_second": 0,
            "switching_cost_usd": 0,
        },
        "providers": providers,
    }
    return value


def request(**overrides) -> dict:
    value = {
        "tier": "BALANCED",
        "task_class": "coding.repository",
        "context_tokens": 100_000,
        "cached_input_tokens": 0,
        "expected_output_tokens": 1_000,
        "required_capabilities": ["tools"],
        "allow_remote": True,
        "at": "2026-09-07T10:00:00Z",
    }
    value.update(overrides)
    return value


class RouterFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.state_dir = Path(self.temporary.name) / "router-state"
        self.store = model_router.RuntimeStore(self.state_dir)
        self.router = model_router.ModelRouter(catalog(), self.store)

    def tearDown(self) -> None:
        self.temporary.cleanup()


class CoreRoutingTests(RouterFixture):
    def test_local_tier_never_selects_a_model(self) -> None:
        decision = self.router.route(request(tier="LOCAL", allow_remote=False))
        self.assertEqual(decision["status"], "LOCAL_ONLY")
        self.assertIsNone(decision["route"])
        self.assertEqual(decision["reason_codes"], ["DETERMINISTIC_LOCAL_PROCESSING_REQUIRED"])

    def test_remote_provider_requires_explicit_authorization(self) -> None:
        decision = self.router.route(request(allow_remote=False))
        self.assertEqual(decision["status"], "NO_ROUTE")
        self.assertIn("REMOTE_NOT_AUTHORIZED", decision["reason_codes"])

        provider = self.router.route(request(allowed_providers=["different-provider"]))
        self.assertEqual(provider["status"], "NO_ROUTE")
        self.assertIn("PROVIDER_NOT_ALLOWED", provider["reason_codes"])

    def test_unknown_request_fields_are_rejected(self) -> None:
        with self.assertRaisesRegex(model_router.RouterError, "unknown routing request"):
            self.router.route(request(typo_budget=1))

    def test_cost_of_success_prefers_cheap_model_then_reliable_model_when_failure_is_costly(self) -> None:
        cheap = self.router.route(request(failure_cost_usd=0))
        self.assertEqual(cheap["route"]["model"], "cheap")
        self.assertEqual(cheap["fallbacks"][0]["model"], "reliable")

        reliable = self.router.route(request(failure_cost_usd=1.0))
        self.assertEqual(reliable["route"]["model"], "reliable")

    def test_peak_window_changes_route_epoch_and_expiry(self) -> None:
        off_peak = self.router.route(request(at="2026-09-07T10:00:00Z"))
        self.assertEqual(off_peak["route"]["model"], "cheap")
        self.assertTrue(off_peak["pricing_epoch"].endswith("/base"))
        self.assertEqual(off_peak["valid_until"], "2026-09-07T12:00:00Z")

        peak = self.router.route(request(at="2026-09-07T13:00:00Z"))
        self.assertEqual(peak["route"]["model"], "reliable")
        self.assertNotEqual(off_peak["decision_id"], peak["decision_id"])
        self.assertTrue(any(row["pricing_epoch"].endswith("/official-peak") or row["pricing_epoch"].endswith("/weekday-peak") for row in peak["candidates_considered"]))
        self.assertEqual(peak["valid_until"], "2026-09-07T18:00:00Z")

        over_budget = self.router.route(request(at="2026-09-07T13:00:00Z", max_cost_usd=0.02))
        self.assertEqual(over_budget["status"], "NO_ROUTE")
        self.assertEqual(over_budget["valid_until"], "2026-09-07T18:00:00Z")
        after_peak = self.router.route(request(at="2026-09-07T19:00:00Z", max_cost_usd=0.02))
        self.assertEqual(after_peak["route"]["model"], "cheap")

    def test_overnight_schedule_applies_on_following_day(self) -> None:
        schedule = {
            "days_utc": [0],
            "start_utc": "22:00",
            "end_utc": "02:00",
        }
        self.assertTrue(model_router.schedule_active(schedule, datetime(2026, 9, 7, 23, 0, tzinfo=timezone.utc)))
        self.assertTrue(model_router.schedule_active(schedule, datetime(2026, 9, 8, 1, 0, tzinfo=timezone.utc)))
        self.assertFalse(model_router.schedule_active(schedule, datetime(2026, 9, 8, 3, 0, tzinfo=timezone.utc)))
        self.assertEqual(
            model_router.next_schedule_boundary([schedule], datetime(2026, 9, 8, 1, 0, tzinfo=timezone.utc)),
            datetime(2026, 9, 8, 2, 0, tzinfo=timezone.utc),
        )

    def test_explicit_null_numeric_constraint_is_rejected(self) -> None:
        with self.assertRaisesRegex(model_router.RouterError, "max_cost_usd"):
            self.router.route(request(max_cost_usd=None))

    def test_capability_context_quality_and_expiry_fail_closed(self) -> None:
        capability = self.router.route(request(required_capabilities=["vision"]))
        self.assertEqual(capability["status"], "NO_ROUTE")
        self.assertIn("CAPABILITY_MISMATCH", capability["reason_codes"])

        context = self.router.route(request(context_tokens=300_000))
        self.assertEqual(context["status"], "NO_ROUTE")
        self.assertIn("CONTEXT_WINDOW_EXCEEDED", context["reason_codes"])

        frontier = self.router.route(request(tier="FRONTIER"))
        self.assertEqual(frontier["route"]["model"], "reliable")

        expired_store = model_router.RuntimeStore(self.state_dir / "expired")
        expired = model_router.ModelRouter(catalog(valid_until="2026-09-07T09:00:00Z"), expired_store)
        decision = expired.route(request())
        self.assertEqual(decision["status"], "NO_ROUTE")
        self.assertIn("PRICING_EXPIRED", decision["reason_codes"])

    def test_session_affinity_reuses_confirmed_cached_context_without_storing_raw_session_id(self) -> None:
        first = self.router.route(request())
        self.store.record_outcome(
            provider="cloud-a",
            model="cheap",
            task_class="coding.repository",
            success=True,
            actual_cost_usd=Decimal("0.01"),
            session_id="private-session-label",
            context_tokens=90_000,
            pricing_epoch=first["pricing_epoch"],
            recorded_at=datetime(2026, 9, 7, 10, 1, tzinfo=timezone.utc),
        )
        decision = self.router.route(request(session_id="private-session-label"))
        self.assertEqual(decision["route"]["estimated_cached_input_tokens"], 90_000)
        self.assertEqual(decision["execution"]["cache_strategy"], "preserve_session_affinity")
        state_text = self.store.state_path.read_text(encoding="utf-8")
        self.assertNotIn("private-session-label", state_text)

    def test_declared_cache_applies_only_to_the_matching_current_model(self) -> None:
        decision = self.router.route(
            request(current_provider="cloud-a", current_model="cheap", cached_input_tokens=90_000)
        )
        by_model = {row["model"]: row for row in decision["candidates_considered"]}
        self.assertLess(by_model["cheap"]["estimated_cost_usd"], by_model["reliable"]["estimated_cost_usd"])
        with self.assertRaisesRegex(model_router.RouterError, "cached_input_tokens requires"):
            self.router.route(request(cached_input_tokens=1))

    def test_empirical_failures_change_the_ranking(self) -> None:
        self.assertEqual(self.router.route(request())["route"]["model"], "cheap")
        for _ in range(12):
            self.store.record_outcome(
                provider="cloud-a",
                model="cheap",
                task_class="coding.repository",
                success=False,
                actual_cost_usd=Decimal("0.01"),
            )
        self.assertEqual(self.router.route(request())["route"]["model"], "reliable")

    def test_bounded_evaluation_reservation_and_empirical_graduation(self) -> None:
        for _index in range(3):
            plan = self.router.plan_evaluation(
                request(tier="ECONOMICAL"), budget_usd=Decimal("0.2"), max_candidates=2, reserve=True
            )
            self.assertEqual(plan["status"], "EVALUATION_PLANNED")
            self.assertEqual(len(plan["trials"]), 1)
            trial = plan["trials"][0]
            self.assertEqual(trial["model"], "new")
            self.assertTrue(trial["reserved"])
            self.store.record_outcome(
                provider="cloud-a",
                model="new",
                task_class="coding.repository",
                success=True,
                actual_cost_usd=Decimal("0.001"),
                pricing_epoch=trial["pricing_epoch"],
                evaluation_id=trial["evaluation_id"],
                recorded_at=datetime(2026, 9, 7, 10, 1, tzinfo=timezone.utc),
            )
        decision = self.router.route(request(tier="ECONOMICAL"))
        self.assertEqual(decision["route"]["model"], "new")
        self.assertEqual(decision["route"]["assessment"], "ASSESSED")

    def test_unassessed_model_never_bypasses_bounded_evaluation(self) -> None:
        unknown_only = catalog()
        for model_id, row in unknown_only["providers"]["cloud-a"]["models"].items():
            if model_id != "new":
                row["assessment"] = "DISABLED"
        router = model_router.ModelRouter(unknown_only, model_router.RuntimeStore(self.state_dir / "unknown-only"))
        decision = router.route(request(allow_evaluation=True))
        self.assertEqual(decision["status"], "NO_ROUTE")
        self.assertIn("EVALUATION_REQUIRED", decision["reason_codes"])

    def test_evaluation_outcome_must_match_an_active_reservation(self) -> None:
        with self.assertRaisesRegex(model_router.RouterError, "active reservation"):
            self.store.record_outcome(
                provider="cloud-a",
                model="new",
                task_class="coding.repository",
                success=True,
                actual_cost_usd=Decimal("0.001"),
                pricing_epoch="sha256:prices/base",
                evaluation_id="eval-missing",
            )

    def test_snapshot_is_expiring_runtime_data(self) -> None:
        snapshot = self.router.snapshot(request())
        self.assertTrue(snapshot["runtime_only"])
        self.assertEqual(set(snapshot["routes"]), set(model_router.TIERS))
        self.assertLessEqual(snapshot["valid_until"], "2026-09-07T12:00:00Z")

    def test_schema_contracts_cover_generated_payloads(self) -> None:
        request_schema = json.loads((ROOT / "foundation/schemas/model-routing-request.schema.json").read_text(encoding="utf-8"))
        decision_schema = json.loads((ROOT / "foundation/schemas/model-routing-decision.schema.json").read_text(encoding="utf-8"))
        catalog_schema = json.loads((ROOT / "foundation/schemas/model-router-catalog.schema.json").read_text(encoding="utf-8"))
        snapshot_schema = json.loads((ROOT / "foundation/schemas/model-routing-snapshot.schema.json").read_text(encoding="utf-8"))
        profiles_schema = json.loads((ROOT / "foundation/schemas/model-router-profiles.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(set(request_schema["properties"]), model_router.REQUEST_FIELDS)
        for decision in (
            self.router.route(request()),
            self.router.route(request(tier="LOCAL", allow_remote=False)),
            self.router.route(request(allow_remote=False)),
        ):
            self.assertTrue(set(decision_schema["required"]).issubset(decision))
            self.assertEqual(decision["contract"], decision_schema["properties"]["contract"]["const"])
        self.assertTrue(set(catalog_schema["required"]).issubset(self.router.catalog))
        snapshot = self.router.snapshot(request())
        self.assertTrue(set(snapshot_schema["required"]).issubset(snapshot))
        profiles = json.loads((CAPABILITY / "profiles.example.json").read_text(encoding="utf-8"))
        self.assertTrue(set(profiles_schema["required"]).issubset(profiles))


class OllamaAdapterTests(unittest.TestCase):
    PRICING_HTML = """
    <section id="model-pricing">
      <h2>Model pricing</h2><p>Prices are per million tokens</p>
      <table><tr><th>Model</th><th>Input</th><th>Cached input</th><th>Output</th></tr>
      <tr><td>alpha</td><td>$0.10</td><td>-</td><td>$0.30</td></tr>
      <tr><td>family:large</td><td>$0.20</td><td>$0.02</td><td>$0.60</td></tr></table>
      <h3>Peak pricing</h3><p>Peak pricing applies between 12:00 and 18:00 UTC, Monday to Friday.</p>
      <table><tr><th>Model</th><th>Input</th><th>Cached input</th><th>Output</th></tr>
      <tr><td>alpha</td><td>$0.20</td><td>-</td><td>$0.60</td></tr></table>
    </section>
    """

    def test_pricing_parser_and_model_alias_matching(self) -> None:
        parsed = ollama_cloud.parse_pricing_page(self.PRICING_HTML)
        self.assertEqual(parsed["base"]["alpha"]["input"], 0.10)
        self.assertIsNone(parsed["base"]["alpha"]["cached_input"])
        self.assertEqual(parsed["peak_schedule"]["days_utc"], [0, 1, 2, 3, 4])
        self.assertEqual(ollama_cloud.pricing_key_for("alpha:70b", set(parsed["base"])), "alpha")
        self.assertEqual(ollama_cloud.pricing_key_for("family:large", set(parsed["base"])), "family:large")

    def test_sync_combines_inventory_prices_profiles_and_new_model_detection(self) -> None:
        inventory = json.dumps(
            {
                "models": [
                    {"name": "alpha:70b", "model": "alpha:70b", "digest": "a"},
                    {"name": "unpriced", "model": "unpriced", "digest": "b"},
                ]
            }
        )
        profiles = {
            "schema_version": 1,
            "profiles": {
                "ollama-cloud": {
                    "alpha": {
                        "assessment": "ASSESSED",
                        "capabilities": ["text", "tools"],
                        "context_window": 100_000,
                        "quality_prior": {"*": 0.8},
                        "supported_tiers": ["ECONOMICAL", "BALANCED"],
                        "reasoning_efforts": ["low", "medium"],
                    }
                }
            },
        }
        with mock.patch.object(ollama_cloud, "_read_url", side_effect=[inventory, self.PRICING_HTML]):
            result = ollama_cloud.sync_ollama_catalog(
                model_url="https://provider.invalid/api/tags",
                pricing_url="https://provider.invalid/pricing",
                timeout_seconds=1,
                ttl_hours=24,
                profiles=profiles,
            )
        alpha = result["providers"]["ollama-cloud"]["models"]["alpha:70b"]
        self.assertEqual(alpha["pricing_key"], "alpha")
        self.assertEqual(alpha["assessment"], "ASSESSED")
        self.assertEqual(alpha["pricing"]["schedules"][0]["start_utc"], "12:00")
        self.assertEqual(
            result["providers"]["ollama-cloud"]["models"]["unpriced"]["availability"], "MISSING_PRICE"
        )
        self.assertIn("alpha:70b", result["new_models"])
        self.assertTrue(result["pricing_epoch"].startswith("sha256:"))
        invalid_profiles = {
            "schema_version": 1,
            "profiles": {"unused-provider": {"unused-model": {"quality_prior": {"*": "0.5"}}}},
        }
        with mock.patch.object(ollama_cloud, "_read_url") as read_url:
            with self.assertRaisesRegex(model_router.RouterError, "quality_prior"):
                ollama_cloud.sync_ollama_catalog(
                    model_url="https://provider.invalid/api/tags",
                    pricing_url="https://provider.invalid/pricing",
                    timeout_seconds=1,
                    ttl_hours=24,
                    profiles=invalid_profiles,
                )
            read_url.assert_not_called()

    def test_changed_prices_change_pricing_epoch(self) -> None:
        inventory = json.dumps({"models": [{"model": "alpha"}]})
        with mock.patch.object(ollama_cloud, "_read_url", side_effect=[inventory, self.PRICING_HTML]):
            first = ollama_cloud.sync_ollama_catalog(
                model_url="https://provider.invalid/api/tags",
                pricing_url="https://provider.invalid/pricing",
                timeout_seconds=1,
                ttl_hours=24,
            )
        changed = self.PRICING_HTML.replace("$0.10", "$0.11", 1)
        with mock.patch.object(ollama_cloud, "_read_url", side_effect=[inventory, changed]):
            second = ollama_cloud.sync_ollama_catalog(
                model_url="https://provider.invalid/api/tags",
                pricing_url="https://provider.invalid/pricing",
                timeout_seconds=1,
                ttl_hours=24,
            )
        self.assertNotEqual(first["pricing_epoch"], second["pricing_epoch"])

    def test_discovery_reports_models_entering_and_leaving_inventory(self) -> None:
        first_inventory = json.dumps({"models": [{"model": "alpha"}]})
        second_inventory = json.dumps({"models": [{"model": "family:large"}]})
        with mock.patch.object(
            ollama_cloud,
            "_read_url",
            side_effect=[first_inventory, self.PRICING_HTML, second_inventory, self.PRICING_HTML],
        ):
            first = ollama_cloud.sync_ollama_catalog(
                model_url="https://provider.invalid/api/tags",
                pricing_url="https://provider.invalid/pricing",
                timeout_seconds=1,
                ttl_hours=24,
            )
            second = ollama_cloud.sync_ollama_catalog(
                model_url="https://provider.invalid/api/tags",
                pricing_url="https://provider.invalid/pricing",
                timeout_seconds=1,
                ttl_hours=24,
                previous=first,
            )
        self.assertEqual(second["new_models"], ["family:large"])
        self.assertEqual(second["removed_models"], ["alpha"])

    def test_api_key_is_not_sent_to_a_nonofficial_endpoint(self) -> None:
        with mock.patch.dict("os.environ", {"OLLAMA_API_KEY": "synthetic-secret"}):
            with self.assertRaisesRegex(model_router.RouterError, "official HTTPS ollama.com"):
                ollama_cloud.sync_ollama_catalog(
                    model_url="https://provider.invalid/api/tags",
                    pricing_url="https://provider.invalid/pricing",
                    timeout_seconds=1,
                    ttl_hours=24,
                )
        with self.assertRaisesRegex(model_router.RouterError, "credential-free HTTPS"):
            ollama_cloud.sync_ollama_catalog(
                model_url="https://ollama.com/api/tags?token=synthetic",
                pricing_url="https://ollama.com/pricing",
                timeout_seconds=1,
                ttl_hours=24,
            )


class AdapterAndCliTests(RouterFixture):
    def setUp(self) -> None:
        super().setUp()
        self.catalog_path = Path(self.temporary.name) / "catalog.json"
        self.catalog_path.write_text(json.dumps(catalog()), encoding="utf-8")
        self.script = CAPABILITY / "model_router.py"

    def test_mcp_handshake_tools_and_structured_route(self) -> None:
        messages = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "model_router_route", "arguments": request(context_tokens=0, expected_output_tokens=100)}},
        ]
        completed = subprocess.run(
            [sys.executable, str(self.script), "--state-dir", str(self.state_dir), "mcp", "--catalog", str(self.catalog_path)],
            input="".join(json.dumps(row) + "\n" for row in messages),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        output = [json.loads(line) for line in completed.stdout.splitlines()]
        self.assertEqual(len(output), 3)
        self.assertEqual(output[0]["result"]["protocolVersion"], "2025-11-25")
        self.assertEqual(output[1]["result"]["tools"][0]["name"], "model_router_route")
        self.assertEqual(output[2]["result"]["structuredContent"]["status"], "ROUTED")

    def test_running_mcp_server_reloads_an_atomically_replaced_catalog(self) -> None:
        process = subprocess.Popen(
            [
                sys.executable,
                str(self.script),
                "--state-dir",
                str(self.state_dir),
                "mcp",
                "--catalog",
                str(self.catalog_path),
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.assertIsNotNone(process.stdin)
        self.assertIsNotNone(process.stdout)
        try:
            initialize = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}},
            }
            process.stdin.write(json.dumps(initialize) + "\n")
            process.stdin.flush()
            self.assertIn("result", json.loads(process.stdout.readline()))

            route_call = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": "model_router_route", "arguments": request(context_tokens=0, expected_output_tokens=100)},
            }
            process.stdin.write(json.dumps(route_call) + "\n")
            process.stdin.flush()
            first = json.loads(process.stdout.readline())
            self.assertEqual(first["result"]["structuredContent"]["route"]["model"], "cheap")

            updated = catalog()
            updated["providers"]["cloud-a"]["models"]["cheap"]["assessment"] = "DISABLED"
            updated["catalog_epoch"] = "sha256:updated"
            model_router.atomic_json_write(self.catalog_path, updated)
            route_call["id"] = 3
            process.stdin.write(json.dumps(route_call) + "\n")
            process.stdin.flush()
            second = json.loads(process.stdout.readline())
            self.assertEqual(second["result"]["structuredContent"]["route"]["model"], "reliable")
        finally:
            process.stdin.close()
            process.wait(timeout=10)
            process.stdout.close()
            if process.stderr is not None:
                process.stderr.close()

    def test_cli_route_and_shell_free_launch(self) -> None:
        command = [
            sys.executable,
            str(self.script),
            "--state-dir",
            str(self.state_dir),
            "route",
            "--catalog",
            str(self.catalog_path),
            "--tier",
            "BALANCED",
            "--task-class",
            "coding.repository",
            "--context-tokens",
            "1000",
            "--output-tokens",
            "100",
            "--required-capability",
            "tools",
            "--allow-remote",
        ]
        routed = subprocess.run(command, text=True, capture_output=True, check=False)
        self.assertEqual(routed.returncode, 0, routed.stderr)
        self.assertEqual(json.loads(routed.stdout)["status"], "ROUTED")

        launched = subprocess.run(
            [
                sys.executable,
                str(self.script),
                "--state-dir",
                str(self.state_dir),
                "launch",
                "--catalog",
                str(self.catalog_path),
                "--tier",
                "BALANCED",
                "--task-class",
                "coding.repository",
                "--output-tokens",
                "10",
                "--allow-remote",
                "--",
                sys.executable,
                "-c",
                "import os,sys;sys.exit(0 if os.environ.get('AI_ROUTED_MODEL') else 9)",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(launched.returncode, 0, launched.stdout + launched.stderr)

    def test_runtime_state_inside_repository_is_rejected(self) -> None:
        with self.assertRaises(model_router.RouterError):
            model_router.RuntimeStore(ROOT / ".runtime-model-router")
        other_repository = Path(self.temporary.name) / "other-repository"
        (other_repository / ".git").mkdir(parents=True)
        with self.assertRaises(model_router.RouterError):
            model_router.RuntimeStore(other_repository / "runtime")

    def test_mcp_tool_order_is_deterministic_and_route_tools_are_read_only(self) -> None:
        first = mcp_stdio.tools()
        second = mcp_stdio.tools()
        self.assertEqual(first, second)
        self.assertEqual(first[0]["name"], "model_router_route")
        self.assertTrue(first[0]["annotations"]["readOnlyHint"])
        self.assertEqual(set(first[0]["inputSchema"]["properties"]), model_router.REQUEST_FIELDS)

    def test_mcp_rejects_wrong_types_and_unknown_arguments(self) -> None:
        wrong_reserve = mcp_stdio.call_tool(
            "model_router_plan_evaluation",
            {"request": request(), "budget_usd": 0.1, "reserve": "false"},
            self.router,
            self.store,
        )
        self.assertTrue(wrong_reserve["isError"])
        unknown = mcp_stdio.call_tool(
            "model_router_record_outcome",
            {"provider": "cloud-a", "model": "cheap", "task_class": "coding", "success": True, "extra": 1},
            self.router,
            self.store,
        )
        self.assertTrue(unknown["isError"])


if __name__ == "__main__":
    unittest.main()
