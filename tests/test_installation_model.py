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
import foundation_validator  # noqa: E402
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

    def test_existing_readme_and_license_are_preserved_and_notice_is_installed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "README.md").write_text("Target README\n", encoding="utf-8")
            (target / "LICENSE").write_text("Target license\n", encoding="utf-8")
            with redirect_stdout(StringIO()):
                rc = install_foundation.main([str(target), "--adapters", "none", "--apply"])
            self.assertEqual(rc, 0)
            self.assertEqual((target / "README.md").read_text(encoding="utf-8"), "Target README\n")
            self.assertEqual((target / "LICENSE").read_text(encoding="utf-8"), "Target license\n")
            notice = target / ".ai" / "foundation" / "AI_REPOSITORY_FOUNDATION_NOTICE.md"
            self.assertTrue(notice.is_file())
            self.assertIn((ROOT / "LICENSE").read_text(encoding="utf-8"), notice.read_text(encoding="utf-8"))

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
            self.assertFalse((target / ".ai" / "foundation" / "AI_REPOSITORY_FOUNDATION_NOTICE.md").exists())
            self.assertEqual((target / "AGENTS.md").read_text(encoding="utf-8"), "# Existing project rules\n")

    def test_attribution_manifest_and_source_preserve_complete_mit_notice(self) -> None:
        attribution = self.manifest["attribution"]
        self.assertTrue(attribution["required"])
        self.assertNotEqual(attribution["target"], "LICENSE")
        rows = [row for row in self.manifest["core"] if row.get("kind") == "attribution"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["source"], attribution["source"])
        self.assertEqual(rows[0]["target"], attribution["target"])
        source_text = (ROOT / attribution["source"]).read_text(encoding="utf-8")
        self.assertIn((ROOT / "LICENSE").read_text(encoding="utf-8"), source_text)

    def test_target_validator_blocks_tampered_attribution_notice(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            with redirect_stdout(StringIO()):
                self.assertEqual(install_foundation.main([str(target), "--adapters", "none", "--apply"]), 0)
            notice = target / ".ai" / "foundation" / "AI_REPOSITORY_FOUNDATION_NOTICE.md"
            notice.write_text("# Incomplete notice\n", encoding="utf-8")
            with redirect_stdout(StringIO()):
                rc = foundation_validator.main(["--target", str(target), "--adapters", "none"])
            self.assertEqual(rc, 2)

    def test_validation_contract_is_machine_readable(self) -> None:
        contract = self.manifest["validation_contract"]
        self.assertEqual(contract["foundation_validator_scope"], "FOUNDATION_INTEGRITY")
        self.assertEqual(contract["project_semantic_authority"], "target_repository")
        self.assertEqual(contract["runtime_empirical_authority"], "target_repository")
        self.assertEqual(contract["completion"], "impact_based_combination")
        self.assertTrue(contract["foundation_green_does_not_imply_project_green"])

    def test_target_validator_declares_foundation_integrity_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            with redirect_stdout(StringIO()):
                self.assertEqual(install_foundation.main([str(target), "--adapters", "none", "--apply"]), 0)
            output = StringIO()
            with redirect_stdout(output):
                rc = foundation_validator.main(["--target", str(target), "--adapters", "none", "--json"])
            self.assertEqual(rc, 0)
            payload = json.loads(output.getvalue())
            self.assertEqual(payload["validation_scope"], "FOUNDATION_INTEGRITY")
            codes = {item["code"] for item in payload["results"]}
            self.assertIn("PROJECT_VALIDATION_OUT_OF_SCOPE", codes)

    def test_local_override_is_drift_not_semantic_approval(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            with redirect_stdout(StringIO()):
                self.assertEqual(install_foundation.main([str(target), "--adapters", "none", "--apply"]), 0)
            policy = target / ".ai" / "foundation" / "DOCUMENTATION_POLICY.md"
            policy.write_text(policy.read_text(encoding="utf-8") + "\n# Target-specific compatible override\n", encoding="utf-8")
            output = StringIO()
            with redirect_stdout(output):
                rc = foundation_validator.main(["--target", str(target), "--adapters", "none", "--json"])
            self.assertEqual(rc, 0)
            payload = json.loads(output.getvalue())
            drift = [item for item in payload["results"] if item["code"] == "LOCAL_OVERRIDE_OR_DRIFT"]
            self.assertTrue(drift)
            self.assertIn("does not establish semantic correctness", drift[0]["message"])

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
        self.assertEqual(parsed["ruleset_version"], "1.1.2")


if __name__ == "__main__":
    unittest.main()
