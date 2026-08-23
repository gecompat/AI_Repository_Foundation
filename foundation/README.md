# Transferable rule set

This directory defines how reusable Foundation rules/provenance are installed or semantically integrated into another repository.

- `manifest.json` is the machine- and AI-readable transfer whitelist and integration contract.
- `AI_TRANSFER.md` defines direct transfer/semantic merge by an AI system.
- `AGENTS.template.md`, `FOUNDATION_RULESET.template.md`, and `repo_map.template.yaml` are target bridge/index templates.
- `Documentation/Standards/SEMANTIC_INTEGRATION_POLICY.md` defines compatibility classes, target-governance discovery, stricter-rule compatibility, adapter migration, and existing-policy interoperability.
- Generic policy sources referenced by the manifest remain canonical in the Foundation repository; the installer maps them into target `.ai/foundation/` paths.

The deterministic installer and an AI use the same manifest. The installer handles file-state planning; semantic integration of an existing repository is performed under the AI transfer/integration contract. This directory is never copied wholesale.
