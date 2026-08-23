# Known Limitations

- Semantic privacy classification cannot be proven by deterministic scanning; the v1.1 rules reduce false gates by distinguishing public/repository-intended, confidential, personal/sensitive, secret, and unknown information.
- The deterministic installer intentionally does not semantically merge differing existing files. It reports `MERGE_REQUIRED`; an AI may merge under `foundation/AI_TRANSFER.md` while preserving project-specific content.
- The validator checks the explicit transfer manifest and installed target rules but is not a full semantic governance prover or dedicated secret scanner.
- Manifest hashes and richer cross-version drift analysis are not yet implemented.
- The target project's root license is never copied or replaced. The preferred mechanism for satisfying any applicable attribution/notice obligations for transferred rule text is tracked as FND-006.
- Vendor adapter discovery behavior must be checked against current primary documentation before adapter changes.
- Fresh-agent semantic transfer/continuation remains a manual acceptance test even when deterministic gates are green.
