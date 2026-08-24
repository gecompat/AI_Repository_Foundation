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
    def test_installed_repo_map_exposes_upgrade_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            with redirect_stdout(StringIO()):
                rc = install_foundation.main([str(target), "--adapters", "none", "--apply"])
            self.assertEqual(rc, 0)
            repo_map = (target / ".ai" / "foundation" / "repo_map.yaml").read_text(encoding="utf-8")
            self.assertIn("upgrade_contract:", repo_map)
            self.assertIn("feature_catalog: .ai/foundation/feature_catalog.json", repo_map)
            self.assertIn("silent_skip_prohibited: true", repo_map)
            self.assertIn("RECOMMENDED_DECISION_REQUIRED_CONFLICT", repo_map)

    def test_feature_catalog_and_manifest_versions_match(self) -> None:
        manifest = json.loads((ROOT / "foundation" / "manifest.json").read_text(encoding="utf-8"))
        catalog = json.loads((ROOT / "foundation" / "feature_catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["ruleset_version"], catalog["ruleset_version"])
        self.assertEqual(manifest["ruleset_version"], "1.5.0")

    def test_1_2_to_1_5_delta_forces_nomenclature_candidate(self) -> None:
        catalog = json.loads((ROOT / "foundation" / "feature_catalog.json").read_text(encoding="utf-8"))
        candidates = upgrade_applicability.candidate_features(catalog, "1.2.0", "1.5.0")
        identity = next(item for item in candidates if item["feature_id"] == "persistent-identity")
        self.assertIn("durable_planning_identifiers", identity["applicability"]["signals"])
        self.assertIn("ADOPT_FORWARD", identity["recommendation"]["summary"])


if __name__ == "__main__":
    unittest.main()
