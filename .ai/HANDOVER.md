# Handover

Status: GENERATED/EVIDENCE

## Current state

Foundation 1.17.2 is the `WI-0033` documentation-integrity candidate. It reconciles the source and transferable overview, maps, ruleset/transfer summaries, capability guides, roadmap, state/evidence boundaries, and current client references with the contracts already shipped through Foundation 1.17. The validators now detect omitted evidence/orchestration map entries, the generated backlog no longer reports completed fresh-agent work as pending, and the time-sensitive router CLI fixture is deterministic. All 277 tests and the local transfer, hash, feature, registry, backlog, full Foundation, JSON, compile, relative-link, and diff gates pass on Windows. `WI-0033` remains in progress until protected pull-request validation succeeds.

The durable audit scope, findings, source/link method, exact local checks, and evidence boundary are recorded in `Documentation/Quality/DOCUMENTATION_AUDIT_2026-09-09.md`. External product behavior remains a dated runtime/source observation rather than permanent Foundation truth.

## Historical implementation evidence

Foundation 1.17.1 is the validated `WI-0032` compatibility update discovered from the 1.17 post-merge run. Official current action documentation identifies v7 as the Node-24 generation, and GitHub warned that the previous checkout/setup action generations depend on deprecated Node 20. Source CI and the transferable artifact-registry workflow now use `actions/checkout@v7` and `actions/setup-python@v7` while retaining Python 3.12, permissions, check names, and registry semantics. The upgrade catalog surfaces the change from 1.17.0. All 276 tests and deterministic local gates passed on Windows. PR #32 validated implementation head `23c45b4061d70de3a18298fa0e91bb2211be55a6` passed Foundation CI run `34288966540` on macOS, Windows, and Linux plus registry-integrity run `34288966571` without the prior Node-20 annotations.

Foundation 1.17 is the merged `WI-0031` implementation under `DEC-0020`. The optional end-to-end facade composes live isolated catalogs, external source-backed model evidence, router v2, content-handle invocation, deterministic validation, bounded fallback, and content-free reporting. Missing evidence yields a manual handoff; `LOCAL` invokes no model; requested/actual mismatches require exact fresh provider documentation or signed metadata. Evidence sources are shell-free, bounded, last-known-good capable, and attempted at most once per source per 24 hours. Content-free input-bound checkpoints prevent terminal replay and stop interrupted/timeout results for reconciliation before any new catalog or invocation. All 269 tests and local deterministic gates passed on Windows. A real read-only MCP acceptance saw both configured Ollama local/cloud catalogs and correctly returned `MANUAL_REQUIRED` without invoking a model because no profile evidence is configured. The `foundation-ai-orchestrator` MCP is globally registered for Codex with no credential or evidence-source argument. PR #30 was squash-merged as `f19461402d00fc3d8bf1541654672c1e5ec4f1f6`; its exact post-merge Foundation CI run `34285246184` passed.

`WI-0003`, the last proposed project work item, now has a bounded implementation: a deterministic universal source ZIP plus SHA-256 sidecar for offline/air-gapped delivery. It contains exactly the manifest, all manifest-whitelisted selectable sources, the minimum installer runtime, and a generated content index. Verification rejects unsafe, extra, missing, or changed content; extracted no-Git installation preserves the package's validated source commit. The package remains a delivery convenience rather than a signature, authority, or replacement for semantic installation. All 274 tests passed locally. A clean-commit 103-entry package was built and verified outside the repository. PR #31 validated head `625ac11f4cd6f2c8b2dc8f713e87031e2c496a9e` passed Foundation CI run `34287113769` on macOS, Windows, and Linux plus registry-integrity run `34287113759`.

Foundation 1.16 is the validated `WI-0030` implementation under `DEC-0020`. It adds external multi-runtime configuration, safe first-run question/answer setup, an unconfigured-safe runtime stdio MCP bridge, requested/actual model evidence, expiring native client capability descriptors, and a read-only VS Code role/subagent planner. Optional runtimes, Python, MCP, models, providers, network, and credentials remain unnecessary for Foundation integrity. All 257 tests and the local gates passed on Windows; bounded live stdio MCP acceptance selected existing local `qwen3.5:4b` with matching actual-model attestation and content separation. PR #29 implementation head `b7d872a30f78357792232286e3739fac5024ef20` passed Foundation CI run `34273466764` on macOS, Windows, and Linux plus registry-integrity run `34273466770`; `WI-0030` is done.

