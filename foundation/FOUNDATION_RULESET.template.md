# AI Repository Foundation Ruleset

Status: AUTHORITATIVE BASELINE
Ruleset version: 1.1.2

This directory contains reusable governance rules plus the source-license notice required for transferred Foundation material. It does not describe the Foundation source project and does not define the target project's README, root license, architecture, backlog, status, or release state.

## Rule classes

- `REQUIRED`: baseline safety, privacy, integrity, evidence, and authorization behavior that may not be silently weakened.
- `DEFAULT`: applies unless an intentional project-specific override exists.
- `PROJECT_SELECTABLE`: must be selected by the project when relevant.

## Read by scope

- project/baseline rules: `PROJECT_RULES.md`
- authorization and working behavior: `WORKING_RULES.md`
- model/resource selection: `MODEL_ROUTING_POLICY.md`
- validation and manual test plans: `VALIDATION_POLICY.md`
- data handling: `DATA_PRIVACY_AND_CONFIDENTIALITY.md`
- safe operations: `SECURITY_AND_SAFE_OPERATIONS.md`
- documentation truth: `DOCUMENTATION_POLICY.md`
- third-party/licensing: `THIRD_PARTY_AND_LICENSING.md`
- evidence/sources: `SOURCE_AND_EVIDENCE_POLICY.md`
- dependencies/services: `DEPENDENCY_POLICY.md`
- machine-readable authority and validation-scope index: `repo_map.yaml`

## Validation boundary

Foundation validation supplements rather than replaces the target repository's validation system. The Foundation validator covers `FOUNDATION_INTEGRITY` only. Project-specific semantic correctness remains under `PROJECT_SEMANTIC`; executable/empirical behavior remains under `RUNTIME_EMPIRICAL`. Existing project validators, static contracts, tests, reviews, and manual validation remain authoritative for those scopes when affected.

A local override or drift warning identifies a difference; it is not semantic approval of that difference. A green Foundation validator must never be used as evidence that the entire target project is validated.

## Provenance and license notice

`AI_REPOSITORY_FOUNDATION_NOTICE.md` is not a target-project license. It preserves the MIT notice for the Foundation material copied into this repository. Keep that notice with the installed Foundation rules; do not use it to replace or reinterpret the target project's own root license.

Read only the rules relevant to the current task. Repository-specific instructions and facts remain in the target repository; these Foundation files are a reusable baseline, not a replacement for project context.
