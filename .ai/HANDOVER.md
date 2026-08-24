# Handover

Status: GENERATED/EVIDENCE

## Current state

The v1.4 ruleset includes persistent identity plus language-neutral artifact registration for both humans and AI. A final sequential human reference is allocated by a project-defined **Registration Authority**. Humans and AI use the same authority for the same identifier scope. `DIRECT` is valid only when that authority serializes allocation or provides equivalent uniqueness. `DEFERRED` creates the permanent machine UID immediately while leaving the final human reference unallocated until a safe registration point.

Core transfer includes `PERSISTENT_IDENTITY_POLICY.md`, `ARTIFACT_REGISTRATION_POLICY.md`, and the three registration JSON Schemas. The optional `artifact-registration-clients` capability contains independent Python and PowerShell reference clients; Python is not required. Existing compatible Jira/GitHub Issues/Azure DevOps/database/service/project allocators remain valid and are preserved.

The source transfer plane is now explicitly guarded. `foundation/manifest.json#ruleset_version` is the single Foundation source-version authority. Its `transfer_coverage_contract` defines managed reusable policy/schema roots, fixed core sources, registered legacy capability roots, the future `foundation/capabilities/<capability>/` layout, and version mirrors. `tools/transfer_manifest_guard.py` fails closed when a managed reusable policy/schema/capability file exists without a matching manifest entry, when a capability source is outside allowed roots, when a contract policy/schema mapping is not transferred, or when a declared version mirror differs from the manifest version.

This guard preserves the explicit-whitelist model: it does not auto-transfer repository files. Instead it prevents a reusable Foundation feature from being declared complete while its transfer representation is incomplete.

Source Foundation version and target installed Foundation version are now explicitly separate concepts. For upgrade/capability questions, read `foundation/manifest.json` from the exact Foundation source ref and compare that with the target's installed `.ai/foundation/repo_map.yaml`; a target still on 1.2 does not imply that the current Foundation source is limited to 1.2.

GitHub Actions `Foundation CI` run `32716654407` on implementation head `f8b0d9f35379ebc9ab775bbfc5a8cd9b69c942cf` completed successfully. The run passed PowerShell runtime verification, the new transfer completeness/version guard, the existing Foundation validator, and all installation/cross-language/unit tests. Negative tests prove that version drift and omitted policy/schema/capability transfer entries are blocking. FND-012 is complete for its deterministic contract.

## Next actions

1. Confirm `Foundation CI` on the evidence-only final PR #9 head.
2. Merge PR #9 only if that final head is green.
3. Execute `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md` with a genuinely fresh AI session/test target when available; do not claim it as executed beforehand.
4. Complete FND-001 only after that separate manual acceptance is recorded.

## Open constraints

- The completeness guard proves structural transfer coverage for managed roots and declared mappings. It cannot infer that arbitrary source-project prose outside the managed reusable roots was semantically intended to become a transferable rule; Foundation maintenance therefore requires new reusable policies/schemas/capabilities to use the prescribed managed locations.
- The local reference registry is safe only for the concurrency envelope documented by `ARTIFACT_REGISTRATION_POLICY.md`; it is not a distributed database. Multi-user/network-concurrent projects should use an appropriate central authority.
- The Foundation validator can prove core/capability installation integrity and client drift, but cannot determine whether an arbitrary project's chosen Registration Authority is semantically or operationally correct.
- Manifest hashes/cross-version installed provenance remain pending under FND-002; the new guard addresses completeness/version-consistency, not cryptographic installed-provenance tracking.
- Vendor adapter discovery behavior can change and must be rechecked against current primary documentation when adapters change.
