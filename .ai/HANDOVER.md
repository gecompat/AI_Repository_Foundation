# Handover

Status: GENERATED/EVIDENCE

## Current state

The v1.1 work branch replaces repository-wide copying with a manifest-whitelisted rules-only transfer model. Both a deterministic installer and direct AI transfer consume the same manifest. Target README, LICENSE, project context/state, backlog, decisions, tests, and implementation are not part of the transfer set.

Authorization is task-envelope based: ordinary expected operations proceed without repeated confirmation. Privacy is classification/destination based rather than triggered merely by real information.

## Next actions

1. Run `python tools/foundation_validator.py --profile full` on the final branch head.
2. Run `python -m unittest discover -s tests -v`.
3. Open a pull request and confirm Foundation CI is green.
4. Perform one repository-only semantic review: a fresh AI reads `foundation/manifest.json` and `foundation/AI_TRANSFER.md` and explains/applies the bounded transfer without using chat history.
5. Record actual evidence in `.ai/PROJECT_STATUS.md` and complete FND-001.

## Open constraints

- Deterministic installation never overwrites differing existing rules; semantic merge is deliberately delegated to the AI transfer protocol or explicit human resolution.
- The target project's root license is never modified. FND-006 tracks the preferred notice/attribution mechanism for transferred rule text.
- Vendor discovery behavior can change and must be rechecked against current primary documentation when adapters change.
