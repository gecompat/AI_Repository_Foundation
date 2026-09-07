#!/usr/bin/env python3
"""Refresh or verify portable SHA-256 values on Foundation manifest transfer rows."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from content_equivalence import portable_file_sha256

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "foundation" / "manifest.json"
ROW_KEYS = {"source", "target", "kind", "merge"}
ROW_PATTERN = re.compile(
    r'\{"source": "(?:[^"\\]|\\.)*", "target": "(?:[^"\\]|\\.)*", '
    r'"kind": "(?:[^"\\]|\\.)*", "merge": "(?:[^"\\]|\\.)*"'
    r'(?:, "source_sha256": "[0-9a-f]*")?\}'
)


def refresh_text(text: str, root: Path) -> tuple[str, list[str]]:
    lines = text.splitlines(keepends=True)
    changed: list[str] = []
    output: list[str] = []
    for line in lines:
        def replace(match: re.Match[str]) -> str:
            row = json.loads(match.group(0))
            if not isinstance(row, dict) or not ROW_KEYS.issubset(row) or set(row) - (ROW_KEYS | {"source_sha256"}):
                return match.group(0)
            source = root / row["source"]
            if not source.is_file():
                raise ValueError(f"manifest source missing: {row['source']}")
            expected = portable_file_sha256(source)
            if row.get("source_sha256") != expected:
                changed.append(row["source"])
            row["source_sha256"] = expected
            return json.dumps(row, ensure_ascii=False, separators=(", ", ": "))

        output.append(ROW_PATTERN.sub(replace, line))
    return "".join(output), changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report stale or missing hashes without writing")
    args = parser.parse_args(argv)
    try:
        original = MANIFEST_PATH.read_text(encoding="utf-8")
        refreshed, changed = refresh_text(original, ROOT)
    except (OSError, ValueError) as exc:
        print(f"[BLOCK] {exc}")
        return 2
    if args.check:
        for source in changed:
            print(f"[STALE] {source}")
        print(f"[SUMMARY] stale={len(changed)}")
        return 2 if changed else 0
    if refreshed != original:
        MANIFEST_PATH.write_text(refreshed, encoding="utf-8", newline="\n")
    print(f"[OK] refreshed={len(changed)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
