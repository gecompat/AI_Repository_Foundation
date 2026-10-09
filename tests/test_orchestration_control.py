"""Offline host fixtures: decisions never call a model or execute client effects."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from pathlib import Path
from unittest.mock import patch

try:
    from .test_ai_orchestrator import AT, ROOT, CAPABILITY, FakeRuntime, ai_orchestrator, evidence, profile, request, router_v2, orchestrator_mcp
except ImportError:
    from test_ai_orchestrator import AT, ROOT, CAPABILITY, FakeRuntime, ai_orchestrator, evidence, profile, request, router_v2, orchestrator_mcp
import orchestration_control as controller


class HostRuntime(FakeRuntime):
    @staticmethod
    def execute_adapter(connection, operation, arguments):
        result = FakeRuntime.execute_adapter(connection, operation, arguments)
        for fragment in result.get("fragments", []):
            fragment["provider"] = "CedarCompute" if connection["connection_id"] == "one" else "QuartzCompute"
        return result


class ControlTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.state = self.root / "state"
        self.path = self.root / "control.json"
        self.snapshot_path = self.root / "observation.json"
        self.cfg = {"schema_version": 1, "contract": controller.CONTRACT, "job_id": "job-1",
                    "work_ref": "WI-test", "authorization_ref": "auth-test", "completion_ref": "accept-test",
                    "budget_ref": "budget-test", "bootstrap_ref": "current-rules", "autonomy": True,
                    "state_root": str(self.state),
                    "max_dispatches": 5, "start_request": request(self.root), "research_ref": "research-authorized",
                    "client": {"client_id": "HarborConsole", "source_ref": "host-capabilities",
                               "valid_until": (max(AT, ai_orchestrator.utc_now()) + timedelta(days=2)).isoformat(), "capabilities": sorted(controller.CAPABILITIES),
                               "observation_path": str(self.snapshot_path)}}
        self.snapshot = {"schema_version": 1, "contract": controller.CONTRACT, "job_id": "job-1",
                         "client_id": "HarborConsole", "observed_at": "2026-09-08T11:00:00Z",
                         "valid_until": self.cfg["client"]["valid_until"], "generation": 0, "owner_session_id": "old-chat",
                         "execution": "RUNNING", "work_remaining": True, "executable": True,
                         "checkpoint_ref": "checkpoint-1", "completion_verified": False,
                         "models": [{"connection_id": "one", "model_id": "alpha"}, {"connection_id": "two", "model_id": "beta"}]}
        self.evidence = evidence(self.root)
        FakeRuntime.connections = ["one", "two"]
        FakeRuntime.calls = FakeRuntime.catalog_calls = 0
        FakeRuntime.failures, FakeRuntime.actual_models, FakeRuntime.failure_classes = set(), {}, {}
        self.save()

    def tearDown(self):
        self.temp.cleanup()

    def save(self):
        self.path.write_text(json.dumps(self.cfg), encoding="utf-8")
        self.snapshot_path.write_text(json.dumps(self.snapshot), encoding="utf-8")

    def call(self, event="EVENT", at=AT, **kwargs):
        self.save()
        raw = {"schema_version": 1, "contract": controller.CONTRACT, "job_id": self.cfg["job_id"], "event": event}
        with patch.object(ai_orchestrator, "_dependencies", return_value=(router_v2, HostRuntime)):
            result = controller.control(raw, control_config=self.path, state_root=self.state,
                                        evidence_path=self.evidence, at=at, **kwargs)
        self.assertEqual(result["model_calls"], 0)
        self.assertEqual(FakeRuntime.calls, 0)
        return result

    def idle(self):
        self.call("REGISTER")
        self.snapshot["execution"] = "IDLE"

    def only(self, result, kind):
        actions = [a for a in result["actions"] if a["kind"] == kind]
        self.assertEqual(len(actions), 1, result)
        return actions[0]

    def ack(self, action, outcome="SUCCEEDED", **fields):
        self.snapshot["ack"] = {"action_id": action["action_id"], "outcome": outcome, **fields}

    def start_ack(self, action, session="new-chat"):
        self.snapshot.update(generation=action["next_generation"], owner_session_id=session, execution="RUNNING")
        self.ack(action, session_id=session, receipt={"requested_model": action["route"]["model"],
                 "actual_model": action["route"]["model"], "issuer": self.cfg["client"]["client_id"], "evidence_kind": "HOST_EXECUTION"})

    def lifecycle(self, boundary="USER_REQUESTED"):
        value = json.loads((ROOT / "foundation/capabilities/ai-work/session-lifecycle.example.json").read_text(encoding="utf-8"))
        value.update(session_id="old-chat", boundary=boundary, successor_session_capability="AUTOMATIC")
        self.snapshot["lifecycle_request"] = value

    def handoff_ack(self, action):
        self.snapshot.update(execution="IDLE", checkpoint_ref="checkpoint-handoff")
        self.snapshot["handoff"] = {"schema_version": 1, "contract": "foundation-session-handoff/v1",
            "handoff_id": "handoff-1", "predecessor_session_id": "old-chat", "successor_role": "ORCHESTRATOR",
            "checkpoint_id": "checkpoint-handoff", "created_at": "2026-09-08T12:00:00Z",
            "durable_state_refs": [self.cfg[k] for k in ("authorization_ref", "completion_ref", "budget_ref", "bootstrap_ref")],
            "current_work_refs": ["WI-test"], "changed_state_refs": ["status"], "unresolved_refs": ["blockade-test"], "delta_handle": None}
        self.ack(action, checkpoint_ref="checkpoint-handoff", handoff_ref="handoff-1", predecessor_retired=True)

    def test_two_independent_client_provider_start_profiles_and_worker_routing(self):
        source = json.loads(self.evidence.read_text(encoding="utf-8"))["records"][0]
        other = {**copy.deepcopy(source), "connection_id": "two", "model_id": "beta", "profile": profile(1)}
        self.evidence.write_text(json.dumps({**json.loads(self.evidence.read_text(encoding="utf-8")), "records": [source, other]}), encoding="utf-8")
        for i, (client, connection, model, provider) in enumerate([
                ("HarborConsole", "one", "alpha", "CedarCompute"), ("MapleWorkbench", "two", "beta", "QuartzCompute")]):
            with self.subTest(client=client):
                self.cfg["job_id"] = self.snapshot["job_id"] = f"start-{i}"
                self.cfg["client"]["client_id"] = self.snapshot["client_id"] = client
                self.cfg["start_request"]["router_request"].pop("tier", None)
                self.snapshot.update(owner_session_id=None, generation=0, execution="IDLE",
                                     models=[{"connection_id": connection, "model_id": model}])
                self.snapshot.pop("ack", None)
                action = self.only(self.call("REGISTER"), "START_SESSION")
                self.assertEqual(action["route"]["model"], model)
                self.assertIn(provider, action["route"]["provider"])
                self.start_ack(action, f"new-{i}")
                self.assertEqual(self.call()["generation"], 1)
        # Worker routing retains the existing economical tier and full evidence contract.
        work = request(self.root)
        work["router_request"]["tier"] = "ECONOMICAL"
        with patch.object(ai_orchestrator, "_dependencies", return_value=(router_v2, HostRuntime)):
            result = ai_orchestrator.plan_or_execute(work, execute=False, state_root=self.state, evidence_path=self.evidence, at=AT)
        self.assertEqual(result["status"], "PLANNED")
        self.assertEqual(result["route"]["model"], "alpha")

    def test_unchanged_running_and_waiting_cost_zero_calls_and_notifications(self):
        self.call("REGISTER")
        for status in ("RUNNING", "WAITING"):
            self.snapshot["execution"] = status
            result = self.call("HEARTBEAT", at=AT + timedelta(hours=1))
            self.assertEqual(result["actions"], [])
        self.assertEqual(FakeRuntime.catalog_calls, 0)

    def test_two_hosts_complete_heartbeat_handoff_and_notification_flow(self):
        candidate = json.loads(self.evidence.read_text(encoding="utf-8"))
        candidate["records"].append({**copy.deepcopy(candidate["records"][0]), "connection_id": "two", "model_id": "beta", "profile": profile(1)})
        self.evidence.write_text(json.dumps(candidate), encoding="utf-8")
        for i, (client, connection, model) in enumerate((("HarborConsole", "one", "alpha"), ("MapleWorkbench", "two", "beta"))):
            self.cfg["job_id"] = self.snapshot["job_id"] = f"flow-{i}"
            self.cfg["client"]["client_id"] = self.snapshot["client_id"] = client
            self.snapshot.update(owner_session_id="old-chat", generation=0, execution="RUNNING", work_remaining=True, executable=True,
                                 completion_verified=False, checkpoint_ref="checkpoint-1", models=[{"connection_id": connection, "model_id": model}])
            for name in ("ack", "lifecycle_request", "handoff"):
                self.snapshot.pop(name, None)
            self.idle()
            resume = self.only(self.call("HEARTBEAT"), "RESUME_SESSION")
            self.ack(resume)
            self.lifecycle()
            prepare = self.only(self.call("ROTATE"), "PREPARE_HANDOFF")
            self.handoff_ack(prepare)
            start = self.only(self.call(), "START_SESSION")
            self.assertEqual(start["route"]["model"], model)
            self.start_ack(start)
            self.call()
            self.snapshot.pop("ack")
            self.snapshot.update(execution="IDLE", work_remaining=False, executable=False, completion_verified=True)
            completed = self.call()
            self.assertEqual(completed["state"], "COMPLETED")
            self.only(completed, "NOTIFY")
            self.assertEqual(self.call("HEARTBEAT")["actions"], [])

    def test_duplicate_ticks_restart_and_same_checkpoint_only_resume_once(self):
        self.idle()
        first = self.only(self.call("HEARTBEAT"), "RESUME_SESSION")
        self.assertEqual(first["message"], "HEARTBEAT")
        self.assertEqual(self.call("HEARTBEAT")["actions"], [])
        self.assertEqual(self.call("EVENT")["actions"], [])  # another process loads the same file
        self.ack(first)
        self.assertEqual(self.call("HEARTBEAT", at=AT + timedelta(minutes=30))["actions"], [])
        self.snapshot.pop("ack")
        self.snapshot["checkpoint_ref"] = "checkpoint-2"
        self.snapshot["progress"] = {"previous_checkpoint_ref": "checkpoint-1", "checkpoint_ref": "checkpoint-2", "progress_ref": "verified-change-2"}
        second = self.only(self.call("HEARTBEAT", at=AT + timedelta(minutes=60)), "RESUME_SESSION")
        self.assertNotEqual(first["action_id"], second["action_id"])

    def test_concurrent_processes_reserve_one_effect(self):
        self.idle()
        self.save()
        event = self.root / "event.json"
        event.write_text(json.dumps({"schema_version": 1, "contract": controller.CONTRACT, "job_id": "job-1", "event": "HEARTBEAT"}), encoding="utf-8")
        command = [sys.executable, str(CAPABILITY / "ai_orchestrator.py"), "--control-config", str(self.path), "--state-root", str(self.state), "control", str(event)]
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(lambda _: subprocess.run(command, capture_output=True, text=True, check=True), range(4)))
        reports = [json.loads(r.stdout) for r in results]
        self.assertEqual(sum(a["kind"] == "RESUME_SESSION" for r in reports for a in r["actions"]), 1)
        self.assertEqual(len({p for r in reports for p in r["pending_action_ids"]}), 1)

    def test_new_checkpoint_without_verified_progress_does_not_resume(self):
        self.idle()
        action = self.only(self.call(), "RESUME_SESSION")
        self.ack(action)
        self.snapshot["checkpoint_ref"] = "mechanical-checkpoint"
        result = self.call()
        self.assertEqual(result["reason_code"], "PROGRESS_EVIDENCE_REQUIRED")
        self.assertFalse(any(a["kind"] == "RESUME_SESSION" for a in result["actions"]))

    def test_autonomy_disabled_by_default_and_pre_model_check_required(self):
        self.cfg.pop("autonomy")
        self.idle()
        self.assertEqual(self.call("HEARTBEAT")["actions"], [])
        self.assertEqual(self.call()["actions"], [])
        self.cfg["job_id"] = self.snapshot["job_id"] = "other"
        self.cfg["autonomy"] = True
        self.cfg["client"]["capabilities"].remove("PRE_MODEL_CHECK")
        self.snapshot["execution"] = "RUNNING"
        self.call("REGISTER")
        self.snapshot["execution"] = "IDLE"
        self.assertEqual(self.call("HEARTBEAT")["reason_code"], "PERIODIC_WAKE_DISABLED")

    def test_finite_bound_mandatory_and_shared_across_jobs(self):
        self.cfg.pop("max_dispatches")
        with self.assertRaises(ai_orchestrator.OrchestrationError):
            self.call("REGISTER")
        self.cfg["max_dispatches"] = 1
        self.idle()
        self.only(self.call(), "RESUME_SESSION")
        self.cfg["job_id"] = self.snapshot["job_id"] = "second-job"
        result = self.call("REGISTER")
        self.assertEqual(result["reason_code"], "DISPATCH_BOUND_REACHED")
        self.assertEqual(result["controller_dispatches"], 1)

    def test_missing_budget_cannot_activate_autonomy_without_a_finite_bound(self):
        self.cfg.pop("max_dispatches")
        self.cfg["budget_request_path"] = str(self.root / "missing-budget.json")
        result = self.call("REGISTER")
        self.assertEqual(result["state"], "NEEDS_INPUT")
        self.assertEqual(result["controller_dispatches"], 0)

    def test_pause_cancel_and_completion_disable_automatic_continuation(self):
        for event, expected in (("PAUSE", "PAUSED"), ("CANCEL", "CANCELLED"), ("EVENT", "COMPLETED")):
            self.cfg["job_id"] = self.snapshot["job_id"] = event
            self.snapshot.update(execution="RUNNING", work_remaining=True, completion_verified=False)
            self.call("REGISTER")
            self.snapshot.update(execution="IDLE", work_remaining=False, completion_verified=True)
            result = self.call(event)
            self.assertEqual(result["state"], expected)
            if expected == "COMPLETED":
                self.only(result, "NOTIFY")
            self.assertEqual(self.call("HEARTBEAT", at=AT + timedelta(hours=1))["actions"], [])

    def test_unknown_execution_timeout_and_failed_actions_never_replay(self):
        for outcome in ("UNKNOWN", "FAILED"):
            self.cfg["job_id"] = self.snapshot["job_id"] = outcome
            self.snapshot.update(execution="RUNNING", checkpoint_ref="checkpoint-1")
            self.snapshot.pop("ack", None)
            self.idle()
            action = self.only(self.call(), "RESUME_SESSION")
            self.ack(action, outcome)
            result = self.call()
            self.assertEqual(result["state"], "NEEDS_INPUT")
            self.assertIn(action["action_id"], result["pending_action_ids"])
            self.assertEqual(self.call("HEARTBEAT", at=AT + timedelta(hours=1))["actions"], [])
        self.snapshot.pop("ack")
        self.cfg["job_id"] = self.snapshot["job_id"] = "unknown"
        self.snapshot["execution"] = "UNKNOWN"
        self.assertEqual(self.call("REGISTER")["reason_code"], "EXECUTION_UNKNOWN")

    def test_missing_acknowledgement_expires_without_replay(self):
        self.idle()
        action = self.only(self.call(), "RESUME_SESSION")
        result = self.call(at=AT + timedelta(minutes=5))
        self.assertEqual(result["reason_code"], "ACTION_ACK_TIMEOUT")
        self.assertIn(action["action_id"], result["pending_action_ids"])
        self.assertFalse(any(a["kind"] == "RESUME_SESSION" for a in result["actions"]))

    def test_start_does_not_run_configured_evidence_collectors(self):
        self.snapshot.update(owner_session_id=None, execution="IDLE")
        with patch.object(ai_orchestrator, "refresh_evidence", side_effect=AssertionError("model-capable collector must not run")):
            self.only(self.call("REGISTER", evidence_sources_path=self.root / "sources.json"), "START_SESSION")

    def test_explicit_reconciliation_preserves_checkpoint_dedup(self):
        self.idle()
        action = self.only(self.call(), "RESUME_SESSION")
        self.ack(action, "UNKNOWN")
        self.call()
        self.ack(action, "NOT_STARTED")
        self.snapshot["operator_resume"] = True
        result = self.call("RESUME")
        self.assertEqual(result["reason_code"], "UNCHANGED_CHECKPOINT")
        self.assertFalse(any(a["kind"] == "RESUME_SESSION" for a in result["actions"]))

    def test_missing_capability_or_start_evidence_is_manual(self):
        self.cfg["client"]["capabilities"].remove("RESUME_SESSION")
        self.idle()
        self.assertEqual(self.call()["reason_code"], "MANUAL_CONTINUATION_REQUIRED")
        self.cfg["job_id"] = self.snapshot["job_id"] = "no-start"
        self.snapshot.update(owner_session_id=None, generation=0, execution="IDLE", models=[])
        self.assertEqual(self.call("REGISTER")["reason_code"], "START_MODEL_SELECTION_REQUIRED")

    def test_unattested_model_does_not_adopt_successor(self):
        self.snapshot.update(owner_session_id=None, execution="IDLE")
        action = self.only(self.call("REGISTER"), "START_SESSION")
        self.start_ack(action)
        self.snapshot["ack"]["receipt"]["actual_model"] = "invented"
        result = self.call()
        self.assertEqual(result["reason_code"], "ACTUAL_MODEL_NOT_ATTESTED")
        self.assertIsNone(result["owner_session_id"])
        self.assertEqual(result["generation"], 0)

    def test_handoff_fences_predecessor_preserves_scope_and_confirms_start(self):
        self.idle()
        self.lifecycle()
        prepare = self.only(self.call("ROTATE"), "PREPARE_HANDOFF")
        self.assertEqual(FakeRuntime.catalog_calls, 0)
        self.handoff_ack(prepare)
        start = self.only(self.call(), "START_SESSION")
        self.assertTrue(start["successor"])
        self.assertEqual(start["handoff_ref"], "handoff-1")
        self.start_ack(start)
        accepted = self.call()
        self.assertEqual(accepted["owner_session_id"], "new-chat")
        self.snapshot.pop("ack")
        self.snapshot.update(generation=0, owner_session_id="old-chat", execution="IDLE")
        rejected = self.call()
        self.assertEqual(rejected["status"], "REJECTED")
        self.assertEqual(rejected["state"], "RUNNING")
        self.assertEqual(rejected["actions"], [])

    def test_handoff_without_confirmed_quiescence_or_preserved_rules_is_rejected(self):
        self.idle()
        self.lifecycle()
        prepare = self.only(self.call("ROTATE"), "PREPARE_HANDOFF")
        self.handoff_ack(prepare)
        self.snapshot["execution"] = "RUNNING"
        self.assertEqual(self.call()["reason_code"], "PREDECESSOR_NOT_QUIESCENT")

    def test_idle_without_retirement_is_insufficient_for_successor(self):
        self.idle()
        self.lifecycle()
        prepare = self.only(self.call("ROTATE"), "PREPARE_HANDOFF")
        self.handoff_ack(prepare)
        self.snapshot["ack"].pop("predecessor_retired")
        result = self.call()
        self.assertEqual(result["reason_code"], "PREDECESSOR_NOT_QUIESCENT")
        self.assertFalse(any(a["kind"] == "START_SESSION" for a in result["actions"]))

    def test_failed_successor_keeps_predecessor_retired_and_does_not_resume_it(self):
        self.idle()
        self.lifecycle()
        prepare = self.only(self.call("ROTATE"), "PREPARE_HANDOFF")
        self.handoff_ack(prepare)
        start = self.only(self.call(), "START_SESSION")
        self.ack(start, "FAILED")
        result = self.call()
        self.assertEqual(result["state"], "NEEDS_INPUT")
        self.assertFalse(any(a["kind"] == "RESUME_SESSION" for a in result["actions"]))
        self.assertEqual(self.call("HEARTBEAT", at=AT + timedelta(hours=1))["actions"], [])

    def test_missing_metrics_do_not_rotate_and_checkpoint_trigger_is_not_repeated(self):
        self.idle()
        self.lifecycle("NONE")
        self.snapshot["lifecycle_request"]["metrics"] = dict.fromkeys(self.snapshot["lifecycle_request"]["metrics"], None)
        result = self.call()
        action = self.only(result, "RESUME_SESSION")
        self.ack(action)
        self.call()
        self.snapshot.pop("ack")
        self.snapshot["lifecycle_request"]["metrics"]["tokens_since_checkpoint"] = 30000
        checkpoint = self.only(self.call(), "CHECKPOINT")
        self.ack(checkpoint)
        self.assertEqual(self.call()["actions"], [])

    def test_budget_unknown_cost_after_ack_blocks_further_dispatch(self):
        budget = self.root / "budget.json"
        budget.write_text(json.dumps({"schema_version": 1, "contract": "foundation-processing-budget/v1",
            "wave_id": "budget-test", "unit": "CREDITS", "soft_limit": None, "hard_limit": 10,
            "next_reservation": 2, "entries": []}), encoding="utf-8")
        self.cfg["budget_request_path"] = str(budget)
        self.idle()
        action = self.only(self.call(), "RESUME_SESSION")
        self.ack(action)
        self.snapshot["checkpoint_ref"] = "checkpoint-2"
        self.snapshot["progress"] = {"previous_checkpoint_ref": "checkpoint-1", "checkpoint_ref": "checkpoint-2", "progress_ref": "verified-change-2"}
        self.assertEqual(self.call()["reason_code"], "BUDGET_UNVERIFIED")

    def test_notification_dedup_and_external_authority(self):
        self.cfg.update(notification_target="mail-channel", external_notifications_authorized=False)
        self.snapshot["execution"] = "UNKNOWN"
        self.assertEqual(self.call("REGISTER")["actions"], [])
        self.cfg["job_id"] = self.snapshot["job_id"] = "authorized-channel"
        self.cfg["external_notifications_authorized"] = True
        action = self.only(self.call("REGISTER"), "NOTIFY")
        self.assertEqual(action["target_ref"], "mail-channel")
        self.assertLess(len(action["message"]), 160)
        self.assertEqual(self.call()["actions"], [])

    def test_one_bounded_research_per_source_failure(self):
        self.idle()
        self.snapshot["source_failure"] = {"source_id": "price-source", "failure_ref": "failure-1"}
        research = self.only(self.call("SOURCE_FAILED"), "RESEARCH")
        self.assertEqual(research["request_ref"], "research-authorized")
        self.ack(research)
        self.assertEqual(self.call("SOURCE_FAILED")["actions"], [])
        self.snapshot.pop("ack")
        self.snapshot["checkpoint_ref"] = "new-progress"
        self.assertEqual(self.call("SOURCE_FAILED")["actions"], [])

    def verification(self, candidate):
        self.snapshot["verification"] = {"candidate_path": str(self.evidence), "candidate_sha256": controller.digest(candidate),
            "verifier_ref": "independent-person", "producer_ref": "research-agent", "source_ref": "checked-source",
            "units_ref": "USD-per-million", "model_mapping_ref": "checked-mapping", "verified": True}

    def test_verified_evidence_preserves_unrelated_cache_entries(self):
        self.idle()
        candidate = json.loads(self.evidence.read_text(encoding="utf-8"))
        other = copy.deepcopy(candidate)
        other["records"][0].update(connection_id="two", model_id="beta")
        self.state.mkdir(exist_ok=True)
        (self.state / "model-runtime-evidence.json").write_text(json.dumps(other), encoding="utf-8")
        self.verification(candidate)
        self.assertEqual(self.call("ACCEPT_EVIDENCE")["reason_code"], "VERIFIED_EVIDENCE_ACCEPTED")
        merged = json.loads((self.state / "model-runtime-evidence.json").read_text(encoding="utf-8"))
        self.assertEqual({r["model_id"] for r in merged["records"]}, {"alpha", "beta"})

    def test_unverified_changed_expired_or_conflicting_prices_are_not_adopted(self):
        for case in ("self", "unit", "conflict", "changed", "expired"):
            with self.subTest(case=case):
                self.cfg["job_id"] = self.snapshot["job_id"] = case
                self.snapshot["execution"] = "RUNNING"
                self.snapshot.pop("verification", None)
                self.call("REGISTER")
                self.snapshot["execution"] = "IDLE"
                candidate = json.loads(evidence(self.root).read_text(encoding="utf-8"))
                if case == "unit":
                    candidate["records"][0]["profile"]["pricing"]["unit_tokens"] = 1000
                elif case == "conflict":
                    other = copy.deepcopy(candidate["records"][0])
                    other["profile"]["pricing"]["base"]["input"] = 5
                    candidate["records"].append(other)
                elif case == "expired":
                    candidate["records"][0]["valid_until"] = "2026-09-08T11:30:00Z"
                self.evidence.write_text(json.dumps(candidate), encoding="utf-8")
                self.verification(candidate)
                if case == "self":
                    self.snapshot["verification"]["verifier_ref"] = "research-agent"
                elif case == "changed":
                    self.snapshot["verification"]["candidate_sha256"] = "sha256:" + "f" * 64
                result = self.call("ACCEPT_EVIDENCE")
                self.assertEqual(result["state"], "NEEDS_INPUT")
                self.assertFalse((self.state / "model-runtime-evidence.json").exists())

    def test_payload_and_forged_receipts_rejected_by_closed_request(self):
        for extra in ("prompt", "observation", "ack", "capabilities"):
            raw = {"schema_version": 1, "contract": controller.CONTRACT, "job_id": "job-1", "event": "REGISTER", extra: "fake"}
            with self.assertRaises(ai_orchestrator.OrchestrationError):
                controller.control(raw, control_config=self.path, state_root=self.state, at=AT)
        for raw in ('{"x":1,"x":2}', '{"x":NaN}'):
            self.path.write_text(raw, encoding="utf-8")
            with self.assertRaises(ai_orchestrator.OrchestrationError):
                controller.read(self.path)

    def test_state_corruption_and_git_resident_config_fail_closed(self):
        self.call("REGISTER")
        state_path = self.state / "control/state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["jobs"]["job-1"]["generation"] = 100
        state_path.write_text(json.dumps(state), encoding="utf-8")
        with self.assertRaises(ai_orchestrator.OrchestrationError):
            self.call()
        with self.assertRaises(ai_orchestrator.OrchestrationError):
            controller.external_file(str(ROOT / "control.json"))

    def test_configured_state_authority_cannot_be_reset_by_another_root(self):
        self.idle()
        raw = {"schema_version": 1, "contract": controller.CONTRACT, "job_id": "job-1", "event": "HEARTBEAT"}
        with self.assertRaises(ai_orchestrator.OrchestrationError) as caught:
            controller.control(raw, control_config=self.path, state_root=self.root / "reset", at=AT)
        self.assertEqual(caught.exception.code, "CONTROL_STATE_ROOT_MISMATCH")

    def test_cli_mcp_and_status_probe_share_the_contract(self):
        self.cfg["autonomy"] = False
        self.call("REGISTER")
        action = self.only(self.call("STATUS"), "CHECK_STATUS")
        self.assertEqual(self.call("STATUS")["actions"], [])
        self.ack(action)
        self.call()
        raw = {"schema_version": 1, "contract": controller.CONTRACT, "job_id": "job-1", "event": "STATUS"}
        server = orchestrator_mcp.Server(config=None, state_root=self.state, evidence=None, evidence_sources=None, control_config=self.path)
        report = server.call("orchestration_control", {"request": raw})["structuredContent"]
        self.assertEqual(report["contract"], controller.CONTRACT)
        self.assertEqual(report["model_calls"], 0)
        event = self.root / "event.json"
        event.write_text(json.dumps(raw), encoding="utf-8")
        run = subprocess.run([sys.executable, str(CAPABILITY / "ai_orchestrator.py"), "--control-config", str(self.path),
                              "--state-root", str(self.state), "control", str(event)], capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(run.stdout)["pending_action_ids"], report["pending_action_ids"])

    def test_public_schema_is_closed_and_has_no_payload_or_host_claims_in_request(self):
        schema = json.loads((ROOT / "foundation/schemas/orchestrator-control.schema.json").read_text(encoding="utf-8"))
        defs = schema["$defs"]
        self.assertEqual(set(defs["request"]["properties"]), {"schema_version", "contract", "job_id", "event"})
        for name in ("request", "configuration", "observation", "verification", "client", "ack", "receipt"):
            self.assertFalse(defs[name]["additionalProperties"])
        self.assertEqual(defs["configuration"]["properties"]["heartbeat_seconds"]["default"], 1800)
        report = self.call("REGISTER")
        self.assertEqual(set(report), set(defs["report"]["oneOf"][0]["required"]))
        self.snapshot["execution"] = "IDLE"
        action = self.only(self.call(), "RESUME_SESSION")
        variant = next(v for v in defs["action"]["oneOf"] if v["properties"]["kind"]["const"] == action["kind"])
        self.assertEqual(set(action), set(variant["required"]))
        self.assertNotIn("prompt", json.dumps(schema))

    def test_installed_capability_and_core_helpers_run_offline_example(self):
        target = self.root / "target"
        target.mkdir()
        installed = subprocess.run([sys.executable, str(ROOT / "tools/install_foundation.py"), str(target),
                                    "--adapters", "none", "--capabilities", "ai-orchestrator", "--apply"],
                                   capture_output=True, text=True)
        self.assertEqual(installed.returncode, 0, installed.stderr + installed.stdout[-1500:])
        self.assertTrue((target / ".ai/foundation/runtime/state_io.py").is_file())
        self.assertTrue((target / ".ai/foundation/schemas/orchestrator-control.schema.json").is_file())
        example = subprocess.run([sys.executable, str(target / ".ai/foundation/ai_orchestrator/control.example.py")],
                                 capture_output=True, text=True, check=True)
        records = [json.loads(line) for line in example.stdout.splitlines()]
        self.assertEqual(len(records), 5)
        self.assertEqual([r["actions"] for r in records], [[], ["RESUME_SESSION"], [], ["NOTIFY"], []])
        self.assertTrue(all(r["model_calls"] == 0 for r in records))


if __name__ == "__main__":
    unittest.main()
