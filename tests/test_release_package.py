from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import package_foundation  # noqa: E402


COMMIT = "1" * 40
EPOCH = 1_700_000_000


class ReleasePackageTests(unittest.TestCase):
    def build(self, directory: Path, name: str = "foundation.zip") -> tuple[Path, dict]:
        archive = directory / name
        report = package_foundation.build_package(
            ROOT,
            archive,
            source_commit=COMMIT,
            source_epoch=EPOCH,
        )
        return archive, report

    def test_build_is_deterministic_and_verifies_with_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first, first_report = self.build(root, "first.zip")
            second, second_report = self.build(root, "second.zip")
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(first_report["package_id"], second_report["package_id"])
            first_sidecar = first.with_name(first.name + ".sha256")
            verified = package_foundation.verify_package(first, first_sidecar)
            self.assertEqual(verified["status"], "VERIFIED")
            self.assertTrue(verified["checksum_verified"])
            self.assertEqual(verified["source_commit"], COMMIT)
            self.assertEqual(verified["sha256"], hashlib.sha256(first.read_bytes()).hexdigest())

    def test_archive_contains_only_whitelisted_distribution_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            archive, _ = self.build(Path(tmp))
            manifest = package_foundation.load_manifest(ROOT)
            expected = set(package_foundation.distribution_paths(manifest)) | {package_foundation.PACKAGE_INDEX_REL}
            with zipfile.ZipFile(archive) as package:
                self.assertEqual(set(package.namelist()), expected)
                index = json.loads(package.read(package_foundation.PACKAGE_INDEX_REL))
            self.assertNotIn(".ai/BACKLOG.md", expected)
            self.assertNotIn(".ai/identity/registry.json", expected)
            self.assertNotIn("README.md", expected)
            self.assertEqual(index["selection"], "ALL_MANIFEST_COMPONENTS")
            self.assertEqual(index["layout"], "FOUNDATION_SOURCE_DISTRIBUTION")

    def test_unapproved_or_modified_archive_content_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive, _ = self.build(root)
            unexpected = root / "unexpected.zip"
            unexpected.write_bytes(archive.read_bytes())
            with zipfile.ZipFile(unexpected, "a") as package:
                package.writestr("private/runtime.json", b"{}")
            with self.assertRaisesRegex(package_foundation.PackageError, "reproducibly encoded|unapproved"):
                package_foundation.verify_package(unexpected)

            modified = root / "modified.zip"
            with zipfile.ZipFile(archive) as source, zipfile.ZipFile(modified, "w") as target:
                for info in source.infolist():
                    body = source.read(info.filename)
                    if info.filename == "tools/install_foundation.py":
                        body += b"\n# modified\n"
                    target.writestr(info, body)
            with self.assertRaisesRegex(package_foundation.PackageError, "evidence mismatch"):
                package_foundation.verify_package(modified)

    def test_extracted_package_installs_and_preserves_source_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive, _ = self.build(root)
            extracted = root / "extracted"
            target = root / "target"
            extracted.mkdir()
            target.mkdir()
            with zipfile.ZipFile(archive) as package:
                package.extractall(extracted)
            process = subprocess.run(
                [
                    sys.executable,
                    str(extracted / "tools" / "install_foundation.py"),
                    str(target),
                    "--adapters",
                    "none",
                    "--capabilities",
                    "none",
                    "--apply",
                ],
                cwd=extracted,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(process.returncode, 0, process.stderr or process.stdout)
            provenance = json.loads(
                (target / ".ai" / "foundation" / "installation-provenance.json").read_text(encoding="utf-8")
            )
            self.assertEqual(provenance["source_commit"], COMMIT)

    def test_build_refuses_existing_output_and_invalid_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive, _ = self.build(root)
            with self.assertRaisesRegex(package_foundation.PackageError, "output already exists"):
                package_foundation.build_package(
                    ROOT,
                    archive,
                    source_commit=COMMIT,
                    source_epoch=EPOCH,
                )
            bad = root / "bad.sha256"
            bad.write_text(f"{'0' * 64}  {archive.name}\n", encoding="ascii")
            with self.assertRaisesRegex(package_foundation.PackageError, "checksum mismatch"):
                package_foundation.verify_package(archive, bad)


if __name__ == "__main__":
    unittest.main()
