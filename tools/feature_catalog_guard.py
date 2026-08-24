#!/usr/bin/env python3
"""Fail closed when semantic upgrade feature coverage or review metadata is incomplete."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "foundation" / "manifest.json"
CATALOG_PATH = ROOT / "foundation" / "feature_catalog.json"
CLASSIFICATIONS = [
    "NOT_APPLICABLE",
    "ALREADY_EQUIVALENT",
    "PROJECT_STRONGER",
    "APPLY_DEFAULT",
    "RECOMMENDED",
    "DECISION_REQUIRED",
    "CONFLICT",
]


def problem(code: str, path: str, message: str) -> dict[str, str]:
    return {"severity": "BLOCKING", "code": code, "path": path, "message": message}


def semver(value: str) -> tuple[int, int, int]:
    parts = value.split(".")
    if len(parts) != 3 or any(not part.isdigit() for part in parts):
        raise ValueError(f"invalid SemVer: {value}")
    return tuple(int(part) for part in parts)  # type: ignore[return-value]


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def manifest_sources(manifest: dict[str, Any]) -> tuple[set[str], set[str]]:
    core = {row["source"] for row in manifest.get("core", []) if isinstance(row, dict) and isinstance(row.get("source"), str)}
    capabilities: set[str] = set()
    for rows in manifest.get("capabilities", {}).values():
        if isinstance(rows, list):
            capabilities.update(row["source"] for row in rows if isinstance(row, dict) and isinstance(row.get("source"), str))
    return core, capabilities


def feature_review_versions(feature: dict[str, Any]) -> set[str]:
    versions = {feature.get("introduced_in")}
    for change in feature.get("change_history", []):
        if isinstance(change, dict):
            versions.add(change.get("version"))
    return {value for value in versions if isinstance(value, str)}


def validate_catalog(manifest: dict[str, Any], catalog: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    current_version = manifest.get("ruleset_version")
    try:
        current_semver = semver(str(current_version))
    except ValueError as exc:
        return [problem("FEATURE_VERSION_INVALID", "foundation/manifest.json", str(exc))]

    if catalog.get("schema_version") != 1:
        issues.append(problem("FEATURE_CATALOG_SCHEMA", "foundation/feature_catalog.json", "schema_version must be 1"))
    if catalog.get("ruleset_version") != current_version:
        issues.append(problem("FEATURE_CATALOG_VERSION", "foundation/feature_catalog.json", f"catalog declares {catalog.get('ruleset_version')} but manifest declares {current_version}"))
    if catalog.get("assessment_classifications") != CLASSIFICATIONS:
        issues.append(problem("FEATURE_CLASSIFICATIONS", "foundation/feature_catalog.json", "assessment_classifications must match the canonical ordered set"))

    features = catalog.get("features")
    if not isinstance(features, dict) or not features:
        return issues + [problem("FEATURE_CATALOG_EMPTY", "foundation/feature_catalog.json", "features must be a non-empty object")]

    core_sources, capability_sources = manifest_sources(manifest)
    transferable = core_sources | capability_sources
    coverage: dict[str, list[str]] = {source: [] for source in transferable}

    for feature_id, feature in features.items():
        if not isinstance(feature_id, str) or not feature_id or not isinstance(feature, dict):
            issues.append(problem("FEATURE_SCHEMA", "foundation/feature_catalog.json", "each feature requires a non-empty ID and object value"))
            continue
        try:
            introduced = semver(str(feature.get("introduced_in")))
            if introduced > current_semver:
                issues.append(problem("FEATURE_FUTURE_VERSION", f"feature:{feature_id}", "introduced_in cannot be newer than the current ruleset"))
        except ValueError as exc:
            issues.append(problem("FEATURE_VERSION_INVALID", f"feature:{feature_id}", str(exc)))

        seen_change_versions: set[str] = set()
        for change in feature.get("change_history", []):
            if not isinstance(change, dict) or change.get("impact") not in {"MATERIAL", "NON_MATERIAL"} or not isinstance(change.get("summary"), str) or not change.get("summary"):
                issues.append(problem("FEATURE_CHANGE_SCHEMA", f"feature:{feature_id}", "change_history entries require version, MATERIAL/NON_MATERIAL impact, and summary"))
                continue
            version = str(change.get("version"))
            if version in seen_change_versions:
                issues.append(problem("FEATURE_CHANGE_DUPLICATE", f"feature:{feature_id}", f"duplicate change_history version {version}"))
            seen_change_versions.add(version)
            try:
                if semver(version) > current_semver:
                    issues.append(problem("FEATURE_FUTURE_VERSION", f"feature:{feature_id}", f"change version {version} is newer than current ruleset"))
            except ValueError as exc:
                issues.append(problem("FEATURE_VERSION_INVALID", f"feature:{feature_id}", str(exc)))

        sources = feature.get("transfer_sources")
        if not isinstance(sources, list) or not sources:
            issues.append(problem("FEATURE_SOURCES", f"feature:{feature_id}", "transfer_sources must be non-empty"))
            continue
        for source in sources:
            if source not in transferable:
                issues.append(problem("FEATURE_SOURCE_NOT_TRANSFERRED", str(source), f"feature {feature_id} references a source not classified by manifest core/capabilities"))
            else:
                coverage[source].append(feature_id)

        dependencies = feature.get("dependencies", [])
        if not isinstance(dependencies, list):
            issues.append(problem("FEATURE_DEPENDENCIES", f"feature:{feature_id}", "dependencies must be an array"))
        else:
            for dependency in dependencies:
                if dependency not in features:
                    issues.append(problem("FEATURE_DEPENDENCY_UNKNOWN", f"feature:{feature_id}", f"unknown dependency {dependency}"))

        applicability = feature.get("applicability")
        if not isinstance(applicability, dict) or applicability.get("mode") not in {"ALWAYS", "REPOSITORY_EVIDENCE"}:
            issues.append(problem("FEATURE_APPLICABILITY", f"feature:{feature_id}", "applicability.mode must be ALWAYS or REPOSITORY_EVIDENCE"))
        recommendation = feature.get("recommendation")
        if not isinstance(recommendation, dict) or recommendation.get("when_applicable") not in {"APPLY_DEFAULT", "RECOMMENDED", "DECISION_REQUIRED"}:
            issues.append(problem("FEATURE_RECOMMENDATION", f"feature:{feature_id}", "recommendation.when_applicable is invalid"))

    for source, feature_ids in sorted(coverage.items()):
        if not feature_ids:
            issues.append(problem("FEATURE_SOURCE_UNCOVERED", source, "transferable source is not covered by any semantic feature"))

    return issues


def git_text(base: str, path: str) -> str:
    completed = subprocess.run(["git", "show", f"{base}:{path}"], cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise ValueError(f"cannot read {path} at base {base}: {completed.stderr.strip()}")
    return completed.stdout


def changed_paths(base: str) -> set[str]:
    completed = subprocess.run(["git", "diff", "--name-only", base, "HEAD"], cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise ValueError(f"cannot diff base {base}: {completed.stderr.strip()}")
    return {line.strip() for line in completed.stdout.splitlines() if line.strip()}


def validate_change_review(manifest: dict[str, Any], catalog: dict[str, Any], base: str) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    base_manifest = json.loads(git_text(base, "foundation/manifest.json"))
    base_version = str(base_manifest.get("ruleset_version"))
    current_version = str(manifest.get("ruleset_version"))
    core_sources, capability_sources = manifest_sources(manifest)
    base_core, base_capabilities = manifest_sources(base_manifest)
    transferable = core_sources | capability_sources | base_core | base_capabilities
    changed = changed_paths(base) & transferable
    if not changed:
        return issues
    if base_version == current_version:
        issues.append(problem("FEATURE_CHANGE_WITHOUT_VERSION_BUMP", "foundation/manifest.json", f"transferable sources changed but ruleset_version remains {current_version}"))

    features = catalog.get("features", {})
    for source in sorted(changed):
        covering = [feature for feature in features.values() if isinstance(feature, dict) and source in feature.get("transfer_sources", [])]
        if not covering:
            issues.append(problem("FEATURE_CHANGED_SOURCE_UNCOVERED", source, "changed transferable source has no feature-catalog coverage"))
            continue
        if not any(current_version in feature_review_versions(feature) for feature in covering):
            issues.append(problem("FEATURE_CATALOG_REVIEW_MISSING", source, f"changed transferable source is not reviewed by any covering feature in ruleset {current_version}"))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="optional Git base ref/sha for changed-source review")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args(argv)

    try:
        manifest = load_json(MANIFEST_PATH)
        catalog = load_json(CATALOG_PATH)
        issues = validate_catalog(manifest, catalog)
        if args.base:
            issues.extend(validate_change_review(manifest, catalog, args.base))
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        issues = [problem("FEATURE_GUARD_READ", "foundation/feature_catalog.json", str(exc))]

    payload = {"schema_version": 1, "validation_scope": "FOUNDATION_SEMANTIC_FEATURE_COVERAGE", "blocking": len(issues), "results": issues}
    if args.json_output:
        print(json.dumps(payload, indent=2))
    else:
        for item in issues:
            print(f"[{item['severity']}] {item['code']} {item['path']}: {item['message']}")
        print("[SCOPE] FOUNDATION_SEMANTIC_FEATURE_COVERAGE")
        print(f"[SUMMARY] blocking={len(issues)}")
    return 2 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
