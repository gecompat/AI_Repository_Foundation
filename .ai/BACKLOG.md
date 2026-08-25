# Backlog

Status: GENERATED/INFORMATIVE

Canonical planning state is `.ai/identity/registry.json`. Do not edit this table independently.
Historical `FND-*` references remain aliases according to `Documentation/Architecture/IDENTIFIER_MIGRATION_2026-08-24.md`.

| ID | Priority | Status | Title | Dependencies | Acceptance criteria |
|---|---|---|---|---|---|
| WI-0001 | high | in_progress | Validate current transfer/integration model |  | Deterministic validator/tests and CI are green; existing-repository AI transfer is validated; fresh-agent post-transfer continuation is executed and recorded |
| WI-0002 | high | proposed | Add manifest hashes and installed provenance | WI-0001 | Drift distinguishes unchanged baseline, intentional override, previous Foundation version, and unknown drift |
| WI-0003 | low | proposed | Evaluate packaged release artifact | WI-0001 | Package is justified beyond manifest/AI/installer transfer and contains only intended rule artifacts |
| WI-0004 | low | proposed | Optional adapter modules | WI-0001 | Each adapter is thin, selectable, and validator-covered |
| WI-0005 | high | done | Existing-repository semantic merge assistant | WI-0001 | Deterministic file plan plus AI protocol classify rule overlaps, preserve active target governance/discovery, and produce bounded reviewable semantic merges; Foundation CI run 32646967820 succeeded |
| WI-0006 | high | done | Finalize transferred-rule attribution mechanism |  | Dedicated notice is manifest-required, preserves the complete MIT notice, leaves target root license untouched, and is validator/test covered |
| WI-0007 | high | done | Separate Foundation and project validation scopes |  | Foundation validator owns FOUNDATION_INTEGRITY; target semantic/runtime validation remains authoritative |
| WI-0008 | high | done | Semantic integration compatibility and discovery contract |  | Compatibility taxonomy, stricter-project compatibility, root discovery invariant, adapter rule preservation, and repo-map preservation are transferred and machine-readable |
| WI-0009 | medium | done | Existing policy interoperability | WI-0008 | Richer validation statuses, model-routing policies, and narrow provenance/privacy exceptions are preserved through explicit contracts |
| WI-0010 | high | done | Persistent artifact identity and legacy-safe identifier adoption | WI-0008 | Layered identity policy, Foundation default profile, legacy-safe adoption modes, manifest/repo-map contract, direct AI transfer behavior, validator/tests, and v1.3 documentation are consistent |
| WI-0011 | high | done | Language-neutral artifact Registration Authority and human/AI creation workflow | WI-0010 | Normative registration contract and schemas are core; humans and AI share one authority per scope; DIRECT/DEFERRED semantics are deterministic; reference clients remain optional and cross-language |
| WI-0012 | high | done | Block transfer-manifest and ruleset-version drift | WI-0011 | Manifest is the single version authority; managed policies/schemas/capabilities cannot exist unclassified; source-vs-installed version semantics are explicit; negative tests prove omissions/version drift fail |
| WI-0013 | high | done | Semantic Foundation upgrade applicability assessment | WI-0012 | Every introduced/materially changed feature is deterministically assessed once and relevant improvements are surfaced; feature catalog, transfer rules, guards, tests, and CI are green |
| WI-0014 | high | in_progress | Central artifact registry with semantic GitHub merge gates | WI-0013 | Central registry v2 stores complete records without next_sequence; allocation derives MAX+1; object-level three-way merge and actual Git-merge comparison are deterministic; cross-PR collisions are detected early; generated backlog and CI/tests are green |

Existing-repository AI transfer evidence is recorded in `Documentation/Quality/EXISTING_REPOSITORY_AI_TRANSFER_EVIDENCE.md`; the fresh-agent continuation criterion remains tracked by WI-0001.

Allowed work-item statuses are project-governed values such as `proposed`, `ready`, `in_progress`, `blocked`, and `done`.
