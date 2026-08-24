# Handover

Status: GENERATED/EVIDENCE

## Current state

The v1.3 candidate adds a project-independent persistent identity model without turning Foundation integration into a historical renaming exercise. Persistent machine identity, human reference, aliases/external references, mutable relations/classification, revision identity, and current locator are separate concepts.

For new/adopting projects the Foundation default uses an opaque RFC 9562 UUIDv7 machine UID plus flat typed project-local human references. UUIDv4 is compatible. Broad default prefixes include `CAP`, `REQ`, `WI`, `DEC`, `GATE`, `RISK`, `EXP`, `OPS`, `INC`, `REL`, and `TEST`; finer subtypes, hierarchy, wave, status, owner, phase, and location remain metadata.

Existing projects default to `PRESERVE`. `ADOPT_FORWARD` may introduce the improved profile prospectively while retaining historical references. `MIGRATE_EXPLICIT` is never implied by Foundation installation and requires an explicit durable migration decision, old-to-new mappings, alias retention, impact analysis, validation, and recovery. Missing input means preserve the existing convention.

The identity policy is transferred through `foundation/manifest.json`, indexed in the target `repo_map`, incorporated into semantic integration/direct AI transfer, and checked by Foundation validator/tests. Target-specific historical identifier correctness remains `PROJECT_SEMANTIC`/`RUNTIME_EMPIRICAL`, not something a generic Foundation validator can prove.

Foundation CI run `32708542537` validated implementation head `a1f5463d5d32d0e04394303fd6f6aac8846810ce`; both the Foundation validator and installation-model test job steps succeeded. FND-010 is therefore complete for its deterministic contract. The evidence-only closing commits must still pass the final PR-head CI before merge.

## Next actions

1. Confirm `Foundation CI` on the final evidence/PR head.
2. Merge PR #7 only after that final CI result is green.
3. Execute `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md` with a genuinely fresh AI session/test target when available; do not claim it as executed beforehand.
4. Complete FND-001 only after that separate manual acceptance is recorded.

## Open constraints

- The deterministic installer does not perform semantic merges or identifier migrations; the AI/project integration path owns semantic classification and adoption-mode decisions.
- The Foundation validator verifies the installed identity contract but cannot deterministically prove that every target-specific historical identifier, alias, relation, prefix, or migration mapping is semantically correct.
- Foundation v1.3 intentionally does not add a mandatory identity-registry serialization or resolver implementation; add one only if target-project evidence demonstrates a reusable need beyond the policy/manifest contract.
- Manifest hashes/cross-version installed provenance remain pending under FND-002.
- Vendor adapter discovery behavior can change and must be rechecked against current primary documentation when adapters change.
