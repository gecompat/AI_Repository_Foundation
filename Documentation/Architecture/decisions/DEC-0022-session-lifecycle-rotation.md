# DEC-0022 — AI session rotation uses deterministic metadata and delta handoff

Status: Accepted  
Date: 2026-10-05

## Context

Long-lived AI project chats can accumulate enough history that repeated context processing increases latency and token cost. A naive health monitor that repeatedly asks a model to rescan, cluster, or summarize the same conversation can consume the savings it is intended to create. The repository is already the Foundation's durable source of truth.

## Decision

Treat the orchestrator as a logical role, not as one permanent chat. Session lifecycle decisions use deterministic metadata already available to the caller plus explicit natural work boundaries. They do not perform continuous semantic conversation analysis.

Soft context or checkpoint-delta thresholds prepare a checkpoint and defer rotation to a natural boundary. A hard context threshold or explicit user request may require rotation. Threshold values are target-project policy, not Foundation claims about universal model limits. Unknown token metrics remain unknown. Response latency is diagnostic only.

When rotation occurs, the successor role bootstraps from current durable repository state and a content-minimized `foundation-session-handoff/v1` delta since the previous checkpoint. The handoff carries references and at most one external content handle rather than another whole-project or whole-chat summary. Actual successor-session creation is client-specific and may be marked automatic only when that capability is attested; otherwise continuation is manual.

## Consequences

- context-management overhead remains bounded and deterministic;
- recurring summary-of-summary degradation is avoided;
- project truth stays in durable repository artifacts instead of chat history;
- clients without automatic chat/session creation remain compatible;
- `foundation-ai-work/v1` and `foundation-ai-orchestration/v1` remain unchanged and compatible;
- the optional `ai-work` reference planner gains a separate `foundation-session-lifecycle/v1` decision command.

## Rejected alternatives

- fixed message-count rotation was rejected because message count is a weak proxy for useful context;
- continuous semantic topic-diversity/context-health scoring was rejected because its token and latency overhead can negate the benefit;
- response-latency-triggered rotation was rejected as authoritative logic because latency also reflects provider load, tool calls, networking, and reasoning effort;
- periodic full-chat summarization was rejected because it spends tokens continuously and compounds summary loss.

## Affected areas

AI work orchestration, long-running project sessions, client integration, context/token efficiency, handoff/bootstrap, upgrade applicability, and optional reference tooling.
