# Architecture Overview

Status: INFORMATIVE

The Foundation separates durable governance from optional execution. Its rules, schemas, installation model, and truthful manual fallbacks remain usable when Python, MCP, Ollama, a model, a provider, a network, or every executable AI component is absent.

## Repository and transfer boundary

1. **Foundation source project** — its own README, license, development governance, registry/backlog, status, handover, decisions, quality evidence, tests, and tools.
2. **Transferable rule set** — the explicit `core`, adapter, and optional-capability whitelist in `foundation/manifest.json`. The manifest is also the single ruleset-version and portable source-hash authority.
3. **Transfer mechanisms** — direct semantic AI transfer and the deterministic installer consume the same manifest. The optional deterministic ZIP transports that exact manifest payload and minimum installer runtime for offline use; it does not create a third integration policy.

A target repository never receives Foundation-project state merely because a file exists in this repository. Its README, root license, architecture, context, decisions, status, backlog, validation system, identifier history, and Registration Authority remain project-owned. Generic reusable policies are mapped to `.ai/foundation/`, and selected capability code is installed only when explicitly requested.

The target root `AGENTS.md` is a discovery bridge. If absent, it can be created from the transfer template. If it differs, deterministic installation reports `MERGE_REQUIRED`; semantic transfer preserves project instructions and merges only the marked Foundation bridge. A clean installation records content-minimized provenance without claiming semantic or runtime validation.

## AI work layers

| Layer | Contract/reference | Responsibility | Required? |
| --- | --- | --- | --- |
| Governance | `foundation-ai-work/v1`, policies and JSON Schemas | Describes work, data/risk, capabilities, effects, limits, validation and truthful terminal states | yes as readable rules when transferred |
| Planning | optional `ai-work` | Produces an `ExecutionPlan` or `GapReport`; never invokes a capability | no |
| Model decision | optional `model-router` | Preserves router v1 and adds v2 provider-fragment, boundary, evidence, resource and complete-chain routing | no |
| Runtime access | optional `ai-runtime-adapters` | Configures and probes named Ollama/OpenAI-compatible/command connections and invokes explicit models through content handles | no |
| Generic execution | optional `ai-executor` | Executes an exact AI-work plan with checkpoints, limits, approvals, idempotency and validation evidence | no |
| Host preparation | optional `ai-provisioning` | Diagnoses/inventories runtimes and performs only exact approved bounded provision plans; caches verified cost evidence | no |
| Client integration | optional `ai-client-integration` | Detects, plans, applies, verifies and rolls back client configuration; handles native or manual model dispatch evidence | no |
| Routed model facade | optional `ai-orchestrator` | Composes catalog, fresh model evidence, router v2, content-handle invocation, deterministic validation, fallback and reporting | no |

The router is intentionally decision-only. Runtime adapters may invoke a caller-selected model without the router. The generic executor runs a validated `ExecutionPlan`; the narrower orchestrator directly composes the model-routing pipeline. Manifest dependency declarations install companion code but never merge these authority boundaries or grant execution, network, credential, data-transfer, spend, publication, Git, push, or pull-request permission.

## Data, evidence, and runtime state

Control-plane contracts carry identifiers, hashes, classifications, limits, status, cost/resource totals and evidence metadata. Prompts, retrieved material and generated content travel through short-lived allowlisted handles or stdin/stdout protocols and are not persisted by default. Credentials, endpoint configuration, live inventories, model profiles, evidence-source definitions, checkpoints, reports, backups, downloads and host paths stay outside version control.

Discovery is not trust or authority. Catalog presence proves only an observation of availability. Automatic routing requires fresh source-backed capability/quality/context/cost evidence. A requested model is distinct from the actual model; `ATTESTED` requires matching response/execution metadata from a configured trusted issuer. Otherwise the system emits `REQUESTED_NOT_ATTESTED` or an expiring `MANUAL_DISPATCH_REQUIRED` handoff.

## Failure and validation behavior

Each provider, adapter, validator and evidence source has an independent health/expiry boundary. One malformed, expired or unavailable component is excluded without invalidating healthy alternatives. With no safe automatic path, the successful contract result is `MANUAL_REQUIRED`, `UNAVAILABLE`, `BLOCKED`, or the portable tier only—not an invented model, price, capability, execution or validation claim.

Foundation validation proves `FOUNDATION_INTEGRITY` only. Target-specific semantics and real runtime behavior remain `PROJECT_SEMANTIC` and `RUNTIME_EMPIRICAL` responsibilities. Tool/vendor adapters remain thin discovery/import bridges; no subagent, web, shell, Git, memory, model-switching or cloud feature is assumed.
