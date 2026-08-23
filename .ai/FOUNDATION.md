# Foundation Metadata

Status: AUTHORITATIVE

- foundation: AI Repository Foundation
- version: 1.2.0
- profile: general
- canonical_entrypoint: AGENTS.md
- project_license: MIT
- transfer_manifest: `foundation/manifest.json`
- direct_ai_transfer: `foundation/AI_TRANSFER.md`
- semantic_integration_policy: `Documentation/Standards/SEMANTIC_INTEGRATION_POLICY.md`
- transfer_model: explicit whitelist plus semantic integration for existing repositories
- attribution_notice: `foundation/AI_REPOSITORY_FOUNDATION_NOTICE.md` -> target `.ai/foundation/AI_REPOSITORY_FOUNDATION_NOTICE.md`
- validation_scope_contract: Foundation validator = `FOUNDATION_INTEGRITY`; target repository retains `PROJECT_SEMANTIC` and `RUNTIME_EMPIRICAL`
- project_governance_discovery: active target governance must remain transitively discoverable from root `AGENTS.md`
- target_project_license: never replaced or modified by installation
- default_adapters: github-copilot, claude-code, gemini

Versioning follows Semantic Versioning. PATCH fixes defects without new governance requirements; MINOR adds backward-compatible rules/capabilities/adapters or improves installation/integration semantics; MAJOR changes authority or governance incompatibly.

The Foundation repository and the transferable rule set have separate scopes. Project README, root LICENSE, changelog, project context, status, handover, backlog, roadmap, Foundation-internal decisions, tests, and tools are Foundation-project artifacts and are never transferred merely because they exist. The dedicated attribution notice is the only Foundation licensing artifact included in the transfer payload.

For existing repositories, semantic integration preserves target-owned governance. Foundation `REQUIRED` rules are minimum floors; stricter target rules are compatible. Existing target policy vocabularies do not need to be rewritten into Foundation terms when a semantic mapping is sufficient.

Foundation validation establishes deterministic Foundation integration/integrity only. Project-specific semantic validation and runtime/empirical validation remain target-repository responsibilities and are not replaced by Foundation installation.

Upgrades are explicit and impact-based. Never auto-upgrade or auto-downgrade a target repository. Classify file states as `CREATE`, `UNCHANGED`, `MERGE_REQUIRED`, or `CONFLICT`, then use the semantic integration classes for meaningful rule overlaps. Preserve project-specific rules and report real conflicts rather than normalizing the target repository to Foundation wording.
