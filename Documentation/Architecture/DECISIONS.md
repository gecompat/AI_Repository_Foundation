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

## DEC-0008 — Layered validation ownership

- Status: Accepted
- Date: 2026-08-23
- Context: A generic Foundation validator can prove deterministic Foundation integration contracts but cannot generally prove the semantic correctness of target-project rules, local overrides, architecture, domain behavior, or runtime results.
- Decision: Validation is separated into `FOUNDATION_INTEGRITY`, `PROJECT_SEMANTIC`, and `RUNTIME_EMPIRICAL`. The Foundation validator owns only `FOUNDATION_INTEGRITY`; the target repository remains authoritative for the other scopes. Completion combines the scopes relevant to the affected change.
- Rationale: treating Foundation validation as complete project validation would create false assurance and could cause existing project-specific static contracts, validators, tests, or reviews to be removed or skipped.
- Consequences: transferred rules and machine-readable metadata explicitly preserve target validation; drift detection is not semantic approval; Foundation-green does not imply project-green.

## DEC-0009 — Semantic integration preserves mature project governance

- Status: Accepted
- Date: 2026-08-23
- Context: Real existing repositories contain mature privacy, validation, model-routing, Git, approval, adapter, documentation, and identifier contracts that often overlap the Foundation without being wrong.
- Decision: Existing-repository integration uses explicit semantic compatibility classes. Foundation `REQUIRED` rules are minimum protected floors, intentionally stricter project rules are compatible, active project governance must remain discoverable from root `AGENTS.md`, and unique adapter governance must be preserved/re-homed before adapters are thinned.
- Rationale: file-level `MERGE_REQUIRED` alone is insufficient to distinguish a valid stricter project rule, an equivalent rule, a selectable override, a target-internal contradiction, or a true Foundation required-floor conflict.
- Alternatives: normalizing all projects to Foundation wording was rejected because it would destroy project-specific policy detail and create unnecessary churn; leaving semantic merge entirely informal was rejected because different AI systems produced inconsistent classifications.
- Consequences: direct AI transfer becomes a bounded semantic merge protocol; richer project validation statuses and model-routing policies remain valid through semantic mapping; target repo maps are preserved; orphaned active authority is treated as an integration defect.
- Affected areas: semantic integration, root discovery, adapters, privacy, model routing, validation, repo-map integration, existing-repository migration.

## DEC-0010 — Layered persistent identity with legacy-safe adoption

- Status: Accepted
- Date: 2026-08-24
- Context: Human-readable identifiers such as hierarchical wave/slice IDs are useful but become unstable when they encode mutable hierarchy, phase, status, location, or tool ownership. Repository splits/merges, forks, multiple AI agents, offline work, and issue-tracker migration also require identity that does not depend on a central local sequence or current repository path. Existing repositories, however, may already contain deeply referenced identifier conventions that must not be invalidated by Foundation integration.
- Decision: Separate persistent machine identity, human reference, aliases/external references, mutable relations/classification, revision identity, and locator. The Foundation default for new/adopting projects uses an opaque RFC 9562 UUID machine UID (UUIDv7 default, UUIDv4 compatible) plus a flat typed project-local human reference. Hierarchy/status/location remain metadata/relations. Existing repositories default to `PRESERVE`; prospective adoption uses `ADOPT_FORWARD`; historical renaming requires explicitly authorized `MIGRATE_EXPLICIT` with durable mappings and recovery.
- Rationale: one semantically rich string cannot simultaneously optimize human readability, distributed/offline allocation, cross-repository uniqueness, refactoring stability, and long-lived compatibility. A layered model preserves readable references while decoupling them from the deepest identity.
- Alternatives: making the current `S-FUT11-04`-style hierarchy universal was rejected because reparenting/phase changes make encoded semantics stale; UUID-only references were rejected as poor human interfaces; flat counters alone were rejected as insufficient for concurrent/offline allocation; content hashes were rejected as primary identity for mutable logical artifacts because normal edits would change identity.
- Consequences: the Foundation gains a persistent-identity policy, machine-readable identity contract, default prefix registry, explicit relation/revision semantics, and legacy-safe adoption modes. The Foundation validator checks contract installation/integrity but target-specific historical mappings remain `PROJECT_SEMANTIC`/`RUNTIME_EMPIRICAL` responsibilities.
- Affected areas: planning/governance identifiers, semantic integration, AI transfer, repository federation/split/merge, validation, future tooling.
- Evidence/references: RFC 9562, RFC 8141, RFC 8720, ISO 21511, SPDX 3.x identifier/namespace concepts.

## DEC-0011 — Language-neutral Registration Authority with shared human/AI allocation

- Status: Accepted
- Date: 2026-08-24
- Context: Flat sequential human references are useful only if creation is safe for humans and AI. A Python-only allocator would make the Foundation language-specific, while independent per-client counter logic would reintroduce collisions under branches, offline work, multiple agents, or mixed PowerShell/Python operation. Existing repositories may already have a stronger allocator in Jira, GitHub Issues, Azure DevOps, a database, a service, or project-specific tooling.
- Decision: Define artifact registration as a language-neutral protocol governed by one Registration Authority per overlapping final-reference scope. Humans and AI use the same authority. `DIRECT` may allocate a final human reference only through serialized or equivalently unique authority behavior; `DEFERRED` creates the permanent machine UID first and allocates the final human reference later. The normative policy and JSON Schemas are Foundation core. Python is not required. Python and PowerShell are independent, first-class reference implementations delivered only through the opt-in `artifact-registration-clients` capability and verified against the same contract fixtures. Compatible existing project allocators are preserved and take precedence.
- Rationale: Identity semantics should survive implementation-language, operating-system, IDE, issue-tracker, and vendor changes. A shared authority prevents human/AI and cross-client sequence divergence while optional reference clients provide immediately usable tooling without making either runtime mandatory.
- Alternatives: Python-only tooling was rejected as an unnecessary platform/runtime constraint; PowerShell-only tooling was rejected for the same reason; allowing each client to increment the highest visible sequence independently was rejected as unsafe under concurrency; requiring the Foundation local JSON registry for all projects was rejected because central issue trackers/databases/services are superior authorities in many multi-user environments.
- Consequences: v1.4 adds a Registration Authority contract, `DIRECT`/`DEFERRED` semantics, core JSON Schemas, capability-aware installer/validator behavior, independent Python/PowerShell clients, and cross-language CI. Target-specific authority selection and real concurrency/integration behavior remain `PROJECT_SEMANTIC`/`RUNTIME_EMPIRICAL` responsibilities.
- Affected areas: artifact creation, human and AI workflows, persistent identity, semantic integration, transfer manifest, installer, validator, CI, optional tooling.
