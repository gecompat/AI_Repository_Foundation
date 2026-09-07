# Foundation source AI work profile

Status: AUTHORITATIVE PROJECT PROFILE

This source repository applies `foundation-ai-work/v1` to its own AI-assisted development, research, documentation, structured-data, and project-defined work. The portable project mapping is `.ai/ai-work/profile.json`. It is Foundation source-project governance and is not transfer payload.

Use the profile whether or not the optional Python planner, a model, MCP, Ollama, a cloud provider, or an executor is available. For each material task:

1. map the task to the closest profile or declare a project-specific task class;
2. classify data, risk, effects, required capabilities, limits, and validation before choosing a runtime;
3. discover current capabilities and their execution boundaries without treating discovery as permission;
4. prefer an adequate deterministic tool and execute only within the current authorization envelope;
5. use the listed Foundation validation command argv without shell evaluation when `foundation.validate` is affected;
6. keep payloads, prompts, responses, credentials, live inventories, plans/reports, and host-specific evidence outside Git;
7. distinguish a requested model from the actual execution model; accept `ATTESTED` only from matching host execution/response metadata issued by an explicitly trusted runtime identity;
8. if automatic dispatch is unavailable or unattested, create an expiring `MANUAL_DISPATCH_REQUIRED` handoff outside Git with tier/capability, privacy, acceptance, and validation instructions, then verify the subsequent receipt;
9. if an optional component is absent or unhealthy, continue with healthy alternatives or record `MANUAL_REQUIRED`, `UNAVAILABLE`, or `BLOCKED` truthfully.

The profile grants no remote data transfer, spend, publication, repository administration, push, or pull-request authority. Those effects come only from the current user request and project/repository controls. A generated capability or locally synthesized adapter stays outside the repository and cannot be promoted without the normal authorized branch/PR process.

For the current implementation program, repository inspection/editing is the work capability and the existing deterministic Foundation gate is `foundation.validate`. GitHub PR creation and merge remain separate effects governed by the explicit task authorization and branch Rulesets.

The source project selects no required client or provider. Client detection/plans, configuration backups, manual prompt files, receipts, and synthesized adapters stay outside this repository. A model recommendation may be used in Codex, Visual Studio, GitHub Copilot, or another client, but the project records the result as `REQUESTED_NOT_ATTESTED` until evidence from that client establishes the actual model. Local adapter synthesis is disabled unless the current task explicitly grants it and the resulting external adapter passes conformance while quarantined.

Project conformance includes an end-to-end deterministic self-host check: the profile supplies the task classification, the reference planner creates an exact plan, the neutral command adapter invokes a shell-free process, and the optional executor records one resumable content-free attempt in external temporary state. That check has `LOCAL_READ` and `filesystem:read` only, zero network and money limits, no model binding, and no repository/external write, data-transfer, push, pull-request, publication, spend, credential, or synthesis authority. It proves the integration path, not authority for later tasks.
