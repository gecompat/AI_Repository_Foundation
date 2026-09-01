# Handover

Status: GENERATED/EVIDENCE

## Current state

Branch `codex/rule-context-cache` is the Foundation 1.8.0 implementation for completed `WI-0018` and accepted `DEC-0018`. It adds a transferable Rule Context Cache contract/schema and an opt-in reference planner while preserving native Codex instruction discovery. The local completion gate on 2026-09-01 passed transfer/feature guards, registry/backlog checks, the full Foundation validator, diff hygiene, compilation/JSON parsing, focused regressions, and all 94 tests. Re-read exact branch, PR, CI, and `origin/main` heads before integration.

PR #14 / branch `codex/eol-portable-transfer-integrity` remains the Foundation 1.7.0 integration record for completed `WI-0016` (portable EOL transfer integrity) and `WI-0017` / accepted `DEC-0017` (repository continuity/break-glass). Its last pre-migration implementation head was `fdd67225edaccb912a96f7e2fe1286d0749975c6`.

The Foundation source repository uses `.ai/identity/registry.json` as canonical v2 planning state. `.ai/BACKLOG.md` is generated from that registry. `WI-0018` is `done`; its GitHub CI/merge state remains external runtime evidence until the feature branch is integrated.

## Rule Context Cache — WI-0018 / DEC-0018

Codex still discovers and applies the complete global/project `AGENTS.override.md`/`AGENTS.md` chain at each new run/session. The cache optimizes only repeated semantic analysis of additional repository governance/context after one complete scoped analysis.

The v1 contract fingerprints repository/canonical-root/worktree identity, repository-relative working directory, exact instruction order, effective fallback/size settings, actual working-tree bytes, Git `HEAD`/index/dirty state, source identity, and transitive dependency topology. It emits:

- `CACHE_HIT` only for an exact validated match and only when the exact session analysis key is available;
- `PARTIAL_INVALIDATION` for changed non-instruction sources, rereading those sources and all transitive dependents;
- `CACHE_MISS` for instruction, scope, source-set, topology, discovery, schema/generator, corruption, incomplete-state, or uncertainty changes.

The optional planner is `foundation/capabilities/rule-context-cache/rule_context_cache.py`. Its `check` operation does not mutate rules or cache state; `record` uses a bounded exclusive lock, a stable recheck, flush, and atomic replacement. Records contain fingerprints/dependency metadata only, never rule text or analysis summaries. In-repository cache paths are accepted only when untracked and already ignored; the planner never edits `.gitignore`.

## EOL portability — WI-0016

A Windows integration exposed a portability defect: Git checkout can materialize transferred UTF-8 Foundation text with CRLF while the Foundation source uses LF. The old byte comparison misclassified EOL-only representation as `MERGE_REQUIRED` / `LOCAL_OVERRIDE_OR_DRIFT`.

The candidate uses shared `tools/content_equivalence.py` in installer and validator. UTF-8 CRLF/LF-only differences compare equal; lone CR, final-newline changes, actual text changes, non-UTF-8 data, and binary differences remain significant. Target `.gitattributes` remains project-owned and is not changed merely to make Foundation validation green.

`tests/test_eol_portability.py` creates a temporary Git repository with `core.autocrlf=true`, installs/commits Foundation, deletes the tracked `.ai/foundation` working-tree directory and checks it out again to force conversion, verifies no false drift, introduces real drift, verifies detection, and cleans up automatically.

An earlier PR-head test used `git reset --hard` without first removing the unchanged working-tree files, so Git on the Linux runner did not rewrite them to CRLF. That test failed substantively. It was correctly treated as `VALIDATION_FAILURE`, not as a GitHub Actions outage or break-glass opportunity. The corrected regression, focused tests, complete 72-test suite, and PR-head checks subsequently succeeded; WI-0016 is complete.

## Repository continuity — WI-0017 / DEC-0017

