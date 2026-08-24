# Direct AI Transfer Protocol

This protocol allows an AI system with read access to this Foundation repository and write access to another repository to install and semantically integrate reusable Foundation core material and explicitly selected optional capabilities without running the local installer.

## Source of transfer truth

`foundation/manifest.json` at the **exact Foundation ref being evaluated** is the complete transfer whitelist and the ruleset-version authority. Do not infer transferable files by scanning the repository and do not infer current source capabilities from a target repository's older installed Foundation copy.

- `core` contains the reusable baseline rules, schemas, entrypoint bridge, and required provenance.
- `adapters` are selected discovery adapters.
- `capabilities` are optional implementation modules and are transferred only when explicitly selected by the user/project.
- `ruleset_version` describes the source ruleset at that Foundation ref.
- `transfer_coverage_contract` defines source-side completeness/version checks that must remain green before a Foundation change is considered transferable.

Files not listed in one of those selected manifest sections are not transferred.

A target's installed `.ai/foundation/repo_map.yaml` records the version currently installed in that target. That installed version may legitimately be older than the current Foundation source. For upgrade or capability-availability questions, compare the target's installed version with `foundation/manifest.json` from the requested/current Foundation source ref; do not treat the stale target copy as the current source manifest.

In particular, never copy the Foundation project's README, root LICENSE, changelog, `.gitignore`, project context, Foundation metadata, status, handover, backlog, roadmap, internal decisions, tests, or unlisted tool source merely because they exist here.

The target project's root license is never changed by this transfer.

## Semantic integration contract

Read `Documentation/Standards/SEMANTIC_INTEGRATION_POLICY.md` before integrating into an existing repository. The Foundation is additive: preserve mature target governance and classify overlaps instead of replacing them.

Use these semantic classes consistently: `EQUIVALENT`, `PROJECT_STRONGER`, `PROJECT_SELECTABLE_OVERRIDE`, `COMPLEMENTARY`, `DUPLICATE_GOVERNANCE`, `FOUNDATION_REQUIRED_CONFLICT`, `TARGET_INTERNAL_CONFLICT`, `ORPHANED_AUTHORITY`, and `ADAPTER_GOVERNANCE_MISPLACED`.

A project that is intentionally stricter than the Foundation is normally compatible. Foundation `REQUIRED` rules define minimum protected behavior, not a maximum level of restriction.

## Persistent identifier integration

Read `Documentation/Standards/PERSISTENT_IDENTITY_POLICY.md` whenever the target has durable planning, decision, requirement, risk, test, release, incident, operational, or similar identifiers.

Before changing identifier governance in an existing repository:

1. inventory established identifier forms and where their meaning is defined;
2. distinguish stable project references from hierarchy/position codes, external-tool IDs, locators, and informal labels;
3. preserve all published historical references;
4. assess whether the Foundation layered identity default would materially improve distributed allocation, machine resolution, cross-repository portability, or long-term stability;
5. use `PRESERVE` when no explicit adoption decision exists;
6. recommend `ADOPT_FORWARD` when the Foundation/default profile is beneficial but retroactive renaming would add risk without equivalent value;
7. use `MIGRATE_EXPLICIT` only after an explicit durable migration decision with old-to-new mappings, alias retention, impact analysis, validation, and recovery.

Foundation installation or upgrade never implies an identifier migration. Missing input means `PRESERVE`, not migration.

For a new project with no established durable convention, the Foundation default profile applies unless the project selects another compatible profile: RFC 9562 UUID machine identity, flat typed project-local human references, explicit relations/aliases, and separate revision identity.

## Artifact Registration Authority

Read `Documentation/Standards/ARTIFACT_REGISTRATION_POLICY.md` before creating or changing the mechanism that allocates final human references.

For every relevant identifier scope:

1. discover the existing Registration Authority, if any: issue tracker, service, database sequence, registry, PowerShell module, Python tool, application, or other project allocator;
2. preserve a compatible existing authority rather than installing Foundation tooling over it;
3. ensure humans and AI use the same authority for the same scope;
4. never guess the next final sequence by scanning Markdown, filenames, Git history, chat history, or model memory when an authority exists;
5. use `DIRECT` only through serialized or equivalently unique allocation;
6. use `DEFERRED` for concurrent/offline creation when final sequence allocation cannot safely occur yet; the machine UID is final immediately and the human reference remains unallocated until `register`;
7. record the project-selected authority and allocation mode in project-owned governance/configuration when that choice is durable.

