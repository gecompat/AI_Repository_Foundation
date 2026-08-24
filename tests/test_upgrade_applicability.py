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

    def test_upgrade_from_1_2_surfaces_identity_registration_and_upgrade_assessment(self) -> None:
        candidates = upgrade_applicability.candidate_features(self.catalog, "1.2.0", "1.5.0")
        ids = {item["feature_id"] for item in candidates}
        self.assertIn("persistent-identity", ids)
        self.assertIn("artifact-registration", ids)
        self.assertIn("semantic-upgrade-applicability", ids)
        self.assertIn("semantic-integration", ids)

    def test_upgrade_from_1_4_still_reassesses_material_semantic_integration_change(self) -> None:
        candidates = upgrade_applicability.candidate_features(self.catalog, "1.4.0", "1.5.0")
        reasons = {item["feature_id"]: item["candidate_reasons"] for item in candidates}
        self.assertIn("semantic-upgrade-applicability", reasons)
        self.assertIn("semantic-integration", reasons)
        self.assertIn("material_change:1.5.0", reasons["semantic-integration"])
        self.assertNotIn("persistent-identity", reasons)

    def test_identity_feature_explicitly_recommends_adopt_forward(self) -> None:
        feature = self.catalog["features"]["persistent-identity"]
        self.assertEqual(feature["recommendation"]["when_applicable"], "RECOMMENDED")
        self.assertIn("ADOPT_FORWARD", feature["recommendation"]["summary"])
        self.assertIn("durable_planning_identifiers", feature["applicability"]["signals"])

    def test_uncovered_transfer_source_is_blocking(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        for feature in catalog["features"].values():
            feature["transfer_sources"] = [source for source in feature["transfer_sources"] if source != "Documentation/Standards/PERSISTENT_IDENTITY_POLICY.md"]
        codes = {item["code"] for item in feature_catalog_guard.validate_catalog(self.manifest, catalog)}
        self.assertIn("FEATURE_SOURCE_UNCOVERED", codes)

    def test_catalog_version_drift_is_blocking(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["ruleset_version"] = "9.9.9"
        codes = {item["code"] for item in feature_catalog_guard.validate_catalog(self.manifest, catalog)}
        self.assertIn("FEATURE_CATALOG_VERSION", codes)

    def test_unknown_feature_dependency_is_blocking(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["features"]["artifact-registration"]["dependencies"].append("missing-feature")
        codes = {item["code"] for item in feature_catalog_guard.validate_catalog(self.manifest, catalog)}
        self.assertIn("FEATURE_DEPENDENCY_UNKNOWN", codes)

    def test_material_change_reenters_delta_but_non_material_does_not(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        feature = catalog["features"]["persistent-identity"]
        feature["change_history"] = [
            {"version": "1.4.0", "impact": "NON_MATERIAL", "summary": "editorial"},
            {"version": "1.5.0", "impact": "MATERIAL", "summary": "semantic change"},
        ]
        reasons = {
            item["feature_id"]: item["candidate_reasons"]
            for item in upgrade_applicability.candidate_features(catalog, "1.3.0", "1.5.0")
        }
        self.assertIn("material_change:1.5.0", reasons["persistent-identity"])
        self.assertNotIn("material_change:1.4.0", reasons["persistent-identity"])


if __name__ == "__main__":
    unittest.main()
