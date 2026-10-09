# Foundation user guide

Status: INFORMATIVE

This guide explains how to adopt AI Repository Foundation and choose its optional components. The linked policies and schemas define the rules; these explanations do not create another authority. Commands run from a Foundation checkout unless a step says otherwise. Replace example paths with your own authorized destinations.

## Start with the project, then choose tools

A repository contains the durable project facts: purpose, decisions, instructions, validation, work state, and references. An AI client reads those facts and the current task before acting. Foundation supplies the shared boundaries and discovery structure so that a new person or session can understand and continue the work.

For example, a documentation project may need only the core. A team with an existing issue tracker can keep that tracker as its Registration Authority. A software project can add a model router or execution bridge when it needs automation. Neither installing Foundation nor installing a capability starts a model or grants network, credential, spend, repository, or publication authority.

## Terms you will encounter

| Term | Meaning |
| --- | --- |
| Source project | This repository, including its own development state, registry and decisions |
| Target repository | The project adopting selected Foundation material; it retains its own governance and state |
| Core | Manifest-listed rules, schemas, discovery templates and deterministic runtime helpers transferred in every installation |
| Discovery adapter | A thin product-specific instruction/import bridge, for example the optional Copilot, Claude Code or Gemini files |
| Optional capability | Selectable executable reference code and its guide; a compatible implementation can replace it |
| Runtime adapter | A bridge to an explicitly configured backend over HTTP, JSONL, or the legacy command interface |
| Client | The host using the framework: an IDE, CLI, AI assistant, human-operated tool, or another compatible application |
| Contract | A language-neutral interface or behavior defined by a policy/schema, not a required vendor implementation |
| Registration Authority | The one project-owned allocator of final references within a shared namespace |
| UID / reference / revision | Permanent machine identity / stable human label / immutable version of an artifact |
| Content handle | An allowlisted file reference carrying input or output outside the control response |
| Attestation | Observed execution/model evidence from a configured trusted source; a requested model alone is not evidence |
| Provenance | Which exact source material was installed, with portable hashes and explicit overrides; not semantic approval |

## Minimal installation

Choose a Foundation ref and read its [manifest](../../foundation/manifest.json). `ruleset_version` is the single version authority; the feature catalog explains semantic upgrade changes. For a provider-neutral core preview:

```text
python tools/install_foundation.py ../my-project --adapters none --capabilities none
```

Review selected files and classifications. `CREATE` and `UNCHANGED` permit a clean deterministic apply:

```text
python tools/install_foundation.py ../my-project --adapters none --capabilities none --apply
python tools/foundation_validator.py --target ../my-project --adapters none
```

The result includes a root discovery bridge, a namespaced `.ai/foundation/` ruleset/map, linked standards and schemas, runtime helpers, attribution and installation provenance. It does not copy Foundation's project README, registry, backlog, decisions or handover into your project. The [transfer overview](../../foundation/README.md) and [manifest](../../foundation/manifest.json) give the exact file list.

The reference installer uses Python's standard library. The rules and contracts do not require Python: direct transfer follows [AI_TRANSFER](../../foundation/AI_TRANSFER.md). The core neither requires an AI account nor makes a paid live call. Installer defaults still recommend three product discovery adapters; the explicit `none` selection avoids them.

## Integrating an existing repository

1. Inspect the target's native instruction chain, authority, data handling, validation commands, identity conventions and Registration Authority. Keep existing root README/license and durable project facts.
2. Preview against the exact source ref. `MERGE_REQUIRED` means a differing selected target needs semantic integration; a `CONFLICT` needs its reported cause resolved. Re-running `--apply` does not overwrite either.
3. Use [semantic integration](../Standards/SEMANTIC_INTEGRATION_POLICY.md) to classify overlaps: preserve equivalent/stronger compatible rules, rehome unique adapter governance, and resolve protected-floor conflicts explicitly. Keep active project rules discoverable from the root instruction tree.
4. For upgrades, assess every material candidate from the [feature catalog](../../foundation/feature_catalog.json) under [upgrade applicability](../Standards/UPGRADE_APPLICABILITY_POLICY.md). Existing identifiers default to preservation; optional clients never replace a compatible allocator silently.
5. Assess actual test triggers, duplicate checks, logs, reviews, model calls and polling under [processing efficiency](../Standards/PROCESSING_EFFICIENCY_POLICY.md). A copied policy or a green integrity scan does not establish an efficient workflow. Explain bounded exceptions or keep unresolved choices pending.
6. After authorized semantic merges, record each differing selected file and reason through the installer's `--record-provenance --intentional-override "TARGET=REASON"` path. Run target integrity plus its own semantic and runtime checks. Record what ran, what remains manual and the relevant revision.

