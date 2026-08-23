# Known Limitations

- The privacy stop-gate requires semantic judgment; deterministic scanning cannot prove absence of confidential content.
- The validator is intentionally dependency-free and checks structure, references, adapter size/content, basic secret/path patterns, conflict markers, placeholders, and status vocabulary. It is not a full YAML parser or dedicated secret scanner.
- Bootstrap refuses overwrites but does not yet merge or classify semantic conflicts automatically.
- Foundation hashes and packaged release artifacts are planned after v1.0 self-test evidence.
- Current vendor adapter discovery behavior must be checked against current primary documentation before adapter changes.
- The v1.0 bootstrap/idempotency/continuation acceptance tests remain unexecuted until recorded in project status.