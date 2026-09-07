# AI Work Orchestration Policy

Status: AUTHORITATIVE

This policy defines `foundation-ai-work/v1`, a runtime- and vendor-neutral control plane for AI-assisted development, research, documentation, structured data, media, and project-defined work. It governs planning and evidence even when no executable AI component exists. Models, deterministic tools, retrieval sources, renderers, validators, external services, human review points, transports, and runtimes are discoverable capabilities, not Foundation prerequisites.

## Invariants

- Foundation rules, installation, upgrade assessment, and `FOUNDATION_INTEGRITY` validation MUST remain usable when Python, MCP, a model, a provider, a network, an executor, or every optional capability is unavailable.
- Planning MUST apply data handling, authorization, required capability, quality, health/freshness, validation, time, money, and resource constraints before economic ranking.
- Discovery, routing, code generation, adapter synthesis, and model agreement grant no file, network, credential, spend, Git, push, pull-request, publication, or approval authority.
- Effective authority is the intersection of the request, project policy, caller authority, adapter requirements, and execution environment. Missing authority fails closed.
- Payload content is separate from the control plane. Requests use short-lived `stdin`, file, or opaque handles. Prompts and responses are not persisted or logged by default.
- Concrete model names, prices, endpoints, host paths, credentials, health observations, and runtime inventories are expiring runtime facts and MUST NOT become Foundation policy.
- A component failure invalidates only evidence or catalog material derived from that component. Healthy alternatives remain eligible.
- A planner or executor MUST report `MANUAL_REQUIRED`, `UNAVAILABLE`, or `BLOCKED` honestly. It MUST NOT convert absence, timeout, inconclusive evidence, or unknown state into success.

## WorkRequest

A `WorkRequest` declares an open `task_class`, data class, risk, input/output handles, required capabilities, execution-boundary constraints, authorization envelope, resource/cost/time limits, and validation contract. Project-specific task classes are allowed without changing the Foundation schema.

Data classes are `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, and `RESTRICTED`. A project may map a richer taxonomy while preserving or strengthening these boundaries. Remote or unknown-boundary processing of non-public data requires explicit project permission for that data class and destination. A product name, loopback address, process name, or successful probe is not proof of a trusted boundary.

## CapabilityDescriptor

A descriptor identifies a capability type, protocol/version, supported functions, deterministic status, execution boundary, requested authorities, data-class allowance, health/freshness window, provenance, and evidenced cost/resource model. Capability types include `DETERMINISTIC_TOOL`, `MODEL`, `RETRIEVAL`, `RENDERER`, `VALIDATOR`, `EXTERNAL_SERVICE`, and `HUMAN`.

Execution boundaries are `PROCESS`, `HOST`, `LOCAL_NETWORK`, `REMOTE`, `UNKNOWN`, and `HUMAN`. `HOST` means execution on the current trusted host only when project policy and runtime evidence establish that fact. `localhost`, a local client process, or an Ollama product label alone is insufficient.

Health is scoped and expiring. Expired or malformed health excludes that descriptor without making unrelated descriptors unavailable. Aggregators keep provider fragments and last-known-good records separately; stale material remains identifiable and is not silently treated as current.

## Planning and degradation

An `ExecutionPlan` is a directed acyclic graph of steps, alternatives, fallbacks, budgets, validation requirements, and grouped approval points. The planner performs no invocation. It returns:

- `EXECUTABLE` only when a complete bounded plan exists under current constraints and authority;
- `MANUAL_REQUIRED` when a human capability or decision can safely close a known gap;
- `UNAVAILABLE` when required capabilities or validators are not currently available;
- `BLOCKED` when policy, privacy, authority, or a hard limit prohibits execution.

When a deterministic capability sufficiently and verifiably fulfills the task, select it ahead of a model. “Local first” is not a fixed rule: data sovereignty, total expected cost, quality, availability, validation, and measured resource pressure decide together.

## Validation and human approval

Validation evidence states its method, producer, independence, scope, provenance, freshness, and result: `PASSED`, `FAILED`, `INCONCLUSIVE`, or `UNAVAILABLE`. Missing evidence is not passing evidence. Model self-review or agreement between non-independent attempts is not deterministic proof.

Reversible drafts and intermediate work may proceed within the authorization envelope. Deterministically validated outputs may continue automatically. Source checking or genuinely independent comparison may increase confidence for nondeterministic work, but high-impact or insufficiently verifiable conclusions require a human checkpoint.

Human approval is grouped at risk boundaries rather than requested after every operation. It is required before irreversible publication or mutation, sensitive data transmission, unplanned spend, high-impact action, privilege expansion, or acceptance without required evidence. Approval applies only to the described checkpoint and does not grant broader future authority.

Retries require changed inputs, a different capability, or new evidence. A resumable executor must use stable operation/idempotency keys so restart cannot duplicate external effects.

## Persistence and reporting

Runtime state lives outside version control. By default it contains only identifiers, hashes, statuses, timestamps, attempt metadata, cost/resource measurements, approval references, and validation provenance. It contains no prompt, response, retrieved document, secret, environment dump, absolute host path, or payload content unless an explicit target rule authorizes that exact retention.

An `ExecutionReport` records attempts, validation, limits, costs/resources, constraints, and remaining actions without inventing success. A `GapReport` identifies a missing capability, tested alternatives, an optional least-privilege local remedy, and the authority needed to apply it. Without repository authority, gap reports remain local/stdout; they do not create issues, commits, branches, pushes, or pull requests.

## Provisioning and local adapter synthesis

A `ProvisionPlan` is read-only until explicitly approved. It is content-addressed, expires, and lists exact source, artifact/model identifier, target runtime, license/use notice, expected transfer/disk/memory, network destination, monetary ceiling, verification, rollback, and recovery. Automated provisioning may perform only actions included in the approved plan; partial failure must not look complete.

Local adapter synthesis requires explicit `allow_local_adapter_synthesis` authority. Generated material remains outside the repository, starts without network, credentials, or repository write access, includes its source hash, and is quarantined until protocol conformance passes. Durable repository adoption is a separate authorized workflow.

## Compatibility

`foundation-model-router/v1` remains valid. New orchestration may consume `foundation-model-router/v2`, but must preserve v1 request/decision behavior and the existing tier meanings. `LOCAL` always means deterministic work for which no generative model is required. A model executing on the host remains `ECONOMICAL`, `BALANCED`, or `FRONTIER` with `execution_boundary=HOST`; target aliases such as `LOCAL_ECONOMICAL` require an explicit semantic mapping and do not redefine Foundation tiers.

Reference implementations are optional and replaceable. Another language, client, adapter, provider, transport, executor, or project-specific planner is compatible when it enforces at least these contracts and reports unavailable states truthfully.
