# Foundation Metadata

Status: AUTHORITATIVE

- foundation: AI Repository Foundation
- version: 1.3.0
- profile: general
- canonical_entrypoint: AGENTS.md
- project_license: MIT
- transfer_manifest: `foundation/manifest.json`
- direct_ai_transfer: `foundation/AI_TRANSFER.md`
- semantic_integration_policy: `Documentation/Standards/SEMANTIC_INTEGRATION_POLICY.md`
- persistent_identity_policy: `Documentation/Standards/PERSISTENT_IDENTITY_POLICY.md`
- transfer_model: explicit whitelist plus semantic integration for existing repositories
- attribution_notice: `foundation/AI_REPOSITORY_FOUNDATION_NOTICE.md` -> target `.ai/foundation/AI_REPOSITORY_FOUNDATION_NOTICE.md`
- validation_scope_contract: Foundation validator = `FOUNDATION_INTEGRITY`; target repository retains `PROJECT_SEMANTIC` and `RUNTIME_EMPIRICAL`
- project_governance_discovery: active target governance must remain transitively discoverable from root `AGENTS.md`
- identity_contract: stable no-reuse identity floor; Foundation default = opaque RFC 9562 UUID machine UID plus flat typed project-local human reference; existing-project default = `PRESERVE`
- target_project_license: never replaced or modified by installation
- default_adapters: github-copilot, claude-code, gemini

Versioning follows Semantic Versioning. PATCH fixes defects without new governance requirements; MINOR adds backward-compatible rules/capabilities/adapters or improves installation/integration semantics; MAJOR changes authority or governance incompatibly.

The Foundation repository and the transferable rule set have separate scopes. Project README, root LICENSE, changelog, project context, status, handover, backlog, roadmap, Foundation-internal decisions, tests, and tools are Foundation-project artifacts and are never transferred merely because they exist. The dedicated attribution notice is the only Foundation licensing artifact included in the transfer payload.

For existing repositories, semantic integration preserves target-owned governance. Foundation `REQUIRED` rules are minimum floors; stricter target rules are compatible. Existing target policy vocabularies do not need to be rewritten into Foundation terms when a semantic mapping is sufficient.

Persistent identifier integration follows the same compatibility rule. Existing published identifiers are preserved by default. `ADOPT_FORWARD` may introduce a better profile prospectively while retaining history; `MIGRATE_EXPLICIT` requires a separate explicit migration decision. Foundation installation never treats missing input as migration authority.

Foundation validation establishes deterministic Foundation integration/integrity only. Project-specific semantic validation and runtime/empirical validation remain target-repository responsibilities and are not replaced by Foundation installation.

Upgrades are explicit and impact-based. Never auto-upgrade or auto-downgrade a target repository. Classify file states as `CREATE`, `UNCHANGED`, `MERGE_REQUIRED`, or `CONFLICT`, then use the semantic integration classes for meaningful rule overlaps. Preserve project-specific rules and identifier history and report real conflicts rather than normalizing the target repository to Foundation wording.
