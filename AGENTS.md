# Repository Agent Contract

## Authority

This file is the canonical entry point for work on the Foundation repository itself. Apply instructions in this order:

1. platform and system constraints;
2. the current explicit task;
3. scoped repository instructions nearest the affected files;
4. this file and the authoritative documents listed in `.ai/repo_map.yaml`;
5. informative documents.

User or workspace prompts may add temporary constraints, but are not durable project truth. If a material conflict remains unresolved, stop only for that conflict; do not turn ordinary work into a confirmation loop.

## Required preflight

Before mutation or transfer:

1. read only the authoritative scope required for the task;
2. classify relevant data and its intended destination under `Documentation/Standards/DATA_PRIVACY_AND_CONFIDENTIALITY.md`;
3. determine the authorization envelope from the current task, project rules, configured scope, environment, and budget;
4. classify the operation under `Documentation/Standards/SECURITY_AND_SAFE_OPERATIONS.md`;
5. identify relevant decisions, validation, dependencies, recovery needs, and whether the change adds or changes reusable Foundation material;
6. for durable Foundation planning/governance artifacts, read `.ai/identity/registry.json` as the canonical planning state and allocate/modify through the v2 registry contract rather than editing `.ai/BACKLOG.md` independently.

A concrete task authorizes the ordinary, reasonably expected, proportionate operations needed to complete it. Do not request repeated confirmation for normal operations inside that envelope. Stop only when classification or handling authority is unresolved, the action materially exceeds the envelope, a destructive/irreversible target is not explicitly authorized, or another explicit project/platform gate applies.

## Canonical reading path

- Foundation-project context: `.ai/PROJECT_CONTEXT.md`
- Foundation-project rules: `.ai/PROJECT_RULES.md`
- workflow and authorization: `.ai/WORKING_RULES.md`
- model/resource routing: `.ai/MODEL_ROUTING_POLICY.md`
- validation: `.ai/VALIDATION_POLICY.md`
- Foundation-project planning/identity authority: `.ai/identity/registry.json`
- generated backlog projection: `.ai/BACKLOG.md`
- Foundation-project state: `.ai/PROJECT_STATUS.md`
- continuation: `.ai/HANDOVER.md`
- durable policies: `Documentation/Standards/`
- decisions: `Documentation/Architecture/DECISIONS.md`
- transferable rules/capabilities and version authority: `foundation/manifest.json`
- direct AI transfer protocol: `foundation/AI_TRANSFER.md`
- transfer completeness guard: `tools/transfer_manifest_guard.py`
- central registry semantic tool: `foundation/capabilities/artifact-registry-github/registry_semantic.py`

Use `.ai/repo_map.yaml` for authority and discovery. The transfer manifest, not repository traversal, defines what may be installed into another repository.

## Foundation source-project planning invariant

The Foundation source project uses `foundation-artifact-registry/v2` at `.ai/identity/registry.json`.

- The registry is the canonical planning/identity state for `WI-*`, `DEC-*`, and future registered artifact kinds.
- `.ai/BACKLOG.md` is generated from the registry and must not be edited as an independent source of truth.
- `next_sequence` is not stored. Derive the next reference from the maximum canonical sequence for the prefix plus live reservations known to the Registration Authority.
- Do not store a second mutable global registry revision counter; Git state is the concurrency token for this repository.
- Preserve every registered or retired canonical reference and UID; never delete/reassign them to make numbering contiguous.
- For pull-request changes to the registry, object-level three-way merge and semantic integrity are authoritative. A textually clean Git merge is insufficient unless its parsed result equals the semantic merge result.
- Check other open pull requests early for human-reference, UID, alias, or overlapping-artifact collisions; re-check against current `main` at merge time.

## Transfer-plane invariant

A Foundation feature is not complete merely because code, documentation, or tests exist in this source repository.

- `foundation/manifest.json#ruleset_version` is the single Foundation ruleset-version authority; files that mirror that version must agree with it.
- Any new or changed reusable policy, schema, adapter, or optional capability must be classified in `foundation/manifest.json` in the same coherent change.
- New reusable policies belong under `Documentation/Standards/`; every managed policy there must be present in manifest `core`.
- New reusable schemas belong under `foundation/schemas/`; every managed schema there must be present in manifest `core`.
- New optional capability payloads belong under `foundation/capabilities/<capability>/`; every payload file must be present in the matching manifest `capabilities` entry. Existing explicitly registered legacy capability roots remain allowed only while declared by the manifest coverage contract.
- Do not mark a reusable feature complete until transfer completeness, semantic feature coverage, central-registry checks when affected, Foundation validation, installation tests, and relevant capability tests are green.
- A stale installed target ruleset does not define current source capability availability. For source/upgrade questions, read `foundation/manifest.json` from the exact Foundation ref being evaluated.

## Non-negotiable rules

- Repository state, not chat history or memory, is durable project truth.
- Never invent facts, validation, sources, permissions, secrets, or decisions.
- Never version secrets or private local runtime state.
- Real public or repository-intended information is not automatically confidential; classify data according to policy.
- Normal task-authorized operations do not require additional confirmation merely because they mutate local or external state.
- Do not silently exceed scope, budget, environment, or authorization boundaries.
- Keep one coherent implementation scope under one owner; parallelize only independent work.
- Do not duplicate governance in tool adapters.
- Do not silently make an unresolved durable material decision; record it according to project authority.
- Report `not executed`, `pending manual validation`, and `validated` truthfully.
- Never copy Foundation-project state, README, LICENSE, changelog, backlog, handover, status, identity registry, or internal decisions into a target repository. Transfer only manifest-listed rules/capabilities and required provenance.

## Completion

A change is complete when its scoped requirements are implemented, reusable material is correctly represented in the transfer manifest and feature catalog, transfer/version completeness is green, central-registry and generated-view checks are green when affected, relevant validation is executed or explicitly left pending, factual state/handover is updated when needed, and no known material conflict, privacy boundary, or authorization ambiguity remains hidden.
