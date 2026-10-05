"""Boundary, degradation, and invalid-input contracts for session planning."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

try:
    from .test_ai_work import ai_work, MODULE_PATH, ROOT
except ImportError:  # unittest discovery with tests as the start directory
    from test_ai_work import ai_work, MODULE_PATH, ROOT


def request():
    return json.loads((MODULE_PATH.parent / "session-lifecycle.example.json").read_text(encoding="utf-8"))


class SessionLifecycleTests(unittest.TestCase):
    def test_exact_thresholds_and_precedence(self):
        for tokens, boundary, delta, expected in [
            (64999, "NONE", 0, "CONTINUE"),
            (65000, "NONE", 0, "CHECKPOINT"),
            (65000, "WORK_ITEM_COMPLETED", 0, "ROTATE_AT_BOUNDARY"),
            (65000, "MILESTONE_COMPLETED", 0, "ROTATE_AT_BOUNDARY"),
            (65000, "MAJOR_TOPIC_CHANGE", 0, "ROTATE_AT_BOUNDARY"),
            (80000, "WORK_ITEM_COMPLETED", 0, "ROTATE_REQUIRED"),
            (120000, "NONE", 0, "ROTATE_REQUIRED"),
            (0, "USER_REQUESTED", 0, "ROTATE_REQUIRED"),
            (0, "NONE", 30000, "CHECKPOINT"),
            (0, "WORK_ITEM_COMPLETED", 30000, "CHECKPOINT"),
        ]:
            with self.subTest(tokens=tokens, boundary=boundary, delta=delta):
                value = request()
                value["metrics"].update(estimated_context_tokens=tokens, tokens_since_checkpoint=delta)
                value["boundary"] = boundary
                result = ai_work.session_lifecycle(value)
                self.assertEqual(result["action"], expected)
                self.assertFalse(result["semantic_scan_required"])
                if expected == "CHECKPOINT":
                    self.assertEqual(result["successor_session"], {"required": False, "mode": "NONE", "role": None})

    def test_partial_unknown_metrics_and_all_roles(self):
        for role in sorted(ai_work.SESSION_ROLES):
            for missing in ("estimated_context_tokens", "context_window_tokens", "tokens_since_checkpoint"):
                with self.subTest(role=role, missing=missing):
                    value = request()
                    value["role"] = role
                    value["metrics"] = dict.fromkeys(value["metrics"], None)
                    value["metrics"]["tokens_since_checkpoint"] = 0
                    value["metrics"][missing] = None
                    original = copy.deepcopy(value)
                    result = ai_work.session_lifecycle(value)
                    self.assertEqual(result["action"], "CONTINUE")
                    self.assertIsNone(result["context_ratio"])
                    self.assertEqual(value, original)

    def test_successor_modes_are_requests_and_preserve_roles(self):
        for capability, expected in (("AUTOMATIC", "AUTOMATIC"), ("MANUAL", "MANUAL"), ("UNKNOWN", "MANUAL")):
            for role in sorted(ai_work.SESSION_ROLES):
                value = request()
                value.update(boundary="USER_REQUESTED", role=role, successor_session_capability=capability)
                result = ai_work.session_lifecycle(value)
                self.assertEqual(result["successor_session"], {"required": True, "mode": expected, "role": role})
                self.assertNotIn("created", result["successor_session"])

    def test_invalid_inputs_raise_contract_error(self):
        cases = [
            ("schema_version", True), ("role", []), ("boundary", {}),
            ("successor_session_capability", []), ("session_id", ""),
            ("metrics.context_window_tokens", 0), ("metrics.estimated_context_tokens", True),
            ("metrics.tokens_since_checkpoint", -1), ("metrics.context_window_tokens", 1.5),
            ("policy.checkpoint_delta_tokens", None), ("policy.checkpoint_delta_tokens", 0),
            ("policy.checkpoint_delta_tokens", True), ("policy.soft_context_ratio", float("nan")),
            ("policy.hard_context_ratio", float("inf")), ("policy.hard_context_ratio", 0.6),
            ("policy.soft_context_ratio", 0), ("policy.hard_context_ratio", 1.1),
        ]
        for path, bad in cases:
            with self.subTest(path=path, bad=bad):
                value = request()
                parts = path.split(".")
                target = value if len(parts) == 1 else value[parts[0]]
                target[parts[-1]] = bad
                with self.assertRaises(ai_work.WorkError):
                    ai_work.session_lifecycle(value)
        value = request()
        value["metrics"]["estimated_context_tokens"] = 10 ** 400
        with self.assertRaises(ai_work.WorkError):
            ai_work.session_lifecycle(value)

    def test_control_plane_rejects_extra_payload_fields_at_every_input_level(self):
        for scope in (None, "metrics", "policy"):
            for field in ("prompt", "response", "chat_history", "environment", "credentials"):
                value = request()
                target = value if scope is None else value[scope]
                target[field] = "synthetic payload sentinel"
                with self.subTest(scope=scope, field=field), self.assertRaises(ai_work.WorkError):
                    ai_work.session_lifecycle(value)

    def test_all_schema_objects_are_closed(self):
        def check(node):
            if isinstance(node, dict):
                if node.get("type") == "object":
                    self.assertIs(node.get("additionalProperties"), False)
                for child in node.values():
                    check(child)
            elif isinstance(node, list):
                for child in node:
                    check(child)
        for name in ("session-lifecycle-request", "session-lifecycle-decision", "session-handoff"):
            check(json.loads((ROOT / "foundation" / "schemas" / (name + ".schema.json")).read_text(encoding="utf-8")))
        handoff = json.loads((ROOT / "foundation" / "schemas" / "session-handoff.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(set(handoff["properties"]), {
            "schema_version", "contract", "handoff_id", "predecessor_session_id", "successor_role",
            "checkpoint_id", "created_at", "durable_state_refs", "changed_state_refs",
            "current_work_refs", "unresolved_refs", "delta_handle",
        })

    def test_cli_failure_is_structured_and_does_not_echo_payload(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "request.json"
            for value in ({**request(), "role": []}, {**request(), "policy": {**request()["policy"], "checkpoint_delta_tokens": None}}, {**request(), "prompt": "synthetic payload sentinel"}):
                path.write_text(json.dumps(value), encoding="utf-8")
                result = subprocess.run([sys.executable, str(MODULE_PATH), "session", "--request", str(path)], capture_output=True, text=True, check=False)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(result.stdout, "")
                error = json.loads(result.stderr)
                self.assertEqual(error["contract"], "foundation-session-lifecycle/v1")
                self.assertEqual(error["status"], "BLOCKED")
                self.assertNotIn("synthetic payload sentinel", result.stderr)


if __name__ == "__main__":
    unittest.main()
