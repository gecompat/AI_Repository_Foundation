# AI Repository Foundation

AI Repository Foundation is a reusable framework for governing AI-assisted and human-maintained repositories. It gives a project durable instructions, safe working boundaries, stable artifact identities, validation contracts, and a way to continue work without depending on one conversation or AI provider.

The core consists of readable rules, schemas, discovery bridges, and small deterministic helpers. Optional capabilities add planning, model selection, runtime invocation, client integration, and provisioning. You can use the core with your existing tools and add executable capabilities only where they help.

## What it helps you do

- Continue a software, research, documentation, or knowledge project from repository state rather than chat memory.
- Integrate AI into an existing repository while preserving its rules, identifiers, license, and validation system.
- Give humans and AI the same authority for registering work items and decisions.
- Select and invoke models through evidenced capabilities and explicit data boundaries.
- Reduce repeated rule reading and unnecessary processing while retaining required validation and truthful evidence.

## Functionality at a glance

| Area | Core functionality | Optional executable capability / boundary |
| --- | --- | --- |
| Governance and continuation | Authority, privacy, safe operations, project context and handover contracts | Existing project governance remains authoritative; chat history is not durable truth |
| Installation, upgrades and provenance | Manifest whitelist, semantic feature assessment, portable hashes and installation receipt | Deterministic installer or direct AI transfer; differing files require semantic integration |
| Identity and registration | Persistent UIDs, stable references, shared Registration Authority | `artifact-registration-clients`, `artifact-registry-github`; existing compatible authorities may remain |
| Validation and continuity | Integrity/semantic/runtime scopes, honest status, repository recovery contracts | Foundation integrity cannot prove target domain correctness or grant bypass authority |
| Model routing | Portable capability tiers and evidence contracts | `model-router` decides; it does not invoke models or invent prices/quality |
| Planning and execution | Work, capability, plan, approval, checkpoint and report schemas | `ai-work` plans; `ai-executor` executes exact generic plans |
| Runtime and client integration | Language-neutral JSONL, configuration and dispatch evidence contracts | `ai-runtime-adapters`, `ai-client-integration`, `ai-orchestrator`; missing evidence leads to manual handling |
| Bounded autonomous jobs | Optional startup routing, pre-model heartbeat checks, fenced chat handoff and fixed notifications | `ai-orchestrator` control; autonomy off by default, finite authority/budget and evidenced client support required |
| Host preparation | Inventory, provisioning and resource-cost evidence contracts | `ai-provisioning`; installation of capability code does not authorize downloads or spending |
| Session lifecycle | Counters, natural boundaries, rotation decisions and delta handoffs | `ai-work` evaluates decisions; successor creation depends on evidenced client support |
| Processing efficiency | Scoped reading, session-local reuse, bounded budget decisions and required overhead assessment | `rule-context-cache` adds persistent fingerprints; caches are never authority or evidence |

The [user guide](Documentation/Guides/USER_GUIDE.md) explains these areas, all ten optional capabilities, and their limits. The [architecture overview](Documentation/Architecture/OVERVIEW.md) explains components, data flow, dependencies, and failure behavior.

## Minimal installation without product adapters

From a Foundation checkout, preview the core transfer into your project, review the result, then apply a clean plan:

```text
python tools/install_foundation.py ../my-project --adapters none --capabilities none
python tools/install_foundation.py ../my-project --adapters none --capabilities none --apply
python tools/foundation_validator.py --target ../my-project --adapters none
```

