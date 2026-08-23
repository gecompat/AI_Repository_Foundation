#!/usr/bin/env python3
"""Copy the Foundation core into a target directory without overwriting files."""

from __future__ import annotations
import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_TOP = {".git", ".local", "tools"}
EXCLUDE_FILES = {"LICENSE", "CHANGELOG.md"}

def source_files():
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if rel.parts[0] in EXCLUDE_TOP or rel.as_posix() in EXCLUDE_FILES:
            continue
        if any(part == "__pycache__" for part in rel.parts):
            continue
        yield path, rel

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    target = args.target.resolve()
    if target == ROOT or ROOT in target.parents:
        print("[BLOCK] target must be outside the Foundation repository")
        return 2
    conflicts, planned = [], []
    for source, rel in source_files():
        destination = target / rel
        (conflicts if destination.exists() else planned).append((source, destination, rel))
    for _, _, rel in planned:
        print(f"[CREATE] {rel}")
    for _, _, rel in conflicts:
        print(f"[CONFLICT] {rel} already exists; no overwrite")
    if conflicts:
        print("[BLOCK] review conflicts; nothing written")
        return 2
    if args.dry_run:
        print(f"[DRY-RUN] {len(planned)} files would be created")
        return 0
    target.mkdir(parents=True, exist_ok=True)
    for source, destination, _ in planned:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    print(f"[OK] created {len(planned)} files")
    return 0

if __name__ == "__main__":
    sys.exit(main())
