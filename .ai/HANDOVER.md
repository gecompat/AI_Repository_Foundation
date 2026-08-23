# Handover

Status: GENERATED/EVIDENCE

## Current state

The v1.1 transfer model uses a manifest whitelist consumed by both the deterministic installer and direct AI transfer. Target README, root LICENSE, project context/state, backlog, decisions, tests, and implementation are outside the transfer set.

FND-006 is complete. Every rules transfer includes `.ai/foundation/AI_REPOSITORY_FOUNDATION_NOTICE.md`, which preserves the complete Foundation MIT notice while leaving the target project's root license independent and untouched. Foundation CI run `32638922019` validated the attribution mechanism on head `9102a70bc13efb6f1642321ccbcedd56a54d6046`.

Authorization is task-envelope based: ordinary expected operations proceed without repeated confirmation. Privacy is classification/destination based rather than triggered merely by real information.

## Next actions

1. Confirm Foundation CI on the final PR head containing this evidence update.
2. Execute `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md` when a genuinely fresh AI session/test target is available; do not claim it as executed beforehand.
3. After manual acceptance, complete FND-001 and use the `release` validation profile before tagging a release.

## Open constraints

- Deterministic installation never overwrites differing existing rules; semantic merge is deliberately delegated to the AI transfer protocol or explicit resolution.
- Vendor discovery behavior can change and must be rechecked against current primary documentation when adapters change.