See [validation/provenance](../../.ai/VALIDATION_POLICY.md) for receipt semantics and drift classes. Stronger target rules remain valid unless there is a real logical conflict. Foundation does not create repository bypass authority; continuity handling remains project-owned.

## Choose only the capabilities you need

The following dependency names come from the manifest. Dependencies install companion files; they do not configure services or grant permissions.

| Capability | Use it when | Dependencies | Limit / detailed guide |
| --- | --- | --- | --- |
| `artifact-registration-clients` | Humans/AI need Python or PowerShell reference allocation clients | none | Does not replace an existing authority; [registration contract](../Standards/ARTIFACT_REGISTRATION_POLICY.md) |
| `artifact-registry-github` | Git-native v2 registry records need object merge, generated views and PR collision checks | none | GitHub is a reference backend; [central registry](../Standards/CENTRAL_ARTIFACT_REGISTRY_POLICY.md) |
| `rule-context-cache` | Retained analysis can reuse verified persistent fingerprint bindings | none | Records contain no rule authority or reconstructed analysis; [cache policy](../Standards/RULE_CONTEXT_CACHE_POLICY.md) |
| `ai-work` | A task needs an explicit capability plan, gap report or session decision | none | Decision-only; [AI work](../../foundation/capabilities/ai-work/AI_WORK.md) |
| `model-router` | Evidence-backed model choice is useful | none | Decision-only, no invented quality/prices; [router](../../foundation/capabilities/model-router/MODEL_ROUTER.md) |
| `ai-runtime-adapters` | An explicit/pinned/routed model must be invoked through handles | none | Reviewed HTTP or JSONL bridge, not a sandbox; [runtime guide](../../foundation/capabilities/ai-runtime-adapters/AI_RUNTIME_ADAPTERS.md) |
| `ai-executor` | A generic exact `ExecutionPlan` needs execution/checkpoint/validation handling | `ai-work` | No blanket effect authority; [executor](../../foundation/capabilities/ai-executor/AI_EXECUTOR.md) |
| `ai-provisioning` | A host needs inventory or an exact approved provision plan | `ai-work` | No unrestricted installer/download permission; [provisioning](../../foundation/capabilities/ai-provisioning/AI_PROVISIONING.md) |
| `ai-client-integration` | A client's evidenced native/MCP/CLI/manual path needs integration | `ai-work`, `ai-runtime-adapters`, `model-router` | Product configuration is reference data; [client integration](../../foundation/capabilities/ai-client-integration/AI_CLIENT_INTEGRATION.md) |
| `ai-orchestrator` | Catalog → evidence → route → invoke → validate should be composed | `ai-work`, `ai-runtime-adapters`, `model-router` | Missing evidence/attestation or ambiguous outcomes require manual handling; [orchestrator](../../foundation/capabilities/ai-orchestrator/AI_ORCHESTRATOR.md) |

For example, explicitly adding runtime access keeps product discovery adapters disabled:

```text
python tools/install_foundation.py ../my-project --adapters none --capabilities ai-runtime-adapters
python tools/install_foundation.py ../my-project --adapters none --capabilities ai-runtime-adapters --apply
```

Review each new preview. Adding a dependency does not upgrade or semantically merge an existing differing file automatically.

## A complete example: document, validate, continue

Suppose your project maintains a public equipment guide. Your task is to explain one new feature and verify its examples.

