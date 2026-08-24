# Handover

Status: GENERATED/EVIDENCE

## Current state

The v1.5 candidate adds a machine-readable semantic upgrade-applicability layer on top of the existing transfer and semantic-integration model. Upgrading an older target no longer depends on an AI happening to notice a newly introduced Foundation policy.

`foundation/feature_catalog.json` is the source feature catalog. `Documentation/Standards/UPGRADE_APPLICABILITY_POLICY.md` requires a complete feature delta from the target's installed Foundation version to the exact source Foundation ref. Every feature introduced after the installed version, or materially changed after it, must be assessed exactly once as `NOT_APPLICABLE`, `ALREADY_EQUIVALENT`, `PROJECT_STRONGER`, `APPLY_DEFAULT`, `RECOMMENDED`, `DECISION_REQUIRED`, or `CONFLICT`.

Relevant `RECOMMENDED`, `DECISION_REQUIRED`, and `CONFLICT` outcomes must be surfaced explicitly. For persistent identity/nomenclature, the catalog contains durable-identifier applicability signals and directs an upgrade to recommend `ADOPT_FORWARD` when the target's existing convention is compatible but materially weaker. Historical renaming still requires explicit `MIGRATE_EXPLICIT` authority.

The catalog, upgrade policy, feature-catalog schema, and upgrade-assessment schema are Foundation core transfer payload. `tools/upgrade_applicability.py` computes candidate deltas deterministically. `tools/feature_catalog_guard.py` verifies catalog coverage and, in CI, requires a ruleset-version bump plus a feature-catalog review entry whenever transferable Foundation sources change.

The Foundation source project itself now follows the identity model it provides to targets. `DEC-0013` authorized `MIGRATE_EXPLICIT`: historical `FND-001`..`FND-012` are retained as aliases of preferred `WI-0001`..`WI-0012`; `WI-0013` is the semantic-upgrade work item. Existing `DEC-*` references remain preferred. `.ai/identity/registry.json` is the Foundation source project's Registration Authority state and is explicitly excluded from target transfer. `DEC-0014` records the semantic upgrade-applicability architecture decision.

Foundation CI run `32733817943` on implementation head `9e91cd21e3941a77cbb2e5a3abbf501c2d6a4788` completed successfully. It passed PowerShell runtime verification, transfer completeness/version consistency, semantic feature coverage/changed-source review, the Foundation validator, installation/transfer/feature-catalog/source-project-migration tests, and cross-language registration tests. WI-0013 is complete for its deterministic contract.

## Next actions

1. Confirm `Foundation CI` on the final evidence-only PR #10 head.
2. Merge PR #10 by squash only if that exact head is green.
3. Verify `origin/main` points to the resulting merge commit and that no feature branch remains.
4. Separately execute `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md` with a genuinely fresh AI session/test target when available; do not claim it as executed beforehand.
5. Complete WI-0001 only after that separate fresh-agent acceptance is recorded.

## Open constraints

- The semantic feature catalog makes feature-delta omission deterministic, but applicability classification still requires target-repository evidence. The catalog guides semantic assessment; it does not replace project judgment.
- `RECOMMENDED` is not implicit migration authority. Identifier history remains protected by `PRESERVE`/`ADOPT_FORWARD`/`MIGRATE_EXPLICIT` semantics.
- The changed-source guard requires catalog review for transferable-source changes, but a maintainer must still describe genuinely new/material behavior correctly in the catalog rather than using a false `NO_SEMANTIC_CHANGE` record.
- The local artifact registry is not a distributed database. Multi-user/network-concurrent targets should use an appropriate central Registration Authority.
- Manifest hashes/cross-version installed provenance remain pending under WI-0002; current guards address transfer completeness, semantic upgrade coverage, and version consistency rather than cryptographic installed-provenance tracking.
- Vendor adapter discovery behavior can change and must be rechecked against current primary documentation when adapters change.
