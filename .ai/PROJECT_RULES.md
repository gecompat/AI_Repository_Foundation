# Project Rules

Status: AUTHORITATIVE

## Rule classes

- `REQUIRED`: may not be weakened by a target project when safety, privacy, authorization, or integrity would be reduced.
- `DEFAULT`: applies unless an intentional compatible override is documented.
- `PROJECT_SELECTABLE`: must be decided by the target project.

## Required

- Apply the privacy/confidentiality stop-gate before every mutation or transfer.
- Never version secrets or `.local/` content.
- Preserve truthful status and validation evidence.
- Stop on unclear or incompatible third-party rights.
- Protect recovery and require authority for destructive or irreversible work.
- Tool adapters must only perform discovery/import and must not define parallel governance.

## Defaults

- Use `branch_and_pr` for AI-assisted Git changes.
- Prefer local, deterministic, impact-based work and validation.
- Keep changes small, coherent, and free of unrelated cleanup.
- Use synthetic or redistributable data for examples and tests.
- Document durable material decisions with stable IDs.
- No automatic Foundation upgrade or overwrite of local changes.

## Project-selectable

- target-project license;
- merge strategy;
- AI commit attribution;
- additional adapters and capabilities;
- approval thresholds for low-risk implementation;
- language, platform, concrete validation commands, and release process.