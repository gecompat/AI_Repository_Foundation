# .ai

Version-controlled AI/project governance and continuation state. This directory is authoritative where declared by `repo_map.yaml`.

Never place local runtime state, logs, caches, scratch work, credentials, or machine-specific values in `.ai/`. Ordinary disposable work may use the repository's ignored root `.local/` only when its owning contract permits worktree-local state. AI router/adapter/executor/provisioner/orchestrator state explicitly belongs outside every Git worktree at the component's documented operating-system path or external override.
