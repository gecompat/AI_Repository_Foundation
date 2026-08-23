# Architecture Overview

The Foundation separates three concerns:

1. **Foundation project** — its own README, license, development governance, backlog, status, decisions, tests, and tools.
2. **Transferable rule set** — an explicit whitelist in `foundation/manifest.json` containing only reusable governance rules and selected discovery adapters.
3. **Transfer mechanisms** — a deterministic installer and an AI transfer protocol that consume the same manifest.

A target repository never receives Foundation-project README, LICENSE, changelog, project context, status, handover, backlog, roadmap, internal decisions, tests, or installer source merely because they exist in this repository.

Generic reusable policies remain canonical in their Foundation source locations and are mapped by the manifest into the namespaced target path `.ai/foundation/`. This avoids copying the Foundation project's own state while avoiding duplicate source-of-truth rule text inside this repository.

The target root `AGENTS.md` is an entry bridge. If absent, it can be created from the transfer template. If already present, deterministic installation reports `MERGE_REQUIRED`; an AI may merge only the marked Foundation bridge while preserving target-project instructions.

Tool adapters are discovery only. No vendor capability—subagents, web, shell, Git writes, memory, or model switching—is assumed.
