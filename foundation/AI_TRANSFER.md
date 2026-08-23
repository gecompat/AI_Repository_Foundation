# Direct AI Transfer Protocol

This protocol allows an AI system with read access to this Foundation repository and write access to another repository to install the reusable rules without running the local installer.

## Source of transfer truth

`foundation/manifest.json` is the complete whitelist. Do not infer transferable files by scanning the repository. Files not listed in `core` or a selected adapter are not transferred.

In particular, never copy the Foundation project's README, LICENSE, changelog, `.gitignore`, project context, Foundation metadata, status, handover, backlog, roadmap, internal decisions, tests, or tool source merely because they exist here.

The target project's root license is never changed by this transfer. Transferred text originates from the Foundation source repository; preserve any legally required attribution/notice through the target project's appropriate third-party/provenance mechanism. If that mechanism or obligation is unclear, report a licensing review item rather than copying/replacing the target root license.

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
6. Files under target `.ai/foundation/` are Foundation baseline rule copies. If one already differs, treat it as a local override/drift and review the semantic difference; do not overwrite silently.
7. Apply the smallest coherent set of changes. The target repository's README, license, domain documentation, project state, backlog, decisions, and implementation remain untouched unless the user's separate task explicitly changes them.
8. Validate that every selected manifest target exists or has an explicitly documented local merge/override, that adapters lead to root `AGENTS.md`, and that no `never_transfer` project artifact was introduced by the transfer.
9. Report `CREATE`, `UNCHANGED`, merged/overridden files, conflicts, and any validation not executed.

## Authorization

The user's instruction to apply the Foundation to a target repository authorizes the ordinary file creation and compatible merges described above. Do not ask for repeated confirmation for each file. Stop only for a real semantic conflict, unresolved data-handling boundary, unexpected target/scope, or another explicit gate.
