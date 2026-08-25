# GitHub Branch Protection for the Foundation Source Repository

Status: AUTHORITATIVE PROJECT OPERATIONS

## Scope

This document describes the GitHub repository-administration state required for the **AI Repository Foundation source repository itself**. It is not transferred to target repositories and is not a Foundation-wide requirement for every adopting project.

Repository: `gecompat/AI_Repository_Foundation`
Protected branch: `main`

## Required source-project state

The Foundation source repository requires server-side protection for `main` so that the semantic registry checks cannot be bypassed merely because the workflow files exist.

Required settings:

- branch protection enabled for `main`;
- pull request required before merging;
- no mandatory human approval for this single-maintainer repository;
- required status checks enabled and strict/up-to-date;
- required checks:
  - `validate` from the `Foundation CI` workflow;
  - `registry-integrity` from the `Foundation Artifact Registry` workflow;
- administrator/bypass enforcement enabled;
- linear history required;
- force pushes disabled;
- branch deletion disabled.

The two workflow files are necessary but not sufficient. Server-side branch protection/ruleset configuration is a separate repository-administration control.

## Current verified state

Verified on 2026-08-25.

GitHub's branch metadata reports:

- `main` is protected (`protected: true`);
- required-status-check enforcement level is `everyone`;
- required checks are `registry-integrity` and `validate`.

The saved GitHub branch-protection rule was also reviewed in the repository UI and confirms:

- branch pattern `main`;
- pull request required before merge;
- approvals not required;
- required status checks enabled;
- branch must be up to date before merge;
- `registry-integrity` and `validate` selected as required GitHub Actions checks;
- linear history required;
- bypass of the above settings disabled, including administrators;
- force pushes disabled;
- branch deletion disabled;
- conversation resolution, signed commits, deployments, and branch locking not required.

This satisfies the source-project protection requirement defined by `WI-0015` and `DEC-0016`.

## Automated configuration helper

A repository administrator may reproduce or verify the intended state with:

```bash
export GITHUB_ADMIN_TOKEN="..."
python tools/github/configure_branch_protection.py
```

The token must have repository `Administration: write`. The helper reads the token only from the named environment variable, configures the required state, then reads GitHub back and verifies the effective protection.

Verification without mutation:

```bash
export GITHUB_ADMIN_TOKEN="..."
python tools/github/configure_branch_protection.py --verify-only
```

Do not commit, log, or paste the token into repository files, command arguments, issues, PRs, or chat.

## Manual GitHub configuration

Equivalent configuration can be applied in GitHub repository settings under branch protection/rulesets for `main`:

1. require a pull request before merging but do not require human approvals unless project governance changes;
2. require the relevant status checks before updating `main`;
3. select `Foundation CI / validate` and `Foundation Artifact Registry / registry-integrity`;
4. require the branch to be up to date before merge;
5. apply enforcement to administrators/bypass-capable maintainers;
6. require linear history;
7. prohibit force pushes and branch deletion.

After configuration, verify with GitHub rather than relying only on documentation.

## Target-project distinction

When Foundation is transferred into another repository, including when the optional `artifact-registry-github` capability is selected, server-side GitHub protection is **recommended hardening, not a Foundation-required target invariant**.

The transfer process must explicitly tell the target that:

- installing workflow files does not make checks required on GitHub;
- branch protection/rulesets are configured separately in repository administration;
- enabling the semantic registry checks as required status checks is recommended when the target wants hard merge enforcement;
- the target project decides whether to enable that administration setting;
- absence of the setting alone does not fail `FOUNDATION_INTEGRITY` and must not be silently configured without project authority.
