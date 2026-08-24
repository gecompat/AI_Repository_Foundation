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
        for rows in self.manifest.get("capabilities", {}).values():
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

    def test_semantic_integration_policy_is_installed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            with redirect_stdout(StringIO()):
                rc = install_foundation.main([str(target), "--adapters", "none", "--apply"])
            self.assertEqual(rc, 0)
            policy = target / ".ai" / "foundation" / "SEMANTIC_INTEGRATION_POLICY.md"
            self.assertTrue(policy.is_file())
            self.assertIn("PROJECT_STRONGER", policy.read_text(encoding="utf-8"))

    def test_persistent_identity_policy_is_installed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            with redirect_stdout(StringIO()):
                rc = install_foundation.main([str(target), "--adapters", "none", "--apply"])
            self.assertEqual(rc, 0)
            policy = target / ".ai" / "foundation" / "PERSISTENT_IDENTITY_POLICY.md"
            self.assertTrue(policy.is_file())
            text = policy.read_text(encoding="utf-8")
            self.assertIn("PRESERVE", text)
            self.assertIn("ADOPT_FORWARD", text)
            self.assertIn("MIGRATE_EXPLICIT", text)
            self.assertIn("urn:uuid:<uuid>", text)

    def test_artifact_registration_policy_and_schemas_are_core(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            with redirect_stdout(StringIO()):
                rc = install_foundation.main([str(target), "--adapters", "none", "--apply"])
            self.assertEqual(rc, 0)
            policy = target / ".ai" / "foundation" / "ARTIFACT_REGISTRATION_POLICY.md"
            self.assertTrue(policy.is_file())
            text = policy.read_text(encoding="utf-8")
            self.assertIn("Registration Authority", text)
            self.assertIn("Humans and AI systems MUST use the same authority", text)
            self.assertIn("Python", text)
            self.assertIn("PowerShell", text)
            for name in [
                "artifact-record.schema.json",
                "artifact-registry.schema.json",
                "artifact-registration-request.schema.json",
            ]:
                schema = target / ".ai" / "foundation" / "schemas" / name
                self.assertTrue(schema.is_file(), name)
                self.assertEqual(json.loads(schema.read_text(encoding="utf-8"))["$schema"], "https://json-schema.org/draft/2020-12/schema")

    def test_reference_clients_are_opt_in_capability(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            with redirect_stdout(StringIO()):
                self.assertEqual(install_foundation.main([str(target), "--adapters", "none", "--apply"]), 0)
            client_dir = target / ".ai" / "foundation" / "reference_clients"
            self.assertFalse(client_dir.exists())

        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            with redirect_stdout(StringIO()):
                rc = install_foundation.main([
                    str(target), "--adapters", "none", "--capabilities", "artifact-registration-clients", "--apply"
                ])
            self.assertEqual(rc, 0)
            client_dir = target / ".ai" / "foundation" / "reference_clients"
            self.assertTrue((client_dir / "artifact_reference.py").is_file())
            self.assertTrue((client_dir / "ArtifactReference.ps1").is_file())

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
        self.assertTrue(contract["target_status_extensions_allowed"])
        self.assertTrue(contract["reserved_statuses_may_not_be_redefined"])
        self.assertEqual(contract["foundation_reserved_statuses"], ["not executed", "pending manual validation", "validated"])

    def test_semantic_integration_contract_is_machine_readable(self) -> None:
        contract = self.manifest["integration_contract"]
        self.assertTrue(contract["project_governance_must_be_transitively_discoverable"])
        self.assertEqual(contract["stricter_project_rules"], "compatible")
        self.assertFalse(contract["existing_project_rule_labels_required"])
        self.assertEqual(contract["adapter_governance_migration"], "preserve_then_rehome_then_thin")
        self.assertEqual(contract["project_repo_map_behavior"], "preserve_and_optionally_bridge")
        self.assertTrue(contract["orphaned_authority_is_integration_defect"])
        self.assertEqual(
            contract["compatibility_classes"],
            [
                "EQUIVALENT",
                "PROJECT_STRONGER",
                "PROJECT_SELECTABLE_OVERRIDE",
                "COMPLEMENTARY",
                "DUPLICATE_GOVERNANCE",
                "FOUNDATION_REQUIRED_CONFLICT",
                "TARGET_INTERNAL_CONFLICT",
                "ORPHANED_AUTHORITY",
                "ADAPTER_GOVERNANCE_MISPLACED",
            ],
        )

    def test_identity_contract_is_machine_readable(self) -> None:
        contract = self.manifest["identity_contract"]
        self.assertEqual(contract["policy_target"], ".ai/foundation/PERSISTENT_IDENTITY_POLICY.md")
        self.assertEqual(contract["default_machine_identifier"], "rfc9562_uuidv7_as_urn_uuid")
        self.assertEqual(contract["compatible_uuid_profiles"], ["uuidv7", "uuidv4"])
        self.assertEqual(contract["default_human_reference"], "flat_typed_project_local")
        self.assertEqual(contract["default_human_reference_pattern"], "<PREFIX>-<SEQUENCE>")
        self.assertEqual(contract["existing_project_default_mode"], "PRESERVE")
        self.assertEqual(contract["new_project_default_mode"], "FOUNDATION_DEFAULT")
        self.assertEqual(contract["adoption_modes"], ["PRESERVE", "ADOPT_FORWARD", "MIGRATE_EXPLICIT"])
        self.assertTrue(contract["migration_requires_explicit_decision"])
        self.assertEqual(contract["unknown_existing_project_choice"], "PRESERVE")
        self.assertEqual(contract["hierarchy_and_status"], "metadata_not_canonical_identity")
        self.assertEqual(contract["content_hash_scope"], "immutable_revision_or_content")
        self.assertIn("legacy_identifier_preservation", contract["required_invariants"])
        self.assertIn("identifiers_are_not_authorization", contract["required_invariants"])

    def test_registration_contract_is_machine_readable(self) -> None:
        contract = self.manifest["registration_contract"]
        self.assertEqual(contract["policy_target"], ".ai/foundation/ARTIFACT_REGISTRATION_POLICY.md")
        self.assertTrue(contract["same_authority_for_humans_and_ai"])
        self.assertEqual(contract["implementation_language"], "project_selectable")
        self.assertFalse(contract["python_required"])
        self.assertTrue(contract["powershell_supported"])
        self.assertEqual(contract["allocation_modes"], ["DIRECT", "DEFERRED"])
        self.assertTrue(contract["direct_requires_serialized_or_equivalent_unique_allocation"])
        self.assertTrue(contract["deferred_uid_is_final_before_human_reference"])
        self.assertTrue(contract["final_human_reference_must_be_authority_allocated"])
        self.assertEqual(contract["reference_clients"], "optional_capability")
        self.assertTrue(contract["reference_clients_must_match_shared_contract"])
        self.assertEqual(self.manifest["default_capabilities"], [])

    def test_model_routing_contract_preserves_richer_project_policy(self) -> None:
        contract = self.manifest["model_routing_contract"]
        self.assertEqual(contract["foundation_tiers"], ["LOCAL", "ECONOMICAL", "BALANCED", "FRONTIER"])
        self.assertTrue(contract["target_policy_may_be_more_detailed"])
        self.assertTrue(contract["semantic_mapping_required_when_overlapping"])
        self.assertTrue(contract["concrete_models_are_runtime_facts"])

    def test_agents_bridge_declares_project_governance_discovery(self) -> None:
        text = (ROOT / "foundation" / "AGENTS.template.md").read_text(encoding="utf-8")
        self.assertIn("transitively discoverable", text)
        self.assertIn("SEMANTIC_INTEGRATION_POLICY.md", text)
        self.assertIn("outside this managed Foundation block", text)

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
            self.assertIn("PROJECT_GOVERNANCE_DISCOVERY_SEMANTIC", codes)
            self.assertIn("PROJECT_IDENTITY_SEMANTICS_OUT_OF_SCOPE", codes)
            self.assertIn("PROJECT_REGISTRATION_AUTHORITY_OUT_OF_SCOPE", codes)

    def test_target_validator_covers_selected_reference_clients(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            with redirect_stdout(StringIO()):
                self.assertEqual(install_foundation.main([
                    str(target), "--adapters", "none", "--capabilities", "artifact-registration-clients", "--apply"
                ]), 0)
            output = StringIO()
            with redirect_stdout(output):
                rc = foundation_validator.main([
                    "--target", str(target), "--adapters", "none", "--capabilities", "artifact-registration-clients", "--json"
                ])
            self.assertEqual(rc, 0)
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

    def test_interoperability_rules_are_explicit(self) -> None:
        project_rules = (ROOT / ".ai" / "PROJECT_RULES.md").read_text(encoding="utf-8")
        validation = (ROOT / ".ai" / "VALIDATION_POLICY.md").read_text(encoding="utf-8")
        routing = (ROOT / ".ai" / "MODEL_ROUTING_POLICY.md").read_text(encoding="utf-8")
        privacy = (ROOT / "Documentation" / "Standards" / "DATA_PRIVACY_AND_CONFIDENTIALITY.md").read_text(encoding="utf-8")
        integration = (ROOT / "Documentation" / "Standards" / "SEMANTIC_INTEGRATION_POLICY.md").read_text(encoding="utf-8")
        identity = (ROOT / "Documentation" / "Standards" / "PERSISTENT_IDENTITY_POLICY.md").read_text(encoding="utf-8")
        registration = (ROOT / "Documentation" / "Standards" / "ARTIFACT_REGISTRATION_POLICY.md").read_text(encoding="utf-8")
        transfer = (ROOT / "foundation" / "AI_TRANSFER.md").read_text(encoding="utf-8")
        self.assertIn("project may be stricter", project_rules)
        self.assertIn("Target repositories may define additional statuses", validation)
        self.assertIn("Preserve it when it is compatible", routing)
        self.assertIn("AI_REPOSITORY_FOUNDATION_NOTICE.md", privacy)
        self.assertIn("unknown -> PRESERVE", integration)
        self.assertIn("MIGRATE_EXPLICIT", identity)
        self.assertIn("same authority", registration.lower())
        self.assertIn("Missing input means `PRESERVE`", transfer)
        self.assertIn("ADAPTER_GOVERNANCE_MISPLACED", transfer)
        self.assertIn("ORPHANED_AUTHORITY", transfer)

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
        for capability_rows in self.manifest.get("capabilities", {}).values():
            rows.extend(capability_rows)
        targets = [row["target"] for row in rows]
        self.assertEqual(len(targets), len(set(targets)))
        for row in rows:
            self.assertTrue((ROOT / row["source"]).is_file(), row["source"])

    def test_manifest_is_machine_readable(self) -> None:
        parsed = json.loads((ROOT / "foundation" / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(parsed["schema_version"], 1)
        self.assertEqual(parsed["ruleset_version"], "1.4.0")
        self.assertEqual(parsed["installation_scope"], "core_rules_with_opt_in_capabilities")


if __name__ == "__main__":
    unittest.main()
