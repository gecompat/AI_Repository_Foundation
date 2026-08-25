# Handover

Status: GENERATED/EVIDENCE

## Current state

The v1.6 candidate adds a central repository-native artifact registry and semantic merge layer on top of persistent identity, Registration Authority, and semantic Foundation upgrades.

`foundation-artifact-registry/v2` is the default profile when a project chooses a JSON-file Registration Authority. Complete records live in one `artifacts` object keyed by canonical human reference. The v2 profile does not persist `next_sequence`; the next candidate is derived from the maximum existing canonical sequence plus live reservations. For Git-native repositories, a second mutable global `registry_revision` is also omitted because Git commit/blob state is the concurrency token.

`Documentation/Standards/CENTRAL_ARTIFACT_REGISTRY_POLICY.md` is transferred core. It requires cross-record validation and an object/property-level three-way merge over the merge-base registry, current target-branch registry, and PR-head registry. Independent properties may combine; divergent changes to the same value and concurrent different additions of the same canonical reference block. The merge candidate is then validated semantically.

The optional `artifact-registry-github` capability provides `registry_semantic.py` plus a GitHub Actions workflow template. It performs early open-PR preflight for duplicate new human references, duplicate UIDs, alias collisions, and overlapping artifact edits. At final PR validation it computes the object-level merge, separately simulates Git's textual registry merge, and requires the parsed Git result to equal the semantic expected object. A normal textually clean Git merge is therefore not accepted as correctness evidence by itself.

The Foundation source repository has migrated `.ai/identity/registry.json` to v2. It contains complete records through `WI-0014` and `DEC-0015`. `.ai/BACKLOG.md` is now a generated projection and is CI-checked against the registry. `DEC-0015` records the architecture decision in `Documentation/Architecture/decisions/DEC-0015-central-registry-semantic-merge.md`.

The v1 allocation-only registry remains a compatible legacy profile. Existing projects are not auto-migrated. The existing optional Python/PowerShell `artifact-registration-clients` remain v1 reference implementations; v2 is normative through policy/schema and the optional GitHub reference capability. Another language or CI platform may implement the same v2 contract.

The previous v1.5 semantic-upgrade work is complete: PR #10 final evidence head `3fec8bad5f7816b7741ef729735aeec56e492c0c` passed Foundation CI run `32735966279` and was squash-merged as `400c175dac222af0c4eaee159caa955e67bbdbb7`.

## Next actions

1. Open the WI-0014 PR from `codex/central-registry-semantic-merge` after the branch state is internally coherent.
2. Require the normal Foundation CI plus the new Foundation Artifact Registry workflow to pass on the implementation head.
3. Correct only evidenced defects; then update WI-0014/DEC-0015/status/handover with implementation evidence.
4. Run the same gates again on the final evidence head.
5. Squash-merge only that exact green final head to `main`; verify `origin/main` and branch cleanup.
6. Separately execute `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md` with a genuinely fresh AI session/test target when available; WI-0001 remains open only for that criterion.

## Open constraints

- GitHub workflow files provide checks, but this repository currently has no connector-exposed API for configuring branch protection/rulesets. Hard server-side enforcement that the registry checks are **required** may therefore still need repository-admin configuration; do not claim it is enforced unless verified.
- Early cross-PR preflight is a snapshot and cannot replace the final check against current `main`.
- The reference GitHub capability treats arrays as atomic merge values unless a project defines narrower safe semantics.
- The central v2 profile improves repository-native state consistency but is still not a high-frequency distributed database; projects with stronger service/database authorities should preserve them.
- Migration from v1/split artifact storage to v2 is a project decision because it changes Registration Authority storage representation even when canonical IDs stay unchanged.
- Manifest hashes/cross-version installed provenance remain pending under WI-0002.
- Vendor adapter discovery behavior can change and must be rechecked against current primary documentation when adapters change.