Foundation 1.15 is the validated `WI-0002` implementation under `DEC-0021`. Manifest rows carry portable content hashes; clean installs write content-minimized receipts; completed direct semantic transfers explicitly record every reasoned override; target validation separates current baseline, intentional override, previous version, and unknown drift. Transfer, feature, registry, backlog, full Foundation, diff-hygiene, focused tests, and all 240 tests passed locally on Windows. The fresh-agent disposable transfer/continuation procedure also passed: a new agent preserved project-owned content, installed 57 exact baselines plus one reasoned `AGENTS.md` override, obtained a zero-warning/error installed-target validation, and continued correctly from repository state alone. PR #28 implementation head `391ba0db2775deef1c5ddcdfe7d842d557b77662` passed Foundation CI run `34153838489` on macOS, Windows, and Linux; Foundation Artifact Registry run `34153838498` passed. `WI-0001` and `WI-0002` are done.

Foundation 1.14.0 was squash-merged by PR #24 as `a52a5c3c0e5c100c06b039318b1e3eecf3263314`; its post-merge Foundation CI run `34145275461` passed. PR #25 was squash-merged as `a50b843a58b17368ed600350d6ae0eb9dc031f81`; post-merge Foundation CI run `34147315393` passed the macOS, Windows, and Linux gates. PR #26 was squash-merged as `39cd94fe56ebfbd4218f971644cda5d0e12fc246`; post-merge Foundation CI run `34148447309` passed the same three-platform gate. This closes the registered `WI-0020`–`WI-0029` AI-work program with a real source-profile planner/adapter/executor path that does not expand authority.

The manual fallback is deliberate: a router recommendation cannot force every chat host to switch models. `MANUAL_DISPATCH_REQUIRED` emits a content-free record plus an external prompt file containing tier/capability/acceptance/validation instructions. A concrete model is named only from fresh privacy-eligible evidence. The selected/actual model still requires matching host execution or response metadata; an accepted parameter, model list, user-visible subagent label, or recommendation alone remains `REQUESTED_NOT_ATTESTED`.

The v1.14 implementation head `a0e0d439c53bc9277aca3a36ca862a3c563e7642` passed Foundation Artifact Registry run `34145206655` and Foundation CI run `34145206653`. Its local gate passed all 222 tests on Windows. No client configuration, runtime, network service, model, credential, or repository external to that branch was mutated during deterministic acceptance.

The `WI-0028` focused 91-test contract/degradation gate and complete 229-test suite pass locally on Windows, together with transfer/feature, registry/backlog, and full Foundation validation gates. PR #25 head `b7878347cb1fe7866ae99bdb55729974d8fa8ca3` passed Foundation CI run `34147019605` on macOS, Windows, and the required Linux `validate` gate; registry-integrity run `34147019778` passed. Separate live acceptance used only loopback and already-installed artifacts: Ollama-local completed one bounded request without leaving a model loaded, and LM Studio completed one bounded OpenAI-compatible request before the test stopped and verified the server it had started. No credential file, download, paid/remote request, or response content was used or retained.

The `WI-0029` source profile plans and executes one deterministic `LOCAL_READ` operation via the neutral JSONL command adapter and optional executor. All configuration, handles, output, and checkpoints are external temporary state; the report is content-free, has no model claim, and resume does not repeat the completed operation. With the optional catalog absent, the same profile returns `MANUAL_REQUIRED`. The focused 97-test platform selection and complete 231-test suite pass locally on Windows, together with all deterministic Foundation gates. PR #26 final head `653a2c9bc3635d5ed355f0d09acc3cb0981d8ddb` passed Foundation CI run `34148362064` on macOS, Windows, and the required Linux `validate` gate; registry-integrity run `34148361996` passed. The squash merge and post-merge run are recorded above. `WI-0029` is done.

The provisioner accepts only exact credential-free file/HTTPS sources and reference install commands declaring network denial. It cannot itself enforce an operating-system network sandbox, so only audited offline installers are admissible; stronger implementations may add sandboxing. Failed source refreshes are also throttled for 24 hours, preventing an unavailable endpoint from creating a retry loop. No live download, paid call, or productive runtime interruption was used for the deterministic tests.

