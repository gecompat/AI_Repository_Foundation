from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


preparation = load_module(
    "foundation_ai_host_preparation_tests",
    ROOT / "foundation" / "capabilities" / "ai-provisioning" / "host_preparation.py",
)
AT = datetime(2026, 9, 7, 12, 0, tzinfo=timezone.utc)


class AIHostPreparationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.state = preparation.ProvisionStore(self.root / "state")
        self.source = self.root / "source.bin"
        self.source.write_bytes(b"bounded artifact")
        self.source_hash = preparation.file_digest(self.source)
        self.target = self.root / "target" / "artifact.bin"

    def definition(self, runtime_id: str = "synthetic", *, inventory_argv=None, inventory_format="NONE"):
        executable = str(Path(sys.executable).resolve())
        return {
            "runtime_id": runtime_id,
            "executable_names": ["foundation-runtime-that-is-not-on-path"],
            "search_paths": [executable],
            "version_argv": ["{executable}", "--version"],
            "inventory_argv": inventory_argv or ["{executable}", "--version"],
            "inventory_format": inventory_format,
            "environment_allowlist": [],
            "timeout_seconds": 10,
            "health_ttl_seconds": 300,
            "execution_boundary": "HOST",
        }

    def request(self, **updates):
        value = {
            "schema_version": 1,
            "contract": preparation.CONTRACT,
            "request_id": "request-1",
            "artifact_id": "artifact-1",
            "target_runtime": "synthetic",
            "target_path": str(self.target),
            "valid_for_seconds": 3600,
            "limits": {
                "max_download_mb": 1,
                "max_disk_mb": 2,
                "max_memory_mb": 16,
                "max_cost_usd": 0,
            },
            "authorization": {
                "network_authorized": False,
                "allowed_network_destinations": [],
                "environment_allowlist": [],
            },
        }
        value.update(updates)
        return value

    def recipe(self, **updates):
        value = {
            "recipe_id": "recipe-1",
            "artifact_id": "artifact-1",
            "target_runtime": "synthetic",
            "source": self.source.as_uri(),
            "source_sha256": self.source_hash,
            "download_mb": 1,
            "expected_disk_mb": 2,
            "expected_memory_mb": 16,
            "license_notice": "Synthetic test artifact; no third-party payload.",
            "license_source": self.source.as_uri(),
            "network_destination": "NONE",
            "max_cost_usd": 0,
            "install_argv": [],
            "verify_argv": [],
            "environment_names": [],
            "idempotent_install": True,
            "install_network_access": "DENY",
        }
        value.update(updates)
        return value

    @staticmethod
    def approval(plan, *, at=AT):
        return {
            "schema_version": 1,
            "contract": preparation.APPROVAL_CONTRACT,
            "receipt_id": "approval-1",
            "provision_id": plan["provision_id"],
            "plan_hash": plan["plan_hash"],
            "authority": "approve:provision",
            "approved_at": preparation.isoformat(at - timedelta(minutes=1)),
            "expires_at": preparation.isoformat(at + timedelta(minutes=30)),
        }

    def test_doctor_finds_runtime_outside_path_and_isolates_missing_runtime(self) -> None:
        missing = self.definition("missing")
        missing["search_paths"] = [str(self.root / "missing")]
        report = preparation.doctor([self.definition(), missing], at=AT)
        self.assertEqual(report["status"], "PARTIAL")
        self.assertEqual(report["runtimes"][0]["state"], "HEALTHY")
        self.assertEqual(report["runtimes"][0]["discovery"], "SEARCH_PATH")
        self.assertEqual(report["runtimes"][1]["reason_code"], "EXECUTABLE_NOT_FOUND")

    def test_inventory_uses_exact_shell_free_command_and_isolates_failure(self) -> None:
        helper = self.root / "inventory.py"
        helper.write_text('print("{\\\"artifacts\\\":[{\\\"id\\\":\\\"model-a\\\"}]}")\n', encoding="utf-8")
        good = self.definition(inventory_argv=["{executable}", str(helper)], inventory_format="JSON")
        bad = self.definition("bad", inventory_argv=["{executable}", "--not-a-real-option"], inventory_format="JSON")
        doctor_report = preparation.doctor([good, bad], at=AT)
        report = preparation.inventory([good, bad], doctor_report, at=AT)
        self.assertEqual(report["status"], "PARTIAL")
        self.assertEqual(report["runtimes"][0]["artifacts"], [{"artifact_id": "model-a", "execution_boundary": "UNKNOWN", "boundary_reason": "MODEL_EXECUTION_NOT_ATTESTED"}])
        self.assertEqual(report["runtimes"][1]["state"], "UNAVAILABLE")
        malformed = dict(doctor_report)
        malformed["runtimes"] = [None, *doctor_report["runtimes"]]
        isolated = preparation.inventory([good, bad], malformed, at=AT)
        self.assertEqual(isolated["runtimes"][0]["reason_code"], "DOCTOR_RECORD_INVALID")
        with self.assertRaisesRegex(preparation.PreparationError, "refreshed"):
            preparation.inventory([good, bad], doctor_report, at=AT + timedelta(minutes=6))

    def test_doctor_and_inventory_redact_allowlisted_environment_values(self) -> None:
        name = "FOUNDATION_TEST_SECRET_VALUE"
        previous = os.environ.get(name)
        os.environ[name] = "not-a-real-secret-12345"

        def restore():
            if previous is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = previous

        self.addCleanup(restore)
        helper = self.root / "redaction.py"
        helper.write_text(
            'import json, os\nprint(json.dumps({"artifacts": [os.environ["FOUNDATION_TEST_SECRET_VALUE"]]}))\n',
            encoding="utf-8",
        )
        definition = self.definition(inventory_argv=["{executable}", str(helper)], inventory_format="JSON")
        definition["environment_allowlist"] = [name]
        doctor_report = preparation.doctor([definition], at=AT)
        report = preparation.inventory([definition], doctor_report, at=AT)
        self.assertEqual(report["runtimes"][0]["artifacts"], [{"artifact_id": "[REDACTED]", "execution_boundary": "UNKNOWN", "boundary_reason": "MODEL_EXECUTION_NOT_ATTESTED"}])
        self.assertNotIn(os.environ[name], json.dumps(report))

    def test_ollama_cloud_tags_are_never_reported_as_host_local(self) -> None:
        helper = self.root / "ollama_inventory.py"
        helper.write_text('print("NAME SIZE\\nmodel-a:cloud 1 GB\\nmodel-b 1 GB")\n', encoding="utf-8")
        definition = self.definition("ollama", inventory_argv=["{executable}", str(helper)], inventory_format="OLLAMA_TABLE")
        report = preparation.inventory([definition], preparation.doctor([definition], at=AT), at=AT)
        artifacts = {item["artifact_id"]: item for item in report["runtimes"][0]["artifacts"]}
        self.assertEqual(artifacts["model-a:cloud"]["execution_boundary"], "REMOTE")
        self.assertEqual(artifacts["model-a:cloud"]["boundary_reason"], "CLOUD_TAG_REQUIRES_REMOTE")
        self.assertEqual(artifacts["model-b"]["execution_boundary"], "UNKNOWN")

    def test_plan_enforces_hard_limits_network_and_offline_install_contract(self) -> None:
        plan = preparation.plan_provision(self.request(), [self.recipe()], at=AT)
        self.assertEqual(plan["contract"], preparation.WORK_CONTRACT)
        self.assertEqual(plan["actions"][0]["install_network_access"], "DENY")
        preparation.validate_plan(plan, at=AT)

        with self.assertRaisesRegex(preparation.PreparationError, "hard provision limit"):
            preparation.plan_provision(self.request(), [self.recipe(download_mb=2)], at=AT)
        with self.assertRaisesRegex(preparation.PreparationError, "network destination"):
            preparation.plan_provision(
                self.request(),
                [self.recipe(source="https://example.invalid/artifact", network_destination="example.invalid")],
                at=AT,
            )
        with self.assertRaisesRegex(preparation.PreparationError, "network access DENY"):
            preparation.plan_provision(self.request(), [self.recipe(install_network_access="ALLOW")], at=AT)

    def test_approval_is_bound_to_exact_plan_and_expiry(self) -> None:
        plan = preparation.plan_provision(self.request(), [self.recipe()], at=AT)
        preparation.validate_approval(self.approval(plan), plan, AT)
        changed = self.approval(plan)
        changed["plan_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(preparation.PreparationError, "exact plan"):
            preparation.validate_approval(changed, plan, AT)

    def test_file_provision_is_verified_and_resume_has_no_second_download(self) -> None:
        plan = preparation.plan_provision(self.request(), [self.recipe()], at=AT)
        report = preparation.provision(plan, self.approval(plan), store=self.state, at=AT)
        self.assertEqual(report["status"], "COMPLETED")
        self.assertEqual(self.target.read_bytes(), b"bounded artifact")
        self.source.unlink()
        resumed = preparation.provision(plan, self.approval(plan), store=self.state, at=AT)
        self.assertEqual(resumed["status"], "COMPLETED")
        self.assertEqual(resumed["reason_codes"], ["RESUMED_COMPLETED_REPORT"])
        self.assertEqual(preparation.verify(plan, store=self.state, at=AT + timedelta(days=2))["status"], "PASSED")

    def test_hash_failure_is_terminal_until_a_new_plan_is_approved(self) -> None:
        plan = preparation.plan_provision(self.request(), [self.recipe(source_sha256="sha256:" + "0" * 64)], at=AT)
        first = preparation.provision(plan, self.approval(plan), store=self.state, at=AT)
        self.assertEqual(first["status"], "FAILED")
        self.assertEqual(first["reason_codes"], ["PROVISION_HASH_MISMATCH"])
        second = preparation.provision(plan, self.approval(plan), store=self.state, at=AT)
        self.assertEqual(second["status"], "FAILED")
        self.assertEqual(second["reason_codes"], ["TERMINAL_CHECKPOINT_REQUIRES_NEW_PLAN"])
        self.assertFalse(self.target.exists())

    def test_ambiguous_non_idempotent_install_requires_manual_reconciliation(self) -> None:
        recipe = self.recipe(install_argv=[str(Path(sys.executable).resolve()), "{artifact_path}"], idempotent_install=False)
        plan = preparation.plan_provision(self.request(), [recipe], at=AT)
        operation_id = preparation.digest({"provision_id": plan["provision_id"], "recipe_id": recipe["recipe_id"]})
        self.state.save({
            "schema_version": 1,
            "contract": preparation.CONTRACT,
            "provision_id": plan["provision_id"],
            "plan_hash": plan["plan_hash"],
            "operation_id": operation_id,
            "status": "IN_PROGRESS",
            "downloaded_bytes": 0,
            "artifact_sha256": None,
            "reason_code": None,
            "updated_at": preparation.isoformat(AT),
        })
        report = preparation.provision(plan, self.approval(plan), store=self.state, at=AT)
        self.assertEqual(report["status"], "MANUAL_REQUIRED")
        self.assertIn("AMBIGUOUS_NON_IDEMPOTENT_INSTALL", report["reason_codes"])

    def test_runtime_state_and_targets_inside_repository_are_rejected(self) -> None:
        with self.assertRaisesRegex(preparation.PreparationError, "outside version control"):
            preparation.ProvisionStore(ROOT / ".runtime")
        request = self.request(target_path=str(ROOT / "provisioned.bin"))
        with self.assertRaisesRegex(preparation.PreparationError, "outside version control"):
            preparation.plan_provision(request, [self.recipe()], at=AT)

    def cost_source(self, source_path: Path, **updates):
        value = {
            "source_id": "price-1",
            "url": source_path.as_uri(),
            "json_path": ["price"],
            "subject": {"kind": "PROVIDER_PRICE", "subject_id": "service-a"},
            "currency": "USD",
            "unit": "per_request",
            "provenance": "RESEARCH_VERIFIED",
            "valid_for_seconds": 172800,
            "refresh_seconds": 86400,
            "normalized_attempt_cost": None,
        }
        value.update(updates)
        return value

    def test_cost_evidence_refreshes_at_most_daily_and_reuses_fresh_evidence(self) -> None:
        source = self.root / "price.json"
        source.write_text('{"price": 1.25}\n', encoding="utf-8")
        calls = []

        def fetch(url):
            calls.append(url)
            return source.read_bytes()

        definition = [self.cost_source(source)]
        first = preparation.refresh_cost_evidence(definition, state_root=self.root / "cost", network_authorized=False, at=AT, fetch=fetch)
        second = preparation.refresh_cost_evidence(definition, state_root=self.root / "cost", network_authorized=False, at=AT + timedelta(hours=23), fetch=fetch)
        self.assertEqual(first["status"], "COMPLETE")
        self.assertEqual(second["records"][0]["status"], "CACHED")
        self.assertEqual(len(calls), 1)
        self.assertEqual(first["records"][0]["evidence"]["amount"], 1.25)

    def test_failed_cost_research_is_also_rate_limited(self) -> None:
        missing = self.root / "missing.json"
        calls = []

        def fail(url):
            calls.append(url)
            raise OSError("synthetic failure")

        definition = [self.cost_source(missing)]
        first = preparation.refresh_cost_evidence(definition, state_root=self.root / "cost", network_authorized=False, at=AT, fetch=fail)
        second = preparation.refresh_cost_evidence(definition, state_root=self.root / "cost", network_authorized=False, at=AT + timedelta(hours=1), fetch=fail)
        self.assertEqual(first["status"], "UNAVAILABLE")
        self.assertEqual(second["records"][0]["status"], "DEFERRED")
        self.assertEqual(len(calls), 1)

    def test_remote_cost_evidence_remains_available_offline_until_expiry(self) -> None:
        source = self.cost_source(self.source, url="https://prices.example.invalid/current.json")
        calls = []

        def fetch(url):
            calls.append(url)
            return b'{"price": 0.5}'

        online = preparation.refresh_cost_evidence([source], state_root=self.root / "cost", network_authorized=True, at=AT, fetch=fetch)
        offline = preparation.refresh_cost_evidence([source], state_root=self.root / "cost", network_authorized=False, at=AT + timedelta(hours=12), fetch=lambda _url: self.fail("offline refresh attempted"))
        self.assertEqual(online["records"][0]["status"], "REFRESHED")
        self.assertEqual(offline["records"][0]["status"], "CACHED")
        self.assertEqual(offline["records"][0]["reason_code"], "NETWORK_NOT_AUTHORIZED")
        self.assertEqual(len(calls), 1)

    def test_cost_refresh_below_daily_limit_is_rejected(self) -> None:
        with self.assertRaisesRegex(preparation.PreparationError, "at least 24 hours"):
            preparation.validate_cost_sources([self.cost_source(self.source, refresh_seconds=86399)])

    def test_public_schemas_are_strict_and_contain_no_product_or_price_defaults(self) -> None:
        names = [
            "runtime-inventory.schema.json",
            "provision-request.schema.json",
            "provision-approval.schema.json",
            "provision-report.schema.json",
        ]
        for name in names:
            schema = json.loads((ROOT / "foundation" / "schemas" / name).read_text(encoding="utf-8"))
            self.assertFalse(schema["additionalProperties"])
            serialized = json.dumps(schema).lower()
            self.assertNotIn("ollama", serialized)
            self.assertNotIn("lm studio", serialized)
            self.assertNotIn("qwen", serialized)
        plan = preparation.plan_provision(self.request(), [self.recipe()], at=AT)
        plan_schema = json.loads((ROOT / "foundation" / "schemas" / "provision-plan.schema.json").read_text(encoding="utf-8"))
        self.assertTrue(set(plan_schema["required"]) <= set(plan))
        action_schema = plan_schema["properties"]["actions"]["items"]
        self.assertTrue(set(action_schema["required"]) <= set(plan["actions"][0]))
        self.assertTrue(set(plan["actions"][0]) <= set(action_schema["properties"]))


if __name__ == "__main__":
    unittest.main()
