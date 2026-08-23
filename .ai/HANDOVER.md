# Handover

Status: GENERATED/EVIDENCE

## Current state

The v1.1 transfer model uses a manifest whitelist consumed by both the deterministic installer and direct AI transfer. Target README, root LICENSE, project context/state, backlog, decisions, tests, and implementation are outside the transfer set.

FND-006 adds a dedicated `.ai/foundation/AI_REPOSITORY_FOUNDATION_NOTICE.md` to the transfer payload. It preserves the complete Foundation MIT notice while leaving the target project's root license independent and untouched.

Authorization is task-envelope based: ordinary expected operations proceed without repeated confirmation. Privacy is classification/destination based rather than triggered merely by real information.

## Next actions

1. Confirm Foundation CI on the FND-006 PR head.
2. If green, record the deterministic attribution evidence and mark FND-006 done.
3. Execute `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md` when a genuinely fresh AI session/test target is available; do not claim it as executed beforehand.
4. After manual acceptance, complete FND-001 and use the `release` validation profile before tagging a release.

## Open constraints

- Deterministic installation never overwrites differing existing rules; semantic merge is deliberately delegated to the AI transfer protocol or explicit resolution.
- Vendor discovery behavior can change and must be rechecked against current primary documentation when adapters change.
