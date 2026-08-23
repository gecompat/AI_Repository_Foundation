# Repository Agent Contract

## Authority

This file is the canonical entry point. For repository work, apply instructions in this order:

1. platform and system safety constraints;
2. the current explicit task;
3. scoped repository instructions nearest the affected files;
4. this file and the authoritative documents listed in `.ai/repo_map.yaml`;
5. informative documents.

User or workspace prompts may add temporary constraints, but are not durable project truth. If instructions conflict, stop for material ambiguity; stricter safety, privacy, or authorization limits prevail.

## Required preflight

Before every file write, commit, push, export, package, upload, external transfer, or other mutation, apply the privacy stop-gate in `Documentation/Standards/DATA_PRIVACY_AND_CONFIDENTIALITY.md`. If real personal, user, customer, company, organization, environment, or proprietary internal information is present, possible, or cannot be ruled out, do not mutate or transfer anything; ask the user.

Then determine scope, authority, mutation class, relevant decisions, validation, and recovery.

## Canonical reading path

Read only what the task needs:

- context: `.ai/PROJECT_CONTEXT.md`
- project rules: `.ai/PROJECT_RULES.md`
- workflow and authorization: `.ai/WORKING_RULES.md`
- model/resource routing: `.ai/MODEL_ROUTING_POLICY.md`
- validation: `.ai/VALIDATION_POLICY.md`
- current truth: `.ai/PROJECT_STATUS.md`
- continuation: `.ai/HANDOVER.md`
- durable human-facing policies: `Documentation/Standards/`
- decisions: `Documentation/Architecture/DECISIONS.md`

Use `.ai/repo_map.yaml` for authority, coupling, and validation discovery.

## Non-negotiable rules

- The repository, not chat history or memory, is the durable source of truth.
- Never invent project facts, validation results, sources, permissions, secrets, or decisions.
- Never commit secrets or private/local runtime data.
- Use synthetic or explicitly redistributable examples by default.
- Do not make destructive, irreversible, costly, or external mutations without task authority and recovery analysis.
- Keep one coherent implementation scope under one owner; parallelize only independent, disjoint work.
- Do not duplicate governance in adapters.
- Do not silently make a material durable decision; record it or request approval according to project authority.
- Report `not executed`, `pending manual validation`, and `validated` truthfully.
- Keep documentation and project state consistent with the actual result.

## Completion

A change is complete only when its scoped requirements are implemented, relevant validation is executed or explicitly left pending, status/handover are updated when needed, and no known material conflict or privacy concern remains hidden.