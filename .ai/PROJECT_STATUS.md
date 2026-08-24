# Project Status

Status: GENERATED/EVIDENCE
Last updated: 2026-08-24
Foundation version: 1.5.0 candidate

## Implemented baseline

- rules/provenance transfer manifest and direct AI transfer protocol;
- semantic integration compatibility taxonomy and root-governance discovery;
- layered validation ownership: `FOUNDATION_INTEGRITY`, `PROJECT_SEMANTIC`, `RUNTIME_EMPIRICAL`;
- persistent identity with `PRESERVE`, `ADOPT_FORWARD`, and explicitly authorized `MIGRATE_EXPLICIT`;
- language-neutral Artifact Registration Authority with `DIRECT`/`DEFERRED` and optional Python/PowerShell reference clients;
- source-side transfer completeness/version guard and negative regression tests;
- source/installed Foundation version separation.

## v1.5 — WI-0013

- semantic `foundation/feature_catalog.json` covering reusable Foundation features from the baseline through v1.5;
- transferred `UPGRADE_APPLICABILITY_POLICY.md`, feature-catalog schema, and upgrade-assessment schema;
- deterministic upgrade-delta computation based on `introduced_in` plus `MATERIAL` change history;
- required assessment classifications `NOT_APPLICABLE`, `ALREADY_EQUIVALENT`, `PROJECT_STRONGER`, `APPLY_DEFAULT`, `RECOMMENDED`, `DECISION_REQUIRED`, `CONFLICT`;
- explicit requirement that every candidate feature is assessed exactly once and that recommendations/decisions/conflicts are surfaced;
- `persistent-identity` applicability signals include durable planning/decision/requirement/risk/test/release/incident/operational identifiers and explicitly recommend `ADOPT_FORWARD` when a compatible existing convention is materially weaker;
- `tools/upgrade_applicability.py` deterministic candidate-delta helper;
- `tools/feature_catalog_guard.py` source feature-coverage and changed-transfer-source review guard;
- CI changed-source review requires a ruleset version bump and a feature-catalog review record for every changed transferable source;
- direct AI transfer computes the semantic feature delta before normal semantic merge/adoption choices;
- `DEC-0014` records the durable semantic-upgrade applicability decision.

## Foundation source-project self-migration

- active planning references were explicitly migrated from historical aliases `FND-001`..`FND-012` to preferred `WI-0001`..`WI-0012` under `MIGRATE_EXPLICIT`;
- the completed v1.5 development is registered as `WI-0013`;
- existing decisions remain `DEC-*`; `DEC-0013` records the source-project identifier migration and `DEC-0014` records semantic upgrade applicability;
- `.ai/identity/registry.json` is the Foundation source project's Registration Authority state and contains registered UIDs through `WI-0013` and `DEC-0014`;
- `Documentation/Architecture/IDENTIFIER_MIGRATION_2026-08-24.md` preserves historical `FND-*` alias mappings;
- Foundation source-project identity state is explicitly excluded from target transfer;
- deterministic tests prevent active `FND-*` backlog identifiers from being reintroduced.

## Validation evidence

- v1.2.0 semantic integration: Foundation CI run `32646967820`, head `17662ba58a88abee8ef951d22918aa4c5543392d`, success.
- Existing-repository AI transfer: validated in five repositories; see `Documentation/Quality/EXISTING_REPOSITORY_AI_TRANSFER_EVIDENCE.md`.
- v1.3.0 persistent identity: Foundation CI run `32708542537`, head `a1f5463d5d32d0e04394303fd6f6aac8846810ce`, success.
- v1.4.0 artifact registration: Foundation CI runs `32711801576` and `32711959226`, success; PR #8 merged as `07b7405d5dda27f8d3e0a5164e5cfcbe46396e24`.
- Transfer completeness/version guard: Foundation CI runs `32716654407` and `32716818991`, success; PR #9 merged as `2c9de5d5299a0eefec59fdc6131519886dc5e195`.
- v1.5 semantic upgrade applicability plus Foundation source-project identifier migration: Foundation CI run `32733817943`, implementation head `9e91cd21e3941a77cbb2e5a3abbf501c2d6a4788`, `validated`, conclusion `success`. PowerShell runtime verification, transfer-manifest completeness/version guard, semantic feature coverage/change-review guard, Foundation validator, installation/transfer/feature-catalog/source-migration tests, and cross-language registration tests all completed successfully.
- The evidence-only final PR #10 head must still pass the same full CI gate before merge.
- Fresh-agent post-transfer continuation without prior conversation context remains `pending manual validation` under `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md`.

WI-0005, WI-0008, WI-0009, WI-0010, WI-0011, WI-0012, and WI-0013 are complete for their deterministic contracts. WI-0001 remains in progress only for the separate fresh-agent continuation criterion. PR #10 is mergeable only after the final evidence head is green.
