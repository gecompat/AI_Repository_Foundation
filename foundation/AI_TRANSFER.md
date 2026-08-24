# Direct AI Transfer Protocol

This protocol allows an AI system with read access to this Foundation repository and write access to another repository to install or upgrade reusable Foundation core material and explicitly selected optional capabilities without running the local installer.

## Source of transfer truth

`foundation/manifest.json` at the **exact Foundation ref being evaluated** is the complete transfer whitelist and ruleset-version authority. `foundation/feature_catalog.json` at that same ref is the semantic feature source for upgrades.

Do not infer current source capabilities from an older Foundation copy already installed in the target.

- `core` contains reusable baseline rules, schemas, feature catalog, entrypoint bridge, and required provenance.
- `adapters` are selected discovery adapters.
- `capabilities` are optional implementation modules and are transferred only when explicitly selected.
- `ruleset_version` describes the source ruleset at that Foundation ref.
- `transfer_coverage_contract` defines source-side transfer/version checks.
- `feature_catalog.json` records semantic features, their introduction/material-change versions, applicability evidence, and recommendation/decision semantics.

Files outside selected manifest sections are not transferred. Never copy the Foundation project's README, root LICENSE, changelog, project context, Foundation metadata/state, backlog, roadmap, internal decisions, identity registry, tests, or unlisted tool source merely because they exist.

The target project's root license is never changed by Foundation transfer.

## Source version versus installed target version

A target's installed `.ai/foundation/repo_map.yaml` records the Foundation version currently installed in that target. It may legitimately be older than the current source.

For every upgrade/capability question:

1. resolve the exact source Foundation ref;
2. read its `foundation/manifest.json` and `foundation/feature_catalog.json`;
3. read the target's installed Foundation version when present;
4. report source and installed versions separately.

Never treat the stale target copy as the current source manifest/catalog.

## Mandatory semantic upgrade assessment

If the installed target version is older than the source version, read `Documentation/Standards/UPGRADE_APPLICABILITY_POLICY.md` before deciding what to adopt.

Compute the **complete** feature delta. A feature is a candidate when it was introduced after the installed version through the source version, or when a `MATERIAL` feature change occurred in that interval.

Every candidate must receive exactly one classification:

- `NOT_APPLICABLE`
- `ALREADY_EQUIVALENT`
- `PROJECT_STRONGER`
- `APPLY_DEFAULT`
- `RECOMMENDED`
- `DECISION_REQUIRED`
- `CONFLICT`

For each candidate, inspect target evidence using the feature catalog's signals/questions and record rationale. Explicitly surface every `RECOMMENDED`, `DECISION_REQUIRED`, and `CONFLICT` result. A missing candidate is a defective upgrade assessment; silence is not equivalent to `NOT_APPLICABLE`.

In particular, if a target upgraded from a pre-1.3 Foundation version and contains durable planning/decision/requirement/risk/test/release/etc. identifiers, `persistent-identity` must be assessed. If its established convention is compatible but materially weaker, recommend `ADOPT_FORWARD` for new identifiers while preserving historical references. Do not wait for the user to mention nomenclature explicitly.

The helper `tools/upgrade_applicability.py --installed X.Y.Z --json` may compute the deterministic candidate set when the tool is available. An AI may perform the equivalent calculation directly from the catalog. Repository-specific classification remains semantic work, not a deterministic Foundation claim.

## Semantic integration contract

Read `Documentation/Standards/SEMANTIC_INTEGRATION_POLICY.md` before integrating into an existing repository. Foundation is additive: preserve mature target governance and classify overlaps instead of replacing them.

Use the semantic classes `EQUIVALENT`, `PROJECT_STRONGER`, `PROJECT_SELECTABLE_OVERRIDE`, `COMPLEMENTARY`, `DUPLICATE_GOVERNANCE`, `FOUNDATION_REQUIRED_CONFLICT`, `TARGET_INTERNAL_CONFLICT`, `ORPHANED_AUTHORITY`, and `ADAPTER_GOVERNANCE_MISPLACED`.

Feature applicability and semantic compatibility are separate layers: first ensure every newer/materially-changed feature was considered, then integrate the applicable behavior with the target's existing governance.

## Persistent identifiers

Read `PERSISTENT_IDENTITY_POLICY.md` whenever durable project identifiers exist or are introduced.

Before changing identifier governance:

1. inventory established identifiers and their authority;
2. distinguish stable references from hierarchy/position codes, tool IDs, locators, and informal labels;
3. preserve all published historical references;
4. assess the `persistent-identity` feature from the catalog;
5. use `PRESERVE` when no explicit adoption decision exists;
6. recommend `ADOPT_FORWARD` when improved future nomenclature/identity is beneficial without justifying retroactive churn;
7. use `MIGRATE_EXPLICIT` only after an explicit durable migration decision with mappings, alias retention, impact analysis, validation, and recovery.

Foundation installation/upgrade never implies historical identifier migration. Missing input means `PRESERVE`.

