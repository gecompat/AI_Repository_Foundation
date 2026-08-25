from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import transfer_manifest_guard  # noqa: E402


class TransferManifestGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = transfer_manifest_guard.load_manifest(ROOT)

    def codes(self, manifest: dict) -> set[str]:
        return {item["code"] for item in transfer_manifest_guard.validate_transfer_coverage(ROOT, manifest)}

    def test_current_repository_has_complete_transfer_coverage(self) -> None:
        self.assertEqual(transfer_manifest_guard.validate_transfer_coverage(ROOT, self.manifest), [])

    def test_generated_python_runtime_cache_is_not_transfer_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            capability = root / "foundation" / "capabilities" / "example"
            cache = capability / "__pycache__"
            cache.mkdir(parents=True)
            (capability / "tool.py").write_text("print('ok')\n", encoding="utf-8")
            (cache / "tool.cpython-312.pyc").write_bytes(b"runtime-cache")
            files = transfer_manifest_guard.collect_files(root, "foundation/capabilities", [], True)
            self.assertEqual(files, {"foundation/capabilities/example/tool.py"})

    def test_version_drift_is_blocking(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["ruleset_version"] = "9.9.9"
        self.assertIn("TRANSFER_VERSION_MISMATCH", self.codes(manifest))

    def test_unmanifested_policy_is_blocking(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["core"] = [
            row for row in manifest["core"]
            if row["source"] != "Documentation/Standards/ARTIFACT_REGISTRATION_POLICY.md"
        ]
        self.assertIn("TRANSFER_CORE_SOURCE_UNCLASSIFIED", self.codes(manifest))

    def test_unmanifested_schema_is_blocking(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["core"] = [
            row for row in manifest["core"]
            if row["source"] != "foundation/schemas/artifact-record.schema.json"
        ]
        codes = self.codes(manifest)
        self.assertIn("TRANSFER_CORE_SOURCE_UNCLASSIFIED", codes)
        self.assertIn("TRANSFER_CONTRACT_SCHEMA_UNCLASSIFIED", codes)

    def test_unmanifested_capability_file_is_blocking(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["capabilities"]["artifact-registration-clients"] = [
            row for row in manifest["capabilities"]["artifact-registration-clients"]
            if row["source"] != "tools/identity/ArtifactReference.ps1"
        ]
        self.assertIn("TRANSFER_CAPABILITY_SOURCE_UNCLASSIFIED", self.codes(manifest))

    def test_capability_source_outside_managed_roots_is_blocking(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["capabilities"]["bad-capability"] = [
            {
                "source": "README.md",
                "target": ".ai/foundation/reference_clients/bad.txt",
                "kind": "reference-client",
                "merge": "review_if_exists",
            }
        ]
        self.assertIn("TRANSFER_CAPABILITY_SOURCE_OUTSIDE_MANAGED_ROOT", self.codes(manifest))

    def test_every_standard_and_foundation_schema_is_manifest_core(self) -> None:
        core_sources = {row["source"] for row in self.manifest["core"]}
        standards = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "Documentation" / "Standards").glob("*.md")
            if path.is_file()
        }
        schemas = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "foundation" / "schemas").rglob("*.json")
            if path.is_file()
        }
        self.assertTrue(standards)
        self.assertTrue(schemas)
        self.assertTrue(standards.issubset(core_sources))
        self.assertTrue(schemas.issubset(core_sources))


if __name__ == "__main__":
    unittest.main()
