# Handover

Status: GENERATED/EVIDENCE

## Current state

Foundation v1.0.0 baseline is defined. The next contributor must begin at `AGENTS.md`; no chat history is required.

## Next actions

1. Run `python tools/foundation_validator.py`.
2. Bootstrap a new empty temporary repository with `--dry-run`, then apply.
3. Run the identical bootstrap again and confirm no planned writes.
4. Validate the generated repository.
5. Ask a fresh agent with repository-only context to explain purpose, rules, allowed actions, validation, and next work.
6. Record actual evidence in `.ai/PROJECT_STATUS.md`.

## Open constraints

- Bootstrap intentionally refuses all overwrites.
- Validator uses only the Python standard library and performs deterministic checks; it does not replace semantic privacy review or a dedicated secret scanner.
- Vendor discovery behavior can change and must be rechecked against current primary documentation before changing adapters.