## Artifact Registration Authority

Read `ARTIFACT_REGISTRATION_POLICY.md` when final human references are allocated or created.

For every relevant identifier scope:

1. discover the existing Registration Authority: issue tracker, service, database sequence, registry, PowerShell module, Python tool, application, or other allocator;
2. preserve a compatible authority instead of installing Foundation tooling over it;
3. ensure humans and AI use the same authority;
4. never guess the next final sequence by scanning Markdown, filenames, Git history, chat history, or model memory;
5. use `DIRECT` only through serialized/equivalently unique allocation;
6. use `DEFERRED` when concurrent/offline creation cannot safely allocate the final sequence yet;
7. record a durable project choice when Registration Authority/allocation mode must be remembered.

Python is not a Foundation requirement. PowerShell is a first-class supported reference client; any language is compatible when it preserves the contract.

The optional manifest capability `artifact-registration-clients` installs the Python and PowerShell reference clients only when the target explicitly wants them. A compatible existing project allocator takes precedence.

## Project-governance discovery

After integration, root `AGENTS.md` must provide a reliable discovery path to Foundation baseline and active project-specific governance.

For an existing repository:

1. inventory root/scoped instructions, `.ai/`, project governance, repo maps, adapters with substantive rules, identifier conventions, Registration Authority, validation/model/privacy/license rules;
2. preserve useful existing project routing;
3. merge only the marked Foundation block into root `AGENTS.md`;
4. outside that block preserve/add concise project-owned discovery links;
5. do not duplicate rule text merely for discovery;
6. resolve `ORPHANED_AUTHORITY` before completion.

Preserve a target's machine-readable repo map. Add only a safe minimal reference to `.ai/foundation/repo_map.yaml` when the target schema supports it.

## Required attribution

Every Foundation rules transfer includes `.ai/foundation/AI_REPOSITORY_FOUNDATION_NOTICE.md` with the complete Foundation MIT notice.

- Preserve the notice with transferred core and selected capability material.
- Do not move it into or replace the target root `LICENSE`.
- The notice applies to transferred Foundation material, not independently created target content.
- A differing existing notice is `MERGE_REQUIRED`; preserve the complete Foundation notice during semantic merge.
- Use a narrow path-scoped privacy exception when a stricter scanner would otherwise reject the legally required notice; do not weaken scanners globally.

## Adapter migration

Before thinning an existing Copilot/Claude/Gemini/other adapter, inspect it for unique substantive project rules. Rehome those rules to canonical project governance and preserve discovery first. If safe rehoming cannot be determined, keep the rule and report `ADAPTER_GOVERNANCE_MISPLACED`.

## Existing model/validation policy

Do not replace richer target policies with simplified Foundation vocabulary.

- Preserve detailed model/cost policy and map overlapping semantics to `LOCAL`, `ECONOMICAL`, `BALANCED`, `FRONTIER` when useful.
- Preserve existing validation systems. Foundation validator covers only `FOUNDATION_INTEGRITY`; target `PROJECT_SEMANTIC` and `RUNTIME_EMPIRICAL` remain authoritative.
- Foundation-green does not imply target-project semantic/runtime correctness.

## Procedure

1. Resolve exact source ref; read its manifest and feature catalog.
2. Determine installed target Foundation version separately.
3. If upgrading from an older version, compute and classify the complete semantic feature delta; surface recommendations/decisions/conflicts.
4. Read semantic integration policy plus feature-specific policies required by applicable candidates.
5. Inspect target governance, identifiers, Registration Authority, adapters, repo maps, validation, model routing, privacy/license constraints.
6. Select `core`, requested adapters, and only explicitly requested/project-selected optional capabilities.
7. Build deterministic file states (`CREATE`, `UNCHANGED`, `MERGE_REQUIRED`, `CONFLICT`) and semantic overlap classifications.
8. Preserve equivalent, stronger, selectable-override, and complementary target behavior; resolve true required conflicts and target-internal conflicts separately.
9. Apply identifier adoption and Registration Authority rules without silent migration/replacement.
10. Never replace a differing existing file wholesale; preserve target README, root license, domain docs, project state/backlog/decisions, repo map, identifier history, allocator, and project validation unless separately authorized.
11. Run/perform `FOUNDATION_INTEGRITY`; determine and preserve relevant `PROJECT_SEMANTIC` and `RUNTIME_EMPIRICAL` checks.
12. Report source ref/version, installed version, complete feature assessment, selected capabilities, file plan, semantic classifications, identifier/registration choices, discovery fixes, unresolved conflicts, and validation evidence by scope.

## Authorization

The user's instruction to apply or upgrade Foundation authorizes ordinary file creation and compatible semantic merges described above. It does not authorize historical identifier migration, replacement of an established Registration Authority, or another durable project-selectable change unless explicitly selected. Do not request repeated confirmation for each file; stop only for a real unresolved semantic conflict, data-handling boundary, unexpected target/scope, destructive migration without authority, or another explicit gate.
