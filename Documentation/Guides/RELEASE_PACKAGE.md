# Download, verify and use a Foundation release

Status: INFORMATIVE

Use this guide to obtain a fixed Foundation version without cloning the repository. The reference installer needs Python 3.12 or newer and uses only its standard library. Git and an AI account are not needed for installation from the ZIP. The rules can also be integrated through the [direct transfer protocol](../../foundation/AI_TRANSFER.md).

## Choose and verify the download

Open [release v1.25.0](https://github.com/gecompat/AI_Repository_Foundation/releases/tag/v1.25.0) and download both assets into the same directory:

- `ai-repository-foundation-1.25.0.zip`: the installable Foundation distribution;
- `ai-repository-foundation-1.25.0.zip.sha256`: its SHA-256 checksum.

GitHub's automatic **Source code** archives are full repository snapshots. The separately attached Foundation ZIP contains the manifest-selected material and minimal installer, excluding Foundation project state and history. Optional capability sources are included, but installation still leaves them off unless selected.

Check the checksum before extraction. In PowerShell, from the download directory:

```powershell
$archive = 'ai-repository-foundation-1.25.0.zip'
$expected = ((Get-Content -LiteralPath "$archive.sha256" -Raw).Trim() -split '\s+')[0]
$actual = (Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash
if ($actual -ine $expected) { throw 'SHA-256 mismatch: do not extract or install this archive.' }
```

On systems with `sha256sum`, use `sha256sum -c ai-repository-foundation-1.25.0.zip.sha256` and require an `OK` result. A matching digest detects changed bytes; it is not a publisher signature. When authenticity matters, obtain the expected digest through an independently trusted channel. See [known limitations](../Quality/KNOWN_LIMITATIONS.md).

## Extract into staging and preview installation

Create an empty staging directory beside the download, then extract there:

```text
mkdir foundation-v1.25.0
python -m zipfile -e ai-repository-foundation-1.25.0.zip foundation-v1.25.0
```

Never extract over the target project. Replace `../my-project` below with the intended project path. Start with a provider-neutral core preview:

```text
python foundation-v1.25.0/tools/install_foundation.py ../my-project --adapters none --capabilities none
```

Review the file list and classifications. If the selected files are `CREATE` or `UNCHANGED`, apply that same selection:

```text
python foundation-v1.25.0/tools/install_foundation.py ../my-project --adapters none --capabilities none --apply
```

The result includes `AGENTS.md`, `.ai/foundation/FOUNDATION_RULESET.md`, the selected rules/schemas/helpers, the namespaced MIT notice, and `.ai/foundation/installation-provenance.json`. The receipt should identify ruleset `1.25.0` and the release's exact source commit. Repeating the preview should classify the selected files as `UNCHANGED`. The installer checks the extracted package index when establishing package-derived source provenance.

Existing project README, license, planning, identifiers and domain rules remain project-owned. For discovery-adapter or capability choices, follow the [user guide](USER_GUIDE.md#choose-only-the-capabilities-you-need); no optional code is activated merely because it is carried in the ZIP.

## Existing projects, upgrades and problems

If the preview reports `MERGE_REQUIRED`, preserve the differing files and follow the [existing-repository integration path](USER_GUIDE.md#integrating-an-existing-repository). The installer does not resolve semantic conflicts. Assess the complete applicable feature delta and retain explicit legacy-documentation gaps with scope, owner/role and trigger. Installing v1.25.0 does not certify all existing documentation or automatically upgrade a project.

For a checksum mismatch, stop and check the selected version, download and independently expected digest. For package-index/provenance problems, extract a verified download into a fresh empty staging directory; do not manufacture a receipt. For other errors and full source-checkout integrity checks, use [installation diagnosis](USER_GUIDE.md#check-an-installation-or-investigate-a-problem). The minimal ZIP does not carry the source project's complete validation toolchain. Target semantic and runtime validation remain separate obligations.

To inspect machine information, start with the target's `AGENTS.md` and short ruleset. The extracted `foundation/manifest.json` selects transferable sources; `foundation/release-package.json` is the generated index binding version, source commit and file hashes. The installed provenance receipt records the selected result. [Package design and verification](../Quality/PACKAGED_RELEASE_ARTIFACT_EVALUATION.md) explains those relationships and the boundaries of that evidence.

## Build a distribution from a source checkout

Maintainers can reproduce a distribution from a clean checkout at the intended immutable release commit. Read its manifest version first and use a new output directory outside the checkout:

```text
mkdir ../release-artifacts
python tools/package_foundation.py build --output ../release-artifacts/ai-repository-foundation-1.25.0.zip
python tools/package_foundation.py verify --archive ../release-artifacts/ai-repository-foundation-1.25.0.zip --sha256-file ../release-artifacts/ai-repository-foundation-1.25.0.zip.sha256
```

The builder refuses dirty source or an existing output file. Require `VERIFIED`, the expected ruleset/source commit, and a verified checksum. Archive and index verification establishes package integrity; it does not replace the project's release qualification. [Contributing](../../CONTRIBUTING.md#source-completion-checks) lists source gates.
