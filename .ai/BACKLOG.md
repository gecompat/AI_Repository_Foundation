# Backlog

Status: INFORMATIVE

Planning is not implementation authority.

| ID | Priority | Status | Title | Dependencies | Acceptance criteria |
|---|---|---|---|---|---|
| FND-001 | high | in_progress | Validate current transfer/integration model | current candidate | Deterministic validator/tests and CI are green; fresh-agent semantic transfer/continuation is executed and recorded |
| FND-002 | high | proposed | Add manifest hashes and installed provenance | FND-001 | Drift distinguishes unchanged baseline, intentional override, previous Foundation version, and unknown drift |
| FND-003 | low | proposed | Evaluate packaged release artifact | FND-001 | Package is justified beyond manifest/AI/installer transfer and contains only intended rule artifacts |
| FND-004 | low | proposed | Optional adapter modules | FND-001 | Each adapter is thin, selectable, and validator-covered |
| FND-005 | high | done | Existing-repository semantic merge assistant | FND-001 | Deterministic file plan plus AI protocol classify rule overlaps, preserve active target governance/discovery, and produce bounded reviewable semantic merges; Foundation CI run 32646967820 on `17662ba58a88abee8ef951d22918aa4c5543392d` succeeded |
| FND-006 | high | done | Finalize transferred-rule attribution mechanism | v1.1 transfer model | Dedicated notice is manifest-required, preserves the complete MIT notice, leaves target root license untouched, and is validator/test covered |
| FND-007 | high | done | Separate Foundation and project validation scopes | v1.1 ruleset | Foundation validator owns `FOUNDATION_INTEGRITY`; target semantic/runtime validation remains authoritative |
| FND-008 | high | done | Semantic integration compatibility and discovery contract | existing-repository feedback | Compatibility taxonomy, stricter-project compatibility, root discovery invariant, adapter rule preservation, and repo-map preservation are transferred and machine-readable; Foundation CI run 32646967820 on `17662ba58a88abee8ef951d22918aa4c5543392d` succeeded |
| FND-009 | medium | done | Existing policy interoperability | FND-008 | Richer validation statuses, model-routing policies, and narrow provenance/privacy exceptions are preserved through explicit contracts; Foundation CI run 32646967820 on `17662ba58a88abee8ef951d22918aa4c5543392d` succeeded |

Allowed statuses: `proposed`, `ready`, `in_progress`, `blocked`, `done`. A completed item must retain traceable evidence.
