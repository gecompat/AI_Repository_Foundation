# Backlog

Status: INFORMATIVE

Planning is not implementation authority.

| ID | Priority | Status | Title | Dependencies | Acceptance criteria |
|---|---|---|---|---|---|
| FND-001 | high | in_progress | Validate v1.1 transfer model | v1.1 branch | Validator and unit tests pass; CI is green; target README/LICENSE preservation and idempotency are proven |
| FND-002 | medium | proposed | Add manifest hashes | FND-001 | Drift distinguishes unchanged, intentional override, and unknown drift |
| FND-003 | low | proposed | Evaluate packaged release artifact | FND-001 | Package is justified beyond manifest/AI/installer transfer and contains only intended rule artifacts |
| FND-004 | low | proposed | Optional adapter modules | FND-001 | Each adapter is thin, selectable, and validator-covered |
| FND-005 | medium | proposed | Existing-repository merge assistant | FND-001 | Deterministic plan plus AI protocol produce bounded, reviewable semantic merges |
| FND-006 | high | done | Finalize transferred-rule attribution mechanism | v1.1 transfer model | Dedicated notice is manifest-required, preserves the complete MIT notice, leaves target root license untouched, and is validator/test covered; Foundation CI run 32638922019 on `9102a70bc13efb6f1642321ccbcedd56a54d6046` succeeded |
| FND-007 | high | done | Separate Foundation and project validation scopes | v1.1 ruleset | Transferred rules and machine-readable metadata define `FOUNDATION_INTEGRITY`, `PROJECT_SEMANTIC`, and `RUNTIME_EMPIRICAL`; Foundation validator declares its scope; local drift is not semantic approval; Foundation CI run 32642237490 on `f910947fd186c0ed52317238de200b89350d5ce8` succeeded |

Allowed statuses: `proposed`, `ready`, `in_progress`, `blocked`, `done`. A completed item must retain traceable evidence.
