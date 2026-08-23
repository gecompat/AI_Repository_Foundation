# Foundation Metadata

Status: AUTHORITATIVE

- foundation: AI Repository Foundation
- version: 1.1.0
- profile: general
- canonical_entrypoint: AGENTS.md
- project_license: MIT
- transfer_manifest: `foundation/manifest.json`
- direct_ai_transfer: `foundation/AI_TRANSFER.md`
- transfer_model: explicit whitelist; rules only
- target_project_license: never replaced by installation
- default_adapters: github-copilot, claude-code, gemini

Versioning follows Semantic Versioning. PATCH fixes defects without new governance requirements; MINOR adds backward-compatible rules/capabilities/adapters or improves installation semantics; MAJOR changes authority or governance incompatibly.

The Foundation repository and the transferable rule set have separate scopes. Project README, LICENSE, changelog, project context, status, handover, backlog, roadmap, Foundation-internal decisions, tests, and tools are Foundation-project artifacts and are never transferred unless a future manifest explicitly defines a different rule artifact.

Upgrades are explicit and impact-based. Never auto-upgrade or auto-downgrade a target repository. Classify target states as `CREATE`, `UNCHANGED`, `MERGE_REQUIRED`, or `CONFLICT`; an AI may perform a semantic merge only under `foundation/AI_TRANSFER.md` while preserving project-specific rules and reporting real conflicts.
