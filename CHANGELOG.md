# Changelog

All notable Foundation changes follow Semantic Versioning.

## [1.17.1] - 2026-09-09

### Project tooling

- evaluated and implemented a deterministic, offline-verifiable Foundation source distribution containing only the manifest, manifest-whitelisted payload, minimum installer runtime, and generated content index;
- preserved exact package source provenance after extraction while keeping semantic integration and opt-in capability selection authoritative.

### Compatibility

- moved source and transferable GitHub workflows to `actions/checkout@v7` and `actions/setup-python@v7`, removing the deprecated Node-20 action-runtime dependency while preserving Python 3.12 and existing permissions/check semantics.

## [1.17.0] - 2026-09-09

### Added

- optional `foundation-ai-orchestration/v1` end-to-end planning and execution facade over live isolated catalogs, router v2, content-handle runtime invocation, deterministic validation, and bounded fallbacks;
- external `foundation-model-runtime-evidence/v1` profiles for source-backed, expiring quality, price, context, capability, resource, latency, and exact requested/actual alias evidence;
- shell-free refresh-on-plan evidence sources with narrow environment allowlists, last-known-good reuse, bounded output/time, and a minimum 24-hour interval for successful and failed attempts;
- an unconfigured-safe stdio MCP surface for status, plan, execute, and evidence refresh.

### Safety and compatibility

- live model discovery remains availability evidence only and never invents quality, price, capabilities, context, resource use, or aliases;
- model identifier differences stop for manual verification unless fresh provider documentation or signed metadata attests the exact pair;
- `LOCAL` still means deterministic work without a generative model; router v1 remains unchanged; default Foundation transfer remains rules-only with no runtime prerequisite.

## [1.16.0] - 2026-09-08

### Added

- external `foundation-ai-runtime-configuration/v1` named connections with hostname/IP/port endpoints, execution boundaries, credential references, data/remote-model authority, content roots, timeouts, and router/manual/pinned selection;
- an optional question-and-answer setup assistant with bounded loopback detection, editable proposals, connection tests, atomic save, verify, and exact rollback;
- an unconfigured-safe stdio MCP bridge for isolated runtime status, discovery, probe, catalog, and content-handle invocation;
- provider-neutral `foundation-client-model-routing-capability/v1` descriptors and a read-only native VS Code role/subagent plan bound to fresh client evidence and model inventory.

### Changed

- Ollama-local, Ollama-cloud, and OpenAI-compatible connections are configured independently; loopback/product identity does not establish host trust, non-loopback discovery is never contacted implicitly, and one invalid connection does not hide healthy entries;
- runtime invocation records requested and response-reported actual models separately and requires explicit remote authority for cloud-tagged Ollama models;
- client integration now prefers evidenced native role/agent/subagent/invocation surfaces before MCP, CLI, launcher, or expiring manual handoff, while product keys and precedence remain adapter data rather than universal policy.

### Migration

No runtime, model, provider, MCP host, Python interpreter, network, or credential is required for Foundation integrity. Select the optional `ai-runtime-adapters` and `ai-client-integration` references only when useful, keep runtime configuration and content handles outside Git, and apply client changes only through the authorized detect/plan/apply/verify/rollback lifecycle.

## [1.15.0] - 2026-09-07

### Added

- portable SHA-256 provenance on every manifest transfer row and a core `foundation-installation-provenance/v1` schema;
- atomic installed receipts containing exact ruleset/manifest identity, selected modules, and source/installed hashes without payloads, secrets, or host paths;
- precise drift classifications for current baseline, intentional override, previous Foundation version, and unknown drift;
- deterministic hash refresh/check tooling and regression coverage for tampering, stale receipts, semantic overrides, previous versions, and LF/CRLF portability.

### Changed

- clean installer applications now write an idempotent receipt; completed direct semantic transfers can record explicitly reasoned overrides without recopying files;
- target validation retains the legacy broad drift warning for compatibility while adding exact provenance classifications;
- transfer instructions require source-hash verification and a receipt after installation or semantic merge.

### Validation

- `WI-0001` closes only after the documented fresh-agent transfer and continuation procedure succeeds on a disposable synthetic repository; `WI-0002` closes only after deterministic local and required PR checks pass.

