# Handover

Status: GENERATED/EVIDENCE

## Current state

The v1.4 candidate operationalizes the v1.3 persistent-identity model for both human and AI artifact creation without making any implementation language mandatory.

A final sequential human reference is allocated by a project-defined **Registration Authority**. Humans and AI use the same authority for the same identifier scope. `DIRECT` is valid only when that authority serializes allocation or provides equivalent uniqueness. `DEFERRED` creates the permanent machine UID immediately while leaving the final human reference unallocated until a safe registration point.

The normative contract is language-neutral. Core transfer includes `ARTIFACT_REGISTRATION_POLICY.md` and three JSON Schemas for artifact records, registry state, and registration requests. Existing compatible Jira/GitHub Issues/Azure DevOps/database/service/project allocators are preserved rather than replaced.

Python is not required. The opt-in `artifact-registration-clients` capability contains independent Python and PowerShell reference clients. Both implement registry initialization, direct/deferred creation, later registration, resolve, registry revision checks, stable allocation/non-reuse, and UUIDv7 generation. Foundation CI runs the same deterministic fixtures against both clients and explicitly verifies the PowerShell runtime.

Installer and validator understand optional capabilities. Reference clients are not transferred by default. Target-specific Registration Authority selection, network/distributed concurrency, issue-tracker/database integration, and operational recovery remain `PROJECT_SEMANTIC`/`RUNTIME_EMPIRICAL` responsibilities.

Two development CI runs were useful failure evidence rather than completion evidence: run `32711122382` exposed PowerShell scriptblock result-scope handling; run `32711344144` reduced the remaining defects to deferred-null coercion and an incorrect UUID-version assertion. Both defects were corrected. GitHub Actions `Foundation CI` run `32711801576` on implementation/documentation head `e56017f06d0084a444c0a812896eb89f1386657b` then completed successfully, including PowerShell runtime verification, Foundation validation, and all cross-language/installation contract tests. FND-011 is complete for its deterministic contract.

## Next actions

1. Confirm `Foundation CI` on the evidence-only final PR #8 head.
2. Merge PR #8 only if that final head is green.
3. Execute `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md` with a genuinely fresh AI session/test target when available; do not claim it as executed beforehand.
4. Complete FND-001 only after that separate manual acceptance is recorded.

## Open constraints

- The local reference registry is safe only for the concurrency envelope documented by `ARTIFACT_REGISTRATION_POLICY.md`; it is not a distributed database. Multi-user/network-concurrent projects should use an appropriate central authority.
- The Foundation validator can prove core/capability installation integrity and client drift, but cannot determine whether an arbitrary project's chosen Registration Authority is semantically or operationally correct.
- `DEFERRED` solves distributed creation identity by making the UID final before human-reference allocation; it does not make local sequence allocation itself distributed.
- Existing project allocators and identifier histories remain project-owned governance and must not be replaced merely because Foundation reference clients are available.
- Manifest hashes/cross-version installed provenance remain pending under FND-002.
- Vendor adapter discovery behavior can change and must be rechecked against current primary documentation when adapters change.
