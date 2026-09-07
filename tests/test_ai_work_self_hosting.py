from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AIWorkSelfHostingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.profile = json.loads((ROOT / ".ai" / "ai-work" / "profile.json").read_text(encoding="utf-8"))

    def test_source_profile_is_provider_free_and_runtime_external(self) -> None:
        self.assertEqual(self.profile["contract"], "foundation-ai-work/v1")
        self.assertEqual(self.profile["provider_requirements"], [])
        self.assertEqual(self.profile["runtime_inventory_location"], "OUTSIDE_REPOSITORY")
        self.assertEqual(self.profile["client_dispatch"]["client_requirements"], [])
        self.assertEqual(self.profile["client_dispatch"]["runtime_state_location"], "OUTSIDE_REPOSITORY")
        text = json.dumps(self.profile).lower()
        for forbidden in ("ollama", "openai", "lm studio", "c:\\", "d:\\", "token", "credential"):
            self.assertNotIn(forbidden, text)

    def test_source_profile_covers_representative_open_work_classes(self) -> None:
        profiles = self.profile["task_profiles"]
        self.assertEqual(
            set(profiles),
            {"software.change", "research.sourced", "documentation.author", "data.structured", "project.custom"},
        )
        self.assertEqual(self.profile["degradation"]["no_capability"], "MANUAL_REQUIRED")
        self.assertEqual(self.profile["degradation"]["provider_failure"], "EXCLUDE_PROVIDER_FRAGMENT_ONLY")
        dispatch = self.profile["client_dispatch"]
        self.assertEqual(dispatch["requested_without_actual_evidence"], "REQUESTED_NOT_ATTESTED")
        self.assertEqual(dispatch["manual_fallback"], "MANUAL_DISPATCH_REQUIRED")
        self.assertEqual(dispatch["actual_model_evidence"], ["HOST_EXECUTION", "HOST_RESPONSE_METADATA"])
        self.assertEqual(dispatch["trusted_dispatch_issuers"], [])

    def test_foundation_validation_is_shell_free_and_maps_existing_gates(self) -> None:
        validation = self.profile["validation_capabilities"]["foundation.validate"]
        self.assertFalse(validation["shell_evaluation"])
        commands = validation["commands"]
        self.assertTrue(all(isinstance(command, list) and command for command in commands))
        flat = [item for command in commands for item in command]
        for required in (
            "tools/transfer_manifest_guard.py",
            "tools/feature_catalog_guard.py",
            "foundation/capabilities/artifact-registry-github/registry_semantic.py",
            "tools/foundation_validator.py",
            "unittest",
        ):
            self.assertIn(required, flat)

    def test_source_profile_is_not_transfer_payload(self) -> None:
        manifest = json.loads((ROOT / "foundation" / "manifest.json").read_text(encoding="utf-8"))
        sources = {item["source"] for item in manifest["core"]}
        for rows in manifest["adapters"].values():
            sources.update(item["source"] for item in rows)
        for rows in manifest["capabilities"].values():
            sources.update(item["source"] for item in rows)
        self.assertNotIn(".ai/AI_WORK_PROFILE.md", sources)
        self.assertNotIn(".ai/ai-work/profile.json", sources)


if __name__ == "__main__":
    unittest.main()
