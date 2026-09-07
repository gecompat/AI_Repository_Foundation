# Project Status

Status: GENERATED/EVIDENCE
Last updated: 2026-09-07
Foundation version: 1.10.0 candidate

## Implemented baseline

- rules/provenance transfer manifest and direct AI transfer protocol;
- semantic integration compatibility taxonomy and root-governance discovery;
- layered validation ownership: `FOUNDATION_INTEGRITY`, `PROJECT_SEMANTIC`, `RUNTIME_EMPIRICAL`;
- persistent identity with `PRESERVE`, `ADOPT_FORWARD`, and explicitly authorized `MIGRATE_EXPLICIT`;
- language-neutral Artifact Registration Authority with `DIRECT`/`DEFERRED` and optional reference clients;
- source-side transfer completeness/version guard and negative regression tests;
- source/installed Foundation version separation;
- complete semantic upgrade feature applicability assessment.

## v1.5 — WI-0013

- semantic `foundation/feature_catalog.json` covering reusable Foundation features from the baseline through v1.5;
- transferred `UPGRADE_APPLICABILITY_POLICY.md`, feature-catalog schema, and upgrade-assessment schema;
- deterministic upgrade-delta computation and mandatory surfacing of recommendations/decisions/conflicts;
- `DEC-0014` records the durable semantic-upgrade applicability decision;
- PR #10 final evidence head `3fec8bad5f7816b7741ef729735aeec56e492c0c` passed Foundation CI run `32735966279` and was squash-merged as `400c175dac222af0c4eaee159caa955e67bbdbb7`.

## v1.6 — WI-0014

- `foundation-artifact-registry/v2` central JSON profile stores complete artifact records in one canonical registry;
- canonical human references are `artifacts` object keys and are not duplicated inside records;
- `next_sequence` is not persisted; next references derive from `MAX(existing canonical sequence)+1`;
- Git commit/blob state is the Git-native concurrency token;
- object-level three-way merge, early cross-PR identity preflight, semantic integrity, and actual Git-merge equivalence are enforced by the optional GitHub capability;
- `.ai/identity/registry.json` is the Foundation source project's canonical v2 planning state and `.ai/BACKLOG.md` is its generated projection;
- `DEC-0015` records the durable central-registry/object-level-merge decision;
- final head `ac7c5011c415f6cf468d980882f45f8cd11b63b8` passed Foundation CI `32837891739` and Foundation Artifact Registry `32837891764` and was squash-merged by PR #11 as `9176ecaea7c972d7f5ec48c66ed19caa0ca68d8c`.

## GitHub merge protection — WI-0015 / DEC-0016

- WI-0015 established the previously verified classic branch protection with pull requests, strict `validate` and `registry-integrity`, up-to-date validation, linear history, no bypass, no force push, and no deletion;
- GitHub API read-back plus manual settings review on 2026-08-25 satisfied WI-0015;
- WI-0017 subsequently migrated the same core protections and CI gates to two layered Rulesets so only CI-gate unavailability has a controlled PR-only bypass path.

## v1.7.0 — WI-0016

- installation planning and target drift validation share `tools/content_equivalence.py`;
- UTF-8 LF and CRLF-only working-tree representations are treated as equivalent;
- lone CR, final-newline changes, true content changes, non-UTF-8 data, and binary differences remain significant;
- direct AI transfer does not create/change target `.gitattributes` merely to silence EOL-only comparison;
- `tests/test_eol_portability.py` creates a temporary Git repository with `core.autocrlf=true`, installs/commits Foundation, forces a fresh checkout, re-plans and validates without false drift, then introduces true drift and verifies detection;
- the first regression implementation exposed a real test-fixture defect; this was correctly treated as `VALIDATION_FAILURE`, not as an outage/bypass candidate, and the fixture was corrected to force a fresh checkout of the tracked Foundation directory;
- corrected focused EOL/Ruleset tests, all deterministic Foundation gates, and the complete 72-test suite succeeded locally on 2026-08-26;
- PR #14 head `fdd67225edaccb912a96f7e2fe1286d0749975c6` passed Foundation CI run `33002938158` and Foundation Artifact Registry run `33002938204`;
- WI-0016 is `done`.

