from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FoundationIdentityMigrationTests(unittest.TestCase):
    def registry(self) -> dict:
        return json.loads((ROOT / ".ai" / "identity" / "registry.json").read_text(encoding="utf-8"))

    def test_active_backlog_uses_registered_work_item_references(self) -> None:
        backlog = (ROOT / ".ai" / "BACKLOG.md").read_text(encoding="utf-8")
        self.assertNotRegex(backlog, r"(?m)^\| FND-[0-9]+ \|")
        refs = re.findall(r"(?m)^\| (WI-[0-9]{4}) \|", backlog)
        registry_refs = sorted(
            ref
            for ref, record in self.registry()["artifacts"].items()
            if record.get("kind") == "work_item"
        )
        self.assertEqual(refs, registry_refs)
        self.assertIn("WI-0015", refs)

    def test_registry_contains_complete_v2_work_items_and_decisions(self) -> None:
        registry = self.registry()
        self.assertEqual(registry["schema_version"], 2)
        self.assertEqual(registry["profile"], "foundation-artifact-registry/v2")
        self.assertNotIn("registry_revision", registry)
        self.assertTrue(all("next_sequence" not in row for row in registry["prefixes"].values()))
        artifacts = registry["artifacts"]
        self.assertIn("WI-0015", artifacts)
        self.assertIn("DEC-0016", artifacts)
        for ref, record in artifacts.items():
            self.assertNotIn("human_ref", record)
            prefix = ref.split("-", 1)[0]
            if prefix in registry["prefixes"]:
                self.assertEqual(record["kind"], registry["prefixes"][prefix]["kind"])
        uids = [record["artifact_uid"] for record in artifacts.values()]
        self.assertEqual(len(uids), len(set(uids)))

    def test_historical_fnd_aliases_are_mapped_one_to_one(self) -> None:
        mapping_path = ROOT / "Documentation" / "Architecture" / "IDENTIFIER_MIGRATION_2026-08-24.md"
        mapping = mapping_path.read_text(encoding="utf-8")
        registry = self.registry()
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
