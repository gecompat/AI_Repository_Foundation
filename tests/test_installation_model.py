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

    def install(self, target: Path, *extra: str) -> int:
        with redirect_stdout(StringIO()):
            return install_foundation.main([str(target), "--adapters", "none", *extra, "--apply"])

    def test_manifest_transfers_rules_not_foundation_project_artifacts(self) -> None:
        targets = {row["target"] for row in self.manifest["core"]}
        for rows in self.manifest["adapters"].values():
            targets.update(row["target"] for row in rows)
        for rows in self.manifest.get("capabilities", {}).values():
            targets.update(row["target"] for row in rows)
        forbidden = {"README.md", "LICENSE", "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md", ".gitignore"}
        self.assertTrue(targets.isdisjoint(forbidden))
        self.assertFalse(any(path.startswith("Documentation/Architecture/") for path in targets))
        self.assertFalse(any(path.startswith("Documentation/Quality/") for path in targets))
        self.assertNotIn(".ai/identity/registry.json", {row["source"] for row in self.manifest["core"]})

    def test_existing_readme_and_license_are_preserved_and_notice_is_installed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "README.md").write_text("Target README\n", encoding="utf-8")
            (target / "LICENSE").write_text("Target license\n", encoding="utf-8")
            self.assertEqual(self.install(target), 0)
            self.assertEqual((target / "README.md").read_text(encoding="utf-8"), "Target README\n")
            self.assertEqual((target / "LICENSE").read_text(encoding="utf-8"), "Target license\n")
            notice = target / ".ai" / "foundation" / "AI_REPOSITORY_FOUNDATION_NOTICE.md"
            self.assertTrue(notice.is_file())
            self.assertIn((ROOT / "LICENSE").read_text(encoding="utf-8"), notice.read_text(encoding="utf-8"))

    def test_core_semantic_identity_registration_and_upgrade_material_is_installed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target), 0)
            root = target / ".ai" / "foundation"
            expected = [
                "SEMANTIC_INTEGRATION_POLICY.md",
                "PERSISTENT_IDENTITY_POLICY.md",
                "ARTIFACT_REGISTRATION_POLICY.md",
                "UPGRADE_APPLICABILITY_POLICY.md",
                "feature_catalog.json",
            ]
            for name in expected:
                self.assertTrue((root / name).is_file(), name)
            self.assertIn("PROJECT_STRONGER", (root / "SEMANTIC_INTEGRATION_POLICY.md").read_text(encoding="utf-8"))
            self.assertIn("ADOPT_FORWARD", (root / "PERSISTENT_IDENTITY_POLICY.md").read_text(encoding="utf-8"))
            self.assertIn("Registration Authority", (root / "ARTIFACT_REGISTRATION_POLICY.md").read_text(encoding="utf-8"))
            self.assertIn("complete semantic feature delta", (root / "UPGRADE_APPLICABILITY_POLICY.md").read_text(encoding="utf-8"))
            catalog = json.loads((root / "feature_catalog.json").read_text(encoding="utf-8"))
            self.assertEqual(catalog["ruleset_version"], "1.5.0")
            self.assertIn("persistent-identity", catalog["features"])
            for name in [
                "artifact-record.schema.json",
                "artifact-registry.schema.json",
                "artifact-registration-request.schema.json",
                "feature-catalog.schema.json",
                "upgrade-assessment.schema.json",
            ]:
                schema = root / "schemas" / name
                self.assertTrue(schema.is_file(), name)
                self.assertEqual(json.loads(schema.read_text(encoding="utf-8"))["$schema"], "https://json-schema.org/draft/2020-12/schema")

    def test_reference_clients_are_opt_in_capability(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target), 0)
            self.assertFalse((target / ".ai" / "foundation" / "reference_clients").exists())
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target, "--capabilities", "artifact-registration-clients"), 0)
            client_dir = target / ".ai" / "foundation" / "reference_clients"
            self.assertTrue((client_dir / "artifact_reference.py").is_file())
            self.assertTrue((client_dir / "ArtifactReference.ps1").is_file())

    def test_second_install_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target), 0)
            self.assertEqual(self.install(target), 0)
            entries = install_foundation.transfer_entries(self.manifest, [])
            self.assertTrue(all(item.state == "UNCHANGED" for item in install_foundation.build_plan(target, entries)))

    def test_existing_agents_conflict_is_transactional(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "AGENTS.md").write_text("# Existing project rules\n", encoding="utf-8")
            self.assertEqual(self.install(target), 2)
            self.assertFalse((target / ".ai" / "foundation" / "FOUNDATION_RULESET.md").exists())
            self.assertEqual((target / "AGENTS.md").read_text(encoding="utf-8"), "# Existing project rules\n")

    def test_attribution_manifest_and_target_validation_preserve_complete_notice(self) -> None:
        attribution = self.manifest["attribution"]
        rows = [row for row in self.manifest["core"] if row.get("kind") == "attribution"]
        self.assertTrue(attribution["required"])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["source"], attribution["source"])
        self.assertEqual(rows[0]["target"], attribution["target"])
        self.assertNotEqual(attribution["target"], "LICENSE")
        source_text = (ROOT / attribution["source"]).read_text(encoding="utf-8")
        self.assertIn((ROOT / "LICENSE").read_text(encoding="utf-8"), source_text)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target), 0)
            notice = target / ".ai" / "foundation" / "AI_REPOSITORY_FOUNDATION_NOTICE.md"
            notice.write_text("# Incomplete notice\n", encoding="utf-8")
            with redirect_stdout(StringIO()):
                rc = foundation_validator.main(["--target", str(target), "--adapters", "none"])
            self.assertEqual(rc, 2)

    def test_machine_readable_contracts_are_consistent(self) -> None:
        validation = self.manifest["validation_contract"]
        self.assertEqual(validation["foundation_validator_scope"], "FOUNDATION_INTEGRITY")
        self.assertEqual(validation["project_semantic_authority"], "target_repository")
        self.assertTrue(validation["foundation_green_does_not_imply_project_green"])

        integration = self.manifest["integration_contract"]
        self.assertTrue(integration["project_governance_must_be_transitively_discoverable"])
        self.assertEqual(integration["stricter_project_rules"], "compatible")
        self.assertIn("ORPHANED_AUTHORITY", integration["compatibility_classes"])

        identity = self.manifest["identity_contract"]
        self.assertEqual(identity["default_machine_identifier"], "rfc9562_uuidv7_as_urn_uuid")
        self.assertEqual(identity["adoption_modes"], ["PRESERVE", "ADOPT_FORWARD", "MIGRATE_EXPLICIT"])
        self.assertEqual(identity["unknown_existing_project_choice"], "PRESERVE")

        registration = self.manifest["registration_contract"]
        self.assertTrue(registration["same_authority_for_humans_and_ai"])
        self.assertFalse(registration["python_required"])
        self.assertTrue(registration["powershell_supported"])
        self.assertEqual(registration["allocation_modes"], ["DIRECT", "DEFERRED"])

        upgrade = self.manifest["upgrade_contract"]
        self.assertTrue(upgrade["complete_feature_delta_required"])
        self.assertTrue(upgrade["silent_skip_prohibited"])
        self.assertEqual(upgrade["surface_results"], ["RECOMMENDED", "DECISION_REQUIRED", "CONFLICT"])
        self.assertEqual(upgrade["feature_catalog_target"], ".ai/foundation/feature_catalog.json")

        routing = self.manifest["model_routing_contract"]
        self.assertEqual(routing["foundation_tiers"], ["LOCAL", "ECONOMICAL", "BALANCED", "FRONTIER"])
        self.assertTrue(routing["target_policy_may_be_more_detailed"])

    def test_target_validator_declares_foundation_integrity_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target), 0)
            output = StringIO()
            with redirect_stdout(output):
                rc = foundation_validator.main(["--target", str(target), "--adapters", "none", "--json"])
            self.assertEqual(rc, 0)
            payload = json.loads(output.getvalue())
            self.assertEqual(payload["validation_scope"], "FOUNDATION_INTEGRITY")
            codes = {item["code"] for item in payload["results"]}
            self.assertIn("PROJECT_VALIDATION_OUT_OF_SCOPE", codes)
            self.assertIn("PROJECT_GOVERNANCE_DISCOVERY_SEMANTIC", codes)
            self.assertIn("PROJECT_IDENTITY_SEMANTICS_OUT_OF_SCOPE", codes)
            self.assertIn("PROJECT_REGISTRATION_AUTHORITY_OUT_OF_SCOPE", codes)

    def test_target_validator_covers_selected_reference_client_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target, "--capabilities", "artifact-registration-clients"), 0)
            client = target / ".ai" / "foundation" / "reference_clients" / "ArtifactReference.ps1"
            client.write_text(client.read_text(encoding="utf-8") + "\n# local drift\n", encoding="utf-8")
            output = StringIO()
            with redirect_stdout(output):
                rc = foundation_validator.main([
                    "--target", str(target), "--adapters", "none", "--capabilities", "artifact-registration-clients", "--json"
                ])
            self.assertEqual(rc, 0)
            payload = json.loads(output.getvalue())
            self.assertTrue(any(item["code"] == "LOCAL_OVERRIDE_OR_DRIFT" for item in payload["results"]))

    def test_local_override_is_drift_not_semantic_approval(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target), 0)
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

    def test_interoperability_rules_are_explicit(self) -> None:
        project_rules = (ROOT / ".ai" / "PROJECT_RULES.md").read_text(encoding="utf-8")
        integration = (ROOT / "Documentation" / "Standards" / "SEMANTIC_INTEGRATION_POLICY.md").read_text(encoding="utf-8")
        identity = (ROOT / "Documentation" / "Standards" / "PERSISTENT_IDENTITY_POLICY.md").read_text(encoding="utf-8")
        registration = (ROOT / "Documentation" / "Standards" / "ARTIFACT_REGISTRATION_POLICY.md").read_text(encoding="utf-8")
        upgrade = (ROOT / "Documentation" / "Standards" / "UPGRADE_APPLICABILITY_POLICY.md").read_text(encoding="utf-8")
        transfer = (ROOT / "foundation" / "AI_TRANSFER.md").read_text(encoding="utf-8")
        self.assertIn("complete semantic feature delta", project_rules)
        self.assertIn("unknown -> PRESERVE", integration)
        self.assertIn("MIGRATE_EXPLICIT", identity)
        self.assertIn("same authority", registration.lower())
        self.assertIn("silently skipped", upgrade)
        self.assertIn("persistent-identity", transfer)
        self.assertIn("ADOPT_FORWARD", transfer)

    def test_v1_bootstrap_compatibility_semantics_remain_intact(self) -> None:
        dry = bootstrap.compatibility_args(["target", "--dry-run"])
        self.assertNotIn("--dry-run", dry)
        self.assertNotIn("--apply", dry)
        apply = bootstrap.compatibility_args(["target"])
        self.assertIn("--apply", apply)

    def test_manifest_sources_exist_targets_unique_and_version_is_v1_5(self) -> None:
        rows = list(self.manifest["core"])
        for adapter_rows in self.manifest["adapters"].values():
            rows.extend(adapter_rows)
        for capability_rows in self.manifest.get("capabilities", {}).values():
            rows.extend(capability_rows)
        targets = [row["target"] for row in rows]
        self.assertEqual(len(targets), len(set(targets)))
        for row in rows:
            self.assertTrue((ROOT / row["source"]).is_file(), row["source"])
        self.assertEqual(self.manifest["schema_version"], 1)
        self.assertEqual(self.manifest["ruleset_version"], "1.5.0")
        self.assertEqual(self.manifest["installation_scope"], "core_rules_with_opt_in_capabilities")


if __name__ == "__main__":
    unittest.main()
