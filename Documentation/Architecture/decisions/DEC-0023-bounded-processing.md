# DEC-0023 — Bounded processing with scoped rules and session-local reuse

Status: Accepted  
Date: 2026-10-09

## Context

Large entrypoints, uncertain optional cache setup, repeated full reading, fine-grained evidence review, and unbounded concurrent agent work can overwhelm the savings intended by existing cost policies.

## Decision

Provide a short core entrypoint and route detailed boundaries on demand. Standardize verified session-local rule reuse without requiring optional components; keep the persistent cache v1 unchanged. Bind reusable analysis to current repository/native authority/scope and transitive source content, not merely HEAD or old chat assertions. A freshly validated equivalent worktree may reuse available analysis. Unknown discovery, changed authority, and missing analysis remain fail-closed.

Use a proportionate routine workflow, distinct-purpose additional reviews, one shared root/descendant budget, and bounded waiting. Ship a small core deterministic reference for these decisions and advisory governance audits. Pure budget decisions are not atomic reservations or actual provider limits. Preserve protected evidence, safety, privacy, independence, and stronger compatible project rules; report their efficiency cost rather than silently overriding them.

## Consequences

Core-only adopters can use the reference with Python or implement the procedure in another client/language. Numeric budgets and target governance amendments remain explicit project choices. No account quota, pricing, provider, model, or private telemetry becomes repository policy. Transfer completeness and semantic feature assessment cover every new artifact.
