# AI Repository Foundation

`AI_Repository_Foundation` provides a vendor-neutral foundation for software projects developed with AI assistance or primarily by AI agents.

The goal is to make a repository sufficiently self-describing and self-governing that development can continue safely and consistently with different AI systems, tools, models, or human contributors without depending on previous chat history or proprietary project prompts.

## Goals

The foundation provides reusable rules and structures for:

- vendor-neutral AI agent instructions;
- repository and project context;
- cost- and resource-aware model selection;
- local-first development and testing;
- context-efficient AI usage;
- documentation governance;
- security and privacy;
- secrets and sensitive-data handling;
- dependency and third-party governance;
- licensing and attribution;
- Git, branch, commit, pull-request and merge workflows;
- architecture decisions;
- backlog, roadmap and handover;
- reproducible validation and test evidence;
- tool-specific AI adapters without duplicating project rules.

## Core principle

The repository is the source of truth.

A project using this foundation should remain understandable and safely maintainable without requiring access to:

- previous AI conversations;
- chat history;
- AI memory;
- user-specific project instructions;
- proprietary agent scratchpads;
- undocumented decisions from previous development sessions.

User and project prompts may provide convenience or personal preferences, but information required for correct project continuation should be stored in the repository.

## Vendor neutrality

The foundation does not depend on a specific AI vendor, model or agent framework.

The canonical repository rules are separated from tool-specific discovery adapters.

Where supported, AI systems should use the root `AGENTS.md` as the primary repository entry point.

Tool-specific files such as:

- `.github/copilot-instructions.md`
- `CLAUDE.md`
- `GEMINI.md`
- Cursor rules
- Amazon Q rules
- Continue rules
- other future adapters

should remain thin adapters that reference the canonical repository rules rather than duplicating them.

## Cost- and resource-aware development

AI processing should use the least expensive and least resource-intensive method that can reliably satisfy the required quality, safety and validation level.

The foundation distinguishes vendor-neutral processing tiers such as:

- `LOCAL`
- `ECONOMICAL`
- `BALANCED`
- `FRONTIER`

Deterministic local tools should be preferred whenever they can perform or verify a task without requiring a generative model.

Examples include:

- builds;
- tests;
- linters;
- formatters;
- static analysis;
- repository searches;
- diff analysis;
- log aggregation;
- schema validation;
- link checks;
- hashing and integrity checks.

Model names, pricing, quotas and vendor-specific reasoning settings are runtime concerns and should not become permanent repository contracts.

## Local-first validation

Validation should normally proceed from the smallest useful check to broader verification:

1. reproduction or characterization;
2. focused tests;
3. affected regression tests;
4. relevant static checks;
5. complete project or CI gate when required.

Successful tests should not be repeated without a concrete reason.

Tests may only be reported as successful when they were actually executed.

## Security and privacy

Projects based on this foundation should define explicit rules for:

- personal and confidential information;
- proprietary data;
- credentials and secrets;
- local environment information;
- logs and diagnostic output;
- external APIs and services;
- irreversible or destructive operations;
- generated artifacts and repository contents.

Synthetic or explicitly redistributable data should be preferred for tests and examples.

## Documentation and decisions

Persistent project knowledge belongs in version-controlled repository documents.

Architecture and other durable decisions should be documented so that later contributors can understand:

- what was decided;
- why it was decided;
- which alternatives were considered;
- which constraints apply;
- when a decision has been superseded.

Documentation should describe the actual project state and must not claim implementation or validation that has not occurred.

## Project-specific rules

This repository provides a foundation, not a complete project specification.

Individual projects are expected to define their own:

- purpose and scope;
- architecture;
- programming languages and frameworks;
- domain rules;
- supported platforms;
- concrete test commands;
- release process;
- project-specific safety constraints;
- project-specific licensing decisions where different from the foundation;
- backlog and roadmap.

Project-specific rules may extend the foundation but should not silently contradict its canonical governance rules.

## Intended workflow

A typical new project can be initialized as follows:

1. create a new repository;
2. add basic project information to `README.md`;
3. clone the repository;
4. apply the AI Repository Foundation;
5. initialize the project-specific context and rules;
6. validate the resulting repository structure;
7. commit and push the initial state;
8. continue development with any supported AI system or human contributor.

After initialization, a new AI session should ideally require only the concrete work request rather than repeated project-wide instructions.

## Status

This project is intended to evolve as AI development tools, repository instruction standards and agent capabilities change.

Vendor-specific discovery behavior should therefore be treated as adapter-level information and periodically verified against current vendor documentation.

The vendor-neutral project contracts should remain stable wherever possible.

## License

This project is licensed under the MIT License.

See [`LICENSE`](LICENSE) for the complete license text.
