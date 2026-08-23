# Handover

Status: GENERATED/EVIDENCE

## Current state

The v1.1 transfer model uses a manifest whitelist consumed by both the deterministic installer and direct AI transfer. Target README, root LICENSE, project context/state, backlog, decisions, tests, implementation, and project-specific validation infrastructure are outside the transfer set.

FND-006 is complete. Every rules transfer includes `.ai/foundation/AI_REPOSITORY_FOUNDATION_NOTICE.md`, which preserves the complete Foundation MIT notice while leaving the target project's root license independent and untouched.

FND-007 is complete. Foundation validation is explicitly limited to `FOUNDATION_INTEGRITY`; target repositories retain authority for `PROJECT_SEMANTIC` and `RUNTIME_EMPIRICAL`. Foundation CI run `32642237490` validated the scope contract on head `f910947fd186c0ed52317238de200b89350d5ce8`. Local override/drift detection is not semantic approval, and existing project validators/static contracts/tests must be preserved when relevant.

Authorization is task-envelope based: ordinary expected operations proceed without repeated confirmation. Privacy is classification/destination based rather than triggered merely by real information.

## Next actions

1. Confirm Foundation CI on the final PR head containing this evidence update.
2. Execute `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md` when a genuinely fresh AI session/test target is available; do not claim it as executed beforehand.
3. After manual acceptance, complete FND-001 and use the `release` validation profile before tagging a release.

## Open constraints

- Deterministic installation never overwrites differing existing rules; semantic merge is deliberately delegated to the AI transfer protocol or explicit resolution.
- Foundation validator success proves Foundation integration integrity only; project-specific semantic/runtime validation remains target-owned.
- Vendor adapter discovery behavior can change and must be rechecked against current primary documentation when adapters change.
