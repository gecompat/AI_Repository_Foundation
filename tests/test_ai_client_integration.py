from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


integration = load_module(
    "foundation_ai_client_integration_tests",
    ROOT / "foundation" / "capabilities" / "ai-client-integration" / "client_integration.py",
)
AT = datetime(2026, 9, 7, 16, 0, tzinfo=timezone.utc)


class AIClientIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.config = self.root / "client.json"
        self.store = integration.IntegrationStore(self.root / "state")

    def request(self, **updates):
        value = {
            "schema_version": 1,
            "contract": integration.CONTRACT,
            "integration_id": "integration-1",
            "client_kind": "VISUAL_STUDIO",
            "configuration_path": str(self.config),
            "entry_id": "foundation-model-router",
            "router_argv": [str(Path(sys.executable).resolve()), "mcp"],
            "preferred_transports": ["MCP", "MANUAL"],
            "supported_transports": ["MCP", "MANUAL"],
            "authorization": {"configuration_read": True, "configuration_write": True, "repository_write": False},
            "valid_for_seconds": 600,
        }
        value.update(updates)
        return value

    def test_detect_plan_apply_verify_and_exact_rollback_preserve_other_configuration(self) -> None:
        original = b'{"servers":{"existing":{"command":"other"}},"setting":true}\n'
        self.config.write_bytes(original)
        request = self.request()
        detected = integration.detect(request, at=AT)
        plan = integration.plan_integration(request, detected, at=AT)
        self.assertEqual(plan["status"], "EXECUTABLE")
        self.assertEqual(plan["change"], "MERGE_ENTRY")
        applied = integration.apply_integration(request, plan, store=self.store, at=AT)
        self.assertEqual(applied["status"], "APPLIED")
        document = json.loads(self.config.read_text(encoding="utf-8"))
        self.assertEqual(document["servers"]["existing"], {"command": "other"})
        self.assertEqual(document["servers"]["foundation-model-router"]["type"], "stdio")
        self.assertTrue(document["setting"])
        self.assertEqual(integration.verify_integration(request, plan, store=self.store, at=AT)["status"], "PASSED")
        self.assertEqual(integration.rollback_integration(request, plan, store=self.store)["status"], "ROLLED_BACK")
        self.assertEqual(self.config.read_bytes(), original)

    def test_github_copilot_shape_is_distinct_and_existing_conflict_is_manual(self) -> None:
        request = self.request(client_kind="GITHUB_COPILOT")
        plan = integration.plan_integration(request, integration.detect(request, at=AT), at=AT)
        self.assertEqual(plan["mutation"]["root_key"], "mcpServers")
        self.assertEqual(plan["mutation"]["entry"]["type"], "local")
        self.assertEqual(plan["mutation"]["entry"]["tools"], ["*"])
        self.config.write_text('{"mcpServers":{"foundation-model-router":{"command":"different"}}}\n', encoding="utf-8")
        conflicted = integration.plan_integration(request, integration.detect(request, at=AT), at=AT)
        self.assertEqual(conflicted["status"], "MANUAL_REQUIRED")
        self.assertEqual(conflicted["selected_transport"], "MANUAL")
        self.assertEqual(conflicted["change"], "MANUAL_GUIDANCE")
        self.assertIn("EXISTING_ENTRY_CONFLICT", conflicted["reason_codes"])

    def test_configuration_write_and_repository_write_are_not_inferred(self) -> None:
        request = self.request(authorization={"configuration_read": True, "configuration_write": False, "repository_write": False})
        plan = integration.plan_integration(request, integration.detect(request, at=AT), at=AT)
        self.assertEqual(plan["status"], "MANUAL_REQUIRED")
        self.assertIn("CONFIGURATION_WRITE_NOT_AUTHORIZED", plan["reason_codes"])
        self.assertEqual(integration.apply_integration(request, plan, store=self.store, at=AT)["status"], "MANUAL_REQUIRED")
        repository_request = self.request(
            configuration_path=str(ROOT / ".vscode" / "mcp.json"),
            authorization={"configuration_read": True, "configuration_write": True, "repository_write": False},
        )
        repository_plan = integration.plan_integration(repository_request, integration.detect(repository_request, at=AT), at=AT)
        self.assertEqual(repository_plan["status"], "MANUAL_REQUIRED")
        self.assertIn("REPOSITORY_WRITE_NOT_AUTHORIZED", repository_plan["reason_codes"])

    def test_changed_configuration_blocks_apply_and_rollback(self) -> None:
        self.config.write_text('{"setting":1}\n', encoding="utf-8")
        request = self.request()
        plan = integration.plan_integration(request, integration.detect(request, at=AT), at=AT)
        self.config.write_text('{"setting":2}\n', encoding="utf-8")
        with self.assertRaisesRegex(integration.IntegrationError, "changed after planning"):
            integration.apply_integration(request, plan, store=self.store, at=AT)
        fresh_plan = integration.plan_integration(request, integration.detect(request, at=AT), at=AT)
        integration.apply_integration(request, fresh_plan, store=self.store, at=AT)
        self.config.write_text(self.config.read_text(encoding="utf-8") + " ", encoding="utf-8")
        with self.assertRaisesRegex(integration.IntegrationError, "changed after apply"):
            integration.rollback_integration(request, fresh_plan, store=self.store)

    def test_codex_uses_cli_without_mutating_configuration(self) -> None:
        request = self.request(
            client_kind="CODEX",
            configuration_path=None,
            preferred_transports=["CLI", "MANUAL"],
            supported_transports=["CLI", "MANUAL"],
        )
        plan = integration.plan_integration(request, integration.detect(request, at=AT), at=AT)
        self.assertEqual(plan["selected_transport"], "CLI")
        self.assertEqual(plan["change"], "NO_CONFIG_REQUIRED")
        self.assertEqual(integration.apply_integration(request, plan, store=self.store, at=AT)["status"], "APPLIED")
        self.assertEqual(integration.verify_integration(request, plan, store=self.store, at=AT)["status"], "PASSED")
        self.assertEqual(integration.rollback_integration(request, plan, store=self.store)["status"], "ROLLED_BACK")

    def test_missing_router_and_unusable_client_configuration_degrade_to_manual(self) -> None:
        missing = self.request(router_argv=[str(self.root / "missing-router"), "mcp"])
        missing_detection = integration.detect(missing, at=AT)
        self.assertEqual(missing_detection["available_transports"], ["MANUAL"])
        missing_plan = integration.plan_integration(missing, missing_detection, at=AT)
        self.assertEqual(missing_plan["status"], "MANUAL_REQUIRED")
        self.assertEqual(missing_plan["selected_transport"], "MANUAL")
        self.assertEqual(integration.apply_integration(missing, missing_plan, store=self.store, at=AT)["status"], "MANUAL_REQUIRED")

        self.config.write_text('{"servers":[]}', encoding="utf-8")
        invalid = self.request()
        invalid_plan = integration.plan_integration(invalid, integration.detect(invalid, at=AT), at=AT)
        self.assertEqual(invalid_plan["status"], "MANUAL_REQUIRED")
        self.assertEqual(invalid_plan["selected_transport"], "MANUAL")
        self.assertIn("CLIENT_CONFIGURATION_SHAPE_CONFLICT", invalid_plan["reason_codes"])

    def test_client_configuration_never_embeds_credential_arguments(self) -> None:
        executable = str(Path(sys.executable).resolve())
        for argument in ("--token=secret-value", "https://user:password@example.invalid/path"):
            with self.assertRaisesRegex(integration.IntegrationError, "must not contain credentials"):
                integration.detect(self.request(router_argv=[executable, "mcp", argument]), at=AT)

    def manual_request(self, **updates):
        source = self.root / "source-prompt.txt"
        source.write_text("Analyze the bounded task.", encoding="utf-8")
        value = {
            "schema_version": 1,
            "contract": integration.MANUAL_CONTRACT,
            "work_id": "work-1",
            "task_class": "software.architecture",
            "data_class": "INTERNAL",
            "risk": "HIGH",
            "required_capabilities": ["architecture.reasoning"],
            "recommended_tier": "FRONTIER",
            "recommended_model": None,
            "automatic_dispatch": {"supported": False, "attestation_available": False, "reason_code": "CLIENT_SESSION_MODEL_FIXED"},
            "remote_authorized": False,
            "acceptance_criteria": ["Return a concrete decision."],
            "validation_requirements": ["Check against repository tests."],
            "source_prompt_path": str(source),
            "output_prompt_path": str(self.root / "manual-prompt.txt"),
            "valid_for_seconds": 600,
        }
        value.update(updates)
        return value

    def model_evidence(self, **updates):
        value = {
            "provider": "provider-a",
            "model": "model-a",
            "execution_boundary": "REMOTE",
            "evidence_kind": "CLIENT_CATALOG",
            "observed_at": integration.isoformat(AT - timedelta(minutes=1)),
            "expires_at": integration.isoformat(AT + timedelta(minutes=5)),
        }
        value.update(updates)
        return value

    def test_manual_handoff_writes_prompt_without_putting_content_in_control_plane(self) -> None:
        request = self.manual_request()
        handoff = integration.create_manual_handoff(request, at=AT)
        self.assertEqual(handoff["status"], "MANUAL_DISPATCH_REQUIRED")
        self.assertIsNone(handoff["recommended_model"])
        self.assertNotIn("Analyze the bounded task", json.dumps(handoff))
        prompt = Path(request["output_prompt_path"]).read_text(encoding="utf-8")
        self.assertIn("Recommended tier: FRONTIER", prompt)
        self.assertIn("Analyze the bounded task", prompt)
        self.assertIn("Acceptance criteria", prompt)

    def test_manual_handoff_uses_only_fresh_privacy_allowed_concrete_model_evidence(self) -> None:
        denied = integration.create_manual_handoff(self.manual_request(recommended_model=self.model_evidence()), at=AT)
        self.assertIsNone(denied["recommended_model"])
        self.assertIn("REMOTE_DATA_TRANSFER_NOT_AUTHORIZED", denied["reason_codes"])
        allowed_request = self.manual_request(
            data_class="PUBLIC",
            recommended_model=self.model_evidence(),
            output_prompt_path=str(self.root / "allowed.txt"),
        )
        allowed = integration.create_manual_handoff(allowed_request, at=AT)
        self.assertEqual(allowed["recommended_model"]["model"], "model-a")
        self.assertEqual(allowed["model_evidence_state"], "AVAILABLE_NOT_EXECUTION_ATTESTED")
        self.assertIn("Recommended model: provider-a/model-a", Path(allowed_request["output_prompt_path"]).read_text(encoding="utf-8"))
        prior_receipt_request = self.manual_request(
            data_class="PUBLIC",
            recommended_model=self.model_evidence(evidence_kind="EXECUTION_RECEIPT"),
            output_prompt_path=str(self.root / "prior-receipt.txt"),
        )
        prior_receipt = integration.create_manual_handoff(prior_receipt_request, at=AT)
        self.assertEqual(prior_receipt["model_evidence_state"], "AVAILABLE_NOT_EXECUTION_ATTESTED")
        expired_request = self.manual_request(
            data_class="PUBLIC",
            recommended_model=self.model_evidence(expires_at=integration.isoformat(AT)),
            output_prompt_path=str(self.root / "expired.txt"),
        )
        expired = integration.create_manual_handoff(expired_request, at=AT)
        self.assertIsNone(expired["recommended_model"])
        self.assertIn("MODEL_EVIDENCE_EXPIRED", expired["reason_codes"])

    def test_dispatch_receipt_never_claims_unattested_requested_model(self) -> None:
        handoff = integration.create_manual_handoff(
            self.manual_request(data_class="PUBLIC", recommended_model=self.model_evidence()),
            at=AT,
        )
        receipt = {
            "schema_version": 1,
            "contract": integration.RECEIPT_CONTRACT,
            "receipt_id": "receipt-1",
            "handoff_id": handoff["handoff_id"],
            "client_id": "copilot",
            "issuer_id": "copilot-host",
            "requested_model": "model-a",
            "actual_model": "model-b",
            "observed_at": integration.isoformat(AT),
            "evidence_kind": "HOST_RESPONSE_METADATA",
            "status": "ATTESTED",
            "reason_codes": ["HOST_REPORTED_MODEL"],
        }
        result = integration.verify_dispatch_receipt(handoff, receipt, at=AT)
        self.assertEqual(result["status"], "REQUESTED_NOT_ATTESTED")
        receipt["actual_model"] = "model-a"
        untrusted = integration.verify_dispatch_receipt(handoff, receipt, at=AT)
        self.assertEqual(untrusted["status"], "REQUESTED_NOT_ATTESTED")
        self.assertIn("DISPATCH_ISSUER_NOT_TRUSTED", untrusted["reason_codes"])
        self.assertEqual(integration.verify_dispatch_receipt(handoff, receipt, trusted_issuers={"copilot-host"}, at=AT)["status"], "ATTESTED")
        receipt["requested_model"] = "model-b"
        receipt["actual_model"] = "model-b"
        changed = integration.verify_dispatch_receipt(handoff, receipt, trusted_issuers={"copilot-host"}, at=AT)
        self.assertEqual(changed["status"], "ATTESTED")
        self.assertEqual(changed["requested_model"], "model-b")
        self.assertIn("MANUAL_SELECTION_DIFFERS_FROM_RECOMMENDATION", changed["reason_codes"])
        receipt["evidence_kind"] = "USER_OBSERVATION"
        self.assertEqual(integration.verify_dispatch_receipt(handoff, receipt, trusted_issuers={"copilot-host"}, at=AT)["status"], "REQUESTED_NOT_ATTESTED")
        tampered = json.loads(json.dumps(handoff))
        tampered["recommended_model"]["model"] = "tampered"
        with self.assertRaisesRegex(integration.IntegrationError, "integrity"):
            integration.verify_dispatch_receipt(tampered, receipt, at=AT)

    def synthesis_request(self, helper: Path, output: Path, **updates):
        executable = str(Path(sys.executable).resolve())
        config = {
            "provider": "synthetic-command",
            "execution_boundary": "PROCESS",
            "probe_argv": [executable, str(helper), "probe"],
            "catalog_argv": [executable, str(helper), "catalog"],
            "invoke_argv": [executable, str(helper), "invoke"],
            "environment_allowlist": [],
            "allowed_data_classes": ["PUBLIC"],
            "read_roots": [str(self.root)],
            "write_roots": [str(self.root)],
            "timeout_seconds": 10,
            "cwd": str(self.root),
        }
        value = {
            "schema_version": 1,
            "contract": integration.SYNTHESIS_CONTRACT,
            "synthesis_id": "synthesis-1",
            "allow_local_adapter_synthesis": True,
            "output_directory": str(output),
            "network_access": "DENY",
            "credential_environment_names": [],
            "repository_write": False,
            "command_config": config,
        }
        value.update(updates)
        return value

    def test_adapter_synthesis_is_authority_gated_quarantined_and_conformance_verified(self) -> None:
        helper = self.root / "adapter_helper.py"
        helper.write_text(
            "import json, sys\n"
            "mode=sys.argv[1]\n"
            "if mode=='catalog': print(json.dumps({'fragments': []}))\n"
            "elif mode=='invoke': sys.stdout.buffer.write(sys.stdin.buffer.read())\n",
            encoding="utf-8",
        )
        output = self.root / "adapter"
        denied = self.synthesis_request(helper, output, allow_local_adapter_synthesis=False)
        with self.assertRaisesRegex(integration.IntegrationError, "not authorized"):
            integration.synthesize_adapter(denied, at=AT)
        report = integration.synthesize_adapter(self.synthesis_request(helper, output), at=AT)
        self.assertEqual(report["status"], "QUARANTINED")
        self.assertEqual(report["constraints"]["network_access"], "DENY")
        fixture = self.root / "fixture.txt"
        fixture.write_text("conformance", encoding="utf-8")
        verified = integration.verify_synthesized(output, fixture, self.root / "fixture-output.txt")
        self.assertEqual(verified["status"], "VERIFIED")
        self.assertEqual(verified["conformance"]["status"], "PASSED")

    def test_tampered_synthesized_adapter_remains_unusable(self) -> None:
        helper = self.root / "adapter_helper.py"
        helper.write_text("import sys\n", encoding="utf-8")
        output = self.root / "adapter"
        integration.synthesize_adapter(self.synthesis_request(helper, output), at=AT)
        (output / "adapter_protocol.py").write_text("tampered\n", encoding="utf-8")
        fixture = self.root / "fixture.txt"
        fixture.write_text("input", encoding="utf-8")
        with self.assertRaisesRegex(integration.IntegrationError, "source hash changed"):
            integration.verify_synthesized(output, fixture, self.root / "fixture-output.txt")

    def test_public_schemas_are_strict_and_runtime_neutral(self) -> None:
        for name in ("client-integration-plan.schema.json", "client-model-routing-capability.schema.json", "manual-handoff.schema.json", "dispatch-receipt.schema.json", "adapter-synthesis-report.schema.json", "vscode-model-routing-plan.schema.json"):
            schema = json.loads((ROOT / "foundation" / "schemas" / name).read_text(encoding="utf-8"))
            self.assertFalse(schema["additionalProperties"])
            text = json.dumps(schema).lower()
            self.assertNotIn("ollama", text)
            self.assertNotIn("claude", text)
            self.assertNotIn("gpt-", text)

    def test_vscode_native_role_plan_uses_only_fresh_available_models(self) -> None:
        sources = [{"evidence_kind": "OFFICIAL_DOCUMENTATION", "locator": "https://example.invalid/client-docs", "observed_at": integration.isoformat(AT - timedelta(minutes=2))}]
        def surface(surface_id, task_class, mode, target):
            return {
                "surface_id": surface_id,
                "task_classes": [task_class],
                "dispatch_mode": mode,
                "selection_scope": "PER_TASK_CLASS" if mode == "ROLE_SETTING" else "PER_AGENT",
                "binding_target": target,
                "model_binding": "PRIORITY_LIST" if mode == "AGENT_PROFILE" else "SINGLE",
                "automatic_dispatch": True,
                "fallback_behavior": "INHERIT_PARENT",
                "actual_model_evidence": ["NOT_AVAILABLE"],
                "configuration_authority": "PROJECT_CONFIGURATION",
                "repository_managed": True,
            }
        request = {
            "schema_version": 1,
            "contract": integration.VSCODE_ROUTING_REQUEST,
            "request_id": "vscode-routing-1",
            "model_inventory_observed_at": integration.isoformat(AT - timedelta(minutes=1)),
            "model_inventory_expires_at": integration.isoformat(AT + timedelta(minutes=10)),
            "available_models": ["fast-runtime-model", "deep-runtime-model"],
            "client_capability": {
                "schema_version": 1,
                "contract": integration.CLIENT_MODEL_CAPABILITY,
                "client_id": "vscode-test",
                "client_kind": "VISUAL_STUDIO_CODE",
                "observed_at": integration.isoformat(AT - timedelta(minutes=1)),
                "expires_at": integration.isoformat(AT + timedelta(minutes=10)),
                "sources": sources,
                "surfaces": [
                    surface("PLAN_SETTING", "software.planning", "ROLE_SETTING", "chat.planAgent.defaultModel"),
                    surface("IMPLEMENT_SETTING", "software.implementation", "ROLE_SETTING", "github.copilot.chat.implementAgent.model"),
                    surface("CUSTOM_AGENT", "research.sourced", "AGENT_PROFILE", ".github/agents/*.agent.md"),
                    surface("SUBAGENT_PARAMETER", "terminal.validation", "SUBAGENT_PARAMETER", "agent.model"),
                ],
                "fallback_order": ["NATIVE_ROLE", "NATIVE_SUBAGENT", "MCP", "MANUAL"],
            },
            "roles": {
                "planning": {"task_class": "software.planning", "surface": "PLAN_SETTING", "models": ["deep-runtime-model"], "tools": []},
                "implementation": {"task_class": "software.implementation", "surface": "IMPLEMENT_SETTING", "models": ["deep-runtime-model"], "tools": []},
                "research": {"task_class": "research.sourced", "surface": "CUSTOM_AGENT", "models": ["fast-runtime-model", "deep-runtime-model"], "tools": ["search", "web"]},
                "terminal": {"task_class": "terminal.validation", "surface": "SUBAGENT_PARAMETER", "models": ["fast-runtime-model"], "tools": ["terminal"]},
            },
            "valid_for_seconds": 600,
        }
        plan = integration.plan_vscode_model_routing(request, at=AT)
        self.assertEqual(plan["status"], "EXECUTABLE")
        self.assertEqual(plan["native_changes"]["settings_patch"]["chat.planAgent.defaultModel"], "deep-runtime-model")
        self.assertEqual(plan["native_changes"]["custom_agents"][0]["frontmatter"]["model"], ["fast-runtime-model", "deep-runtime-model"])
        self.assertEqual(plan["native_changes"]["subagent_parameters"][0]["models"], ["fast-runtime-model"])
        self.assertTrue(plan["host_constraints"]["actual_model_attestation_required"])
        self.assertTrue(plan["client_capability_hash"].startswith("sha256:"))

        request["roles"]["research"]["models"] = ["not-observed"]
        unavailable = integration.plan_vscode_model_routing(request, at=AT)
        self.assertEqual(unavailable["status"], "MANUAL_REQUIRED")
        self.assertEqual(unavailable["unavailable_bindings"], ["research"])

        request["client_capability"]["expires_at"] = integration.isoformat(AT)
        with self.assertRaisesRegex(integration.IntegrationError, "must be refreshed"):
            integration.plan_vscode_model_routing(request, at=AT)


if __name__ == "__main__":
    unittest.main()