## [1.14.0] - 2026-09-07

### Added

- optional `ai-client-integration` reference capability with semantic `detect`, `plan`, `apply`, `verify`, and exact `rollback` for Codex, Visual Studio, GitHub Copilot, and generic client paths;
- portable client-plan, manual-handoff, model-dispatch-receipt, and adapter-synthesis-report schemas;
- an expiring `MANUAL_DISPATCH_REQUIRED` fallback that stores prompt content only in an external handle and may suggest a concrete model only from fresh eligible runtime evidence;
- governed local adapter materialization with explicit synthesis authority, reviewed source hashes, least-privilege configuration, quarantine, and full JSONL protocol conformance.

### Changed

- a requested model, accepted parameter, advertised model, or created subagent no longer counts as proof of execution; only matching host execution/response metadata produces `ATTESTED`, otherwise status is `REQUESTED_NOT_ATTESTED`;
- graceful degradation now includes a truthful manual model-selection step before portable tier-only guidance;
- client configuration and capability-gap handling preserve separate configuration/repository/push/PR/publication authorities and keep backups, prompts, receipts, plans, and synthesis state outside version control.

### Migration

Core policy and schemas remain usable without Python, MCP, a model router, any AI runtime, network, or client integration. Select `ai-client-integration` only when its optional reference is useful. Existing client settings are semantically merged, never replaced wholesale; automatic or manual model selection does not grant data-transfer, spend, write, push, PR, or publication authority.

## [1.13.0] - 2026-09-07

### Added

- optional `ai-provisioning` reference capability with isolated `doctor` and `inventory`, expiring content-addressed `plan-provision`, exact-plan-approved `provision`, repeatable `verify`, and per-source cost-evidence refresh;
- portable runtime-inventory, host-provision-request, exact provision-approval, and provision-report schemas plus a complete manual workflow for environments without Python;
- regressions for discovery outside `PATH`, partial runtime failure, hard resource/network limits, approval binding, verified resume, terminal hash failure, non-idempotent ambiguity, external state, and successful/failed refresh throttling.

### Changed

- provision actions may carry reference-executor metadata for exact target, license source, shell-free install/verify argument arrays, environment allowlisting, idempotency, and required offline installation;
- failed cost-source attempts are throttled as strictly as successful refreshes, while unexpired last-known-good evidence remains locally usable and unrelated sources remain isolated;
- host preparation treats discovery as evidence only, never as trust or authority, and requires a changed newly approved plan after failure or ambiguous non-idempotent execution.

### Migration

Core rules and schemas remain runtime-neutral and usable without Python, models, Ollama, LM Studio, MCP, providers, or network access. Select `ai-provisioning` only when its optional reference is useful. Keep definitions, inventories, plans, approvals, targets, downloads, checkpoints, credentials, and cost evidence outside Git. Installation grants no download, network, credential, spend, install, repository, push, pull-request, or publication authority.

## [1.12.0] - 2026-09-07

### Added

- optional `ai-executor` reference capability for exact-plan revalidation, shell-free adapter dispatch, bounded alternatives, plan-scoped cancellation, and resumable content-free checkpoints outside version control;
- `foundation-ai-executor-checkpoint/v1` and `foundation-ai-approval/v1` schemas for integrity-checked runtime state and exact-plan grouped risk approval receipts;
- deterministic regressions for completed-plan resume, fallback isolation, approval scope/authority, ambiguous external outcomes, idempotent replay, cancellation, output hashing, measured overruns, external state location, and independent validation evidence.

### Changed

- `CapabilityDescriptor.execution` optionally records idempotency/resume semantics while omitted fields preserve router/planner v1 consumers; `WorkRequest.limits.max_attempts` optionally bounds all attempts;
- execution accounts actual spend and cumulative resources even for attempts that later fail, treats RAM/VRAM as peak limits, verifies output-handle hashes, and requires passing evidence for every validation scope;
- the AI work policy now defines crash ambiguity, exact approval binding, cooperative cancellation, bounded timeouts, and the limit of exactly-once claims.

### Migration

