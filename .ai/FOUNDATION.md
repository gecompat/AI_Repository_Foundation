# Foundation Metadata

Status: AUTHORITATIVE

- foundation: gecompat/AI_Repository_Foundation
- version: 1.0.0
- applied: 2026-08-23
- profile: general
- canonical_entrypoint: AGENTS.md
- license: MIT
- source_classification: FOUNDATION_DEFAULT
- enabled_capabilities: governance, documentation, research, data, git, ai-agents, bootstrap, validation
- enabled_adapters: codex-native, github-copilot, claude-code, gemini
- local_overrides: none

Versioning follows Semantic Versioning. PATCH fixes defects without new governance requirements; MINOR adds backward-compatible rules/capabilities/adapters; MAJOR changes structure, authority, or governance incompatibly.

Upgrades are explicit and impact-based. Never auto-upgrade or auto-downgrade a target repository. Classify file provenance as `FOUNDATION_DEFAULT`, `LOCAL_OVERRIDE`, `PROJECT_SPECIFIC`, or `CONFLICT`; classify conflicts as `NONE`, `COMPATIBLE_OVERRIDE`, `REVIEW_REQUIRED`, or `BLOCKING_CONFLICT`. Similar wording is not proof of semantic equivalence.