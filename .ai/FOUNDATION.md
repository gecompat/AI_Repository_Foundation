# Foundation Metadata

Status: AUTHORITATIVE

- foundation: AI Repository Foundation
- version: 1.8.0
- profile: general
- canonical_entrypoint: AGENTS.md
- project_license: MIT
- transfer_manifest: `foundation/manifest.json`
- ruleset_version_authority: `foundation/manifest.json#ruleset_version`
- transfer_coverage_contract: `foundation/manifest.json#transfer_coverage_contract`
- transfer_completeness_guard: `tools/transfer_manifest_guard.py`
- semantic_feature_catalog: `foundation/feature_catalog.json`
- semantic_feature_guard: `tools/feature_catalog_guard.py`
- semantic_upgrade_delta_tool: `tools/upgrade_applicability.py`
- direct_ai_transfer: `foundation/AI_TRANSFER.md`
- semantic_integration_policy: `Documentation/Standards/SEMANTIC_INTEGRATION_POLICY.md`
- persistent_identity_policy: `Documentation/Standards/PERSISTENT_IDENTITY_POLICY.md`
- artifact_registration_policy: `Documentation/Standards/ARTIFACT_REGISTRATION_POLICY.md`
- central_artifact_registry_policy: `Documentation/Standards/CENTRAL_ARTIFACT_REGISTRY_POLICY.md`
- upgrade_applicability_policy: `Documentation/Standards/UPGRADE_APPLICABILITY_POLICY.md`
- repository_continuity_policy: `Documentation/Standards/REPOSITORY_CONTINUITY_POLICY.md`
- rule_context_cache_policy: `Documentation/Standards/RULE_CONTEXT_CACHE_POLICY.md`
- registration_schemas: `foundation/schemas/`
- transfer_model: explicit core whitelist plus semantic integration and explicitly selected optional capabilities
- attribution_notice: `foundation/AI_REPOSITORY_FOUNDATION_NOTICE.md` -> target `.ai/foundation/AI_REPOSITORY_FOUNDATION_NOTICE.md`
- validation_scope_contract: Foundation validator = `FOUNDATION_INTEGRITY`; target repository retains `PROJECT_SEMANTIC` and `RUNTIME_EMPIRICAL`
- portable_text_equivalence: UTF-8 CRLF/LF-only Git working-tree differences are equivalent for Foundation install/drift checks; true text/binary differences remain detectable
- rule_context_cache_contract: native instruction discovery per run; session-local semantic analyses keyed by validated scope/source dependencies; optional local records contain fingerprints/dependency metadata only and fail closed on scope, instruction, topology, source-set, schema, generator, corruption, or uncertainty changes
- validation_availability_contract: `VALIDATION_FAILURE` is never break-glass eligible; `INFRASTRUCTURE_UNAVAILABLE` may use an authorized project path; `UNKNOWN` is non-bypassable
- project_governance_discovery: active target governance must remain transitively discoverable from root `AGENTS.md`
- identity_contract: stable no-reuse identity floor; Foundation default = opaque RFC 9562 UUID machine UID plus flat typed project-local human reference; existing-project default = `PRESERVE`
- registration_contract: one Registration Authority per overlapping final-reference scope; humans and AI use the same authority; `DIRECT` or `DEFERRED` allocation semantics are language-neutral
- central_registry_contract: repository-native JSON default = `foundation-artifact-registry/v2`; complete records are central; human ref is object key; no `next_sequence`; object-level merge plus Git-result verification
- upgrade_contract: complete introduced/materially-changed feature delta; exactly one applicability classification per candidate; recommendations/decisions/conflicts surfaced explicitly
- source_github_merge_protection: required; target state = layered Rulesets with unbypassable core safety and pull-request-only CI bypass; see `Documentation/Quality/GITHUB_BRANCH_PROTECTION.md`
- source_github_break_glass: infrastructure-unavailability only; see `Documentation/Quality/GITHUB_BREAK_GLASS.md`
- target_github_merge_protection: recommended when relevant, never silently imposed by Foundation transfer
- python_runtime_required: false
- powershell_reference_client: supported first-class for the v1 compatibility profile
- optional_capabilities: `artifact-registration-clients`; `artifact-registry-github`; `rule-context-cache`
- target_project_license: never replaced or modified by installation
- default_adapters: github-copilot, claude-code, gemini
- default_capabilities: none