The rules and schemas remain usable without Python or any executable component. Select `ai-executor` only when an optional Python executor is wanted and configure adapters, handles, approvals, credentials, and state outside the repository. A crash during a non-idempotent external effect requires manual reconciliation; installation grants no permission to invoke, transfer data, spend, publish, push, or create a pull request.

## [1.11.0] - 2026-09-07

### Added

- compatible `foundation-model-router/v2` request/decision/provider-fragment contracts with explicit execution boundaries, data classes, health/quality/resource provenance, hard latency/resource limits, and per-provider last-known-good state;
- language-neutral `foundation-ai-adapter-jsonl/v1` plus optional Ollama-local/cloud, OpenAI-compatible HTTP, and shell-free command/stdio Python reference adapters;
- `foundation-resource-cost-evidence/v1` for locally reusable, expiring and hashed provider/energy/hardware/resource price evidence with a maximum automated source-refresh frequency of once per 24 hours;
- golden router-v1 compatibility, adapter protocol/security, provider-isolation, resource-provenance, cost/pressure, latency, and stale-evidence regressions.

### Changed

- fallback routing now exhaustively optimizes the complete bounded attempt chain, reserves expected output in context limits, applies a documented material-benefit floor, and fails truthfully when the complete search exceeds its safety bound;
- bounded model evaluation now declares task sets, sample counts, stopping rules and spend ceilings, reserves candidate/incumbent arms separately, reconciles actual arm spend, and counts only completely settled pairs as graduation evidence;
- measured/configured per-attempt resource money enters total expected cost, while resource pressure remains a non-monetary tie-breaker when no defensible conversion exists;
- provider catalog failures and expiry are isolated; Ollama cloud tags are always remote, and loopback/product identity never proves a trusted host boundary.

### Migration

Router-v1 requests and decisions remain valid. New orchestrators may select router v2 and the separate `ai-runtime-adapters` capability. Keep fragments, endpoint configuration, resource-cost evidence, payload handles, credentials, and adapter state outside Git. Refresh one cost source no more than once per day, normally less often according to its validity, and never treat AI-assisted research as verified monetary evidence without source validation and project configuration.

## [1.10.0] - 2026-09-07

### Added

- runtime-neutral `foundation-ai-work/v1` contracts for work requests, capability descriptors, execution plans/reports, validation evidence, gap reports, and bounded provisioning plans;
- authoritative orchestration policy covering payload/control-plane separation, capability health and boundary evidence, authority intersection, risk-gated validation, isolated failure, external runtime state, and truthful manual/unavailable/blocked degradation;
- an opt-in dependency-free `ai-work` reference planner that filters hard constraints, prefers an adequate deterministic capability, emits grouped approval points, and never invokes or provisions a runtime;
- deterministic tests for missing runtimes, isolated failures, privacy and authority denial, resource/cost uncertainty, validation DAGs, grouped risk gates, adapter-synthesis authorization, content minimization, and CLI failure behavior.

### Changed

- the semantic feature catalog and transfer metadata now expose general AI-assisted development, research, documentation, data, media, and project-defined work independently of any model, provider, transport, IDE, or implementation language;
- Foundation rules remain valid when every optional component is absent, while selected projects may use the reference planner without granting it execution, network, repository, publication, or spend authority.

### Migration

Existing targets may adopt the core policy and schemas without installing a runtime. Select the optional `ai-work` capability only when the Python reference planner is useful. Keep payloads, credentials, host paths, live catalogs, plans/reports, and runtime evidence outside Git unless an explicit target rule authorizes narrower retention. Preserve compatible target orchestration and map richer data/risk/task vocabularies semantically.

## [1.9.0] - 2026-09-07

### Added

- provider-neutral `foundation-model-router/v1` request, decision, catalog, snapshot, and provider-profile schemas;
- an opt-in, dependency-free `model-router` capability with deterministic Cost-of-Success routing, fallback planning, aggregate outcome learning, conditional cache/session affinity, bounded evaluation reservations, shell-free launch, expiring snapshots, and an outside-repository atomic runtime store;
- an Ollama Cloud provider adapter that discovers current models and official time-dependent prices at runtime, hashes normalized pricing into epochs, preserves an unexpired last-known-good catalog on refresh failure, and reads authentication only from the execution environment;
- a newline-delimited JSON-RPC stdio MCP adapter plus separate current configuration examples for Visual Studio and GitHub Copilot;
- `DEC-0019`, recording the dynamic routing authority, freshness, evaluation, storage, and graceful-degradation design.

