# Known Limitations

- Semantic privacy classification cannot be proven by deterministic scanning; v1.1 distinguishes public/repository-intended, confidential, personal/sensitive, secret, and unknown information to avoid blanket gates.
- The deterministic installer intentionally does not semantically merge differing existing files. It reports `MERGE_REQUIRED`; an AI may merge under `foundation/AI_TRANSFER.md` while preserving project-specific content.
- The Foundation validator proves deterministic `FOUNDATION_INTEGRITY` contracts only. It can detect missing rules/provenance, adapter failures, selected secret/path patterns, validation-scope metadata, and local drift; it cannot prove `PROJECT_SEMANTIC` correctness of local overrides, architecture, domain/documentation contracts, or `RUNTIME_EMPIRICAL` behavior. Target-project validators and reviews remain required when their contracts are affected.
- Manifest hashes and richer cross-version drift analysis are not yet implemented.
- FND-006 is complete: transferred rules carry a dedicated namespaced MIT attribution notice while the target project's root license remains independent and untouched.
- Vendor adapter discovery behavior must be checked against current primary documentation before adapter changes.
- Fresh-agent semantic transfer/continuation is pending manual validation under `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md`; deterministic CI success is not substituted for that evidence.
