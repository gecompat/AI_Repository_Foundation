#!/usr/bin/env python3
"""Dependency-free validator for the Foundation project or an installed target ruleset."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "foundation" / "manifest.json"

PROJECT_REQUIRED = [
    "README.md", "AGENTS.md", "LICENSE", ".gitignore", "CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md",
    ".ai/PROJECT_CONTEXT.md", ".ai/PROJECT_RULES.md", ".ai/WORKING_RULES.md",
    ".ai/MODEL_ROUTING_POLICY.md", ".ai/VALIDATION_POLICY.md", ".ai/FOUNDATION.md",
    ".ai/PROJECT_STATUS.md", ".ai/HANDOVER.md", ".ai/ROADMAP.md", ".ai/BACKLOG.md", ".ai/repo_map.yaml",
    "Documentation/Architecture/OVERVIEW.md", "Documentation/Architecture/DECISIONS.md",
    "Documentation/Standards/DATA_PRIVACY_AND_CONFIDENTIALITY.md",
    "Documentation/Standards/SECURITY_AND_SAFE_OPERATIONS.md",
    "Documentation/Standards/DOCUMENTATION_POLICY.md",
    "Documentation/Standards/THIRD_PARTY_AND_LICENSING.md",
    "Documentation/Standards/SOURCE_AND_EVIDENCE_POLICY.md",
    "Documentation/Standards/DEPENDENCY_POLICY.md",
    "Documentation/Quality/KNOWN_LIMITATIONS.md",
    "foundation/manifest.json", "foundation/AI_TRANSFER.md", "foundation/AGENTS.template.md",
    "foundation/FOUNDATION_RULESET.template.md", "foundation/repo_map.template.yaml",
    "foundation/AI_REPOSITORY_FOUNDATION_NOTICE.md",
    "tools/install_foundation.py", "tools/foundation_validator.py",
]

FORBIDDEN_TARGETS = {"README.md", "LICENSE", "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md", ".gitignore"}
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(?:api[_-]?key|token|password)\s*[:=]\s*['\"][^'\"]{8,}"),
]
ABSOLUTE_PATHS = [re.compile(r"[A-Za-z]:\\Users\\"), re.compile(r"/home/[^/\s]+/")]
CONFLICT = re.compile(r"^(?:<<<<<<<|=======|>>>>>>>)", re.MULTILINE)
PLACEHOLDER = re.compile(r"\b(?:CHANGEME|TODO_TEMPLATE|TBD_TEMPLATE)\b")

results: list[dict] = []


def add(severity: str, code: str, path: str, message: str) -> None:
    results.append({"severity": severity, "code": code, "path": path, "message": message})


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def selected_rows(manifest: dict, adapter_selection: str) -> list[dict]:
    if adapter_selection == "default":
        names = list(manifest.get("default_adapters", []))
    elif adapter_selection == "none":
        names = []
    else:
        names = [part.strip() for part in adapter_selection.split(",") if part.strip()]
    unknown = sorted(set(names) - set(manifest.get("adapters", {})))
    if unknown:
        raise ValueError(f"unknown adapter(s): {', '.join(unknown)}")
    rows = list(manifest.get("core", []))
    for name in names:
        rows.extend(manifest["adapters"][name])
    return rows


def scan_text(path: Path, display: str) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return
    if CONFLICT.search(text):
        add("ERROR", "MERGE_CONFLICT", display, "merge conflict marker found")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            add("BLOCKING", "POSSIBLE_SECRET", display, "possible secret pattern found")
    for pattern in ABSOLUTE_PATHS:
        if pattern.search(text):
            add("WARNING", "ABSOLUTE_USER_PATH", display, "possible local user path found")
    if PLACEHOLDER.search(text):
        add("WARNING", "PLACEHOLDER", display, "unresolved template placeholder found")


def validate_manifest(manifest: dict) -> None:
    if manifest.get("schema_version") != 1:
        add("ERROR", "MANIFEST_SCHEMA", "foundation/manifest.json", "schema_version must be 1")
    if not manifest.get("ruleset_version"):
        add("ERROR", "MANIFEST_VERSION", "foundation/manifest.json", "ruleset_version is required")

    targets: set[str] = set()
    rows = list(manifest.get("core", []))
    for name, adapter_rows in manifest.get("adapters", {}).items():
        if not isinstance(adapter_rows, list):
            add("ERROR", "ADAPTER_SCHEMA", f"adapter:{name}", "adapter value must be a list")
            continue
        rows.extend(adapter_rows)

    for row in rows:
        source = row.get("source", "")
        target = row.get("target", "")
        if not source or not target:
            add("ERROR", "MANIFEST_ENTRY", "foundation/manifest.json", "source and target are required")
            continue
        if target in targets:
            add("ERROR", "DUPLICATE_TARGET", target, "manifest target occurs more than once")
        targets.add(target)
        if target in FORBIDDEN_TARGETS:
            add("BLOCKING", "PROJECT_ARTIFACT_TARGET", target, "Foundation project artifact must not be transferred")
        if target.startswith("Documentation/Architecture/") or target.startswith("Documentation/Quality/"):
            add("BLOCKING", "PROJECT_STATE_TARGET", target, "Foundation project architecture/quality state must not be transferred")
        source_path = ROOT / source
        if not source_path.is_file():
            add("ERROR", "MISSING_SOURCE", source, "manifest source does not exist")

    for adapter in manifest.get("default_adapters", []):
        if adapter not in manifest.get("adapters", {}):
            add("ERROR", "DEFAULT_ADAPTER", adapter, "default adapter is not defined")

    attribution = manifest.get("attribution")
    if not isinstance(attribution, dict) or not attribution.get("required"):
        add("BLOCKING", "ATTRIBUTION_CONFIG", "foundation/manifest.json", "required attribution configuration is missing")
        return

    attr_source = attribution.get("source")
    attr_target = attribution.get("target")
    matching = [row for row in rows if row.get("kind") == "attribution"]
    if len(matching) != 1:
        add("BLOCKING", "ATTRIBUTION_ENTRY", "foundation/manifest.json", "exactly one attribution transfer entry is required")
        return
    row = matching[0]
    if row.get("source") != attr_source or row.get("target") != attr_target:
        add("BLOCKING", "ATTRIBUTION_MAPPING", "foundation/manifest.json", "attribution metadata and transfer entry do not match")
    if attr_target in FORBIDDEN_TARGETS or attr_target == "LICENSE":
        add("BLOCKING", "ATTRIBUTION_ROOT_LICENSE", str(attr_target), "Foundation attribution must not replace the target root license")

    source_path = ROOT / str(attr_source)
    license_path = ROOT / "LICENSE"
    if source_path.is_file() and license_path.is_file():
        required_notice = license_path.read_text(encoding="utf-8")
        if required_notice not in source_path.read_text(encoding="utf-8"):
            add("BLOCKING", "ATTRIBUTION_SOURCE", str(attr_source), "attribution source does not contain the complete Foundation MIT notice")


def validate_foundation(profile: str) -> None:
    for rel in PROJECT_REQUIRED:
        path = ROOT / rel
        if not path.is_file():
            add("ERROR", "MISSING_REQUIRED", rel, "required Foundation-project file is missing")
        elif not path.read_text(encoding="utf-8").strip():
            add("ERROR", "EMPTY_REQUIRED", rel, "required file is empty")

    try:
        manifest = load_manifest()
    except (OSError, json.JSONDecodeError) as exc:
        add("BLOCKING", "MANIFEST_READ", "foundation/manifest.json", str(exc))
        return
    validate_manifest(manifest)

    repo_map = ROOT / ".ai" / "repo_map.yaml"
    if repo_map.is_file():
        text = repo_map.read_text(encoding="utf-8")
        for rel in [
            "Documentation/Standards/DOCUMENTATION_POLICY.md",
            "Documentation/Standards/SOURCE_AND_EVIDENCE_POLICY.md",
            "Documentation/Standards/DEPENDENCY_POLICY.md",
            "Documentation/Architecture/DECISIONS.md",
        ]:
            if rel not in text:
                add("ERROR", "AUTHORITY_MAP", ".ai/repo_map.yaml", f"authoritative source missing from map: {rel}")

    for rel in [".github/copilot-instructions.md", "CLAUDE.md", "GEMINI.md"]:
        path = ROOT / rel
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            if len(text) > 1000 or "AGENTS.md" not in text:
                add("WARNING", "ADAPTER_NOT_THIN", rel, "adapter may duplicate governance")

    if profile != "quick":
        for path in sorted(ROOT.rglob("*")):
            if not path.is_file() or ".git" in path.parts or ".local" in path.parts or "__pycache__" in path.parts:
                continue
            scan_text(path, path.relative_to(ROOT).as_posix())

    if profile == "release":
        status = ROOT / ".ai" / "PROJECT_STATUS.md"
        if status.is_file() and ("not executed" in status.read_text(encoding="utf-8") or "pending manual validation" in status.read_text(encoding="utf-8")):
            add("ERROR", "PENDING_RELEASE_VALIDATION", ".ai/PROJECT_STATUS.md", "release profile still contains pending validation")


def validate_target(target: Path, adapter_selection: str, profile: str) -> None:
    try:
        manifest = load_manifest()
        rows = selected_rows(manifest, adapter_selection)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        add("BLOCKING", "MANIFEST_READ", "foundation/manifest.json", str(exc))
        return

    selected_paths: list[Path] = []
    required_mit_notice = (ROOT / "LICENSE").read_text(encoding="utf-8")
    for row in rows:
        source = ROOT / row["source"]
        destination = target / row["target"]
        display = row["target"]
        if not destination.is_file():
            add("ERROR", "MISSING_TARGET_RULE", display, "selected Foundation rule/adapter is missing")
            continue
        selected_paths.append(destination)
        text = destination.read_text(encoding="utf-8", errors="replace")
        if display == "AGENTS.md" and "AI_REPOSITORY_FOUNDATION" not in text:
            add("ERROR", "ENTRYPOINT_BRIDGE", display, "Foundation bridge marker is missing")
        if row.get("kind") == "adapter" and "AGENTS.md" not in text:
            add("ERROR", "ADAPTER_DISCOVERY", display, "adapter does not lead to AGENTS.md")
        if row.get("kind") == "attribution" and required_mit_notice not in text:
            add("BLOCKING", "ATTRIBUTION_NOTICE", display, "installed attribution file does not preserve the complete Foundation MIT notice")
        if display.startswith(".ai/foundation/") and source.is_file() and destination.read_bytes() != source.read_bytes():
            add("WARNING", "LOCAL_OVERRIDE_OR_DRIFT", display, "installed Foundation rule/provenance file differs from current source; review intentionally")

    if profile != "quick":
        for path in selected_paths:
            scan_text(path, path.relative_to(target).as_posix())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, help="validate installed rules in another repository")
    parser.add_argument("--adapters", default="default", help="default, none, or comma-separated adapter names")
    parser.add_argument("--profile", choices=["quick", "commit", "full", "release"], default="full")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args(argv)

    results.clear()
    if args.target:
        validate_target(args.target.resolve(), args.adapters, args.profile)
    else:
        validate_foundation(args.profile)

    counts = {severity: sum(item["severity"] == severity for item in results) for severity in ["INFO", "WARNING", "ERROR", "BLOCKING"]}
    payload = {"schema_version": 1, "counts": counts, "results": results}
    if args.json_output:
        print(json.dumps(payload, indent=2))
    else:
        for item in results:
            print(f"[{item['severity']}] {item['code']} {item['path']}: {item['message']}")
        print("[SUMMARY] " + " ".join(f"{key.lower()}={value}" for key, value in counts.items()))

    if counts["BLOCKING"]:
        return 2
    if counts["ERROR"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
