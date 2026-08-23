# Project Status

Status: GENERATED/EVIDENCE
Last updated: 2026-08-23
Foundation version: 1.1.2 candidate

## Implemented

- rules-only transfer manifest;
- direct AI transfer protocol;
- deterministic manifest-driven installer;
- namespaced target rule layout;
- authorization-envelope action model;
- data-classification privacy model;
- proportional dependency/third-party review;
- target-aware Foundation-integrity validator;
- deterministic installation-model tests and CI;
- v1.0 bootstrap CLI compatibility mapping;
- dedicated Foundation attribution notice that accompanies transferred rules without modifying the target root license;
- explicit layered validation ownership: `FOUNDATION_INTEGRITY`, `PROJECT_SEMANTIC`, and `RUNTIME_EMPIRICAL`.

## Validation evidence

- Previous v1.1 deterministic Foundation CI: validated successfully on the final v1.1 PR head.
- FND-006 attribution implementation: Foundation CI run `32638922019`, head `9102a70bc13efb6f1642321ccbcedd56a54d6046`: validated, conclusion `success`.
- FND-006 deterministic coverage includes target README/root-LICENSE preservation, mandatory notice installation, complete MIT-notice preservation, attribution-manifest integrity, tampered-notice blocking, idempotency, and transactional conflict handling.
- FND-007 layered validation implementation: Foundation CI run `32642237490`, head `f910947fd186c0ed52317238de200b89350d5ce8`: validated, conclusion `success`.
- FND-007 deterministic coverage includes machine-readable validation ownership, target validator scope `FOUNDATION_INTEGRITY`, explicit `PROJECT_VALIDATION_OUT_OF_SCOPE`, and local-override drift warnings that do not claim semantic correctness.
- fresh-agent semantic transfer/continuation: pending manual validation under `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md`.

FND-006 and FND-007 are complete. The release profile remains intentionally blocked until the pending fresh-agent manual acceptance test is completed.
