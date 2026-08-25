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
- required status checks enabled and strict/up-to-date;
- required checks:
  - `validate` from the `Foundation CI` workflow;
  - `registry-integrity` from the `Foundation Artifact Registry` workflow;
- administrator enforcement enabled;
- linear history required;
- force pushes disabled;
- branch deletion disabled.

The two workflow files are necessary but not sufficient. A workflow can report a failing check while an unprotected branch may still be merged or pushed by a user with sufficient repository rights. Server-side branch protection/ruleset configuration is therefore a separate repository-administration control.

## Current state

At the time this requirement was recorded, GitHub reported `main` as `protected: false` with required-status-check enforcement `off`. The current ChatGPT GitHub connector exposes repository content, PR, branch, and Actions operations but no branch-protection/ruleset mutation; the execution environment also has no independent GitHub administration token. Therefore the desired server-side setting cannot be activated from this session and must remain explicitly tracked until a repository administrator applies it.

Do not mark the protection requirement satisfied until GitHub itself reports the configured protection and the required checks.

## Automated configuration helper

A repository administrator may run:

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

1. require the relevant status checks before updating `main`;
2. select the checks produced by `Foundation CI / validate` and `Foundation Artifact Registry / registry-integrity`;
3. require the branch to be up to date before merge;
4. apply enforcement to administrators/bypass-capable maintainers where the GitHub plan/UI permits it;
5. require linear history;
6. prohibit force pushes and branch deletion.

After configuration, verify with GitHub rather than relying only on documentation.

## Target-project distinction

When Foundation is transferred into another repository, including when the optional `artifact-registry-github` capability is selected, server-side GitHub protection is **recommended hardening, not a Foundation-required target invariant**.

The transfer process must explicitly tell the target that:

- installing workflow files does not make checks required on GitHub;
- branch protection/rulesets are configured separately in repository administration;
- enabling the semantic registry checks as required status checks is recommended when the target wants hard merge enforcement;
- the target project decides whether to enable that administration setting;
- absence of the setting alone does not fail `FOUNDATION_INTEGRITY` and must not be silently configured without project authority.
