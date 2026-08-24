#!/usr/bin/env python3
"""Fail closed when Foundation transfer sources/version mirrors drift from manifest.json."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "foundation" / "manifest.json"
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def issue(code: str, path: str, message: str) -> dict[str, str]:
    return {"severity": "BLOCKING", "code": code, "path": path, "message": message}


def load_manifest(root: Path = ROOT) -> dict[str, Any]:
    return json.loads((root / "foundation" / "manifest.json").read_text(encoding="utf-8"))


def rows_by_section(manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    core = list(manifest.get("core", []))
    capabilities = {
        name: list(rows) if isinstance(rows, list) else []
        for name, rows in manifest.get("capabilities", {}).items()
    }
    return core, capabilities


def collect_files(root: Path, rel_root: str, suffixes: list[str], recursive: bool) -> set[str]:
    base = root / rel_root
    if not base.exists():
        return set()
    iterator = base.rglob("*") if recursive else base.glob("*")
    allowed = set(suffixes)
    result: set[str] = set()
    for path in iterator:
        if not path.is_file() or path.name in {".gitkeep", "README.md"}:
            continue
        if allowed and path.suffix not in allowed:
            continue
        result.add(path.relative_to(root).as_posix())
    return result


def matches_prefix(path: str, root: str) -> bool:
    normalized = root.rstrip("/") + "/"
    return path.startswith(normalized)


def validate_version_mirrors(root: Path, manifest: dict[str, Any], contract: dict[str, Any]) -> list[dict[str, str]]:
    problems: list[dict[str, str]] = []
    version = manifest.get("ruleset_version")
    if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
        return [issue("TRANSFER_VERSION_INVALID", "foundation/manifest.json", "ruleset_version must be SemVer MAJOR.MINOR.PATCH")]

    if contract.get("version_authority") != "foundation/manifest.json#ruleset_version":
        problems.append(issue("TRANSFER_VERSION_AUTHORITY", "foundation/manifest.json", "version_authority must point to foundation/manifest.json#ruleset_version"))

    for mirror in contract.get("version_mirrors", []):
        path_value = mirror.get("path")
        pattern_value = mirror.get("pattern")
        if not isinstance(path_value, str) or not isinstance(pattern_value, str):
            problems.append(issue("TRANSFER_VERSION_MIRROR_SCHEMA", "foundation/manifest.json", "every version mirror requires path and pattern"))
            continue
        path = root / path_value
        if not path.is_file():
            problems.append(issue("TRANSFER_VERSION_MIRROR_MISSING", path_value, "declared version mirror file is missing"))
            continue
        match = re.search(pattern_value, path.read_text(encoding="utf-8"), re.MULTILINE)
        if match is None or "version" not in match.groupdict():
            problems.append(issue("TRANSFER_VERSION_MIRROR_UNREADABLE", path_value, "version mirror pattern did not capture a named 'version' group"))
            continue
        if match.group("version") != version:
            problems.append(issue("TRANSFER_VERSION_MISMATCH", path_value, f"declares {match.group('version')} but manifest authority declares {version}"))
    return problems


def validate_transfer_coverage(root: Path = ROOT, manifest: dict[str, Any] | None = None) -> list[dict[str, str]]:
    manifest = copy.deepcopy(manifest if manifest is not None else load_manifest(root))
    contract = manifest.get("transfer_coverage_contract")
    if not isinstance(contract, dict):
        return [issue("TRANSFER_COVERAGE_CONTRACT", "foundation/manifest.json", "transfer_coverage_contract is required")]

    problems = validate_version_mirrors(root, manifest, contract)
    core, capabilities = rows_by_section(manifest)
    core_sources = [row.get("source") for row in core if isinstance(row, dict) and isinstance(row.get("source"), str)]
    core_source_set = set(core_sources)

    duplicates = sorted({source for source in core_sources if core_sources.count(source) > 1})
    for source in duplicates:
        problems.append(issue("TRANSFER_SOURCE_DUPLICATE", str(source), "core source is classified more than once"))

    for source in contract.get("fixed_core_sources", []):
        if source not in core_source_set:
            problems.append(issue("TRANSFER_FIXED_CORE_UNCLASSIFIED", str(source), "required fixed core source is not classified in manifest core"))

    for managed in contract.get("managed_core_roots", []):
        rel_root = managed.get("path")
        suffixes = managed.get("suffixes", [])
        recursive = bool(managed.get("recursive", False))
        if not isinstance(rel_root, str) or not isinstance(suffixes, list):
            problems.append(issue("TRANSFER_MANAGED_ROOT_SCHEMA", "foundation/manifest.json", "managed_core_roots entries require path and suffixes"))
            continue
        actual = collect_files(root, rel_root, [str(value) for value in suffixes], recursive)
        for source in sorted(actual - core_source_set):
            problems.append(issue("TRANSFER_CORE_SOURCE_UNCLASSIFIED", source, "managed reusable core source exists but is absent from manifest core"))
        for source in sorted({value for value in core_source_set if matches_prefix(value, rel_root)} - actual):
            problems.append(issue("TRANSFER_CORE_SOURCE_ORPHANED", source, "manifest core source is under a managed root but is not an allowed file there"))

    legacy_roots = contract.get("legacy_capability_roots", [])
    future_root = contract.get("future_capability_root")
    allowed_capability_roots: list[tuple[str, str | None, list[str], bool]] = []
    for item in legacy_roots:
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            allowed_capability_roots.append((item["path"], item.get("capability"), [str(v) for v in item.get("suffixes", [])], bool(item.get("recursive", True))))
    if isinstance(future_root, str):
        allowed_capability_roots.append((future_root, None, [], True))

    capability_sources: dict[str, set[str]] = {
        name: {row.get("source") for row in rows if isinstance(row, dict) and isinstance(row.get("source"), str)}
        for name, rows in capabilities.items()
    }

    for rel_root, fixed_capability, suffixes, recursive in allowed_capability_roots:
        actual = collect_files(root, rel_root, suffixes, recursive)
        if fixed_capability:
            declared = capability_sources.get(fixed_capability, set())
            for source in sorted(actual - declared):
                problems.append(issue("TRANSFER_CAPABILITY_SOURCE_UNCLASSIFIED", source, f"managed capability source is absent from capability {fixed_capability}"))
            for source in sorted({value for value in declared if matches_prefix(value, rel_root)} - actual):
                problems.append(issue("TRANSFER_CAPABILITY_SOURCE_ORPHANED", source, f"capability {fixed_capability} declares a missing/disallowed source under {rel_root}"))
        else:
            for source in sorted(actual):
                relative = Path(source).relative_to(rel_root)
                if len(relative.parts) < 2:
                    problems.append(issue("TRANSFER_CAPABILITY_LAYOUT", source, "future capability payload must be under foundation/capabilities/<capability>/..."))
                    continue
                capability = relative.parts[0]
                if source not in capability_sources.get(capability, set()):
                    problems.append(issue("TRANSFER_CAPABILITY_SOURCE_UNCLASSIFIED", source, f"future capability payload is not classified in manifest capability {capability}"))

    allowed_prefixes = [root_value.rstrip("/") + "/" for root_value, _, _, _ in allowed_capability_roots]
    for capability, sources in capability_sources.items():
        if not sources:
            problems.append(issue("TRANSFER_CAPABILITY_EMPTY", f"capability:{capability}", "capability must contain at least one source"))
        for source in sorted(sources):
            if not any(source.startswith(prefix) for prefix in allowed_prefixes):
                problems.append(issue("TRANSFER_CAPABILITY_SOURCE_OUTSIDE_MANAGED_ROOT", source, "capability source must live under a registered legacy root or foundation/capabilities/<capability>/"))

    for key, value in manifest.items():
        if not key.endswith("_contract") or not isinstance(value, dict):
            continue
        policy_source = value.get("policy_source")
        if isinstance(policy_source, str) and policy_source not in core_source_set:
            problems.append(issue("TRANSFER_CONTRACT_POLICY_UNCLASSIFIED", policy_source, f"{key}.policy_source is not transferred in manifest core"))
        for schema_target in value.get("schema_targets", []) if isinstance(value.get("schema_targets"), list) else []:
            if sum(1 for row in core if row.get("target") == schema_target) != 1:
                problems.append(issue("TRANSFER_CONTRACT_SCHEMA_UNCLASSIFIED", str(schema_target), f"{key} schema target must be transferred exactly once in core"))

    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args(argv)

    try:
        manifest = load_manifest(ROOT)
        problems = validate_transfer_coverage(ROOT, manifest)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        problems = [issue("TRANSFER_GUARD_READ", "foundation/manifest.json", str(exc))]

    payload = {"schema_version": 1, "validation_scope": "FOUNDATION_TRANSFER_COMPLETENESS", "blocking": len(problems), "results": problems}
    if args.json_output:
        print(json.dumps(payload, indent=2))
    else:
        for problem in problems:
            print(f"[{problem['severity']}] {problem['code']} {problem['path']}: {problem['message']}")
        print("[SCOPE] FOUNDATION_TRANSFER_COMPLETENESS")
        print(f"[SUMMARY] blocking={len(problems)}")
    return 2 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
