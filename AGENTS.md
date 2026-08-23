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
5. identify relevant decisions, validation, dependencies, and recovery needs.

A concrete task authorizes the ordinary, reasonably expected, proportionate operations needed to complete it. Do not request repeated confirmation for normal operations inside that envelope. Stop only when classification or handling authority is unresolved, the action materially exceeds the envelope, a destructive/irreversible target is not explicitly authorized, or another explicit project/platform gate applies.

## Canonical reading path

- Foundation-project context: `.ai/PROJECT_CONTEXT.md`
- Foundation-project rules: `.ai/PROJECT_RULES.md`
- workflow and authorization: `.ai/WORKING_RULES.md`
- model/resource routing: `.ai/MODEL_ROUTING_POLICY.md`
- validation: `.ai/VALIDATION_POLICY.md`
- Foundation-project state: `.ai/PROJECT_STATUS.md`
- continuation: `.ai/HANDOVER.md`
- durable policies: `Documentation/Standards/`
- decisions: `Documentation/Architecture/DECISIONS.md`
- transferable rules: `foundation/manifest.json`
- direct AI transfer protocol: `foundation/AI_TRANSFER.md`

Use `.ai/repo_map.yaml` for authority and discovery. The transfer manifest, not repository traversal, defines what may be installed into another repository.

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
- Never copy Foundation-project state, README, LICENSE, changelog, backlog, handover, status, or internal decisions into a target repository. Transfer only manifest-listed rules.

## Completion

A change is complete when its scoped requirements are implemented, relevant validation is executed or explicitly left pending, factual state/handover is updated when needed, and no known material conflict, privacy boundary, or authorization ambiguity remains hidden.
