from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "github" / "configure_rulesets.py"
spec = importlib.util.spec_from_file_location("configure_rulesets", TOOL)
configure_rulesets = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(configure_rulesets)


class RepositoryContinuityTests(unittest.TestCase):
    def test_core_ruleset_has_no_bypass_and_preserves_branch_safety(self) -> None:
        payload = configure_rulesets.core_payload("main")
        self.assertEqual(payload["name"], "foundation-main-core-safety")
        self.assertEqual(payload["enforcement"], "active")
        self.assertEqual(payload["bypass_actors"], [])
        self.assertIn("refs/heads/main", payload["conditions"]["ref_name"]["include"])
        types = {row["type"] for row in payload["rules"]}
        self.assertEqual(
            types,
            {"pull_request", "required_linear_history", "non_fast_forward", "deletion"},
        )
        pull = next(row for row in payload["rules"] if row["type"] == "pull_request")
        self.assertEqual(pull["parameters"]["required_approving_review_count"], 0)
        self.assertEqual(configure_rulesets.verify_core(payload, "main"), [])

    def test_ci_ruleset_has_strict_checks_and_pull_request_only_user_bypass(self) -> None:
        payload = configure_rulesets.ci_payload(
            "main", ["validate", "registry-integrity"], 48807214
        )
        self.assertEqual(payload["name"], "foundation-main-ci-gates")
        self.assertEqual(
            payload["bypass_actors"],
            [{"actor_id": 48807214, "actor_type": "User", "bypass_mode": "pull_request"}],
        )
        status = next(row for row in payload["rules"] if row["type"] == "required_status_checks")
        self.assertTrue(status["parameters"]["strict_required_status_checks_policy"])
        self.assertEqual(
            {row["context"] for row in status["parameters"]["required_status_checks"]},
            {"validate", "registry-integrity"},
        )
        self.assertEqual(
            configure_rulesets.verify_ci(
                payload, "main", ["validate", "registry-integrity"], 48807214
            ),
            [],
        )

    def test_ci_ruleset_rejects_always_bypass_and_missing_checks(self) -> None:
        payload = configure_rulesets.ci_payload(
            "main", ["validate", "registry-integrity"], 48807214
        )
        payload["bypass_actors"][0]["bypass_mode"] = "always"
        status = next(row for row in payload["rules"] if row["type"] == "required_status_checks")
        status["parameters"]["required_status_checks"] = [{"context": "validate"}]
        joined = "\n".join(
            configure_rulesets.verify_ci(
                payload, "main", ["validate", "registry-integrity"], 48807214
            )
        )
        self.assertIn("pull_request-only bypass", joined)
        self.assertIn("registry-integrity", joined)

    def test_transfer_contains_continuity_policy_and_break_glass_is_not_auto_admin(self) -> None:
        manifest = json.loads((ROOT / "foundation" / "manifest.json").read_text(encoding="utf-8"))
        rows = {row["target"]: row for row in manifest["core"]}
        self.assertIn(".ai/foundation/REPOSITORY_CONTINUITY_POLICY.md", rows)
        self.assertEqual(
            rows[".ai/foundation/REPOSITORY_CONTINUITY_POLICY.md"]["source"],
            "Documentation/Standards/REPOSITORY_CONTINUITY_POLICY.md",
        )
        policy = (ROOT / "Documentation" / "Standards" / "REPOSITORY_CONTINUITY_POLICY.md").read_text(encoding="utf-8")
        transfer = (ROOT / "foundation" / "AI_TRANSFER.md").read_text(encoding="utf-8")
        for token in ["VALIDATION_FAILURE", "INFRASTRUCTURE_UNAVAILABLE", "UNKNOWN"]:
            self.assertIn(token, policy)
            self.assertIn(token, transfer)
        self.assertIn("Break-glass is prohibited", transfer)
        self.assertIn("For pull requests only", transfer)
        self.assertIn("MUST NOT silently create Rulesets", transfer)

    def test_feature_catalog_surfaces_continuity_as_recommendation(self) -> None:
        catalog = json.loads((ROOT / "foundation" / "feature_catalog.json").read_text(encoding="utf-8"))
        feature = catalog["features"]["repository-continuity-break-glass"]
        self.assertEqual(feature["introduced_in"], "1.7.0")
        self.assertEqual(feature["recommendation"]["when_applicable"], "RECOMMENDED")
        self.assertIn("required_ci_checks", feature["applicability"]["signals"])
        self.assertIn("enabling a repository break-glass path", feature["recommendation"]["decision_required_when"])


if __name__ == "__main__":
    unittest.main()