Mandatory external CI must not be the only availability gate for the durable repository/agent-coordination channel. The new transferable `Documentation/Standards/REPOSITORY_CONTINUITY_POLICY.md` distinguishes:

- `VALIDATION_FAILURE`: check ran and found a substantive defect — break-glass prohibited;
- `INFRASTRUCTURE_UNAVAILABLE`: validation cannot produce a trustworthy result because the execution platform/runners/service are unavailable or materially degraded — project-authorized break-glass may be used;
- `UNKNOWN`: cause not established — break-glass prohibited until classified.

The Foundation source GitHub state is two verified active Rulesets targeting exactly `refs/heads/main`:

- `foundation-main-core-safety` (ID `21588442`): no bypass actors; PR required, zero mandatory approvals, linear history, no force push, no branch deletion;
- `foundation-main-ci-gates` (ID `21588444`): strict required checks `validate` and `registry-integrity`; only user `48807214` may bypass with mode `pull_request` / **For pull requests only**.

This means break-glass never enables direct push to `main`. The PR must record outage evidence, immutable base/head, local/manual checks, unreproduced checks, residual risk, and deferred post-recovery validation. Missing CI remains pending rather than being represented as green.

`Documentation/Quality/GITHUB_BREAK_GLASS.md` defines the source procedure. `tools/github/configure_rulesets.py` implements fail-safe migration: create both Rulesets, read back/verify both, then and only then remove legacy classic branch protection, then verify the Rulesets again.

On 2026-08-26, `tools/github/configure_rulesets.py` created and read back both Rulesets, then removed classic protection, then read both Rulesets again. Independent authenticated GitHub API read-back confirmed the exact actors/rules and effective `main` rules; the classic branch-protection endpoint returned HTTP 404 only after replacement verification. `main` remained reported as protected. WI-0017 is complete.

## Target-project behavior

Foundation 1.8.0 preserves the 1.7 repository-continuity semantics but does not transfer repository-administration changes. Targets are told that making external CI mandatory can create an availability dependency; projects needing continuity should consider separating unbypassable core safety from PR-only bypassable CI gates. Foundation does not silently select bypass actors, create Rulesets, weaken existing protection, or treat missing break-glass configuration as a `FOUNDATION_INTEGRITY` defect.

Rule-context policy/schema are core transfer material; the executable planner remains opt-in. Target adoption preserves stronger project governance and native instruction discovery, selects an authorized local non-versioned cache location, performs a complete first analysis per scope/rule version, and never treats the record as authority or evidence.

## Continuation

- Re-read exact `origin/main`, PR head, Required Checks, and Rulesets before any future integration or administration change.
- Re-run rule discovery/fingerprints before each later change wave; absent analysis keys, incomplete discovery, or any uncertainty requires the full-read path.
- Treat the Ruleset IDs and actor/mode read-back above as the 2026-08-26 evidence snapshot; GitHub remains authoritative for current state.
- For future break-glass use, require an actual `INFRASTRUCTURE_UNAVAILABLE` classification and the complete evidence/recovery procedure. Never use it for `VALIDATION_FAILURE` or `UNKNOWN`.

## Remaining project work

- `WI-0001`: fresh-agent continuation validation.
- `WI-0002`: manifest hashes/cross-version installed provenance.
- `WI-0003`: evaluate packaged release artifact.
- `WI-0004`: optional adapter modules.

## Open constraints

- Early cross-PR preflight is a snapshot and cannot replace the final check against current `main`.
- The reference GitHub registry capability treats arrays as atomic merge values unless a project defines narrower safe semantics.
- The central v2 profile is not a high-frequency distributed database; projects with stronger service/database authorities should preserve them.
- GitHub repository-administration controls are outside ordinary Foundation file transfer and must not be silently changed in target repositories.
- Break-glass solves CI-service unavailability only; it cannot make GitHub Git/PR/API itself available during a broader GitHub outage.
- Persistent cache records do not persist semantic analyses; a cross-run fingerprint hit saves analysis only when the exact analysis object is independently available under its validated key.
