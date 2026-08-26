# Handover

Status: GENERATED/EVIDENCE

## Current state

Foundation v1.6 is merged on `main` at `2892b6656933e735b8ab3684af1327ae5a8afc86`. PR #14 / branch `codex/eol-portable-transfer-integrity` is now the combined Foundation **1.7.0 candidate** containing `WI-0016` (portable EOL transfer integrity) and `WI-0017` / `DEC-0017` (repository continuity/break-glass).

The Foundation source repository uses `.ai/identity/registry.json` as canonical v2 planning state. `.ai/BACKLOG.md` is generated from that registry. `WI-0016` is `in_progress`; `WI-0017` is `blocked` only on source GitHub Ruleset migration/read-back after the code/policy gates are consistent.

## EOL portability — WI-0016

A Windows integration exposed a portability defect: Git checkout can materialize transferred UTF-8 Foundation text with CRLF while the Foundation source uses LF. The old byte comparison misclassified EOL-only representation as `MERGE_REQUIRED` / `LOCAL_OVERRIDE_OR_DRIFT`.

The candidate uses shared `tools/content_equivalence.py` in installer and validator. UTF-8 CRLF/LF-only differences compare equal; lone CR, final-newline changes, actual text changes, non-UTF-8 data, and binary differences remain significant. Target `.gitattributes` remains project-owned and is not changed merely to make Foundation validation green.

`tests/test_eol_portability.py` creates a temporary Git repository with `core.autocrlf=true`, installs/commits Foundation, deletes the tracked `.ai/foundation` working-tree directory and checks it out again to force conversion, verifies no false drift, introduces real drift, verifies detection, and cleans up automatically.

An earlier PR-head test used `git reset --hard` without first removing the unchanged working-tree files, so Git on the Linux runner did not rewrite them to CRLF. That test failed substantively. It was correctly treated as `VALIDATION_FAILURE`, not as a GitHub Actions outage or break-glass opportunity. The fixture is now corrected and must pass normally before WI-0016 can close.

## Repository continuity — WI-0017 / DEC-0017

Mandatory external CI must not be the only availability gate for the durable repository/agent-coordination channel. The new transferable `Documentation/Standards/REPOSITORY_CONTINUITY_POLICY.md` distinguishes:

- `VALIDATION_FAILURE`: check ran and found a substantive defect — break-glass prohibited;
- `INFRASTRUCTURE_UNAVAILABLE`: validation cannot produce a trustworthy result because the execution platform/runners/service are unavailable or materially degraded — project-authorized break-glass may be used;
- `UNKNOWN`: cause not established — break-glass prohibited until classified.

The Foundation source target GitHub state is two layered Rulesets:

- `foundation-main-core-safety`: no bypass actors; PR required, zero mandatory approvals, linear history, no force push, no branch deletion;
- `foundation-main-ci-gates`: strict required checks `validate` and `registry-integrity`; the authorized source maintainer may bypass **for pull requests only**.

This means break-glass never enables direct push to `main`. The PR must record outage evidence, immutable base/head, local/manual checks, unreproduced checks, residual risk, and deferred post-recovery validation. Missing CI remains pending rather than being represented as green.

`Documentation/Quality/GITHUB_BREAK_GLASS.md` defines the source procedure. `tools/github/configure_rulesets.py` implements fail-safe migration: create both Rulesets, read back/verify both, then and only then remove legacy classic branch protection, then verify the Rulesets again.

The connected ChatGPT GitHub interface can read Rulesets but does not expose Ruleset mutation. Current server read-back still shows no Rulesets and the previously verified classic branch protection remains active. Therefore `WI-0017` must remain `blocked` until a repository administrator applies the migration and GitHub read-back confirms the two Rulesets.

## Target-project behavior

Foundation 1.7.0 transfers repository-continuity semantics but not repository-administration changes. Targets are told that making external CI mandatory can create an availability dependency; projects needing continuity should consider separating unbypassable core safety from PR-only bypassable CI gates. Foundation does not silently select bypass actors, create Rulesets, weaken existing protection, or treat missing break-glass configuration as a `FOUNDATION_INTEGRITY` defect.

## Next actions

1. Complete deterministic consistency for Foundation 1.7.0 and get PR #14's corrected `validate` and `registry-integrity` checks green when GitHub Actions can execute them.
2. If Actions is genuinely unavailable, do not confuse this with the earlier substantive failure; classify and record the outage according to the new policy.
3. Apply `tools/github/configure_rulesets.py` with an Administration-write token or configure the two Rulesets manually in GitHub; keep classic protection until both replacements are verified.
4. Read back `/rulesets`; verify `foundation-main-core-safety` has no bypass and `foundation-main-ci-gates` has only the authorized source user with `pull_request` bypass plus strict `validate`/`registry-integrity`.
5. Verify legacy classic protection is removed only after Ruleset verification. Then set `WI-0017` to `done` and record evidence.
6. Set `WI-0016` to `done` only after its corrected autonomous regression/full suite succeeds.
7. Finalize PR #14/evidence head and merge according to normal gates, or only use break-glass if a remaining blocked required check is genuinely `INFRASTRUCTURE_UNAVAILABLE` and all policy evidence is recorded.

## Remaining project work

- `WI-0001`: fresh-agent continuation validation.
- `WI-0002`: manifest hashes/cross-version installed provenance.
- `WI-0003`: evaluate packaged release artifact.
- `WI-0004`: optional adapter modules.
- `WI-0016`: corrected EOL portability validation/evidence.
- `WI-0017`: source Ruleset administration/read-back and continuity evidence.

## Open constraints

- Early cross-PR preflight is a snapshot and cannot replace the final check against current `main`.
- The reference GitHub registry capability treats arrays as atomic merge values unless a project defines narrower safe semantics.
- The central v2 profile is not a high-frequency distributed database; projects with stronger service/database authorities should preserve them.
- GitHub repository-administration controls are outside ordinary Foundation file transfer and must not be silently changed in target repositories.
- Break-glass solves CI-service unavailability only; it cannot make GitHub Git/PR/API itself available during a broader GitHub outage.
