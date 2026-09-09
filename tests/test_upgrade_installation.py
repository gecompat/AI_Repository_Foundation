from __future__ import annotations

import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import install_foundation  # noqa: E402
import upgrade_applicability  # noqa: E402


class UpgradeInstallationTests(unittest.TestCase):
    def test_installed_repo_map_exposes_upgrade_registry_continuity_cache_routing_and_ai_work_contracts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            with redirect_stdout(StringIO()):
                rc = install_foundation.main([str(target), "--adapters", "none", "--apply"])
            self.assertEqual(rc, 0)
            repo_map = (target / ".ai" / "foundation" / "repo_map.yaml").read_text(encoding="utf-8")
            self.assertIn("upgrade_contract:", repo_map)
            self.assertIn("central_registry_contract:", repo_map)
            self.assertIn("continuity_contract:", repo_map)
            self.assertIn("rule_context_cache_contract:", repo_map)
            self.assertIn("validation_failure_bypass: prohibited", repo_map)
            self.assertIn("infrastructure_unavailable_bypass: project_selectable", repo_map)
            self.assertIn("deferred_validation_after_recovery: required", repo_map)
            self.assertIn("utf8_crlf_lf_equivalent: true", repo_map)
            self.assertIn("statuses: CACHE_HIT_PARTIAL_INVALIDATION_CACHE_MISS", repo_map)
            self.assertIn("head_only_hit: prohibited", repo_map)
            self.assertIn("model_routing_contract:", repo_map)
            self.assertIn("profile: foundation-model-router/v2", repo_map)
            self.assertIn("compatible_profiles: foundation-model-router/v1_foundation-model-router/v2", repo_map)
            self.assertIn("objective: minimum_complete_chain_expected_cost_of_success", repo_map)
            self.assertIn("runtime_state: outside_version_control", repo_map)
            self.assertIn("ai_work_contract:", repo_map)
            self.assertIn("profile: foundation-ai-work/v1", repo_map)
            self.assertIn("capability_failures: isolated", repo_map)
            self.assertIn("authority_expansion: prohibited", repo_map)
            self.assertIn("python_required: false", repo_map)
            self.assertIn("runtime_inventory_schema: .ai/foundation/schemas/runtime-inventory.schema.json", repo_map)
            self.assertIn("host_preparation_capability: ai-provisioning", repo_map)
            self.assertIn("model_runtime_evidence_schema: .ai/foundation/schemas/model-runtime-evidence.schema.json", repo_map)
            self.assertIn("model_evidence_sources_schema: .ai/foundation/schemas/model-evidence-sources.schema.json", repo_map)
            self.assertIn("orchestration_request_schema: .ai/foundation/schemas/ai-orchestration-request.schema.json", repo_map)
            self.assertIn("orchestration_report_schema: .ai/foundation/schemas/ai-orchestration-report.schema.json", repo_map)
            self.assertIn("orchestrator_capability: ai-orchestrator", repo_map)
            self.assertIn("orchestration_profile: foundation-ai-orchestration/v1", repo_map)
            self.assertIn("orchestration_unattested_result: MANUAL_REQUIRED", repo_map)
            self.assertIn("cost_refresh_minimum_seconds: 86400", repo_map)
            self.assertIn("ai_client_integration_contract:", repo_map)
            self.assertIn("profile: foundation-ai-client-integration/v1", repo_map)
            self.assertIn("native_model_capability_schema: .ai/foundation/schemas/client-model-routing-capability.schema.json", repo_map)
            self.assertIn("vscode_model_plan_schema: .ai/foundation/schemas/vscode-model-routing-plan.schema.json", repo_map)
            self.assertIn("manual_fallback_status: MANUAL_DISPATCH_REQUIRED", repo_map)
            self.assertIn("unattested_status: REQUESTED_NOT_ATTESTED", repo_map)
            self.assertIn("installation_receipt: .ai/foundation/installation-provenance.json", repo_map)
            self.assertIn("UNKNOWN_DRIFT", repo_map)

    def test_feature_catalog_and_manifest_versions_match(self) -> None:
        manifest = json.loads((ROOT / "foundation" / "manifest.json").read_text(encoding="utf-8"))
        catalog = json.loads((ROOT / "foundation" / "feature_catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["ruleset_version"], catalog["ruleset_version"])
        self.assertEqual(manifest["ruleset_version"], "1.17.2")

    def test_1_2_to_1_8_delta_surfaces_nomenclature_registry_eol_continuity_and_cache(self) -> None:
        catalog = json.loads((ROOT / "foundation" / "feature_catalog.json").read_text(encoding="utf-8"))
        candidates = upgrade_applicability.candidate_features(catalog, "1.2.0", "1.8.0")
        by_id = {item["feature_id"]: item for item in candidates}
        identity = by_id["persistent-identity"]
        self.assertIn("durable_planning_identifiers", identity["applicability"]["signals"])
        self.assertIn("ADOPT_FORWARD", identity["recommendation"]["summary"])
        central = by_id["central-artifact-registry"]
        self.assertIn("json_file_registration_authority", central["applicability"]["signals"])
        self.assertIn("object/property", central["recommendation"]["summary"])
        self.assertIn("material_change:1.7.0", by_id["layered-validation"]["candidate_reasons"])
        continuity = by_id["repository-continuity-break-glass"]
        self.assertIn("introduced_in:1.7.0", continuity["candidate_reasons"])
        self.assertIn("required_ci_checks", continuity["applicability"]["signals"])
        cache = by_id["rule-context-cache"]
        self.assertIn("introduced_in:1.8.0", cache["candidate_reasons"])
        self.assertIn("multi_wave_ai_work", cache["applicability"]["signals"])

    def test_1_8_to_1_9_delta_surfaces_dynamic_model_routing(self) -> None:
        catalog = json.loads((ROOT / "foundation" / "feature_catalog.json").read_text(encoding="utf-8"))
        candidates = upgrade_applicability.candidate_features(catalog, "1.8.0", "1.9.0")
        by_id = {item["feature_id"]: item for item in candidates}
        routing = by_id["model-routing-interoperability"]
        self.assertEqual(routing["candidate_reasons"], ["material_change:1.9.0"])
        self.assertIn("time_dependent_pricing", routing["applicability"]["signals"])
        self.assertIn("cost-of-success", routing["recommendation"]["summary"])

    def test_1_9_to_1_10_delta_surfaces_system_independent_ai_work(self) -> None:
        catalog = json.loads((ROOT / "foundation" / "feature_catalog.json").read_text(encoding="utf-8"))
        candidates = upgrade_applicability.candidate_features(catalog, "1.9.0", "1.10.0")
        by_id = {item["feature_id"]: item for item in candidates}
        work = by_id["ai-work-orchestration"]
        self.assertEqual(work["candidate_reasons"], ["introduced_in:1.10.0"])
        self.assertIn("runtime_failure_isolation", work["applicability"]["signals"])
        self.assertIn("runtime-neutral", work["recommendation"]["summary"])

    def test_1_10_to_1_11_delta_surfaces_router_v2_and_runtime_adapters(self) -> None:
        catalog = json.loads((ROOT / "foundation" / "feature_catalog.json").read_text(encoding="utf-8"))
        candidates = upgrade_applicability.candidate_features(catalog, "1.10.0", "1.11.0")
        by_id = {item["feature_id"]: item for item in candidates}
        self.assertEqual(
            by_id["model-routing-interoperability"]["candidate_reasons"],
            ["material_change:1.11.0"],
        )
        self.assertEqual(
            by_id["ai-runtime-adapters"]["candidate_reasons"],
            ["introduced_in:1.11.0"],
        )

    def test_1_11_to_1_12_delta_surfaces_resumable_executor(self) -> None:
        catalog = json.loads((ROOT / "foundation" / "feature_catalog.json").read_text(encoding="utf-8"))
        candidates = upgrade_applicability.candidate_features(catalog, "1.11.0", "1.12.0")
        by_id = {item["feature_id"]: item for item in candidates}
        self.assertEqual(by_id["ai-work-orchestration"]["candidate_reasons"], ["material_change:1.12.0"])
        self.assertEqual(by_id["ai-work-execution"]["candidate_reasons"], ["introduced_in:1.12.0"])

    def test_1_12_to_1_13_delta_surfaces_bounded_host_preparation(self) -> None:
        catalog = json.loads((ROOT / "foundation" / "feature_catalog.json").read_text(encoding="utf-8"))
        candidates = upgrade_applicability.candidate_features(catalog, "1.12.0", "1.13.0")
        by_id = {item["feature_id"]: item for item in candidates}
        self.assertEqual(by_id["ai-work-orchestration"]["candidate_reasons"], ["material_change:1.13.0"])
        preparation = by_id["ai-host-preparation"]
        self.assertEqual(preparation["candidate_reasons"], ["introduced_in:1.13.0"])
        self.assertIn("runtime_outside_path", preparation["applicability"]["signals"])
        self.assertIn("no more than once per source per day", preparation["recommendation"]["summary"])

    def test_1_13_to_1_14_delta_surfaces_attested_and_manual_client_dispatch(self) -> None:
        catalog = json.loads((ROOT / "foundation" / "feature_catalog.json").read_text(encoding="utf-8"))
        candidates = upgrade_applicability.candidate_features(catalog, "1.13.0", "1.14.0")
        by_id = {item["feature_id"]: item for item in candidates}
        self.assertEqual(by_id["model-routing-interoperability"]["candidate_reasons"], ["material_change:1.14.0"])
        self.assertEqual(by_id["ai-work-orchestration"]["candidate_reasons"], ["material_change:1.14.0"])
        integration = by_id["ai-client-integration"]
        self.assertEqual(integration["candidate_reasons"], ["introduced_in:1.14.0"])
        self.assertIn("model_dispatch_attestation", integration["applicability"]["signals"])
        self.assertIn("manual handoff", integration["recommendation"]["summary"])

    def test_1_14_to_1_15_delta_surfaces_installed_provenance(self) -> None:
        catalog = json.loads((ROOT / "foundation" / "feature_catalog.json").read_text(encoding="utf-8"))
        candidates = upgrade_applicability.candidate_features(catalog, "1.14.0", "1.15.0")
        self.assertEqual([item["feature_id"] for item in candidates], ["installed-foundation-provenance"])
        self.assertEqual(candidates[0]["candidate_reasons"], ["introduced_in:1.15.0"])

    def test_1_15_to_1_16_delta_surfaces_runtime_configuration_and_mcp(self) -> None:
        catalog = json.loads((ROOT / "foundation" / "feature_catalog.json").read_text(encoding="utf-8"))
        candidates = upgrade_applicability.candidate_features(catalog, "1.15.0", "1.16.0")
        self.assertEqual([item["feature_id"] for item in candidates], ["ai-client-integration", "ai-runtime-adapters"])
        by_id = {item["feature_id"]: item for item in candidates}
        self.assertEqual(by_id["ai-runtime-adapters"]["candidate_reasons"], ["material_change:1.16.0"])
        self.assertIn("interactive_runtime_configuration", by_id["ai-runtime-adapters"]["applicability"]["signals"])
        self.assertEqual(by_id["ai-client-integration"]["candidate_reasons"], ["material_change:1.16.0"])
        self.assertIn("native_client_model_roles", by_id["ai-client-integration"]["applicability"]["signals"])

    def test_1_16_to_1_17_delta_surfaces_end_to_end_evidence_routing(self) -> None:
        catalog = json.loads((ROOT / "foundation" / "feature_catalog.json").read_text(encoding="utf-8"))
        candidates = upgrade_applicability.candidate_features(catalog, "1.16.0", "1.17.0")
        self.assertEqual([item["feature_id"] for item in candidates], ["ai-work-orchestration", "model-routing-interoperability"])
        by_id = {item["feature_id"]: item for item in candidates}
        self.assertEqual(by_id["ai-work-orchestration"]["candidate_reasons"], ["material_change:1.17.0"])
        self.assertEqual(by_id["model-routing-interoperability"]["candidate_reasons"], ["material_change:1.17.0"])

    def test_1_17_0_to_1_17_1_delta_surfaces_node24_registry_workflow(self) -> None:
        catalog = json.loads((ROOT / "foundation" / "feature_catalog.json").read_text(encoding="utf-8"))
        candidates = upgrade_applicability.candidate_features(catalog, "1.17.0", "1.17.1")
        self.assertEqual([item["feature_id"] for item in candidates], ["central-artifact-registry"])
        self.assertEqual(candidates[0]["candidate_reasons"], ["material_change:1.17.1"])

    def test_1_17_1_to_1_17_2_documentation_reconciliation_is_non_material(self) -> None:
        catalog = json.loads((ROOT / "foundation" / "feature_catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(upgrade_applicability.candidate_features(catalog, "1.17.1", "1.17.2"), [])
        for feature_id in ["central-artifact-registry", "ai-work-orchestration", "ai-client-integration"]:
            changes = catalog["features"][feature_id]["change_history"]
            current = [change for change in changes if change["version"] == "1.17.2"]
            self.assertEqual(len(current), 1)
            self.assertEqual(current[0]["impact"], "NON_MATERIAL")


if __name__ == "__main__":
    unittest.main()
