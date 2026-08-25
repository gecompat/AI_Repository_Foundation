# Changelog

All notable Foundation changes follow Semantic Versioning.

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

Existing repositories do not need to install either Foundation reference client. Preserve a compatible existing Registration Authority and make it discoverable to humans and AI. If the Foundation sequential human-reference profile is adopted, establish a safe allocator before publishing final sequence references. Use `DEFERRED` when concurrent/offline work cannot safely allocate a final sequence at creation time.

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
