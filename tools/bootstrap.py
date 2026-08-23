#!/usr/bin/env python3
"""Compatibility wrapper for the manifest-driven Foundation installer."""

from __future__ import annotations

import sys

from install_foundation import main

if __name__ == "__main__":
    print("[INFO] bootstrap.py is retained for compatibility; use install_foundation.py")
    sys.exit(main())
