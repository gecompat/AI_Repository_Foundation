#!/usr/bin/env python3
"""Build and verify deterministic offline Foundation source distributions."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

from content_equivalence import portable_content_sha256

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_REL = "foundation/manifest.json"
PACKAGE_INDEX_REL = "foundation/release-package.json"
BOOTSTRAP_PATHS = ("tools/content_equivalence.py", "tools/install_foundation.py")
CONTRACT = "foundation-release-package/v1"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
MAX_ARCHIVE_BYTES = 512 * 1024 * 1024
MAX_EXPANDED_BYTES = 1024 * 1024 * 1024
MAX_ENTRY_BYTES = 128 * 1024 * 1024
MAX_ENTRIES = 10_000
MAX_INDEX_BYTES = 8 * 1024 * 1024
MAX_ZIP_EPOCH = 4_354_819_199
INDEX_FIELDS = {
    "schema_version",
    "contract",
    "ruleset_version",
    "source_repository",
    "source_commit",
    "source_epoch",
    "created_at",
    "layout",
    "selection",
    "content_normalization",
    "files",
    "install_command",
    "package_id",
}


class PackageError(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_manifest(root: Path) -> dict[str, Any]:
    path = root / MANIFEST_REL
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PackageError("Foundation manifest is unavailable or invalid") from exc
    if not isinstance(value, dict) or not isinstance(value.get("ruleset_version"), str):
        raise PackageError("Foundation manifest contract is invalid")
    return value


def manifest_rows(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    groups: list[Any] = [manifest.get("core")]
    groups.extend((manifest.get("adapters") or {}).values())
    groups.extend((manifest.get("capabilities") or {}).values())
    rows: list[dict[str, Any]] = []
    for group in groups:
        if not isinstance(group, list):
            raise PackageError("Foundation manifest transfer rows are invalid")
        for row in group:
            if not isinstance(row, dict):
                raise PackageError("Foundation manifest transfer row is invalid")
            source = row.get("source")
            expected = row.get("source_sha256")
            if not isinstance(source, str) or not safe_archive_path(source):
                raise PackageError("Foundation manifest source path is unsafe")
            if not isinstance(expected, str) or not SHA256_RE.fullmatch(expected):
                raise PackageError(f"Foundation manifest source hash is invalid: {source}")
            rows.append(row)
    return rows


def distribution_paths(manifest: dict[str, Any]) -> list[str]:
    paths = {MANIFEST_REL, *BOOTSTRAP_PATHS}
    paths.update(row["source"] for row in manifest_rows(manifest))
    return sorted(paths)


def safe_archive_path(raw: str) -> bool:
    if not raw or "\\" in raw or raw.startswith("/"):
        return False
    path = PurePosixPath(raw)
    return not path.is_absolute() and all(part not in {"", ".", ".."} for part in path.parts)


def source_identity(root: Path) -> tuple[str, int]:
    try:
        status = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=normal"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
        if status.stdout.strip():
            raise PackageError("release packages require a clean Git working tree")
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True
        ).stdout.strip().lower()
        epoch_raw = subprocess.run(
            ["git", "show", "-s", "--format=%ct", "HEAD"], cwd=root, check=True, capture_output=True, text=True
        ).stdout.strip()
    except PackageError:
        raise
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        raise PackageError("release packages require a clean Git checkout with an exact commit") from exc
    if not COMMIT_RE.fullmatch(commit) or not epoch_raw.isdigit():
        raise PackageError("Git source identity is invalid")
    return commit, int(epoch_raw)


def collect_files(root: Path, manifest: dict[str, Any]) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    expected_portable = {row["source"]: row["source_sha256"] for row in manifest_rows(manifest)}
    for relative in distribution_paths(manifest):
        path = root / relative
        try:
            body = path.read_bytes()
        except OSError as exc:
            raise PackageError(f"distribution source is unavailable: {relative}") from exc
        expected = expected_portable.get(relative)
        if expected is not None and portable_content_sha256(body) != expected:
            raise PackageError(f"manifest source hash mismatch: {relative}")
        result[relative] = body
    return result


def package_index(
    manifest: dict[str, Any], files: dict[str, bytes], source_commit: str, source_epoch: int
) -> dict[str, Any]:
    created = datetime.fromtimestamp(source_epoch, tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    entries = [
        {
            "path": path,
            "role": "MANIFEST" if path == MANIFEST_REL else "INSTALLER" if path in BOOTSTRAP_PATHS else "PAYLOAD",
            "sha256": sha256(body),
            "portable_sha256": portable_content_sha256(body),
            "size_bytes": len(body),
        }
        for path, body in sorted(files.items())
    ]
    material = {
        "schema_version": 1,
        "contract": CONTRACT,
        "ruleset_version": manifest["ruleset_version"],
        "source_repository": manifest.get("source_repository"),
        "source_commit": source_commit,
        "source_epoch": source_epoch,
        "created_at": created,
        "layout": "FOUNDATION_SOURCE_DISTRIBUTION",
        "selection": "ALL_MANIFEST_COMPONENTS",
        "content_normalization": "UTF8_CRLF_TO_LF_ELSE_EXACT",
        "files": entries,
        "install_command": "python tools/install_foundation.py TARGET --adapters default --capabilities none --apply",
    }
    return {**material, "package_id": sha256(canonical(material))}


def zip_datetime(epoch: int) -> tuple[int, int, int, int, int, int]:
    value = datetime.fromtimestamp(epoch, tz=timezone.utc)
    if value.year < 1980:
        value = datetime(1980, 1, 1, tzinfo=timezone.utc)
    if value.year > 2107:
        raise PackageError("source commit timestamp is outside the ZIP range")
    return value.year, value.month, value.day, value.hour, value.minute, value.second - value.second % 2


def archive_entry(path: str, body: bytes, epoch: int) -> tuple[zipfile.ZipInfo, bytes]:
    info = zipfile.ZipInfo(path, zip_datetime(epoch))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    info.flag_bits |= 0x800
    return info, body


def build_package(
    root: Path,
    output: Path,
    *,
    source_commit: str,
    source_epoch: int,
) -> dict[str, Any]:
    if output.exists():
        raise PackageError(f"output already exists: {output}")
    if not output.parent.is_dir():
        raise PackageError(f"output directory does not exist: {output.parent}")
    if not COMMIT_RE.fullmatch(source_commit) or source_epoch < 0:
        raise PackageError("source identity is invalid")
    manifest = load_manifest(root)
    files = collect_files(root, manifest)
    index = package_index(manifest, files, source_commit, source_epoch)
    index_body = json.dumps(index, indent=2, sort_keys=False).encode("utf-8") + b"\n"
    archive_files = {**files, PACKAGE_INDEX_REL: index_body}
    try:
        with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for relative, body in sorted(archive_files.items()):
                info, payload = archive_entry(relative, body, source_epoch)
                archive.writestr(info, payload, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    except Exception:
        output.unlink(missing_ok=True)
        raise
    archive_hash = sha256(output.read_bytes())
    checksum_path = output.with_name(output.name + ".sha256")
    if checksum_path.exists():
        output.unlink(missing_ok=True)
        raise PackageError(f"checksum output already exists: {checksum_path}")
    checksum_path.write_text(f"{archive_hash}  {output.name}\n", encoding="ascii", newline="\n")
    return {
        "status": "BUILT",
        "archive": str(output.resolve()),
        "sha256_file": str(checksum_path.resolve()),
        "sha256": archive_hash,
        "package_id": index["package_id"],
        "ruleset_version": index["ruleset_version"],
        "source_commit": source_commit,
        "entry_count": len(archive_files),
    }


def read_checksum(path: Path, archive: Path) -> str:
    try:
        line = path.read_text(encoding="ascii").strip()
    except OSError as exc:
        raise PackageError("checksum file is unavailable") from exc
    parts = line.split()
    if len(parts) != 2 or not SHA256_RE.fullmatch(parts[0]) or parts[1] != archive.name:
        raise PackageError("checksum file contract is invalid")
    return parts[0]


def verify_package(archive_path: Path, checksum_path: Path | None = None) -> dict[str, Any]:
    try:
        if archive_path.stat().st_size > MAX_ARCHIVE_BYTES:
            raise PackageError("release package exceeds the verification size limit")
        archive_hash = sha256(archive_path.read_bytes())
    except OSError as exc:
        raise PackageError("release package is unavailable") from exc
    if checksum_path is not None and read_checksum(checksum_path, archive_path) != archive_hash:
        raise PackageError("release package checksum mismatch")
    try:
        with zipfile.ZipFile(archive_path, "r") as archive:
            infos = archive.infolist()
            names = [item.filename for item in infos]
            if len(infos) > MAX_ENTRIES:
                raise PackageError("release package exceeds the entry limit")
            if any(item.file_size > MAX_ENTRY_BYTES for item in infos) or sum(item.file_size for item in infos) > MAX_EXPANDED_BYTES:
                raise PackageError("release package exceeds the expanded-size limit")
            if len(names) != len(set(names)) or any(not safe_archive_path(name) for name in names):
                raise PackageError("release package contains duplicate or unsafe paths")
            if any((item.external_attr >> 16) & 0o170000 not in {0, 0o100000} for item in infos):
                raise PackageError("release package contains a non-regular entry")
            if PACKAGE_INDEX_REL not in names or MANIFEST_REL not in names:
                raise PackageError("release package lacks required metadata")
            if archive.getinfo(PACKAGE_INDEX_REL).file_size > MAX_INDEX_BYTES:
                raise PackageError("release package index exceeds the verification size limit")
            index = json.loads(archive.read(PACKAGE_INDEX_REL).decode("utf-8"))
            manifest = json.loads(archive.read(MANIFEST_REL).decode("utf-8"))
            if not isinstance(manifest, dict):
                raise PackageError("release package manifest contract is invalid")
            if not isinstance(index, dict) or set(index) != INDEX_FIELDS or index.get("contract") != CONTRACT or index.get("schema_version") != 1:
                raise PackageError("release package index contract is invalid")
            package_id = index.get("package_id")
            material = {key: value for key, value in index.items() if key != "package_id"}
            if not isinstance(package_id, str) or not SHA256_RE.fullmatch(package_id) or package_id != sha256(canonical(material)):
                raise PackageError("release package index hash is invalid")
            if (
                not isinstance(index.get("source_commit"), str)
                or not COMMIT_RE.fullmatch(index["source_commit"])
                or isinstance(index.get("source_epoch"), bool)
                or not isinstance(index.get("source_epoch"), int)
                or index["source_epoch"] < 0
                or index["source_epoch"] > MAX_ZIP_EPOCH
                or index.get("created_at") != datetime.fromtimestamp(index["source_epoch"], tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
                or index.get("source_repository") != manifest.get("source_repository")
                or index.get("layout") != "FOUNDATION_SOURCE_DISTRIBUTION"
                or index.get("selection") != "ALL_MANIFEST_COMPONENTS"
                or index.get("content_normalization") != "UTF8_CRLF_TO_LF_ELSE_EXACT"
                or index.get("install_command") != "python tools/install_foundation.py TARGET --adapters default --capabilities none --apply"
            ):
                raise PackageError("release package source or layout evidence is invalid")
            if index.get("ruleset_version") != manifest.get("ruleset_version"):
                raise PackageError("release package ruleset version mismatch")
            expected_time = zip_datetime(index["source_epoch"])
            if any(
                item.date_time != expected_time
                or item.compress_type != zipfile.ZIP_DEFLATED
                or ((item.external_attr >> 16) & 0o777) != 0o644
                for item in infos
            ):
                raise PackageError("release package is not reproducibly encoded")
            indexed = index.get("files")
            if not isinstance(indexed, list):
                raise PackageError("release package file index is invalid")
            by_path: dict[str, dict[str, Any]] = {}
            for entry in indexed:
                if not isinstance(entry, dict) or set(entry) != {"path", "role", "sha256", "portable_sha256", "size_bytes"}:
                    raise PackageError("release package file entry is invalid")
                path = entry["path"]
                role = entry["role"]
                if (
                    not isinstance(path, str)
                    or not safe_archive_path(path)
                    or not isinstance(entry["sha256"], str)
                    or not SHA256_RE.fullmatch(entry["sha256"])
                    or not isinstance(entry["portable_sha256"], str)
                    or not SHA256_RE.fullmatch(entry["portable_sha256"])
                    or isinstance(entry["size_bytes"], bool)
                    or not isinstance(entry["size_bytes"], int)
                    or entry["size_bytes"] < 0
                ):
                    raise PackageError("release package file index contains an invalid path")
                expected_role = "MANIFEST" if path == MANIFEST_REL else "INSTALLER" if path in BOOTSTRAP_PATHS else "PAYLOAD"
                if path in by_path or role != expected_role:
                    raise PackageError("release package file index contains an invalid path")
                by_path[path] = entry
            expected_paths = set(distribution_paths(manifest))
            if set(by_path) != expected_paths or set(names) != expected_paths | {PACKAGE_INDEX_REL}:
                raise PackageError("release package contains missing or unapproved files")
            for path, entry in by_path.items():
                body = archive.read(path)
                if (
                    entry["sha256"] != sha256(body)
                    or entry["portable_sha256"] != portable_content_sha256(body)
                    or entry["size_bytes"] != len(body)
                ):
                    raise PackageError(f"release package file evidence mismatch: {path}")
            expected_portable = {row["source"]: row["source_sha256"] for row in manifest_rows(manifest)}
            for path, expected in expected_portable.items():
                if by_path[path]["portable_sha256"] != expected:
                    raise PackageError(f"release package does not match its transfer manifest: {path}")
    except PackageError:
        raise
    except (OSError, zipfile.BadZipFile, KeyError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PackageError("release package is corrupt or invalid") from exc
    return {
        "status": "VERIFIED",
        "archive": str(archive_path.resolve()),
        "sha256": archive_hash,
        "package_id": index["package_id"],
        "ruleset_version": index["ruleset_version"],
        "source_commit": index["source_commit"],
        "entry_count": len(names),
        "checksum_verified": checksum_path is not None,
    }


def output(value: dict[str, Any]) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="operation", required=True)
    build = subparsers.add_parser("build")
    build.add_argument("--output", type=Path, required=True)
    verify = subparsers.add_parser("verify")
    verify.add_argument("--archive", type=Path, required=True)
    verify.add_argument("--sha256-file", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.operation == "build":
            commit, epoch = source_identity(ROOT)
            output(build_package(ROOT, args.output.resolve(), source_commit=commit, source_epoch=epoch))
        else:
            output(verify_package(args.archive.resolve(), args.sha256_file.resolve() if args.sha256_file else None))
        return 0
    except PackageError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
