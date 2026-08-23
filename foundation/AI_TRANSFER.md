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

## Procedure

1. Read `foundation/manifest.json`.
2. Inspect the target repository's existing root `AGENTS.md`, selected adapter files, and any project-specific instruction hierarchy needed to avoid conflicts.
3. Select `core` plus the adapters requested by the user/project. If none are specified, the manifest's `default_adapters` are recommended, not mandatory.
4. For each manifest entry compare source content with the target path:
   - target absent: `CREATE`;
   - identical: `UNCHANGED`;
   - existing project-specific file with compatible semantics: `MERGE_REQUIRED`;
   - incompatible semantics affecting REQUIRED rules or an unresolved authority conflict: `CONFLICT`.
5. Never replace a differing existing file wholesale. For `AGENTS.md`, preserve all project-specific content and merge only the marked `AI_REPOSITORY_FOUNDATION` block from `foundation/AGENTS.template.md` at an appropriate root scope. For existing adapter files, preserve existing tool-specific content and add only the discovery path back to root `AGENTS.md` when needed.
6. Files under target `.ai/foundation/` are Foundation baseline rule/provenance copies. If one already differs, treat it as a local override/drift and review the semantic difference; do not overwrite silently. The attribution notice is special: any merged version must still contain the complete MIT notice from the Foundation source.
7. Apply the smallest coherent set of changes. The target repository's README, root license, domain documentation, project state, backlog, decisions, and implementation remain untouched unless the user's separate task explicitly changes them.
8. Validate that every selected manifest target exists or has an explicitly documented local merge/override, that adapters lead to root `AGENTS.md`, that the attribution notice preserves the complete Foundation MIT notice, and that no `never_transfer` project artifact was introduced by the transfer.
9. Report `CREATE`, `UNCHANGED`, merged/overridden files, conflicts, attribution validation, and any validation not executed.

## Authorization

The user's instruction to apply the Foundation to a target repository authorizes the ordinary file creation and compatible merges described above. Do not ask for repeated confirmation for each file. Stop only for a real semantic conflict, unresolved data-handling boundary, unexpected target/scope, or another explicit gate.
