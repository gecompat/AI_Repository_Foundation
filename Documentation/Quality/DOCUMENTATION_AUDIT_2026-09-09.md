# Documentation Audit — 2026-09-09

Status: GENERATED/EVIDENCE

- Work item: `WI-0033`
- Audited baseline: `origin/main` at `c29ef2916834460455ec79be225a3632fabaf758` (Foundation 1.17.1)
- Reconciled candidate: Foundation 1.17.2
- Validation scope: `FOUNDATION_INTEGRITY` plus source/document consistency; no claim of universal vendor-runtime behavior

## Scope and method

The audit covered all 65 pre-existing tracked Markdown documents through repository-wide inventory/link/staleness scans and reviewed the root entry points, authoritative maps/policies, source status/handover/roadmap, transfer protocol/templates, capability guides, quality records, manifest, feature catalog, schemas, implementation CLI surfaces, and relevant tests in detail. This evidence record is the candidate's 66th Markdown document.

The review compared documentation against:

- the exact manifest payload, dependency graph, ruleset mirrors, and all 53 tracked JSON files;
- current source and installed repo-map contracts;
- actual `--help` output for the installer, packager, model router, AI-work planner, runtime configuration assistant, executor, host-preparation reference, client integration, and orchestrator;
- current primary documentation for Codex, Visual Studio Code, GitHub Copilot, Claude Code, Gemini CLI, Continue, JetBrains AI Assistant, Cursor, Aider, Ollama, MCP transports, and GitHub Actions;
- historical registry, pull-request, CI, package, transfer, and runtime evidence without rewriting the original observation scope.

## Corrections

1. The architecture overview, transferable ruleset summary, direct-transfer protocol, source/target repo maps, root README, and optional orchestrator guide now enumerate the complete shipped router-v2 and AI-orchestration contracts, schemas, dependencies, commands, evidence rules, external-state paths, and graceful-degradation behavior.
2. The transfer-evidence and known-limitations records no longer describe completed manifest hashing or fresh-agent continuation as pending. The generated backlog footer is corrected at its generator and regression-protected.
3. The client-integration guide now records the current VS Code agent/subagent controls, GitHub Copilot CLI `Auto`/fallback behavior, and current Cursor documentation location while retaining requested-versus-actual attestation limits.
4. Contributor/privacy wording and `.local/` guidance now distinguish ordinary ignored scratch from AI capability state that must remain outside every Git worktree.
5. The roadmap now covers Foundation 1.7 through 1.17.2 and no longer presents the delivered AI capabilities or offline source package as hypothetical future work.
6. Installation and Foundation validators now fail when current repo maps silently omit shipped runtime-evidence or orchestration contracts. Installation/upgrade tests cover the complete schema set and the non-material 1.17.2 documentation reconciliation.
7. The router CLI/launcher regression is bound to its synthetic catalog observation time; it no longer turns red merely because the fixture's real wall-clock expiry has passed.

## Link and source result

- Relative Markdown links checked: all 66 candidate Markdown files, zero missing targets.
- HTTPS references found: 32.
- Automated reachability: 29 documentation/source URLs returned HTTP 200 (including allowed redirects); the ISO 21511 page rejected the automated GET with HTTP 403 but was independently resolved through ISO's current index.
- Deliberate non-documentation exclusions: `https://models.example:8443` is a reserved example endpoint, and `https://ollama.com/api/tags` is an authenticated runtime endpoint rather than a human documentation page.
- Product claims remain dated observations. Reachability alone was not treated as semantic proof; the relevant primary pages and implementation surfaces were read. No claim is made that every vendor/account exposes every documented option at runtime.

## Deterministic validation

The final local candidate passed:

- `py -3.13 tools/transfer_manifest_guard.py` — zero blocking findings;
- `py -3.13 tools/refresh_manifest_hashes.py --check` — zero stale hashes;
- `py -3.13 tools/feature_catalog_guard.py --base origin/main` — zero blocking findings;
- registry v2 validation — 54 artifacts valid;
- generated backlog comparison — exact match;
- `py -3.13 tools/foundation_validator.py --profile full` — zero errors/blocking findings and the two known validator self-scan warnings;
- parsing of all 53 tracked JSON documents;
- `py -3.13 -m compileall -q tools foundation/capabilities`;
- `git diff --check`;
- `py -3.13 -m unittest discover -s tests -v` — all 277 tests passed on Windows in 91.848 seconds.

## Boundary

This audit establishes current repository and transferable-document consistency for the reviewed revision. It does not replace `PROJECT_SEMANTIC` review in a target repository, `RUNTIME_EMPIRICAL` validation of a concrete provider/client/account, publisher signatures for offline packages, or future source revalidation when external product documentation changes.
