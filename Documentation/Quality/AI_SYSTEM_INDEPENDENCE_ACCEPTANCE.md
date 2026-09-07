# AI system-independence acceptance

Status: RUNTIME EMPIRICAL EVIDENCE

## Contract

`WI-0028` verifies that the Foundation rules and control-plane contracts remain useful when every executable AI component is absent or fails. Optional reference implementations may require Python when selected; default Foundation integrity and direct/manual transfer do not. A component failure may exclude that component, but must not create authority, fabricate evidence, invalidate an unrelated healthy component, or turn an unexecuted action into success.

Automated acceptance uses synthetic local fixtures and deliberately unavailable isolated endpoints/processes. It never stops a productive service to simulate failure. Live runtime checks are separate, read-only or bounded, content-minimized, and never become durable model rankings or cost/quality claims.

## Automated matrix

| Concern | Expected result | Evidence |
|---|---|---|
| no optional capability or executable AI runtime | core policy/schemas install without executable payload; work is manual/unavailable truthfully | `test_default_transfer_contains_no_executable_ai_runtime`, `test_component_failure_matrix_isolated_or_degrades_truthfully` |
| no MCP or network | healthy deterministic process capability remains executable | `test_no_network_or_mcp_does_not_block_healthy_process_tool` |
| missing process, dead endpoint, timeout, invalid response, expired fragment, missing credential | bad entry is excluded; unrelated healthy entry remains usable | component failure matrix plus adapter/router unit tests |
| exhausted money/resource bound or unavailable validator | no unsafe route; manual/unavailable status | component failure matrix plus AI-work/router-v2 tests |
| read-only, local write, no push, branch/PR authorization, forbidden publication | exact effect and capability authorities fail closed | `test_rights_matrix_requires_exact_capability_and_effect_authority` |
| non-public remote data, credentials, logs, adapter synthesis | remote route denied without exact data authority; payload/secret fields rejected; synthesis denied or quarantined | `test_nonpublic_remote_processing_requires_explicit_data_authority` plus AI-work, runtime-adapter, executor, and client-integration privacy tests |
| software, sourced research, documentation, structured data, custom work | executable deterministic work plus independent validation, or truthful manual state | `test_representative_workflows_have_safe_plans_and_independent_validation` |
| Windows, Linux, macOS | the same runtime-neutral contract suite passes | `test_ci_contract_keeps_linux_gate_and_adds_windows_macos_matrix`; `foundation-ci.yml`: Linux completion gate plus Windows/macOS contract matrix |

The full existing suite also covers router-v1 golden compatibility, malformed provider isolation, circuit breaking, bounded timeouts/cancellation, invalid JSON, last-known-good fragments, missing credentials, hard money/RAM/VRAM/CPU/GPU/disk/network/energy constraints, approval scope, resumable execution, and client configuration rollback.

## Windows dual-runtime acceptance — 2026-09-07

Environment: Windows host, loopback only. No credential file was read, no download or paid/remote request was made, and no response content was retained.

1. Ollama local: the already-running loopback service returned a catalog; a smallest available non-cloud-tagged stored model completed a bounded eight-token chat request. The selected tag was explicitly filtered against all Foundation cloud-tag forms. Result: `PASSED` in 11.907 seconds. The test did not stop Ollama; no model remained loaded afterward.
2. LM Studio: the CLI was present while the API server was initially stopped and no model was loaded. A resource estimate preceded the run (11.28 GiB expected, 48 GiB host memory free). The test started a server bound only to `127.0.0.1:1234`, loaded one already-present model under a temporary `foundation-acceptance` identifier with 2,048-token context, CPU-only request, single concurrency and 120-second TTL, then completed an OpenAI-compatible eight-token chat request. Result: `PASSED` in 2.530 seconds. The test stopped the server it had started and verified it was stopped.

Limitations: this proves two independent host execution paths and their protocol compatibility at that time. It does not establish model quality, future availability, pricing, production capacity, universal host-boundary trust, or automatic client model switching. The runtime observations are evidence for this acceptance only and are not Foundation model recommendations.

## Completion interpretation

If every optional component is absent together, the Foundation still supplies readable policy, schemas, transfer instructions, portable tiers, and truthful manual/unavailable outcomes. When one component fails, healthy alternatives remain eligible. If no safe alternative exists, `MANUAL_REQUIRED`, `UNAVAILABLE`, `BLOCKED`, `MANUAL_DISPATCH_REQUIRED`, or `REQUESTED_NOT_ATTESTED` is the successful contract behavior—not an implementation failure.

`MANUAL_DISPATCH_REQUIRED` is also the deliberate fallback for a client that cannot switch models automatically. It gives the user an expiring, content-separated prompt handoff and an evidenced tier/model suggestion. The suggestion does not claim selection or execution: the subsequent result remains `REQUESTED_NOT_ATTESTED` until trusted host execution/response metadata identifies the actual model.