The v1.13 local gate passed transfer/feature guards, registry/backlog checks, full Foundation validation, JSON/compile/diff hygiene, focused provisioning/install/upgrade tests, and all 207 tests on Windows. A separate read-only live check found Ollama 0.33.3 outside `PATH` and the LM Studio CLI on `PATH`; both diagnosis and inventory completed. Cloud-tagged Ollama artifacts were `REMOTE`, and locally listed artifacts stayed `UNKNOWN` until a later execution probe attests their boundary. No runtime evidence was committed.

The 2026-09-07 v1.12 local gate passed transfer/feature guards against `origin/main`, registry validation/backlog projection, full Foundation validation, JSON/compile/diff hygiene, focused planner/executor/install/upgrade tests, and all 190 tests on Windows. The validator retains only its two pre-existing non-blocking self-scan warnings. Runtime state and payload paths remain external; ambiguous non-idempotent external effects require manual reconciliation rather than blind replay.

The previous v1.11 local gate passed all 176 tests. Resource-cost evidence is locally reusable and limits automated refresh per source to once per 24 hours; AI-assisted research remains optional and untrusted until source verification/project configuration.

PR #21 implementation head `cea0d14e525ccb837cfd6d66cbefe0e9355230ed` passed Foundation Artifact Registry run `34130851451` and Foundation CI run `34130851510`.

PR #20 was squash-merged as `3cf4239dca60ed766ac47d135f57f7802e719348`; that exact merge commit passed post-merge Foundation CI run `34125163370`.

The 2026-09-07 v1.10 contract gate is green: transfer/feature guards against `3b260c612b318aeeaac08feac724e3c73e770b9c`, registry/backlog checks, full Foundation validator, JSON/compile/diff hygiene, focused contract/install/upgrade/self-hosting tests, and all 146 tests passed on Windows. The validator has only its two pre-existing non-blocking self-scan warnings.

PR #20 implementation head `f770e01c95314ccee60fa9b0d556bdd8d4cf2faf` passed Foundation Artifact Registry run `34124924485` and Foundation CI run `34124924493`.

PR #19 was squash-merged as `3b260c612b318aeeaac08feac724e3c73e770b9c`; that exact merge commit passed post-merge Foundation CI run `34121914451`.

The 2026-09-07 candidate local gate is green: transfer/feature guards, registry/backlog checks, full Foundation validator, diff hygiene, Python compilation, all Foundation JSON parsing, and all 125 tests passed on Windows. The validator has only its two pre-existing non-blocking self-scan warnings. The live public Ollama price-page compatibility check parsed 19 base rows, 2 peak rows, and the documented weekday 12:00–18:00 UTC window. Authenticated inventory and real task quality are deliberately not claimed without target credentials/workloads.

PR #17 final head `7abcc9d5bcf0d3acc6ea5de1a46277de74d4a7cb` passed Foundation CI run `34065848433` and Foundation Artifact Registry run `34065848555`, then squash-merged to `main` as `49c73f3cc2ba4031b83ab343038a16ba2e03bbb4`.

The 2026-09-07 post-merge audit found two bounded follow-ups while confirming the rest of the requested model-routing scope. `WI-0020` covers full-chain Cost-of-Success optimization and output-aware context bounds. `WI-0021` covers explicit evaluation task/sample/stopping plans plus complete paired-arm reservation settlement and auditable outcome linkage. Both are proposed follow-ups to the implemented `WI-0019` baseline rather than a reversal of its completed status.

Accepted `DEC-0020` and registered `WI-0022`–`WI-0029` define the staged system-independent AI work program. The design keeps rules and contracts usable without an AI runtime, treats Ollama/MCP/Python/providers as optional capabilities, isolates failures, adds an optional risk-gated executor and bounded provisioner, and ends with cross-system degradation plus Foundation source-project self-hosting. `WI-0022` is complete on the candidate branch; isolated adapters are the next implementation stage.

PR #19 head `5a0cb7a49e59bd6e5876f2a48391b0e921c7be05` passed Foundation Artifact Registry run `34121700368` and Foundation CI run `34121700457` for the program-registration baseline.

