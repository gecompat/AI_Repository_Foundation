# Architecture Overview

The Foundation separates concerns:

- `AGENTS.md`: small canonical discovery and stop-gate contract;
- `.ai/`: AI/workflow governance, routing, metadata, and current continuation state;
- `Documentation/Standards/`: durable policies applying to humans and AI;
- `Documentation/Architecture/`: durable decisions and structure;
- tool adapter files: discovery only;
- `tools/`: deterministic local bootstrap and validation.

Core is mandatory. Project-type capabilities and additional adapters are optional and should not create empty or irrelevant structure in target repositories. No vendor capability—subagents, web, shell, Git writes, memory, or model switching—is assumed.