"""Offline process-backed tests for two arbitrary providers through public facades."""
from __future__ import annotations

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'foundation/capabilities/ai-runtime-adapters'))
import runtime_configuration as runtime
import runtime_mcp
from adapter_protocol import AdapterError
from tests import test_ai_orchestrator as orchestration


PROGRAM = r'''
import hashlib, json, os, sys, time
from pathlib import Path
provider, model, mode = sys.argv[1:4]
frame = json.loads(sys.stdin.readline())
operation, arguments = frame['operation'], frame['arguments']
if mode == 'timeout' and operation == 'invoke':
    time.sleep(5)
if mode == 'exit':
    sys.exit(7)
if mode == 'flood':
    sys.stdout.write('x' * 2000000)
    sys.exit(0)
if mode == 'stderr':
    sys.stderr.write('x' * 100000)
    sys.stderr.flush()
if operation == 'probe':
    result = {'health': {'state': 'HEALTHY'}}
    if len(sys.argv) > 4:
        Path(sys.argv[4]).write_text(json.dumps(dict(os.environ)), encoding='utf-8')
elif operation == 'catalog':
    result = {'fragments': [{
        'schema_version': 2, 'contract': 'foundation-model-router/v2', 'provider': provider,
        'adapter': 'synthetic-stdio/v1', 'execution_boundary': 'HOST',
        'generated_at': '2026-09-08T11:59:00Z', 'valid_until': '2026-09-09T11:00:00Z',
        'pricing_epoch': 'synthetic', 'health': {'state': 'HEALTHY',
            'checked_at': '2026-09-08T11:59:00Z', 'expires_at': '2026-09-09T11:00:00Z'},
        'provenance': {'source': 'synthetic', 'observed_at': '2026-09-08T11:59:00Z'},
        'models': {model: {'model_id': model, 'availability': 'AVAILABLE', 'assessment': 'UNASSESSED',
            'capabilities': ['text'], 'context_window': None, 'quality_prior': {'*': 0.5},
            'quality_provenance': 'UNKNOWN', 'supported_tiers': ['BALANCED'],
            'reasoning_efforts': ['low'], 'resource_estimate': {}, 'resource_provenance': 'UNKNOWN', 'pricing': None}}
    }]}
else:
    target = Path(arguments['output_path'])
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = b'{"message":"synthetic output payload"}\n'
    target.write_bytes(payload)
    result = {'status': 'COMPLETED', 'operation_id': arguments['operation_id'],
        'requested_model': arguments['model'], 'actual_model': None if mode == 'missing' else model,
        'output_bytes': len(payload), 'output_sha256': 'sha256:' + hashlib.sha256(payload).hexdigest()}
    if mode == 'hash':
        result['output_sha256'] = 'sha256:' + '0' * 64
reply = {'protocol': frame['protocol'], 'request_id': frame['request_id'], 'status': 'OK', 'result': result}
if mode == 'id': reply['request_id'] = 'foreign-request'
if mode == 'protocol': reply['protocol'] = 'foreign-protocol'
if mode == 'payload': result['nested'] = {'response': 'private marker'}
if mode == 'catalog-shape' and operation == 'catalog': result['fragments'][0]['models'] = {'bad': []}
if mode == 'error':
    reply.pop('result')
    reply.update(status='ERROR', error={'class': 'AVAILABILITY', 'code': 'REMOTE_DOWN', 'message': 'private marker', 'retryable': True})
if mode == 'malformed':
    print('{bad json')
elif mode == 'multi':
    print(json.dumps(reply)); print(json.dumps(reply))
elif mode == 'duplicate':
    print(json.dumps(reply)[:-1] + ',"status":"OK"}')
else:
    print(json.dumps(reply))
'''


class StdioRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.program = self.root / 'synthetic_adapter.py'
        self.program.write_text(PROGRAM, encoding='utf-8')
        (self.root / 'input').mkdir()
        (self.root / 'input/prompt.txt').write_text('synthetic input payload', encoding='utf-8')
        self.store = runtime.ConfigurationStore(self.root / 'runtime.json')

    def tearDown(self) -> None:
        self.temp.cleanup()

    def connection(self, provider: str = 'Nebula', model: str = 'alpha', mode: str = 'normal', **updates: object) -> dict:
        value = runtime._connection_defaults(self.root, '', 'stdio')
        value.update(argv=[str(Path(sys.executable).resolve()), str(self.program), provider, model, mode],
                     label=provider, execution_boundary='HOST', read_roots=[str(self.root / 'input')],
                     write_roots=[str(self.root / 'output')], timeout_seconds=3)
        value.update(updates)
        return value

    def arguments(self, **updates: object) -> dict:
        value = dict(operation_id='synthetic-operation', model='alpha', data_class='PUBLIC',
                     input_path=str(self.root / 'input/prompt.txt'), output_path=str(self.root / 'output/result.json'))
        value.update(updates)
        return value

    def save(self, connections: dict) -> None:
        value = runtime.empty_configuration()
        value['connections'] = connections
        self.store.save(value)

    def test_two_arbitrary_providers_configure_catalog_invoke_and_mcp(self) -> None:
        self.save({'nebula': self.connection(), 'cedar': self.connection('Cedar', 'beta')})
        for name, model in [('nebula', 'alpha'), ('cedar', 'beta')]:
            with self.subTest(provider=name):
                connection = self.store.load_connection(name)
                probe = runtime.execute_adapter(connection, 'probe', {})
                self.assertEqual(probe['health']['state'], 'HEALTHY')
                catalog = runtime_mcp.call_tool('runtime_catalog', {'connection_id': name}, self.store)
                self.assertFalse(catalog['isError'])
                self.assertIn(model, catalog['structuredContent']['fragments'][0]['models'])
                invoke = runtime_mcp.call_tool('runtime_invoke', {'connection_id': name, **self.arguments(
                    model=model, output_path=str(self.root / f'output/{name}.json'))}, self.store)
                self.assertFalse(invoke['isError'])
                self.assertEqual(invoke['structuredContent']['dispatch_status'], 'REQUESTED_NOT_ATTESTED')
                self.assertNotIn('synthetic output payload', json.dumps(invoke))
                self.assertNotIn('synthetic input payload', json.dumps(invoke))

    def test_cli_configure_and_invoke_share_stdio_contract(self) -> None:
        connection = self.connection()
        argv = ['--config', str(self.store.path), 'configure', '--yes', '--connection-id', 'nebula',
                '--adapter', 'stdio', '--argv-json', json.dumps(connection['argv']), '--environment-allowlist',
                '--execution-boundary', 'HOST', '--read-root', str(self.root / 'input'),
                '--write-root', str(self.root / 'output'), '--selection', 'PINNED', '--default-model', 'alpha']
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(runtime.main(argv), 0)
            self.assertEqual(runtime.main(['--config', str(self.store.path), 'invoke', 'nebula',
                '--operation-id', 'cli-test', '--data-class', 'PUBLIC', '--input-path', str(self.root / 'input/prompt.txt'),
                '--output-path', str(self.root / 'output/cli.json')]), 0)

    def test_wizard_selects_type_before_discovery_and_never_discovers_stdio(self) -> None:
        prompts = []
        def answer(prompt: str) -> str:
            prompts.append(prompt)
            if prompt.startswith('Adapter-Typ'): return 'STDIO'
            if prompt.startswith('Exakte Argumentliste'): return json.dumps(self.connection()['argv'])
            if prompt.startswith('Ausführungsgrenze'): return 'HOST'
            if prompt.startswith('Aktion'): return 'SAVE'
            return ''
        with patch.object(runtime, 'discover_candidates') as discover:
            runtime.interactive_configure(self.store, input_fn=answer, output_fn=lambda _: None)
        discover.assert_not_called()
        self.assertTrue(prompts[0].startswith('Adapter-Typ'))
        self.assertEqual(self.store.load_connection('stdio-runtime')['adapter'], 'stdio')

    def test_closed_configuration_rejects_unsafe_or_inapplicable_fields(self) -> None:
        schema = json.loads((ROOT / 'foundation/schemas/ai-runtime-configuration.schema.json').read_text(encoding='utf-8'))
        variant = schema['$defs']['stdio_connection']
        self.assertFalse(variant['additionalProperties'])
        normalized = runtime.validate_connection('test', self.connection())
        self.assertLessEqual(set(variant['required']), set(normalized))
        self.assertLessEqual(set(normalized), set(variant['properties']))
        self.assertNotIn('endpoint', variant['properties'])
        for updates in [dict(argv='command string'), dict(argv=['python']), dict(argv=['C:\\run.cmd'] if os.name == 'nt' else ['/tmp/run.sh']),
                        dict(environment_allowlist=['BAD-NAME']), dict(environment_allowlist=['KEY', 'KEY']),
                        dict(cwd='relative'), dict(endpoint='http://127.0.0.1'), dict(trust_model_metadata='yes'),
                        dict(credential={'source': 'ENVIRONMENT', 'source_name': 'KEY', 'export_as': 'KEY'}),
                        dict(timeout_seconds=float('nan')), dict(adapter=[]), dict(execution_boundary=[]),
                        dict(model_selection={'mode': [], 'default_model': None})]:
            with self.subTest(updates=updates), self.assertRaises(runtime.ConfigurationError):
                runtime.validate_connection('test', self.connection(**updates))

    def test_environment_is_explicit_and_shell_is_disabled(self) -> None:
        observed = self.root / 'environment.json'
        connection = self.connection(environment_allowlist=['ALLOWED_KEY'])
        connection['argv'].append(str(observed))
        import stdio_adapter
        original = stdio_adapter.subprocess.Popen
        with patch.dict(os.environ, {'ALLOWED_KEY': 'synthetic', 'FORBIDDEN_KEY': 'do-not-inherit'}), patch.object(
                stdio_adapter.subprocess, 'Popen', wraps=original) as launch:
            runtime.execute_adapter(connection, 'probe', {})
        self.assertIs(launch.call_args.kwargs['shell'], False)
        self.assertEqual(launch.call_args.kwargs['env'], {'ALLOWED_KEY': 'synthetic'})
        seen = json.loads(observed.read_text(encoding='utf-8'))
        self.assertEqual(seen['ALLOWED_KEY'], 'synthetic')
        self.assertNotIn('FORBIDDEN_KEY', seen)

    def test_malformed_identity_payload_and_bounded_output_fail_closed(self) -> None:
        for mode in ['id', 'protocol', 'malformed', 'multi', 'duplicate', 'payload', 'error', 'exit', 'flood', 'stderr']:
            with self.subTest(mode=mode), self.assertRaises(AdapterError) as error:
                runtime.execute_adapter(self.connection(mode=mode), 'probe', {})
            self.assertEqual(error.exception.error_class, 'PROTOCOL')
            self.assertNotIn('private marker', str(error.exception))

    def test_permissions_checked_before_process_start(self) -> None:
        import stdio_adapter
        for connection, arguments in [
            (self.connection(allowed_data_classes=[]), self.arguments()),
            (self.connection(execution_boundary='UNKNOWN', remote_data_classes=['PUBLIC']), self.arguments(remote_authorized=True)),
            (self.connection(execution_boundary='REMOTE', network_authorized=True), self.arguments(remote_authorized=True)),
            (self.connection(execution_boundary='REMOTE', network_authorized=True, remote_data_classes=['PUBLIC']), self.arguments()),
            (self.connection(), self.arguments(input_path=str(self.root / 'outside.txt'))),
        ]:
            with self.subTest(connection=connection), patch.object(stdio_adapter.subprocess, 'Popen') as launch:
                with self.assertRaises(AdapterError): runtime.execute_adapter(connection, 'invoke', arguments)
                launch.assert_not_called()

    def test_receipt_hash_and_missing_attestation(self) -> None:
        with self.assertRaises(AdapterError) as error:
            runtime.execute_adapter(self.connection(mode='hash'), 'invoke', self.arguments())
        self.assertEqual(error.exception.code, 'OUTPUT_RECEIPT_MISMATCH')
        result = runtime.execute_adapter(self.connection(mode='missing', trust_model_metadata=True), 'invoke',
                                        self.arguments(output_path=str(self.root / 'output/missing.json')))
        self.assertIsNone(result['actual_model'])
        self.assertEqual(result['dispatch_status'], 'REQUESTED_NOT_ATTESTED')

    def test_catalog_never_promotes_locality_or_extends_stale_expiry(self) -> None:
        connection = self.connection(execution_boundary='UNKNOWN', network_authorized=True)
        result = runtime.execute_adapter(connection, 'catalog', {})
        fragment = result['fragments'][0]
        self.assertEqual(fragment['execution_boundary'], 'UNKNOWN')
        self.assertEqual(fragment['valid_until'], '2026-09-09T11:00:00Z')
        import stdio_adapter
        bad = {'fragments': [{**fragment, 'execution_boundary': 'REMOTE'}]}
        adapter = runtime.create_adapter(self.connection())
        with patch.object(adapter, '_call', return_value=bad), self.assertRaises(AdapterError):
            adapter.catalog({})

    def test_handle_limits_stale_outputs_and_unknown_model_do_not_invoke(self) -> None:
        import stdio_adapter
        with patch.object(stdio_adapter, 'MAX_HANDLE_BYTES', 2), self.assertRaises(AdapterError) as error:
            runtime.execute_adapter(self.connection(), 'invoke', self.arguments())
        self.assertEqual(error.exception.code, 'INPUT_TOO_LARGE')
        target = self.root / 'output/result.json'
        target.parent.mkdir()
        target.write_text('stale', encoding='utf-8')
        with self.assertRaises(AdapterError) as error:
            runtime.execute_adapter(self.connection(), 'invoke', self.arguments())
        self.assertEqual(error.exception.code, 'OUTPUT_ALREADY_EXISTS')
        self.save({'nebula': self.connection()})
        args = self.arguments()
        del args['model']
        result = runtime_mcp.call_tool('runtime_invoke', {'connection_id': 'nebula', **args}, self.store)
        self.assertTrue(result['isError'])
        self.assertEqual(result['structuredContent']['reason_code'], 'MODEL_SELECTION_REQUIRED')

    def orchestrate(self, mode: str = 'normal', trust: bool = True, provider: str = 'Nebula', model: str = 'alpha') -> dict:
        self.save({'one': self.connection(provider, model, mode, trust_model_metadata=trust),
                   'broken': self.connection(mode='malformed')})
        source = {'kind': 'PROJECT_CONFIGURATION', 'locator': 'synthetic:test', 'content_sha256': 'sha256:' + 'a' * 64}
        records = [dict(connection_id='one', model_id=model, profile=orchestration.profile(), source=source,
                        observed_at='2026-09-08T11:00:00Z', valid_until='2026-09-09T11:00:00Z')]
        value = orchestration.request(self.root)
        return orchestration.ai_orchestrator.plan_or_execute(value, execute=True, config_path=self.store.path,
            state_root=self.root / 'state', evidence_path=orchestration.evidence(self.root, records=records), at=orchestration.AT)

    def test_two_providers_execute_via_orchestrator_with_isolated_catalog_failure(self) -> None:
        for provider, model in [('Nebula', 'alpha'), ('Cedar', 'beta')]:
            with self.subTest(provider=provider):
                # Each scenario has a distinct checkpoint and output handle.
                result = self.orchestrate(provider=provider, model=model)
                self.assertEqual(result['status'], 'COMPLETED')
                self.assertEqual(result['attempts'][0]['actual_model'], model)
                self.assertEqual(next(row for row in result['catalog_status'] if row['connection_id'] == 'broken')['status'], 'UNAVAILABLE')
                (self.root / 'output/result.json').unlink()
                for file in (self.root / 'state/checkpoints').glob('*'): file.unlink()

    def test_untrusted_model_metadata_requires_manual_reconciliation(self) -> None:
        result = self.orchestrate(trust=False)
        self.assertEqual(result['status'], 'MANUAL_REQUIRED')
        self.assertIn('ACTUAL_MODEL_NOT_ATTESTED', result['reason_codes'])
        self.assertEqual(len(result['attempts']), 1)

    def test_invalid_catalog_structure_and_configuration_are_isolated(self) -> None:
        self.save({'one': self.connection(trust_model_metadata=True), 'broken': self.connection(mode='catalog-shape')})
        document = self.store.load()
        document['connections']['invalid'] = self.connection(adapter=[])
        runtime.atomic_write_json(self.store.path, document)
        result = orchestration.ai_orchestrator.plan_or_execute(orchestration.request(self.root), execute=True,
            config_path=self.store.path, state_root=self.root / 'state',
            evidence_path=orchestration.evidence(self.root), at=orchestration.AT)
        self.assertEqual(result['status'], 'COMPLETED')
        statuses = {row['connection_id']: row['status'] for row in result['catalog_status']}
        self.assertEqual(statuses, {'one': 'AVAILABLE', 'broken': 'UNAVAILABLE', 'invalid': 'INVALID'})

    def test_child_invocation_error_stops_before_eligible_fallback(self) -> None:
        self.save({'one': self.connection(mode='error', trust_model_metadata=True),
                   'two': self.connection('Cedar', 'beta', trust_model_metadata=True)})
        # Only invoke returns an error; both catalogs stay available.
        text = self.program.read_text(encoding='utf-8').replace("if mode == 'error':", "if mode == 'error' and operation == 'invoke':")
        self.program.write_text(text, encoding='utf-8')
        source = {'kind': 'PROJECT_CONFIGURATION', 'locator': 'synthetic:test', 'content_sha256': 'sha256:' + 'a' * 64}
        records = [dict(connection_id=name, model_id=model, profile=orchestration.profile(cost=cost), source=source,
                        observed_at='2026-09-08T11:00:00Z', valid_until='2026-09-09T11:00:00Z')
                   for name, model, cost in [('one', 'alpha', 0), ('two', 'beta', 5)]]
        result = orchestration.ai_orchestrator.plan_or_execute(orchestration.request(self.root), execute=True,
            config_path=self.store.path, state_root=self.root / 'state',
            evidence_path=orchestration.evidence(self.root, records=records), at=orchestration.AT)
        self.assertEqual(result['status'], 'MANUAL_REQUIRED')
        self.assertEqual(len(result['attempts']), 1)
        self.assertEqual(result['attempts'][0]['reason_code'], 'ADAPTER_REPORTED_ERROR')
        self.assertIn('AMBIGUOUS_INVOCATION_RESULT', result['reason_codes'])

    def test_timeout_is_ambiguous_and_checkpoint_prevents_retry(self) -> None:
        self.save({'one': self.connection(mode='timeout', timeout_seconds=0.4, trust_model_metadata=True)})
        args = dict(execute=True, config_path=self.store.path, state_root=self.root / 'state',
                    evidence_path=orchestration.evidence(self.root), at=orchestration.AT)
        first = orchestration.ai_orchestrator.plan_or_execute(orchestration.request(self.root), **args)
        self.assertEqual(first['status'], 'MANUAL_REQUIRED')
        self.assertEqual(len(first['attempts']), 1)
        self.assertIn('AMBIGUOUS_INVOCATION_RESULT', first['reason_codes'])
        second = orchestration.ai_orchestrator.plan_or_execute(orchestration.request(self.root), **args)
        self.assertIn('AMBIGUOUS_PRIOR_INVOCATION', second['reason_codes'])
        self.assertFalse((self.root / 'output/result.json').exists())


if __name__ == '__main__':
    unittest.main()
