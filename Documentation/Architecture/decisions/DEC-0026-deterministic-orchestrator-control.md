# DEC-0026 — Bounded deterministic provider-neutral orchestrator control

Status: Accepted

Date: 2026-10-09

## Decision

Add optional `foundation-orchestrator-control/v1` to `ai-orchestrator`, exposed by one Python implementation through CLI `control` and MCP `orchestration_control`. Deliver Foundation 1.23.0 on the 1.22.0 work in open PR #38; do not merge either PR as part of this task. Core-only use, existing adapters and installer defaults remain supported.

Use explicit external host configuration and short, fresh host observations instead of chat inspection. The host supplies capability evidence, execution status, available start models, acknowledgments and independent evidence verification. Public requests contain only a job reference and event. A target must protect these trust inputs from model writes; selecting a file is not cryptographic authentication or an OS sandbox. Unknown client support or execution outcome requires manual reconciliation.

Autonomy defaults off. A job binds work, authorization, completion, current bootstrap and shared budget references. Enablement requires a measurable hard budget or an explicitly configured finite dispatch bound. A bound counts starts, resumes and research across jobs sharing that budget; it is not a token, subscription or provider spending estimate. Unknown usage remains unknown. The example start tier is BALANCED, overridden by project configuration and constrained by fresh router and client availability evidence. Model-capable evidence collectors are never run by mechanical control.

Prefer events. The optional scheduler defaults to 30 minutes and can send exactly `HEARTBEAT` only after an evidenced check before model invocation establishes an idle owner with executable remaining work. No such check means periodic model wake is disabled. No change, waiting, pause, cancellation or completion produces another model call. One automatic resume per owner generation/checkpoint requires new progress before another. Fixed notification templates report completion or intervention once; external destinations need explicit authority.

Reserve effects atomically under a shared OS lock before returning stable action IDs. The client checks the current grant, generation and expiry, deduplicates the action ID, then acknowledges the actual effect. A lost response, expired acknowledgment, timeout or failed successor does not authorize replay. Late predecessor observations are rejected without changing the successor. Rotation uses the existing session planner and handoff: confirmed predecessor quiescence precedes successor start, and only a trusted matching actual-model receipt establishes its owner. Preserve work, instructions, budget and unresolved references; do not retain whole-chat summaries.

Bounded source research uses a pre-authorized reference and the same budget. Independently verified proposals bind the exact candidate hash, source, units and model mapping. Reject invalid, expired, changed or contradictory records; merge accepted records into the shared last-known-good cache without erasing unrelated providers. Collector code is not automatically edited. Reuse existing evidence/refresh contracts and shared atomic IO.

## Alternatives and limits

A permanent orchestrator chat, unconditional timer prompts, automatic retry after timeout, inferred client/model support and research self-approval would add cost or duplicate effects without evidence. They are rejected. The controller requests client effects; it supplies no daemon, vendor SDK, scheduler, account or guaranteed delivery/exactly-once execution. Targets can implement the same contract in another language. Real client integration requires target-specific validation; offline fixtures prove only these reference contracts.

## Processing-overhead assessment

One owner implements the finite authorized 1.23.0/control/documentation/test/PR scope without delegated agents or paid live calls. Token/spend metering is unavailable and no savings measurement is claimed. Existing discovery and analyzed rules are reused only within their applicable current scope. Focused controller/state regressions precede the required full suite. The full completion and Windows/macOS/Linux gates are justified because shared IO, optional installation, schemas, routing and workflow selection are affected. Stable green logs are reduced locally to counts/findings; repeat checks require changed inputs, a finding or an unmet exact-head gate. No new review chain, broad per-edit reading, recurring model scan or telemetry system is introduced. Live host integration is not applicable to this offline reference implementation; clients must attest their own capability boundaries before enabling it.

## References

Registered work: `WI-0038`; prerequisite: `WI-0037` / `DEC-0025`. Existing [orchestration policy](../../Standards/AI_WORK_ORCHESTRATION_POLICY.md), [session decision](DEC-0022-session-lifecycle-rotation.md), [capability guide](../../../foundation/capabilities/ai-orchestrator/AI_ORCHESTRATOR.md) and [user guide](../../Guides/USER_GUIDE.md) remain the relevant reading path. No prior decision is superseded.
