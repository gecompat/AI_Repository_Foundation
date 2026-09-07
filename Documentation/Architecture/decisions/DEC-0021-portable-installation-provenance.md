# DEC-0021 — Installed Foundation provenance uses portable manifest hashes and explicit override receipts

- Status: Accepted
- Date: 2026-09-07
- Scope: `WI-0002`, Foundation transfer, installation, semantic integration, upgrade and drift validation

## Context

The transfer manifest identified the selected source and target paths but did not bind each row to content. Target validation could detect only whether installed content differed from the current checkout. It could not distinguish a deliberate semantic merge from unrecorded drift or an intact older Foundation installation. Raw working-tree byte hashes would also reintroduce false drift when Git materializes UTF-8 Foundation text as LF or CRLF on different platforms.

## Decision

Every manifest transfer row carries `source_sha256`, computed over UTF-8 content after CRLF-to-LF normalization and over exact bytes for non-UTF-8/binary content. This is the same narrow equivalence rule used by installation planning and drift validation. Source-side guards fail closed when a declared hash is missing, malformed, or stale.

A completed deterministic install or direct semantic transfer records a generated target-owned `.ai/foundation/installation-provenance.json` receipt conforming to `foundation-installation-provenance/v1`. The receipt binds the ruleset version, public source repository, exact source commit when established, portable source-manifest hash, selected adapters/capabilities, and portable source/installed hashes for every selected file. It records `FOUNDATION_BASELINE` only for equal hashes and `INTENTIONAL_OVERRIDE` only for a differing hash plus a non-empty semantic-integration reason.

Target validation classifies each selected installed file as `UNCHANGED_CURRENT_BASELINE`, `INTENTIONAL_OVERRIDE`, `PREVIOUS_FOUNDATION_VERSION`, or `UNKNOWN_DRIFT`. A missing, malformed, inconsistent, future-version, stale-current-manifest, unexplained, or subsequently changed receipt/file combination fails closed to `UNKNOWN_DRIFT`. The legacy `LOCAL_OVERRIDE_OR_DRIFT` warning remains available as a compatibility umbrella for differing namespaced files.

The receipt is generated installation state, not a source payload row. Its schema and governing policy are transferred as core. It contains no target content, prompt, response, credential, absolute host path, or private runtime state. It is neither a signature nor authorization, semantic approval, or proof of target validation.

## Alternatives rejected

- Comparing only with the current Foundation checkout cannot identify an intact previous version or a deliberate recorded merge.
- Treating any differing file as an intentional local override would hide accidental or malicious drift.
- Exact working-tree byte hashes would contradict the established LF/CRLF portability contract.
- Hashing only the overall manifest would not provide per-file diagnosis.
- Committing a reusable receipt template would confuse generated target installation state with transferable source material.

## Consequences

Foundation 1.15 adds one core schema, manifest row hashes, deterministic hash refresh/check tooling, automatic idempotent receipt creation for clean installs, explicit post-merge receipt recording, and exact validator classifications. Older installations without receipts remain usable but cannot claim intentional provenance; differences remain unknown until a legitimate upgrade or semantic integration records them.
