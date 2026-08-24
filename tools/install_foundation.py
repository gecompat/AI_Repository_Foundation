#!/usr/bin/env python3
"""Plan or install manifest-whitelisted AI Repository Foundation core and optional modules."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "foundation" / "manifest.json"


@dataclass(frozen=True)
class TransferEntry:
    source: Path
    target_rel: Path
    kind: str
    merge: str


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
    return parse_selection(manifest, raw, section="capabilities", default_key="default_capabilities")


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
        result.append(TransferEntry(source, target_rel, row["kind"], row["merge"]))
    return result


def build_plan(target: Path, entries: list[TransferEntry]) -> list[PlanItem]:
    plan: list[PlanItem] = []
    for entry in entries:
        destination = target / entry.target_rel
        if not destination.exists():
            state = "CREATE"
        elif not destination.is_file():
            state = "CONFLICT"
        elif destination.read_bytes() == entry.source.read_bytes():
            state = "UNCHANGED"
        else:
            state = "MERGE_REQUIRED"
        plan.append(PlanItem(state, entry, destination))
    return plan


def plan_payload(plan: list[PlanItem]) -> dict:
    return {
        "schema_version": 1,
        "items": [
            {
                "state": item.state,
                "source": item.entry.source.relative_to(ROOT).as_posix(),
                "target": item.entry.target_rel.as_posix(),
                "kind": item.entry.kind,
                "merge": item.entry.merge,
            }
            for item in plan
        ],
    }


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
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"[BLOCK] {exc}")
        return 2

    plan = build_plan(target, entries)
    payload = plan_payload(plan)
    if args.json_output:
        print(json.dumps(payload, indent=2))
    else:
        for item in plan:
            print(f"[{item.state}] {item.entry.target_rel.as_posix()}")

    blocked = [item for item in plan if item.state in {"MERGE_REQUIRED", "CONFLICT"}]
    if args.apply and blocked:
        print("[BLOCK] semantic merge/conflict review required; nothing written")
        return 2

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
    print(f"[OK] created={created} unchanged={sum(i.state == 'UNCHANGED' for i in plan)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
