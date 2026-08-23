#!/usr/bin/env python3
"""Dependency-free deterministic Foundation validator."""

from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "AGENTS.md", ".gitignore", "CONTRIBUTING.md", "SECURITY.md",
    ".ai/README.md", ".ai/PROJECT_CONTEXT.md", ".ai/PROJECT_RULES.md",
    ".ai/WORKING_RULES.md", ".ai/MODEL_ROUTING_POLICY.md",
    ".ai/VALIDATION_POLICY.md", ".ai/PROJECT_STATUS.md", ".ai/HANDOVER.md",
    ".ai/ROADMAP.md", ".ai/BACKLOG.md", ".ai/FOUNDATION.md",
    ".ai/TOOL_ADAPTERS.yaml", ".ai/repo_map.yaml",
    "Documentation/Architecture/OVERVIEW.md",
    "Documentation/Architecture/DECISIONS.md",
    "Documentation/Standards/DATA_PRIVACY_AND_CONFIDENTIALITY.md",
    "Documentation/Standards/SECURITY_AND_SAFE_OPERATIONS.md",
    "Documentation/Standards/DOCUMENTATION_POLICY.md",
    "Documentation/Standards/THIRD_PARTY_AND_LICENSING.md",
    "Documentation/Standards/SOURCE_AND_EVIDENCE_POLICY.md",
    "Documentation/Quality/KNOWN_LIMITATIONS.md",
    ".github/copilot-instructions.md", "CLAUDE.md", "GEMINI.md",
]
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(?:api[_-]?key|token|password)\s*[:=]\s*['\"][^'\"]{8,}"),
]
ABSOLUTE_PATHS = [re.compile(r"[A-Za-z]:\\Users\\"), re.compile(r"/home/[^/\s]+/")]
PLACEHOLDER = re.compile(r"(?:TODO|TBD|CHANGEME|<[^>]+>)")
CONFLICT = re.compile(r"^(?:<<<<<<<|=======|>>>>>>>)", re.MULTILINE)

results = []
def add(severity, code, path, message):
    results.append({"severity": severity, "code": code, "path": path, "message": message})

for rel in REQUIRED:
    path = ROOT / rel
    if not path.is_file():
        add("ERROR", "MISSING_REQUIRED", rel, "required file is missing")
    elif not path.read_text(encoding="utf-8").strip():
        add("ERROR", "EMPTY_REQUIRED", rel, "required file is empty")

for path in sorted(ROOT.rglob("*")):
    if not path.is_file() or ".git" in path.parts or ".local" in path.parts:
        continue
    rel = path.relative_to(ROOT).as_posix()
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    if CONFLICT.search(text):
        add("ERROR", "MERGE_CONFLICT", rel, "merge conflict marker found")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            add("ERROR", "POSSIBLE_SECRET", rel, "possible secret pattern found")
    for pattern in ABSOLUTE_PATHS:
        if pattern.search(text):
            add("WARNING", "ABSOLUTE_USER_PATH", rel, "possible local user path found")
    if PLACEHOLDER.search(text) and rel not in {"tools/foundation_validator.py"}:
        add("WARNING", "PLACEHOLDER", rel, "unresolved placeholder-like text found")

for rel in [".github/copilot-instructions.md", "CLAUDE.md", "GEMINI.md"]:
    path = ROOT / rel
    if path.is_file():
        text = path.read_text(encoding="utf-8")
        if len(text) > 1000 or "AGENTS.md" not in text:
            add("WARNING", "ADAPTER_NOT_THIN", rel, "adapter may duplicate governance")

for rel in [".ai/repo_map.yaml", ".ai/TOOL_ADAPTERS.yaml"]:
    path = ROOT / rel
    if path.is_file() and "schema_version: 1" not in path.read_text(encoding="utf-8"):
        add("ERROR", "SCHEMA_VERSION", rel, "schema_version 1 not declared")

errors = sum(r["severity"] == "ERROR" for r in results)
warnings = sum(r["severity"] == "WARNING" for r in results)
for item in results:
    print(f"[{item['severity']}] {item['code']} {item['path']}: {item['message']}")
print(f"[SUMMARY] errors={errors} warnings={warnings}")
print(json.dumps({"schema_version": 1, "errors": errors, "warnings": warnings, "results": results}, indent=2))
sys.exit(1 if errors else 0)
