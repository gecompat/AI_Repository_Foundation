# Project Status

Status: GENERATED/EVIDENCE
Last updated: 2026-08-26
Foundation version: 1.7.0

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

- WI-0015 established the previously verified classic branch protection with pull requests, strict `validate` and `registry-integrity`, up-to-date validation, linear history, no bypass, no force push, and no deletion;
- GitHub API read-back plus manual settings review on 2026-08-25 satisfied WI-0015;
- WI-0017 subsequently migrated the same core protections and CI gates to two layered Rulesets so only CI-gate unavailability has a controlled PR-only bypass path.

## v1.7.0 — WI-0016

- installation planning and target drift validation share `tools/content_equivalence.py`;
- UTF-8 LF and CRLF-only working-tree representations are treated as equivalent;
- lone CR, final-newline changes, true content changes, non-UTF-8 data, and binary differences remain significant;
- direct AI transfer does not create/change target `.gitattributes` merely to silence EOL-only comparison;
- `tests/test_eol_portability.py` creates a temporary Git repository with `core.autocrlf=true`, installs/commits Foundation, forces a fresh checkout, re-plans and validates without false drift, then introduces true drift and verifies detection;
- the first regression implementation exposed a real test-fixture defect; this was correctly treated as `VALIDATION_FAILURE`, not as an outage/bypass candidate, and the fixture was corrected to force a fresh checkout of the tracked Foundation directory;
- corrected focused EOL/Ruleset tests, all deterministic Foundation gates, and the complete 72-test suite succeeded locally on 2026-08-26;
- PR #14 head `fdd67225edaccb912a96f7e2fe1286d0749975c6` passed Foundation CI run `33002938158` and Foundation Artifact Registry run `33002938204`;
- WI-0016 is `done`.

## v1.7.0 — WI-0017 / DEC-0017

- new transferable `REPOSITORY_CONTINUITY_POLICY.md` protects repository availability without weakening validation truth;
- required-check blocking is classified as `VALIDATION_FAILURE`, `INFRASTRUCTURE_UNAVAILABLE`, or `UNKNOWN`;
- break-glass is prohibited for `VALIDATION_FAILURE` and `UNKNOWN` and may be project-authorized only for `INFRASTRUCTURE_UNAVAILABLE`;
- break-glass preserves a PR/audit path, local/manual evidence where reproducible, residual-risk recording, and mandatory post-recovery validation;
- Foundation source GitHub architecture is now active as layered Rulesets:
  - `foundation-main-core-safety` (ID `21588442`): no bypass, PR required, linear history, no force push, no deletion;
  - `foundation-main-ci-gates` (ID `21588444`): strict `validate` and `registry-integrity`, only authorized user `48807214` with `pull_request` bypass;
- `tools/github/configure_rulesets.py` creates/verifies both Rulesets and removes legacy classic protection only after replacement verification;
- `Documentation/Quality/GITHUB_BREAK_GLASS.md` defines exact source procedure and prohibited uses;
- authenticated GitHub read-back on 2026-08-26 verified both exact active Rulesets, their `refs/heads/main` condition, bypass state, required checks, strict policy, and effective combined branch rules;
- classic branch protection was removed only after replacement verification and its endpoint then returned HTTP 404 while `main` remained protected by the Rulesets;
- target projects receive the continuity recommendation but Foundation does not silently create Rulesets/bypass permissions;
- WI-0017 is `done`; DEC-0017 remains `Accepted`.

## Validation evidence

- v1.2.0 semantic integration: Foundation CI run `32646967820`, success.
- v1.3.0 persistent identity: Foundation CI run `32708542537`, success.
- v1.4.0 artifact registration: Foundation CI runs `32711801576` and `32711959226`, success.
- transfer completeness/version guard: Foundation CI runs `32716654407` and `32716818991`, success.
- v1.5 semantic upgrade applicability: Foundation CI runs `32733817943` and `32735966279`, success; merged as `400c175dac222af0c4eaee159caa955e67bbdbb7`.
- v1.6 central registry final: Foundation CI `32837891739`, Foundation Artifact Registry `32837891764`, success; merged as `9176ecaea7c972d7f5ec48c66ed19caa0ca68d8c`.
- classic branch protection verification 2026-08-25: GitHub reports `main` protected with `registry-integrity` and `validate` required for `everyone`; saved repository settings confirm the remaining required controls.
- PR #14 prior head: registry-integrity succeeded; Foundation CI reached the EOL regression and found a project-owned fixture failure. This evidence is intentionally recorded as validation failure, not infrastructure unavailability.
- v1.7.0 implementation head `fdd67225edaccb912a96f7e2fe1286d0749975c6`: Foundation CI `33002938158` and Foundation Artifact Registry `33002938204`, success.
- local completion gate on 2026-08-26: transfer manifest guard, feature catalog guard, central registry validation, backlog projection, full Foundation validator, focused EOL/Ruleset tests, and all 72 unit tests succeeded; validator reported two non-blocking pre-existing warnings.
- source Ruleset migration/read-back on 2026-08-26: active IDs `21588442` and `21588444`; only CI user `48807214` has `pull_request` bypass; classic protection absent after replacement verification.
- Fresh-agent post-transfer continuation without prior conversation context remains `pending manual validation` under `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md`.

WI-0005, WI-0008, WI-0009, WI-0010, WI-0011, WI-0012, WI-0013, WI-0014, WI-0015, WI-0016, and WI-0017 are complete. WI-0001 remains in progress only for the separate fresh-agent continuation criterion.