Python is not a Foundation requirement. PowerShell is a first-class supported reference client. The same applies to any other project-selected implementation language that preserves the contract.

## Optional artifact-registration reference clients

The manifest capability `artifact-registration-clients` contains both official reference clients:

- Python: `.ai/foundation/reference_clients/artifact_reference.py`
- PowerShell: `.ai/foundation/reference_clients/ArtifactReference.ps1`

Select this capability only when the target project wants Foundation reference tooling. Do not install it merely because the core registration policy is transferred.

Both clients implement the same language-neutral schemas and contract fixtures. A target may use neither, one operationally, or both; the selected project Registration Authority remains authoritative regardless of implementation language.

## Project-governance discovery

After integration, root `AGENTS.md` must provide a reliable discovery path to both the Foundation baseline and active project-specific governance.

For an existing repository:

1. inventory active project governance before modifying `AGENTS.md`: root/scoped `AGENTS.md`, `.ai/`, project metadata/rule directories, documentation standards, decision/validation indexes, repo maps, tool adapters containing substantive instructions, identifier/naming conventions, and Registration Authority configuration;
2. preserve any existing project router or reading order that is already useful;
3. merge only the marked Foundation block into root `AGENTS.md`;
4. outside the managed Foundation block, keep or add a concise project-owned discovery section that points to canonical project governance entrypoints when they are not otherwise discoverable;
5. do not duplicate project rule text in root `AGENTS.md` merely for discoverability;
6. classify active but unreachable governance as `ORPHANED_AUTHORITY` and fix discovery before completion.

If a project has a machine-readable repo map, preserve it. Add a minimal reference to `.ai/foundation/repo_map.yaml` only if the target schema safely supports the extension; otherwise do not rewrite the map.

## Required attribution

The transferred Foundation material originates from an MIT-licensed source. The manifest includes one mandatory attribution entry: `.ai/foundation/AI_REPOSITORY_FOUNDATION_NOTICE.md`.

- Transfer that notice together with the core material.
- Preserve the complete MIT copyright and permission notice contained in it.
- Selected optional Foundation capability files remain covered by the same Foundation source provenance.
- Do not move the Foundation license into, replace, or rewrite the target repository's root `LICENSE`.
- The notice applies only to transferred Foundation material; independently created target-project content remains governed by the target project's own licensing decisions.
- If an existing Foundation notice differs, treat it as `MERGE_REQUIRED`. A semantic merge may add target-specific third-party information, but it must retain the complete Foundation MIT notice.
- If a stricter target privacy scanner rejects the legally required notice, use the narrowest path-scoped exception for the notice; do not weaken the scanner globally or alter the notice.

## Adapter migration without rule loss

Before reducing an existing Copilot/Claude/Gemini/other adapter to a thin discovery bridge, inspect it for unique substantive project rules. Rehome those rules to a canonical project-governance source and preserve discovery first. If a safe destination cannot be determined, leave the existing rule in place and report `ADAPTER_GOVERNANCE_MISPLACED`; never delete governance merely to make an adapter look Foundation-compliant.

## Existing model-routing policy

Do not replace a richer target model/cost policy with the four Foundation tier names. Preserve the project policy and map overlapping categories semantically to `LOCAL`, `ECONOMICAL`, `BALANCED`, and `FRONTIER` when the mapping is needed for portability. Concrete model/provider choices remain target/runtime facts.

## Validation preservation contract

Foundation installation must preserve the target repository's existing validation system. The Foundation validator covers only `FOUNDATION_INTEGRITY`: installed Foundation structure, provenance, selected adapters/capabilities, deterministic Foundation contracts, and detectable drift.

It does not establish `PROJECT_SEMANTIC` correctness for project-specific rules, local overrides, identifier mappings, Registration Authority selection, architecture, domain behavior, or documentation contracts, and it does not establish `RUNTIME_EMPIRICAL` correctness for tests, builds, integrations, actual concurrency control, issue-tracker/service behavior, migration execution, or manual procedures.

