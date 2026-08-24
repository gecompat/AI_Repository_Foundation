#!/usr/bin/env python3
"""Compute the complete semantic Foundation feature delta for an upgrade."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "foundation" / "feature_catalog.json"
MANIFEST_PATH = ROOT / "foundation" / "manifest.json"


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


def candidate_features(catalog: dict[str, Any], installed_version: str, source_version: str) -> list[dict[str, Any]]:
    installed = semver(installed_version)
    source = semver(source_version)
    if installed > source:
        raise ValueError(f"installed version {installed_version} is newer than source {source_version}")

    candidates: list[dict[str, Any]] = []
    for feature_id, feature in catalog.get("features", {}).items():
        reasons: list[str] = []
        introduced = semver(feature["introduced_in"])
        if installed < introduced <= source:
            reasons.append(f"introduced_in:{feature['introduced_in']}")
        for change in feature.get("change_history", []):
            if change.get("impact") != "MATERIAL":
                continue
            version = semver(change["version"])
            if installed < version <= source:
                reasons.append(f"material_change:{change['version']}")
        if reasons:
            candidates.append({
                "feature_id": feature_id,
                "title": feature["title"],
                "candidate_reasons": reasons,
                "applicability": feature["applicability"],
                "recommendation": feature["recommendation"],
                "dependencies": feature.get("dependencies", []),
            })
    return sorted(candidates, key=lambda item: item["feature_id"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--installed", required=True, help="installed target Foundation version")
    parser.add_argument("--source-ref", default="current", help="source ref label for reporting")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args(argv)

    try:
        manifest = load_json(MANIFEST_PATH)
        catalog = load_json(CATALOG_PATH)
        source_version = str(manifest["ruleset_version"])
        candidates = candidate_features(catalog, args.installed, source_version)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"[BLOCK] {exc}", file=sys.stderr)
        return 2

    payload = {
        "schema_version": 1,
        "installed_version": args.installed,
        "source_version": source_version,
        "source_ref": args.source_ref,
        "candidate_count": len(candidates),
        "candidates": candidates,
    }
    if args.json_output:
        print(json.dumps(payload, indent=2))
    else:
        print(f"Foundation upgrade {args.installed} -> {source_version}: {len(candidates)} semantic candidate(s)")
        for item in candidates:
            print(f"- {item['feature_id']}: {', '.join(item['candidate_reasons'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