PR #15 is the Foundation 1.8.0 integration record for completed `WI-0018` and accepted `DEC-0018`. It adds a transferable Rule Context Cache contract/schema and an opt-in reference planner while preserving native Codex instruction discovery. Feature head `4a958344dea5cc8a8b57d2468752c415562e8486` passed Foundation Artifact Registry run `33560909931` and Foundation CI run `33560910019`, then squash-merged as `9a0f949ee0cdba73c8309e9dbb75c077ca21ab06`. The exact merge commit passed post-merge Foundation CI run `33561041239`.

The local completion gate on 2026-09-01 passed transfer/feature guards, registry/backlog checks, the full Foundation validator, diff hygiene, compilation/JSON parsing, focused regressions, and all 94 tests. Post-merge local read-back confirmed the canonical clone and `origin/main` at the same merge commit with transfer, feature, registry, backlog, and Foundation validation green.

PR #14 / branch `codex/eol-portable-transfer-integrity` remains the Foundation 1.7.0 integration record for completed `WI-0016` (portable EOL transfer integrity) and `WI-0017` / accepted `DEC-0017` (repository continuity/break-glass). Its last pre-migration implementation head was `fdd67225edaccb912a96f7e2fe1286d0749975c6`.

The Foundation source repository uses `.ai/identity/registry.json` as canonical v2 planning state. `.ai/BACKLOG.md` is generated from that registry. `WI-0004`, `WI-0020`, `WI-0021`, `WI-0022`, `WI-0023`, and `WI-0025` are `done`; `origin/main` remains the integrated source authority until the current PR merges. Re-read exact current heads and GitHub state before future integration or administration work.

## Rule Context Cache — WI-0018 / DEC-0018

Codex still discovers and applies the complete global/project `AGENTS.override.md`/`AGENTS.md` chain at each new run/session. The cache optimizes only repeated semantic analysis of additional repository governance/context after one complete scoped analysis.

The v1 contract fingerprints repository/canonical-root/worktree identity, repository-relative working directory, exact instruction order, effective fallback/size settings, actual working-tree bytes, Git `HEAD`/index/dirty state, source identity, and transitive dependency topology. It emits:

- `CACHE_HIT` only for an exact validated match and only when the exact session analysis key is available;
- `PARTIAL_INVALIDATION` for changed non-instruction sources, rereading those sources and all transitive dependents;
- `CACHE_MISS` for instruction, scope, source-set, topology, discovery, schema/generator, corruption, incomplete-state, or uncertainty changes.

The optional planner is `foundation/capabilities/rule-context-cache/rule_context_cache.py`. Its `check` operation does not mutate rules or cache state; `record` uses a bounded exclusive lock, a stable recheck, flush, and atomic replacement. Records contain fingerprints/dependency metadata only, never rule text or analysis summaries. In-repository cache paths are accepted only when untracked and already ignored; the planner never edits `.gitignore`.

## EOL portability — WI-0016

A Windows integration exposed a portability defect: Git checkout can materialize transferred UTF-8 Foundation text with CRLF while the Foundation source uses LF. The old byte comparison misclassified EOL-only representation as `MERGE_REQUIRED` / `LOCAL_OVERRIDE_OR_DRIFT`.

The candidate uses shared `tools/content_equivalence.py` in installer and validator. UTF-8 CRLF/LF-only differences compare equal; lone CR, final-newline changes, actual text changes, non-UTF-8 data, and binary differences remain significant. Target `.gitattributes` remains project-owned and is not changed merely to make Foundation validation green.

`tests/test_eol_portability.py` creates a temporary Git repository with `core.autocrlf=true`, installs/commits Foundation, deletes the tracked `.ai/foundation` working-tree directory and checks it out again to force conversion, verifies no false drift, introduces real drift, verifies detection, and cleans up automatically.

An earlier PR-head test used `git reset --hard` without first removing the unchanged working-tree files, so Git on the Linux runner did not rewrite them to CRLF. That test failed substantively. It was correctly treated as `VALIDATION_FAILURE`, not as a GitHub Actions outage or break-glass opportunity. The corrected regression, focused tests, complete 72-test suite, and PR-head checks subsequently succeeded; WI-0016 is complete.

## Repository continuity — WI-0017 / DEC-0017

