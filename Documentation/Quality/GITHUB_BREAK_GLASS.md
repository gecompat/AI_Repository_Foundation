# GitHub Break-Glass Continuity for the Foundation Source Repository

Status: AUTHORITATIVE PROJECT OPERATIONS

## Purpose

`origin/main` is both the protected integration branch and a durable coordination channel for humans and AI agents. Required GitHub Actions checks protect integrity, but the Actions service must not become a complete availability single point of failure for repository coordination.

The Foundation source repository therefore uses a controlled break-glass model for **CI infrastructure unavailability only**.

## Normal mode

Normal merges to `main` require:

- a pull request;
- current/up-to-date target branch validation;
- `validate` (`Foundation CI`) successful;
- `registry-integrity` (`Foundation Artifact Registry`) successful;
- linear history;
- no force push;
- no protected-branch deletion.

## Break-glass classification

Before any bypass, classify the required check:

- `VALIDATION_FAILURE`: the check ran and reported a substantive failure. **Bypass prohibited.**
- `INFRASTRUCTURE_UNAVAILABLE`: GitHub Actions/runners/platform cannot produce a trustworthy check result because the service is unavailable or materially degraded. **Bypass permitted** when the remaining requirements below are met.
- `UNKNOWN`: cause not established. **Bypass prohibited** until classified.

A failing unit test, schema failure, registry collision, semantic merge conflict, or project timeout caused by code/configuration is `VALIDATION_FAILURE`, even during a wider GitHub incident.

## Required GitHub ruleset architecture

Classic branch protection is replaced by two layered branch Rulesets targeting `main`.

### `foundation-main-core-safety`

Active, no bypass actors:

- require pull request before merge;
- required approvals: 0;
- require linear history;
- block force pushes (`non_fast_forward`);
- restrict deletion (`deletion`).

This ruleset is never bypassed during an Actions outage. Direct pushes to `main` therefore remain disallowed.

### `foundation-main-ci-gates`

Active:

- require status check `validate`;
- require status check `registry-integrity`;
- require strict/up-to-date status checks;
- bypass actor: the authorized source maintainer;
- bypass mode: **For pull requests only** (`pull_request`).

This isolates the availability escape hatch to CI gates while preserving PR/audit/core branch safety.

## Break-glass procedure

1. Keep/open a normal PR. Never direct-push to `main`.
2. Establish evidence that the blocked required check is `INFRASTRUCTURE_UNAVAILABLE`, not a substantive test failure.
3. Run all reasonably reproducible local deterministic checks. For the Foundation this includes, when locally executable:
   - `python tools/transfer_manifest_guard.py`
   - `python tools/feature_catalog_guard.py`
   - `python foundation/capabilities/artifact-registry-github/registry_semantic.py validate --registry .ai/identity/registry.json`
   - generated-backlog consistency
   - `python tools/foundation_validator.py --profile full`
   - `python -m unittest discover -s tests -v`
4. Add a `BREAK-GLASS` section to the PR conversation containing:
   - incident/outage evidence;
   - blocked checks;
   - immutable PR head/base SHAs;
   - local/manual checks and results;
   - checks that could not be reproduced;
   - residual risk;
   - explicit statement that deferred GitHub validation must run after recovery.
5. Use the GitHub Ruleset bypass on the **pull request only** and merge using the normal linear merge method.
6. After GitHub Actions recovers, run the previously bypassed checks against the merged revision or an equivalent immutable revision and record the result.
7. If deferred validation fails, immediately create corrective/incident work and restore a known-good state or merge the correction.

## Prohibited uses

Break-glass MUST NOT be used to:

- merge a known red `validate` or `registry-integrity` result;
- bypass a semantic registry conflict;
- hide a flaky or slow project test by calling it infrastructure;
- avoid fixing a project-owned workflow/configuration defect;
- direct-push to `main`;
- force-push or delete `main`;
- fabricate successful status checks.

## Current migration

The repository historically used classic branch protection with administrator bypass disabled. That configuration provides integrity but cannot express the required PR-only CI bypass. The target source-project state is therefore layered Rulesets as described above.

`tools/github/configure_rulesets.py` can create/verify the two Rulesets and remove the legacy classic branch protection only after both Rulesets have been verified. Repository `Administration: write` is required.

Do not remove classic protection manually until both active Rulesets are present and verified; otherwise `main` may temporarily lose required safeguards.

## Target projects

When Foundation is transferred to another GitHub repository, this architecture is a **recommendation**, not a mandatory Foundation integration invariant. The target decides whether it needs break-glass continuity, which actors may bypass, the outage evidence threshold, and which local checks are required. Foundation transfer must never silently create bypass permissions or repository Rulesets.
