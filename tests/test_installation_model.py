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

    def test_core_semantic_identity_registration_registry_and_upgrade_material_is_installed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target), 0)
            root = target / ".ai" / "foundation"
            expected = [
                "SEMANTIC_INTEGRATION_POLICY.md",
                "PERSISTENT_IDENTITY_POLICY.md",
                "ARTIFACT_REGISTRATION_POLICY.md",
                "CENTRAL_ARTIFACT_REGISTRY_POLICY.md",
                "UPGRADE_APPLICABILITY_POLICY.md",
                "feature_catalog.json",
            ]
            for name in expected:
                self.assertTrue((root / name).is_file(), name)
            self.assertIn("PROJECT_STRONGER", (root / "SEMANTIC_INTEGRATION_POLICY.md").read_text(encoding="utf-8"))
            self.assertIn("ADOPT_FORWARD", (root / "PERSISTENT_IDENTITY_POLICY.md").read_text(encoding="utf-8"))
            self.assertIn("Registration Authority", (root / "ARTIFACT_REGISTRATION_POLICY.md").read_text(encoding="utf-8"))
            central = (root / "CENTRAL_ARTIFACT_REGISTRY_POLICY.md").read_text(encoding="utf-8")
            self.assertIn("next_sequence", central)
            self.assertIn("Object-level three-way merge", central)
            self.assertIn("complete semantic feature delta", (root / "UPGRADE_APPLICABILITY_POLICY.md").read_text(encoding="utf-8"))
            catalog = json.loads((root / "feature_catalog.json").read_text(encoding="utf-8"))
            self.assertEqual(catalog["ruleset_version"], "1.6.0")
            self.assertIn("central-artifact-registry", catalog["features"])
            for name in [
                "artifact-record.schema.json",
                "artifact-registry.schema.json",
                "artifact-registry-v2.schema.json",
                "artifact-registration-request.schema.json",
                "feature-catalog.schema.json",
                "upgrade-assessment.schema.json",
            ]:
                schema = root / "schemas" / name
                self.assertTrue(schema.is_file(), name)
                self.assertEqual(json.loads(schema.read_text(encoding="utf-8"))["$schema"], "https://json-schema.org/draft/2020-12/schema")

    def test_optional_capabilities_are_not_installed_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target), 0)
            self.assertFalse((target / ".ai" / "foundation" / "reference_clients").exists())
            self.assertFalse((target / ".ai" / "foundation" / "artifact_registry_github").exists())
            self.assertFalse((target / ".github" / "workflows" / "artifact-registry-integrity.yml").exists())

    def test_reference_clients_and_github_registry_capabilities_are_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target, "--capabilities", "artifact-registration-clients"), 0)
            client_dir = target / ".ai" / "foundation" / "reference_clients"
            self.assertTrue((client_dir / "artifact_reference.py").is_file())
            self.assertTrue((client_dir / "ArtifactReference.ps1").is_file())
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target, "--capabilities", "artifact-registry-github"), 0)
            self.assertTrue((target / ".ai" / "foundation" / "artifact_registry_github" / "registry_semantic.py").is_file())
            self.assertTrue((target / ".github" / "workflows" / "artifact-registry-integrity.yml").is_file())

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

        registration = self.manifest["registration_contract"]
        self.assertTrue(registration["same_authority_for_humans_and_ai"])
        self.assertFalse(registration["python_required"])
        self.assertEqual(registration["default_registry_profile"], "foundation-artifact-registry/v2")
        self.assertIn("foundation-artifact-registry/v1", registration["compatible_registry_profiles"])

        central = self.manifest["central_registry_contract"]
        self.assertFalse(central["persist_next_sequence"])
        self.assertFalse(central["persist_global_registry_revision"])
        self.assertEqual(central["allocation_derivation"], "max_existing_sequence_plus_one")
        self.assertTrue(central["object_level_three_way_merge_required"])
        self.assertTrue(central["git_merge_result_must_equal_semantic_merge"])
        self.assertTrue(central["cross_pr_preflight_recommended"])

        upgrade = self.manifest["upgrade_contract"]
        self.assertTrue(upgrade["complete_feature_delta_required"])
        self.assertTrue(upgrade["silent_skip_prohibited"])
        self.assertEqual(upgrade["surface_results"], ["RECOMMENDED", "DECISION_REQUIRED", "CONFLICT"])

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
            self.assertIn("PROJECT_REGISTRATION_AUTHORITY_OUT_OF_SCOPE", codes)

    def test_target_validator_covers_selected_reference_client_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target, "--capabilities", "artifact-registration-clients"), 0)
            client = target / ".ai" / "foundation" / "reference_clients" / "ArtifactReference.ps1"
            client.write_text(client.read_text(encoding="utf-8") + "\n# local drift\n", encoding="utf-8")
            output = StringIO()
            with redirect_stdout(output):
                rc = foundation_validator.main(["--target", str(target), "--adapters", "none", "--capabilities", "artifact-registration-clients", "--json"])
            self.assertEqual(rc, 0)
            payload = json.loads(output.getvalue())
            self.assertTrue(any(item["code"] == "LOCAL_OVERRIDE_OR_DRIFT" for item in payload["results"]))

    def test_interoperability_rules_are_explicit(self) -> None:
        project_rules = (ROOT / ".ai" / "PROJECT_RULES.md").read_text(encoding="utf-8")
        integration = (ROOT / "Documentation" / "Standards" / "SEMANTIC_INTEGRATION_POLICY.md").read_text(encoding="utf-8")
        identity = (ROOT / "Documentation" / "Standards" / "PERSISTENT_IDENTITY_POLICY.md").read_text(encoding="utf-8")
        registration = (ROOT / "Documentation" / "Standards" / "ARTIFACT_REGISTRATION_POLICY.md").read_text(encoding="utf-8")
        central = (ROOT / "Documentation" / "Standards" / "CENTRAL_ARTIFACT_REGISTRY_POLICY.md").read_text(encoding="utf-8")
        upgrade = (ROOT / "Documentation" / "Standards" / "UPGRADE_APPLICABILITY_POLICY.md").read_text(encoding="utf-8")
        transfer = (ROOT / "foundation" / "AI_TRANSFER.md").read_text(encoding="utf-8")
        self.assertIn("complete semantic feature delta", project_rules)
        self.assertIn("unknown -> PRESERVE", integration)
        self.assertIn("MIGRATE_EXPLICIT", identity)
        self.assertIn("same authority", registration.lower())
        self.assertIn("object-level", central.lower())
        self.assertIn("silently skipped", upgrade)
        self.assertIn("persistent-identity", transfer)

    def test_v1_bootstrap_compatibility_semantics_remain_intact(self) -> None:
        dry = bootstrap.compatibility_args(["target", "--dry-run"])
        self.assertNotIn("--dry-run", dry)
        self.assertNotIn("--apply", dry)
        apply = bootstrap.compatibility_args(["target"])
        self.assertIn("--apply", apply)

    def test_manifest_sources_exist_targets_unique_and_version_is_v1_6(self) -> None:
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
        self.assertEqual(self.manifest["ruleset_version"], "1.6.0")
        self.assertEqual(self.manifest["installation_scope"], "core_rules_with_opt_in_capabilities")


if __name__ == "__main__":
    unittest.main()
