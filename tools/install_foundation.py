#!/usr/bin/env python3
"""Plan or install manifest-whitelisted AI Repository Foundation core and optional modules."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from content_equivalence import files_equivalent, portable_file_sha256

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "foundation" / "manifest.json"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
PROVENANCE_CONTRACT = "foundation-installation-provenance/v1"
RELEASE_PACKAGE_CONTRACT = "foundation-release-package/v1"


@dataclass(frozen=True)
class TransferEntry:
    source: Path
    target_rel: Path
    kind: str
    merge: str
    source_sha256: str


@dataclass(frozen=True)
class PlanItem:
    state: str
    entry: TransferEntry
    destination: Path


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def parse_selection(manifest: dict, raw: str, *, section: str, default_key: str) -> list[str]:
    if raw == "default":
        return list(manifest.get(default_key, []))
    if raw == "none":
        return []
    names = [name.strip() for name in raw.split(",") if name.strip()]
    unknown = sorted(set(names) - set(manifest.get(section, {})))
    if unknown:
        raise ValueError(f"unknown {section.rstrip('s')}(s): {', '.join(unknown)}")
    return names


def parse_adapters(manifest: dict, raw: str) -> list[str]:
    return parse_selection(manifest, raw, section="adapters", default_key="default_adapters")


def parse_capabilities(manifest: dict, raw: str) -> list[str]:
    selected = parse_selection(manifest, raw, section="capabilities", default_key="default_capabilities")
    dependencies = manifest.get("capability_dependencies", {})
    result: list[str] = []

    def include(name: str, active: set[str]) -> None:
        if name in active:
            raise ValueError(f"cyclic capability dependency: {name}")
        if name in result:
            return
        if name not in manifest.get("capabilities", {}):
            raise ValueError(f"unknown capability dependency: {name}")
        active.add(name)
        for dependency in dependencies.get(name, []):
            include(dependency, active)
        active.remove(name)
        result.append(name)

    for name in selected:
        include(name, set())
    return result


def transfer_entries(
    manifest: dict,
    adapters: list[str],
    capabilities: list[str] | None = None,
) -> list[TransferEntry]:
    rows = list(manifest["core"])
    for adapter in adapters:
        rows.extend(manifest["adapters"][adapter])
    for capability in capabilities or []:
        rows.extend(manifest.get("capabilities", {})[capability])

    result = []
    seen_targets: set[Path] = set()
    for row in rows:
        target_rel = Path(row["target"])
        if target_rel in seen_targets:
            raise ValueError(f"duplicate target in manifest: {target_rel}")
        seen_targets.add(target_rel)
        source = ROOT / row["source"]
        if not source.is_file():
            raise ValueError(f"manifest source missing: {row['source']}")
        source_sha256 = row.get("source_sha256")
        if not isinstance(source_sha256, str) or not SHA256_RE.fullmatch(source_sha256):
            raise ValueError(f"manifest source hash missing or invalid: {row['source']}")
        actual_sha256 = portable_file_sha256(source)
        if source_sha256 != actual_sha256:
            raise ValueError(f"manifest source hash mismatch: {row['source']}")
        result.append(TransferEntry(source, target_rel, row["kind"], row["merge"], source_sha256))
    return result


def parse_intentional_overrides(values: list[str]) -> dict[str, str]:
    overrides: dict[str, str] = {}
    for value in values:
        target, separator, reason = value.partition("=")
        target = Path(target.strip()).as_posix()
        reason = reason.strip()
        if not separator or not target or not reason:
            raise ValueError("intentional overrides require TARGET=REASON")
        if target in overrides:
            raise ValueError(f"duplicate intentional override: {target}")
        overrides[target] = reason
    return overrides


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def packaged_source_commit() -> str | None:
    """Recover source identity only from a completely self-consistent extracted package."""
    index_path = ROOT / "foundation" / "release-package.json"
    if not index_path.is_file():
        return None
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
        package_id = index.pop("package_id")
        if (
            index.get("schema_version") != 1
            or index.get("contract") != RELEASE_PACKAGE_CONTRACT
            or index.get("ruleset_version") != load_manifest().get("ruleset_version")
            or package_id != hashlib.sha256(canonical_json(index)).hexdigest()
        ):
            return None
        commit = index.get("source_commit")
        files = index.get("files")
        if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit) or not isinstance(files, list):
            return None
        expected_sources = {
            "foundation/manifest.json",
            "tools/content_equivalence.py",
            "tools/install_foundation.py",
        }
        manifest = load_manifest()
        expected_sources.update(row["source"] for row in manifest["core"])
        for rows in manifest.get("adapters", {}).values():
            expected_sources.update(row["source"] for row in rows)
        for rows in manifest.get("capabilities", {}).values():
            expected_sources.update(row["source"] for row in rows)
        if {entry.get("path") for entry in files if isinstance(entry, dict)} != expected_sources:
            return None
        for entry in files:
            if not isinstance(entry, dict) or set(entry) != {"path", "role", "sha256", "portable_sha256", "size_bytes"}:
                return None
            source = ROOT / entry["path"]
            body = source.read_bytes()
            if (
                len(body) != entry["size_bytes"]
                or hashlib.sha256(body).hexdigest() != entry["sha256"]
                or portable_file_sha256(source) != entry["portable_sha256"]
            ):
                return None
        return commit
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return None


def source_commit() -> str | None:
    """Return an exact source commit only when the checkout has no local changes."""
    try:
        status = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=normal"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        if status.stdout.strip():
            return packaged_source_commit()
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return packaged_source_commit()
    commit = result.stdout.strip().lower()
    return commit if re.fullmatch(r"[0-9a-f]{40}", commit) else packaged_source_commit()


def provenance_target(manifest: dict, target: Path) -> Path:
    contract = manifest.get("installed_provenance_contract")
    if not isinstance(contract, dict) or contract.get("profile") != PROVENANCE_CONTRACT:
        raise ValueError("installed_provenance_contract is missing or invalid")
    target_value = contract.get("target")
    if not isinstance(target_value, str) or not target_value:
        raise ValueError("installed_provenance_contract.target is missing")
    return target / target_value


def build_provenance(
    manifest: dict,
    target: Path,
    entries: list[TransferEntry],
    adapters: list[str],
    capabilities: list[str],
    overrides: dict[str, str],
) -> dict:
    selected = {entry.target_rel.as_posix() for entry in entries}
    unknown = sorted(set(overrides) - selected)
    if unknown:
        raise ValueError(f"intentional override target is not selected: {', '.join(unknown)}")

    files: list[dict[str, object]] = []
    required_overrides: list[str] = []
    for entry in sorted(entries, key=lambda item: item.target_rel.as_posix()):
        destination = target / entry.target_rel
        if not destination.is_file():
            raise ValueError(f"selected target file is missing: {entry.target_rel.as_posix()}")
        installed_sha256 = portable_file_sha256(destination)
        target_name = entry.target_rel.as_posix()
        differs = installed_sha256 != entry.source_sha256
        if differs and target_name not in overrides:
            required_overrides.append(target_name)
        if not differs and target_name in overrides:
            raise ValueError(f"intentional override matches the Foundation baseline: {target_name}")
        files.append(
            {
                "source": entry.source.relative_to(ROOT).as_posix(),
                "target": target_name,
                "kind": entry.kind,
                "merge": entry.merge,
                "source_sha256": entry.source_sha256,
                "installed_sha256": installed_sha256,
                "integration_state": "INTENTIONAL_OVERRIDE" if differs else "FOUNDATION_BASELINE",
                "reason": overrides.get(target_name),
            }
        )
    if required_overrides:
        raise ValueError(
            "differing selected files require explicit --intentional-override TARGET=REASON: "
            + ", ".join(required_overrides)
        )

    repository = manifest.get("source_repository")
    if not isinstance(repository, str) or not repository:
        raise ValueError("manifest source_repository is missing")
    return {
        "schema_version": 1,
        "contract": PROVENANCE_CONTRACT,
        "ruleset_version": manifest["ruleset_version"],
        "source_repository": repository,
        "source_commit": source_commit(),
        "source_manifest_sha256": portable_file_sha256(MANIFEST_PATH),
        "recorded_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "selection": {
            "adapters": sorted(adapters),
            "capabilities": sorted(capabilities),
        },
        "files": files,
    }


def write_provenance(path: Path, payload: dict) -> bool:
    """Atomically write changed provenance; preserve timestamps for an identical receipt."""
    if path.is_file():
        try:
            current = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            current = None
        if isinstance(current, dict):
            comparable_current = {**current, "recorded_at": payload["recorded_at"]}
            if comparable_current == payload:
                return False
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(payload, stream, indent=2, sort_keys=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_path, path)
    finally:
        temp_path.unlink(missing_ok=True)
    return True


def capability_notices(capabilities: list[str]) -> list[dict[str, str]]:
    notices: list[dict[str, str]] = []
    if "artifact-registry-github" in capabilities:
        notices.append(
            {
                "code": "GITHUB_REQUIRED_CHECKS_RECOMMENDED",
                "severity": "RECOMMENDATION",
                "message": (
                    "The artifact-registry-github workflow files do not enable GitHub branch protection or make checks required. "
                    "If hard server-side enforcement is desired, configure branch protection/rulesets separately and require the "
                    "semantic registry check plus the project's normal CI. Mandatory external CI can also become an availability "
                    "dependency: if repository continuity matters, consider separating unbypassable core branch safety from a CI "
                    "ruleset with a narrowly authorized pull-request-only bypass for infrastructure-unavailable checks. Never use "
                    "that path for a substantive validation failure. Repository protection, break-glass actors, and outage thresholds "
                    "are target-project administration choices; Foundation installation does not configure them and they are not "
                    "required for FOUNDATION_INTEGRITY."
                ),
            }
        )
    if "model-router" in capabilities:
        notices.append(
            {
                "code": "MODEL_ROUTER_RUNTIME_CONFIGURATION_REQUIRED",
                "severity": "NOTICE",
                "message": (
                    "The model-router capability is installed without credentials, live catalog data, or client configuration. "
                    "Keep its runtime store outside the repository, supply provider credentials only through the execution "
                    "environment, sync a fresh catalog, and merge only the relevant Visual Studio or GitHub Copilot MCP template "
                    "into that client's configuration. The two clients use different top-level MCP shapes. Remote routing remains "
                    "disabled unless each request explicitly authorizes it."
                ),
            }
        )
    if "ai-work" in capabilities:
        notices.append(
            {
                "code": "AI_WORK_PLANNER_IS_DECISION_ONLY",
                "severity": "NOTICE",
                "message": (
                    "The ai-work capability installs an optional decision-only planner. It does not configure or invoke models, "
                    "tools, providers, MCP, networks, executors, provisioners, clients, or credentials and grants no authority. "
                    "Keep payloads and runtime evidence outside version control; unavailable components must remain truthful "
                    "MANUAL_REQUIRED, UNAVAILABLE, or BLOCKED outcomes."
                ),
            }
        )
    if "ai-runtime-adapters" in capabilities:
        notices.append(
            {
                "code": "AI_RUNTIME_ADAPTER_CONFIGURATION_REQUIRED",
                "severity": "NOTICE",
                "message": (
                    "The ai-runtime-adapters capability installs protocol and reference code only. It does not trust a loopback "
                    "endpoint, enable network access, allow remote models, disclose credentials, choose file roots, or invoke a "
                    "runtime. Keep endpoint/host configuration, payloads, resource-cost evidence, and adapter state outside version "
                    "control; allowlist only required environment names and data classes."
                ),
            }
        )
    if "ai-executor" in capabilities:
        notices.append(
            {
                "code": "AI_EXECUTOR_RUNTIME_CONFIGURATION_REQUIRED",
                "severity": "NOTICE",
                "message": (
                    "The ai-executor capability installs an optional reference executor without adapter bindings, handles, "
                    "approvals, credentials, or execution authority. Keep all runtime configuration and checkpoints outside "
                    "version control, use absolute shell-free adapter argv, and reconcile ambiguous non-idempotent external "
                    "effects manually. Installing it does not make Python, any adapter, model, provider, or network mandatory."
                ),
            }
        )
    if "ai-provisioning" in capabilities:
        notices.append(
            {
                "code": "AI_PROVISIONING_EXACT_APPROVAL_REQUIRED",
                "severity": "NOTICE",
                "message": (
                    "The ai-provisioning capability installs optional reference code only. Keep definitions, inventories, "
                    "plans, approvals, downloads, cost evidence, targets, and checkpoints outside version control. A download "
                    "or offline install requires an exact unexpired plan and matching approval; failed or ambiguous work must "
                    "be reconciled under a new plan. Installing it grants no network, credential, spend, install, or repository "
                    "authority and does not make Python or any runtime mandatory."
                ),
            }
        )
    if "ai-client-integration" in capabilities:
        notices.append(
            {
                "code": "AI_CLIENT_INTEGRATION_EXTERNAL_STATE_AND_AUTHORITY_REQUIRED",
                "severity": "NOTICE",
                "message": (
                    "The ai-client-integration capability installs optional reference code only. Detect and plan before any "
                    "apply, preserve existing client configuration semantically, and keep backups, plans, prompt handles, "
                    "dispatch receipts, and synthesized adapters outside version control. A requested model is not proof of "
                    "actual execution; use host execution/response evidence or preserve REQUESTED_NOT_ATTESTED and the "
                    "MANUAL_DISPATCH_REQUIRED fallback. Installation grants no configuration, repository, network, credential, "
                    "model, push, pull-request, publication, or adapter-synthesis authority."
                ),
            }
        )
    if "ai-orchestrator" in capabilities:
        notices.append(
            {
                "code": "AI_ORCHESTRATOR_EXTERNAL_EVIDENCE_REQUIRED",
                "severity": "NOTICE",
                "message": (
                    "The ai-orchestrator capability installs optional reference code only. Keep runtime configuration, model "
                    "evidence, source definitions, content handles, and state outside version control. Automatic routing requires "
                    "fresh source-backed quality/cost evidence; otherwise use the truthful MANUAL_REQUIRED handoff. Installation "
                    "grants no network, credential, data-transfer, spend, model, file, Git, push, pull-request, or publication authority."
                ),
            }
        )
    return notices


def build_plan(target: Path, entries: list[TransferEntry]) -> list[PlanItem]:
    plan: list[PlanItem] = []
    for entry in entries:
        destination = target / entry.target_rel
        if not destination.exists():
            state = "CREATE"
        elif not destination.is_file():
            state = "CONFLICT"
        elif files_equivalent(destination, entry.source):
            state = "UNCHANGED"
        else:
            state = "MERGE_REQUIRED"
        plan.append(PlanItem(state, entry, destination))
    return plan


def plan_payload(plan: list[PlanItem], notices: list[dict[str, str]] | None = None) -> dict:
    return {
        "schema_version": 1,
        "items": [
            {
                "state": item.state,
                "source": item.entry.source.relative_to(ROOT).as_posix(),
                "target": item.entry.target_rel.as_posix(),
                "kind": item.entry.kind,
                "merge": item.entry.merge,
                "source_sha256": item.entry.source_sha256,
            }
            for item in plan
        ],
        "notices": notices or [],
    }


def print_notices(notices: list[dict[str, str]]) -> None:
    for notice in notices:
        print(f"[{notice['severity']}] {notice['code']}: {notice['message']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="target repository directory")
    parser.add_argument(
        "--adapters",
        default="default",
        help="default, none, or comma-separated adapter names",
    )
    parser.add_argument(
        "--capabilities",
        default="none",
        help="default, none, or comma-separated optional capability names",
    )
    parser.add_argument("--apply", action="store_true", help="create missing files after a clean plan")
    parser.add_argument(
        "--record-provenance",
        action="store_true",
        help="record an already completed direct/semantic transfer without copying files",
    )
    parser.add_argument(
        "--intentional-override",
        action="append",
        default=[],
        metavar="TARGET=REASON",
        help="classify one selected differing target as an intentional semantic override",
    )
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args(argv)

    target = args.target.resolve()
    if target == ROOT or ROOT in target.parents:
        print("[BLOCK] target must be outside the Foundation repository")
        return 2

    try:
        manifest = load_manifest()
        adapters = parse_adapters(manifest, args.adapters)
        capabilities = parse_capabilities(manifest, args.capabilities)
        entries = transfer_entries(manifest, adapters, capabilities)
        overrides = parse_intentional_overrides(args.intentional_override)
        receipt_path = provenance_target(manifest, target)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"[BLOCK] {exc}")
        return 2

    if args.apply and args.record_provenance:
        print("[BLOCK] --apply and --record-provenance are mutually exclusive")
        return 2
    if args.intentional_override and not args.record_provenance:
        print("[BLOCK] --intentional-override requires --record-provenance")
        return 2

    notices = capability_notices(capabilities)
    plan = build_plan(target, entries)
    payload = plan_payload(plan, notices)
    if args.json_output:
        print(json.dumps(payload, indent=2))
    else:
        for item in plan:
            print(f"[{item.state}] {item.entry.target_rel.as_posix()}")
        print_notices(notices)

    blocked = [item for item in plan if item.state in {"MERGE_REQUIRED", "CONFLICT"}]
    if args.apply and blocked:
        print("[BLOCK] semantic merge/conflict review required; nothing written")
        return 2

    if args.record_provenance:
        conflicts = [item for item in plan if item.state in {"CREATE", "CONFLICT"}]
        if conflicts:
            print("[BLOCK] every selected target must be an existing file before provenance is recorded")
            return 2
        try:
            receipt = build_provenance(manifest, target, entries, adapters, capabilities, overrides)
            changed = write_provenance(receipt_path, receipt)
        except (OSError, ValueError) as exc:
            print(f"[BLOCK] {exc}")
            return 2
        print(f"[PROVENANCE] {'written' if changed else 'unchanged'}={receipt_path.relative_to(target).as_posix()}")
        return 0

    if not args.apply:
        creates = sum(item.state == "CREATE" for item in plan)
        unchanged = sum(item.state == "UNCHANGED" for item in plan)
        merges = sum(item.state == "MERGE_REQUIRED" for item in plan)
        conflicts = sum(item.state == "CONFLICT" for item in plan)
        print(f"[PLAN] create={creates} unchanged={unchanged} merge_required={merges} conflicts={conflicts}")
        return 2 if conflicts else 0

    target.mkdir(parents=True, exist_ok=True)
    created = 0
    for item in plan:
        if item.state != "CREATE":
            continue
        item.destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item.entry.source, item.destination)
        created += 1
    try:
        receipt = build_provenance(manifest, target, entries, adapters, capabilities, {})
        provenance_changed = write_provenance(receipt_path, receipt)
    except (OSError, ValueError) as exc:
        print(f"[BLOCK] transferred files were written but provenance failed: {exc}")
        return 2
    print(f"[OK] created={created} unchanged={sum(i.state == 'UNCHANGED' for i in plan)}")
    print(f"[PROVENANCE] {'written' if provenance_changed else 'unchanged'}={receipt_path.relative_to(target).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