1. Install the core using the preview/apply steps above into a new empty `../my-project` directory. Create target-owned context identifying the guide, a validation command for its examples, and a status/handover location. Link that context from the target's root instructions. Foundation provides the boundaries; these facts belong to your project.
2. Read the current task and applicable rules. Classify the guide text as public for its intended repository destination. Use the task's ordinary edit/validation authority; do not invent extra approval gates.
3. If this work needs a durable work item/decision, use the target's Registration Authority. A UID persists even if the title, owner or status changes. Foundation's `WI-*` records are not copied as your target backlog.
4. Write the explanation and execute the selected example checks. Keep runtime-only output outside Git. Record the executed command/result/revision in the target's evidence format. An unexecuted check stays `not executed`; an integrity scan alone does not prove the guide's examples.
5. Update target state and handover with durable references and the next action. A successor session starts with fresh native discovery and repository truth, then reconciles any compact delta. Session counters and a natural boundary can suggest a checkpoint/rotation; they do not rescan the chat or assume the client can create a successor.

This workflow works without a model runtime. To explore the optional invocation path with the same public/synthetic classification, use the deterministic offline demonstration below. It generates fixed synthetic output rather than contacting an AI provider.

### Optional offline Stdio demonstration

Install `ai-runtime-adapters` as above. Save this Python recipe outside both repositories and run it from the Foundation checkout. It creates external configuration and content handles, using the installed demonstration program:

```python
import json
import sys
from pathlib import Path

target = Path("../my-project").resolve()
runtime_dir = target / ".ai/foundation/ai_runtime_adapters"
sys.path.insert(0, str(runtime_dir))
import runtime_configuration as runtime

state = runtime.default_state_dir() / "offline-demo"
connection = runtime._connection_defaults(state, "", "stdio")
connection.update(
    label="Example provider", argv=[str(Path(sys.executable).resolve()), str(runtime_dir / "stdio_demo.py")],
    environment_allowlist=[], execution_boundary="HOST", network_authorized=False,
    model_selection={"mode": "PINNED", "default_model": "synthetic-demo"},
)
store = runtime.ConfigurationStore(state / "runtime.json")
document = runtime.empty_configuration()
document["connections"]["example"] = connection
store.save(document)
input_path = Path(connection["read_roots"][0]) / "public.txt"
input_path.parent.mkdir(parents=True, exist_ok=True)
input_path.write_text("Public synthetic demonstration", encoding="utf-8")
output_path = Path(connection["write_roots"][0]) / "result.json"
print(json.dumps(runtime.execute_adapter(connection, "catalog", {}), indent=2))
print(json.dumps(runtime.execute_adapter(connection, "invoke", {
    "operation_id": "demo-1", "model": "synthetic-demo", "data_class": "PUBLIC",
    "input_path": str(input_path), "output_path": str(output_path),
}), indent=2))
```

On first execution, the output handle contains synthetic JSON, while the control result contains hashes/counts and `REQUESTED_NOT_ATTESTED`. The demo supplies no actual AI model identity, price or quality evidence. A second invocation needs a new output filename; Stdio refuses an existing output handle to exclude stale results. Keep the external files only as long as your handling policy permits, then remove those exact demo artifacts.

For a real backend, select the adapter type first in `runtime_configuration.py configure`. Choose Ollama for its bounded reference discovery, OpenAI-compatible for an explicit HTTP origin, or `STDIO` for your reviewed exact executable/argument list. No generic program is auto-discovered. Use credential references and an explicit environment allowlist; never put secrets or input text into arguments. A provider-specific JSONL wrapper translates the existing protocol to that provider's API without introducing provider governance into the core.

Use `probe`, `catalog`, or `invoke` through the same CLI or `runtime_*` MCP tools. `ROUTER` and `MANUAL` require a concrete model; `PINNED` supplies only its configured model. Network/data/handle restrictions apply before calls. Generic programs can have ambient OS privileges: configure trusted programs and target-owned isolation. An asserted `HOST` boundary must describe the actual backend, not merely where its wrapper runs.

If you add `ai-orchestrator`, fresh source-backed model evidence is also necessary. It may return `MANUAL_REQUIRED` even though probe/catalog work. Missing or untrusted model metadata stays unattested, and aliases require stronger evidence. Timeout, malformed response, or child-reported invocation failure may have occurred after an external effect: reconcile it before retrying. There is no automatic retry of an ambiguous call. These outcomes preserve useful output without pretending execution or validation was proven.

## A bounded orchestrator job from start to completion

Suppose your client should finish an authorized work item and recover from an idle chat without repeated status prompts. Select `ai-orchestrator` explicitly; the core remains usable without it:

```text
python tools/install_foundation.py ../my-project --adapters none --capabilities ai-orchestrator --apply
```

