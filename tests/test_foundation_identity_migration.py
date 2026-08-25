from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FoundationIdentityMigrationTests(unittest.TestCase):
    def test_active_backlog_uses_registered_work_item_references(self) -> None:
        backlog = (ROOT / ".ai" / "BACKLOG.md").read_text(encoding="utf-8")
        self.assertNotRegex(backlog, r"(?m)^\| FND-[0-9]+ \|")
        refs = re.findall(r"(?m)^\| (WI-[0-9]{4}) \|", backlog)
        self.assertEqual(refs, [f"WI-{index:04d}" for index in range(1, 15)])

    def test_registry_contains_complete_v2_work_items_and_decisions(self) -> None:
        registry = json.loads((ROOT / ".ai" / "identity" / "registry.json").read_text(encoding="utf-8"))
        self.assertEqual(registry["schema_version"], 2)
        self.assertEqual(registry["profile"], "foundation-artifact-registry/v2")
        self.assertNotIn("registry_revision", registry)
        self.assertTrue(all("next_sequence" not in row for row in registry["prefixes"].values()))
        artifacts = registry["artifacts"]
        for index in range(1, 15):
            ref = f"WI-{index:04d}"
            self.assertIn(ref, artifacts)
            self.assertNotIn("human_ref", artifacts[ref])
            self.assertEqual(artifacts[ref]["kind"], "work_item")
        for index in range(1, 16):
            ref = f"DEC-{index:04d}"
            self.assertIn(ref, artifacts)
            self.assertNotIn("human_ref", artifacts[ref])
            self.assertEqual(artifacts[ref]["kind"], "decision")
        uids = [record["artifact_uid"] for record in artifacts.values()]
        self.assertEqual(len(uids), len(set(uids)))

    def test_historical_fnd_aliases_are_mapped_one_to_one(self) -> None:
        mapping_path = ROOT / "Documentation" / "Architecture" / "IDENTIFIER_MIGRATION_2026-08-24.md"
        mapping = mapping_path.read_text(encoding="utf-8")
        registry = json.loads((ROOT / ".ai" / "identity" / "registry.json").read_text(encoding="utf-8"))
        for index in range(1, 13):
            self.assertIn(f"`FND-{index:03d}` | `WI-{index:04d}`", mapping)
            self.assertIn(f"FND-{index:03d}", registry["artifacts"][f"WI-{index:04d}"]["aliases"])
        repo_map = (ROOT / ".ai" / "repo_map.yaml").read_text(encoding="utf-8")
        self.assertIn("registry_profile: foundation-artifact-registry/v2", repo_map)
        self.assertIn("persist_next_sequence: false", repo_map)
        self.assertIn("migration_mode: MIGRATE_EXPLICIT", repo_map)

    def test_source_project_identity_is_not_transfer_payload(self) -> None:
        manifest = json.loads((ROOT / "foundation" / "manifest.json").read_text(encoding="utf-8"))
        sources = {row["source"] for row in manifest["core"]}
        self.assertNotIn(".ai/identity/registry.json", sources)
        self.assertNotIn("Documentation/Architecture/IDENTIFIER_MIGRATION_2026-08-24.md", sources)
        self.assertIn(".ai/identity/", manifest["never_transfer"])


if __name__ == "__main__":
    unittest.main()
