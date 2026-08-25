from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "foundation" / "capabilities" / "artifact-registry-github" / "registry_semantic.py"
spec = importlib.util.spec_from_file_location("registry_semantic", TOOL)
registry_semantic = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(registry_semantic)


class CentralArtifactRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads((ROOT / ".ai" / "identity" / "registry.json").read_text(encoding="utf-8"))

    def test_foundation_source_uses_v2_without_allocator_counters(self) -> None:
        self.assertEqual(self.registry["schema_version"], 2)
        self.assertEqual(self.registry["profile"], "foundation-artifact-registry/v2")
        self.assertNotIn("registry_revision", self.registry)
        self.assertTrue(all("next_sequence" not in row for row in self.registry["prefixes"].values()))
        self.assertEqual(registry_semantic.validate_registry(self.registry), [])

    def test_next_sequence_is_derived_from_canonical_keys(self) -> None:
        self.assertEqual(registry_semantic.next_reference(self.registry, "WI"), "WI-0015")
        self.assertEqual(registry_semantic.next_reference(self.registry, "DEC"), "DEC-0016")
        self.assertEqual(
            registry_semantic.next_reference(self.registry, "WI", {"WI-0015", "WI-0017"}),
            "WI-0018",
        )

    def test_independent_artifact_additions_merge_by_object(self) -> None:
        base = copy.deepcopy(self.registry)
        main = copy.deepcopy(base)
        head = copy.deepcopy(base)
        main["artifacts"]["WI-0015"] = {
            "artifact_uid": "urn:uuid:018f11aa-0000-7000-8000-000000000001",
            "kind": "work_item",
            "title": "Main work",
            "registration_state": "REGISTERED",
            "aliases": [],
            "relations": [],
        }
        head["artifacts"]["WI-0016"] = {
            "artifact_uid": "urn:uuid:018f11aa-0000-7000-8000-000000000002",
            "kind": "work_item",
            "title": "Head work",
            "registration_state": "REGISTERED",
            "aliases": [],
            "relations": [],
        }
        merged, conflicts = registry_semantic.semantic_merge(base, main, head)
        self.assertEqual(conflicts, [])
        self.assertIn("WI-0015", merged["artifacts"])
        self.assertIn("WI-0016", merged["artifacts"])

    def test_concurrent_same_reference_add_is_blocking(self) -> None:
        base = copy.deepcopy(self.registry)
        main = copy.deepcopy(base)
        head = copy.deepcopy(base)
        main["artifacts"]["WI-0015"] = {
            "artifact_uid": "urn:uuid:018f11aa-0000-7000-8000-000000000003",
            "kind": "work_item", "title": "A", "registration_state": "REGISTERED"
        }
        head["artifacts"]["WI-0015"] = {
            "artifact_uid": "urn:uuid:018f11aa-0000-7000-8000-000000000004",
            "kind": "work_item", "title": "B", "registration_state": "REGISTERED"
        }
        _, conflicts = registry_semantic.semantic_merge(base, main, head)
        self.assertTrue(any("CONCURRENT_ADD artifacts.WI-0015" in value for value in conflicts))

    def test_independent_properties_of_same_artifact_merge(self) -> None:
        base = copy.deepcopy(self.registry)
        main = copy.deepcopy(base)
        head = copy.deepcopy(base)
        base["artifacts"]["WI-0014"]["status"] = "in_progress"
        main = copy.deepcopy(base)
        head = copy.deepcopy(base)
        main["artifacts"]["WI-0014"]["status"] = "blocked"
        head["artifacts"]["WI-0014"]["priority"] = "medium"
        merged, conflicts = registry_semantic.semantic_merge(base, main, head)
        self.assertEqual(conflicts, [])
        self.assertEqual(merged["artifacts"]["WI-0014"]["status"], "blocked")
        self.assertEqual(merged["artifacts"]["WI-0014"]["priority"], "medium")

    def test_same_property_changed_differently_is_blocking(self) -> None:
        base = copy.deepcopy(self.registry)
        base["artifacts"]["WI-0014"]["status"] = "in_progress"
        main = copy.deepcopy(base)
        head = copy.deepcopy(base)
        main["artifacts"]["WI-0014"]["status"] = "blocked"
        head["artifacts"]["WI-0014"]["status"] = "done"
        _, conflicts = registry_semantic.semantic_merge(base, main, head)
        self.assertTrue(any("VALUE_CONFLICT artifacts.WI-0014.status" in value for value in conflicts))

    def test_registered_reference_removal_is_blocking(self) -> None:
        new = copy.deepcopy(self.registry)
        del new["artifacts"]["WI-0014"]
        problems = registry_semantic.validate_transition(self.registry, new, "test")
        self.assertTrue(any("registered reference removed" in value for value in problems))

    def test_duplicate_uid_alias_and_cycle_are_blocking(self) -> None:
        value = copy.deepcopy(self.registry)
        value["artifacts"]["WI-0014"]["artifact_uid"] = value["artifacts"]["WI-0013"]["artifact_uid"]
        self.assertTrue(any("artifact UID" in item for item in registry_semantic.validate_registry(value)))

        value = copy.deepcopy(self.registry)
        value["artifacts"]["WI-0014"]["aliases"] = ["FND-001"]
        self.assertTrue(any("alias FND-001" in item for item in registry_semantic.validate_registry(value)))

        value = copy.deepcopy(self.registry)
        value["artifacts"]["WI-0013"]["relations"] = [{"type": "depends_on", "target": "WI-0014"}]
        self.assertTrue(any("depends_on cycle" in item for item in registry_semantic.validate_registry(value)))

    def test_backlog_is_generated_from_registry(self) -> None:
        expected = registry_semantic.backlog_text(self.registry)
        actual = (ROOT / ".ai" / "BACKLOG.md").read_text(encoding="utf-8")
        self.assertEqual(actual, expected)
        self.assertIn("WI-0014", actual)

    def test_manifest_exposes_optional_github_registry_capability(self) -> None:
        manifest = json.loads((ROOT / "foundation" / "manifest.json").read_text(encoding="utf-8"))
        rows = manifest["capabilities"]["artifact-registry-github"]
        sources = {row["source"] for row in rows}
        self.assertIn("foundation/capabilities/artifact-registry-github/registry_semantic.py", sources)
        self.assertIn("foundation/capabilities/artifact-registry-github/artifact-registry-integrity.yml", sources)
        self.assertEqual(manifest["registration_contract"]["default_registry_profile"], "foundation-artifact-registry/v2")


if __name__ == "__main__":
    unittest.main()