### Changed

- model routing now applies privacy, authorization, capability, context, quality, price-freshness, and budget filters before minimizing expected cost of success rather than headline token price;
- routing decisions expire at relevant price boundaries for all eligible candidates and record auditable exclusion reasons, fallback reach probabilities, validation strategy, pricing epoch, and estimated spend/success;
- newly discovered models default to `UNASSESSED` and require project profiles or spend-bounded empirical graduation before ordinary routing;
- Foundation transfer metadata, feature applicability, installer notices, validation markers, ruleset documentation, and client guidance include the new core contracts and optional capability without hard-coded model names or prices.

### Migration

Existing target routing remains authoritative when compatible. Targets may adopt only the core schemas/policy, install the optional reference implementation, or preserve a stronger router. Installing the capability does not configure credentials or clients: runtime state must remain outside version control, remote use must be explicitly authorized per request, live catalog sync is required, and the relevant client-specific MCP example must be merged rather than copied over existing configuration.

## [1.8.0] - 2026-09-01

### Added

- transferable `RULE_CONTEXT_CACHE_POLICY.md` and a versioned `foundation-rule-context-cache/v1` record schema;
- an opt-in, dependency-free `rule-context-cache` planner with machine-readable `CACHE_HIT`, `PARTIAL_INVALIDATION`, and `CACHE_MISS` decisions plus human explain output;
- deterministic repository/worktree/scope identity, exact instruction precedence, effective discovery configuration, working-tree/Git fingerprints, dependency topology, analysis keys, and cache-record self-integrity;
- focused regression coverage for scoped instructions, dirty and untracked rules, rename/delete, repository/worktree isolation, corrupt/incomplete records, EOL/encoding/final-newline semantics, dependency changes, privacy, atomic writes, and bounded locking;
- `DEC-0018`, recording the hybrid session-analysis plus local fingerprint-record architecture.

### Changed

- native Codex instruction discovery remains mandatory at every new run/session, while later change waves may reuse an actually available session analysis after deterministic validation;
- changed non-instruction rules trigger targeted rereading and transitive dependent reanalysis; instruction, scope, source-set, topology, discovery, schema/generator, corruption, or uncertainty changes fail closed to a full rebuild;
- rule-context checks hash the actual working tree and account for `HEAD`, index, staged, unstaged, and relevant untracked state rather than trusting `HEAD` alone;
- UTF-8 LF/CRLF-only representation differences reuse the Foundation portable-content policy, while lone CR, final-newline, encoding, binary, and actual content differences remain significant;
- persistent cache records are explicitly local, non-versioned, non-authoritative, non-evidence metadata containing no rule text, semantic summaries, secrets, environment values, or absolute host paths.

### Migration

Caching is optional. Existing targets may continue full rule reads. Targets choosing it keep native instruction discovery active, install or implement the v1 planner contract, select an authorized local cache directory, perform one complete analysis for each new scope/rule version, and record only after that analysis. Never persist semantic analyses or treat a fingerprint record as authority or validation evidence.

## [1.7.0] - 2026-08-26

### Added

- transferable `REPOSITORY_CONTINUITY_POLICY.md` distinguishing `VALIDATION_FAILURE`, `INFRASTRUCTURE_UNAVAILABLE`, and `UNKNOWN` so repository availability can be preserved without treating a known red validation result as acceptable;
- an audited break-glass contract requiring PR continuity, outage evidence, locally reproducible validation, residual-risk recording, and deferred post-recovery validation;
- source-project `GITHUB_BREAK_GLASS.md` and `DEC-0017` defining a layered GitHub Ruleset architecture: unbypassable core branch safety plus strict CI gates with authorized **pull-request-only** bypass;
- `tools/github/configure_rulesets.py` for fail-safe creation/read-back of the two source Rulesets and removal of legacy classic branch protection only after replacement verification;
- autonomous Git checkout regression coverage that creates a temporary repository, enables `core.autocrlf=true`, installs Foundation, commits, forces a fresh checkout, validates EOL equivalence, detects real drift, and cleans itself up.

