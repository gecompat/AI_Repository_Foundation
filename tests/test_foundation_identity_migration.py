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
        self.assertEqual(refs, [f"WI-{index:04d}" for index in range(1, 14)])

    def test_registry_contains_all_current_work_items_and_decisions(self) -> None:
        registry = json.loads((ROOT / ".ai" / "identity" / "registry.json").read_text(encoding="utf-8"))
        allocations = registry["allocations"]
        for index in range(1, 14):
            self.assertIn(f"WI-{index:04d}", allocations)
        for index in range(1, 15):
            self.assertIn(f"DEC-{index:04d}", allocations)
        self.assertEqual(len(allocations.values()), len(set(allocations.values())))
        self.assertEqual(registry["prefixes"]["WI"]["next_sequence"], 14)
        self.assertEqual(registry["prefixes"]["DEC"]["next_sequence"], 15)

    def test_historical_fnd_aliases_are_mapped_one_to_one(self) -> None:
        mapping = (ROOT / "Documentation" / "Architecture" / "IDENTIFIER_MIGRATION_2026-08-24.md").read_text(encoding="utf-8")
        for index in range(1, 13):
            self.assertIn(f"`FND-{index:03d}` | `WI-{index:04d}`", mapping)
        self.assertIn("FND-*` aliases are reserved forever", (ROOT / ".ai" / "FOUNDATION.md").read_text(encoding="utf-8"))

    def test_source_project_identity_is_not_transfer_payload(self) -> None:
        manifest = json.loads((ROOT / "foundation" / "manifest.json").read_text(encoding="utf-8"))
        sources = {row["source"] for row in manifest["core"]}
        self.assertNotIn(".ai/identity/registry.json", sources)
        self.assertNotIn("Documentation/Architecture/IDENTIFIER_MIGRATION_2026-08-24.md", sources)
        self.assertIn(".ai/identity/", manifest["never_transfer"])


if __name__ == "__main__":
    unittest.main()