Mandatory external CI must not be the only availability gate for the durable repository/agent-coordination channel. The new transferable `Documentation/Standards/REPOSITORY_CONTINUITY_POLICY.md` distinguishes:

- `VALIDATION_FAILURE`: check ran and found a substantive defect — break-glass prohibited;
- `INFRASTRUCTURE_UNAVAILABLE`: validation cannot produce a trustworthy result because the execution platform/runners/service are unavailable or materially degraded — project-authorized break-glass may be used;
- `UNKNOWN`: cause not established — break-glass prohibited until classified.

The Foundation source GitHub state is two verified active Rulesets targeting exactly `refs/heads/main`:

- `foundation-main-core-safety` (ID `21588442`): no bypass actors; PR required, zero mandatory approvals, linear history, no force push, no branch deletion;
- `foundation-main-ci-gates` (ID `21588444`): strict required checks `validate` and `registry-integrity`; only user `48807214` may bypass with mode `pull_request` / **For pull requests only**.

This means break-glass never enables direct push to `main`. The PR must record outage evidence, immutable base/head, local/manual checks, unreproduced checks, residual risk, and deferred post-recovery validation. Missing CI remains pending rather than being represented as green.

`Documentation/Quality/GITHUB_BREAK_GLASS.md` defines the source procedure. `tools/github/configure_rulesets.py` implements fail-safe migration: create both Rulesets, read back/verify both, then and only then remove legacy classic branch protection, then verify the Rulesets again.

On 2026-08-26, `tools/github/configure_rulesets.py` created and read back both Rulesets, then removed classic protection, then read both Rulesets again. Independent authenticated GitHub API read-back confirmed the exact actors/rules and effective `main` rules; the classic branch-protection endpoint returned HTTP 404 only after replacement verification. `main` remained reported as protected. WI-0017 is complete.

## Target-project behavior

Foundation 1.9.0 preserves the 1.7 repository-continuity semantics but does not transfer repository-administration changes. Targets are told that making external CI mandatory can create an availability dependency; projects needing continuity should consider separating unbypassable core safety from PR-only bypassable CI gates. Foundation does not silently select bypass actors, create Rulesets, weaken existing protection, or treat missing break-glass configuration as a `FOUNDATION_INTEGRITY` defect.

Rule-context policy/schema are core transfer material; the executable planner remains opt-in. Target adoption preserves stronger project governance and native instruction discovery, selects an authorized local non-versioned cache location, performs a complete first analysis per scope/rule version, and never treats the record as authority or evidence.

Model-routing policy and schemas are core transfer material; the executable `model-router` remains opt-in. Target adoption preserves stronger compatible routing, explicitly authorizes remote data handling, keeps runtime state outside version control, supplies credentials only through the environment, syncs fresh provider data, and merges the appropriate client-specific MCP template. Visual Studio and GitHub Copilot templates are intentionally different.

## Continuation

- Re-read exact `origin/main`, PR head, Required Checks, and Rulesets before any future integration or administration change.
- Re-run rule discovery/fingerprints before each later change wave; absent analysis keys, incomplete discovery, or any uncertainty requires the full-read path.
- Treat the Ruleset IDs and actor/mode read-back above as the 2026-08-26 evidence snapshot; GitHub remains authoritative for current state.
- For future break-glass use, require an actual `INFRASTRUCTURE_UNAVAILABLE` classification and the complete evidence/recovery procedure. Never use it for `VALIDATION_FAILURE` or `UNKNOWN`.

## Remaining project work

`WI-0033` is the only registered open work item and closes when the documentation-integrity pull request passes the protected checks. No other registered work remains open; create further work only from new evidence or requirements.

## Open constraints

- Early cross-PR preflight is a snapshot and cannot replace the final check against current `main`.
- The reference GitHub registry capability treats arrays as atomic merge values unless a project defines narrower safe semantics.
- The central v2 profile is not a high-frequency distributed database; projects with stronger service/database authorities should preserve them.
- GitHub repository-administration controls are outside ordinary Foundation file transfer and must not be silently changed in target repositories.
- Break-glass solves CI-service unavailability only; it cannot make GitHub Git/PR/API itself available during a broader GitHub outage.
- Persistent cache records do not persist semantic analyses; a cross-run fingerprint hit saves analysis only when the exact analysis object is independently available under its validated key.
