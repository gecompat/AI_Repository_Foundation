# Model and Resource Routing Policy

Status: AUTHORITATIVE

Choose per work step, not per project. Safety, privacy, authorization, correctness, and validation outrank cost.

- `LOCAL`: deterministic local processing; no generative model required.
- `ECONOMICAL`: bounded, low-risk, clearly specified, cheaply verifiable work.
- `BALANCED`: integrates multiple contracts, files, layers, or competing sources; diagnosis is not obvious.
- `FRONTIER`: an unresolved, critical or hard-to-verify decision involving architecture, security, privacy, authorization, data loss, persistence boundaries, or another high-impact conclusion.

Routine work involving an already-defined security, privacy, authorization, or architecture contract does not become `FRONTIER` merely because that domain is involved. Tier selection is based on unresolved risk, complexity, criticality, and verifiability—not human review effort. A stronger model does not replace required human review or approval.

Human review effort is an execution-efficiency factor only after the required capability tier has been established. It may motivate better automation, clearer evidence, or a better model within the same tier; it must not by itself escalate the tier or remove a required review.

Concrete models, pricing, quotas, and provider features are runtime facts, never repository contracts. After a difficult decision, reassess and downgrade subsequent mechanical or deterministic work. Start with the lowest plausibly sufficient reasoning level and escalate only on evidence.

Minimize context: use relevant diffs, deduplicated error signatures, compact confirmed facts, and repository maps where available. Do not load entire repositories, chats, logs, or research collections by default. Do not repeat an identical failed attempt without new evidence.
