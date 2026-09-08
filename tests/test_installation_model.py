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
        self.assertIn("tools/content_equivalence.py", self.manifest["never_transfer"])

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

    def test_core_semantic_identity_registration_registry_upgrade_eol_cache_routing_and_ai_work_material_is_installed(self) -> None:
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
                "REPOSITORY_CONTINUITY_POLICY.md",
                "RULE_CONTEXT_CACHE_POLICY.md",
                "AI_WORK_ORCHESTRATION_POLICY.md",
                "VALIDATION_POLICY.md",
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
            validation = (root / "VALIDATION_POLICY.md").read_text(encoding="utf-8")
            self.assertIn("CRLF", validation)
            self.assertIn("INFRASTRUCTURE_UNAVAILABLE", validation)
            self.assertIn("Do not create, replace, or modify a target repository's `.gitattributes`", validation)
            continuity = (root / "REPOSITORY_CONTINUITY_POLICY.md").read_text(encoding="utf-8")
            self.assertIn("VALIDATION_FAILURE", continuity)
            self.assertIn("INFRASTRUCTURE_UNAVAILABLE", continuity)
            self.assertIn("For pull requests only", continuity)
            cache_policy = (root / "RULE_CONTEXT_CACHE_POLICY.md").read_text(encoding="utf-8")
            self.assertIn("CACHE_HIT", cache_policy)
            self.assertIn("PARTIAL_INVALIDATION", cache_policy)
            self.assertIn("CACHE_MISS", cache_policy)
            self.assertIn("session memory", cache_policy)
            self.assertIn("complete semantic feature delta", (root / "UPGRADE_APPLICABILITY_POLICY.md").read_text(encoding="utf-8"))
            catalog = json.loads((root / "feature_catalog.json").read_text(encoding="utf-8"))
            self.assertEqual(catalog["ruleset_version"], "1.17.1")
            self.assertIn("central-artifact-registry", catalog["features"])
            self.assertIn("repository-continuity-break-glass", catalog["features"])
            self.assertIn("rule-context-cache", catalog["features"])
            self.assertIn("ai-work-orchestration", catalog["features"])
            self.assertIn("ai-client-integration", catalog["features"])
            for name in [
                "artifact-record.schema.json",
                "artifact-registry.schema.json",
                "artifact-registry-v2.schema.json",
                "artifact-registration-request.schema.json",
                "feature-catalog.schema.json",
                "upgrade-assessment.schema.json",
                "installation-provenance.schema.json",
                "rule-context-cache.schema.json",
                "model-routing-request.schema.json",
                "model-routing-decision.schema.json",
                "model-router-catalog.schema.json",
                "model-routing-snapshot.schema.json",
                "model-router-profiles.schema.json",
                "model-routing-request-v2.schema.json",
                "model-routing-decision-v2.schema.json",
                "model-router-catalog-fragment-v2.schema.json",
                "ai-work-request.schema.json",
                "capability-descriptor.schema.json",
                "execution-plan.schema.json",
                "execution-report.schema.json",
                "execution-checkpoint.schema.json",
                "approval-receipt.schema.json",
                "validation-evidence.schema.json",
                "gap-report.schema.json",
                "provision-plan.schema.json",
                "provision-request.schema.json",
                "provision-approval.schema.json",
                "provision-report.schema.json",
                "runtime-inventory.schema.json",
                "ai-adapter-protocol.schema.json",
                "resource-cost-evidence.schema.json",
                "client-integration-plan.schema.json",
                "manual-handoff.schema.json",
                "dispatch-receipt.schema.json",
                "adapter-synthesis-report.schema.json",
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
            self.assertFalse((target / ".ai" / "foundation" / "rule_context_cache").exists())
            self.assertFalse((target / ".ai" / "foundation" / "model_router").exists())
            self.assertFalse((target / ".ai" / "foundation" / "ai_work").exists())
            self.assertFalse((target / ".ai" / "foundation" / "ai_runtime_adapters").exists())
            self.assertFalse((target / ".ai" / "foundation" / "ai_executor").exists())
            self.assertFalse((target / ".ai" / "foundation" / "ai_provisioning").exists())
            self.assertFalse((target / ".ai" / "foundation" / "ai_orchestrator").exists())

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
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target, "--capabilities", "rule-context-cache"), 0)
            planner = target / ".ai" / "foundation" / "rule_context_cache" / "rule_context_cache.py"
            self.assertTrue(planner.is_file())
            self.assertIn("foundation-rule-context-cache/v1", planner.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target, "--capabilities", "model-router"), 0)
            router = target / ".ai" / "foundation" / "model_router"
            self.assertTrue((router / "model_router.py").is_file())
            self.assertTrue((router / "router_v2.py").is_file())
            self.assertTrue((router / "ollama_cloud.py").is_file())
            self.assertTrue((router / "mcp_stdio.py").is_file())
            self.assertTrue((router / "mcp.visual-studio.json").is_file())
            self.assertTrue((router / "mcp.github-copilot.json").is_file())
            self.assertIn("foundation-model-router/v1", (router / "model_router.py").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target, "--capabilities", "ai-work"), 0)
            planner = target / ".ai" / "foundation" / "ai_work"
            self.assertTrue((planner / "AI_WORK.md").is_file())
            self.assertTrue((planner / "ai_work.py").is_file())
            self.assertTrue((planner / "work-request.example.json").is_file())
            self.assertTrue((planner / "capabilities.example.json").is_file())
            self.assertIn("foundation-ai-work/v1", (planner / "ai_work.py").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target, "--capabilities", "ai-runtime-adapters"), 0)
            adapters = target / ".ai" / "foundation" / "ai_runtime_adapters"
            self.assertTrue((adapters / "AI_RUNTIME_ADAPTERS.md").is_file())
            self.assertTrue((adapters / "adapter_protocol.py").is_file())
            self.assertTrue((adapters / "reference_adapters.py").is_file())
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target, "--capabilities", "ai-executor"), 0)
            executor_dir = target / ".ai" / "foundation" / "ai_executor"
            self.assertTrue((executor_dir / "AI_EXECUTOR.md").is_file())
            self.assertTrue((executor_dir / "ai_executor.py").is_file())
            self.assertIn("foundation-ai-executor-checkpoint/v1", (executor_dir / "ai_executor.py").read_text(encoding="utf-8"))
            self.assertTrue((target / ".ai" / "foundation" / "ai_work" / "ai_work.py").is_file())
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target, "--capabilities", "ai-provisioning"), 0)
            provisioner = target / ".ai" / "foundation" / "ai_provisioning"
            self.assertTrue((provisioner / "AI_PROVISIONING.md").is_file())
            self.assertTrue((provisioner / "host_preparation.py").is_file())
            self.assertIn("foundation-ai-host-preparation/v1", (provisioner / "host_preparation.py").read_text(encoding="utf-8"))
            self.assertTrue((target / ".ai" / "foundation" / "ai_work" / "ai_work.py").is_file())
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target, "--capabilities", "ai-client-integration"), 0)
            integration = target / ".ai" / "foundation" / "ai_client_integration"
            self.assertTrue((integration / "AI_CLIENT_INTEGRATION.md").is_file())
            self.assertTrue((integration / "client_integration.py").is_file())
            self.assertIn("foundation-manual-dispatch/v1", (integration / "client_integration.py").read_text(encoding="utf-8"))
            self.assertTrue((target / ".ai" / "foundation" / "ai_work" / "ai_work.py").is_file())
            self.assertTrue((target / ".ai" / "foundation" / "ai_runtime_adapters" / "reference_adapters.py").is_file())
            self.assertTrue((target / ".ai" / "foundation" / "model_router" / "model_router.py").is_file())
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target, "--capabilities", "ai-orchestrator"), 0)
            orchestrator = target / ".ai" / "foundation" / "ai_orchestrator"
            self.assertTrue((orchestrator / "AI_ORCHESTRATOR.md").is_file())
            self.assertTrue((orchestrator / "ai_orchestrator.py").is_file())
            self.assertTrue((orchestrator / "orchestrator_mcp.py").is_file())
            self.assertTrue((target / ".ai" / "foundation" / "ai_work" / "ai_work.py").is_file())
            self.assertTrue((target / ".ai" / "foundation" / "ai_runtime_adapters" / "runtime_configuration.py").is_file())
            self.assertTrue((target / ".ai" / "foundation" / "model_router" / "router_v2.py").is_file())

    def test_model_router_capability_surfaces_runtime_configuration_notice(self) -> None:
        notices = install_foundation.capability_notices(["model-router"])
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0]["code"], "MODEL_ROUTER_RUNTIME_CONFIGURATION_REQUIRED")
        self.assertIn("outside the repository", notices[0]["message"])
        self.assertIn("different top-level MCP shapes", notices[0]["message"])
        self.assertIn("explicitly authorizes", notices[0]["message"])

    def test_ai_work_capability_is_explicitly_decision_only(self) -> None:
        notices = install_foundation.capability_notices(["ai-work"])
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0]["code"], "AI_WORK_PLANNER_IS_DECISION_ONLY")
        self.assertIn("grants no authority", notices[0]["message"])
        self.assertIn("outside version control", notices[0]["message"])

    def test_ai_runtime_adapters_require_explicit_runtime_authority(self) -> None:
        notices = install_foundation.capability_notices(["ai-runtime-adapters"])
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0]["code"], "AI_RUNTIME_ADAPTER_CONFIGURATION_REQUIRED")
        self.assertIn("does not trust a loopback", notices[0]["message"])
        self.assertIn("outside version control", notices[0]["message"])

    def test_ai_executor_requires_external_runtime_configuration(self) -> None:
        notices = install_foundation.capability_notices(["ai-executor"])
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0]["code"], "AI_EXECUTOR_RUNTIME_CONFIGURATION_REQUIRED")
        self.assertIn("outside version control", notices[0]["message"])
        self.assertIn("non-idempotent", notices[0]["message"])

    def test_ai_provisioning_requires_exact_external_approval(self) -> None:
        notices = install_foundation.capability_notices(["ai-provisioning"])
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0]["code"], "AI_PROVISIONING_EXACT_APPROVAL_REQUIRED")
        self.assertIn("outside version control", notices[0]["message"])
        self.assertIn("exact unexpired plan", notices[0]["message"])
        self.assertIn("grants no network", notices[0]["message"])

    def test_ai_client_integration_requires_external_state_and_separate_authority(self) -> None:
        notices = install_foundation.capability_notices(["ai-client-integration"])
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0]["code"], "AI_CLIENT_INTEGRATION_EXTERNAL_STATE_AND_AUTHORITY_REQUIRED")
        self.assertIn("outside version control", notices[0]["message"])
        self.assertIn("REQUESTED_NOT_ATTESTED", notices[0]["message"])
        self.assertIn("grants no configuration", notices[0]["message"])

    def test_ai_orchestrator_requires_external_evidence_without_granting_authority(self) -> None:
        notices = install_foundation.capability_notices(["ai-orchestrator"])
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0]["code"], "AI_ORCHESTRATOR_EXTERNAL_EVIDENCE_REQUIRED")
        self.assertIn("outside version control", notices[0]["message"])
        self.assertIn("MANUAL_REQUIRED", notices[0]["message"])
        self.assertIn("grants no network", notices[0]["message"])

    def test_github_registry_capability_surfaces_non_blocking_protection_recommendation(self) -> None:
        notices = install_foundation.capability_notices(["artifact-registry-github"])
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0]["code"], "GITHUB_REQUIRED_CHECKS_RECOMMENDED")
        self.assertEqual(notices[0]["severity"], "RECOMMENDATION")
        self.assertIn("do not enable GitHub branch protection", notices[0]["message"])
        self.assertIn("not required for FOUNDATION_INTEGRITY", notices[0]["message"])

        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            output = StringIO()
            with redirect_stdout(output):
                rc = install_foundation.main([
                    str(target),
                    "--adapters", "none",
                    "--capabilities", "artifact-registry-github",
                ])
            self.assertEqual(rc, 0)
            text = output.getvalue()
            self.assertIn("[RECOMMENDATION] GITHUB_REQUIRED_CHECKS_RECOMMENDED", text)
            self.assertIn("target-project administration choice", text)

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

        cache_contract = self.manifest["rule_context_cache_contract"]
        self.assertTrue(cache_contract["native_instruction_discovery_per_run"])
        self.assertTrue(cache_contract["repository_files_are_source_of_truth"])
        self.assertEqual(cache_contract["statuses"], ["CACHE_HIT", "PARTIAL_INVALIDATION", "CACHE_MISS"])
        self.assertEqual(cache_contract["uncertainty_behavior"], "CACHE_MISS")
        self.assertEqual(cache_contract["semantic_analysis_storage"], "session_local_by_analysis_key")
        self.assertEqual(cache_contract["persistent_record_authority"], "none")

        work = self.manifest["ai_work_contract"]
        self.assertEqual(work["profile"], "foundation-ai-work/v1")
        self.assertFalse(work["python_required"])
        self.assertEqual(work["capability_failures"], "isolated")
        self.assertEqual(work["authority_expansion"], "prohibited")
        self.assertEqual(work["runtime_state"], "outside_version_control")
        self.assertEqual(work["host_preparation"]["profile"], "foundation-ai-host-preparation/v1")
        self.assertEqual(work["host_preparation"]["cost_refresh_minimum_seconds"], 86400)
        self.assertEqual(work["host_preparation"]["reference_install_network"], "denied")
        self.assertEqual(work["reference_orchestrator"]["profile"], "foundation-ai-orchestration/v1")
        self.assertEqual(work["reference_orchestrator"]["refresh_minimum_seconds"], 86400)
        self.assertEqual(work["reference_orchestrator"]["unattested_result"], "MANUAL_REQUIRED")

        client = self.manifest["ai_client_integration_contract"]
        self.assertEqual(client["profile"], "foundation-ai-client-integration/v1")
        self.assertEqual(client["lifecycle"], ["detect", "plan", "apply", "verify", "rollback"])
        self.assertEqual(client["unattested_status"], "REQUESTED_NOT_ATTESTED")
        self.assertEqual(client["manual_fallback_status"], "MANUAL_DISPATCH_REQUIRED")
        self.assertEqual(client["runtime_state"], "outside_version_control")
        self.assertIn("explicitly_trusted", client["dispatch_attestation"])

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
        continuity = (ROOT / "Documentation" / "Standards" / "REPOSITORY_CONTINUITY_POLICY.md").read_text(encoding="utf-8")
        cache_policy = (ROOT / "Documentation" / "Standards" / "RULE_CONTEXT_CACHE_POLICY.md").read_text(encoding="utf-8")
        validation = (ROOT / ".ai" / "VALIDATION_POLICY.md").read_text(encoding="utf-8")
        upgrade = (ROOT / "Documentation" / "Standards" / "UPGRADE_APPLICABILITY_POLICY.md").read_text(encoding="utf-8")
        transfer = (ROOT / "foundation" / "AI_TRANSFER.md").read_text(encoding="utf-8")
        self.assertIn("complete semantic feature delta", project_rules)
        self.assertIn("unknown -> PRESERVE", integration)
        self.assertIn("MIGRATE_EXPLICIT", identity)
        self.assertIn("same authority", registration.lower())
        self.assertIn("object-level", central.lower())
        self.assertIn("INFRASTRUCTURE_UNAVAILABLE", continuity)
        self.assertIn("VALIDATION_FAILURE", continuity)
        self.assertIn("native client instruction discovery", cache_policy)
        self.assertIn("actual working-tree bytes", cache_policy)
        self.assertIn("transitive semantic dependent", cache_policy)
        self.assertIn("CRLF", validation)
        self.assertIn("INFRASTRUCTURE_UNAVAILABLE", validation)
        self.assertIn("silently skipped", upgrade)
        self.assertIn("persistent-identity", transfer)
        self.assertIn("workflow files and green Actions runs do **not** automatically", transfer)
        self.assertIn("MUST NOT be silently applied", transfer)
        self.assertIn("do not create, replace, or modify the target's `.gitattributes`", transfer)
        self.assertIn("For pull requests only", transfer)
        self.assertIn("MUST NOT silently create Rulesets", transfer)

    def test_v1_bootstrap_compatibility_semantics_remain_intact(self) -> None:
        dry = bootstrap.compatibility_args(["target", "--dry-run"])
        self.assertNotIn("--dry-run", dry)
        self.assertNotIn("--apply", dry)
        apply = bootstrap.compatibility_args(["target"])
        self.assertIn("--apply", apply)

    def test_manifest_sources_exist_targets_unique_hashed_and_version_is_v1_16(self) -> None:
        rows = list(self.manifest["core"])
        for adapter_rows in self.manifest["adapters"].values():
            rows.extend(adapter_rows)
        for capability_rows in self.manifest.get("capabilities", {}).values():
            rows.extend(capability_rows)
        targets = [row["target"] for row in rows]
        self.assertEqual(len(targets), len(set(targets)))
        for row in rows:
            self.assertTrue((ROOT / row["source"]).is_file(), row["source"])
            self.assertRegex(row["source_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(self.manifest["schema_version"], 1)
        self.assertEqual(self.manifest["ruleset_version"], "1.17.1")
        self.assertEqual(self.manifest["installation_scope"], "core_rules_with_opt_in_capabilities")


if __name__ == "__main__":
    unittest.main()
