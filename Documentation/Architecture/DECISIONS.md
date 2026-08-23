# Decision Records

Status: AUTHORITATIVE

Use stable IDs and statuses `Proposed`, `Accepted`, `Superseded`, or `Rejected`. Do not rewrite historical decisions; supersede them with a new record.

A record includes: ID, status, date, title, context, decision, rationale, alternatives, consequences, affected areas, supersedes/superseded-by, and evidence/references.

Create one for durable material decisions affecting multiple areas, difficult recovery, security/privacy/integrity, vendor commitment, methodology, validation strategy, or an override of Foundation defaults. An AI may make a decision when the current task/project authority permits it, but must not silently invent an unresolved material choice; record the decision when durable traceability is warranted.

## DEC-0001 — Repository as durable source of truth

- Status: Accepted
- Date: 2026-08-23
- Decision: Correct continuation must require only repository state plus the current task. Chats, memory, personal prompts, and scratchpads are non-authoritative.
- Consequences: canonical repository documents and concise state/continuation information are required when relevant.

## DEC-0002 — Modular vendor-neutral core

- Status: Accepted
- Date: 2026-08-23
- Decision: Use a small reusable governance core and thin adapters. Validation is universal; software testing is one capability.
- Consequences: adapter governance duplication is prohibited.

## DEC-0003 — Explicit safe upgrades

- Status: Accepted
- Date: 2026-08-23
- Decision: Use SemVer, protect local overrides, classify conflicts, and never automatically overwrite differing rules in existing repositories.
- Consequences: upgrade tooling is diff- and impact-based.

## DEC-0004 — Rules-only manifest transfer

- Status: Accepted
- Date: 2026-08-23
- Decision: The Foundation repository is not itself a target template. A manifest explicitly whitelists reusable rule sources and maps them into target paths. The same manifest is consumed by deterministic tooling and direct AI transfer.
- Rationale: repository-wide copying leaked Foundation README/license/state into target projects and made existing-repository installation unsafe.
- Consequences: Foundation project artifacts are never transferred merely because they exist; target rules are namespaced under `.ai/foundation/` and root discovery bridges are merged conservatively.

## DEC-0005 — Authorization envelope instead of mutation gate

- Status: Accepted
- Date: 2026-08-23
- Decision: A concrete task authorizes ordinary expected and proportionate operations inside its project/environment/budget scope. Additional authorization is needed only when an action materially exceeds that envelope or lacks exact authority for a destructive/irreversible effect.
- Rationale: treating every local/external mutation as a gate makes normal product operation unusable.
- Consequences: normal file, Git, API, test, and release operations do not require redundant confirmations when already clearly authorized.

## DEC-0006 — Privacy classification instead of "real data" gate

- Status: Accepted
- Date: 2026-08-23
- Decision: Privacy gates depend on data classification, destination, and permitted handling boundary. Real public or repository-intended information is not automatically confidential.
- Consequences: public research and ordinary project facts remain usable while secrets, sensitive/confidential transfer, and unknown classification retain strict handling rules.

## DEC-0007 — Dedicated attribution notice for transferred Foundation material

- Status: Accepted
- Date: 2026-08-23
- Context: The Foundation's MIT notice must accompany copied Foundation material, while target repositories must retain independent control of their own root license.
- Decision: Every Foundation rules transfer includes `.ai/foundation/AI_REPOSITORY_FOUNDATION_NOTICE.md`, containing the complete Foundation MIT copyright and permission notice. Installation never replaces or amends the target repository's root `LICENSE`.
- Rationale: a dedicated, namespaced notice satisfies Foundation provenance/attribution needs without creating the false impression that the target project as a whole is MIT-licensed by the Foundation.
- Alternatives: copying the Foundation root `LICENSE` was rejected because it could be misread as the target-project license; README-only attribution was rejected because README is outside the transfer payload and may not exist.
- Consequences: the manifest, installer, direct AI protocol, validator, and tests treat the notice as mandatory transfer provenance rather than project-license selection.
- Affected areas: transfer manifest, installer behavior, direct AI transfer, target validation, licensing policy.
