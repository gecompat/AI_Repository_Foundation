"""Changed-rule safety, worktree reuse, shared budget, and transfer regressions."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "foundation/runtime/processing_efficiency.py"
spec = importlib.util.spec_from_file_location("processing_efficiency", MODULE)
processing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(processing)


def budget():
    return {"schema_version": 1, "contract": "foundation-processing-budget/v1",
            "wave_id": "wave-1", "unit": "TOKENS", "soft_limit": 80, "hard_limit": 100,
            "next_reservation": 10, "entries": [
                {"invocation_id": "root-1", "actor": "root", "consumed": 30,
                 "reserved": 0, "provenance": "MEASURED"},
                {"invocation_id": "child-1", "actor": "child", "consumed": 20,
                 "reserved": 10, "provenance": "MEASURED"}]}


class ProcessingEfficiencyTests(unittest.TestCase):
    def test_changed_rule_invalidates_dependents_not_independent_analysis(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("A.md", "B.md", "C.md"):
                (root / name).write_text(name, encoding="utf-8")
            deps = {"A.md": ["B.md"], "B.md": [], "C.md": []}
            def capture(**kw):
                args = dict(repository_identity="repo", authority_key="a" * 64,
                            scope_key="scope", discovery_complete=True)
                args.update(kw)
                return processing.capture_context(root, deps, **args)
            session = processing.SessionContext()
            first = capture()
            self.assertEqual(session.check(first)["reread"], sorted(deps))
            session.acknowledge(first, {s: "Analyzed " + s for s in deps})
            self.assertEqual(session.analysis_for(first, "A.md"), "Analyzed A.md")
            self.assertEqual(session.check(capture())["status"], "REUSE")
            (root / "B.md").write_text("changed dirty rule", encoding="utf-8")
            result = session.check(capture())
            self.assertEqual(result["reread"], ["A.md", "B.md"])
            self.assertEqual(result["reuse"], ["C.md"])
            self.assertEqual(session.check(capture(authority_key="b" * 64))["reuse"], [])
            incomplete = capture(discovery_complete=False)
            self.assertEqual(session.check(incomplete)["reuse"], [])
            with self.assertRaises(ValueError):
                session.acknowledge(incomplete, {s: "Analyzed " + s for s in deps})
            self.assertEqual(processing.SessionContext().check(first)["reuse"], [])

    def test_equivalent_worktree_eol_reuses_but_scope_and_repository_do_not(self):
        with tempfile.TemporaryDirectory() as tmp:
            roots = [Path(tmp) / n for n in ("one", "two")]
            for root in roots:
                root.mkdir()
            (roots[0] / "A.md").write_bytes(b"stable\n")
            (roots[1] / "A.md").write_bytes(b"stable\r\n")
            def capture(root, **kw):
                args = dict(repository_identity="repo", authority_key="a" * 64,
                            scope_key="scope", discovery_complete=True)
                args.update(kw)
                return processing.capture_context(root, {"A.md": []}, **args)
            session = processing.SessionContext()
            first = capture(roots[0])
            session.acknowledge(first, {"A.md": "Stable rule analysis"})
            self.assertEqual(session.check(capture(roots[1]))["status"], "REUSE")
            for override in ({"scope_key": "other"}, {"repository_identity": "other"}):
                self.assertEqual(session.check(capture(roots[1], **override))["reuse"], [])
            (roots[1] / "A.md").write_bytes(b"stable")
            self.assertEqual(session.check(capture(roots[1]))["reuse"], [])

    def test_topology_changes_and_missing_or_escaping_sources_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "A.md").write_text("A", encoding="utf-8")
            (root / "B.md").write_text("B", encoding="utf-8")
            args = dict(repository_identity="repo", authority_key="a" * 64,
                        scope_key="scope", discovery_complete=True)
            session = processing.SessionContext()
            first = processing.capture_context(root, {"A.md": [], "B.md": []}, **args)
            session.acknowledge(first, {"A.md": "A analysis", "B.md": "B analysis"})
            second = processing.capture_context(root, {"A.md": ["B.md"], "B.md": []}, **args)
            self.assertEqual(session.check(second)["reread"], ["A.md"])
            for deps in ({"../A.md": []}, {"A.md": ["missing.md"]}):
                with self.assertRaises(ValueError):
                    processing.capture_context(root, deps, **args)
            with self.assertRaises(OSError):
                processing.capture_context(root, {"missing.md": []}, **args)

    def test_shared_budget_boundaries_deduplication_and_no_implicit_reservation(self):
        req = budget()
        original = copy.deepcopy(req)
        self.assertEqual(processing.budget_decision(req)["action"], "ALLOW_NEW_WORK")
        req["next_reservation"] = 20
        self.assertEqual(processing.budget_decision(req)["action"], "CHECKPOINT")
        req["next_reservation"] = 40
        result = processing.budget_decision(req)
        self.assertEqual(result["action"], "STOP_NEW_WORK")
        self.assertFalse(result["reservation_applied"])
        self.assertFalse(result["provider_limit_enforced"])
        req = original
        req["entries"].append(copy.deepcopy(req["entries"][1]))
        self.assertEqual(processing.budget_decision(req)["unique_invocations"], 2)
        req["entries"][-1]["consumed"] += 1
        with self.assertRaises(ValueError):
            processing.budget_decision(req)

    def test_unverified_and_invalid_budgets_never_claim_enforcement(self):
        for provenance, consumed in (("UNKNOWN", None), ("ESTIMATED", 20)):
            req = budget()
            req["entries"][1].update(provenance=provenance, consumed=consumed)
            self.assertEqual(processing.budget_decision(req)["action"], "BUDGET_UNVERIFIED")
        for bad in (True, -1, float("nan"), float("inf"), "5", 10 ** 400):
            req = budget()
            req["next_reservation"] = bad
            with self.assertRaises(ValueError):
                processing.budget_decision(req)
        req = budget()
        req["hard_limit"] = 10
        with self.assertRaises(ValueError):
            processing.budget_decision(req)
        req = budget()
        req["entries"][1]["provenance"] = "UNKNOWN"
        with self.assertRaises(ValueError):
            processing.budget_decision(req)

    def test_audit_is_advisory_and_does_not_disclose_rule_text(self):
        rules = {"AGENTS.md": "Vor jeder Änderung lesen\nKeep protected validation.\nReview each review."}
        result = processing.audit_governance(rules)
        self.assertEqual([r["code"] for r in result], ["BROAD_READING_PER_EDIT", "REVIEW_CHAIN"])
        self.assertTrue(all(r["advisory"] for r in result))
        self.assertNotIn("protected validation", json.dumps(result))

    def test_core_only_install_contains_runtime_and_budget_cli_works(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "target"
            target.mkdir()
            done = subprocess.run([sys.executable, str(ROOT / "tools/install_foundation.py"),
                                   str(target), "--adapters", "none",
                                   "--capabilities", "none", "--apply"], capture_output=True, text=True)
            self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
            installed = target / ".ai/foundation/runtime/processing_efficiency.py"
            self.assertTrue(installed.is_file())
            req = Path(tmp) / "budget.json"
            req.write_text(json.dumps(budget()), encoding="utf-8")
            done = subprocess.run([sys.executable, str(installed), "budget", "--request", str(req)],
                                  capture_output=True, text=True)
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertEqual(json.loads(done.stdout)["action"], "ALLOW_NEW_WORK")
            req.write_text('{"prompt": "not control data"}', encoding="utf-8")
            done = subprocess.run([sys.executable, str(installed), "budget", "--request", str(req)],
                                  capture_output=True, text=True)
            self.assertEqual(done.returncode, 2)


if __name__ == "__main__":
    unittest.main()
