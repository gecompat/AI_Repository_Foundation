# Handover

Status: GENERATED/EVIDENCE

## Current state

Foundation v1.6 is merged on `main` at `2892b6656933e735b8ab3684af1327ae5a8afc86`. It includes the central `foundation-artifact-registry/v2`, derived sequence allocation, generated planning projection, object/property-level three-way merge, early cross-PR collision preflight, Git-text-merge equivalence validation, and verified GitHub merge protection.

The Foundation source repository uses `.ai/identity/registry.json` as canonical v2 planning state. `.ai/BACKLOG.md` is generated from that registry. `WI-0014`/`DEC-0015` and `WI-0015`/`DEC-0016` are complete.

GitHub `main` is server-side protected. GitHub branch metadata reports `protected: true`, required checks `registry-integrity` and `validate`, and enforcement level `everyone`. Manual review of the saved repository rule confirms pull-request-only merge, approvals not required, branch up-to-date required, linear history required, bypass disabled, force pushes disabled, and deletion disabled.

`Documentation/Quality/GITHUB_BRANCH_PROTECTION.md` is the authoritative operational record. `tools/github/configure_branch_protection.py` remains available to reproduce or verify the intended state with an Administration-write token.

## v1.6.1 candidate — WI-0016

A Windows integration exposed a portability defect: Git checkout can materialize transferred UTF-8 Foundation text with CRLF while the Foundation source uses LF. The previous installer and target validator compared bytes and therefore misclassified an EOL-only working-tree representation difference as `MERGE_REQUIRED` / `LOCAL_OVERRIDE_OR_DRIFT`.

The candidate fix introduces `tools/content_equivalence.py`, shared by installer and validator. UTF-8 CRLF is normalized to LF before equality comparison. The rule remains deliberately narrow: lone CR, final-newline changes, actual text edits, non-UTF-8 data, and binary differences remain significant.

The transferred validation policy and direct AI transfer protocol now state that an LF/CRLF-only difference is not Foundation drift and must not cause an otherwise valid integration to be reopened. A target `.gitattributes` must not be created or modified merely to silence such a comparison; target line-ending policy remains project-owned.

`tests/test_eol_portability.py` is an autonomous repository-level regression: it creates a temporary Git repository, sets `core.autocrlf=true`, installs Foundation, commits it, forces a fresh checkout that materializes CRLF, re-runs installer planning and target validation, verifies there is no false drift, introduces a real content edit and verifies drift detection, then relies on `TemporaryDirectory` cleanup to delete the test repository.

The GitHub connector does not expose repository create/delete administration, so the autonomous regression uses a real temporary **local Git repository** rather than creating disposable remote GitHub repositories. This exercises the Git checkout behavior that caused the defect without leaving remote resources behind.

WI-0016 remains `in_progress` until the complete Foundation CI and `registry-integrity` Required Checks pass on the coherent PR head; only then should its evidence be recorded and status changed to `done`.

For target repositories, GitHub protection behavior remains intentionally separate: `foundation/AI_TRANSFER.md` and `tools/install_foundation.py` surface that Actions workflow files do not automatically become required checks. Enabling suitable branch protection/rulesets is recommended when hard merge enforcement is desired, but Foundation transfer does not silently configure it and absence alone is not a `FOUNDATION_INTEGRITY` failure.

## Remaining project work

- `WI-0001`: fresh-agent continuation validation.
- `WI-0002`: manifest hashes/cross-version installed provenance.
- `WI-0003`: evaluate packaged release artifact.
- `WI-0004`: optional adapter modules.
- `WI-0016`: complete 1.6.1 EOL portability validation and merge.

## Open constraints

- Early cross-PR preflight is a snapshot and cannot replace the final check against current `main`.
- The reference GitHub capability treats arrays as atomic merge values unless a project defines narrower safe semantics.
- The central v2 profile is not a high-frequency distributed database; projects with stronger service/database authorities should preserve them.
- Migration from v1/split artifact storage to v2 is a project decision because it changes Registration Authority storage representation even when canonical IDs stay unchanged.
- GitHub repository-administration controls are outside ordinary Foundation file transfer and must not be silently changed in target repositories.
