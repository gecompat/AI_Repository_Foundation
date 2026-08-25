#!/usr/bin/env python3
"""Configure and verify the Foundation source repository's GitHub branch protection.

Requires a token with repository Administration: write. The token is read only from
an environment variable and is never accepted on the command line.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API_VERSION = "2026-03-10"
DEFAULT_REPOSITORY = "gecompat/AI_Repository_Foundation"
DEFAULT_BRANCH = "main"
DEFAULT_CHECKS = ["validate", "registry-integrity"]


def request(method: str, url: str, token: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("X-GitHub-Api-Version", API_VERSION)
    req.add_header("User-Agent", "AI-Repository-Foundation-branch-protection")
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API {exc.code}: {detail}") from exc


def desired_payload(checks: list[str]) -> dict:
    return {
        "required_status_checks": {
            "strict": True,
            "checks": [{"context": name} for name in checks],
        },
        "enforce_admins": True,
        "required_pull_request_reviews": None,
        "restrictions": None,
        "required_linear_history": True,
        "allow_force_pushes": False,
        "allow_deletions": False,
    }


def verify(protection: dict, checks: list[str]) -> list[str]:
    problems: list[str] = []
    status = protection.get("required_status_checks") or {}
    if status.get("strict") is not True:
        problems.append("required status checks are not strict/up-to-date")
    actual_contexts = set(status.get("contexts") or [])
    actual_contexts.update(
        row.get("context") for row in status.get("checks") or [] if isinstance(row, dict)
    )
    missing = sorted(set(checks) - {value for value in actual_contexts if isinstance(value, str)})
    if missing:
        problems.append("missing required checks: " + ", ".join(missing))
    if (protection.get("enforce_admins") or {}).get("enabled") is not True:
        problems.append("administrator enforcement is disabled")
    if (protection.get("required_linear_history") or {}).get("enabled") is not True:
        problems.append("required linear history is disabled")
    if (protection.get("allow_force_pushes") or {}).get("enabled") is True:
        problems.append("force pushes are allowed")
    if (protection.get("allow_deletions") or {}).get("enabled") is True:
        problems.append("branch deletion is allowed")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY)
    parser.add_argument("--branch", default=DEFAULT_BRANCH)
    parser.add_argument("--token-env", default="GITHUB_ADMIN_TOKEN")
    parser.add_argument("--check", action="append", dest="checks")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args(argv)

    token = os.environ.get(args.token_env)
    if not token:
        print(f"[BLOCK] environment variable {args.token_env} is not set", file=sys.stderr)
        return 2
    if "/" not in args.repository:
        print("[BLOCK] --repository must be OWNER/REPO", file=sys.stderr)
        return 2

    checks = args.checks or DEFAULT_CHECKS
    owner, repo = args.repository.split("/", 1)
    url = f"https://api.github.com/repos/{owner}/{repo}/branches/{args.branch}/protection"

    try:
        if not args.verify_only:
            request("PUT", url, token, desired_payload(checks))
        protection = request("GET", url, token)
        problems = verify(protection, checks)
    except (OSError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"[BLOCK] {exc}", file=sys.stderr)
        return 2

    if problems:
        for problem in problems:
            print(f"[BLOCK] {problem}", file=sys.stderr)
        return 2

    print(f"[OK] {args.repository}:{args.branch} protection matches Foundation source requirements")
    print("[OK] required checks: " + ", ".join(checks))
    return 0


if __name__ == "__main__":
    sys.exit(main())
