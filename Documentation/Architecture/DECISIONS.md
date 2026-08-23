# Decision Records

Status: AUTHORITATIVE

Use `DEC-NNNN` IDs and statuses `Proposed`, `Accepted`, `Superseded`, or `Rejected`. Do not rewrite historical decisions; supersede them with a new record.

A record includes: ID, status, date, title, context, decision, rationale, alternatives, consequences, affected areas, supersedes/superseded-by, and evidence/references.

Create one for durable material decisions affecting multiple areas, difficult recovery, security/privacy/integrity, vendor commitment, methodology, validation strategy, or an override of Foundation defaults. An AI may analyze options or draft `Proposed`, but must not silently invent an undecided material choice.

## DEC-0001 — Repository as durable source of truth

- Status: Accepted
- Date: 2026-08-23
- Decision: Correct continuation must require only repository state plus the current task. Chats, memory, personal prompts, and scratchpads are non-authoritative.
- Consequences: canonical repository documents and concise handover/state files are required.

## DEC-0002 — Modular vendor-neutral core

- Status: Accepted
- Date: 2026-08-23
- Decision: Use a small mandatory core, optional capabilities, and thin adapters. Validation is universal; software testing is one capability.
- Consequences: adapter governance duplication is prohibited.

## DEC-0003 — Explicit safe upgrades

- Status: Accepted
- Date: 2026-08-23
- Decision: Use SemVer, protect local overrides, classify conflicts, and never automatically upgrade existing repositories.
- Consequences: upgrade tooling must be diff- and impact-based.