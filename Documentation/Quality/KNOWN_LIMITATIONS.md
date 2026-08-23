# Known Limitations

- Semantic privacy classification cannot be proven by deterministic scanning; v1.1 distinguishes public/repository-intended, confidential, personal/sensitive, secret, and unknown information to avoid blanket gates.
- The deterministic installer intentionally does not semantically merge differing existing files. It reports `MERGE_REQUIRED`; an AI may merge under `foundation/AI_TRANSFER.md` while preserving project-specific content.
- The validator checks the explicit transfer manifest and installed target rules but is not a full semantic governance prover or dedicated secret scanner.
- Manifest hashes and richer cross-version drift analysis are not yet implemented.
- The target project's root license is never copied or replaced. The preferred mechanism for satisfying applicable attribution/notice obligations for transferred rule text is tracked as FND-006.
- Vendor adapter discovery behavior must be checked against current primary documentation before adapter changes.
- Fresh-agent semantic transfer/continuation is pending manual validation under `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md`; deterministic CI success is not substituted for that evidence.
