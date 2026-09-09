# Transferable rule set

Status: INFORMATIVE

This directory defines how reusable Foundation rules/provenance are installed or semantically integrated into another repository.

- `manifest.json` is the machine- and AI-readable transfer whitelist and integration contract.
- `AI_TRANSFER.md` defines direct transfer/semantic merge by an AI system.
- `AGENTS.template.md`, `FOUNDATION_RULESET.template.md`, and `repo_map.template.yaml` are target bridge/index templates.
- `Documentation/Standards/SEMANTIC_INTEGRATION_POLICY.md` defines compatibility classes, target-governance discovery, stricter-rule compatibility, adapter migration, and existing-policy interoperability.
- Generic policy sources referenced by the manifest remain canonical in the Foundation repository; the installer maps them into target `.ai/foundation/` paths.

The deterministic installer and an AI use the same manifest. The installer handles file-state planning; semantic integration of an existing repository is performed under the AI transfer/integration contract. This directory is never copied wholesale.

The core rules and language-neutral schemas cover model routing v1/v2, AI work requests and plans, adapter/runtime configuration, execution and validation evidence, provisioning, client integration, manual dispatch, and end-to-end orchestration. Executable references remain explicitly selectable capabilities:

- `model-router` decides among evidenced candidates but never invokes a model;
- `ai-work` plans generic capability work;
- `ai-runtime-adapters` configure, probe, catalog, and invoke isolated Ollama, OpenAI-compatible, or shell-free command runtimes;
- `ai-executor` executes exact generic plans with checkpoints and validation;
- `ai-provisioning` diagnoses hosts and executes only exact approved provision plans;
- `ai-client-integration` plans native, MCP, CLI, launcher, or manual model dispatch and verifies receipts;
- `ai-orchestrator` composes the narrower catalog/evidence/route/invoke/validate/fallback/report path.

Capability dependencies install companion files only. They do not configure or start a runtime and grant no download, network, model, credential, data-transfer, spend, execution, publication, Git, push, or pull-request authority. Runtime configuration, payloads, credentials, model evidence, inventories, checkpoints, and reports stay outside Git. Missing Python, MCP, runtimes, models, providers, evidence, validators, credentials, or network yield a deterministic alternative or a truthful manual/unavailable state without invalidating the Foundation rules.
