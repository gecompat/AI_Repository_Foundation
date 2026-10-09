# DEC-0024 — Assess actual test, log, review, and model-call overhead

Status: Accepted  
Date: 2026-10-09

## Context

The project rule reviews supplied for SammlungsLotse, SQL_PerformanceSchulung, SQL_Server_Analyze, and SQL_Server_Toolbelt agree that impact-based prose does not ensure impact-based execution. Their reported patterns include full static suites despite existing impact metadata, overlapping direct/suite validators and privacy scans, validator self-tests on unrelated changes, broad runtime path triggers, and development fixes inheriting full qualification matrices. These are structural findings, not measured CI-minute or token savings.

Additional model effort surrounds those cycles: full-log ingestion, review of mechanical readers/receipts and prior reviews, repeated diagnostics at unchanged inputs, and large continuation contexts. Foundation 1.20 supplies bounded defaults but its advisory assessment does not ensure that target workflows implement or explicitly justify them.

## Decision

Require an assessment of actual processing routes at installation/upgrade and material workflow-rule changes. Cover test triggers, duplicate/self-tests, validation phases, log handling, review/delegation, repeated model calls, and unchanged-state polling. Reuse existing assessment and decision records. Implemented behavior, justified bounded exceptions, and reasoned non-applicability are complete dispositions; unresolved choices stay pending and prevent claiming completed efficiency integration. `PROJECT_STRONGER` does not exempt a rule from assessment.

Prefer deterministic local log processing with bounded findings and retained original evidence. Additional model work needs an unresolved semantic question, changed inputs, a new finding, required independent judgment, or an authorized retry/gate. Separate development/integration from qualification/release, validate selectors conservatively, and deduplicate identical checks without dropping distinct assertions. Missing tools permit proportionate bounded inspection, not an invented successful parser or mandatory new framework.

## Consequences

Required gates, current-head/integration binding, qualification oracles, repetitions, privacy, independence, and safe mutating-runtime cleanup remain protected. Existing project rules are amended only within authority; necessary choices receive targeted contextual questions while independent work continues. No target repository or automation changes automatically. Integrity/heuristic checks do not prove actual workflow efficiency, token savings, or provider enforcement; metrics remain measured, estimated, or unknown. Foundation 1.21 exposes the material delta through the transfer catalog and manifest.