The installer classifies files as `CREATE`, `UNCHANGED`, `MERGE_REQUIRED`, or `CONFLICT` and never overwrites a differing file. It verifies portable source hashes and records installation provenance after a clean apply. For an existing repository, follow the [integration walkthrough](Documentation/Guides/USER_GUIDE.md#integrating-an-existing-repository) before claiming completion.

The installer’s existing defaults remain GitHub Copilot, Claude Code, and Gemini discovery adapters, with no optional capabilities. The explicit `--adapters none` recipe above is provider-neutral. Python runs this reference installer; another implementation may follow the [direct AI transfer protocol](foundation/AI_TRANSFER.md).

Only [manifest-listed](foundation/manifest.json) rules and selected modules are transferred. The Foundation project's README, root license, changelog, identity registry, backlog, status, handover, and internal decisions stay here. Your project keeps its own state and governance. Transferred MIT material carries a [namespaced notice](foundation/AI_REPOSITORY_FOUNDATION_NOTICE.md) without replacing your root license.

## Provider openness

The core defines capabilities and evidence rather than a provider list. Any client or provider can integrate through compatible contracts. Codex, Copilot, Claude, Gemini, and other named products are optional reference paths with distinct observed capabilities.

`ai-runtime-adapters` supports Ollama HTTP, OpenAI-compatible HTTP, and explicitly configured `stdio` JSONL programs through the shared configuration, CLI, MCP, and orchestrator paths. “OpenAI-compatible” names an HTTP interface format; it does not require an OpenAI account or prove compatibility with every endpoint. A provider with another API can supply a reviewed JSONL wrapper in any implementation language. The earlier raw-output `CommandAdapter` remains available separately.

Actual compatibility requires protocol, permissions, catalog, model evidence, and runtime validation. A running local process does not prove a local model backend. Unknown model identity or an ambiguous invocation leads to manual reconciliation. See the [runtime guide](foundation/capabilities/ai-runtime-adapters/AI_RUNTIME_ADAPTERS.md).

## Reading paths

| Goal | Start here | Then deepen |
| --- | --- | --- |
| Learn and try the framework | [User guide](Documentation/Guides/USER_GUIDE.md) | [Architecture](Documentation/Architecture/OVERVIEW.md), [transfer overview](foundation/README.md) |
| Integrate or upgrade a project | [Transfer protocol](foundation/AI_TRANSFER.md) | [Semantic integration](Documentation/Standards/SEMANTIC_INTEGRATION_POLICY.md), [upgrade applicability](Documentation/Standards/UPGRADE_APPLICABILITY_POLICY.md) |
| Understand normative behavior | [Short transferred ruleset](foundation/FOUNDATION_RULESET.template.md) | [Foundation reference](Documentation/Standards/FOUNDATION_REFERENCE.md), relevant linked standards |
| Configure execution | [Runtime adapters](foundation/capabilities/ai-runtime-adapters/AI_RUNTIME_ADAPTERS.md) | [Router](foundation/capabilities/model-router/MODEL_ROUTER.md), [orchestrator](foundation/capabilities/ai-orchestrator/AI_ORCHESTRATOR.md) |
| Contribute to Foundation | [Repository contract](AGENTS.md) | [Repository map](.ai/repo_map.yaml), [decisions](Documentation/Architecture/DECISIONS.md), [generated backlog](.ai/BACKLOG.md) |
| Inspect release or validation evidence | [Changelog](CHANGELOG.md), [current status](.ai/PROJECT_STATUS.md) | [Handover](.ai/HANDOVER.md), [known limitations](Documentation/Quality/KNOWN_LIMITATIONS.md) |

README, the user guide, and architecture are explanations. Normative rules remain in the linked authoritative contracts. Dated quality reports and older status sections describe historical evidence, not current compatibility guarantees. [Offline package instructions](Documentation/Quality/PACKAGED_RELEASE_ARTIFACT_EVALUATION.md) describe delivery from an exact clean checkout.

## Source completion checks

Run these from this Foundation repository; the feature review uses the declared integration base:

```text
python tools/transfer_manifest_guard.py
python tools/refresh_manifest_hashes.py --check
python tools/feature_catalog_guard.py --base origin/main
python foundation/capabilities/artifact-registry-github/registry_semantic.py validate --registry .ai/identity/registry.json
python foundation/capabilities/artifact-registry-github/registry_semantic.py backlog --registry .ai/identity/registry.json --output .ai/BACKLOG.md --check
python tools/foundation_validator.py --profile full
python -m unittest discover -s tests -v
```

The [canonical validation map](.ai/repo_map.yaml) and [validation policy](.ai/VALIDATION_POLICY.md) govern completion, including relevant installation/capability checks and successful exact PR-head CI. CI also runs Windows/macOS contracts and registry semantic integrity. An installed target check establishes `FOUNDATION_INTEGRITY` only; its own `PROJECT_SEMANTIC` and `RUNTIME_EMPIRICAL` checks remain required for their respective claims.

## License

The Foundation project is [MIT-licensed](LICENSE). Its namespaced attribution notice applies to transferred Foundation material; the target repository chooses and retains its own license.
