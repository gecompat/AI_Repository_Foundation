from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
CAPABILITY = ROOT / "foundation" / "capabilities" / "ai-runtime-adapters"
sys.path.insert(0, str(CAPABILITY))

import runtime_configuration  # noqa: E402
import runtime_mcp  # noqa: E402


class RuntimeConfigurationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.store = runtime_configuration.ConfigurationStore(self.root / "runtime-connections.json")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def connection(self, **updates: object) -> dict:
        value = runtime_configuration._connection_defaults(self.root, "http://127.0.0.1:11434")
        value.update(updates)
        return value

    def document(self, connections: dict[str, dict] | None = None) -> dict:
        value = runtime_configuration.empty_configuration()
        value["connections"] = connections or {}
        return value

    @unittest.skipUnless(os.name == "nt", "Windows-specific stable cross-client path")
    def test_windows_default_state_is_not_localappdata_virtualization_sensitive(self) -> None:
        with mock.patch.dict(os.environ, {"LOCALAPPDATA": str(self.root / "virtualized")}, clear=False):
            os.environ.pop("AI_RUNTIME_ADAPTER_HOME", None)
            state = runtime_configuration.default_state_dir()
        self.assertNotIn("virtualized", str(state))
        self.assertEqual(state.name, "ai-runtime-adapters")
        self.assertEqual(state.parent.name, ".ai-repository-foundation")

    def test_configuration_schema_accepts_hostname_ip_and_port(self) -> None:
        schema = json.loads(
            (ROOT / "foundation" / "schemas" / "ai-runtime-configuration.schema.json").read_text(encoding="utf-8")
        )
        document = self.document(
            {
                "lan-ollama": self.connection(
                    endpoint="http://192.0.2.10:11434",
                    execution_boundary="LOCAL_NETWORK",
                    trust_loopback_host=False,
                    remote_data_classes=["PUBLIC"],
                ),
                "named-host": self.connection(
                    endpoint="https://models.example.test:8443",
                    execution_boundary="REMOTE",
                    trust_loopback_host=False,
                    remote_data_classes=["PUBLIC"],
                ),
            }
        )
        self.assertEqual(schema["properties"]["contract"]["const"], runtime_configuration.CONTRACT)
        self.assertFalse(schema["additionalProperties"])
        normalized = runtime_configuration.validate_configuration(document)
        self.assertEqual(normalized["connections"]["lan-ollama"]["endpoint"], "http://192.0.2.10:11434")
        self.assertEqual(normalized["connections"]["named-host"]["endpoint"], "https://models.example.test:8443")

    def test_loopback_host_boundary_requires_explicit_confirmation(self) -> None:
        with self.assertRaisesRegex(runtime_configuration.ConfigurationError, "explicit trust_loopback_host"):
            runtime_configuration.validate_connection(
                "ollama-local", self.connection(execution_boundary="HOST", trust_loopback_host=False)
            )

    def test_store_is_atomic_reversible_and_refuses_diverged_rollback(self) -> None:
        first = self.document({"ollama-local": self.connection()})
        saved = self.store.save(first)
        self.assertEqual(saved["status"], "SAVED")
        second = self.store.load()
        second["connections"]["ollama-local"]["label"] = "Changed"
        self.store.save(second)
        rolled_back = self.store.rollback()
        self.assertEqual(rolled_back["status"], "ROLLED_BACK")
        self.assertEqual(self.store.load()["connections"]["ollama-local"]["label"], "Ollama local")

        current = self.store.load()
        current["connections"]["ollama-local"]["label"] = "Planned"
        self.store.save(current)
        tampered = self.store.load()
        tampered["connections"]["ollama-local"]["label"] = "External edit"
        runtime_configuration.atomic_write_json(self.store.path, tampered)
        with self.assertRaisesRegex(runtime_configuration.ConfigurationError, "changed after"):
            self.store.rollback()

    def test_runtime_state_inside_git_is_rejected(self) -> None:
        git_root = self.root / "repo"
        (git_root / ".git").mkdir(parents=True)
        store = runtime_configuration.ConfigurationStore(git_root / "state" / "runtime.json")
        with self.assertRaisesRegex(runtime_configuration.ConfigurationError, "outside a Git worktree"):
            store.save(self.document())

    def test_dotenv_reference_never_persists_or_emits_secret(self) -> None:
        dotenv = self.root / ".env"
        secret = "test-secret-that-must-not-appear"
        dotenv.write_text(f"OLLAMA='{secret}'\n", encoding="utf-8")
        connection = self.connection(
            credential={
                "source": "DOTENV_REFERENCE",
                "path": str(dotenv),
                "key": "OLLAMA",
                "export_as": "OLLAMA_API_KEY",
            }
        )
        self.store.save(self.document({"ollama-local": connection}))
        self.assertNotIn(secret, self.store.path.read_text(encoding="utf-8"))
        public = runtime_configuration.public_connection("ollama-local", connection)
        self.assertNotIn(str(dotenv), json.dumps(public))
        with mock.patch.dict(os.environ, {}, clear=True):
            with runtime_configuration.credential_environment(connection):
                self.assertEqual(os.environ["OLLAMA_API_KEY"], secret)
            self.assertNotIn("OLLAMA_API_KEY", os.environ)

    def test_one_invalid_connection_does_not_hide_a_valid_connection(self) -> None:
        raw = self.document({"healthy": self.connection(), "broken": {"adapter": "ollama"}})
        runtime_configuration.atomic_write_json(self.store.path, raw)
        statuses = {row["connection_id"]: row for row in self.store.connection_statuses()}
        self.assertEqual(statuses["healthy"]["status"], "CONFIGURED")
        self.assertEqual(statuses["broken"]["status"], "INVALID")
        self.assertEqual(self.store.load_connection("healthy")["adapter"], "ollama")

        editable = self.store.load_for_edit()
        editable["connections"]["broken"] = self.connection(label="Repaired")
        self.store.save(editable)
        self.assertEqual(self.store.load_connection("broken")["label"], "Repaired")
        self.store.rollback()
        restored = {row["connection_id"]: row for row in self.store.connection_statuses()}
        self.assertEqual(restored["healthy"]["status"], "CONFIGURED")
        self.assertEqual(restored["broken"]["status"], "INVALID")

    def test_non_loopback_discovery_never_probes_without_authority(self) -> None:
        with mock.patch.dict(os.environ, {"OLLAMA_HOST": "http://models.example.test:11434"}, clear=False):
            with mock.patch.object(runtime_configuration, "_probe_candidate") as probe:
                probe.return_value = {
                    "adapter": "ollama", "endpoint": "http://127.0.0.1:11434", "state": "UNAVAILABLE",
                    "checked_at": "now", "version": None,
                }
                rows = runtime_configuration.discover_candidates(probe=True)
        self.assertEqual(probe.call_count, 1)
        remote = next(row for row in rows if row["endpoint"].startswith("http://models.example.test"))
        self.assertEqual(remote["state"], "AUTHORIZATION_REQUIRED")

    def test_first_run_wizard_detects_then_proposes_without_silent_save(self) -> None:
        answers = iter(["", "", "", "", "", "", "", "", "", "", "", "", "", "", "SAVE"])
        observed: list[str] = []
        discovery = [{
            "adapter": "ollama", "endpoint": "http://127.0.0.1:11434", "state": "HEALTHY",
            "checked_at": "now", "version": "test", "source": "SAFE_LOOPBACK_DEFAULT",
            "proposal_only": True, "requires_confirmation": [],
        }]
        with mock.patch.object(runtime_configuration, "discover_candidates", return_value=discovery):
            result = runtime_configuration.interactive_configure(
                self.store,
                input_fn=lambda _prompt: next(answers),
                output_fn=observed.append,
            )
        self.assertEqual(result["status"], "SAVED")
        saved = self.store.load_connection("ollama-local")
        self.assertEqual(saved["endpoint"], "http://127.0.0.1:11434")
        self.assertEqual(saved["model_selection"]["mode"], "ROUTER")
        self.assertTrue(any("Gefunden" in line for line in observed))


class RuntimeMcpTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.store = runtime_configuration.ConfigurationStore(self.root / "runtime-connections.json")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def connection(self, **updates: object) -> dict:
        value = runtime_configuration._connection_defaults(self.root, "http://127.0.0.1:11434")
        value.update(updates)
        return value

    def save(self, connection: dict) -> None:
        document = runtime_configuration.empty_configuration()
        document["connections"] = {"ollama-local": connection}
        self.store.save(document)

    def test_mcp_starts_without_configuration_and_returns_setup_proposal(self) -> None:
        initialized = runtime_mcp.handle(
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}},
            self.store,
        )
        self.assertEqual(initialized["result"]["serverInfo"]["name"], "foundation-ai-runtime")
        result = runtime_mcp.call_tool("runtime_configuration_status", {}, self.store)
        value = result["structuredContent"]
        self.assertEqual(value["status"], "CONFIGURATION_REQUIRED")
        self.assertEqual(value["next_action"], "RUN_CONFIGURATION_WIZARD")
        self.assertTrue(value["proposals"])

    def test_router_and_manual_modes_require_explicit_model(self) -> None:
        self.save(self.connection())
        result = runtime_mcp.call_tool(
            "runtime_invoke",
            {
                "connection_id": "ollama-local", "operation_id": "op-1", "data_class": "PUBLIC",
                "input_path": str(self.root / "input"), "output_path": str(self.root / "output"),
            },
            self.store,
        )
        self.assertTrue(result["isError"])
        self.assertEqual(result["structuredContent"]["reason_code"], "MODEL_SELECTION_REQUIRED")

    def test_explicit_model_is_forwarded_and_attested_metadata_is_returned(self) -> None:
        self.save(self.connection())
        adapter_result = {
            "status": "COMPLETED", "operation_id": "op-2", "requested_model": "qwen:test",
            "actual_model": "qwen:test", "dispatch_status": "ACTUAL_MODEL_ATTESTED",
            "output_sha256": "sha256:" + "a" * 64, "output_bytes": 12,
        }
        with mock.patch.object(runtime_mcp, "execute_adapter", return_value=adapter_result) as invoke:
            result = runtime_mcp.call_tool(
                "runtime_invoke",
                {
                    "connection_id": "ollama-local", "operation_id": "op-2", "model": "qwen:test",
                    "data_class": "PUBLIC", "input_path": str(self.root / "in.txt"),
                    "output_path": str(self.root / "out.json"),
                },
                self.store,
            )
        self.assertFalse(result["isError"])
        self.assertEqual(result["structuredContent"]["actual_model"], "qwen:test")
        self.assertEqual(invoke.call_args.args[2]["model"], "qwen:test")
        self.assertNotIn("response", json.dumps(result))

    def test_pinned_model_is_used_but_cloud_still_requires_per_call_authority(self) -> None:
        self.save(
            self.connection(
                allow_remote_models=True,
                remote_data_classes=["PUBLIC"],
                model_selection={"mode": "PINNED", "default_model": "large:cloud"},
            )
        )
        result = runtime_mcp.call_tool(
            "runtime_invoke",
            {
                "connection_id": "ollama-local", "operation_id": "op-cloud", "data_class": "PUBLIC",
                "input_path": str(self.root / "in.txt"), "output_path": str(self.root / "out.json"),
            },
            self.store,
        )
        self.assertEqual(result["structuredContent"]["reason_code"], "OLLAMA_CLOUD_NOT_AUTHORIZED")


if __name__ == "__main__":
    unittest.main()