### Fixed

- Foundation installation planning and target drift validation no longer treat Git working-tree LF/CRLF conversion as a project override or Foundation drift;
- installer and validator now use one shared UTF-8 content-equivalence implementation, while true text changes and binary/non-UTF-8 differences remain detectable;
- repeat installation/upgrade checks on Windows no longer create spurious `MERGE_REQUIRED` work solely because `core.autocrlf` materialized CRLF files.

### Changed

- direct AI transfer explicitly treats UTF-8 LF/CRLF-only differences as equivalent and prohibits creating or changing a target `.gitattributes` merely to silence Foundation EOL-only drift;
- target projects retain ownership of their own `.gitattributes` and line-ending policy;
- required validation now has explicit availability semantics: a substantive failed check is never break-glass eligible, infrastructure-unavailable validation may follow an authorized project path, and unknown failure causes remain non-bypassable;
- GitHub projects that make external CI mandatory are advised to consider separating core safety from PR-only bypassable CI gates when repository continuity matters; Foundation does not silently create target Rulesets or bypass permissions.

### Migration

The Foundation source repository migrates from its previously verified classic branch protection to two layered branch Rulesets. Create and verify `foundation-main-core-safety` and `foundation-main-ci-gates` before removing classic protection. Core safety has no bypass; only CI gates may be bypassed by the authorized source maintainer and only through a pull request.

Existing target repositories are not automatically reconfigured. During upgrade, assess `repository-continuity-break-glass`; projects may preserve stronger/no-break-glass controls or explicitly choose their own actors, outage thresholds, and recovery evidence.

## [1.6.0] - 2026-08-25

### Added

- `foundation-artifact-registry/v2`, a central JSON registry profile that stores complete artifact records under canonical human-reference object keys;
- `CENTRAL_ARTIFACT_REGISTRY_POLICY.md` defining derived sequence allocation, cross-record integrity, object-level three-way merge, Git-merge verification, cross-PR preflight, deterministic serialization, and generated views;
- `artifact-registry-v2.schema.json` as transferable core while the v1 allocation-only registry schema remains compatible legacy support;
- optional `artifact-registry-github` capability with a reference semantic registry tool and GitHub Actions workflow template;
- deterministic checks for duplicate UIDs/aliases, prefix-kind consistency, no-reuse/removal, relation resolution, self-relations, and `parent`/`depends_on` cycles;
- early open-PR collision detection for newly introduced human references, UIDs, aliases, and concurrent artifact edits;
- verification that Git's actual line-oriented merge result parses to exactly the same JSON object as the object-level semantic merge result.

### Changed

- repository-native JSON Registration Authorities now default to the v2 central profile;
- `next_sequence` is no longer persisted in the v2 profile; the next candidate is derived from the maximum existing canonical sequence plus live reservations;
- Git-native v2 registries do not persist a mutable global `registry_revision`; Git commit/blob state is the concurrency token;
- the Foundation source project's `.ai/identity/registry.json` is migrated to v2 and now contains complete `WI-*` and `DEC-*` records;
- `.ai/BACKLOG.md` is generated from the central registry rather than maintained as an independent planning authority;
- central JSON correctness no longer depends on Git's textual merge heuristics.

### Migration

Existing `foundation-artifact-registry/v1` projects remain compatible and are not automatically migrated. When a project selects the v2 central registry, preserve canonical references and UIDs, move complete artifact records into the central `artifacts` object, remove redundant `human_ref`, `next_sequence`, and Git-redundant global revision state, and validate the migration before changing the project Registration Authority declaration.

For GitHub repositories, the optional capability may be selected to provide early cross-PR preflight and the final object-level/Git-result merge gate. Another CI platform or implementation language is compatible when it enforces the same contract.

## [1.5.0] - 2026-08-24

### Added

