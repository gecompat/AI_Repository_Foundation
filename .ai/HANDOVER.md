# Handover

Status: GENERATED/EVIDENCE

## Current state

Foundation v1.6 is merged on `main` at `9176ecaea7c972d7f5ec48c66ed19caa0ca68d8c`. It adds the central `foundation-artifact-registry/v2`, derived sequence allocation, generated planning projection, object/property-level three-way merge, early cross-PR collision preflight, and Git-text-merge equivalence validation.

The Foundation source repository uses `.ai/identity/registry.json` as canonical v2 planning state. `.ai/BACKLOG.md` is generated from that registry. `WI-0014` and `DEC-0015` are complete.

A new source-project governance requirement is recorded by `WI-0015` and `DEC-0016`: GitHub `main` must have server-side branch protection with strict/up-to-date required checks `validate` and `registry-integrity`, administrator enforcement, linear history, force pushes disabled, and branch deletion disabled.

`Documentation/Quality/GITHUB_BRANCH_PROTECTION.md` is the authoritative operational guide. `tools/github/configure_branch_protection.py` can apply and read back the desired configuration when run with a token that has repository `Administration: write`.

The connected ChatGPT GitHub interface does not expose a branch-protection/ruleset mutation, no suitable installable plugin was available, and the execution environment has no independent GitHub administration token. GitHub had reported `main` as `protected: false` with required-check enforcement `off`. Therefore `WI-0015` remains `blocked` until a repository administrator activates the setting and GitHub verification confirms it. Do not claim server-side enforcement before that verification.

For target repositories, the behavior is intentionally different. `foundation/AI_TRANSFER.md` and `tools/install_foundation.py` now explicitly surface that GitHub Actions workflow files do not automatically become required checks. When the `artifact-registry-github` capability is relevant, enabling suitable branch protection/rulesets is recommended if the target wants hard merge enforcement, but Foundation transfer must not silently configure it and absence alone is not a `FOUNDATION_INTEGRITY` failure.

## Next actions

1. Apply the source-repository GitHub protection described in `Documentation/Quality/GITHUB_BRANCH_PROTECTION.md` using repository administration or `tools/github/configure_branch_protection.py` with an Administration-write token.
2. Verify the effective GitHub state; only then change `WI-0015` from `blocked` to `done` and record the verification evidence.
3. Keep target-project protection as an explicit recommendation rather than a transferred hard requirement.
4. Separately execute `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md` with a genuinely fresh AI session/test target; WI-0001 remains open only for that criterion.

## Remaining project work

- `WI-0001`: fresh-agent continuation validation.
- `WI-0002`: manifest hashes/cross-version installed provenance.
- `WI-0003`: evaluate packaged release artifact.
- `WI-0004`: optional adapter modules.
- `WI-0015`: source GitHub branch protection activation/verification.

## Open constraints

- Early cross-PR preflight is a snapshot and cannot replace the final check against current `main`.
- The reference GitHub capability treats arrays as atomic merge values unless a project defines narrower safe semantics.
- The central v2 profile is not a high-frequency distributed database; projects with stronger service/database authorities should preserve them.
- Migration from v1/split artifact storage to v2 is a project decision because it changes Registration Authority storage representation even when canonical IDs stay unchanged.
- GitHub repository-administration controls are outside ordinary Foundation file transfer and must not be silently changed in target repositories.
