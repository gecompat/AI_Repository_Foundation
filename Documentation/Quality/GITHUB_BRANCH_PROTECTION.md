# GitHub Protection for the Foundation Source Repository

Status: AUTHORITATIVE PROJECT OPERATIONS

## Scope

This document describes the GitHub repository-administration state required for the **AI Repository Foundation source repository itself**. It is not transferred to target repositories and is not a universal Foundation requirement for every adopting project.

Repository: `gecompat/AI_Repository_Foundation`
Protected branch: `main`

## Protection objectives

The source repository must provide both:

1. strong normal-mode integrity: PR-only integration, strict required checks, linear history, no force push, no deletion;
2. controlled continuity when GitHub Actions infrastructure is unavailable, without allowing a known validation failure to be bypassed.

The authoritative break-glass procedure is `Documentation/Quality/GITHUB_BREAK_GLASS.md`. `DEC-0017` records the architecture decision.

## Required source-project state

Use two layered **branch Rulesets** targeting `main`.

### `foundation-main-core-safety`

Active, with **no bypass actors**:

- require a pull request before merging;
- required approvals: 0 for the current single-maintainer model;
- require linear history;
- block force pushes (`non_fast_forward`);
- restrict branch deletion (`deletion`).

These controls remain active during every break-glass event. In particular, direct push to `main` is not an emergency path.

### `foundation-main-ci-gates`

Active:

- required check `validate` from `Foundation CI`;
- required check `registry-integrity` from `Foundation Artifact Registry`;
- strict/up-to-date required status checks;
- bypass actor limited to the authorized source maintainer;
- bypass mode **For pull requests only** (`pull_request`).

The CI bypass is used only for `INFRASTRUCTURE_UNAVAILABLE` according to `REPOSITORY_CONTINUITY_POLICY.md` and `GITHUB_BREAK_GLASS.md`. A check that ran and failed substantively is not bypassable under this policy.

## Current verified server state

Verified by authenticated GitHub API read-back on 2026-08-26:

- `foundation-main-core-safety` is active as Ruleset `21588442`, targets only `refs/heads/main`, has no bypass actors, requires a pull request with zero mandatory approvals and linear history, and blocks non-fast-forward updates and deletion;
- `foundation-main-ci-gates` is active as Ruleset `21588444`, targets only `refs/heads/main`, requires strict/up-to-date `validate` and `registry-integrity`, and has exactly user `48807214` with bypass mode `pull_request`;
- GitHub reports the current user's CI bypass as `pull_requests_only` and the core-safety bypass as `never`;
- the effective rules for `main` are the union of the CI status checks and the unbypassable pull-request, linear-history, non-fast-forward, and deletion rules;
- the legacy classic branch-protection endpoint returns HTTP 404 after the Rulesets were verified, while branch metadata still reports `main` as protected.

The migration tool created and read back both Rulesets before deleting classic protection and read both Rulesets back again afterward. This satisfies WI-0017's server-administration acceptance criterion.

## Migration from classic branch protection

The previously verified state used classic branch protection with required checks enforced for everyone and administrator bypass disabled. That state protects integrity but cannot provide the narrow PR-only CI escape hatch required for repository continuity.

Migration order is fail-safe:

1. create/update `foundation-main-core-safety`;
2. create/update `foundation-main-ci-gates` with PR-only bypass;
3. read back and verify both Rulesets;
4. only then remove the legacy classic branch protection;
5. read back the two Rulesets again.

Never remove classic protection first.

`tools/github/configure_rulesets.py` implements this order with a token that has repository `Administration: write`.

```bash
export GITHUB_ADMIN_TOKEN="..."
python tools/github/configure_rulesets.py
```

Verification only:

```bash
export GITHUB_ADMIN_TOKEN="..."
python tools/github/configure_rulesets.py --verify-only
```

To stage Rulesets while deliberately retaining classic protection:

```bash
python tools/github/configure_rulesets.py --keep-classic-protection
```

Do not commit, log, or paste the token into repository files, command arguments, issues, PRs, or chat.

## Manual GitHub configuration

Equivalent configuration can be created under repository **Settings → Rules → Rulesets**:

1. create branch Ruleset `foundation-main-core-safety`, target `main`, Active;
2. leave its bypass list empty;
3. enable Require a pull request, 0 approvals, Require linear history, Restrict deletions, and Block force pushes;
4. create branch Ruleset `foundation-main-ci-gates`, target `main`, Active;
5. require `validate` and `registry-integrity` and require the branch to be up to date;
6. add only the authorized source maintainer to its bypass list and change bypass mode from `Always allow` to **For pull requests only**;
7. verify both Rulesets are effective;
8. remove the old classic Branch protection rule for `main` only after verification.

## Normal and break-glass behavior

Normal PR:

```text
PR → validate + registry-integrity → merge
```

Actions infrastructure outage:

```text
PR → classify INFRASTRUCTURE_UNAVAILABLE
   → run available local deterministic checks
   → record BREAK-GLASS evidence in PR
   → bypass CI Ruleset for this PR only
   → core-safety Ruleset still applies
   → merge
   → rerun deferred checks after recovery
```

Known red validation:

```text
VALIDATION_FAILURE → no bypass → fix the defect
```

## Target-project distinction

When Foundation is transferred into another repository, including when the optional `artifact-registry-github` capability is selected, server-side protection and break-glass configuration are **recommended project administration**, not a Foundation-required target invariant.

The transfer process must explicitly tell the target that:

- workflow files do not make checks required on GitHub;
- making CI mandatory can create an availability dependency on the CI provider;
- a project that requires continuity should consider separating unbypassable core branch safety from PR-only bypassable CI gates;
- infrastructure unavailability may justify break-glass, while a substantive failed check does not;
- the target chooses bypass actors and outage evidence thresholds;
- Foundation installation must not silently create Rulesets, bypass permissions, or change repository administration;
- absence of such repository administration does not by itself fail `FOUNDATION_INTEGRITY`.
