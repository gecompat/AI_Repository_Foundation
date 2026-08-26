#!/usr/bin/env python3
"""Shared Foundation content-equivalence rules for transfer planning and drift checks."""

from __future__ import annotations

from pathlib import Path


def _normalized_utf8_text(data: bytes) -> bytes | None:
    """Return UTF-8 bytes with CRLF normalized to LF, or None for non-text data.

    Foundation transfer integrity treats Git working-tree CRLF conversion as a
    representation difference, not semantic drift. Lone CR characters remain
    significant so the equivalence rule is intentionally limited to the Git
    LF/CRLF conversion that occurs with core.autocrlf and related settings.
    """
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return None
    if "\x00" in text:
        return None
    return text.replace("\r\n", "\n").encode("utf-8")


def content_equivalent(left: bytes, right: bytes) -> bool:
    """Compare content exactly for binary data and EOL-normalized for UTF-8 text."""
    if left == right:
        return True
    normalized_left = _normalized_utf8_text(left)
    normalized_right = _normalized_utf8_text(right)
    return (
        normalized_left is not None
        and normalized_right is not None
        and normalized_left == normalized_right
    )


def files_equivalent(left: Path, right: Path) -> bool:
    """Compare two files using the Foundation transfer-equivalence contract."""
    return content_equivalent(left.read_bytes(), right.read_bytes())