## v1.7.0 — WI-0017 / DEC-0017

- new transferable `REPOSITORY_CONTINUITY_POLICY.md` protects repository availability without weakening validation truth;
- required-check blocking is classified as `VALIDATION_FAILURE`, `INFRASTRUCTURE_UNAVAILABLE`, or `UNKNOWN`;
- break-glass is prohibited for `VALIDATION_FAILURE` and `UNKNOWN` and may be project-authorized only for `INFRASTRUCTURE_UNAVAILABLE`;
- break-glass preserves a PR/audit path, local/manual evidence where reproducible, residual-risk recording, and mandatory post-recovery validation;
- Foundation source GitHub architecture is now active as layered Rulesets:
  - `foundation-main-core-safety` (ID `21588442`): no bypass, PR required, linear history, no force push, no deletion;
  - `foundation-main-ci-gates` (ID `21588444`): strict `validate` and `registry-integrity`, only authorized user `48807214` with `pull_request` bypass;
- `tools/github/configure_rulesets.py` creates/verifies both Rulesets and removes legacy classic protection only after replacement verification;
- `Documentation/Quality/GITHUB_BREAK_GLASS.md` defines exact source procedure and prohibited uses;
- authenticated GitHub read-back on 2026-08-26 verified both exact active Rulesets, their `refs/heads/main` condition, bypass state, required checks, strict policy, and effective combined branch rules;
- classic branch protection was removed only after replacement verification and its endpoint then returned HTTP 404 while `main` remained protected by the Rulesets;
- target projects receive the continuity recommendation but Foundation does not silently create Rulesets/bypass permissions;
- WI-0017 is `done`; DEC-0017 remains `Accepted`.

## v1.8.0 — WI-0018 / DEC-0018

- native Codex discovery of the applicable `AGENTS.override.md`/`AGENTS.md` chain remains mandatory for every new run/session;
- `foundation-rule-context-cache/v1` combines session-local semantic analyses with an optional local, non-versioned fingerprint/dependency record;
- deterministic checks include repository/canonical-root/worktree identity, repository-relative working directory, exact instruction precedence, discovery fallback/size configuration, actual working-tree hashes, Git `HEAD`/index/dirty state, source identity, and transitive dependency topology;
- `CACHE_HIT` reuses only an actually available exact analysis key, `PARTIAL_INVALIDATION` rereads changed non-instruction sources plus transitive dependents, and all instruction/scope/source-set/topology/schema/generator/corruption/uncertainty changes fail closed to `CACHE_MISS`;
- portable UTF-8 LF/CRLF equivalence is preserved while lone CR, final-newline, encoding, binary, and actual content changes remain significant;
- persistent records contain no rule text or semantic summaries, are atomically replaced under a bounded exclusive lock, and cannot be written into a repository unless the destination is untracked and already ignored;
- the reusable policy and schema are core; the dependency-free `rule-context-cache` planner is an explicitly selected optional capability;
- `DEC-0018` is `Accepted`; `WI-0018` is `done` based on the stable local completion gate recorded below.

## v1.9.0 — WI-0019 / DEC-0019

- provider-neutral `foundation-model-router/v1` contracts cover request, decision, catalog, snapshot, and provider profiles;
- deterministic routing filters privacy/remote authorization, capabilities, context, tier, quality, price freshness, failed attempts, and spend bounds before minimizing expected cost of success;
- Cost-of-Success includes estimated attempt and fallback spend, predicted success, failure-recovery value, latency value, conditional session/cache affinity, and fallback reach probability;
- concrete provider/model facts and time-dependent rates are discovered into expiring runtime catalogs; decisions carry a pricing epoch and expire at any eligible candidate's next relevant rate boundary;
- newly discovered models remain `UNASSESSED`; explicitly authorized evaluation plans are capped by candidates, trials, daily spend, and atomic reservations, while the router itself never invokes a model;
- runtime catalogs, aggregate outcomes, hashed session references, reservations, launchers, and snapshots stay outside version control under atomic locking; credentials are not persisted;
- the opt-in capability includes the provider-neutral core/CLI, Ollama Cloud provider adapter, local stdio MCP adapter, shell-free launcher, expiring snapshots, and separate Visual Studio/GitHub Copilot MCP examples;
- graceful degradation is MCP → CLI → launcher/unexpired snapshot → portable Foundation tier without an invented concrete model or price;
- `DEC-0019` is `Accepted`; `WI-0019` is `done` based on the local completion gate and required PR checks recorded below.

