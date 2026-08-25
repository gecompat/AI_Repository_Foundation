# Project Status

Status: GENERATED/EVIDENCE
Last updated: 2026-08-25
Foundation version: 1.6.0

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
- `next_sequence` is not persisted; next references derive from `MAX(existing canonical sequence)+1`, with live reservations considered by the authority when applicable;
- the Git-native profile does not persist a global registry revision counter; Git commit/blob state is the concurrency token;
- `Documentation/Standards/CENTRAL_ARTIFACT_REGISTRY_POLICY.md` defines structural integrity, no-reuse, relation validation, generated views, and merge semantics;
- optional `artifact-registry-github` capability contains the object-level registry tool and GitHub Actions workflow template;
- object-level three-way merge uses `BASE`, current target `MAIN`, and PR `HEAD`; independent properties may merge while divergent same-property changes block;
- the GitHub gate separately simulates Git's textual registry merge and requires its parsed result to equal the semantic object-level result;
- early cross-PR preflight detects duplicate new canonical references, duplicate UIDs, alias collisions, and concurrent artifact edits;
- `.ai/identity/registry.json` is the Foundation source project's canonical v2 planning state;
- `.ai/BACKLOG.md` is generated from that registry and checked for drift;
- `DEC-0015` records the durable central-registry/object-level-merge decision;
- Python runtime caches under managed capability roots are explicitly excluded from transfer completeness and regression-tested;
- implementation head `1bd2a9bb0a487780e2d12401ae2747cadef3f6d3` passed Foundation CI `32837531482` and Foundation Artifact Registry `32837531385`;
- final head `ac7c5011c415f6cf468d980882f45f8cd11b63b8` passed Foundation CI `32837891739` and Foundation Artifact Registry `32837891764` and was squash-merged by PR #11 as `9176ecaea7c972d7f5ec48c66ed19caa0ca68d8c`.

## GitHub merge protection — WI-0015 / DEC-0016

- Foundation source `main` has server-side GitHub branch protection enabled;
- pull requests are required before merge and mandatory human approvals are disabled for the current single-maintainer model;
- required checks are `validate` and `registry-integrity`;
- branches must be up to date before merge;
- required-check enforcement is reported by GitHub as `everyone`;
- linear history is required;
- bypass of the protection is disabled, including administrators;
- force pushes and branch deletion are disabled;
- `Documentation/Quality/GITHUB_BRANCH_PROTECTION.md` records the required and verified source-project state;
- `tools/github/configure_branch_protection.py` can reproduce/verify the state when an Administration-write token is available;
- direct AI transfer and deterministic installation explicitly tell relevant target projects that workflow files do not make checks required and recommend GitHub protection without making it a `FOUNDATION_INTEGRITY` requirement;
- GitHub API read-back plus manual GitHub settings review on 2026-08-25 satisfy the WI-0015 acceptance criteria.

## Validation evidence

- v1.2.0 semantic integration: Foundation CI run `32646967820`, success.
- v1.3.0 persistent identity: Foundation CI run `32708542537`, success.
- v1.4.0 artifact registration: Foundation CI runs `32711801576` and `32711959226`, success.
- transfer completeness/version guard: Foundation CI runs `32716654407` and `32716818991`, success.
- v1.5 semantic upgrade applicability: Foundation CI runs `32733817943` and `32735966279`, success; merged as `400c175dac222af0c4eaee159caa955e67bbdbb7`.
- v1.6 central registry final: Foundation CI `32837891739`, Foundation Artifact Registry `32837891764`, success; merged as `9176ecaea7c972d7f5ec48c66ed19caa0ca68d8c`.
- branch protection verification 2026-08-25: GitHub reports `main` protected with `registry-integrity` and `validate` required for `everyone`; saved repository settings confirm the remaining required source controls.
- Fresh-agent post-transfer continuation without prior conversation context remains `pending manual validation` under `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md`.

WI-0005, WI-0008, WI-0009, WI-0010, WI-0011, WI-0012, WI-0013, WI-0014, and WI-0015 are complete for their deterministic/project-operation contracts. WI-0001 remains in progress only for the separate fresh-agent continuation criterion.
