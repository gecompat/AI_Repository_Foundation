from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import foundation_validator  # noqa: E402
import install_foundation  # noqa: E402
import refresh_manifest_hashes  # noqa: E402
import transfer_manifest_guard  # noqa: E402
from content_equivalence import portable_content_sha256, portable_file_sha256  # noqa: E402


class InstallationProvenanceTests(unittest.TestCase):
    def install(self, target: Path) -> tuple[int, str]:
        output = StringIO()
        with redirect_stdout(output):
            rc = install_foundation.main([str(target), "--adapters", "none", "--apply"])
        return rc, output.getvalue()

    def validate(self, target: Path) -> tuple[int, dict]:
        output = StringIO()
        with redirect_stdout(output):
            rc = foundation_validator.main(["--target", str(target), "--adapters", "none", "--json"])
        return rc, json.loads(output.getvalue())

    def test_manifest_hashes_match_all_transfer_sources(self) -> None:
        manifest = install_foundation.load_manifest()
        rows = list(manifest["core"])
        for section in (manifest["adapters"], manifest["capabilities"]):
            for values in section.values():
                rows.extend(values)
        self.assertGreater(len(rows), 80)
        for row in rows:
            self.assertEqual(row["source_sha256"], portable_file_sha256(ROOT / row["source"]), row["source"])
        refreshed, changed = refresh_manifest_hashes.refresh_text(
            (ROOT / "foundation" / "manifest.json").read_text(encoding="utf-8"), ROOT
        )
        self.assertEqual(changed, [])
        self.assertEqual(refreshed, (ROOT / "foundation" / "manifest.json").read_text(encoding="utf-8"))

    def test_portable_hash_normalizes_only_crlf(self) -> None:
        self.assertEqual(portable_content_sha256(b"one\ntwo\n"), portable_content_sha256(b"one\r\ntwo\r\n"))
        self.assertNotEqual(portable_content_sha256(b"one\ntwo\n"), portable_content_sha256(b"one\rtwo\r"))
        self.assertNotEqual(portable_content_sha256(b"one\n"), portable_content_sha256(b"one"))

    def test_hash_refresher_handles_inline_adapter_rows(self) -> None:
        text = (
            '  "adapter": [{"source": "CLAUDE.md", "target": "CLAUDE.md", '
            '"kind": "adapter", "merge": "ai_merge_if_exists"}]\n'
        )
        refreshed, changed = refresh_manifest_hashes.refresh_text(text, ROOT)
        self.assertEqual(changed, ["CLAUDE.md"])
        self.assertIn(f'"source_sha256": "{portable_file_sha256(ROOT / "CLAUDE.md")}"', refreshed)

    def test_clean_apply_writes_idempotent_content_minimized_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "README.md").write_text("Synthetic target\n", encoding="utf-8")
            (target / "LICENSE").write_text("Synthetic license\n", encoding="utf-8")
            rc, output = self.install(target)
            self.assertEqual(rc, 0, output)
            receipt_path = target / ".ai" / "foundation" / "installation-provenance.json"
            receipt_text = receipt_path.read_text(encoding="utf-8")
            receipt = json.loads(receipt_text)
            self.assertEqual(receipt["contract"], "foundation-installation-provenance/v1")
            self.assertEqual(receipt["ruleset_version"], "1.18.0")
            self.assertEqual(receipt["selection"], {"adapters": [], "capabilities": []})
            self.assertTrue(all(row["integration_state"] == "FOUNDATION_BASELINE" for row in receipt["files"]))
            self.assertNotIn(str(target), receipt_text)
            self.assertNotIn("prompt", receipt_text.lower())
            self.assertNotIn("response", receipt_text.lower())
            self.assertEqual(receipt["source_manifest_sha256"], portable_file_sha256(ROOT / "foundation" / "manifest.json"))

            second_rc, second_output = self.install(target)
            self.assertEqual(second_rc, 0, second_output)
            self.assertIn("[PROVENANCE] unchanged=", second_output)
            self.assertEqual(receipt_text, receipt_path.read_text(encoding="utf-8"))

            validation_rc, validation = self.validate(target)
            self.assertEqual(validation_rc, 0)
            codes = [item["code"] for item in validation["results"]]
            self.assertIn("UNCHANGED_CURRENT_BASELINE", codes)
            self.assertNotIn("UNKNOWN_DRIFT", codes)

    def test_semantic_override_requires_reason_and_is_distinguished_from_later_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target)[0], 0)
            rule = target / ".ai" / "foundation" / "PROJECT_RULES.md"
            rule.write_text(rule.read_text(encoding="utf-8") + "\nTarget-specific stricter rule.\n", encoding="utf-8")

            blocked = StringIO()
            with redirect_stdout(blocked):
                blocked_rc = install_foundation.main([str(target), "--adapters", "none", "--record-provenance"])
            self.assertEqual(blocked_rc, 2)
            self.assertIn("require explicit --intentional-override", blocked.getvalue())

            recorded = StringIO()
            with redirect_stdout(recorded):
                recorded_rc = install_foundation.main([
                    str(target), "--adapters", "none", "--record-provenance",
                    "--intentional-override", ".ai/foundation/PROJECT_RULES.md=Preserved a stricter target rule",
                ])
            self.assertEqual(recorded_rc, 0, recorded.getvalue())
            validation_rc, validation = self.validate(target)
            self.assertEqual(validation_rc, 0)
            matching = [item for item in validation["results"] if item["path"] == ".ai/foundation/PROJECT_RULES.md"]
            self.assertIn("INTENTIONAL_OVERRIDE", {item["code"] for item in matching})
            self.assertIn("LOCAL_OVERRIDE_OR_DRIFT", {item["code"] for item in matching})

            rule.write_text(rule.read_text(encoding="utf-8") + "Unrecorded edit.\n", encoding="utf-8")
            validation_rc, validation = self.validate(target)
            self.assertEqual(validation_rc, 0)
            matching = [item for item in validation["results"] if item["path"] == ".ai/foundation/PROJECT_RULES.md"]
            self.assertIn("UNKNOWN_DRIFT", {item["code"] for item in matching})
            self.assertNotIn("INTENTIONAL_OVERRIDE", {item["code"] for item in matching})

    def test_previous_version_receipt_is_distinguished(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target)[0], 0)
            receipt_path = target / ".ai" / "foundation" / "installation-provenance.json"
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt["ruleset_version"] = "1.14.0"
            receipt["source_manifest_sha256"] = "0" * 64
            receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
            validation_rc, validation = self.validate(target)
            self.assertEqual(validation_rc, 0)
            codes = [item["code"] for item in validation["results"]]
            self.assertIn("PREVIOUS_FOUNDATION_VERSION", codes)
            self.assertNotIn("UNKNOWN_DRIFT", codes)

    def test_missing_or_invalid_receipt_never_claims_an_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(self.install(target)[0], 0)
            receipt_path = target / ".ai" / "foundation" / "installation-provenance.json"
            receipt_path.write_text("{}\n", encoding="utf-8")
            rule = target / ".ai" / "foundation" / "PROJECT_RULES.md"
            rule.write_text(rule.read_text(encoding="utf-8") + "\nUnproven difference.\n", encoding="utf-8")
            validation_rc, validation = self.validate(target)
            self.assertEqual(validation_rc, 0)
            codes = [item["code"] for item in validation["results"]]
            self.assertIn("INSTALLED_PROVENANCE_INVALID", codes)
            self.assertIn("UNKNOWN_DRIFT", codes)
            self.assertNotIn("INTENTIONAL_OVERRIDE", codes)

    def test_transfer_guard_rejects_a_stale_manifest_hash(self) -> None:
        manifest = install_foundation.load_manifest()
        manifest["core"][0]["source_sha256"] = "0" * 64
        issues = transfer_manifest_guard.validate_transfer_coverage(ROOT, manifest)
        self.assertTrue(any(item["code"] == "TRANSFER_SOURCE_HASH_MISMATCH" for item in issues))


if __name__ == "__main__":
    unittest.main()
