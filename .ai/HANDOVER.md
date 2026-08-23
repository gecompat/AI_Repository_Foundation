# Handover

Status: GENERATED/EVIDENCE

## Current state

The v1.1 branch replaces repository-wide copying with a manifest-whitelisted rules-only transfer model. Both the deterministic installer and direct AI transfer consume the same manifest. Target README, LICENSE, project context/state, backlog, decisions, tests, and implementation are outside the transfer set.

Authorization is task-envelope based: ordinary expected operations proceed without repeated confirmation. Privacy is classification/destination based rather than triggered merely by real information.

Deterministic CI is green for commit `d6439ac60a71c39a9c11bdb943e808b8481f7aaf`. A later documentation/test-plan commit must receive its own CI result before merge.

## Next actions

1. Confirm Foundation CI on the final PR head.
2. Execute `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md` when a genuinely fresh AI session/test target is available; do not claim it as executed beforehand.
3. After manual acceptance, update `.ai/PROJECT_STATUS.md`, complete FND-001, and use the `release` validation profile before tagging a v1.1 release.

## Open constraints

- Deterministic installation never overwrites differing existing rules; semantic merge is deliberately delegated to the AI transfer protocol or explicit resolution.
- The target project's root license is never modified. FND-006 tracks the preferred notice/attribution mechanism for transferred rule text.
- Vendor discovery behavior can change and must be rechecked against current primary documentation when adapters change.
