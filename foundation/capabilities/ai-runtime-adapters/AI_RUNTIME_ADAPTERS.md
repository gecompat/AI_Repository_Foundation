# AI runtime reference adapters

Status: OPTIONAL REFERENCE CAPABILITY

This capability implements `foundation-ai-adapter-jsonl/v1` over newline-delimited stdio. Every request contains only `protocol`, `request_id`, `operation`, and `arguments`; operations are `probe`, `catalog`, `invoke`, `cancel`, and optional `provision`. Results contain control metadata only. Invocation payloads move through explicitly allowlisted files, and generated content is written to an output handle rather than stdout.

`reference_adapters.py` supports three replaceable paths:

- Ollama native HTTP, split into distinct local and cloud-tag provider fragments;
- OpenAI-compatible HTTP for LM Studio, llama.cpp, LocalAI, vLLM, and compatible services;
- configured command/stdio programs using argv arrays, whole-argument substitutions, `shell=False`, and an exact environment-name allowlist.

Each process has bounded timeouts, structured error classes, a circuit breaker, cancel semantics, health TTLs, and content-free responses. HTTP redirects are refused so credentials cannot cross origin. Endpoint trust is explicit: loopback is `UNKNOWN` unless configuration supplies host-boundary evidence; a product name is never boundary evidence. Ollama names ending in a cloud marker always enter a separate `REMOTE` fragment and require explicit remote invocation authority.

Resource-price refresh is independent of model invocation. Cache conforming `foundation-resource-cost-evidence/v1` records outside Git, query a given source at most once per 24 hours (normally less often according to its TTL), and prefer deterministic primary sources or local measurement. AI-assisted source discovery is optional and cannot turn an unverified estimate into routable money evidence.

Configuration is target/runtime data. Store it outside the repository when it contains endpoint, host path, or credential environment details. Credentials are read only from explicitly allowlisted environment names and never emitted; they require HTTPS unless a loopback endpoint has separate explicit host-boundary evidence. `network_authorized`, general and remote data classes, read roots, write roots, remote-model authority, and asserted boundary must all be configured; no default grants them. Command executables use absolute paths and an exact argv/environment. Handle roots restrict what the adapter passes to the child but are not an operating-system sandbox: configure only trusted programs and apply target-owned process isolation when ambient user permissions are too broad.

Run one adapter process:

```text
python .ai/foundation/ai_runtime_adapters/reference_adapters.py ollama --config PATH_OUTSIDE_REPOSITORY
python .ai/foundation/ai_runtime_adapters/reference_adapters.py openai-compatible --config PATH_OUTSIDE_REPOSITORY
python .ai/foundation/ai_runtime_adapters/reference_adapters.py command --config PATH_OUTSIDE_REPOSITORY
```

The protocol and policy are language-neutral. Python is only the optional reference implementation. Catalog entries initially report unknown model quality/context/resources unless a separately governed profile or measured evidence supplies them; discovery alone never creates routable quality evidence.
