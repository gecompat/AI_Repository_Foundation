# MV-FND-001 — Fresh-AI rules transfer and continuation validation

Status: pending manual validation

## Objective

Verify that an AI system with no prior chat history can use only the Foundation repository plus a target repository to transfer the intended rules safely and then understand how to continue the target project.

## Contract / risk

Validate `foundation/manifest.json`, `foundation/AI_TRANSFER.md`, DEC-0001, DEC-0004, and the rule that Foundation-project artifacts must not leak into the target repository.

## Prerequisites

- a disposable test repository with its own non-sensitive `README.md` and its own license file;
- optionally an existing project-specific `AGENTS.md` to exercise semantic merge behavior;
- a fresh AI session/agent that has not received this development conversation;
- read access to this Foundation repository and write access to the disposable target.

Use synthetic/public test content only.

## Initial state

Record:

- Foundation commit/version;
- target repository commit;
- target files that already exist (`README.md`, `LICENSE`, `AGENTS.md`, adapter files);
- selected adapters.

## Steps

1. Give the fresh AI only the target repository, this Foundation repository, and the task: `Apply the AI Repository Foundation rules to the target repository. Follow the Foundation's own transfer instructions.`
   - Expected: the AI discovers `foundation/manifest.json` and `foundation/AI_TRANSFER.md`; it does not treat the Foundation root as a directory template.
2. Ask the AI to show its transfer plan before writing.
   - Expected: only manifest-listed core rules and selected adapters appear. Foundation `README.md`, `LICENSE`, `CHANGELOG.md`, `.gitignore`, `.ai/PROJECT_CONTEXT.md`, `.ai/PROJECT_STATUS.md`, `.ai/HANDOVER.md`, `.ai/BACKLOG.md`, `.ai/ROADMAP.md`, internal decisions, tests, and tools do not appear as target payload.
3. Apply the transfer.
   - Expected for an absent target file: create it at the manifest target path.
   - Expected for an identical rule: leave it unchanged.
   - Expected for an existing differing `AGENTS.md`: preserve project-specific content and merge only the marked Foundation bridge; do not replace the file wholesale.
4. Inspect the target `README.md` and root license.
   - Expected: both are byte-for-byte unchanged unless the separate test task explicitly requested an unrelated edit.
5. Ask the fresh AI to explain, using only the resulting target repository: project purpose, where Foundation rules live, which project-specific information has priority, how normal operations are authorized, when a gate is required, how model tiers are selected, and how manual validation is handled.
   - Expected: answers match the target repository and installed rules without requiring previous chat history.
6. If available, run from the Foundation checkout: `python tools/foundation_validator.py --target <TARGET> --adapters <SELECTED> --profile full`.
   - Expected: exit code 0 or only explicitly reviewed warnings for intentional local overrides.

## Pass criteria

- no Foundation-project artifact outside the manifest transfer set was introduced;
- target README and root license remained unchanged;
- existing project-specific instructions were preserved;
- the Foundation bridge is discoverable from root `AGENTS.md`;
- the fresh AI correctly identifies ordinary task-authorized operations as executable without repeated confirmation;
- privacy gating is based on classification/destination/handling authority, not merely real information;
- the fresh AI can continue project work without chat history;
- validator result meets step 6 expectations when executed.

## Fail criteria

Any payload leakage, silent overwrite, lost project instruction, replaced target license/README, repeated confirmation requirement for normal operations, missing privacy/authorization boundary, or dependence on prior chat context is a failure.

## Outputs to return

- Foundation commit SHA;
- target before/after commit or diff;
- AI transfer plan;
- list of created/merged/unchanged/conflicting files;
- validator command, exit code, and warnings/errors if run;
- the AI's continuation explanation;
- any deviation from expected behavior.

## Cleanup / recovery

Delete the disposable test repository or reset it to its recorded initial commit. Do not use a production or valuable repository for this test.

## Limitations and residual risk

Passing one fresh AI system does not prove identical discovery behavior for every vendor surface. Adapter-specific behavior remains subject to current vendor documentation and should be rechecked when an adapter changes.
