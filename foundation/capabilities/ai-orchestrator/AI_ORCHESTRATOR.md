# Optional AI Orchestrator

This capability joins live runtime discovery, router v2, content-handle invocation, deterministic validation, fallback, and a content-free report. It is optional: Foundation rules, installation, validation, and manual work remain valid without Python, this capability, MCP, a runtime, network, credentials, evidence, or any model.

The control contract is `foundation-ai-orchestration/v1`. Prompts and generated answers stay in absolute input/output handles and never enter the orchestration report. The runtime connection store and all orchestration state remain outside Git.

## Evidence before automatic routing

Runtime catalogs prove availability only. They do not prove quality, context size, resource use, price, or model aliases. `model-runtime-evidence.json` may overlay those fields only when a record is fresh and has a locator plus content hash. A requested/actual model mismatch is accepted only with fresh `PROVIDER_DOCUMENTATION` or `PROVIDER_SIGNED_METADATA`; a successful response by itself never creates an alias.

Optional evidence sources use `foundation-model-evidence-sources/v1`. Each source is an exact argv array executed without a shell, receives only allowlisted environment variables, and returns the strict evidence contract on stdout. Successful evidence becomes last-known-good external state. Every attempt, including a failed one, is rate-limited for at least 86,400 seconds. A source may internally perform governed research or use an AI service, but its output still requires explicit provenance and expiry. No scheduler is required: clients can call `refresh-evidence` before planning; fresh state is reused offline.

## Commands

```text
python ai_orchestrator.py [--config ABSOLUTE_RUNTIME_CONFIG] [--state-root ABSOLUTE_EXTERNAL_DIR] plan REQUEST.json
python ai_orchestrator.py [--config ...] [--state-root ...] execute REQUEST.json
python ai_orchestrator.py [--state-root ...] refresh-evidence SOURCES.json
python orchestrator_mcp.py [--config ...] [--state-root ...] [--evidence-sources ...]
```

`LOCAL` never invokes a model and returns `DETERMINISTIC_TOOL_REQUIRED`. Missing or insufficient evidence returns `MANUAL_REQUIRED` with a manual-handoff action. Catalog and invocation failures are isolated per connection and per fallback. `remote_authorized` is passed through but never adds permission beyond the selected connection's own data-class and remote-model policy.

Validation modes are `NONE`, `OUTPUT_NONEMPTY`, `JSON_DOCUMENT`, and `MANUAL_REVIEW`. Structural checks are deterministic; semantic correctness is never fabricated. A retry occurs only through a different route already present in the router's bounded fallback chain.

Before invocation the reference writes a content-free external checkpoint bound to the complete request and input hash. A terminal identical run returns its prior report without invoking again. An `IN_PROGRESS` restart or timeout/protocol ambiguity requires manual provider reconciliation; only a definite pre-invocation availability/permission failure or deterministic validation failure may continue to a different bounded fallback.
