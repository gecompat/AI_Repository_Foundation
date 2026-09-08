# Packaged release artifact evaluation

Status: VALIDATED DESIGN AND IMPLEMENTATION

Work item: `WI-0003`

## Decision

A packaged Foundation source distribution is justified as an additional delivery form, but not as a third installation or governance model.

The existing manifest/direct-AI/installer paths remain authoritative. A deterministic ZIP adds distinct value when a consumer needs:

- one content-addressable file for offline or air-gapped transfer;
- an immutable review subject that can be retained with release evidence;
- verification that a delivery contains the complete selectable Foundation payload and no source-project planning, history, runtime state, or unrelated repository files; or
- installation without a Git client or network connection after the archive was obtained through an authorized channel.

The package is not a signature, software bill of materials, trusted update channel, or authorization to install. Its SHA-256 must be obtained through an independently trusted channel when authenticity matters. Extraction is into a staging directory, never directly over a target repository. Semantic integration still uses `foundation/AI_TRANSFER.md` or `tools/install_foundation.py`, with the same explicit adapter/capability selection and target-owned conflict handling.

## Artifact contract

`tools/package_foundation.py build` creates a reproducible ZIP from a clean exact Git commit. The commit timestamp supplies every ZIP timestamp, paths are sorted, file modes are normalized, and the command emits a separate SHA-256 sidecar.

The archive contains exactly:

- `foundation/manifest.json`;
- every unique source referenced by manifest core, adapter, and capability rows;
- the minimum deterministic installer runtime, `tools/install_foundation.py` and `tools/content_equivalence.py`; and
- generated `foundation/release-package.json` metadata using `foundation-release-package/v1`.

It deliberately excludes the Foundation project's README, root license, changelog, registry, backlog, status, handover, decisions, quality records, tests, Git metadata, local runtime state, credentials, models, and generated package files. The transferable MIT notice remains included because the transfer manifest explicitly lists it.

The embedded index binds the ruleset version, exact source commit, commit epoch, allowed paths, exact and portable hashes, byte sizes, and package identifier. The installer accepts the embedded source commit for installed provenance only when the complete extracted index and every indexed file are self-consistent. Otherwise it records no package-derived commit.

`verify` rejects unsafe or duplicate paths, non-regular entries, missing or extra files, index changes, payload changes, transfer-manifest mismatches, and an optional sidecar mismatch before extraction.

## Usage

From a clean exact Foundation checkout:

```text
python tools/package_foundation.py build --output OUTSIDE_REPOSITORY/ai-repository-foundation-1.17.0.zip
python tools/package_foundation.py verify --archive OUTSIDE_REPOSITORY/ai-repository-foundation-1.17.0.zip --sha256-file OUTSIDE_REPOSITORY/ai-repository-foundation-1.17.0.zip.sha256
```

After authorized transfer, verify first, extract into an empty staging directory, inspect the plan, and then use the bundled installer:

```text
python STAGING/tools/install_foundation.py TARGET --adapters default --capabilities none
python STAGING/tools/install_foundation.py TARGET --adapters default --capabilities none --apply
```

Optional capabilities remain opt-in even though the universal distribution carries all selectable payload sources. Carrying all sources avoids creating ambiguous partial manifests; selection occurs at installation time exactly as it does from a Git checkout.

## Acceptance evidence

Deterministic tests build the archive twice, compare exact bytes, verify the sidecar and embedded index, assert the exact allowlist, reject extra and modified content, install from an extracted no-Git package, preserve its validated source commit in installation provenance, and reject overwrite or checksum ambiguity. Cross-platform CI remains the completion authority for the pull request.
