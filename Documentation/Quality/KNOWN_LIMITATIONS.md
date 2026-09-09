# Known Limitations

Status: INFORMATIVE

- Semantic privacy classification cannot be proven by deterministic scanning; the Foundation distinguishes public/repository-intended, confidential, personal/sensitive, secret, and unknown information to avoid blanket gates.
- The deterministic installer intentionally does not semantically merge differing existing files. It reports `MERGE_REQUIRED`; direct AI transfer applies the semantic integration policy while preserving project-specific content.
- The Foundation validator proves deterministic `FOUNDATION_INTEGRITY` contracts only. It cannot prove `PROJECT_SEMANTIC` correctness or `RUNTIME_EMPIRICAL` behavior.
- The validator can confirm that the Foundation discovery/integration contract is installed, but it cannot deterministically prove that every active target-specific authority in an arbitrary repository has been discovered and classified correctly. Existing-repository integration therefore requires semantic inventory/review by the AI/human performing the merge.
- Target repo-map schemas vary. The Foundation requires preservation and permits a minimal bridge only when the target schema safely supports it; no generic repo-map rewrite is attempted.
- Manifest hashes and installation receipts establish content provenance and distinguish current baseline, intentional override, previous version, and unknown drift. They are not signatures, proof of publisher authenticity, semantic approval, or evidence that target validation passed.
- The optional offline ZIP has a deterministic content index and SHA-256 sidecar but is not cryptographically signed. When publisher authenticity matters, obtain the expected digest through an independently trusted channel.
- Transferred rules carry a dedicated namespaced MIT attribution notice while the target project's root license remains independent and untouched.
- Vendor adapter discovery behavior must be checked against current primary documentation before adapter changes.
- The fresh-agent transfer/continuation criterion passed once with a persisted Codex CLI agent and a disposable synthetic repository, as recorded in `Documentation/Quality/MANUAL_VALIDATION_FRESH_AI_TRANSFER.md`. That evidence does not prove identical discovery or execution behavior for every client, vendor, model, repository shape, or future release.
- Runtime catalog presence proves availability only. Automatic routing still requires fresh source-backed quality/cost/capability/context evidence, and requested-model execution remains unattested without trusted host response/execution metadata. Missing evidence correctly degrades to a manual or unavailable result.
- The Python reference adapters and provisioner restrict argv, handles, redirects, credentials, time, and declared network behavior but do not create an operating-system security sandbox around an allowed child process. Stronger isolation remains a target/runtime responsibility where ambient process permissions are too broad.
