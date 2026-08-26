# Project Status

Status: GENERATED/EVIDENCE
Last updated: 2026-08-26
Foundation version: 1.7.0 candidate

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

## v1.6 — WI-0014

- `foundation-artifact-registry/v2` central JSON profile stores complete artifact records in one canonical registry;
- canonical human references are `artifacts` object keys and are not duplicated inside records;
- `next_sequence` is not persisted; next references derive from `MAX(existing canonical sequence)+1`;
- Git commit/blob state is the Git-native concurrency token;
- object-level three-way merge, early cross-PR identity preflight, semantic integrity, and actual Git-merge equivalence are enforced by the optional GitHub capability;
- `.ai/identity/registry.json` is the Foundation source project's canonical v2 planning state and `.ai/BACKLOG.md` is its generated projection;
- `DEC-0015` records the durable central-registry/object-level-merge decision;
- final head `ac7c5011c415f6cf468d980882f45f8cd11b63b8` passed Foundation CI `32837891739` and Foundation Artifact Registry `32837891764` and was squash-merged by PR #11 as `9176ecaea7c972d7f5ec48c66ed19caa0ca68d8c`.

## GitHub merge protection — WI-0015 / DEC-0016

- Foundation source `main` currently has the previously verified classic branch protection enabled;
- pull requests, strict `validate` and `registry-integrity`, up-to-date validation, linear history, no bypass, no force push, and no deletion are enforced;
- GitHub API read-back plus manual settings review on 2026-08-25 satisfied WI-0015;
- this classic configuration remains active until the fail-safe Ruleset migration under WI-0017 is verified.

## v1.7.0 candidate — WI-0016

- installation planning and target drift validation share `tools/content_equivalence.py`;
- UTF-8 LF and CRLF-only working-tree representations are treated as equivalent;
- lone CR, final-newline changes, true content changes, non-UTF-8 data, and binary differences remain significant;
- direct AI transfer does not create/change target `.gitattributes` merely to silence EOL-only comparison;
- `tests/test_eol_portability.py` creates a temporary Git repository with `core.autocrlf=true`, installs/commits Foundation, forces a fresh checkout, re-plans and validates without false drift, then introduces true drift and verifies detection;
- the first regression implementation exposed a real test-fixture defect; this was correctly treated as `VALIDATION_FAILURE`, not as an outage/bypass candidate, and the fixture was corrected to force a fresh checkout of the tracked Foundation directory;
- WI-0016 remains `in_progress` until the corrected autonomous regression and full deterministic suite succeed.

## v1.7.0 candidate — WI-0017 / DEC-0017

- new transferable `REPOSITORY_CONTINUITY_POLICY.md` protects repository availability without weakening validation truth;
- required-check blocking is classified as `VALIDATION_FAILURE`, `INFRASTRUCTURE_UNAVAILABLE`, or `UNKNOWN`;
- break-glass is prohibited for `VALIDATION_FAILURE` and `UNKNOWN` and may be project-authorized only for `INFRASTRUCTURE_UNAVAILABLE`;
- break-glass preserves a PR/audit path, local/manual evidence where reproducible, residual-risk recording, and mandatory post-recovery validation;
- Foundation source target GitHub architecture is layered Rulesets:
  - `foundation-main-core-safety`: no bypass, PR required, linear history, no force push, no deletion;
  - `foundation-main-ci-gates`: strict `validate` and `registry-integrity`, authorized source-maintainer bypass **for pull requests only**;
- `tools/github/configure_rulesets.py` creates/verifies both Rulesets and removes legacy classic protection only after replacement verification;
- `Documentation/Quality/GITHUB_BREAK_GLASS.md` defines exact source procedure and prohibited uses;
- target projects receive the continuity recommendation but Foundation does not silently create Rulesets/bypass permissions;
- WI-0017 is `blocked` until GitHub repository administration is migrated and connector/API read-back confirms the two active Rulesets.

## Validation evidence

- v1.2.0 semantic integration: Foundation CI run `32646967820`, success.
- v1.3.0 persistent identity: Foundation CI run `32708542537`, success.
- v1.4.0 artifact registration: Foundation CI runs `32711801576` and `32711959226`, success.
- transfer completeness/version guard: Foundation CI runs `32716654407` and `32716818991`, success.
- v1.5 semantic upgrade applicability: Foundation CI runs `32733817943` and `32735966279`, success; merged as `400c175dac222af0c4eaee159caa955e67bbdbb7`.
- v1.6 central registry final: Foundation CI `32837891739`, Foundation Artifact Registry `32837891764`, success; merged as `9176ecaea7c972d7f5ec48c66ed19caa0ca68d8c`.
- classic branch protection verification 2026-08-25: GitHub reports `main` protected with `registry-integrity` and `validate` required for `everyone`; saved repository settings confirm the remaining required controls.
- PR #14 prior head: registry-integrity succeeded; Foundation CI reached the EOL regression and found a project-owned fixture failure. This evidence is intentionally recorded as validation failure, not infrastructure unavailability.
- v1.7.0 corrected EOL/continuity implementation: pending current PR-head deterministic/CI checks and source Ruleset administration verification.
- Fresh-agent post-transfer continuation without prior conversation context remains `pending manual validation` under `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md`.

WI-0005, WI-0008, WI-0009, WI-0010, WI-0011, WI-0012, WI-0013, WI-0014, and WI-0015 are complete. WI-0016 is in progress pending corrected deterministic evidence. WI-0017 is blocked only on Ruleset administration/read-back after code/policy validation. WI-0001 remains in progress only for the separate fresh-agent continuation criterion.
