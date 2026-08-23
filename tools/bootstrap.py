#!/usr/bin/env python3
"""Compatibility wrapper for the manifest-driven Foundation installer."""

from __future__ import annotations

import sys

from install_foundation import main


def compatibility_args(argv: list[str]) -> list[str]:
    """Translate v1.0 bootstrap semantics to the v1.1 installer CLI."""
    args = list(argv)
    if "--dry-run" in args:
        return [arg for arg in args if arg != "--dry-run"]
    if "--apply" not in args:
        args.append("--apply")
    return args


if __name__ == "__main__":
    print("[INFO] bootstrap.py is retained for v1.0 CLI compatibility; prefer install_foundation.py")
    sys.exit(main(compatibility_args(sys.argv[1:])))
