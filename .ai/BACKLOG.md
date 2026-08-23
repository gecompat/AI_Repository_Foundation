# Backlog

Status: INFORMATIVE

Planning is not implementation authority.

| ID | Priority | Status | Title | Dependencies | Acceptance criteria |
|---|---|---|---|---|---|
| FND-001 | high | ready | Execute v1.0 self-tests | v1.0 baseline | Validator, bootstrap, idempotency, and continuation results recorded |
| FND-002 | medium | proposed | Add manifest hashes | FND-001 | Drift distinguishes unchanged, local override, and unknown drift |
| FND-003 | medium | proposed | Package release artifact | FND-001 | Reproducible archive contains only intended versioned files |
| FND-004 | low | proposed | Optional adapter modules | FND-001 | Each adapter is thin, selectable, and validator-covered |

Allowed statuses: `proposed`, `ready`, `in_progress`, `blocked`, `done`. A completed item must retain traceable evidence.