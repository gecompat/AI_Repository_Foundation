from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "github" / "configure_branch_protection.py"
spec = importlib.util.spec_from_file_location("configure_branch_protection", TOOL)
configure_branch_protection = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(configure_branch_protection)


class GithubBranchProtectionTests(unittest.TestCase):
    def test_default_payload_requires_foundation_checks_and_hardening(self) -> None:
        payload = configure_branch_protection.desired_payload(configure_branch_protection.DEFAULT_CHECKS)
        status = payload["required_status_checks"]
        self.assertTrue(status["strict"])
        self.assertEqual(
            [row["context"] for row in status["checks"]],
            ["validate", "registry-integrity"],
        )
        self.assertTrue(payload["enforce_admins"])
        self.assertTrue(payload["required_linear_history"])
        self.assertFalse(payload["allow_force_pushes"])
        self.assertFalse(payload["allow_deletions"])
        self.assertIsNone(payload["required_pull_request_reviews"])
        self.assertIsNone(payload["restrictions"])

    def test_verify_accepts_expected_effective_state(self) -> None:
        protection = {
            "required_status_checks": {
                "strict": True,
                "contexts": ["validate", "registry-integrity"],
            },
            "enforce_admins": {"enabled": True},
            "required_linear_history": {"enabled": True},
            "allow_force_pushes": {"enabled": False},
            "allow_deletions": {"enabled": False},
        }
        self.assertEqual(
            configure_branch_protection.verify(protection, configure_branch_protection.DEFAULT_CHECKS),
            [],
        )

    def test_verify_reports_missing_server_controls(self) -> None:
        protection = {
            "required_status_checks": {"strict": False, "contexts": ["validate"]},
            "enforce_admins": {"enabled": False},
            "required_linear_history": {"enabled": False},
            "allow_force_pushes": {"enabled": True},
            "allow_deletions": {"enabled": True},
        }
        problems = configure_branch_protection.verify(
            protection, configure_branch_protection.DEFAULT_CHECKS
        )
        joined = "\n".join(problems)
        self.assertIn("strict/up-to-date", joined)
        self.assertIn("registry-integrity", joined)
        self.assertIn("administrator enforcement", joined)
        self.assertIn("linear history", joined)
        self.assertIn("force pushes", joined)
        self.assertIn("branch deletion", joined)


if __name__ == "__main__":
    unittest.main()
