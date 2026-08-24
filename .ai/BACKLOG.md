# Backlog

Status: INFORMATIVE

Planning is not implementation authority.

| ID | Priority | Status | Title | Dependencies | Acceptance criteria |
|---|---|---|---|---|---|
| FND-001 | high | in_progress | Validate current transfer/integration model | current candidate | Deterministic validator/tests and CI are green; existing-repository AI transfer is validated; fresh-agent post-transfer continuation is executed and recorded |
| FND-002 | high | proposed | Add manifest hashes and installed provenance | FND-001 | Drift distinguishes unchanged baseline, intentional override, previous Foundation version, and unknown drift |
| FND-003 | low | proposed | Evaluate packaged release artifact | FND-001 | Package is justified beyond manifest/AI/installer transfer and contains only intended rule artifacts |
| FND-004 | low | proposed | Optional adapter modules | FND-001 | Each adapter is thin, selectable, and validator-covered |
| FND-005 | high | done | Existing-repository semantic merge assistant | FND-001 | Deterministic file plan plus AI protocol classify rule overlaps, preserve active target governance/discovery, and produce bounded reviewable semantic merges; Foundation CI run 32646967820 on `17662ba58a88abee8ef951d22918aa4c5543392d` succeeded |
| FND-006 | high | done | Finalize transferred-rule attribution mechanism | v1.1 transfer model | Dedicated notice is manifest-required, preserves the complete MIT notice, leaves target root license untouched, and is validator/test covered |
| FND-007 | high | done | Separate Foundation and project validation scopes | v1.1 ruleset | Foundation validator owns `FOUNDATION_INTEGRITY`; target semantic/runtime validation remains authoritative |
| FND-008 | high | done | Semantic integration compatibility and discovery contract | existing-repository feedback | Compatibility taxonomy, stricter-project compatibility, root discovery invariant, adapter rule preservation, and repo-map preservation are transferred and machine-readable; Foundation CI run 32646967820 on `17662ba58a88abee8ef951d22918aa4c5543392d` succeeded |
| FND-009 | medium | done | Existing policy interoperability | FND-008 | Richer validation statuses, model-routing policies, and narrow provenance/privacy exceptions are preserved through explicit contracts; Foundation CI run 32646967820 on `17662ba58a88abee8ef951d22918aa4c5543392d` succeeded |
| FND-010 | high | done | Persistent artifact identity and legacy-safe identifier adoption | FND-008 | Layered identity policy, Foundation default profile, existing-project `PRESERVE`/`ADOPT_FORWARD`/`MIGRATE_EXPLICIT` modes, manifest/repo-map contract, direct AI transfer behavior, validator/tests, and v1.3 documentation are consistent; Foundation CI run 32708542537 on `a1f5463d5d32d0e04394303fd6f6aac8846810ce` succeeded |
| FND-011 | high | done | Language-neutral artifact Registration Authority and human/AI creation workflow | FND-010 | Normative registration contract and schemas are core; humans and AI share one authority per scope; `DIRECT`/`DEFERRED` semantics are deterministic; Python is not required; PowerShell and Python reference clients are independent opt-in capability implementations with shared cross-language contract tests; existing compatible allocators are preserved; Foundation CI run 32711801576 on `e56017f06d0084a444c0a812896eb89f1386657b` succeeded |

Existing-repository AI transfer evidence is recorded in `Documentation/Quality/EXISTING_REPOSITORY_AI_TRANSFER_EVIDENCE.md` for five existing repositories. This satisfies the transfer portion of FND-001; only the separate fresh-agent post-transfer continuation criterion remains open.

Allowed statuses: `proposed`, `ready`, `in_progress`, `blocked`, `done`. A completed item must retain traceable evidence.
