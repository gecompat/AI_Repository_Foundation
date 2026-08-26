#!/usr/bin/env python3
"""Configure/verify layered GitHub Rulesets for Foundation main continuity.

Creates an unbypassable core-safety ruleset and a CI-gates ruleset whose bypass is
limited to pull requests for one explicitly resolved user. The legacy classic branch
protection is removed only after both Rulesets have been read back and verified.

Requires repository Administration: write. The token is read only from an environment
variable and is never accepted on the command line.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

API_VERSION = "2026-03-10"
DEFAULT_REPOSITORY = "gecompat/AI_Repository_Foundation"
DEFAULT_BRANCH = "main"
DEFAULT_CHECKS = ["validate", "registry-integrity"]
CORE_NAME = "foundation-main-core-safety"
CI_NAME = "foundation-main-ci-gates"


def request(method: str, url: str, token: str, payload: dict | None = None) -> Any:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("X-GitHub-Api-Version", API_VERSION)
    req.add_header("User-Agent", "AI-Repository-Foundation-ruleset-continuity")
    try:
        with urllib.request.urlopen(req) as response:
            raw = response.read()
            return None if not raw else json.loads(raw.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API {exc.code}: {detail}") from exc


def ref_condition(branch: str) -> dict:
    return {"ref_name": {"include": [f"refs/heads/{branch}"], "exclude": []}}


def pull_request_rule() -> dict:
    return {
        "type": "pull_request",
        "parameters": {
            "dismiss_stale_reviews_on_push": False,
            "require_code_owner_review": False,
            "require_last_push_approval": False,
            "required_approving_review_count": 0,
            "required_review_thread_resolution": False,
        },
    }


def core_payload(branch: str) -> dict:
    return {
        "name": CORE_NAME,
        "target": "branch",
        "enforcement": "active",
        "bypass_actors": [],
        "conditions": ref_condition(branch),
        "rules": [
            pull_request_rule(),
            {"type": "required_linear_history"},
            {"type": "non_fast_forward"},
            {"type": "deletion"},
        ],
    }


def ci_payload(branch: str, checks: list[str], bypass_user_id: int) -> dict:
    return {
        "name": CI_NAME,
        "target": "branch",
        "enforcement": "active",
        "bypass_actors": [
            {
                "actor_id": bypass_user_id,
                "actor_type": "User",
                "bypass_mode": "pull_request",
            }
        ],
        "conditions": ref_condition(branch),
        "rules": [
            {
                "type": "required_status_checks",
                "parameters": {
                    "do_not_enforce_on_create": False,
                    "required_status_checks": [{"context": check} for check in checks],
                    "strict_required_status_checks_policy": True,
                },
            }
        ],
    }


def list_rulesets(base_url: str, token: str) -> list[dict]:
    value = request("GET", f"{base_url}/rulesets", token)
    if not isinstance(value, list):
        raise RuntimeError("GitHub ruleset list response is not an array")
    return value


def full_ruleset(base_url: str, token: str, ruleset_id: int) -> dict:
    value = request("GET", f"{base_url}/rulesets/{ruleset_id}", token)
    if not isinstance(value, dict):
        raise RuntimeError(f"GitHub ruleset {ruleset_id} response is not an object")
    return value


def upsert(base_url: str, token: str, payload: dict) -> dict:
    matches = [row for row in list_rulesets(base_url, token) if row.get("name") == payload["name"]]
    if len(matches) > 1:
        raise RuntimeError(f"multiple rulesets named {payload['name']}")
    if matches:
        ruleset_id = int(matches[0]["id"])
        request("PUT", f"{base_url}/rulesets/{ruleset_id}", token, payload)
    else:
        created = request("POST", f"{base_url}/rulesets", token, payload)
        if not isinstance(created, dict) or "id" not in created:
            raise RuntimeError(f"GitHub did not return an ID for ruleset {payload['name']}")
        ruleset_id = int(created["id"])
    return full_ruleset(base_url, token, ruleset_id)


def rule_types(value: dict) -> set[str]:
    return {row.get("type") for row in value.get("rules", []) if isinstance(row, dict) and isinstance(row.get("type"), str)}


def verify_core(value: dict, branch: str) -> list[str]:
    problems: list[str] = []
    if value.get("name") != CORE_NAME or value.get("enforcement") != "active" or value.get("target") != "branch":
        problems.append("core ruleset name/target/enforcement mismatch")
    if value.get("bypass_actors"):
        problems.append("core ruleset must have no bypass actors")
    include = (((value.get("conditions") or {}).get("ref_name") or {}).get("include") or [])
    if f"refs/heads/{branch}" not in include:
        problems.append(f"core ruleset does not target refs/heads/{branch}")
    required = {"pull_request", "required_linear_history", "non_fast_forward", "deletion"}
    missing = sorted(required - rule_types(value))
    if missing:
        problems.append("core ruleset missing rules: " + ", ".join(missing))
    return problems


def verify_ci(value: dict, branch: str, checks: list[str], bypass_user_id: int) -> list[str]:
    problems: list[str] = []
    if value.get("name") != CI_NAME or value.get("enforcement") != "active" or value.get("target") != "branch":
        problems.append("CI ruleset name/target/enforcement mismatch")
    include = (((value.get("conditions") or {}).get("ref_name") or {}).get("include") or [])
    if f"refs/heads/{branch}" not in include:
        problems.append(f"CI ruleset does not target refs/heads/{branch}")
    bypass = value.get("bypass_actors") or []
    expected_actor = {
        "actor_id": bypass_user_id,
        "actor_type": "User",
        "bypass_mode": "pull_request",
    }
    if not any(
        row.get("actor_id") == expected_actor["actor_id"]
        and row.get("actor_type") == expected_actor["actor_type"]
        and row.get("bypass_mode") == expected_actor["bypass_mode"]
        for row in bypass if isinstance(row, dict)
    ):
        problems.append("CI ruleset lacks the authorized user with pull_request-only bypass")
    status_rules = [row for row in value.get("rules", []) if isinstance(row, dict) and row.get("type") == "required_status_checks"]
    if len(status_rules) != 1:
        problems.append("CI ruleset must contain exactly one required_status_checks rule")
    else:
        params = status_rules[0].get("parameters") or {}
        if params.get("strict_required_status_checks_policy") is not True:
            problems.append("CI status checks are not strict/up-to-date")
        actual = {row.get("context") for row in params.get("required_status_checks", []) if isinstance(row, dict)}
        missing = sorted(set(checks) - {item for item in actual if isinstance(item, str)})
        if missing:
            problems.append("CI ruleset missing checks: " + ", ".join(missing))
    return problems


def resolve_user_id(token: str, explicit: int | None) -> int:
    if explicit is not None:
        return explicit
    user = request("GET", "https://api.github.com/user", token)
    if not isinstance(user, dict) or not isinstance(user.get("id"), int):
        raise RuntimeError("cannot resolve authenticated GitHub user ID; use --bypass-user-id")
    return int(user["id"])


def locate(base_url: str, token: str, name: str) -> dict | None:
    matches = [row for row in list_rulesets(base_url, token) if row.get("name") == name]
    if len(matches) > 1:
        raise RuntimeError(f"multiple rulesets named {name}")
    if not matches:
        return None
    return full_ruleset(base_url, token, int(matches[0]["id"]))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY)
    parser.add_argument("--branch", default=DEFAULT_BRANCH)
    parser.add_argument("--token-env", default="GITHUB_ADMIN_TOKEN")
    parser.add_argument("--check", action="append", dest="checks")
    parser.add_argument("--bypass-user-id", type=int)
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--keep-classic-protection", action="store_true")
    args = parser.parse_args(argv)

    token = os.environ.get(args.token_env)
    if not token:
        print(f"[BLOCK] environment variable {args.token_env} is not set", file=sys.stderr)
        return 2
    if "/" not in args.repository:
        print("[BLOCK] --repository must be OWNER/REPO", file=sys.stderr)
        return 2

    owner, repo = args.repository.split("/", 1)
    base_url = f"https://api.github.com/repos/{owner}/{repo}"
    checks = args.checks or DEFAULT_CHECKS

    try:
        user_id = resolve_user_id(token, args.bypass_user_id)
        if args.verify_only:
            core = locate(base_url, token, CORE_NAME)
            ci = locate(base_url, token, CI_NAME)
        else:
            core = upsert(base_url, token, core_payload(args.branch))
            ci = upsert(base_url, token, ci_payload(args.branch, checks, user_id))

        problems: list[str] = []
        if core is None:
            problems.append(f"missing ruleset {CORE_NAME}")
        else:
            problems.extend(verify_core(core, args.branch))
        if ci is None:
            problems.append(f"missing ruleset {CI_NAME}")
        else:
            problems.extend(verify_ci(ci, args.branch, checks, user_id))
        if problems:
            for problem in problems:
                print(f"[BLOCK] {problem}", file=sys.stderr)
            return 2

        if not args.verify_only and not args.keep_classic_protection:
            protection_url = f"{base_url}/branches/{args.branch}/protection"
            try:
                request("DELETE", protection_url, token)
            except RuntimeError as exc:
                if "GitHub API 404" not in str(exc):
                    raise

        core = locate(base_url, token, CORE_NAME)
        ci = locate(base_url, token, CI_NAME)
        final_problems = ([] if core else [f"missing ruleset {CORE_NAME}"]) + ([] if ci else [f"missing ruleset {CI_NAME}"])
        if core:
            final_problems.extend(verify_core(core, args.branch))
        if ci:
            final_problems.extend(verify_ci(ci, args.branch, checks, user_id))
        if final_problems:
            for problem in final_problems:
                print(f"[BLOCK] {problem}", file=sys.stderr)
            return 2
    except (OSError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"[BLOCK] {exc}", file=sys.stderr)
        return 2

    print(f"[OK] {args.repository}:{args.branch} uses layered Foundation Rulesets")
    print(f"[OK] core safety has no bypass: {CORE_NAME}")
    print(f"[OK] CI gates allow user {user_id} bypass only through pull requests: {CI_NAME}")
    print("[OK] required checks: " + ", ".join(checks))
    if args.keep_classic_protection:
        print("[INFO] legacy classic branch protection was intentionally retained")
    elif not args.verify_only:
        print("[OK] legacy classic branch protection removed after Ruleset verification")
    return 0


if __name__ == "__main__":
    sys.exit(main())
