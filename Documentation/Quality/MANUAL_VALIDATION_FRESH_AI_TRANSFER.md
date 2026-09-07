# MV-FND-001 — Fresh-AI rules transfer and continuation validation

Status: validated

## Current evidence split

The existing-repository AI-transfer portion has been validated separately through successful AI-assisted Foundation integration in five existing repositories. See `Documentation/Quality/EXISTING_REPOSITORY_AI_TRANSFER_EVIDENCE.md`.

The stricter fresh-agent continuation criterion was executed on 2026-09-07: after transfer, a new persisted Codex CLI agent with no prior conversation context understood and continued a disposable synthetic target using repository state alone.

## Executed evidence — 2026-09-07

- Foundation source commit: `67edbccfbcb96d46a83ace160efc0015bdd3b27e`; ruleset `1.15.0`; portable manifest hash `77b818ade51bf080a3c3006b2bfdae0b2acd8aad200eec83a196ead5a1dfa137`.
- Disposable target initial commit: `3f4e592cb6775eeade5da928b41cc6a0f89be5ce`; synthetic ledger fixture with pre-existing `README.md`, `LICENSE`, `AGENTS.md`, `docs/PROJECT_RULES.md`, and `sample.csv`.
- Fresh-agent execution identifier: `01a07d2b-e2ef-77a0-b78c-d93fdb90c550`. The first turn received only the exact source/target locations, pinned source commit, transfer task, core-only selection, and read-only-plan constraint. Both working trees remained clean after that turn.
- Read-only plan: 57 `CREATE`, one `MERGE_REQUIRED` (`AGENTS.md`), zero conflicts, zero adapters, and zero optional capabilities. No Foundation project-only file was planned as target payload.
- Applied transfer: 57 source-identical core files plus one preserved semantic `AGENTS.md` merge. The original project rules/discovery text remained intact; the managed Foundation block was appended exactly once.
- Receipt: `foundation-installation-provenance/v1`, 58 selected files, 57 `FOUNDATION_BASELINE`, one reasoned `INTENTIONAL_OVERRIDE`, zero adapters/capabilities, and the exact source commit/manifest hash. It contained no target content, prompt, response, credential, or absolute host path.
- Full installed-target validator: exit `0`, `info=62`, `warning=0`, `error=0`, `blocking=0`; observed drift classes were 57 `UNCHANGED_CURRENT_BASELINE`, one `INTENTIONAL_OVERRIDE`, zero `PREVIOUS_FOUNDATION_VERSION`, and zero `UNKNOWN_DRIFT`.
- Independent target checks: root discovery passed; the synthetic CSV contract passed with columns `account,debit,credit`, two rows, and debit/credit totals of 10; `README.md`, `LICENSE`, `docs/PROJECT_RULES.md`, and `sample.csv` matched their initial commit bytes; `git diff --check` passed.
- Continuation explanation: the fresh agent correctly described target purpose, rule locations/precedence, normal-operation authority, additional gates, tier semantics, manual model-selection fallback, all four drift classifications, and the distinction between Foundation integrity and still-pending target manual validation.
- The Foundation source remained clean and unchanged. The disposable target was not committed.

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

- exact Foundation commit/version and portable source-manifest hash;
- target repository commit;
- target files that already exist (`README.md`, `LICENSE`, `AGENTS.md`, adapter files);
- selected adapters.

## Steps

1. Give the fresh AI only the target repository, this Foundation repository, and the task: `Apply the AI Repository Foundation rules to the target repository. Follow the Foundation's own transfer instructions.`
   - Expected: the AI discovers `foundation/manifest.json` and `foundation/AI_TRANSFER.md`; it does not treat the Foundation root as a directory template.
2. Ask the AI to show its transfer plan before writing.
   - Expected: only manifest-listed core rules and selected adapters appear as copied/merged payload. The generated namespaced installation-provenance receipt is planned separately. Foundation `README.md`, `LICENSE`, `CHANGELOG.md`, `.gitignore`, `.ai/PROJECT_CONTEXT.md`, `.ai/PROJECT_STATUS.md`, `.ai/HANDOVER.md`, `.ai/BACKLOG.md`, `.ai/ROADMAP.md`, internal decisions, tests, and tools do not appear as target payload.
3. Apply the transfer.
   - Expected for an absent target file: create it at the manifest target path.
   - Expected for an identical rule: leave it unchanged.
   - Expected for an existing differing `AGENTS.md`: preserve project-specific content and merge only the marked Foundation bridge; do not replace the file wholesale.
4. Inspect the target `README.md` and root license.
   - Expected: both are byte-for-byte unchanged unless the separate test task explicitly requested an unrelated edit.
5. Inspect `.ai/foundation/installation-provenance.json`.
   - Expected: it conforms to `foundation-installation-provenance/v1`, identifies the exact source version/commit/manifest hash, contains every selected target once, records the preserved target `AGENTS.md` merge as an explicitly reasoned `INTENTIONAL_OVERRIDE`, and contains no prompt, response, credential, target content, or absolute host path.
6. Ask the fresh AI to explain, using only the resulting target repository: project purpose, where Foundation rules live, which project-specific information has priority, how normal operations are authorized, when a gate is required, how model tiers are selected, how installed drift is classified, and how manual validation is handled.
   - Expected: answers match the target repository and installed rules without requiring previous chat history.
7. If available, run from the Foundation checkout: `python tools/foundation_validator.py --target <TARGET> --adapters <SELECTED> --profile full`.
   - Expected: exit code 0; the merged target entrypoint is classified `INTENTIONAL_OVERRIDE`, unmodified selected files are `UNCHANGED_CURRENT_BASELINE`, and no result is mistaken for `UNKNOWN_DRIFT`. A legacy compatibility umbrella may additionally appear for namespaced Foundation drift where that older diagnostic applies.

## Pass criteria

- no Foundation-project artifact outside the manifest transfer set and the contract-defined generated installation receipt was introduced;
- target README and root license remained unchanged;
- existing project-specific instructions were preserved;
- the Foundation bridge is discoverable from root `AGENTS.md`;
- the fresh AI correctly identifies ordinary task-authorized operations as executable without repeated confirmation;
- privacy gating is based on classification/destination/handling authority, not merely real information;
- the fresh AI can continue project work without chat history;
- source and installed hashes are reconciled without classifying intentional or previous-version state from missing evidence;
- validator result meets step 6 expectations when executed.

## Fail criteria

Any payload leakage, silent overwrite, lost project instruction, replaced target license/README, repeated confirmation requirement for normal operations, missing privacy/authorization boundary, or dependence on prior chat context is a failure.

## Outputs to return

- Foundation commit SHA;
- target before/after commit or diff;
- AI transfer plan;
- list of created/merged/unchanged/conflicting files;
- installation receipt and drift-classification summary;
- validator command, exit code, and warnings/errors if run;
- the AI's continuation explanation;
- any deviation from expected behavior.

## Cleanup / recovery

Delete the disposable test repository or reset it to its recorded initial commit. Do not use a production or valuable repository for this test.

## Limitations and residual risk

Passing one fresh AI system does not prove identical discovery behavior for every vendor surface. Adapter-specific behavior remains subject to current vendor documentation and should be rechecked when an adapter changes.