- a transferred semantic upgrade-applicability policy requiring complete assessment of every Foundation feature introduced or materially changed since the target's installed version;
- `foundation/feature_catalog.json` with structured feature introduction/change history, transfer-source coverage, applicability signals, questions, recommendations, and decision boundaries;
- JSON Schemas for the semantic feature catalog and upgrade-assessment output;
- deterministic `tools/upgrade_applicability.py` feature-delta computation;
- blocking `tools/feature_catalog_guard.py` coverage/change-review validation;
- negative tests for uncovered transferable sources, catalog-version drift, unknown dependencies, and material/non-material delta behavior;
- explicit persistent-identity/nomenclature signals so upgrades from pre-v1.3 versions surface `ADOPT_FORWARD` when the improved convention is relevant;
- Foundation source-project persistent identity registry and explicit `FND-*` -> `WI-*` migration mapping.

### Changed

- an older-Foundation upgrade now computes semantic feature delta before normal file/semantic merge decisions;
- every candidate feature must receive exactly one assessment classification; `RECOMMENDED`, `DECISION_REQUIRED`, and `CONFLICT` results must be surfaced explicitly;
- changed transferable Foundation sources require both a ruleset version bump and feature-catalog review in CI;
- the Foundation source project now uses registered `WI-*` work-item references and `DEC-*` decision references; historical `FND-*` identifiers remain permanent aliases rather than active planning IDs;
- direct AI transfer no longer relies on an AI spontaneously noticing newly relevant governance such as identifier nomenclature.

### Migration

Target repositories are not forced to migrate their own identifiers. During an upgrade, compute the complete feature delta from the installed version to v1.5. For `persistent-identity`, inspect existing durable identifiers: preserve equivalent/stronger conventions; recommend `ADOPT_FORWARD` when the Foundation layered model is materially better for future artifacts; use `MIGRATE_EXPLICIT` only after an explicit project migration decision.

The Foundation source repository itself deliberately selected `MIGRATE_EXPLICIT` for its old internal `FND-*` work-item family. That source-project migration is not part of the target transfer payload.

## [1.4.0] - 2026-08-24

### Added

- a language-neutral artifact Registration Authority contract for durable human/AI creation workflows;
- `DIRECT` and `DEFERRED` allocation semantics so final sequential references are never guessed by individual clients;
- machine-readable JSON Schemas for artifact records, registry state, and registration requests;
- an opt-in `artifact-registration-clients` capability containing independent Python and PowerShell reference clients;
- shared deterministic cross-language fixtures covering direct allocation, deferred creation, later registration, stale revision rejection, resolution, and UUIDv7 generation;
- capability selection in the deterministic installer and target validator.

### Changed

- humans and AI systems now explicitly use the same Registration Authority for the same identifier scope;
- Python is explicitly **not** a Foundation runtime requirement; PowerShell is a first-class supported reference client and other implementation languages remain project-selectable;
- existing Jira, GitHub Issues, Azure DevOps, database/service, project-script/module, GUI/IDE, and other compatible allocators are preserved instead of being replaced by Foundation tooling;
- Foundation core transfer now includes registration policy/schemas, while executable reference clients remain opt-in;
- CI now verifies a PowerShell runtime and runs the same contract tests against both official reference clients.

### Migration

Existing repositories do not need to install either Foundation reference client. Preserve a compatible existing Registration Authority and make it discoverable to humans and AI. If the Foundation sequential human-reference profile is adopted, establish a safe allocator before publishing those references. Use `DEFERRED` when concurrent/offline work cannot safely allocate a final sequence at creation time.

## [1.3.0] - 2026-08-24

### Added

- a transferred persistent-identity policy separating machine identity, human references, aliases/external references, relations/classification, revision identity, and locators;
- RFC 9562 UUIDv7 as the Foundation default machine UID profile, with UUIDv4 as a compatible privacy/compatibility choice;
- flat typed project-local human references and a default broad prefix registry for new/adopting projects;
- explicit `PRESERVE`, `ADOPT_FORWARD`, and `MIGRATE_EXPLICIT` adoption modes for existing repositories;
- project/repository split, merge, fork, template, external-reference, revision, security, and privacy guidance;
- a machine-readable identity contract plus deterministic Foundation validator/test coverage.

