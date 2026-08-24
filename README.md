# AI Repository Foundation

A vendor-neutral, versioned rules foundation for AI-assisted, AI-driven, and human-maintained technical and knowledge projects. Its goal is safe continuation without chat history, memory, personal prompts, or a specific vendor.

## v1.4 integration, identity, and registration model

The Foundation repository itself is **not** a template to unpack into another repository. Its README, root LICENSE, changelog, project state, backlog, handover, internal decisions, tests, and unlisted tool source belong only to this Foundation project.

`foundation/manifest.json` is the explicit whitelist of reusable core material and optional capabilities. `Documentation/Standards/SEMANTIC_INTEGRATION_POLICY.md` defines coexistence with mature target-project governance. `Documentation/Standards/PERSISTENT_IDENTITY_POLICY.md` defines long-lived artifact identity. `Documentation/Standards/ARTIFACT_REGISTRATION_POLICY.md` defines how humans and AI create/register those artifacts through the same project authority without depending on Python, PowerShell, or any other language.

A target repository keeps its own README, root license, architecture, project context, decisions, state, backlog, model policy, validation system, identifier history, Registration Authority, and implementation.

## Two equivalent transfer paths

### Directly by an AI

An AI with read access to this repository and write access to the target repository reads:

1. `foundation/manifest.json`;
2. `foundation/AI_TRANSFER.md`;
3. `Documentation/Standards/SEMANTIC_INTEGRATION_POLICY.md` for an existing repository;
4. `Documentation/Standards/PERSISTENT_IDENTITY_POLICY.md` when durable identifiers exist or are being introduced;
5. `Documentation/Standards/ARTIFACT_REGISTRATION_POLICY.md` when artifact allocation/creation is in scope;
6. only the manifest-listed core material, requested adapters, and explicitly selected optional capabilities it needs.

For existing repositories the AI preserves target governance, identifier history, and compatible Registration Authorities, classifies semantic overlaps, ensures active project rules remain discoverable from root `AGENTS.md`, and never drops unique rules merely to thin a tool adapter.

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

Optional capabilities default to **none**. To install both artifact-registration reference clients explicitly:

```text
python tools/install_foundation.py TARGET --capabilities artifact-registration-clients --apply
```

This does not make Python the target runtime; the installer is only one Foundation transfer path.

## Semantic compatibility

Foundation `REQUIRED` rules are minimum protected floors. A target project may be stricter. Existing mature project policies may remain more detailed.

Semantic integration distinguishes equivalent, stricter, selectable override, complementary, duplicate, required-conflict, target-internal-conflict, orphaned-authority, and misplaced-adapter-governance cases. See `Documentation/Standards/SEMANTIC_INTEGRATION_POLICY.md`.

## Persistent identity

The Foundation separates:

- opaque persistent machine identity;
- concise human reference;
- historical aliases and external-system references;
- mutable hierarchy/status/classification and explicit relations;
- immutable revision identity;
- current repository/tool locator.

For new projects the default machine identity is an RFC 9562 UUIDv7 represented as a UUID URN when text form is needed. UUIDv4 is a compatible choice. Human references use flat typed project-local forms such as `CAP-0011`, `WI-0473`, `DEC-0067`, and `GATE-0032`; type subcategories, wave, status, parent, owner, and location remain metadata.

Existing repositories do **not** have to adopt those strings. `PRESERVE` is the default when an established convention exists, `ADOPT_FORWARD` enables prospective use of an improved convention while retaining historical IDs, and `MIGRATE_EXPLICIT` is reserved for an explicitly authorized migration with durable mappings and recovery.

## Artifact registration for humans and AI

Final sequential human references require an allocator. The Foundation models that allocator as a **Registration Authority**.

- Humans and AI use the same authority for the same identifier scope.
- `DIRECT` creates the final UID and human reference only through serialized or equivalently unique allocation.
- `DEFERRED` creates the permanent UID immediately and postpones final human-reference allocation until a safe registration point.
- Clients do not discover the "next number" by scanning Markdown, filenames, Git history, or model memory.
- An existing Jira/Azure DevOps/GitHub Issues/database/service/project script/module may remain the authority when compatible.

The normative contract is language-neutral and includes JSON Schemas under `foundation/schemas/`.

The optional `artifact-registration-clients` capability contains two independent reference implementations:

```text
.ai/foundation/reference_clients/artifact_reference.py
.ai/foundation/reference_clients/ArtifactReference.ps1
```

Python is **not required**. PowerShell is a first-class supported reference client. A project may instead use .NET, Bash, Node, a GUI/IDE, an issue tracker, or another compatible implementation.

## Attribution without changing the target license

Transferred Foundation material is MIT-licensed source material. Every core transfer includes `.ai/foundation/AI_REPOSITORY_FOUNDATION_NOTICE.md`, which preserves the complete Foundation MIT notice and applies only to transferred Foundation material, including explicitly selected optional capabilities.

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

Validate an installation that explicitly selected the reference clients:

```text
python tools/foundation_validator.py --target TARGET --capabilities artifact-registration-clients
```

The target validation command checks **Foundation integration only** (`FOUNDATION_INTEGRITY`). It does not replace project-specific semantic/static validation (`PROJECT_SEMANTIC`) or executable/empirical validation (`RUNTIME_EMPIRICAL`). Target projects may retain richer validation statuses as long as Foundation reserved meanings are not redefined. Historical identifier mappings, Registration Authority correctness, actual concurrency, and migration correctness remain target validation responsibilities.

Run deterministic Foundation tests:

```text
python -m unittest discover -s tests -v
```

Foundation CI requires both CPython and PowerShell and executes the same deterministic registration fixtures against both reference clients.

## Core principles

- repository state is durable project truth;
- only manifest-listed core material and explicitly selected optional modules are transferable;
- active project governance remains discoverable from root `AGENTS.md` after integration;
- stricter project rules are compatible unless a real logical/required-floor conflict exists;
- existing durable identifiers are preserved by default and never silently reused or reinterpreted;
- identity is separated from mutable hierarchy, status, phase, owner, location, and external tool assignment;
- humans and AI use the same project Registration Authority for final reference allocation;
- implementation language is project-selectable; Python is not a Foundation runtime requirement;
- optional Foundation reference clients never silently replace compatible project tooling;
- normal operations inside the current task's authorization envelope do not create repeated confirmation gates;
- privacy gates depend on data classification, destination, and handling authority, not merely on information being real;
- model/resource routing uses `LOCAL`, `ECONOMICAL`, `BALANCED`, and `FRONTIER` as portable semantics while target routing may be more detailed;
- Foundation validation supplements rather than replaces project-specific validation;
- adapters are thin discovery bridges only after unique adapter governance has been preserved elsewhere.

## License

The Foundation project is MIT-licensed. Installing Foundation material never replaces or silently selects the target repository's own root license. The dedicated namespaced Foundation notice carries the source-license attribution required for copied Foundation material.
