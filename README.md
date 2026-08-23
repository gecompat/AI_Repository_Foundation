# AI Repository Foundation

A vendor-neutral, versioned rules foundation for AI-assisted, AI-driven, and human-maintained technical and knowledge projects. Its goal is safe continuation without chat history, memory, personal prompts, or a specific vendor.

## v1.2 integration model

The Foundation repository itself is **not** a template to unpack into another repository. Its README, root LICENSE, changelog, project state, backlog, handover, internal decisions, tests, and tool source belong only to this Foundation project.

`foundation/manifest.json` is the explicit whitelist of reusable rules/provenance. `Documentation/Standards/SEMANTIC_INTEGRATION_POLICY.md` defines how those rules coexist with mature target-project governance.

A target repository keeps its own README, root license, architecture, project context, decisions, state, backlog, model policy, validation system, and implementation.

## Two equivalent transfer paths

### Directly by an AI

An AI with read access to this repository and write access to the target repository reads:

1. `foundation/manifest.json`;
2. `foundation/AI_TRANSFER.md`;
3. `Documentation/Standards/SEMANTIC_INTEGRATION_POLICY.md` for an existing repository;
4. only the manifest-listed source rules/provenance it needs.

For existing repositories the AI preserves target governance, classifies semantic overlaps, ensures active project rules remain discoverable from root `AGENTS.md`, and never drops unique rules merely to thin a tool adapter.

### Deterministic local installer

Preview only (default):

```text
python tools/install_foundation.py TARGET
```

Apply when the plan contains only `CREATE` and `UNCHANGED` states:

```text
python tools/install_foundation.py TARGET --apply
```

The installer classifies selected target files as `CREATE`, `UNCHANGED`, `MERGE_REQUIRED`, or `CONFLICT`. It never overwrites a differing file. For semantic merges into an existing repository, use the direct AI transfer protocol or resolve the reported merge explicitly.

Adapters default to GitHub Copilot, Claude Code, and Gemini as recommendations. Use `--adapters none` or an explicit comma-separated adapter list when desired.

## Semantic compatibility

Foundation `REQUIRED` rules are minimum protected floors. A target project may be stricter. Existing mature project policies may remain more detailed.

Semantic integration distinguishes equivalent, stricter, selectable override, complementary, duplicate, required-conflict, target-internal-conflict, orphaned-authority, and misplaced-adapter-governance cases. See `Documentation/Standards/SEMANTIC_INTEGRATION_POLICY.md`.

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

The target validation command checks **Foundation integration only** (`FOUNDATION_INTEGRITY`). It does not replace project-specific semantic/static validation (`PROJECT_SEMANTIC`) or executable/empirical validation (`RUNTIME_EMPIRICAL`). Target projects may retain richer validation statuses as long as Foundation reserved meanings are not redefined.

Run deterministic Foundation tests:

```text
python -m unittest discover -s tests -v
```

## Core principles

- repository state is durable project truth;
- only rules/provenance in the transfer manifest are reusable installation payload;
- active project governance remains discoverable from root `AGENTS.md` after integration;
- stricter project rules are compatible unless a real logical/required-floor conflict exists;
- normal operations inside the current task's authorization envelope do not create repeated confirmation gates;
- privacy gates depend on data classification, destination, and handling authority, not merely on information being real;
- model/resource routing uses `LOCAL`, `ECONOMICAL`, `BALANCED`, and `FRONTIER` as portable semantics while target routing may be more detailed;
- Foundation validation supplements rather than replaces project-specific validation;
- adapters are thin discovery bridges only after unique adapter governance has been preserved elsewhere.

## License

The Foundation project is MIT-licensed. Installing Foundation rules never replaces or silently selects the target repository's own root license. The dedicated namespaced Foundation notice carries the source-license attribution required for copied Foundation material.
