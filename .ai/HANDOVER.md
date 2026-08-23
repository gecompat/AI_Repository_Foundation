# Handover

Status: GENERATED/EVIDENCE

## Current state

The v1.2 candidate extends rules-only transfer with a formal semantic-integration contract for existing repositories. File states remain deterministic (`CREATE`, `UNCHANGED`, `MERGE_REQUIRED`, `CONFLICT`), while meaningful governance overlaps are classified separately so mature target rules are preserved rather than normalized to Foundation wording.

Active project governance must remain discoverable from root `AGENTS.md`. Foundation `REQUIRED` rules are minimum floors; `PROJECT_STRONGER`, `PROJECT_SELECTABLE_OVERRIDE`, and `COMPLEMENTARY` target rules are preserved. Unique adapter governance must be rehomed before adapters are thinned.

Validation remains layered: Foundation integrity is not project semantic/runtime validation. Existing target validation-status vocabularies and model-routing policies may remain richer through explicit semantic mapping.

## Next actions

1. Run Foundation validator and deterministic installation/integration tests on the v1.2 implementation head.
2. Confirm GitHub Actions on the final PR head.
3. Record the actual CI evidence and mark FND-005/FND-008/FND-009 done only after the deterministic gate is green.
4. Execute the separate fresh-agent semantic transfer/continuation acceptance test when available; do not claim it beforehand.

## Open constraints

- The deterministic installer does not perform semantic merges; the AI protocol owns semantic classification for existing repositories.
- The Foundation validator can verify the integration contract is installed but cannot deterministically prove that every target-specific active rule was correctly classified/discovered; that remains `PROJECT_SEMANTIC` review.
- Manifest hashes/cross-version provenance remain pending under FND-002.
- Vendor adapter discovery behavior can change and must be rechecked against current primary documentation when adapters change.
