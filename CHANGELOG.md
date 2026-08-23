# Changelog

All notable Foundation changes follow Semantic Versioning.

## [1.1.2] - 2026-08-23

### Fixed

- clarified that the Foundation validator establishes `FOUNDATION_INTEGRITY` only and cannot prove semantic correctness of project-specific rules or local overrides;
- made preservation of target-project semantic/static/runtime validation an explicit transferred rule instead of a Foundation-internal limitation only;
- prevented a green Foundation validator from being interpreted as full project validation.

### Changed

- the transfer manifest and target `repo_map` now expose `FOUNDATION_INTEGRITY`, `PROJECT_SEMANTIC`, and `RUNTIME_EMPIRICAL` as machine-readable validation scopes;
- direct AI transfer now inventories and preserves existing target validation infrastructure and reports validation results by scope.

## [1.1.1] - 2026-08-23

### Fixed

- finalized FND-006 with a dedicated, manifest-required attribution notice for transferred Foundation material;
- preserved the complete Foundation MIT copyright and permission notice without copying or modifying the target repository's root `LICENSE`;
- added deterministic validation that blocks an installed ruleset when the required Foundation MIT notice is missing or incomplete.

### Changed

- direct AI transfer now treats attribution validation as part of completion;
- target ruleset metadata records the attribution notice separately from governance authority.

## [1.1.0] - 2026-08-23

### Changed

- replaced mutation-driven confirmation gates with an authorization-envelope model: ordinary task-authorized operations proceed without repeated confirmation;
- replaced the overly broad "real information" privacy gate with explicit data classification, destination, and handling-boundary rules;
- made model-tier escalation depend on unresolved risk/complexity/verifiability rather than human review effort;
- made third-party/dependency review proportional to risk;
- separated the Foundation project's own state from the reusable rules transferred to target repositories.

### Added

- `foundation/manifest.json` as the sole machine- and AI-readable transfer whitelist;
- direct AI transfer protocol for applying rules to new or existing repositories without a local installer;
- namespaced target rules under `.ai/foundation/`;
- manifest-driven deterministic installer with `CREATE`, `UNCHANGED`, `MERGE_REQUIRED`, and `CONFLICT` states;
- target validation mode and deterministic installation-model unit tests;
- minimal CI for Foundation self-validation.

### Migration

Do not unpack or copy the Foundation repository wholesale. v1.1 transfers only manifest-listed rules/adapters plus the required namespaced Foundation attribution notice. Existing target README, root LICENSE, project context, decisions, backlog, status, handover, and implementation are outside the transfer set and remain untouched.

## [1.0.0] - 2026-08-23

### Added

- canonical repository contract and structured `.ai/` core;
- privacy, security, documentation, licensing, evidence, dependency, and decision policies;
- Copilot, Claude, and Gemini thin adapters;
- Foundation metadata, adapter registry, and repository map;
- local dependency-free bootstrap and validator skeletons.

### Migration

Initial baseline. Superseded for new installations by the manifest-driven v1.1 transfer model.
