# AI work self-hosting evidence

Status: RUNTIME EMPIRICAL EVIDENCE

## Scope

`WI-0029` applies `foundation-ai-work/v1` to the Foundation source repository through `.ai/AI_WORK_PROFILE.md` and `.ai/ai-work/profile.json`. The profile is project governance, names no provider/runtime/model, and is not Foundation transfer payload.

The cross-platform integration test `test_reference_planner_adapter_and_executor_use_profile_without_expanding_authority` uses the project profile rather than a parallel test-only policy. It selects `project.custom`, builds the matching `WorkRequest`, plans it with the optional provider-neutral planner, invokes the neutral JSONL command reference adapter, and executes/resumes the exact plan with the optional executor.

## Authority and state boundary

The exercised request has only:

- effect `LOCAL_READ`;
- authority `filesystem:read`;
- boundary `PROCESS`;
- zero network and monetary limits;
- a deterministic capability and no model binding.

It has no repository write, external write, remote data, credential, synthesis, Git push, pull-request, publication, spend, or approval authority. Adapter configuration, copied output, checkpoints, and handles exist only in an external temporary directory. The persisted checkpoint/report contain identifiers, hashes, status, zero cost, bounded resource metadata, and one attempt—never host paths, prompt/response content, credentials, environment values, requested/actual model claims, or payload bytes. Resume reuses the completed checkpoint and does not invoke the operation twice.

## Interpretation

This proves that the source-project profile drives the real planner → adapter → executor path and preserves its explicit authority envelope. It does not make Python, that adapter, that executor, or any provider a Foundation prerequisite. When those optional implementations are absent, `.ai/AI_WORK_PROFILE.md` still requires the same classification and a truthful `PLAN_ONLY`, `MANUAL_REQUIRED`, `UNAVAILABLE`, or `BLOCKED` outcome.

The profile separately maps `foundation.validate` to the existing shell-free transfer, feature, registry, backlog, Foundation-validator, and complete unit-test commands. CI checks that mapping and the end-to-end self-host integration on Windows, Linux, and macOS.

Cross-platform evidence: PR #26 final head `653a2c9bc3635d5ed355f0d09acc3cb0981d8ddb` passed Foundation CI run `34148362064`, comprising the source-profile integration on macOS and Windows followed by the required complete Linux `validate` gate. Foundation Artifact Registry run `34148361996` also passed. The implementation head passed the focused 97-test platform selection and all 231 tests locally on Windows. The PR was squash-merged as `39cd94fe56ebfbd4218f971644cda5d0e12fc246`; post-merge Foundation CI run `34148447309` passed the same platform gate.