## Post-merge model-router audit — WI-0020 / WI-0021

- a 2026-09-07 audit of current `origin/main` against the complete dynamic-routing plan confirmed that the provider-neutral core, Ollama Cloud adapter, live/time-dependent prices, pricing epochs, session/cache affinity, discovery, outside-repository runtime state, CLI, stdio MCP, graceful-degradation paths, client guidance, schemas, transfer metadata, tests, documentation, and aggregate success/latency learning are implemented;
- `WI-0020` tracks a bounded routing-correctness gap: the current implementation chooses the primary by standalone score and only then appends higher-success fallbacks, so it does not minimize Cost-of-Success over the complete chain; context eligibility also checks input context without reserving expected output tokens;
- `WI-0021` tracks a bounded evaluation/accounting gap: evaluation plans do not explicitly encode the required task set, sample count, and stopping rules, and paired candidate/incumbent reservations currently settle only the candidate-reported cost into daily evaluation spend;
- these follow-ups do not reopen completed `WI-0019`; they preserve its implemented baseline and identify only the remaining work demonstrated by code-path and regression-counterexample review.

## System-independent AI work program — DEC-0020 / WI-0022–WI-0029

- `DEC-0020` establishes a runtime-neutral AI work control plane in which deterministic tools, models, retrieval, rendering, validation, external services, and human checkpoints are discovered capabilities rather than mandatory dependencies;
- `WI-0020` and `WI-0021` remain the first router-correctness prerequisites; `WI-0022` through `WI-0028` stage contracts, isolated adapters, resumable execution, total-resource economics, bounded provisioning, client integration, and degradation validation;
- `WI-0029` applies the completed contracts to this Foundation source repository without committing host paths, credentials, model catalogs, payloads, or runtime traces;
- every implementation stage must preserve router-v1 compatibility and leave Foundation governance usable when Python, MCP, network, providers, models, and optional executors are absent.

## v1.10.0 candidate — WI-0022 and WI-0029 partial

- transferable `foundation-ai-work/v1` policy and schemas define content-free `WorkRequest`, `CapabilityDescriptor`, `ExecutionPlan`, `ExecutionReport`, `ValidationEvidence`, `GapReport`, and `ProvisionPlan` contracts;
- privacy, actual authority, data boundary, capability, health/freshness, validation, deadline, monetary, and measured resource constraints precede ranking; missing or uncertain hard-limit facts fail closed;
- the opt-in dependency-free `ai-work` planner invokes nothing, persists nothing, prefers an adequate deterministic capability, isolates unhealthy descriptors, and reports `EXECUTABLE`, `MANUAL_REQUIRED`, `UNAVAILABLE`, or `BLOCKED`;
- `.ai/AI_WORK_PROFILE.md` and `.ai/ai-work/profile.json` apply the contract to this source project with no required provider, external runtime inventory, shell-free mappings to the existing Foundation gate, and explicit no-runtime degradation;
- the profile grants no remote transfer, spend, publication, repository administration, push, or PR authority; `WI-0029` remains in progress until the later adapters/executor and dual-runtime evidence exist.

## Validation evidence