Do not remove, disable, weaken, or replace existing project validators, static documentation contracts, tests, reviews, or manual validation merely because Foundation validation exists. A local Foundation override may be reported as drift, but its semantic acceptability remains a target-project responsibility. Existing project validation statuses may be richer than the Foundation reserved meanings and should be preserved when compatible.

## Procedure

1. Resolve the exact Foundation source ref and read its `foundation/manifest.json`. Treat its `ruleset_version` and `core`/`adapters`/`capabilities` sections as source truth.
2. If upgrading an existing target, read its installed `.ai/foundation/repo_map.yaml` and distinguish the installed target version from the source manifest version.
3. Read the semantic integration policy, the persistent identity policy when durable identifiers exist, and the artifact registration policy when allocation/creation is in scope.
4. Inspect the target repository's current branch/ref, root/scoped instructions, active project governance, repo maps, adapter contents, identifier conventions, Registration Authority, model-routing policy, privacy/license constraints, and validation infrastructure.
5. Select `core`, requested adapters, and only explicitly requested/project-selected optional capabilities. Manifest defaults are recommendations where defined, not authority to replace target tooling.
6. Build the deterministic file plan (`CREATE`, `UNCHANGED`, `MERGE_REQUIRED`, `CONFLICT`) and separately classify meaningful rule overlaps with the semantic compatibility classes.
7. Preserve `EQUIVALENT`, `PROJECT_STRONGER`, `PROJECT_SELECTABLE_OVERRIDE`, and `COMPLEMENTARY` project behavior. Deduplicate `DUPLICATE_GOVERNANCE` without losing substance. Resolve `FOUNDATION_REQUIRED_CONFLICT`; report `TARGET_INTERNAL_CONFLICT` separately.
8. For identifier governance, select or preserve the adoption mode. Existing convention plus no explicit decision means `PRESERVE`; a prospective change is `ADOPT_FORWARD`; historical renaming requires explicitly authorized `MIGRATE_EXPLICIT`.
9. For artifact creation, preserve or establish one Registration Authority per overlapping scope. Do not let humans, AI, Python, PowerShell, or another client allocate independently of it.
10. Never replace a differing existing file wholesale. For `AGENTS.md`, preserve all project-specific content and merge only the marked Foundation block, then ensure the active project governance remains discoverable from the root instruction tree.
11. For existing adapter files, preserve unique rules before converting them to discovery-only form. Claude/Gemini/other adapters are optional unless the target actually selects them.
12. Files under target `.ai/foundation/` are Foundation baseline rule/provenance/schema or selected capability copies. If one already differs, treat it as local override/drift and review the semantic difference; do not overwrite silently.
13. Preserve the target README, root license, domain documentation, project context/state, backlog, decisions, implementation, project repo map, established identifier history, project allocator, and project-validation infrastructure unless the user's separate task explicitly changes them.
14. Run/perform `FOUNDATION_INTEGRITY` validation and verify the Foundation bridge, attribution, validation/integration/identity/registration contracts, selected adapters, and selected capabilities.
15. Determine which target `PROJECT_SEMANTIC` and `RUNTIME_EMPIRICAL` checks are relevant. For registration this may include uniqueness, registry revision, locking, DB constraints, issue-tracker/service integration, deferred registration, recovery, and cross-client behavior.
16. Report source Foundation ref/version, target installed Foundation version, file plan, selected capabilities, semantic classifications, identifier adoption mode, Registration Authority/allocation mode, discovery fixes, adapter-rule moves, model-routing mapping if any, privacy/provenance exception if any, unresolved conflicts, and validation results by scope.

## Authorization

The user's instruction to apply the Foundation to a target repository authorizes the ordinary file creation and compatible semantic merges described above. It does not authorize a historical identifier migration unless that migration is explicitly selected, and it does not authorize replacement of an established project Registration Authority merely because optional Foundation clients exist. Do not ask for repeated confirmation for each file. Stop only for a real unresolved semantic conflict, unresolved data-handling boundary, unexpected target/scope, destructive identifier migration without explicit authority, or another explicit gate.
