from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
CAPABILITY = ROOT / "foundation" / "capabilities" / "ai-runtime-adapters"
sys.path.insert(0, str(CAPABILITY))

import adapter_protocol  # noqa: E402
import reference_adapters  # noqa: E402


class DummyAdapter:
    def probe(self, arguments: dict) -> dict:
        return {"health": {"state": "HEALTHY"}}

    def catalog(self, arguments: dict) -> dict:
        return {"fragments": []}

    def invoke(self, arguments: dict) -> dict:
        return {"content": "must not cross the control plane"}


class FailingAdapter(DummyAdapter):
    def catalog(self, arguments: dict) -> dict:
        raise adapter_protocol.AdapterError("AVAILABILITY", "DOWN", "unavailable", retryable=True)


class ProtocolTests(unittest.TestCase):
    def frame(self, operation: str, arguments: dict | None = None) -> dict:
        return {
            "protocol": adapter_protocol.CONTRACT,
            "request_id": "request-1",
            "operation": operation,
            "arguments": arguments or {},
        }

    def test_protocol_is_strict_and_rejects_content_in_results(self) -> None:
        server = adapter_protocol.ProtocolServer(DummyAdapter())
        invalid = server.handle({**self.frame("probe"), "unexpected": True})
        self.assertEqual(invalid["error"]["code"], "INVALID_FRAME")
        leaked = server.handle(self.frame("invoke"))
        self.assertEqual(leaked["status"], "ERROR")
        self.assertEqual(leaked["error"]["code"], "CONTENT_IN_CONTROL_PLANE")

    def test_circuit_breaker_opens_after_bounded_failures(self) -> None:
        server = adapter_protocol.ProtocolServer(
            FailingAdapter(), adapter_protocol.CircuitBreaker(failure_threshold=2, cooldown_seconds=60)
        )
        self.assertEqual(server.handle(self.frame("catalog"))["error"]["code"], "DOWN")
        self.assertEqual(server.handle(self.frame("catalog"))["error"]["code"], "DOWN")
        self.assertEqual(server.handle(self.frame("catalog"))["error"]["code"], "CIRCUIT_OPEN")

    def test_jsonl_server_isolates_invalid_lines(self) -> None:
        source = io.StringIO("not-json\n" + json.dumps(self.frame("probe")) + "\n")
        destination = io.StringIO()
        self.assertEqual(adapter_protocol.serve(DummyAdapter(), source, destination), 0)
        rows = [json.loads(line) for line in destination.getvalue().splitlines()]
        self.assertEqual(rows[0]["error"]["code"], "INVALID_JSON")
        self.assertEqual(rows[1]["status"], "OK")


class ReferenceAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.input_path = self.root / "input.txt"
        self.output_path = self.root / "output.json"
        self.input_path.write_text("private payload", encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def http_config(self, **updates: object) -> dict:
        value: dict[str, object] = {
            "provider": "runtime",
            "endpoint": "http://127.0.0.1:12345",
            "execution_boundary": "UNKNOWN",
            "network_authorized": True,
            "allowed_data_classes": ["PUBLIC", "INTERNAL"],
            "remote_data_classes": ["PUBLIC"],
            "read_roots": [str(self.root)],
            "write_roots": [str(self.root)],
            "timeout_seconds": 1,
        }
        value.update(updates)
        return value

    def test_loopback_is_not_implicitly_a_trusted_host_boundary(self) -> None:
        with self.assertRaisesRegex(reference_adapters.AdapterError, "explicit host-boundary evidence"):
            reference_adapters.OllamaAdapter(self.http_config(execution_boundary="HOST"))

    def test_ollama_cloud_tags_are_separate_remote_fragments(self) -> None:
        adapter = reference_adapters.OllamaAdapter(self.http_config())
        adapter._request = mock.Mock(
            return_value={"models": [{"name": "local-model:latest"}, {"name": "large-model:cloud"}]}
        )
        result = adapter.catalog({})
        by_provider = {item["provider"]: item for item in result["fragments"]}
        self.assertIn("local-model:latest", by_provider["runtime-local"]["models"])
        cloud = by_provider["runtime-cloud-tags"]
        self.assertEqual(cloud["execution_boundary"], "REMOTE")
        self.assertIn("large-model:cloud", cloud["models"])
        with self.assertRaisesRegex(reference_adapters.AdapterError, "explicit remote authorization"):
            adapter.invoke(
                {
                    "operation_id": "op-1",
                    "model": "large-model:cloud",
                    "data_class": "PUBLIC",
                    "input_path": str(self.input_path),
                    "output_path": str(self.output_path),
                }
            )

    def test_openai_compatible_invocation_moves_payload_by_handle(self) -> None:
        adapter = reference_adapters.OpenAICompatibleAdapter(self.http_config(execution_boundary="LOCAL_NETWORK"))
        adapter._request = mock.Mock(return_value={"choices": [{"message": {"content": "generated"}}]})
        result = adapter.invoke(
            {
                "operation_id": "op-http",
                "model": "example",
                "data_class": "PUBLIC",
                "input_path": str(self.input_path),
                "output_path": str(self.output_path),
            }
        )
        self.assertEqual(result["operation_id"], "op-http")
        self.assertNotIn("content", result)
        self.assertEqual(result["dispatch_status"], "REQUESTED_NOT_ATTESTED")
        self.assertIsNone(result["actual_model"])
        self.assertIn("generated", self.output_path.read_text(encoding="utf-8"))
        sent = adapter._request.call_args.args[1]
        self.assertEqual(sent["messages"][0]["content"], "private payload")

    def test_ollama_invocation_attests_actual_model_without_returning_content(self) -> None:
        adapter = reference_adapters.OllamaAdapter(self.http_config())
        adapter._request = mock.Mock(return_value={"model": "local-model:latest", "message": {"content": "generated"}})
        result = adapter.invoke(
            {
                "operation_id": "op-ollama",
                "model": "local-model:latest",
                "data_class": "PUBLIC",
                "input_path": str(self.input_path),
                "output_path": str(self.output_path),
            }
        )
        self.assertEqual(result["requested_model"], "local-model:latest")
        self.assertEqual(result["actual_model"], "local-model:latest")
        self.assertEqual(result["dispatch_status"], "ACTUAL_MODEL_ATTESTED")
        self.assertNotIn("content", result)

    def test_credentials_are_allowlisted_and_endpoint_errors_are_redacted(self) -> None:
        with self.assertRaisesRegex(reference_adapters.AdapterError, "not allowlisted"):
            reference_adapters.OpenAICompatibleAdapter(
                self.http_config(credential_env="SECRET_FOR_TEST", environment_allowlist=[])
            )
        adapter = reference_adapters.OpenAICompatibleAdapter(
            self.http_config(
                endpoint="https://runtime.example.test",
                credential_env="SECRET_FOR_TEST",
                environment_allowlist=["SECRET_FOR_TEST"],
            )
        )
        with mock.patch.dict("os.environ", {"SECRET_FOR_TEST": "do-not-disclose"}, clear=False):
            with mock.patch.object(
                adapter.opener,
                "open",
                side_effect=urllib.error.HTTPError(adapter.endpoint, 401, "includes do-not-disclose", {}, None),
            ):
                with self.assertRaises(reference_adapters.AdapterError) as raised:
                    adapter.catalog({})
        self.assertNotIn("do-not-disclose", str(raised.exception))

    def test_http_timeout_is_classified_separately_from_unavailability(self) -> None:
        adapter = reference_adapters.OllamaAdapter(self.http_config())
        with mock.patch.object(
            adapter.opener,
            "open",
            side_effect=urllib.error.URLError(TimeoutError("timed out")),
        ):
            with self.assertRaises(reference_adapters.AdapterError) as raised:
                adapter.catalog({})
        self.assertEqual(raised.exception.error_class, "TIMEOUT")
        self.assertEqual(raised.exception.code, "HTTP_TIMEOUT")
        self.assertTrue(raised.exception.retryable)

    def test_remote_boundary_requires_data_class_authority(self) -> None:
        adapter = reference_adapters.OpenAICompatibleAdapter(
            self.http_config(execution_boundary="REMOTE", remote_data_classes=[])
        )
        with self.assertRaisesRegex(reference_adapters.AdapterError, "execution boundary"):
            adapter.invoke(
                {
                    "operation_id": "op-remote",
                    "model": "example",
                    "data_class": "PUBLIC",
                    "input_path": str(self.input_path),
                    "output_path": str(self.output_path),
                }
            )

    def test_untrusted_plain_http_never_receives_credentials(self) -> None:
        with self.assertRaisesRegex(reference_adapters.AdapterError, "require HTTPS"):
            reference_adapters.OpenAICompatibleAdapter(
                self.http_config(credential_env="SECRET_FOR_TEST", environment_allowlist=["SECRET_FOR_TEST"])
            )

    def command_config(self, invoke_code: str) -> dict:
        return {
            "provider": "command",
            "execution_boundary": "PROCESS",
            "probe_argv": [sys.executable, "-c", "raise SystemExit(0)"],
            "catalog_argv": [sys.executable, "-c", "import json; print(json.dumps({'fragments': []}))"],
            "invoke_argv": [sys.executable, "-c", invoke_code],
            "environment_allowlist": [],
            "allowed_data_classes": ["PUBLIC"],
            "read_roots": [str(self.root)],
            "write_roots": [str(self.root)],
            "timeout_seconds": 5,
        }

    def test_command_adapter_is_shell_free_and_publishes_atomically(self) -> None:
        adapter = reference_adapters.CommandAdapter(
            self.command_config("import sys; sys.stdout.buffer.write(sys.stdin.buffer.read().upper())")
        )
        with mock.patch("subprocess.run", wraps=reference_adapters.subprocess.run) as run:
            result = adapter.invoke(
                {
                    "operation_id": "op-command",
                    "data_class": "PUBLIC",
                    "input_path": str(self.input_path),
                    "output_path": str(self.output_path),
                }
            )
        self.assertEqual(self.output_path.read_bytes(), b"PRIVATE PAYLOAD")
        self.assertFalse(run.call_args.kwargs["shell"])
        self.assertEqual(result["operation_id"], "op-command")

    def test_failed_command_preserves_previous_output(self) -> None:
        self.output_path.write_text("previous", encoding="utf-8")
        adapter = reference_adapters.CommandAdapter(self.command_config("raise SystemExit(9)"))
        with self.assertRaisesRegex(reference_adapters.AdapterError, "non-zero"):
            adapter.invoke(
                {
                    "operation_id": "op-failed",
                    "data_class": "PUBLIC",
                    "input_path": str(self.input_path),
                    "output_path": str(self.output_path),
                }
            )
        self.assertEqual(self.output_path.read_text(encoding="utf-8"), "previous")

    def test_protocol_schema_is_present_and_language_neutral(self) -> None:
        schema = json.loads(
            (ROOT / "foundation" / "schemas" / "ai-adapter-protocol.schema.json").read_text(encoding="utf-8")
        )
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(
            schema["$defs"]["request"]["properties"]["protocol"]["const"],
            "foundation-ai-adapter-jsonl/v1",
        )
        evidence = json.loads(
            (ROOT / "foundation" / "schemas" / "resource-cost-evidence.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            evidence["properties"]["contract"]["const"], "foundation-resource-cost-evidence/v1"
        )
        self.assertEqual(evidence["properties"]["refresh"]["properties"]["maximum_frequency_seconds"]["minimum"], 86400)


if __name__ == "__main__":
    unittest.main()