Define work, acceptance conditions, current rules and a shared budget in project-owned artifacts. A reviewed external host configuration references them and enables autonomy explicitly, with a measurable hard budget or a finite dispatch bound. Configure the client's actual capabilities rather than its product name. The [control guide](../../foundation/capabilities/ai-orchestrator/AI_ORCHESTRATOR.md#host-control-configuration) and [schema](../../foundation/schemas/orchestrator-control.schema.json) explain these inputs. External notification destinations need explicit authority.

If the client supports evidenced model selection and startup, provide a start profile and available connection/model pairs. The existing router selects a sufficiently suitable model from fresh capability, quality, boundary and cost evidence. The example tier is BALANCED; the project may choose another. This requires no earlier model to choose the orchestrator model. Without evidence or startup support, select the chat manually. Individual work steps may use other suitable models or deterministic tools; subscriptions do not become fictitious API tariffs.

After registration, completion events drive control. An optional host scheduler checks every 30 minutes without invoking a model. A running or waiting chat produces no prompt. Only confirmed idle, executable remaining work produces one reserved continuation whose message is exactly `HEARTBEAT`: continue this existing job within its current rules and budget. The client checks the grant, deduplicates its action ID, delivers it and records an actual acknowledgment. A duplicate tick or unchanged checkpoint cannot produce another continuation. Without a check before model invocation, leave periodic model wake disabled.

At a session boundary, the existing lifecycle planner may request a checkpoint or rotation. Confirm the old execution path is idle, preserve work/instructions/budget/blockers in the small handoff, then request the successor. Confirm its actual model and startup before assigning ownership. Missing metrics cause no automatic rotation. A failure or ambiguous timeout requires intervention; it does not resume the retired chat or replay startup. New context may reduce subsequent processing, but the framework makes no measured savings claim.

Completion generates one short notification, then no automatic continuation. A required decision or unexpected stop likewise generates one intervention message. Ordinary waiting stays quiet. Pause/cancel block new grants; dispatched effects still require reconciliation. Source failures may use one authorized bounded research task; proposed price/source/mapping data need independent verification before entering the cache. Collection programs are not changed automatically.

Try the complete offline host roundtrip from your target directory:

```text
python .ai/foundation/ai_orchestrator/control.example.py
```

Expected output is five short records: `REGISTER`/`RUNNING` with no action, one `HEARTBEAT` with `RESUME_SESSION`, a duplicate with no action, `EVENT`/`COMPLETED` with `NOTIFY`, then a quiet heartbeat. Every record reports `model_calls: 0`. Temporary synthetic evidence simulates a manually selected chat; no real model, client, transport or scheduler is called. Tests additionally exercise startup/worker routing and confirmed handoff with freely named HarborConsole/CedarCompute and MapleWorkbench/QuartzCompute fixtures. Real hosts must protect configuration/observations from model writes and establish their own capabilities, deduplication and delivery behavior.

## Feature coverage and deeper reading

This map uses every current semantic feature ID from the [catalog](../../foundation/feature_catalog.json). It is a reading map, not another version or applicability authority.

