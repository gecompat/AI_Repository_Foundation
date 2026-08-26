from __future__ import annotations

import importlib.util
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock

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

    def test_core_ruleset_rejects_missing_or_extra_safety_state(self) -> None:
        payload = configure_rulesets.core_payload("main")
        payload.pop("bypass_actors")
        payload["conditions"]["ref_name"]["include"].append("refs/heads/release")
        pull = next(row for row in payload["rules"] if row["type"] == "pull_request")
        pull["parameters"]["required_approving_review_count"] = 1
        joined = "\n".join(configure_rulesets.verify_core(payload, "main"))
        self.assertIn("no bypass actors", joined)
        self.assertIn("target only refs/heads/main", joined)
        self.assertIn("required_approving_review_count", joined)

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
        self.assertIn("required checks must be exactly", joined)

    def test_ci_ruleset_rejects_additional_bypass_or_direct_push_path(self) -> None:
        payload = configure_rulesets.ci_payload(
            "main", ["validate", "registry-integrity"], 48807214
        )
        payload["bypass_actors"].append(
            {"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}
        )
        joined = "\n".join(
            configure_rulesets.verify_ci(
                payload, "main", ["validate", "registry-integrity"], 48807214
            )
        )
        self.assertIn("exactly the authorized user", joined)
        self.assertIn("no other bypass actors", joined)

    def test_ci_ruleset_rejects_non_exact_conditions_and_status_parameters(self) -> None:
        payload = configure_rulesets.ci_payload(
            "main", ["validate", "registry-integrity"], 48807214
        )
        payload["conditions"]["ref_name"]["exclude"] = ["refs/heads/main"]
        status = next(row for row in payload["rules"] if row["type"] == "required_status_checks")
        status["parameters"].pop("do_not_enforce_on_create")
        status["parameters"]["required_status_checks"].append(
            {"context": "unexpected", "integration_id": 99}
        )
        joined = "\n".join(
            configure_rulesets.verify_ci(
                payload, "main", ["validate", "registry-integrity"], 48807214
            )
        )
        self.assertIn("target only refs/heads/main", joined)
        self.assertIn("enforced on branch creation", joined)
        self.assertIn("required checks must be exactly", joined)
        self.assertIn("unexpected integration", joined)

    def test_migration_deletes_classic_only_after_verified_rulesets(self) -> None:
        core = configure_rulesets.core_payload("main")
        ci = configure_rulesets.ci_payload(
            "main", ["validate", "registry-integrity"], 48807214
        )
        events: list[str] = []

        def fake_upsert(base_url: str, token: str, payload: dict) -> dict:
            events.append(f"upsert:{payload['name']}")
            return payload

        locate_values = iter([None, core, ci])

        def fake_locate(base_url: str, token: str, name: str) -> dict | None:
            events.append(f"locate:{name}")
            return next(locate_values)

        protection_values = iter([True, True, False])

        def fake_protection(base_url: str, token: str, branch: str) -> bool:
            value = next(protection_values)
            events.append(f"classic:{value}")
            return value

        def fake_request(method: str, url: str, token: str, payload: dict | None = None) -> None:
            self.assertEqual(method, "DELETE")
            events.append("delete-classic")

        with (
            mock.patch.dict("os.environ", {"GITHUB_ADMIN_TOKEN": "test-token"}),
            mock.patch.object(configure_rulesets, "resolve_user_id", return_value=48807214),
            mock.patch.object(configure_rulesets, "upsert", side_effect=fake_upsert),
            mock.patch.object(configure_rulesets, "locate", side_effect=fake_locate),
            mock.patch.object(
                configure_rulesets,
                "classic_protection_exists",
                side_effect=fake_protection,
            ),
            mock.patch.object(configure_rulesets, "request", side_effect=fake_request),
            redirect_stdout(StringIO()),
            redirect_stderr(StringIO()),
        ):
            self.assertEqual(configure_rulesets.main([]), 0)

        delete_index = events.index("delete-classic")
        self.assertLess(events.index(f"upsert:{configure_rulesets.CORE_NAME}"), delete_index)
        self.assertLess(events.index(f"upsert:{configure_rulesets.CI_NAME}"), delete_index)
        self.assertEqual(events[-1], "classic:False")

    def test_verify_only_fails_when_classic_protection_remains(self) -> None:
        core = configure_rulesets.core_payload("main")
        ci = configure_rulesets.ci_payload(
            "main", ["validate", "registry-integrity"], 48807214
        )
        with (
            mock.patch.dict("os.environ", {"GITHUB_ADMIN_TOKEN": "test-token"}),
            mock.patch.object(configure_rulesets, "resolve_user_id", return_value=48807214),
            mock.patch.object(
                configure_rulesets,
                "classic_protection_exists",
                side_effect=[True, True],
            ),
            mock.patch.object(configure_rulesets, "locate", side_effect=[core, ci, core, ci]),
            redirect_stdout(StringIO()),
            redirect_stderr(StringIO()),
        ):
            self.assertEqual(configure_rulesets.main(["--verify-only"]), 2)

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