## Foundation source-project identity profile

The Foundation source repository itself uses its own persistent-identity model under explicit `MIGRATE_EXPLICIT`:

- active work items use `WI-*`;
- durable decisions use `DEC-*`;
- `.ai/identity/registry.json` is the source-project Registration Authority and canonical planning state;
- the source registry uses `foundation-artifact-registry/v2` and stores complete records centrally;
- `.ai/BACKLOG.md` is generated from the registry and is not an independent planning authority;
- `Documentation/Architecture/IDENTIFIER_MIGRATION_2026-08-24.md` preserves the old `FND-*` aliases;
- new final Foundation project references are derived from canonical registry keys, never inferred by scanning Markdown;
- `next_sequence` and a mutable global registry revision are intentionally not persisted.

This source-project profile is not transferable target governance and is intentionally kept outside the manifest transfer payload.

## Foundation source-project GitHub protection and continuity

The Foundation source repository requires server-side protection of `main` in addition to repository workflow files. `DEC-0016` established hard merge protection; `DEC-0017` adds a controlled availability path so an external CI outage cannot make the durable repository/agent-coordination channel permanently unavailable.

The target source configuration is two layered GitHub branch Rulesets:

- `foundation-main-core-safety`: no bypass actors; PR required, linear history, no force push, no deletion;
- `foundation-main-ci-gates`: strict required checks `validate` and `registry-integrity`; the authorized source maintainer may bypass **for pull requests only**.

Break-glass is permitted only after explicit classification as `INFRASTRUCTURE_UNAVAILABLE`. A check that ran and found a substantive defect is `VALIDATION_FAILURE` and must not be bypassed. `UNKNOWN` remains non-bypassable. Break-glass keeps the PR/audit path, requires local/manual evidence where available, records residual risk, and creates deferred-validation debt that must be discharged after service recovery.

GitHub read-back on 2026-08-26 verified both active Rulesets on `main`: `foundation-main-core-safety` (ID `21588442`) has no bypass actors, and `foundation-main-ci-gates` (ID `21588444`) has only the authorized source maintainer with `pull_request` bypass plus strict `validate` and `registry-integrity`. Effective branch rules retain pull-request-only change, linear history, non-fast-forward, and deletion protection. The legacy classic protection endpoint returned HTTP 404 only after both replacement Rulesets had been verified. `WI-0017` is complete.

This is a **Foundation source-project requirement**. Target projects receive `REPOSITORY_CONTINUITY_POLICY.md` and an explicit recommendation when mandatory external CI can become an availability single point of failure, but Foundation transfer never creates bypass permissions or repository Rulesets silently.

## Cross-platform transfer integrity

Foundation 1.7.0 includes the Windows/Git portability fix developed under `WI-0016`. The installer and validator share `tools/content_equivalence.py`: UTF-8 LF and CRLF representations compare equal, while lone CR, final-newline changes, actual text changes, non-UTF-8 data, and binary differences remain significant.

A target repository's `.gitattributes` is not modified merely to make Foundation validation green. Existing target EOL policy remains project-owned. The autonomous regression test creates a temporary Git repository, enables `core.autocrlf=true`, installs and commits Foundation, forces a fresh checkout, verifies re-plan/validation without false drift, introduces a real edit, verifies drift detection, and then removes the temporary repository.

Versioning follows Semantic Versioning. PATCH fixes defects without new governance requirements; MINOR adds backward-compatible rules/capabilities/adapters or improves installation/integration semantics; MAJOR changes authority or governance incompatibly.

The Foundation repository and the transferable rule set have separate scopes. Project README, root LICENSE, changelog, project context, status, handover, backlog, roadmap, Foundation-internal decisions, identity registry, tests, and unlisted tools are Foundation-project artifacts and are never transferred merely because they exist. The manifest may explicitly whitelist optional capability files; those files are transferred only when the capability is selected. The dedicated attribution notice is the Foundation licensing/provenance artifact included with transferred material.

## Rule-context analysis reuse

