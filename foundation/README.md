# Transferable rule set

This directory defines how reusable Foundation rules/provenance are installed or semantically integrated into another repository.

- `manifest.json` is the machine- and AI-readable transfer whitelist and integration contract.
- `AI_TRANSFER.md` defines direct transfer/semantic merge by an AI system.
- `AGENTS.template.md`, `FOUNDATION_RULESET.template.md`, and `repo_map.template.yaml` are target bridge/index templates.
- `Documentation/Standards/SEMANTIC_INTEGRATION_POLICY.md` defines compatibility classes, target-governance discovery, stricter-rule compatibility, adapter migration, and existing-policy interoperability.
- Generic policy sources referenced by the manifest remain canonical in the Foundation repository; the installer maps them into target `.ai/foundation/` paths.

The deterministic installer and an AI use the same manifest. The installer handles file-state planning; semantic integration of an existing repository is performed under the AI transfer/integration contract. This directory is never copied wholesale.

Foundation 1.13 adds portable runtime-inventory, provision-request, exact-approval, and report schemas. The optional `ai-provisioning` reference implements bounded diagnosis, inventory, planning, approval-bound offline provisioning, verification, and isolated cost-evidence refresh. It is not required for Foundation integrity and grants no download, network, install, credential, spend, or repository authority. Runtime artifacts and evidence stay outside Git; missing Python, runtimes, models, providers, or network yield truthful degradation.
