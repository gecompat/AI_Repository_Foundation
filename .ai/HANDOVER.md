# Handover

Status: GENERATED/EVIDENCE

## Current state

Foundation v1.6 adds a central repository-native artifact registry and semantic merge layer on top of persistent identity, Registration Authority, and semantic Foundation upgrades.

`foundation-artifact-registry/v2` is the default profile when a project chooses a JSON-file Registration Authority. Complete records live in one `artifacts` object keyed by canonical human reference. The v2 profile does not persist `next_sequence`; the next candidate derives from the maximum existing canonical sequence plus live reservations. For Git-native repositories, a second mutable global `registry_revision` is omitted because Git commit/blob state is the concurrency token.

`Documentation/Standards/CENTRAL_ARTIFACT_REGISTRY_POLICY.md` is transferred core. It requires cross-record validation and an object/property-level three-way merge over the merge-base registry, current target-branch registry, and PR-head registry. Independent properties may combine; divergent changes to the same value and concurrent different additions of the same canonical reference block. Lists are atomic unless a narrower project contract defines safe element semantics.

The optional `artifact-registry-github` capability provides `registry_semantic.py` plus a GitHub Actions workflow template. It performs early open-PR preflight for duplicate new human references, duplicate UIDs, alias collisions, and overlapping artifact edits. At final PR validation it computes the object-level merge, separately simulates Git's textual registry merge, and requires the parsed Git result to equal the semantic expected object. A normal textually clean Git merge is therefore not accepted as correctness evidence by itself.

The Foundation source repository uses `.ai/identity/registry.json` as canonical v2 planning state. It contains complete records through `WI-0014` and `DEC-0015`; `WI-0014` is complete. `.ai/BACKLOG.md` is generated from the registry and CI-checked. `DEC-0015` records the architecture decision in `Documentation/Architecture/decisions/DEC-0015-central-registry-semantic-merge.md`.

The v1 allocation-only registry remains a compatible legacy profile. Existing projects are not auto-migrated. The existing optional Python/PowerShell `artifact-registration-clients` remain v1 reference implementations; v2 is normative through policy/schema and the optional GitHub reference capability. Another language or CI platform may implement the same v2 contract.

Implementation evidence on head `1bd2a9bb0a487780e2d12401ae2747cadef3f6d3`: Foundation CI run `32837531482` succeeded and Foundation Artifact Registry run `32837531385` succeeded. The latter passed registry validation, generated-backlog verification, early cross-PR preflight, object-level three-way merge, and Git-text-merge equivalence. A transient transfer-guard failure caused by generated Python `__pycache__/*.pyc` files was corrected by excluding runtime cache artifacts from managed-source discovery and adding a regression test.

## Remaining project work

- `WI-0001` remains open only for the separate genuinely fresh-agent continuation validation under `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md`.
- `WI-0002` remains proposed for manifest hashes/cross-version installed provenance.
- `WI-0003` remains proposed for evaluating a packaged release artifact.
- `WI-0004` remains proposed for optional adapter modules.

## Open constraints

- The GitHub workflow files provide deterministic checks, but this repository currently has no connector-exposed mutation for configuring branch protection/rulesets. Hard server-side enforcement that these checks are *required* must not be claimed unless repository administration is separately verified/configured.
- Early cross-PR preflight is a snapshot and cannot replace the final check against current `main`.
- The reference GitHub capability treats arrays as atomic merge values unless a project defines narrower safe semantics.
- The central v2 profile improves repository-native state consistency but is still not a high-frequency distributed database; projects with stronger service/database authorities should preserve them.
- Migration from v1/split artifact storage to v2 is a project decision because it changes Registration Authority storage representation even when canonical IDs stay unchanged.
- Manifest hashes/cross-version installed provenance remain pending under WI-0002.
- Vendor adapter discovery behavior can change and must be rechecked against current primary documentation when adapters change.