Foundation 1.8 adds the `foundation-rule-context-cache/v1` contract. Native Codex instruction discovery still runs at every new run/session. Once the applicable additional rules have been fully analyzed, later waves may reuse session-local analyses only after a deterministic check of repository/worktree identity, repository-relative working directory, exact instruction precedence, discovery fallback/byte-limit settings, actual working-tree content, Git `HEAD`/index/dirty state, source identity, and transitive dependencies.

The decision states are `CACHE_HIT`, `PARTIAL_INVALIDATION`, and `CACHE_MISS`. A non-instruction content/Git-state change invalidates that source and transitive dependents while preserving independent analyses. Any instruction, scope, source-set, rename/delete, dependency-topology, contract/schema/generator, corruption, incomplete discovery, byte-limit, or uncertainty change is a full miss. Portable UTF-8 LF/CRLF equivalence is shared with the existing Foundation content policy.

The optional `rule-context-cache` capability supplies a dependency-free reference planner. Semantic analysis remains session-local under content/dependency-addressed keys. Persistent records are optional local non-versioned acceleration metadata: they contain no rule text, summaries, prompts, secrets, environment values, or absolute host paths; they have no authority/evidence status and are atomically written under a per-record lock.

For existing repositories, semantic integration preserves target-owned governance. Foundation `REQUIRED` rules are minimum floors; stricter target rules are compatible. Existing target policy vocabularies do not need to be rewritten into Foundation terms when a semantic mapping is sufficient.

Persistent identifier integration follows the same compatibility rule. Existing published identifiers are preserved by default. `ADOPT_FORWARD` may introduce a better profile prospectively while retaining history; `MIGRATE_EXPLICIT` requires a separate explicit migration decision. Foundation installation never treats missing input as migration authority.

Artifact registration is implementation-language neutral. Existing compatible issue trackers, databases, services, scripts/modules, and applications remain valid Registration Authorities. Humans and AI must use the same authority for the same scope; Foundation reference clients do not replace project tooling implicitly.

For repository-native JSON authorities, v1.6 introduced `foundation-artifact-registry/v2` as the default profile. Complete records live in one canonical JSON registry. The next numeric reference is derived from existing canonical keys plus live reservations; `next_sequence` is not stored. Git-native concurrency uses Git state rather than a second mutable registry counter. The v1 allocation-only profile remains compatible for existing projects.

A central JSON registry is not trusted to Git's text merge semantics. The optional `artifact-registry-github` capability computes an object/property-level three-way merge, runs cross-record integrity checks, performs early cross-PR collision preflight, simulates the Git file merge, and blocks when Git's parsed result differs from the semantic expected result.

Foundation upgrades are semantic as well as file-based. `foundation/feature_catalog.json` records when reusable features were introduced or materially changed, their transfer sources, applicability signals, and recommendation/decision semantics. An upgrade from an older installed version must assess every catalog candidate; relevant improvements such as persistent identity/nomenclature and repository continuity must be surfaced without relying on the user to remember to ask.

Transfer completeness is part of source-project correctness. `foundation/manifest.json#ruleset_version` is the single version authority. Managed reusable policies, schemas, and capability payloads must be classified by the manifest in the same change that introduces them. `tools/transfer_manifest_guard.py` blocks unclassified managed sources, capability payloads outside registered roots, unresolved contract mappings, and version-mirror drift. `tools/feature_catalog_guard.py` additionally blocks transferable sources that lack semantic feature coverage and, in changed-source CI, requires a ruleset bump plus feature-catalog review for every changed transferable source. A stale installed target version is not evidence about current source capability availability.

Foundation validation establishes deterministic Foundation integration/integrity only. Project-specific semantic validation and runtime/empirical validation remain target-repository responsibilities and are not replaced by Foundation installation.

Upgrades are explicit and impact-based. Never auto-upgrade or auto-downgrade a target repository. Compute the complete semantic feature delta before selecting project choices, classify file states as `CREATE`, `UNCHANGED`, `MERGE_REQUIRED`, or `CONFLICT`, then use the semantic integration classes for meaningful rule overlaps. Preserve project-specific rules, identifier history, Registration Authorities, project-selected tooling, and repository-administration choices and report real conflicts rather than normalizing the target repository to Foundation wording.
