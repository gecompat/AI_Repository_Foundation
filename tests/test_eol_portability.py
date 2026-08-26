from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import content_equivalence  # noqa: E402
import foundation_validator  # noqa: E402
import install_foundation  # noqa: E402


class EolPortabilityTests(unittest.TestCase):
    def test_content_equivalence_normalizes_only_utf8_crlf(self) -> None:
        self.assertTrue(content_equivalence.content_equivalent(b"alpha\nbeta\n", b"alpha\r\nbeta\r\n"))
        self.assertFalse(content_equivalence.content_equivalent(b"alpha\nbeta\n", b"alpha\r\ngamma\r\n"))
        self.assertFalse(content_equivalence.content_equivalent(b"alpha\rbeta", b"alpha\nbeta"))
        self.assertFalse(content_equivalence.content_equivalent(b"\x00\x01", b"\x00\x02"))

    def test_temporary_git_repo_survives_autocrlf_checkout_without_false_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "target"
            target.mkdir()

            def git(*args: str) -> subprocess.CompletedProcess[str]:
                return subprocess.run(
                    ["git", "-C", str(target), *args],
                    text=True,
                    capture_output=True,
                    check=True,
                )

            git("init", "-b", "main")
            git("config", "user.name", "Foundation CI")
            git("config", "user.email", "foundation-ci@example.invalid")
            git("config", "core.autocrlf", "true")

            with redirect_stdout(StringIO()):
                self.assertEqual(
                    install_foundation.main([str(target), "--adapters", "none", "--apply"]),
                    0,
                )
            self.assertFalse((target / ".gitattributes").exists())

            git("add", ".")
            git("commit", "-m", "Install Foundation")

            foundation_dir = target / ".ai" / "foundation"
            shutil.rmtree(foundation_dir)
            git("checkout", "--", ".ai/foundation")

            probe = foundation_dir / "PROJECT_RULES.md"
            self.assertIn(b"\r\n", probe.read_bytes(), "core.autocrlf=true did not create the intended CRLF test fixture")

            manifest = install_foundation.load_manifest()
            entries = install_foundation.transfer_entries(manifest, [])
            plan = install_foundation.build_plan(target, entries)
            self.assertTrue(plan)
            self.assertTrue(all(item.state == "UNCHANGED" for item in plan))

            output = StringIO()
            with redirect_stdout(output):
                rc = foundation_validator.main([
                    "--target", str(target),
                    "--adapters", "none",
                    "--json",
                ])
            self.assertEqual(rc, 0)
            payload = json.loads(output.getvalue())
            self.assertFalse(any(item["code"] == "LOCAL_OVERRIDE_OR_DRIFT" for item in payload["results"]))

            probe.write_bytes(probe.read_bytes() + b"\r\nActual semantic drift\r\n")
            changed_plan = install_foundation.build_plan(target, entries)
            changed = {item.entry.target_rel.as_posix(): item.state for item in changed_plan}
            self.assertEqual(changed[".ai/foundation/PROJECT_RULES.md"], "MERGE_REQUIRED")

            output = StringIO()
            with redirect_stdout(output):
                rc = foundation_validator.main([
                    "--target", str(target),
                    "--adapters", "none",
                    "--json",
                ])
            self.assertEqual(rc, 0)
            payload = json.loads(output.getvalue())
            self.assertTrue(
                any(
                    item["code"] == "LOCAL_OVERRIDE_OR_DRIFT"
                    and item["path"] == ".ai/foundation/PROJECT_RULES.md"
                    for item in payload["results"]
                )
            )


if __name__ == "__main__":
    unittest.main()
