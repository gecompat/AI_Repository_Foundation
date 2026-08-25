# Handover

Status: GENERATED/EVIDENCE

## Current state

Foundation v1.6 is merged on `main` at `ed6cb0834dc184653201acb38e3c35e858d0e49d`. It includes the central `foundation-artifact-registry/v2`, derived sequence allocation, generated planning projection, object/property-level three-way merge, early cross-PR collision preflight, Git-text-merge equivalence validation, and explicit GitHub merge-protection guidance.

The Foundation source repository uses `.ai/identity/registry.json` as canonical v2 planning state. `.ai/BACKLOG.md` is generated from that registry. `WI-0014`/`DEC-0015` and `WI-0015`/`DEC-0016` are complete.

GitHub `main` is now server-side protected. GitHub branch metadata reports `protected: true`, required checks `registry-integrity` and `validate`, and enforcement level `everyone`. Manual review of the saved repository rule confirms pull-request-only merge, approvals not required, branch up-to-date required, linear history required, bypass disabled, force pushes disabled, and deletion disabled.

`Documentation/Quality/GITHUB_BRANCH_PROTECTION.md` is the authoritative operational record. `tools/github/configure_branch_protection.py` remains available to reproduce or verify the intended state with an Administration-write token.

For target repositories, the behavior remains intentionally different. `foundation/AI_TRANSFER.md` and `tools/install_foundation.py` explicitly surface that GitHub Actions workflow files do not automatically become required checks. When the `artifact-registry-github` capability is relevant, enabling suitable branch protection/rulesets is recommended if the target wants hard merge enforcement, but Foundation transfer must not silently configure it and absence alone is not a `FOUNDATION_INTEGRITY` failure.

## Remaining project work

- `WI-0001`: fresh-agent continuation validation.
- `WI-0002`: manifest hashes/cross-version installed provenance.
- `WI-0003`: evaluate packaged release artifact.
- `WI-0004`: optional adapter modules.

## Open constraints

- Early cross-PR preflight is a snapshot and cannot replace the final check against current `main`.
- The reference GitHub capability treats arrays as atomic merge values unless a project defines narrower safe semantics.
- The central v2 profile is not a high-frequency distributed database; projects with stronger service/database authorities should preserve them.
- Migration from v1/split artifact storage to v2 is a project decision because it changes Registration Authority storage representation even when canonical IDs stay unchanged.
- GitHub repository-administration controls are outside ordinary Foundation file transfer and must not be silently changed in target repositories.
