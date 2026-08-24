# Project Status

Status: GENERATED/EVIDENCE
Last updated: 2026-08-24
Foundation version: 1.4.0 candidate

## Implemented

- rules/provenance transfer manifest and direct AI transfer protocol;
- dedicated Foundation attribution notice without changing target root licenses;
- authorization-envelope and privacy-classification models;
- layered validation ownership: `FOUNDATION_INTEGRITY`, `PROJECT_SEMANTIC`, `RUNTIME_EMPIRICAL`;
- semantic integration compatibility taxonomy for existing repositories;
- root-`AGENTS.md` project-governance discovery invariant;
- stricter target rules explicitly compatible with Foundation minimum floors;
- adapter-governance preservation/rehome-before-thin contract;
- richer target validation-status interoperability;
- existing project model-routing semantic mapping;
- narrow path-scoped privacy exception guidance for required Foundation provenance;
- target repo-map preservation with optional safe bridge to the Foundation map;
- persistent identity policy separating machine UID, human reference, aliases/external references, relations/classification, revision identity, and locator;
- Foundation default identity profile using RFC 9562 UUIDv7 plus flat typed project-local human references, with UUIDv4 compatible;
- existing-project identifier adoption modes `PRESERVE`, `ADOPT_FORWARD`, and explicitly authorized `MIGRATE_EXPLICIT`;
- language-neutral Artifact Registration Authority contract with one authority per overlapping final-reference scope and the same authority for humans and AI;
- `DIRECT` serialized/equivalent unique allocation and `DEFERRED` permanent-UID-first registration semantics;
- core JSON Schemas for artifact records, registry state, and language-neutral registration requests;
- opt-in `artifact-registration-clients` capability rather than a mandatory target runtime;
- independent dependency-light Python and PowerShell reference clients using the same registry/record contract;
- capability-aware installer and target validator;
- cross-language deterministic contract fixtures and Foundation CI PowerShell runtime coverage;
- `foundation/manifest.json#ruleset_version` as the single source ruleset-version authority;
- machine-readable `transfer_coverage_contract` covering managed core roots, capability roots, fixed core sources, and version mirrors;
- blocking source-side transfer completeness guard for unclassified policies, schemas, capability payloads, invalid capability locations, unresolved contract mappings, and version drift;
- explicit distinction between current Foundation source version/capabilities and an older ruleset installed in a target repository;
- negative regression tests proving that omitted policy/schema/capability entries and version drift fail.

## Validation evidence

- v1.1.2 validation-scope implementation was validated successfully before this candidate.
- v1.2.0 semantic integration implementation: GitHub Actions `Foundation CI`, run `32646967820`, head `17662ba58a88abee8ef951d22918aa4c5543392d`: validated, conclusion `success`.
- Existing-repository AI transfer: `validated` based on successful Foundation integration initiated and completed with AI assistance in five existing repositories: `gecompat/FolioTone`, `gecompat/SQL_Server_Lab`, `gecompat/SQL_Server_Toolbelt`, `gecompat/SQL_Server_Analyze`, and `gecompat/SQL_PerformanceSchulung`. See `Documentation/Quality/EXISTING_REPOSITORY_AI_TRANSFER_EVIDENCE.md`.
- v1.3.0 persistent-identity implementation: GitHub Actions `Foundation CI`, run `32708542537`, head `a1f5463d5d32d0e04394303fd6f6aac8846810ce`: `validated`, conclusion `success`.
- v1.4.0 artifact-registration implementation: GitHub Actions `Foundation CI`, run `32711801576`, head `e56017f06d0084a444c0a812896eb89f1386657b`: `validated`, conclusion `success`.
- v1.4.0 final artifact-registration evidence head: GitHub Actions `Foundation CI`, run `32711959226`, head `b84677b8d591d46addfaea80bf1b9a13042cda18`: `validated`, conclusion `success`; PR #8 was then squash-merged as `07b7405d5dda27f8d3e0a5164e5cfcbe46396e24`.
- Transfer-completeness implementation: GitHub Actions `Foundation CI`, run `32716654407`, head `f8b0d9f35379ebc9ab775bbfc5a8cd9b69c942cf`: `validated`, conclusion `success`. `Guard transfer manifest completeness and version consistency`, `Validate Foundation project and transfer manifest`, and `Run installation, transfer-guard, and cross-language contract tests` all completed successfully.
- The transfer-guard regression suite includes explicit negative cases for version mismatch, an unmanifested reusable policy, an unmanifested schema, an unmanifested capability file, and a capability source outside registered managed roots.
- Fresh-agent post-transfer continuation without prior conversation context: `pending manual validation` under `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md`.

FND-005, FND-008, FND-009, FND-010, FND-011, and FND-012 are complete for their deterministic contracts. FND-001 remains in progress only for the separate fresh-agent post-transfer continuation criterion. The evidence-only final PR #9 head must remain green before merge.
