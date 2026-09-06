# Model and Resource Routing Policy

Status: AUTHORITATIVE

Choose per work step, not per project. Safety, privacy, authorization, correctness, and validation outrank cost.

- `LOCAL`: deterministic local processing; no generative model required.
- `ECONOMICAL`: bounded, low-risk, clearly specified, cheaply verifiable work.
- `BALANCED`: integrates multiple contracts, files, layers, or competing sources; diagnosis is not obvious.
- `FRONTIER`: an unresolved, critical or hard-to-verify decision involving architecture, security, privacy, authorization, data loss, persistence boundaries, or another high-impact conclusion.

Routine work involving an already-defined security, privacy, authorization, or architecture contract does not become `FRONTIER` merely because that domain is involved. Tier selection is based on unresolved risk, complexity, criticality, and verifiability—not human review effort. A stronger model does not replace required human review or approval.

Human review effort is an execution-efficiency factor only after the required capability tier has been established. It may motivate better automation, clearer evidence, or a better model within the same tier; it must not by itself escalate the tier or remove a required review.

## Existing project routing policies

A target repository may already have a more detailed model, provider, quota, cost, or tool-selection policy. Preserve it when it is compatible. Do not replace a mature project policy merely to introduce Foundation tier names.

When Foundation tiers overlap an existing project taxonomy, maintain an explicit semantic mapping where needed:

- each project category used for AI/model selection should map to the closest Foundation capability tier or state that no direct mapping is needed;
- concrete model names, providers, current prices, quotas, and product-specific features remain runtime/project facts, not Foundation contracts;
- a target policy may split one Foundation tier into several project-specific categories;
- a target policy must not use human review effort alone to justify a higher Foundation capability tier;
- after a difficult decision, reassess and downgrade subsequent mechanical or deterministic work even when the project uses different local tier names.

The Foundation tiers provide a portable semantic abstraction. The target project's detailed routing remains authoritative for concrete runtime selection when compatible with these semantics.

## Dynamic routing contract

When a target selects dynamic routing, use a provider-neutral request/decision contract. The request describes the task class, Foundation tier, authorization envelope, required capabilities, context/output estimates, quality floor, budget, and optional session affinity. The decision records the selected provider/model, expected cost and success, reasoning effort, fallback chain, pricing epoch, expiry, and auditable exclusion reasons.

Apply privacy, authorization, capability, context, quality, price-freshness, and budget constraints before comparing economics. `LOCAL` means deterministic local processing and must not silently authorize a remote model. Concrete providers, model identifiers, capabilities, availability, quotas, and prices are runtime facts and are not hard-coded into this policy.

For feasible candidates, minimize expected cost of success rather than headline token price:

```text
expected_chain_spend = sum(probability_reached * estimated_attempt_cost)
chain_success = 1 - product(1 - predicted_attempt_success)
cost_of_success = (expected_chain_spend + expected_switching_cost
                   + final_failure_probability * failure_cost) / chain_success
                  + expected_latency * latency_value
```

Success estimates may combine explicit project quality priors with aggregate observed outcomes. A fallback is useful only when it materially improves chain success and remains inside the request's expected-spend bound. Session/cache affinity may reduce switching cost, but it is conditional and never overrides safety, capability, quality, freshness, or budget constraints.

## Price epochs, discovery, and evaluation

Remote catalogs and prices require source timestamps and expiry. A routing decision carries the applicable `pricing_epoch` and expires no later than the next price boundary of any eligible candidate; a rate change therefore invalidates cached rankings even when the previously selected model's own price is unchanged. If live refresh fails, retain an unexpired last-known-good catalog or fail closed—never invent a current price.

Newly discovered models start `UNASSESSED`. They may become eligible only through an explicitly allowed, bounded evaluation plan with task set, sample count, spend ceiling, stopping rules, and atomic reservation where concurrent evaluators could overspend. Graduation requires the project's minimum evidence; discovery alone is not a quality claim.

## Runtime state and graceful degradation

Catalogs, outcome aggregates, session hashes, evaluation reservations, and snapshots are runtime state. Keep them outside the repository and version control, write them atomically under a lock, store no credentials, and avoid retaining prompt or response content. Credentials are supplied by the target environment at execution time.

Thin integrations consume the same deterministic decision contract. The preferred order is local MCP, then the CLI, then a shell-free launcher or unexpired generated snapshot, and finally the portable Foundation tier without an invented concrete model. Each lower layer must preserve the same authorization and fail-closed semantics.

Minimize context: use relevant diffs, deduplicated error signatures, compact confirmed facts, and repository maps where available. After one complete rule analysis for a scope, use the deterministic `RULE_CONTEXT_CACHE_POLICY.md` contract between later change waves so unchanged additional rules are not repeatedly ingested or semantically analyzed. Cache fingerprinting never replaces native instruction discovery and uncertainty remains a full-read miss. Do not load entire repositories, chats, logs, or research collections by default. Do not repeat an identical failed attempt without new evidence.
