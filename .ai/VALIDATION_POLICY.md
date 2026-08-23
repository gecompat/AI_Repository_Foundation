# Validation Policy

Status: AUTHORITATIVE

Use the smallest local, reproducible method that reliably tests the affected contract:

1. reproduction or characterization;
2. focused validation;
3. affected regression or consistency checks;
4. structural/static checks;
5. integration or runtime validation;
6. stable completion gate.

Determine affected artifacts and consumers before selecting checks. Prefer existing tools, synthetic/redistributable fixtures where suitable, mocks, and offline checks. CI confirms a stable result; it is not the primary debugging environment.

Validation applies equally to software, data, research, and documentation: tests, schemas, calculations, links, sources, citations, dates/versions, samples, consistency, reproducibility, and review may all be evidence.

Evidence record:

- method;
- scope;
- environment/platform;
- command or procedure;
- result;
- date;
- limitations.

Statuses have exact meanings:

- `not executed`: no required procedure was run.
- `pending manual validation`: an executable manual plan exists but has not been completed.
- `validated`: the stated procedure actually ran and met its pass criteria.

When human execution is required, create an exact step-by-step manual validation plan containing: ID, objective, contract/risk, prerequisites, environment, initial state, ordered steps, exact commands/UI actions, expected results, pass/fail criteria, outputs to return, cleanup/recovery, limitations, and residual risk. A plan is not evidence that the test passed.

A test with external effects, cost, production impact, or mutation may run without an additional confirmation when that effect is an ordinary and clearly authorized part of the current task's authorization envelope. Gate only effects that exceed the envelope, have ambiguous targets, introduce material unapproved cost, or are destructive/irreversible without exact authority.
