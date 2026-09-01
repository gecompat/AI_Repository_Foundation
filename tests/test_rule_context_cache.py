from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE_TOOL_DIR = ROOT / "foundation" / "capabilities" / "rule-context-cache"
sys.path.insert(0, str(CACHE_TOOL_DIR))

import rule_context_cache as cache  # noqa: E402


TEST_TMP_ROOT = Path(os.environ.get("FOUNDATION_TEST_TMP", tempfile.gettempdir()))


class RuleContextFixture:
    def __init__(self) -> None:
        TEST_TMP_ROOT.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="foundation-rule-cache-", dir=TEST_TMP_ROOT)
        self.base = Path(self.temporary.name)
        self.repository = self.base / "repository"
        self.cache_dir = self.base / "cache"
        self.codex_home = self.base / "codex-home"
        self.repository.mkdir()
        self.codex_home.mkdir()
        self._git("init", "-b", "main")
        self._git("config", "user.name", "Rule Cache Tests")
        self._git("config", "user.email", "rule-cache@example.invalid")
        self._git("config", "core.autocrlf", "false")
        self.write(
            "AGENTS.md",
            "# Root instructions\n\nRead `.ai/repo_map.yaml`.\n",
        )
        self.write(
            ".ai/repo_map.yaml",
            "schema_version: 1\nauthority:\n  authoritative:\n    - rules/A.md\n    - rules/C.md\n",
        )
        self.write("rules/A.md", "# Rule A\n\nDepends on [Rule B](B.md).\n")
        self.write("rules/B.md", "# Rule B\n\nStable rule.\n")
        self.write("rules/C.md", "# Rule C\n\nIndependent rule.\n")
        self.write(".gitignore", ".local/\n")
        (self.repository / "sub").mkdir()
        self.write("sub/.keep", "tracked\n")
        self._git("add", ".")
        self._git("commit", "-m", "Initial rule context")

    def close(self) -> None:
        self.temporary.cleanup()

    def _git(self, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(cwd or self.repository), *args],
            text=True,
            capture_output=True,
            check=True,
        )

    def write(self, relative: str, text: str) -> Path:
        path = self.repository / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
        return path

    def options(
        self,
        *,
        cwd: Path | None = None,
        include_global: bool = False,
        max_bytes: int = cache.DEFAULT_PROJECT_DOC_MAX_BYTES,
        fallbacks: tuple[str, ...] = (),
    ) -> cache.DiscoveryOptions:
        return cache.make_options(
            self.repository,
            cwd or self.repository,
            codex_home=self.codex_home,
            include_global=include_global,
            fallback_filenames=fallbacks,
            project_doc_max_bytes=max_bytes,
        )

    def record(self, options: cache.DiscoveryOptions | None = None) -> dict:
        payload = cache.record_cache(options or self.options(), self.cache_dir)
        if payload["status"] != "CACHE_HIT":
            raise AssertionError(payload)
        return payload

    def record_path(self, options: cache.DiscoveryOptions | None = None) -> Path:
        snapshot = cache.capture_snapshot(options or self.options())
        return cache.cache_record_path(self.cache_dir, snapshot.record)


class RuleContextCacheTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = RuleContextFixture()

    def tearDown(self) -> None:
        self.fixture.close()

    def test_unchanged_rules_are_cache_hit_without_analysis_rereads(self) -> None:
        self.fixture.record()
        payload = cache.check_cache(self.fixture.options(), self.fixture.cache_dir)

        self.assertEqual(payload["status"], "CACHE_HIT")
        self.assertEqual(payload["reanalyze"], [])
        self.assertEqual(payload["analysis_full_read_count"], 0)
        self.assertIn("rules/A.md", payload["reuse"])
        self.assertIn("rules/B.md", payload["reuse"])
        self.assertIn("CACHE_RECORD_VALID", payload["reason_codes"])

    def test_changed_rule_invalidates_only_itself_and_transitive_dependents(self) -> None:
        self.fixture.record()
        self.fixture.write("rules/B.md", "# Rule B\n\nChanged rule.\n")

        payload = cache.check_cache(self.fixture.options(), self.fixture.cache_dir)

        self.assertEqual(payload["status"], "PARTIAL_INVALIDATION")
        self.assertEqual(
            set(payload["reanalyze"]),
            {"rules/B.md", "rules/A.md", ".ai/repo_map.yaml", "AGENTS.md"},
        )
        self.assertIn("rules/C.md", payload["reuse"])
        self.assertIn("TRANSITIVE_DEPENDENT_INVALIDATED", payload["reason_codes"])

    def test_root_agents_change_forces_full_cache_miss(self) -> None:
        self.fixture.record()
        self.fixture.write("AGENTS.md", "# Changed root instructions\n\nRead `.ai/repo_map.yaml`.\n")

        payload = cache.check_cache(self.fixture.options(), self.fixture.cache_dir)

        self.assertEqual(payload["status"], "CACHE_MISS")
        self.assertIn("INSTRUCTION_CONTENT_OR_GIT_STATE_CHANGED", payload["reason_codes"])
        self.assertEqual(set(payload["reanalyze"]), set(payload["analysis_keys"]))

    def test_new_untracked_scoped_override_is_discovered(self) -> None:
        options = self.fixture.options(cwd=self.fixture.repository / "sub")
        self.fixture.record(options)
        self.fixture.write("sub/AGENTS.override.md", "# Scoped override\n")

        payload = cache.check_cache(options, self.fixture.cache_dir)

        self.assertEqual(payload["status"], "CACHE_MISS")
        self.assertIn("INSTRUCTION_CHAIN_CHANGED", payload["reason_codes"])
        self.assertEqual(payload["instruction_chain"], ["AGENTS.md", "sub/AGENTS.override.md"])

    def test_working_directory_change_creates_unknown_scope(self) -> None:
        self.fixture.record(self.fixture.options(cwd=self.fixture.repository))

        payload = cache.check_cache(
            self.fixture.options(cwd=self.fixture.repository / "sub"),
            self.fixture.cache_dir,
        )

        self.assertEqual(payload["status"], "CACHE_MISS")
        self.assertIn("SCOPE_UNKNOWN", payload["reason_codes"])
        self.assertEqual(payload["cwd"], "sub")

    def test_staged_and_unstaged_rule_changes_are_detected(self) -> None:
        self.fixture.record()
        self.fixture.write("rules/B.md", "# Rule B\n\nUnstaged change.\n")
        unstaged = cache.check_cache(self.fixture.options(), self.fixture.cache_dir)
        self.assertEqual(unstaged["status"], "PARTIAL_INVALIDATION")
        self.assertIn("RULE_CONTENT_CHANGED", unstaged["reason_codes"])

        self.fixture._git("add", "rules/B.md")
        staged = cache.check_cache(self.fixture.options(), self.fixture.cache_dir)
        self.assertEqual(staged["status"], "PARTIAL_INVALIDATION")
        self.assertIn("RULE_GIT_STATE_CHANGED", staged["reason_codes"])

    def test_new_untracked_rule_from_repo_map_is_a_full_miss(self) -> None:
        self.fixture.record()
        self.fixture.write(
            ".ai/repo_map.yaml",
            "schema_version: 1\nauthority:\n  authoritative:\n    - rules/A.md\n    - rules/C.md\n    - rules/New.md\n",
        )
        self.fixture.write("rules/New.md", "# New untracked rule\n")

        payload = cache.check_cache(self.fixture.options(), self.fixture.cache_dir)

        self.assertEqual(payload["status"], "CACHE_MISS")
        self.assertIn("SOURCE_ADDED", payload["reason_codes"])
        self.assertIn("rules/New.md", payload["reanalyze"])

    def test_rename_is_detected_as_full_miss(self) -> None:
        self.fixture.record()
        (self.fixture.repository / "rules/B.md").rename(self.fixture.repository / "rules/D.md")
        self.fixture.write("rules/A.md", "# Rule A\n\nDepends on [Rule D](D.md).\n")

        payload = cache.check_cache(self.fixture.options(), self.fixture.cache_dir)

        self.assertEqual(payload["status"], "CACHE_MISS")
        self.assertIn("SOURCE_RENAMED_OR_MOVED", payload["reason_codes"])

    def test_delete_or_unresolved_reference_is_fail_closed(self) -> None:
        self.fixture.record()
        (self.fixture.repository / "rules/B.md").unlink()

        payload = cache.check_cache(self.fixture.options(), self.fixture.cache_dir)

        self.assertEqual(payload["status"], "CACHE_MISS")
        self.assertIn("UNRESOLVED_REFERENCE", payload["reason_codes"])

    def test_corrupt_schema_and_generator_records_are_cache_misses(self) -> None:
        self.fixture.record()
        record_path = self.fixture.record_path()
        record_path.write_bytes(b"{broken")
        corrupt = cache.check_cache(self.fixture.options(), self.fixture.cache_dir)
        self.assertEqual(corrupt["status"], "CACHE_MISS")
        self.assertIn("CACHE_RECORD_CORRUPT", corrupt["reason_codes"])

        self.fixture.record()
        record = json.loads(record_path.read_text(encoding="utf-8"))
        record["schema_version"] = 99
        record_path.write_text(json.dumps(record), encoding="utf-8")
        schema = cache.check_cache(self.fixture.options(), self.fixture.cache_dir)
        self.assertIn("CACHE_SCHEMA_CHANGED", schema["reason_codes"])

        self.fixture.record()
        record = json.loads(record_path.read_text(encoding="utf-8"))
        record["generator"]["version"] = "2.0.0"
        record_path.write_text(json.dumps(record), encoding="utf-8")
        generator = cache.check_cache(self.fixture.options(), self.fixture.cache_dir)
        self.assertIn("CACHE_GENERATOR_CHANGED", generator["reason_codes"])

        self.fixture.record()
        record = json.loads(record_path.read_text(encoding="utf-8"))
        del record["scope"]["cwd"]
        record["record_digest"] = cache._sha256_json(  # noqa: SLF001 - deliberate malformed fixture
            {key: value for key, value in record.items() if key != "record_digest"}
        )
        record_path.write_text(json.dumps(record), encoding="utf-8")
        incomplete = cache.check_cache(self.fixture.options(), self.fixture.cache_dir)
        self.assertEqual(incomplete["status"], "CACHE_MISS")
        self.assertIn("CACHE_RECORD_CORRUPT", incomplete["reason_codes"])

    def test_repository_and_worktree_record_keys_do_not_collide(self) -> None:
        first = cache.capture_snapshot(self.fixture.options()).record
        other_repository = self.fixture.base / "other-repository"
        shutil.copytree(self.fixture.repository, other_repository, ignore=shutil.ignore_patterns(".git"))
        subprocess.run(["git", "-C", str(other_repository), "init", "-b", "main"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(other_repository), "config", "user.name", "Other"], check=True)
        subprocess.run(["git", "-C", str(other_repository), "config", "user.email", "other@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(other_repository), "add", "."], check=True)
        subprocess.run(["git", "-C", str(other_repository), "commit", "-m", "Other repository"], check=True, capture_output=True)
        other_options = cache.make_options(
            other_repository,
            other_repository,
            include_global=False,
            fallback_filenames=(),
            project_doc_max_bytes=cache.DEFAULT_PROJECT_DOC_MAX_BYTES,
        )
        second = cache.capture_snapshot(other_options).record
        self.assertNotEqual(cache.cache_record_key(first), cache.cache_record_key(second))

        linked = self.fixture.base / "linked-worktree"
        self.fixture._git("worktree", "add", "-b", "linked", str(linked))
        linked_options = cache.make_options(
            linked,
            linked,
            include_global=False,
            fallback_filenames=(),
            project_doc_max_bytes=cache.DEFAULT_PROJECT_DOC_MAX_BYTES,
        )
        linked_record = cache.capture_snapshot(linked_options).record
        self.assertEqual(first["repository"]["repository_id"], linked_record["repository"]["repository_id"])
        self.assertNotEqual(first["repository"]["worktree_id"], linked_record["repository"]["worktree_id"])
        self.assertNotEqual(cache.cache_record_key(first), cache.cache_record_key(linked_record))

    def test_utf8_lf_crlf_only_difference_remains_cache_hit(self) -> None:
        self.fixture.record()
        source = self.fixture.repository / "rules/B.md"
        source.write_bytes(source.read_bytes().replace(b"\n", b"\r\n"))

        payload = cache.check_cache(self.fixture.options(), self.fixture.cache_dir)

        self.assertEqual(payload["status"], "CACHE_HIT")
        self.assertIn("EOL_REPRESENTATION_EQUIVALENT", payload["reason_codes"])

    def test_content_encoding_lone_cr_and_final_newline_changes_are_visible(self) -> None:
        self.fixture.record()
        source = self.fixture.repository / "rules/B.md"

        variants = {
            "content": b"# Rule B\n\nDifferent meaning.\n",
            "encoding": "# Rule B\n\nCaf\u00e9.\n".encode("latin-1"),
            "lone_cr": b"# Rule B\rStable rule.\n",
            "final_newline": b"# Rule B\n\nStable rule.",
        }
        for name, data in variants.items():
            with self.subTest(name=name):
                source.write_bytes(data)
                payload = cache.check_cache(self.fixture.options(), self.fixture.cache_dir)
                self.assertEqual(payload["status"], "PARTIAL_INVALIDATION")
                self.assertIn("RULE_CONTENT_CHANGED", payload["reason_codes"])

    def test_repo_map_and_discovery_link_changes_are_detected(self) -> None:
        self.fixture.record()
        self.fixture.write(
            ".ai/repo_map.yaml",
            "schema_version: 1\nauthority:\n  authoritative:\n    - rules/C.md\n    - rules/A.md\n",
        )
        repo_map_change = cache.check_cache(self.fixture.options(), self.fixture.cache_dir)
        self.assertEqual(repo_map_change["status"], "PARTIAL_INVALIDATION")
        self.assertIn(".ai/repo_map.yaml", repo_map_change["reanalyze"])
        self.assertIn("AGENTS.md", repo_map_change["reanalyze"])
        self.assertIn("rules/B.md", repo_map_change["reuse"])

        self.fixture.write("rules/A.md", "# Rule A\n\nDepends on [Rule C](C.md).\n")
        link_change = cache.check_cache(self.fixture.options(), self.fixture.cache_dir)
        self.assertEqual(link_change["status"], "CACHE_MISS")
        self.assertIn("DEPENDENCY_GRAPH_CHANGED", link_change["reason_codes"])

    def test_record_contains_no_source_secret_or_absolute_host_path(self) -> None:
        secret = "s3cr3t-value-that-must-not-appear"
        self.fixture._git(
            "remote",
            "add",
            "origin",
            f"https://cache-user:{secret}@example.invalid/example/repository.git",
        )
        self.fixture.write("rules/B.md", f"# Rule B\n\nCredential material: {secret}\n")
        self.fixture._git("add", "rules/B.md")
        self.fixture._git("commit", "-m", "Sensitive synthetic rule")
        self.fixture.record()

        serialized = self.fixture.record_path().read_text(encoding="utf-8")
        self.assertNotIn(secret, serialized)
        self.assertNotIn(str(self.fixture.repository), serialized)
        self.assertNotRegex(serialized, r"[A-Za-z]:\\Users\\")
        self.assertNotIn("Credential material", serialized)

    def test_global_and_scoped_instruction_order_is_exact(self) -> None:
        (self.fixture.codex_home / "AGENTS.md").write_bytes(b"# Global\n")
        self.fixture.write("sub/AGENTS.override.md", "# Scoped\n")
        options = self.fixture.options(
            cwd=self.fixture.repository / "sub",
            include_global=True,
        )

        snapshot = cache.capture_snapshot(options)

        self.assertTrue(snapshot.complete, snapshot.reason_codes)
        self.assertEqual(
            snapshot.record["scope"]["instruction_chain"],
            ["@global/AGENTS.md", "AGENTS.md", "sub/AGENTS.override.md"],
        )

    def test_schema_contract_matches_a_generated_record(self) -> None:
        schema = json.loads(
            (ROOT / "foundation" / "schemas" / "rule-context-cache.schema.json").read_text(
                encoding="utf-8"
            )
        )
        record = cache.capture_snapshot(self.fixture.options()).record

        self.assertEqual(schema["properties"]["schema_version"]["const"], cache.SCHEMA_VERSION)
        self.assertEqual(schema["properties"]["contract"]["const"], cache.CONTRACT)
        self.assertEqual(
            schema["properties"]["normalization_policy"]["const"],
            cache.NORMALIZATION_POLICY,
        )
        self.assertEqual(set(schema["required"]), set(record))
        self.assertEqual(cache._validate_record_shape(record), (True, None))  # noqa: SLF001

        pending = [schema]
        while pending:
            value = pending.pop()
            if isinstance(value, dict):
                if isinstance(value.get("pattern"), str):
                    re.compile(value["pattern"])
                pending.extend(value.values())
            elif isinstance(value, list):
                pending.extend(value)

    def test_discovery_limit_change_and_overflow_are_full_misses(self) -> None:
        self.fixture.record()
        changed_config = cache.check_cache(
            self.fixture.options(max_bytes=64 * 1024),
            self.fixture.cache_dir,
        )
        self.assertEqual(changed_config["status"], "CACHE_MISS")
        self.assertIn("DISCOVERY_CONFIGURATION_CHANGED", changed_config["reason_codes"])

        overflow = cache.check_cache(
            self.fixture.options(max_bytes=4),
            self.fixture.cache_dir,
        )
        self.assertEqual(overflow["status"], "CACHE_MISS")
        self.assertIn("DISCOVERY_SIZE_LIMIT_EXCEEDED", overflow["reason_codes"])

    def test_check_is_read_only_and_record_is_atomic_and_lock_bounded(self) -> None:
        unused_cache = self.fixture.base / "unused-cache"
        payload = cache.check_cache(self.fixture.options(), unused_cache)
        self.assertEqual(payload["status"], "CACHE_MISS")
        self.assertFalse(unused_cache.exists())

        recorded = self.fixture.record()
        record_path = self.fixture.record_path()
        self.assertTrue(record_path.is_file())
        self.assertFalse(list(record_path.parent.glob("*.tmp")))
        self.assertFalse(list(record_path.parent.glob("*.lock")))
        self.assertIn("CACHE_RECORD_WRITTEN", recorded["reason_codes"])

        lock_path = record_path.with_suffix(record_path.suffix + ".lock")
        lock_path.touch()
        with self.assertRaises(cache.CacheError):
            cache.record_cache(self.fixture.options(), self.fixture.cache_dir, lock_timeout_seconds=0)
        lock_path.unlink()

    def test_record_rejects_versioned_cache_destination(self) -> None:
        with self.assertRaises(cache.CacheError):
            cache.check_cache(self.fixture.options(), self.fixture.repository / "cache")
        with self.assertRaises(cache.CacheError):
            cache.record_cache(self.fixture.options(), self.fixture.repository / "cache")
        with self.assertRaises(cache.CacheError):
            cache.record_cache(self.fixture.options(), self.fixture.repository / ".git" / "rule-cache")

        payload = cache.record_cache(
            self.fixture.options(),
            self.fixture.repository / ".local" / "rule-context-cache",
        )
        self.assertEqual(payload["status"], "CACHE_HIT")


if __name__ == "__main__":
    unittest.main()
