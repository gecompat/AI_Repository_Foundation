# Model and Resource Routing Policy

Status: AUTHORITATIVE

Choose per work step, not per project. Safety, privacy, authorization, correctness, and validation outrank cost.

- `LOCAL`: deterministic local processing; no generative model required.
- `ECONOMICAL`: bounded, low-risk, clearly specified, cheaply verifiable work.
- `BALANCED`: integrates multiple contracts, files, layers, or competing sources; diagnosis is not obvious.
- `FRONTIER`: critical or hard-to-verify decisions involving architecture, security, privacy, authorization, data loss, persistence boundaries, or high-impact conclusions.

Tier selection is based on risk, complexity, criticality, and verifiability—not human review effort. A stronger model does not replace required human review or approval. Concrete models, pricing, quotas, and provider features are runtime facts, never repository contracts.

After a difficult decision, reassess and downgrade subsequent mechanical or deterministic work. Start with the lowest plausibly sufficient reasoning level and escalate only on evidence.

Minimize context: use `repo_map.yaml`, relevant diffs, deduplicated error signatures, and compact confirmed facts. Do not load entire repositories, chats, logs, or research collections by default. Do not repeat an identical failed attempt without new evidence.