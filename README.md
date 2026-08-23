# AI Repository Foundation

A vendor-neutral, versioned foundation for repositories developed with AI assistance or by AI agents. Its goal is continuation without chat history, memory, personal prompts, or a specific vendor.

## What v1.0 provides

- a canonical root contract in `AGENTS.md`;
- authoritative project, work, routing, validation, state, and handover files under `.ai/`;
- human-facing privacy, security, documentation, licensing, evidence, dependency, and decision policies;
- thin adapters for GitHub Copilot, Claude Code, and Gemini;
- machine-readable Foundation metadata, adapter registry, and repository map;
- local, dependency-free bootstrap and validation tools.

## Start here

1. Read `AGENTS.md`.
2. Review `.ai/PROJECT_CONTEXT.md` and `.ai/PROJECT_RULES.md`.
3. Run `python tools/foundation_validator.py`.
4. For a target repository, preview with `python tools/bootstrap.py TARGET --dry-run`.

The bootstrap tool never overwrites existing files. Review every planned write, especially for an existing repository. The target project's license remains an independent decision; copied Foundation material remains subject to this repository's MIT license.

## Status

Foundation version: **1.0.0**. The repository is intended to validate itself. See `.ai/PROJECT_STATUS.md` for evidence and known pending validation.

## License

MIT. See [LICENSE](LICENSE).