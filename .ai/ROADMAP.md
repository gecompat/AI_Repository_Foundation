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

## v1.7 — Portable transfer integrity and repository continuity

- shared UTF-8 LF/CRLF equivalence for installation and validation without hiding real content drift;
- cross-platform checkout regression coverage;
- layered required-check availability semantics with no bypass for validation failures;
- optional pull-request-only continuity procedure while unbypassable branch safety remains active.

## v1.8 — Rule-context cache

- native instruction discovery remains mandatory for each new run;
- optional content-free fingerprint/dependency records support explainable cache hits and targeted invalidation;
- scope, instruction, topology, source-set, schema, corruption, or uncertainty changes fail closed to a full reread.

## v1.9 — Dynamic cost-aware model routing

- provider-neutral router v1 contracts and opt-in reference CLI/MCP/launcher/snapshot paths;
- hard privacy, authority, capability, context, quality, freshness, and budget filters before complete cost-of-success ranking;
- runtime model/price discovery, bounded assessment, conditional affinity, and external content-free state;
- Ollama Cloud is one replaceable provider adapter, not a Foundation dependency.

## v1.10 — Runtime-neutral AI work

- `foundation-ai-work/v1` contracts for open task classes, capabilities, plans, evidence, gaps, and truthful terminal states;
- optional decision-only planner with no invocation or provisioning authority;
- payload/control-plane separation, deterministic-tool preference, risk-gated validation, and isolated failure.

## v1.11 — Router v2, neutral adapters, and resource economics

- router v2 execution boundaries, isolated provider fragments, health/quality/resource provenance, and last-known-good behavior while preserving v1;
- language-neutral JSONL/stdio protocol plus Ollama local/cloud, OpenAI-compatible HTTP, and shell-free command references;
- complete fallback-chain optimization, output-aware context limits, paired evaluation settlement, and hard host-resource constraints;
- evidenced resource money or explainable non-monetary pressure without invented conversion values.

## v1.12 — Resumable execution and validation

- optional exact-plan executor with bounded attempts, time, spend, resources, cancellation, and deterministic/independent validation;
- grouped exact approval receipts, content-free checkpoints, idempotent replay, and manual reconciliation of ambiguous effects.

## v1.13 — Host preparation and cost evidence

- optional `doctor`, `inventory`, `plan-provision`, `provision`, and `verify` reference path;
- expiring hash-bound plans and approvals for exact bounded downloads and offline installation;
- isolated source-backed cost-evidence refresh at most once per source per 24 hours with offline last-known-good reuse.

## v1.14 — Client integration and manual dispatch

- semantic `detect → plan → apply → verify → rollback` integration without blind configuration overwrite;
- native client routing when freshly evidenced, followed by MCP/CLI/launcher and content-separated manual selection;
- requested/actual model receipts and governed, external, quarantined adapter synthesis.

## v1.15 — Transfer provenance and fresh-agent continuation

- portable manifest hashes and content-minimized installation receipts with explicit drift classifications;
- completed clean existing-repository transfer and fresh-agent continuation evidence without treating Foundation integrity as target semantic/runtime validation.

## v1.16 — Interactive runtime configuration and native client routing

- external multi-runtime host/IP/port configuration with safe first-run proposals and exact rollback;
- unconfigured-safe runtime invocation MCP with isolated probe/catalog/invoke paths;
- explicit local/cloud separation, credential references, model selection, and requested/actual evidence;
- expiring provider-neutral client model-routing capabilities and read-only native VS Code role/subagent planning;
- native client dispatch first, then MCP/CLI/launcher, then an expiring manual-selection handoff.

## v1.17 — End-to-end model orchestration with external evidence

- optional catalog-to-router-to-invocation-to-validation orchestration with bounded fallbacks;
- source-backed expiring model profiles without turning runtime observations into permanent policy;
- strict requested/actual alias attestation and content-free reports;
- refresh-on-plan research/evidence inputs, no more than once per source per day, with offline last-known-good reuse;
- unconfigured-safe CLI and stdio MCP entry points while the Foundation default remains rules-only;
- deterministic offline source package with content index and SHA-256 sidecar as project tooling over the same manifest payload.

## v1.17.1 — Current GitHub workflow runtime

- source and optional registry workflows use the current Node-24 GitHub Action generations while preserving permissions, Python, check names, and registry semantics.

## v1.17.2 — Documentation integrity

- source and transferable documentation enumerate the complete shipped AI work/orchestration stack, schemas, dependencies, configuration, external-state, evidence, and degradation boundaries;
- stale limitations, continuation/backlog statements, client references, and time-dependent test evidence are reconciled and regression-protected.

## Later

- evaluate additional provider adapters, v2 registry clients, GUI/IDE frontends, signatures/attestations, or non-GitHub CI integrations only when project evidence justifies them;
- keep normative contracts implementation-neutral and make every executable component replaceable and optional;
- register future work in `.ai/identity/registry.json`; this roadmap is informative and does not itself create backlog authority.
