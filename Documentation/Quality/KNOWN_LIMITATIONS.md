# Known Limitations

- Semantic privacy classification cannot be proven by deterministic scanning; the Foundation distinguishes public/repository-intended, confidential, personal/sensitive, secret, and unknown information to avoid blanket gates.
- The deterministic installer intentionally does not semantically merge differing existing files. It reports `MERGE_REQUIRED`; direct AI transfer applies the semantic integration policy while preserving project-specific content.
- The Foundation validator proves deterministic `FOUNDATION_INTEGRITY` contracts only. It cannot prove `PROJECT_SEMANTIC` correctness or `RUNTIME_EMPIRICAL` behavior.
- The validator can confirm that the Foundation discovery/integration contract is installed, but it cannot deterministically prove that every active target-specific authority in an arbitrary repository has been discovered and classified correctly. Existing-repository integration therefore requires semantic inventory/review by the AI/human performing the merge.
- Target repo-map schemas vary. The Foundation requires preservation and permits a minimal bridge only when the target schema safely supports it; no generic repo-map rewrite is attempted.
- Manifest hashes and richer cross-version drift/provenance analysis are not yet implemented (FND-002).
- Transferred rules carry a dedicated namespaced MIT attribution notice while the target project's root license remains independent and untouched.
- Vendor adapter discovery behavior must be checked against current primary documentation before adapter changes.
- Fresh-agent semantic transfer/continuation remains pending manual validation under `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md`; deterministic CI success is not substituted for that evidence.
