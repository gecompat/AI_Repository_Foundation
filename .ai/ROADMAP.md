# Roadmap

Status: INFORMATIVE

## v1.0 — Baseline

Initial governance, metadata, adapters, bootstrap skeleton, and validator skeleton.

## v1.1 — Safe transfer and operational hardening

- rules-only transfer manifest;
- direct AI transfer and deterministic installer using the same whitelist;
- authorization envelope and pragmatic privacy classification;
- idempotent new-repository installation;
- conflict-aware existing-repository planning;
- target-aware validator and deterministic self-tests.

## v1.2 — Semantic integration of existing repositories

- compatibility classes for overlapping Foundation/target governance;
- root discovery invariant for active target authority;
- preservation of stricter target rules and richer local policy vocabularies;
- adapter-governance rehome-before-thin contract;
- separation of Foundation integrity from project semantic/runtime validation.

## v1.3 — Persistent identity and references

- layered persistent identity model for durable project artifacts;
- opaque machine UID plus human-reference separation;
- explicit aliases/external references, relations, revision identity, and locators;
- broad Foundation default human-reference prefix registry;
- legacy-safe `PRESERVE`, `ADOPT_FORWARD`, and `MIGRATE_EXPLICIT` adoption modes;
- fork/template/repository split/merge identity semantics;
- machine-readable identity contract and validator/test coverage.

## v1.4 — Language-neutral artifact registration

- one Registration Authority per overlapping final-reference scope;
- same authority for human and AI creation;
- `DIRECT` serialized allocation and `DEFERRED` permanent-UID-first workflow;
- core language-neutral registration policy and JSON Schemas;
- preservation of compatible target issue-tracker/database/service/project allocators;
- opt-in v1 reference-client capability rather than mandatory target runtime;
- independent Python and PowerShell v1 reference clients with shared deterministic contract fixtures;
- capability-aware installer, target validator, and cross-language CI.

## v1.5 — Semantic upgrade applicability

- complete machine-readable Foundation feature catalog across historical ruleset versions;
- deterministic introduced/materially-changed feature delta for upgrades;
- exactly one applicability classification for every upgrade candidate;
- explicit surfacing of recommendations, durable project decisions, and conflicts;
- persistent-identity/nomenclature applicability signals that actively surface `ADOPT_FORWARD` when useful;
- semantic feature coverage for every transferable core/capability source;
- changed-source CI requiring ruleset version bump plus feature-catalog review;
- Foundation source-project migration from active `FND-*` planning IDs to registered `WI-*` references with durable aliases.

## v1.6 — Central repository-native artifact registry

- `foundation-artifact-registry/v2` as the default profile for repository-native JSON Registration Authorities;
- complete artifact records in one canonical JSON object keyed by human reference;
- no persisted `next_sequence`; allocation derives `MAX(canonical sequence)+1` plus live reservations;
- no Git-redundant global registry revision counter; Git state is the concurrency token;
- cross-record UID/alias/no-reuse/relation/graph validation;
- deterministic object/property-level three-way merge over base, current main, and PR head;
- verification that Git's actual textual merge result equals the semantic object merge result;
- early cross-PR collision preflight for human references, UIDs, aliases, and overlapping artifact edits;
- generated Markdown planning views with central JSON remaining the sole authority;
- optional `artifact-registry-github` capability for reference implementation and GitHub Actions;
- Foundation source-project registry migrated to v2 and `.ai/BACKLOG.md` generated from it.

## Later

- optional adapter/capability modules beyond current registration/registry clients;
- stronger drift hashes and installed provenance under WI-0002;
- packaged release artifacts only if they add value beyond manifest-driven transfer;
- evaluate additional v2 reference clients, GUI/IDE frontends, or non-GitHub CI adapters only when project evidence justifies them; keep the normative registry/merge protocol implementation-neutral.
