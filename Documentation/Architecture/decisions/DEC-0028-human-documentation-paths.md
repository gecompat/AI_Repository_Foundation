# DEC-0028 — Human documentation paths and separated AI control with gradual adoption

Status: Accepted

Date: 2026-10-20

## Context

The previous documentation policy required truthful state and a README entry point but did not define complete human reading paths, understandable storage, or a proportionate acceptance procedure. The user approved a concrete Foundation implementation covering those outcomes, including correction of confusing directory structures. The selected rollout is progressive and uses lean checks rather than a new documentation schema, validator, or per-page metadata.

## Decision

Expand the existing [documentation policy](../../Standards/DOCUMENTATION_POLICY.md) as the single detailed rule source. Make its outcomes REQUIRED while retaining project choice of language, suitable folder names and tools. Shared technical contracts keep one authority. Human guidance, planning/evidence and AI control have separate purposes and navigable entry points; machine information remains inspectable by humans.

Apply the policy to new and materially changed paths including necessary continuation pages. During installation/upgrade, assess central human and AI entries and structural problems. Preserve layouts that support the outcomes and correct confusing ones within authorized scope. Put remaining legacy remediation, its scope, owner/role and trigger into existing planning. Integrating the new rules with explicit legacy gaps can complete an upgrade; it cannot establish full documentation conformity. Active governance contradictions still require resolution.

Release as Foundation 1.25.0 with the semantic feature `human-documentation-paths`. Project rules, validation, short discovery sources, semantic integration and upgrade instructions link to the policy. Preserve installer behavior and all target-owned content; no other repository is upgraded by this task. Apply the paths to Foundation's own introduction, installation, upgrade and debugging guidance. Move source completion commands to the contribution guide.

## Validation and processing overhead

One implementation owner handles the bounded policy/transfer/source-guidance/installation-and-upgrade-test change. Checkpoints are the coherent contract, focused regression, and stable completion gate/PR. No delegated reviewers, new recurring work, telemetry, schemas or executable capabilities are introduced. Token/spend consumption is unknown; the finite bound is this authorized implementation and its required verification.

Use existing deterministic transfer/hash/version/feature and registry/backlog checks, focused installation/upgrade tests, and the required stable Foundation regression gate. Policy text alone is not a readability oracle: author walkthroughs assess actual paths under PROJECT_SEMANTIC, including local links and the distinction between planned and current evidence. Record results in existing status/PR evidence. Additional review follows existing obligations or a concrete new risk, not a review chain. Full stable regression is warranted by shared core policy, discovery, version and install/upgrade consumers; repeat only for changed inputs or a failed gate.

## Consequences

The source validator remains limited to FOUNDATION_INTEGRITY for targets. A clean policy transfer cannot certify human understanding or arbitrary target-project documentation. Existing structures and legal/historical text are not rewritten wholesale. Broader target migrations need their normal task authority and path-consumer checks. Historical identifiers and references remain intact.

`WI-0040` tracks this implementation in the canonical v2 registry. Current validation and delivery status are recorded in [project status](../../../.ai/PROJECT_STATUS.md) and [handover](../../../.ai/HANDOVER.md).

## Follow-up — 2026-10-20: drift prevention within bounded context

The user's follow-up requires preventing documentation drift without repeatedly consuming large text corpora. Extend the same unreleased feature: assess documentation impact for coherent material behavior/configuration changes even without Markdown edits, select relevant paths and dependencies locally, and reuse only actually available analysis under the existing processing efficiency policy. Changed non-documentation dependencies invalidate affected guidance analysis; lost analysis requires reading the selected scope. Link/hash/schema checks are structural evidence, not an oracle for factual accuracy or readability. Existing evidence carries impact/acceptance; no new tool, page metadata, recurring model audit or target migration is added. Register the feature's dependency on bounded processing efficiency and verify transitive source-to-documentation invalidation with the existing reference helper tests. Earlier validation receipts remain historical until the follow-up's required checks complete.
