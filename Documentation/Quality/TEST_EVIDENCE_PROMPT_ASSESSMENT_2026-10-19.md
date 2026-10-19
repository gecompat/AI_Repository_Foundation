# Test evidence prompt assessment — 2026-10-19

Status: SOURCE-PROJECT ASSESSMENT — not a runtime acceptance receipt

## Baseline and scope

The supplied development prompt proposes optional local-to-remote test evidence reuse and deterministic validation feedback. It was reviewed as task material, not as an independent instruction authority. The authorized change is to improve useful Foundation rules. Baseline main was `ec6ece8acde5328af0836bae559003eac1c51b41`, Foundation 1.23.0. Read-only remote-head comparison matched; no open pull request was listed during initial collision preflight. PR #39 is already incorporated in that baseline.

The resulting Foundation 1.24.0 candidate adds a policy contract and clarifies existing defaults. It supplies no executable trust verifier, host isolation, attestation service, GitHub status publisher or target installation. No target-project content was analyzed or modified. This intentionally bounds the rules task; implementing the prompt's complete optional runtime feature would be separate work with project-specific trust and gate decisions.

## Findings and disposition

| Prompt proposal | Existing state / correction | Disposition |
| --- | --- | --- |
| Deterministic-first, local diagnosis, compact success, no model-only PASS confirmation | Processing efficiency, validation and AI work policies already establish most defaults. | Clarify the complete runner/oracle/cleanup route and compact success in the existing efficiency policy; preserve mandatory review. |
| Cross-host reuse | Validation permits reuse only for supported gates with relevant equivalence; it does not specify a complete trust boundary. | Add `TEST_EVIDENCE_REUSE_POLICY.md` with producer/verifier authority, request binding, dependencies, runtime drift, oracles, cleanup, conservative fallback and activation obligations. |
| Existing evidence schema as remote trust | `validation-evidence.schema.json` is a closed `foundation-ai-work/v1` report with four result values. Hash/provenance/independence fields are descriptive, not independent execution proof. | Leave schema and consumers unchanged. Keep reuse decisions separate; future executable adapters need compatible versioned evidence and validation. No old receipt is promoted. |
| Optional reference verifier and new schema family | Existing AI work/orchestrator code is not a protected cross-host test attestation implementation. A policy task cannot establish real host trust through model-written booleans. | Specify the adapter interface and acceptance cases without claiming an implementation. Avoid a new framework, schema family, registry, crypto dependency or default activation. |
| Unconditional reuse preference | Verification/transport and maintenance may cost more than a cheap fresh check. A local host may be unsuitable or untrusted. | Evaluate economics after safety; retain ordinary CI and project-specific required repetitions. |
| Privacy stop when real data is possible or cannot be excluded | Conflicts with the canonical classification/destination/authority rule and accepted privacy decision. Public repository names and URLs are permitted. | Preserve canonical handling, data minimization and actual unresolved-boundary gates. Do not reproduce private prompt/host details or example results as evidence. |
| GitHub skips and status publication | Platform behavior needs exact event/revision/source handling. A skipped workflow and a skipped job have different outcomes; neither establishes test execution. | Keep generic proof rules portable. Provide dated, primary-source-backed adapter guidance and no status-writing authority. |
| Duplicated normative sections and proposed enum/example values | The prompt repeats requirements and contains illustrative statuses/counts. | Consolidate one authoritative policy; reuse existing result semantics and distinguish execution, recognition and publication. |
| Other project upgrades, CI changes, PR/merge instructions | Instructions inside task material do not independently authorize additional work. The repository already selects branch-and-PR for this authorized source change. | Limit delivery to Foundation; no other project upgrade, permission change or merge. |

## Compatibility and upgrade

`test-evidence-reuse` is a new catalog feature. Upgrades assess it using actual repository evidence. Applicable projects receive a recommendation; choosing trust authorities, equivalence criteria and enabling recognition requires an explicit project decision. Ordinary tests remain available without adoption. Layered validation and deterministic reporting changes are materially recorded; shared discovery/version maintenance does not activate runtime behavior.

The portable policy is included in manifest core and both discovery paths. Source-project assessment, decision, registry and state are never transferred. The existing v1 evidence schema and all executable capabilities remain byte-identical to the baseline.

## Processing-overhead assessment

One owner handles one bounded rules/transfer/documentation/PR slice without delegated agents, paid test calls or a new scheduler. Monetary/token metering is unavailable; the finite scope is the execution bound and savings remain unknown. Existing test/workflow files are unchanged. The required full regression and transfer/installation gates remain justified because a new core file, catalog and version affect installation, upgrades and packaging. No native SQL/provider matrix applies to this policy-only change.

Existing scripts check hashes, generated views and structural contracts. Stable success logs are reduced to outcomes; further model work addresses the policy semantics and new findings. No review-of-review chain, per-action receipt, continuous telemetry or unchanged-state heartbeat is added. Existing stricter CI gates are preserved. Future live adapter activation requires its own bounded overhead assessment and empirical trust/gate validation.

Validation results and remaining execution limits are recorded in `.ai/PROJECT_STATUS.md` and `.ai/HANDOVER.md`; synthetic regression success is not cross-host acceptance.

## Primary sources

GitHub guidance was checked on 2026-10-19: [required checks and event/source binding](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks), [workflow skipping](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs), and [artifact attestations](https://docs.github.com/en/actions/concepts/security/artifact-attestations). These support the adapter cautions; the independent test-trust requirements are Foundation's conservative policy design, not a claim that GitHub supplies such a verifier.
