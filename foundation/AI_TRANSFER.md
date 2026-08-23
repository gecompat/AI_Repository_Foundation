# Direct AI Transfer Protocol

This protocol allows an AI system with read access to this Foundation repository and write access to another repository to install the reusable rules without running the local installer.

## Source of transfer truth

`foundation/manifest.json` is the complete whitelist. Do not infer transferable files by scanning the repository. Files not listed in `core` or a selected adapter are not transferred.

In particular, never copy the Foundation project's README, root LICENSE, changelog, `.gitignore`, project context, Foundation metadata, status, handover, backlog, roadmap, internal decisions, tests, or tool source merely because they exist here.

The target project's root license is never changed by this transfer.

## Required attribution

The transferred Foundation material originates from an MIT-licensed source. The manifest therefore includes one mandatory attribution entry: `.ai/foundation/AI_REPOSITORY_FOUNDATION_NOTICE.md`.

- Transfer that notice together with the rules.
- Preserve the complete MIT copyright and permission notice contained in it.
- Do not move the Foundation license into, replace, or rewrite the target repository's root `LICENSE`.
- The notice applies only to transferred Foundation material; independently created target-project content remains governed by the target project's own licensing decisions.
- If an existing Foundation notice differs, treat it as `MERGE_REQUIRED`. A semantic merge may add target-specific third-party information, but it must retain the complete Foundation MIT notice.

## Validation preservation contract

Foundation installation must preserve the target repository's existing validation system. The Foundation validator covers only `FOUNDATION_INTEGRITY`: installed Foundation structure, provenance, adapters, deterministic Foundation contracts, and detectable drift.

It does not establish `PROJECT_SEMANTIC` correctness for project-specific rules, local overrides, architecture, domain behavior, or documentation contracts, and it does not establish `RUNTIME_EMPIRICAL` correctness for tests, builds, integrations, runtime behavior, research/data verification, or manual procedures.

Do not remove, disable, weaken, or replace existing project validators, static documentation contracts, tests, reviews, or manual validation merely because Foundation validation exists. A local Foundation override may be reported as drift, but its semantic acceptability remains a target-project responsibility. Completion combines only the validation scopes relevant to the affected change; Foundation-green alone never means project-green.

## Procedure

1. Read `foundation/manifest.json`.
2. Inspect the target repository's existing root `AGENTS.md`, selected adapter files, project-specific instruction hierarchy, and existing validation infrastructure/commands/static contracts needed to avoid conflicts or accidental replacement.
3. Select `core` plus the adapters requested by the user/project. If none are specified, the manifest's `default_adapters` are recommended, not mandatory.
4. For each manifest entry compare source content with the target path:
   - target absent: `CREATE`;
   - identical: `UNCHANGED`;
   - existing project-specific file with compatible semantics: `MERGE_REQUIRED`;
   - incompatible semantics affecting REQUIRED rules or an unresolved authority conflict: `CONFLICT`.
5. Never replace a differing existing file wholesale. For `AGENTS.md`, preserve all project-specific content and merge only the marked `AI_REPOSITORY_FOUNDATION` block from `foundation/AGENTS.template.md` at an appropriate root scope. For existing adapter files, preserve existing tool-specific content and add only the discovery path back to root `AGENTS.md` when needed.
6. Files under target `.ai/foundation/` are Foundation baseline rule/provenance copies. If one already differs, treat it as a local override/drift and review the semantic difference; do not overwrite silently. The attribution notice is special: any merged version must still contain the complete MIT notice from the Foundation source.
7. Apply the smallest coherent set of changes. The target repository's README, root license, domain documentation, project state, backlog, decisions, implementation, and project-validation infrastructure remain untouched unless the user's separate task explicitly changes them.
8. Run/perform Foundation-integrity validation: selected manifest targets exist or have documented local merges/overrides, adapters lead to root `AGENTS.md`, the attribution notice preserves the complete Foundation MIT notice, the validation-scope contract is present, and no `never_transfer` project artifact was introduced.
9. Determine which existing `PROJECT_SEMANTIC` and `RUNTIME_EMPIRICAL` checks are relevant to the affected target-project contracts and preserve/run them according to the target repository's own rules. Do not invent a requirement to run unrelated full suites.
10. Report `CREATE`, `UNCHANGED`, merged/overridden files, conflicts, attribution validation, and validation results separately by scope. Never report the target project as fully validated solely because `FOUNDATION_INTEGRITY` is green.

## Authorization

The user's instruction to apply the Foundation to a target repository authorizes the ordinary file creation and compatible merges described above. Do not ask for repeated confirmation for each file. Stop only for a real semantic conflict, unresolved data-handling boundary, unexpected target/scope, or another explicit gate.
