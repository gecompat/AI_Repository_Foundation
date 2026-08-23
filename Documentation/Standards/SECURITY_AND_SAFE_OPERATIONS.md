# Security and Safe Operations

Status: AUTHORITATIVE — REQUIRED

Classify actions as `READ-ONLY`, `LOCAL MUTATION`, `EXTERNAL MUTATION`, or `DESTRUCTIVE / IRREVERSIBLE`.

Before mutation, confirm authority, exact targets, affected systems/data/people, reversibility, backup/recovery, concurrency, cost, and validation. Prefer recoverable and scoped actions. Never broaden task authority merely because a tool can perform an action.

Destructive/irreversible operations, production changes, credential/permission changes, paid actions, external messages, releases, and other material side effects require explicit authority. Use dry-run or preview when available. Re-resolve exact targets immediately before destructive action and stop on ambiguity.

Failures must be bounded by timeouts/cancellation where applicable and must not leave silent partial state. Document recovery and residual risk. Do not weaken privacy, secret handling, or integrity as a project override.