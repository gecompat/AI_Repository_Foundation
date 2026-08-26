from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import feature_catalog_guard  # noqa: E402
import upgrade_applicability  # noqa: E402


class UpgradeApplicabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads((ROOT / "foundation" / "manifest.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((ROOT / "foundation" / "feature_catalog.json").read_text(encoding="utf-8"))

    def test_current_catalog_covers_all_transferable_core_and_capabilities(self) -> None:
        self.assertEqual(feature_catalog_guard.validate_catalog(self.manifest, self.catalog), [])

    def test_upgrade_from_1_2_surfaces_identity_registration_upgrade_registry_and_eol_fix(self) -> None:
        candidates = upgrade_applicability.candidate_features(self.catalog, "1.2.0", "1.6.1")
        ids = {item["feature_id"] for item in candidates}
        self.assertIn("persistent-identity", ids)
        self.assertIn("artifact-registration", ids)
        self.assertIn("semantic-upgrade-applicability", ids)
        self.assertIn("central-artifact-registry", ids)
        self.assertIn("semantic-integration", ids)
        self.assertIn("layered-validation", ids)

    def test_upgrade_from_1_5_surfaces_v2_registry_registration_and_eol_material_changes(self) -> None:
        candidates = upgrade_applicability.candidate_features(self.catalog, "1.5.0", "1.6.1")
        reasons = {item["feature_id"]: item["candidate_reasons"] for item in candidates}
        self.assertIn("central-artifact-registry", reasons)
        self.assertIn("artifact-registration", reasons)
        self.assertIn("material_change:1.6.0", reasons["artifact-registration"])
        self.assertIn("layered-validation", reasons)
        self.assertIn("material_change:1.6.1", reasons["layered-validation"])
        self.assertNotIn("persistent-identity", reasons)

    def test_upgrade_from_1_6_surfaces_only_material_eol_validation_change(self) -> None:
        candidates = upgrade_applicability.candidate_features(self.catalog, "1.6.0", "1.6.1")
        reasons = {item["feature_id"]: item["candidate_reasons"] for item in candidates}
        self.assertEqual(set(reasons), {"layered-validation"})
        self.assertEqual(reasons["layered-validation"], ["material_change:1.6.1"])

    def test_identity_feature_explicitly_recommends_adopt_forward(self) -> None:
        feature = self.catalog["features"]["persistent-identity"]
        self.assertEqual(feature["recommendation"]["when_applicable"], "RECOMMENDED")
        self.assertIn("ADOPT_FORWARD", feature["recommendation"]["summary"])
        self.assertIn("durable_planning_identifiers", feature["applicability"]["signals"])

    def test_central_registry_feature_recommends_object_level_merge(self) -> None:
        feature = self.catalog["features"]["central-artifact-registry"]
        self.assertEqual(feature["introduced_in"], "1.6.0")
        self.assertEqual(feature["recommendation"]["when_applicable"], "RECOMMENDED")
        self.assertIn("object/property", feature["recommendation"]["summary"])
        self.assertIn("github_pull_request_workflow", feature["applicability"]["signals"])

    def test_uncovered_transfer_source_is_blocking(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        for feature in catalog["features"].values():
            feature["transfer_sources"] = [source for source in feature["transfer_sources"] if source != "Documentation/Standards/CENTRAL_ARTIFACT_REGISTRY_POLICY.md"]
        codes = {item["code"] for item in feature_catalog_guard.validate_catalog(self.manifest, catalog)}
        self.assertIn("FEATURE_SOURCE_UNCOVERED", codes)

    def test_catalog_version_drift_is_blocking(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["ruleset_version"] = "9.9.9"
        codes = {item["code"] for item in feature_catalog_guard.validate_catalog(self.manifest, catalog)}
        self.assertIn("FEATURE_CATALOG_VERSION", codes)

    def test_unknown_feature_dependency_is_blocking(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["features"]["central-artifact-registry"]["dependencies"].append("missing-feature")
        codes = {item["code"] for item in feature_catalog_guard.validate_catalog(self.manifest, catalog)}
        self.assertIn("FEATURE_DEPENDENCY_UNKNOWN", codes)

    def test_material_change_reenters_delta_but_non_material_does_not(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        feature = catalog["features"]["persistent-identity"]
        feature["change_history"] = [
            {"version": "1.5.0", "impact": "NON_MATERIAL", "summary": "editorial"},
            {"version": "1.6.0", "impact": "MATERIAL", "summary": "semantic change"},
        ]
        reasons = {
            item["feature_id"]: item["candidate_reasons"]
            for item in upgrade_applicability.candidate_features(catalog, "1.3.0", "1.6.0")
        }
        self.assertIn("material_change:1.6.0", reasons["persistent-identity"])
        self.assertNotIn("material_change:1.5.0", reasons["persistent-identity"])


if __name__ == "__main__":
    unittest.main()
