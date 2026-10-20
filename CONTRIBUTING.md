# Contributing

Read `AGENTS.md` before work. Classify relevant data and its intended destination before mutation or transfer; stop only under the conditions in `Documentation/Standards/DATA_PRIVACY_AND_CONFIDENTIALITY.md`. Use a focused branch and pull request by default; keep commits coherent and factual.

For a change:

1. state scope and affected contracts;
2. avoid unrelated cleanup and governance duplication;
3. record material durable decisions;
4. run `python tools/foundation_validator.py`;
5. add targeted validation appropriate to the change;
6. report unexecuted checks truthfully;
7. update status/handover when continuation facts change.

New dependencies, copied third-party material, capabilities, or adapters require the reviews defined under `Documentation/Standards/`. By contributing, you agree that your contribution is provided under this repository's MIT license.

## Documentation and reading paths

Apply the [documentation policy](Documentation/Standards/DOCUMENTATION_POLICY.md) when changing guidance, navigation, or AI discovery. Follow the complete affected task and a relevant inspection/troubleshooting path, including necessary continuation pages. Use existing checks and focused manual link inspection; record the source binding, paths, results, and gaps in the PR or existing validation evidence. Directory changes include their links, generators, and other path consumers. The policy defines gradual adoption and does not require a separate report or additional reviewer for every edit.

## Source completion checks

Run these from this Foundation repository after focused validation; the feature review uses the declared integration base:

```text
python tools/transfer_manifest_guard.py
python tools/refresh_manifest_hashes.py --check
python tools/feature_catalog_guard.py --base origin/main
python foundation/capabilities/artifact-registry-github/registry_semantic.py validate --registry .ai/identity/registry.json
python foundation/capabilities/artifact-registry-github/registry_semantic.py backlog --registry .ai/identity/registry.json --output .ai/BACKLOG.md --check
python tools/foundation_validator.py --profile full
python -m unittest discover -s tests -v
```

The [canonical validation map](.ai/repo_map.yaml) and [validation policy](.ai/VALIDATION_POLICY.md) govern completion, including relevant installation/capability checks and successful exact PR-head CI. CI also runs Windows/macOS contracts and registry semantic integrity. An installed target check establishes `FOUNDATION_INTEGRITY` only; project semantics, human documentation acceptance, and runtime evidence retain their own checks.

Project maintenance starts with [decisions](Documentation/Architecture/DECISIONS.md), the [canonical registry](.ai/identity/registry.json), its [generated backlog](.ai/BACKLOG.md), and current [status](.ai/PROJECT_STATUS.md)/[handover](.ai/HANDOVER.md). The registry is authoritative for planning; regenerate the backlog with the command above instead of editing it independently. Preserve historical records and distinguish their evidence scope from current delivery.
