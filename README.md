# AI Repository Foundation

A vendor-neutral, versioned rules foundation for AI-assisted, AI-driven, and human-maintained technical and knowledge projects. Its goal is safe continuation without chat history, memory, personal prompts, or a specific vendor.

## v1.1 installation model

The Foundation repository itself is **not** a template to unpack into another repository. Its README, root LICENSE, changelog, project state, backlog, handover, internal decisions, tests, and tool source belong only to this Foundation project.

`foundation/manifest.json` is the explicit whitelist of reusable rules. Only manifest-listed core rules, the required source-license notice, and selected discovery adapters may be transferred to a target repository.

A target repository keeps its own README, root license, architecture, project context, decisions, state, backlog, and implementation.

## Two equivalent transfer paths

### Directly by an AI

An AI with read access to this repository and write access to the target repository reads:

1. `foundation/manifest.json`;
2. `foundation/AI_TRANSFER.md`;
3. only the manifest-listed source rules/provenance it needs.

The AI can safely merge the marked Foundation bridge into an existing `AGENTS.md` while preserving project-specific rules. It must never infer additional transferable files by scanning this repository.

### Deterministic local installer

Preview only (default):

```text
python tools/install_foundation.py TARGET
```

Apply when the plan contains only `CREATE` and `UNCHANGED` states:

```text
python tools/install_foundation.py TARGET --apply
```

The installer classifies selected targets as `CREATE`, `UNCHANGED`, `MERGE_REQUIRED`, or `CONFLICT`. It never overwrites a differing file. Existing target `README.md` and root `LICENSE` are outside the transfer manifest and therefore do not block installation. For semantic merges into an existing repository, use the direct AI transfer protocol or resolve the reported merge explicitly.

Adapters default to GitHub Copilot, Claude Code, and Gemini. Use `--adapters none` or an explicit comma-separated adapter list when desired.

## Attribution without changing the target license

Transferred Foundation rules are MIT-licensed source material. Every rules transfer includes `.ai/foundation/AI_REPOSITORY_FOUNDATION_NOTICE.md`, which preserves the complete Foundation MIT notice and applies only to the transferred Foundation material.

The target repository's own root `LICENSE` is never copied from the Foundation, replaced, amended, or reinterpreted by the installer or AI transfer protocol.

## Validation

Validate this Foundation project:

```text
python tools/foundation_validator.py --profile full
```

Validate an installed target ruleset from a Foundation checkout:

```text
python tools/foundation_validator.py --target TARGET
```

The target validation command checks **Foundation integration only** (`FOUNDATION_INTEGRITY`). It does not replace project-specific semantic/static validation (`PROJECT_SEMANTIC`) or executable/empirical validation (`RUNTIME_EMPIRICAL`). Existing project validators, documentation contracts, tests, reviews, and manual validation remain authoritative when their contracts are affected.

Run deterministic Foundation tests:

```text
python -m unittest discover -s tests -v
```

## Core principles

- repository state is durable project truth;
- only rules/provenance in the transfer manifest are reusable installation payload;
- normal operations inside the current task's authorization envelope do not create repeated confirmation gates;
- privacy gates depend on data classification, destination, and handling authority, not merely on information being real;
- model/resource routing uses `LOCAL`, `ECONOMICAL`, `BALANCED`, and `FRONTIER` per step;
- Foundation validation supplements rather than replaces project-specific validation;
- validation is local-first and manual validation requires an exact step-by-step plan;
- adapters are thin discovery bridges and never duplicate governance.

## License

The Foundation project is MIT-licensed. Installing Foundation rules never replaces or silently selects the target repository's own root license. The dedicated namespaced Foundation notice carries the source-license attribution required for copied Foundation material.