- v1.10.0 contract candidate local gate on 2026-09-07: transfer and semantic feature guards against `3b260c612b318aeeaac08feac724e3c73e770b9c`, central registry/backlog checks, full Foundation validator, JSON parsing, Python compilation, diff hygiene, focused contract/install/upgrade/self-hosting tests, and all 146 tests succeeded on Windows; validator output retained only its two pre-existing non-blocking self-scan warnings.
- PR #19 squash-merged as `3b260c612b318aeeaac08feac724e3c73e770b9c`; the exact merge commit passed post-merge Foundation CI run `34121914451`.
- AI work program registration: PR #19 head `5a0cb7a49e59bd6e5876f2a48391b0e921c7be05` passed Foundation Artifact Registry run `34121700368` and Foundation CI run `34121700457`.
- v1.2.0 semantic integration: Foundation CI run `32646967820`, success.
- v1.3.0 persistent identity: Foundation CI run `32708542537`, success.
- v1.4.0 artifact registration: Foundation CI runs `32711801576` and `32711959226`, success.
- transfer completeness/version guard: Foundation CI runs `32716654407` and `32716818991`, success.
- v1.5 semantic upgrade applicability: Foundation CI runs `32733817943` and `32735966279`, success; merged as `400c175dac222af0c4eaee159caa955e67bbdbb7`.
- v1.6 central registry final: Foundation CI `32837891739`, Foundation Artifact Registry `32837891764`, success; merged as `9176ecaea7c972d7f5ec48c66ed19caa0ca68d8c`.
- classic branch protection verification 2026-08-25: GitHub reports `main` protected with `registry-integrity` and `validate` required for `everyone`; saved repository settings confirm the remaining required controls.
- PR #14 prior head: registry-integrity succeeded; Foundation CI reached the EOL regression and found a project-owned fixture failure. This evidence is intentionally recorded as validation failure, not infrastructure unavailability.
- v1.7.0 implementation head `fdd67225edaccb912a96f7e2fe1286d0749975c6`: Foundation CI `33002938158` and Foundation Artifact Registry `33002938204`, success.
- local completion gate on 2026-08-26: transfer manifest guard, feature catalog guard, central registry validation, backlog projection, full Foundation validator, focused EOL/Ruleset tests, and all 72 unit tests succeeded; validator reported two non-blocking pre-existing warnings.
- v1.8.0 local completion gate on 2026-09-01: transfer manifest guard, feature catalog changed-source review against `d49f978f33001fcc098998ff7c04ffb209b28033`, central registry validation, backlog projection check, full Foundation validator, `git diff --check`, Python compilation/JSON parsing, focused Rule Context Cache regressions, and all 94 tests succeeded on Windows; the validator retained only its two pre-existing self-scan warnings.
- v1.9.0 candidate local gate on 2026-09-07: transfer manifest guard, feature catalog changed-source review against `7ddc29988b23570f462e46ebf527f8dfdd05fd75`, central registry validation, backlog projection check, full Foundation validator, `git diff --check`, Python compilation, every Foundation JSON document parsed, and all 125 tests succeeded on Windows; the validator retained only its two pre-existing self-scan warnings. The public Ollama pricing page parsed successfully with 19 base rows, 2 peak rows, and the documented weekday 12:00–18:00 UTC window; authenticated inventory sync and real model-task quality remain target-owned runtime validation.
- PR #17 implementation head `446fb1b2512f3ed6909db3b8e0418740e36d153a`: Foundation CI run `34065719115` and Foundation Artifact Registry run `34065719116`, success.
- PR #17 final head `7abcc9d5bcf0d3acc6ea5de1a46277de74d4a7cb`: Foundation CI run `34065848433` and Foundation Artifact Registry run `34065848555`, success; squash-merged to `main` as `49c73f3cc2ba4031b83ab343038a16ba2e03bbb4`.
- PR #15 head `4a958344dea5cc8a8b57d2468752c415562e8486` passed Foundation Artifact Registry run `33560909931` and Foundation CI run `33560910019`, was squash-merged as `9a0f949ee0cdba73c8309e9dbb75c077ca21ab06`, and the exact merge commit passed post-merge Foundation CI run `33561041239`.
- source Ruleset migration/read-back on 2026-08-26: active IDs `21588442` and `21588444`; only CI user `48807214` has `pull_request` bypass; classic protection absent after replacement verification.
- Fresh-agent post-transfer continuation without prior conversation context remains `pending manual validation` under `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md`.

WI-0005, WI-0008, WI-0009, WI-0010, WI-0011, WI-0012, WI-0013, WI-0014, WI-0015, WI-0016, WI-0017, and WI-0018 are complete. WI-0001 remains in progress only for the separate fresh-agent continuation criterion.
