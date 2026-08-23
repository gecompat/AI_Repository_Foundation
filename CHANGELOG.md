# Changelog

All notable Foundation changes follow Semantic Versioning.

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

- finalized FND-006 with a dedicated, manifest-required attribution notice for transferred Foundation material;
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
