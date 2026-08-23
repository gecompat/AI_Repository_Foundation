from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import bootstrap  # noqa: E402
import install_foundation  # noqa: E402


class InstallationModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = install_foundation.load_manifest()

    def test_manifest_transfers_rules_not_foundation_project_artifacts(self) -> None:
        targets = {row["target"] for row in self.manifest["core"]}
        for rows in self.manifest["adapters"].values():
            targets.update(row["target"] for row in rows)
        forbidden = {"README.md", "LICENSE", "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md", ".gitignore"}
        self.assertTrue(targets.isdisjoint(forbidden))
        self.assertFalse(any(path.startswith("Documentation/Architecture/") for path in targets))
        self.assertFalse(any(path.startswith("Documentation/Quality/") for path in targets))

    def test_existing_readme_and_license_do_not_block_installation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "README.md").write_text("Target README\n", encoding="utf-8")
            (target / "LICENSE").write_text("Target license\n", encoding="utf-8")
            entries = install_foundation.transfer_entries(self.manifest, [])
            plan = install_foundation.build_plan(target, entries)
            self.assertFalse(any(item.state in {"MERGE_REQUIRED", "CONFLICT"} for item in plan))
            self.assertEqual((target / "README.md").read_text(encoding="utf-8"), "Target README\n")
            self.assertEqual((target / "LICENSE").read_text(encoding="utf-8"), "Target license\n")

    def test_second_install_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            with redirect_stdout(StringIO()):
                first = install_foundation.main([str(target), "--adapters", "none", "--apply"])
                second = install_foundation.main([str(target), "--adapters", "none", "--apply"])
            self.assertEqual(first, 0)
            self.assertEqual(second, 0)
            entries = install_foundation.transfer_entries(self.manifest, [])
            self.assertTrue(all(item.state == "UNCHANGED" for item in install_foundation.build_plan(target, entries)))

    def test_existing_agents_conflict_is_transactional(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "AGENTS.md").write_text("# Existing project rules\n", encoding="utf-8")
            with redirect_stdout(StringIO()):
                rc = install_foundation.main([str(target), "--adapters", "none", "--apply"])
            self.assertEqual(rc, 2)
            self.assertFalse((target / ".ai" / "foundation" / "FOUNDATION_RULESET.md").exists())
            self.assertEqual((target / "AGENTS.md").read_text(encoding="utf-8"), "# Existing project rules\n")

    def test_v1_bootstrap_dry_run_remains_preview_only(self) -> None:
        args = bootstrap.compatibility_args(["target", "--dry-run"])
        self.assertNotIn("--dry-run", args)
        self.assertNotIn("--apply", args)

    def test_v1_bootstrap_without_dry_run_preserves_apply_semantics(self) -> None:
        args = bootstrap.compatibility_args(["target"])
        self.assertIn("--apply", args)

    def test_manifest_sources_exist_and_targets_are_unique(self) -> None:
        rows = list(self.manifest["core"])
        for adapter_rows in self.manifest["adapters"].values():
            rows.extend(adapter_rows)
        targets = [row["target"] for row in rows]
        self.assertEqual(len(targets), len(set(targets)))
        for row in rows:
            self.assertTrue((ROOT / row["source"]).is_file(), row["source"])

    def test_manifest_is_machine_readable(self) -> None:
        parsed = json.loads((ROOT / "foundation" / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(parsed["schema_version"], 1)
        self.assertEqual(parsed["ruleset_version"], "1.1.0")


if __name__ == "__main__":
    unittest.main()
