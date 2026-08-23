# Transferable rule set

This directory defines how reusable Foundation rules are installed into another repository.

- `manifest.json` is the machine- and AI-readable whitelist.
- `AI_TRANSFER.md` defines direct transfer by an AI system.
- `AGENTS.template.md`, `FOUNDATION_RULESET.template.md`, and `repo_map.template.yaml` are target-specific bridge/index templates.
- Generic policy sources referenced by the manifest remain canonical in the Foundation repository; the installer maps them into target `.ai/foundation/` paths.

The deterministic installer and an AI use the same manifest. This directory is not copied wholesale.
