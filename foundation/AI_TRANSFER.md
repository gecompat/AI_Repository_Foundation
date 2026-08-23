# Direct AI Transfer Protocol

This protocol allows an AI system with read access to this Foundation repository and write access to another repository to install and semantically integrate the reusable rules without running the local installer.

## Source of transfer truth

`foundation/manifest.json` is the complete transfer whitelist. Do not infer transferable files by scanning the repository. Files not listed in `core` or a selected adapter are not transferred.

In particular, never copy the Foundation project's README, root LICENSE, changelog, `.gitignore`, project context, Foundation metadata, status, handover, backlog, roadmap, internal decisions, tests, or tool source merely because they exist here.

The target project's root license is never changed by this transfer.

## Semantic integration contract

Read `Documentation/Standards/SEMANTIC_INTEGRATION_POLICY.md` before integrating into an existing repository. The Foundation is additive: preserve mature target governance and classify overlaps instead of replacing them.

Use these semantic classes consistently: `EQUIVALENT`, `PROJECT_STRONGER`, `PROJECT_SELECTABLE_OVERRIDE`, `COMPLEMENTARY`, `DUPLICATE_GOVERNANCE`, `FOUNDATION_REQUIRED_CONFLICT`, `TARGET_INTERNAL_CONFLICT`, `ORPHANED_AUTHORITY`, and `ADAPTER_GOVERNANCE_MISPLACED`.

A project that is intentionally stricter than the Foundation is normally compatible. Foundation `REQUIRED` rules define minimum protected behavior, not a maximum level of restriction.

## Project-governance discovery

After integration, root `AGENTS.md` must provide a reliable discovery path to both the Foundation baseline and active project-specific governance.

For an existing repository:

1. inventory active project governance before modifying `AGENTS.md`: root/scoped `AGENTS.md`, `.ai/`, project metadata/rule directories, documentation standards, decision/validation indexes, repo maps, and tool adapters containing substantive instructions;
2. preserve any existing project router or reading order that is already useful;
3. merge only the marked Foundation block into root `AGENTS.md`;
4. outside the managed Foundation block, keep or add a concise project-owned discovery section that points to canonical project governance entrypoints when they are not otherwise discoverable;
5. do not duplicate project rule text in root `AGENTS.md` merely for discoverability;
6. classify active but unreachable governance as `ORPHANED_AUTHORITY` and fix discovery before completion.

If a project has a machine-readable repo map, preserve it. Add a minimal reference to `.ai/foundation/repo_map.yaml` only if the target schema safely supports the extension; otherwise do not rewrite the map.

## Required attribution

The transferred Foundation material originates from an MIT-licensed source. The manifest includes one mandatory attribution entry: `.ai/foundation/AI_REPOSITORY_FOUNDATION_NOTICE.md`.

- Transfer that notice together with the rules.
- Preserve the complete MIT copyright and permission notice contained in it.
- Do not move the Foundation license into, replace, or rewrite the target repository's root `LICENSE`.
- The notice applies only to transferred Foundation material; independently created target-project content remains governed by the target project's own licensing decisions.
- If an existing Foundation notice differs, treat it as `MERGE_REQUIRED`. A semantic merge may add target-specific third-party information, but it must retain the complete Foundation MIT notice.
- If a stricter target privacy scanner rejects the legally required notice, use the narrowest path-scoped exception for the notice; do not weaken the scanner globally or alter the notice.

## Adapter migration without rule loss

Before reducing an existing Copilot/Claude/Gemini/other adapter to a thin discovery bridge, inspect it for unique substantive project rules. Rehome those rules to a canonical project-governance source and preserve discovery first. If a safe destination cannot be determined, leave the existing rule in place and report `ADAPTER_GOVERNANCE_MISPLACED`; never delete governance merely to make an adapter look Foundation-compliant.

## Existing model-routing policy

Do not replace a richer target model/cost policy with the four Foundation tier names. Preserve the project policy and map overlapping categories semantically to `LOCAL`, `ECONOMICAL`, `BALANCED`, and `FRONTIER` when the mapping is needed for portability. Concrete model/provider choices remain target/runtime facts.

## Validation preservation contract

Foundation installation must preserve the target repository's existing validation system. The Foundation validator covers only `FOUNDATION_INTEGRITY`: installed Foundation structure, provenance, adapters, deterministic Foundation contracts, and detectable drift.

It does not establish `PROJECT_SEMANTIC` correctness for project-specific rules, local overrides, architecture, domain behavior, or documentation contracts, and it does not establish `RUNTIME_EMPIRICAL` correctness for tests, builds, integrations, runtime behavior, research/data verification, or manual procedures.

Do not remove, disable, weaken, or replace existing project validators, static documentation contracts, tests, reviews, or manual validation merely because Foundation validation exists. A local Foundation override may be reported as drift, but its semantic acceptability remains a target-project responsibility. Existing project validation statuses may be richer than the Foundation reserved meanings and should be preserved when compatible.

## Procedure

1. Read `foundation/manifest.json` and the semantic integration policy.
2. Inspect the target repository's current branch/ref, root/scoped instructions, active project governance, repo maps, adapter contents, model-routing policy, privacy/license constraints, and validation infrastructure.
3. Select `core` plus the adapters requested by the user/project. If none are specified, the manifest's `default_adapters` are recommendations, not mandatory.
4. Build the deterministic file plan (`CREATE`, `UNCHANGED`, `MERGE_REQUIRED`, `CONFLICT`) and separately classify meaningful rule overlaps with the semantic compatibility classes.
5. Preserve `EQUIVALENT`, `PROJECT_STRONGER`, `PROJECT_SELECTABLE_OVERRIDE`, and `COMPLEMENTARY` project behavior. Deduplicate `DUPLICATE_GOVERNANCE` without losing substance. Resolve `FOUNDATION_REQUIRED_CONFLICT`; report `TARGET_INTERNAL_CONFLICT` separately.
6. Never replace a differing existing file wholesale. For `AGENTS.md`, preserve all project-specific content and merge only the marked Foundation block, then ensure the active project governance remains discoverable from the root instruction tree.
7. For existing adapter files, preserve unique rules before converting them to discovery-only form. Claude/Gemini/other adapters are optional unless the target actually selects them.
8. Files under target `.ai/foundation/` are Foundation baseline rule/provenance copies. If one already differs, treat it as local override/drift and review the semantic difference; do not overwrite silently.
9. Preserve the target README, root license, domain documentation, project context/state, backlog, decisions, implementation, project repo map, and project-validation infrastructure unless the user's separate task explicitly changes them.
10. Run/perform `FOUNDATION_INTEGRITY` validation and verify the Foundation bridge, attribution, validation/integration contracts, and selected adapters.
11. Determine which target `PROJECT_SEMANTIC` and `RUNTIME_EMPIRICAL` checks are relevant to the integration changes and run/preserve them according to the target repository's own rules. Do not invent unrelated full-suite requirements.
12. Report the file plan, semantic classifications, discovery fixes, adapter-rule moves, model-routing mapping if any, privacy/provenance exception if any, unresolved conflicts, and validation results by scope.

## Authorization

The user's instruction to apply the Foundation to a target repository authorizes the ordinary file creation and compatible semantic merges described above. Do not ask for repeated confirmation for each file. Stop only for a real unresolved semantic conflict, unresolved data-handling boundary, unexpected target/scope, or another explicit gate.
