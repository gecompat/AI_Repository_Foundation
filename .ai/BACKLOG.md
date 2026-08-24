# Backlog

Status: INFORMATIVE

Planning is not implementation authority.

Preferred work-item references use the Foundation project's registered `WI-*` convention. Historical `FND-*` references remain aliases according to `Documentation/Architecture/IDENTIFIER_MIGRATION_2026-08-24.md`.

| ID | Priority | Status | Title | Dependencies | Acceptance criteria |
|---|---|---|---|---|---|
| WI-0001 | high | in_progress | Validate current transfer/integration model | current candidate | Deterministic validator/tests and CI are green; existing-repository AI transfer is validated; fresh-agent post-transfer continuation is executed and recorded |
| WI-0002 | high | proposed | Add manifest hashes and installed provenance | WI-0001 | Drift distinguishes unchanged baseline, intentional override, previous Foundation version, and unknown drift |
| WI-0003 | low | proposed | Evaluate packaged release artifact | WI-0001 | Package is justified beyond manifest/AI/installer transfer and contains only intended rule artifacts |
| WI-0004 | low | proposed | Optional adapter modules | WI-0001 | Each adapter is thin, selectable, and validator-covered |
| WI-0005 | high | done | Existing-repository semantic merge assistant | WI-0001 | Deterministic file plan plus AI protocol classify rule overlaps, preserve active target governance/discovery, and produce bounded reviewable semantic merges; Foundation CI run 32646967820 on `17662ba58a88abee8ef951d22918aa4c5543392d` succeeded |
| WI-0006 | high | done | Finalize transferred-rule attribution mechanism | v1.1 transfer model | Dedicated notice is manifest-required, preserves the complete MIT notice, leaves target root license untouched, and is validator/test covered |
| WI-0007 | high | done | Separate Foundation and project validation scopes | v1.1 ruleset | Foundation validator owns `FOUNDATION_INTEGRITY`; target semantic/runtime validation remains authoritative |
| WI-0008 | high | done | Semantic integration compatibility and discovery contract | existing-repository feedback | Compatibility taxonomy, stricter-project compatibility, root discovery invariant, adapter rule preservation, and repo-map preservation are transferred and machine-readable; Foundation CI run 32646967820 on `17662ba58a88abee8ef951d22918aa4c5543392d` succeeded |
| WI-0009 | medium | done | Existing policy interoperability | WI-0008 | Richer validation statuses, model-routing policies, and narrow provenance/privacy exceptions are preserved through explicit contracts; Foundation CI run 32646967820 on `17662ba58a88abee8ef951d22918aa4c5543392d` succeeded |
| WI-0010 | high | done | Persistent artifact identity and legacy-safe identifier adoption | WI-0008 | Layered identity policy, Foundation default profile, existing-project `PRESERVE`/`ADOPT_FORWARD`/`MIGRATE_EXPLICIT` modes, manifest/repo-map contract, direct AI transfer behavior, validator/tests, and v1.3 documentation are consistent; Foundation CI run 32708542537 on `a1f5463d5d32d0e04394303fd6f6aac8846810ce` succeeded |
| WI-0011 | high | done | Language-neutral artifact Registration Authority and human/AI creation workflow | WI-0010 | Normative registration contract and schemas are core; humans and AI share one authority per scope; `DIRECT`/`DEFERRED` semantics are deterministic; Python is not required; PowerShell and Python reference clients are independent opt-in capability implementations with shared cross-language contract tests; existing compatible allocators are preserved; Foundation CI run 32711801576 on `e56017f06d0084a444c0a812896eb89f1386657b` succeeded |
| WI-0012 | high | done | Block transfer-manifest and ruleset-version drift | WI-0011 | Manifest is the single version authority; managed policies/schemas/capabilities cannot exist unclassified; source-vs-installed version semantics are explicit; negative tests prove omissions/version drift fail; Foundation CI run 32716654407 on `f8b0d9f35379ebc9ab775bbfc5a8cd9b69c942cf` succeeded |
| WI-0013 | high | done | Semantic Foundation upgrade applicability assessment | WI-0012 | Every feature introduced or materially changed since the installed target version is deterministically included in the upgrade delta, receives exactly one applicability classification, and relevant improvements such as persistent-identity/nomenclature are surfaced with recommendation/decision semantics; feature catalog, transfer rules, guards, tests, and CI are green; Foundation CI run 32733817943 on `9e91cd21e3941a77cbb2e5a3abbf501c2d6a4788` succeeded |

Existing-repository AI transfer evidence is recorded in `Documentation/Quality/EXISTING_REPOSITORY_AI_TRANSFER_EVIDENCE.md` for five existing repositories. This satisfies the transfer portion of WI-0001; only the separate fresh-agent post-transfer continuation criterion remains open.

Allowed statuses: `proposed`, `ready`, `in_progress`, `blocked`, `done`. A completed item must retain traceable evidence.
