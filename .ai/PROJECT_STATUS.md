# Project Status

Status: GENERATED/EVIDENCE
Last updated: 2026-08-25
Foundation version: 1.6.0 candidate

## Implemented baseline

- rules/provenance transfer manifest and direct AI transfer protocol;
- semantic integration compatibility taxonomy and root-governance discovery;
- layered validation ownership: `FOUNDATION_INTEGRITY`, `PROJECT_SEMANTIC`, `RUNTIME_EMPIRICAL`;
- persistent identity with `PRESERVE`, `ADOPT_FORWARD`, and explicitly authorized `MIGRATE_EXPLICIT`;
- language-neutral Artifact Registration Authority with `DIRECT`/`DEFERRED` and optional reference clients;
- source-side transfer completeness/version guard and negative regression tests;
- source/installed Foundation version separation;
- complete semantic upgrade feature applicability assessment.

## v1.5 — WI-0013

- semantic `foundation/feature_catalog.json` covering reusable Foundation features from the baseline through v1.5;
- transferred `UPGRADE_APPLICABILITY_POLICY.md`, feature-catalog schema, and upgrade-assessment schema;
- deterministic upgrade-delta computation and mandatory surfacing of recommendations/decisions/conflicts;
- `DEC-0014` records the durable semantic-upgrade applicability decision;
- PR #10 final evidence head `3fec8bad5f7816b7741ef729735aeec56e492c0c` passed Foundation CI run `32735966279` and was squash-merged as `400c175dac222af0c4eaee159caa955e67bbdbb7`.

## v1.6 candidate — WI-0014

- new `foundation-artifact-registry/v2` central JSON profile stores complete artifact records in one canonical registry;
- canonical human references are `artifacts` object keys and are not duplicated inside records;
- `next_sequence` is removed; next references are derived from the maximum existing canonical sequence plus live reservations;
- the Git-native profile does not persist a global registry revision counter; Git commit/blob state is the concurrency token;
- `Documentation/Standards/CENTRAL_ARTIFACT_REGISTRY_POLICY.md` defines structural integrity, no-reuse, relation validation, generated views, and merge semantics;
- `foundation/schemas/artifact-registry-v2.schema.json` is transferable core while the v1 allocation-only schema remains compatible legacy support;
- optional `artifact-registry-github` capability contains an object-level validator/merger and GitHub Actions workflow template;
- object-level three-way merge uses `BASE`, current target `MAIN`, and PR `HEAD`; independent properties may merge, divergent changes to the same property block;
- the GitHub gate separately simulates Git's textual file merge and requires its parsed result to equal the semantic object-level result;
- early cross-PR preflight detects duplicate new canonical references, duplicate UIDs, alias collisions, and concurrent artifact edits;
- `.ai/identity/registry.json` has been migrated to v2 and is now the Foundation source project's canonical planning state;
- `.ai/BACKLOG.md` is generated from that registry and checked for drift;
- `WI-0014` and `DEC-0015` are registered under the new source-project state.

## Validation evidence

- v1.2.0 semantic integration: Foundation CI run `32646967820`, success.
- v1.3.0 persistent identity: Foundation CI run `32708542537`, success.
- v1.4.0 artifact registration: Foundation CI runs `32711801576` and `32711959226`, success.
- transfer completeness/version guard: Foundation CI runs `32716654407` and `32716818991`, success.
- v1.5 semantic upgrade applicability: Foundation CI runs `32733817943` and `32735966279`, success; merged as `400c175dac222af0c4eaee159caa955e67bbdbb7`.
- v1.6 central registry/semantic merge candidate: `not executed` until the PR-head CI gate runs.
- Fresh-agent post-transfer continuation without prior conversation context remains `pending manual validation` under `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md`.

WI-0005, WI-0008, WI-0009, WI-0010, WI-0011, WI-0012, and WI-0013 are complete for their deterministic contracts. WI-0014 is in progress. WI-0001 remains in progress only for the separate fresh-agent continuation criterion.
