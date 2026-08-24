from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON_CLIENT = ROOT / "tools" / "identity" / "artifact_reference.py"
POWERSHELL_CLIENT = ROOT / "tools" / "identity" / "ArtifactReference.ps1"
FIXTURES = json.loads((ROOT / "tests" / "fixtures" / "artifact_registration_contract.json").read_text(encoding="utf-8"))


def run_json(command: list[str], expected_rc: int = 0) -> dict:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode != expected_rc:
        raise AssertionError(
            f"unexpected rc={completed.returncode} expected={expected_rc}\n"
            f"stdout={completed.stdout}\nstderr={completed.stderr}"
        )
    if expected_rc != 0:
        return {"stderr": completed.stderr}
    return json.loads(completed.stdout)


def python_command(operation: str, registry: Path, *args: str) -> list[str]:
    return [sys.executable, str(PYTHON_CLIENT), operation, "--registry", str(registry), *args]


def powershell_command(operation: str, registry: Path, *args: str) -> list[str]:
    pwsh = shutil.which("pwsh")
    if not pwsh:
        raise unittest.SkipTest("pwsh is not installed")
    translated: list[str] = []
    mapping = {
        "--artifact": "-ArtifactPath",
        "--mode": "-Mode",
        "--kind": "-Kind",
        "--title": "-Title",
        "--uid": "-Uid",
        "--human-ref": "-HumanRef",
        "--expected-registry-revision": "-ExpectedRegistryRevision",
    }
    index = 0
    while index < len(args):
        translated.extend([mapping[args[index]], args[index + 1]])
        index += 2
    return [
        pwsh,
        "-NoLogo",
        "-NoProfile",
        "-File",
        str(POWERSHELL_CLIENT),
        "-Operation",
        operation,
        "-RegistryPath",
        str(registry),
        *translated,
    ]


def urn_uuid_version(value: str) -> int | None:
    prefix = "urn:uuid:"
    if not value.startswith(prefix):
        raise AssertionError(f"not a UUID URN: {value}")
    return uuid.UUID(value[len(prefix):]).version


class ArtifactRegistrationContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assertEqual(FIXTURES["schema_version"], 1)

    def init_pair(self, root: Path) -> tuple[Path, Path]:
        python_registry = root / "python" / "registry.json"
        powershell_registry = root / "powershell" / "registry.json"
        python_result = run_json(python_command("init", python_registry))
        powershell_result = run_json(powershell_command("init", powershell_registry))
        self.assertEqual(python_result, powershell_result)
        self.assertEqual(json.loads(python_registry.read_text(encoding="utf-8")), python_result)
        self.assertEqual(json.loads(powershell_registry.read_text(encoding="utf-8-sig")), powershell_result)
        return python_registry, powershell_registry

    def test_direct_allocation_is_contract_equivalent(self) -> None:
        case = FIXTURES["cases"]["direct"]
        with tempfile.TemporaryDirectory() as tmp:
            py_registry, ps_registry = self.init_pair(Path(tmp))
            args = ["--mode", "DIRECT", "--kind", case["kind"], "--title", case["title"], "--uid", case["uid"]]
            py_artifact = run_json(python_command("new", py_registry, *args))
            ps_artifact = run_json(powershell_command("new", ps_registry, *args))
            self.assertEqual(py_artifact, ps_artifact)
            self.assertEqual(py_artifact["human_ref"], case["expected_human_ref"])
            self.assertEqual(py_artifact["registration_state"], "REGISTERED")
            py_state = json.loads(py_registry.read_text(encoding="utf-8"))
            ps_state = json.loads(ps_registry.read_text(encoding="utf-8-sig"))
            self.assertEqual(py_state, ps_state)
            self.assertEqual(py_state["registry_revision"], case["expected_registry_revision"])
            self.assertEqual(py_state["allocations"][case["expected_human_ref"]], case["uid"])

    def test_deferred_creation_does_not_allocate_sequence(self) -> None:
        case = FIXTURES["cases"]["deferred"]
        with tempfile.TemporaryDirectory() as tmp:
            py_registry, ps_registry = self.init_pair(Path(tmp))
            initial_py = json.loads(py_registry.read_text(encoding="utf-8"))
            initial_ps = json.loads(ps_registry.read_text(encoding="utf-8-sig"))
            args = ["--mode", "DEFERRED", "--kind", case["kind"], "--title", case["title"], "--uid", case["uid"]]
            py_artifact = run_json(python_command("new", py_registry, *args))
            ps_artifact = run_json(powershell_command("new", ps_registry, *args))
            self.assertEqual(py_artifact, ps_artifact)
            self.assertIsNone(py_artifact["human_ref"])
            self.assertEqual(py_artifact["registration_state"], "DRAFT")
            self.assertEqual(json.loads(py_registry.read_text(encoding="utf-8")), initial_py)
            self.assertEqual(json.loads(ps_registry.read_text(encoding="utf-8-sig")), initial_ps)

    def test_deferred_artifact_can_be_registered_later(self) -> None:
        case = FIXTURES["cases"]["register"]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            py_registry, ps_registry = self.init_pair(root)
            py_artifact_path = root / "python" / "artifact.json"
            ps_artifact_path = root / "powershell" / "artifact.json"
            new_args = [
                "--artifact", str(py_artifact_path), "--mode", "DEFERRED", "--kind", case["kind"],
                "--title", case["title"], "--uid", case["uid"],
            ]
            run_json(python_command("new", py_registry, *new_args))
            ps_new_args = [
                "--artifact", str(ps_artifact_path), "--mode", "DEFERRED", "--kind", case["kind"],
                "--title", case["title"], "--uid", case["uid"],
            ]
            run_json(powershell_command("new", ps_registry, *ps_new_args))

            py_registered = run_json(python_command("register", py_registry, "--artifact", str(py_artifact_path)))
            ps_registered = run_json(powershell_command("register", ps_registry, "--artifact", str(ps_artifact_path)))
            self.assertEqual(py_registered, ps_registered)
            self.assertEqual(py_registered["human_ref"], case["expected_human_ref"])
            self.assertEqual(py_registered["registration_state"], "REGISTERED")
            self.assertEqual(json.loads(py_registry.read_text(encoding="utf-8"))["registry_revision"], case["expected_registry_revision"])
            self.assertEqual(json.loads(ps_registry.read_text(encoding="utf-8-sig"))["registry_revision"], case["expected_registry_revision"])

    def test_stale_registry_revision_is_rejected_by_both_clients(self) -> None:
        case = FIXTURES["cases"]["direct"]
        with tempfile.TemporaryDirectory() as tmp:
            py_registry, ps_registry = self.init_pair(Path(tmp))
            first_args = [
                "--mode", "DIRECT", "--kind", case["kind"], "--title", case["title"],
                "--uid", case["uid"], "--expected-registry-revision", "0",
            ]
            run_json(python_command("new", py_registry, *first_args))
            run_json(powershell_command("new", ps_registry, *first_args))
            second_uid = "urn:uuid:01890f1c-7b00-7abc-8abc-1234567890ac"
            stale_args = [
                "--mode", "DIRECT", "--kind", case["kind"], "--title", "stale", "--uid", second_uid,
                "--expected-registry-revision", "0",
            ]
            py_error = run_json(python_command("new", py_registry, *stale_args), expected_rc=2)
            ps_error = run_json(powershell_command("new", ps_registry, *stale_args), expected_rc=2)
            self.assertIn("stale registry revision", py_error["stderr"])
            self.assertIn("stale registry revision", ps_error["stderr"])

    def test_resolve_is_contract_equivalent(self) -> None:
        case = FIXTURES["cases"]["direct"]
        with tempfile.TemporaryDirectory() as tmp:
            py_registry, ps_registry = self.init_pair(Path(tmp))
            args = ["--mode", "DIRECT", "--kind", case["kind"], "--title", case["title"], "--uid", case["uid"]]
            run_json(python_command("new", py_registry, *args))
            run_json(powershell_command("new", ps_registry, *args))
            py_result = run_json(python_command("resolve", py_registry, "--human-ref", case["expected_human_ref"]))
            ps_result = run_json(powershell_command("resolve", ps_registry, "--human-ref", case["expected_human_ref"]))
            self.assertEqual(py_result, ps_result)
            self.assertEqual(py_result["artifact_uid"], case["uid"])

    def test_generated_uid_is_uuidv7_in_each_client(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            py_registry, ps_registry = self.init_pair(Path(tmp))
            args = ["--mode", "DEFERRED", "--kind", "work_item", "--title", "generated"]
            py_uid = run_json(python_command("new", py_registry, *args))["artifact_uid"]
            ps_uid = run_json(powershell_command("new", ps_registry, *args))["artifact_uid"]
            self.assertEqual(urn_uuid_version(py_uid), 7)
            self.assertEqual(urn_uuid_version(ps_uid), 7)


if __name__ == "__main__":
    unittest.main()
