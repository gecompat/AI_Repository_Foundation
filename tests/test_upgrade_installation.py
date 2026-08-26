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
    def test_installed_repo_map_exposes_upgrade_central_registry_and_eol_contracts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            with redirect_stdout(StringIO()):
                rc = install_foundation.main([str(target), "--adapters", "none", "--apply"])
            self.assertEqual(rc, 0)
            repo_map = (target / ".ai" / "foundation" / "repo_map.yaml").read_text(encoding="utf-8")
            self.assertIn("upgrade_contract:", repo_map)
            self.assertIn("feature_catalog: .ai/foundation/feature_catalog.json", repo_map)
            self.assertIn("silent_skip_prohibited: true", repo_map)
            self.assertIn("central_registry_contract:", repo_map)
            self.assertIn("default_registry_profile: foundation-artifact-registry/v2", repo_map)
            self.assertIn("persist_next_sequence: false", repo_map)
            self.assertIn("object_level_three_way_merge_required: true", repo_map)
            self.assertIn("utf8_crlf_lf_equivalent: true", repo_map)
            self.assertIn("binary_byte_exact: true", repo_map)
            self.assertIn("preserve_project_policy_do_not_create_for_eol_only_foundation_drift", repo_map)

    def test_feature_catalog_and_manifest_versions_match(self) -> None:
        manifest = json.loads((ROOT / "foundation" / "manifest.json").read_text(encoding="utf-8"))
        catalog = json.loads((ROOT / "foundation" / "feature_catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["ruleset_version"], catalog["ruleset_version"])
        self.assertEqual(manifest["ruleset_version"], "1.6.1")

    def test_1_2_to_1_6_1_delta_surfaces_nomenclature_registry_and_eol_fix(self) -> None:
        catalog = json.loads((ROOT / "foundation" / "feature_catalog.json").read_text(encoding="utf-8"))
        candidates = upgrade_applicability.candidate_features(catalog, "1.2.0", "1.6.1")
        by_id = {item["feature_id"]: item for item in candidates}
        identity = by_id["persistent-identity"]
        self.assertIn("durable_planning_identifiers", identity["applicability"]["signals"])
        self.assertIn("ADOPT_FORWARD", identity["recommendation"]["summary"])
        central = by_id["central-artifact-registry"]
        self.assertIn("json_file_registration_authority", central["applicability"]["signals"])
        self.assertIn("object/property", central["recommendation"]["summary"])
        self.assertIn("material_change:1.6.1", by_id["layered-validation"]["candidate_reasons"])


if __name__ == "__main__":
    unittest.main()
