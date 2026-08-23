# Working Rules

Status: AUTHORITATIVE

## Preflight

1. Apply the privacy stop-gate before any mutation or transfer.
2. Read the smallest authoritative scope needed.
3. Classify the action:
   - `READ-ONLY`
   - `LOCAL MUTATION`
   - `EXTERNAL MUTATION`
   - `DESTRUCTIVE / IRREVERSIBLE`
4. Confirm task authority, blast radius, recovery, cost, dependencies, and validation.
5. Identify existing local overrides and conflicts.

Read-only inspection is normally allowed within scope. Local and external mutations require the task to authorize the relevant outcome. Destructive/irreversible actions require explicit authorization, exact targets, recovery where possible, and a final confirmation when risk remains material.

## Implementation

- One responsible implementation owner per coherent scope.
- Parallel work only for independent, disjoint, separately validated areas.
- Prefer existing project functions and local tools.
- Do not introduce dependencies or services without the required review.
- No blind overwrite, semantic guessing, or unrelated refactoring.
- Retry only after changed input, artifacts, evidence, environment, or an explicit stability test.

## Git default

- `main` is stable.
- Use a feature branch and pull request unless the project documents another workflow.
- Use small coherent commits with factual messages.
- Do not force-push shared branches by default.
- Validate the relevant scope before merge, or document what remains pending.
- Never describe unexecuted checks as passed.

## Completion and handover

Review the stable diff, run the smallest sufficient checks followed by the completion gate, update factual status, record pending manual validation, and keep `.ai/HANDOVER.md` concise enough for a new contributor without chat history.