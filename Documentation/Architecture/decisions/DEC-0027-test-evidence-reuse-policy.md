# DEC-0027 — Optional test evidence reuse with protected trust boundaries

Status: Accepted

Date: 2026-10-19

## Decision

Add the portable `TEST_EVIDENCE_REUSE_POLICY.md` to Foundation 1.24.0 core and the semantic upgrade catalog. The user authorized review of a supplied development prompt and useful corrections/extensions to Foundation rules. Implement the policy and deterministic reporting defaults within that scope; do not treat the prompt as separate runtime or external-system authority.

Separate execution, authenticated producer trust, current gate equivalence, reuse acceptance and CI publication. Reuse requires project-selected gates, protected producer/verifier authority, complete successful oracles/cleanup, relevant input/dependency/environment binding and current freshness/revocation. Missing trust retains existing execution or an honest unmet gate. Models, hashes, role labels and self-authored PASS receipts cannot attest the boundary.

Keep activation optional and project-owned. The policy defines an adapter interface and acceptance obligations but supplies no executable cross-host verifier, keys, host isolation, CI publisher or live acceptance. Existing `foundation-ai-work/v1` schemas and consumers remain unchanged. Future executable evidence extensions need a compatible versioned contract and their own semantic upgrade/manifest/validation coverage. No new registry or default runtime dependency is introduced.

Clarify existing deterministic-first defaults: existing runners select tests, compare oracles, aggregate and clean up; complete success needs no model-only PASS confirmation. Local failure diagnosis and bounded findings precede semantic model work. Preserve mandatory review, qualification, repeated trials and exact current integration gates. Cheap checks can be rerun when recognition costs more.

## Alternatives and consequences

The full prompt also requests a runtime reference verifier. Implementing a model-writable attestation placeholder would provide misleading assurance; constructing a new trust service would exceed the rules task. Both are rejected here. Projects can implement the semantic interface using their existing protected infrastructure, after explicit trust/equivalence decisions and actual integration validation.

Do not adopt the prompt's blanket stop for possibly real information: the canonical privacy classification, destination and handling authority remain in force. Public/repository-intended facts remain usable. No target-project upgrade, repository protection change or merge is authorized by this decision. Existing decisions are preserved.

## Evidence and overhead

Registered work: `WI-0039`. The [prompt assessment](../../Quality/TEST_EVIDENCE_PROMPT_ASSESSMENT_2026-10-19.md) records baseline gaps, corrections, compatibility, primary sources and the bounded processing-overhead assessment. Local and remote validation receipts belong in factual project state, not in this decision as invented acceptance.