### Changed

- existing published identifiers are now explicitly protected by the Foundation identity floor: no silent reuse, renaming, or reinterpretation;
- hierarchy, status, phase, owner, location, and external-tool assignment are treated as metadata/relations rather than canonical identity in the Foundation default profile;
- direct AI transfer inventories existing identifier conventions and defaults to `PRESERVE` when no explicit adoption decision exists;
- historical identifier migration now requires a separate explicit migration decision, durable old-to-new mappings, alias retention, validation, and recovery;
- semantic integration treats established project identifier conventions as target-owned governance rather than normalizing them to Foundation syntax.

### Migration

Existing repositories do not need to rename historical task, wave, slice, ADR/decision, issue, or other project references. On Foundation v1.3 integration, preserve the current convention unless the project explicitly selects prospective adoption. Prefer `ADOPT_FORWARD` when the Foundation default offers better long-term identity without justifying retroactive churn. Use `MIGRATE_EXPLICIT` only for a deliberately planned historical migration.

## [1.2.0] - 2026-08-23

### Added

- a transferred semantic-integration policy for existing repositories;
- machine-readable compatibility classes for equivalent, stricter, selectable override, complementary, duplicate, required-conflict, target-internal-conflict, orphaned-authority, and adapter-governance cases;
- an explicit root-`AGENTS.md` discovery invariant for active target-project governance;
- interoperability contracts for richer target validation-status vocabularies and existing model-routing policies;
- narrow privacy-scanner guidance for the legally required Foundation attribution notice.

### Changed

- Foundation `REQUIRED` semantics are now explicitly a minimum protected floor; intentionally stricter target rules are compatible;
- direct AI transfer inventories existing governance, preserves project routing/validation/privacy policies, classifies overlaps, and rehomes unique adapter rules before thinning adapters;
- target repo maps are preserved and may receive only a minimal Foundation-map bridge when their own schema supports it;
- existing project rules do not need to be relabeled or rewritten into Foundation terminology when semantic mapping is sufficient.

### Migration

For an existing repository, do not treat `MERGE_REQUIRED` as a request to normalize project governance to Foundation wording. Preserve mature project rules, ensure their canonical sources remain discoverable from root `AGENTS.md`, and use the semantic compatibility classes to decide what actually changes.

## [1.1.2] - 2026-08-23

### Fixed

- clarified that the Foundation validator establishes `FOUNDATION_INTEGRITY` only and cannot prove semantic correctness of project-specific rules or local overrides;
- made preservation of target-project semantic/static/runtime validation an explicit transferred rule instead of a Foundation-internal limitation only;
- prevented a green Foundation validator from being interpreted as full project validation.

### Changed

- the transfer manifest and target `repo_map` expose `FOUNDATION_INTEGRITY`, `PROJECT_SEMANTIC`, and `RUNTIME_EMPIRICAL` as machine-readable validation scopes;
- direct AI transfer inventories and preserves existing target validation infrastructure and reports validation results by scope.

## [1.1.1] - 2026-08-23

### Fixed

- finalized historical work item `FND-006` (now alias of `WI-0006`) with a dedicated, manifest-required attribution notice for transferred Foundation material;
- preserved the complete Foundation MIT copyright and permission notice without copying or modifying the target repository's root `LICENSE`;
- added deterministic validation that blocks an installed ruleset when the required Foundation MIT notice is missing or incomplete.

## [1.1.0] - 2026-08-23

### Changed

- replaced mutation-driven confirmation gates with an authorization-envelope model;
- replaced the overly broad "real information" privacy gate with data classification, destination, and handling-boundary rules;
- made model-tier escalation depend on unresolved risk/complexity/verifiability rather than human review effort;
- made third-party/dependency review proportional to risk;
- separated the Foundation project's own state from reusable target rules.

### Added

- `foundation/manifest.json` as the machine- and AI-readable transfer whitelist;
- direct AI transfer protocol;
- namespaced target rules under `.ai/foundation/`;
- deterministic installer and target validation mode.

## [1.0.0] - 2026-08-23

### Added

- initial canonical repository contract, governance core, adapters, bootstrap, and validator baseline.
