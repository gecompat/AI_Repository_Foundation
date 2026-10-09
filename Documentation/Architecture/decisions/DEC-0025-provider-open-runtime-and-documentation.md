# DEC-0025 — Provider-open runtime transport and explanatory documentation

Status: Accepted

Date: 2026-10-09

## Context

Foundation 1.21 has extensive contracts but no coherent beginner-to-deep reading path. Its JSONL protocol and raw CommandAdapter do not make arbitrary provider bridges reachable through shared runtime configuration, CLI, MCP and orchestrator. A schema limited to two HTTP adapters narrows that extension point. Historical state also labels merged releases as pending.

## Decision and rationale

Deliver the authorized additive change as Foundation 1.22.0. Lead README with purpose/functionality, add an informative English learner guide, and explain the full architecture. Link normative contracts rather than creating another governance source. Distinguish source-project state, current evidence and historical checkpoints. Preserve installer defaults and show a core-only installation without product adapters.

Add a closed `stdio` variant to runtime configuration v1. Launch an explicitly configured absolute executable and exact argv with `shell=False`, an explicit environment allowlist and optional absolute cwd. Reuse `foundation-ai-adapter-jsonl/v1`; preserve HTTP configuration and legacy raw CommandAdapter behavior. Add no provider SDKs, accounts, dynamic program discovery or mandatory paid/live tests. Product discovery follows adapter-type selection.

Treat backend boundaries independently from wrapper process location. Check network/data/per-call remote authority and handle roots before invocation; bound request/stdout/stderr, match protocol/request identity, reject payload fields and verify output receipts. Reject existing output handles to exclude stale success. Arbitrary programs are trusted integrations, not sandboxed by bridge checks.

Observed model metadata requires a configured trusted runtime source. Optional Stdio `trust_model_metadata` is false by default and expresses target trust in the reviewed adapter reporting backend response/execution identity. It cannot create missing identity, quality/cost, or strong alias evidence. Missing/untrusted identity stays unattested. Child errors after launch, timeout and invalid responses are ambiguous: preserve manual reconciliation and checkpoint no-replay. Definite pre-launch availability failures may permit availability fallback. Direct-child termination does not prove remote or descendant cancellation.

## Alternatives

Mandatory provider SDKs would narrow portability and require accounts. Treating arbitrary raw command stdout as JSONL would break its contract. Inferring locality or actual model from a process/catalog/request would manufacture evidence. Rewriting governance as a tutorial would duplicate authority. These alternatives are rejected.

## Consequences and affected areas

Schema/configuration, runtime CLI/MCP, orchestrator consumption, optional payload coverage, feature history and hashes change together. Core rules remain provider-open; products describe reference paths. Targets need their normal complete upgrade assessment; none are upgraded automatically. A tested PR is delivery, with merge outside this task.

## Processing-overhead assessment

One owner handles this coherent task without delegated agents or new telemetry. Reliable token/spend metering is unavailable; the finite bound is the authorized documentation/transport/1.22/PR scope with checkpoints after focused contracts, documentation/transfer consistency, local gates and exact PR checks. No live models, paid services or unrelated projects are included. Required source completion and platform gates are a justified full-suite exception because shared schema, optional transfer/install/upgrade, runtime facades and documentation consumers are affected. Focused process tests precede the stable full gate; repetitions require changed inputs, findings or exact-head freshness. Logs stay local with bounded failure/count extraction. No extra review chain or rapid unchanged-state polling is added. Consumption is unknown; no measured savings or provider spending enforcement is claimed.

## Evidence and references

`WI-0037` is allocated in the canonical v2 registry. The user-authorized plan establishes scope/version/no-merge. See [runtime guide](../../../foundation/capabilities/ai-runtime-adapters/AI_RUNTIME_ADAPTERS.md), [work policy](../../Standards/AI_WORK_ORCHESTRATION_POLICY.md), [user guide](../../Guides/USER_GUIDE.md), [status](../../../.ai/PROJECT_STATUS.md) and [handover](../../../.ai/HANDOVER.md) for current evidence. No prior decision is superseded.
