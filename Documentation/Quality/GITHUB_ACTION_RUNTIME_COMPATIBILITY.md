# GitHub Action runtime compatibility

Status: CANDIDATE

Work item: `WI-0032`

## Triggering evidence

The exact post-merge Foundation CI run for PR #31 (`34288039078`) succeeded but emitted runner annotations for both operating-system jobs: `actions/checkout@v4` and `actions/setup-python@v5` target deprecated Node 20 and were being forced to Node 24. The warning creates foreseeable CI-availability debt even though the run remained green.

Current official upstream documentation was checked on 2026-09-09:

- `actions/checkout` documents v7 as the current use form: https://github.com/actions/checkout/blob/main/README.md
- `actions/setup-python` publishes v7 as its current immutable major release and requires runner v2.327.1 or later: https://github.com/actions/setup-python/releases
- current `setup-python` examples pair `actions/checkout@v7` with `actions/setup-python@v7`: https://github.com/actions/setup-python/blob/main/docs/advanced-usage.md

GitHub-hosted `ubuntu-latest`, `windows-latest`, and `macos-latest` already executed Node 24 while reporting the warning, so the documented minimum runner is not a new dependency for the Foundation's hosted jobs. A target selecting the optional workflow on a self-hosted runner must still verify its runner version; Foundation installation does not upgrade runners or enable workflows.

## Change boundary

The source workflows and optional transferable artifact-registry workflow change only these action major versions:

- `actions/checkout@v4` to `actions/checkout@v7`;
- `actions/setup-python@v5` to `actions/setup-python@v7`.

Python remains 3.12. Workflow permissions, events, environment variables, required check names, registry commands, semantic merge procedure, and Foundation rules remain unchanged. The transferable workflow change is recorded as a material compatibility update to `central-artifact-registry` in Foundation 1.17.1 so an upgrade assessment from 1.17.0 cannot silently omit it.

## Acceptance

Static regressions require the Node-24 action generations in all three workflow sources and reject the deprecated pair. Transfer hashes, semantic feature delta, package allowlisting, installation, registry, and complete Foundation validation must remain green. Pull-request and exact post-merge runs must execute successfully on GitHub-hosted macOS, Windows, and Linux without the prior Node-20 annotations before `WI-0032` is complete.