| Catalog feature | Purpose and main boundary | Authority / implementation |
| --- | --- | --- |
| `foundation-baseline` | Shared repository governance; target facts stay project-owned | [Foundation reference](../Standards/FOUNDATION_REFERENCE.md) |
| `rules-only-transfer` | Explicit whitelist transfer; no source-project state copying | [Transfer protocol](../../foundation/AI_TRANSFER.md) |
| `installed-foundation-provenance` | Portable hashes and exact receipts; not semantic approval | [Validation policy](../../.ai/VALIDATION_POLICY.md) |
| `authorization-envelope` | Ordinary task effects proceed within scope; destructive targets need exact authority | [Safe operations](../Standards/SECURITY_AND_SAFE_OPERATIONS.md) |
| `privacy-classification` | Handle data by class, destination and authority; real does not mean confidential | [Data privacy](../Standards/DATA_PRIVACY_AND_CONFIDENTIALITY.md) |
| `foundation-attribution` | Namespaced MIT attribution; preserve target license | [Notice](../../foundation/AI_REPOSITORY_FOUNDATION_NOTICE.md) |
| `layered-validation` | Integrity, semantic and empirical scopes; no invented success | [Validation policy](../../.ai/VALIDATION_POLICY.md) |
| `semantic-integration` | Preserve mature compatible rules; resolve meaningful conflicts | [Semantic integration](../Standards/SEMANTIC_INTEGRATION_POLICY.md) |
| `model-routing-interoperability` | Portable tiers and evidence-based decisions; no mandatory provider | [Model policy](../../.ai/MODEL_ROUTING_POLICY.md), optional `model-router` |
| `persistent-identity` | Stable UID/reference/alias/revision; never silently reassign IDs | [Identity policy](../Standards/PERSISTENT_IDENTITY_POLICY.md) |
| `artifact-registration` | One allocator for humans/AI; language-neutral operations | [Registration policy](../Standards/ARTIFACT_REGISTRATION_POLICY.md), optional clients |
| `semantic-upgrade-applicability` | Complete semantic delta assessment; no automatic target upgrade | [Upgrade policy](../Standards/UPGRADE_APPLICABILITY_POLICY.md) |
| `central-artifact-registry` | v2 object merge, collision checks and generated views | [Registry policy](../Standards/CENTRAL_ARTIFACT_REGISTRY_POLICY.md), optional GitHub backend |
| `repository-continuity-break-glass` | Distinguish failed validation from unavailable infrastructure; target owns bypass rights | [Continuity policy](../Standards/REPOSITORY_CONTINUITY_POLICY.md) |
| `ci-supersession-and-integration-queue` | Preserve current integration evidence; do not cancel authorized mutating work blindly | [Continuity policy](../Standards/REPOSITORY_CONTINUITY_POLICY.md) |
| `rule-context-cache` | Persistent fingerprints with exact invalidation; no reconstructed semantic analysis | [Cache policy](../Standards/RULE_CONTEXT_CACHE_POLICY.md), optional cache planner |
| `ai-work-orchestration` | Capability-oriented plans and narrower model facade; no blanket authority | [Work policy](../Standards/AI_WORK_ORCHESTRATION_POLICY.md), optional `ai-work` / `ai-orchestrator` |
| `orchestrator-job-control` | Opt-in finite jobs, pre-model checks, fenced handoff and quiet deterministic notifications | [Control guide](../../foundation/capabilities/ai-orchestrator/AI_ORCHESTRATOR.md), [work policy](../Standards/AI_WORK_ORCHESTRATION_POLICY.md) |
| `ai-runtime-adapters` | Shared HTTP/Stdio configuration and invocation; trusted backend boundaries remain explicit | [Runtime guide](../../foundation/capabilities/ai-runtime-adapters/AI_RUNTIME_ADAPTERS.md) |
| `ai-work-execution` | Exact-plan execution, receipts/checkpoints and limits | [Executor guide](../../foundation/capabilities/ai-executor/AI_EXECUTOR.md) |
| `ai-host-preparation` | Diagnosed, bounded approved provisioning; code installation grants no downloads | [Provisioning guide](../../foundation/capabilities/ai-provisioning/AI_PROVISIONING.md) |
| `ai-client-integration` | Evidenced native/MCP/CLI/manual dispatch; no universal client settings syntax | [Client guide](../../foundation/capabilities/ai-client-integration/AI_CLIENT_INTEGRATION.md) |
| `session-lifecycle-management` | Metadata-only rotation and delta bootstrap; actual session creation remains client-owned | [AI work guide](../../foundation/capabilities/ai-work/AI_WORK.md) |
| `bounded-processing-efficiency` | Scoped reading, exact session reuse, finite budgets; no provider spending enforcement | [Efficiency policy](../Standards/PROCESSING_EFFICIENCY_POLICY.md) |
| `processing-overhead-assessment` | Inspect actual tests/logs/reviews/model routes; explain bounded stronger exceptions | [Efficiency policy](../Standards/PROCESSING_EFFICIENCY_POLICY.md) |

For component relationships and failure paths, continue with the [architecture overview](../Architecture/OVERVIEW.md). For Foundation development checks use the [README completion commands](../../README.md#source-completion-checks). The current [status](../../.ai/PROJECT_STATUS.md) and [handover](../../.ai/HANDOVER.md) are evidence; older dated sections do not define current source availability. Release history belongs in the [changelog](../../CHANGELOG.md).
