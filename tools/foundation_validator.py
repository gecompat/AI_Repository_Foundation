#!/usr/bin/env python3
"""Dependency-free validator for Foundation integrity in this project or an installed target ruleset."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from content_equivalence import files_equivalent

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "foundation" / "manifest.json"

PROJECT_REQUIRED = [
    "README.md", "AGENTS.md", "LICENSE", ".gitignore", "CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md",
    ".ai/PROJECT_CONTEXT.md", ".ai/PROJECT_RULES.md", ".ai/WORKING_RULES.md",
    ".ai/MODEL_ROUTING_POLICY.md", ".ai/VALIDATION_POLICY.md", ".ai/FOUNDATION.md",
    ".ai/PROJECT_STATUS.md", ".ai/HANDOVER.md", ".ai/ROADMAP.md", ".ai/BACKLOG.md", ".ai/repo_map.yaml",
    ".ai/identity/registry.json",
    "Documentation/Architecture/OVERVIEW.md", "Documentation/Architecture/DECISIONS.md",
    "Documentation/Standards/DATA_PRIVACY_AND_CONFIDENTIALITY.md",
    "Documentation/Standards/SECURITY_AND_SAFE_OPERATIONS.md",
    "Documentation/Standards/DOCUMENTATION_POLICY.md",
    "Documentation/Standards/THIRD_PARTY_AND_LICENSING.md",
    "Documentation/Standards/SOURCE_AND_EVIDENCE_POLICY.md",
    "Documentation/Standards/DEPENDENCY_POLICY.md",
    "Documentation/Standards/SEMANTIC_INTEGRATION_POLICY.md",
    "Documentation/Standards/PERSISTENT_IDENTITY_POLICY.md",
    "Documentation/Standards/ARTIFACT_REGISTRATION_POLICY.md",
    "Documentation/Standards/CENTRAL_ARTIFACT_REGISTRY_POLICY.md",
    "Documentation/Standards/UPGRADE_APPLICABILITY_POLICY.md",
    "Documentation/Standards/RULE_CONTEXT_CACHE_POLICY.md",
    "Documentation/Quality/KNOWN_LIMITATIONS.md",
    "foundation/manifest.json", "foundation/feature_catalog.json", "foundation/AI_TRANSFER.md", "foundation/AGENTS.template.md",
    "foundation/FOUNDATION_RULESET.template.md", "foundation/repo_map.template.yaml",
    "foundation/AI_REPOSITORY_FOUNDATION_NOTICE.md",
    "foundation/schemas/artifact-record.schema.json",
    "foundation/schemas/artifact-registry.schema.json",
    "foundation/schemas/artifact-registry-v2.schema.json",
    "foundation/schemas/artifact-registration-request.schema.json",
    "foundation/schemas/feature-catalog.schema.json",
    "foundation/schemas/upgrade-assessment.schema.json",
    "foundation/schemas/rule-context-cache.schema.json",
    "tools/content_equivalence.py", "tools/install_foundation.py", "tools/foundation_validator.py",
]

FORBIDDEN_TARGETS = {"README.md", "LICENSE", "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md", ".gitignore"}
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(?:api[_-]?key|token|password)\s*[:=]\s*['\"][^'\"]{8,}"),
]
ABSOLUTE_PATHS = [re.compile(r"[A-Za-z]:\\Users\\"), re.compile(r"/home/[^/\s]+/")]
CONFLICT = re.compile(r"^(?:<<<<<<<|=======|>>>>>>>)", re.MULTILINE)
PLACEHOLDER = re.compile(r"\b(?:CHANGEME|TODO_TEMPLATE|TBD_TEMPLATE)\b")

VALIDATION_CONTRACT = {
    "foundation_validator_scope": "FOUNDATION_INTEGRITY",
    "project_semantic_authority": "target_repository",
    "runtime_empirical_authority": "target_repository",
    "completion": "impact_based_combination",
    "foundation_green_does_not_imply_project_green": True,
    "foundation_reserved_statuses": ["not executed", "pending manual validation", "validated"],
    "target_status_extensions_allowed": True,
    "reserved_statuses_may_not_be_redefined": True,
}

INTEGRATION_COMPATIBILITY_CLASSES = [
    "EQUIVALENT",
    "PROJECT_STRONGER",
    "PROJECT_SELECTABLE_OVERRIDE",
    "COMPLEMENTARY",
    "DUPLICATE_GOVERNANCE",
    "FOUNDATION_REQUIRED_CONFLICT",
    "TARGET_INTERNAL_CONFLICT",
    "ORPHANED_AUTHORITY",
    "ADAPTER_GOVERNANCE_MISPLACED",
]
INTEGRATION_CONTRACT = {
    "policy_source": "Documentation/Standards/SEMANTIC_INTEGRATION_POLICY.md",
    "policy_target": ".ai/foundation/SEMANTIC_INTEGRATION_POLICY.md",
    "root_entrypoint": "AGENTS.md",
    "project_governance_must_be_transitively_discoverable": True,
    "stricter_project_rules": "compatible",
    "existing_project_rule_labels_required": False,
    "adapter_governance_migration": "preserve_then_rehome_then_thin",
    "project_repo_map_behavior": "preserve_and_optionally_bridge",
    "orphaned_authority_is_integration_defect": True,
}
IDENTITY_CONTRACT = {
    "policy_source": "Documentation/Standards/PERSISTENT_IDENTITY_POLICY.md",
    "policy_target": ".ai/foundation/PERSISTENT_IDENTITY_POLICY.md",
    "required_invariants": [
        "stable_no_reuse",
        "no_silent_rename_or_reinterpretation",
        "legacy_identifier_preservation",
        "identity_separate_from_mutable_classification",
        "relationships_explicit",
        "revision_identity_separate",
        "identifiers_are_not_authorization",
    ],
    "default_machine_identifier": "rfc9562_uuidv7_as_urn_uuid",
    "compatible_uuid_profiles": ["uuidv7", "uuidv4"],
    "default_human_reference": "flat_typed_project_local",
    "default_human_reference_pattern": "<PREFIX>-<SEQUENCE>",
    "default_prefixes": ["CAP", "REQ", "WI", "DEC", "GATE", "RISK", "EXP", "OPS", "INC", "REL", "TEST"],
    "prefix_meaning_reuse": "prohibited",
    "hierarchy_and_status": "metadata_not_canonical_identity",
    "external_references": "aliases_or_locators_not_canonical_by_default",
    "content_hash_scope": "immutable_revision_or_content",
    "existing_project_default_mode": "PRESERVE",
    "new_project_default_mode": "FOUNDATION_DEFAULT",
    "adoption_modes": ["PRESERVE", "ADOPT_FORWARD", "MIGRATE_EXPLICIT"],
    "migration_requires_explicit_decision": True,
    "unknown_existing_project_choice": "PRESERVE",
}
REGISTRATION_CONTRACT = {
    "policy_source": "Documentation/Standards/ARTIFACT_REGISTRATION_POLICY.md",
    "policy_target": ".ai/foundation/ARTIFACT_REGISTRATION_POLICY.md",
    "schema_targets": [
        ".ai/foundation/schemas/artifact-record.schema.json",
        ".ai/foundation/schemas/artifact-registry.schema.json",
        ".ai/foundation/schemas/artifact-registry-v2.schema.json",
        ".ai/foundation/schemas/artifact-registration-request.schema.json",
    ],
    "authority_scope": "one_registration_authority_per_overlapping_identifier_scope",
    "same_authority_for_humans_and_ai": True,
    "implementation_language": "project_selectable",
    "python_required": False,
    "powershell_supported": True,
    "allocation_modes": ["DIRECT", "DEFERRED"],
    "direct_requires_serialized_or_equivalent_unique_allocation": True,
    "deferred_uid_is_final_before_human_reference": True,
    "final_human_reference_must_be_authority_allocated": True,
    "reference_clients": "optional_capability",
    "reference_clients_must_match_shared_contract": True,
    "default_registry_profile": "foundation-artifact-registry/v2",
    "compatible_registry_profiles": ["foundation-artifact-registry/v1", "foundation-artifact-registry/v2"],
}
CENTRAL_REGISTRY_CONTRACT = {
    "policy_source": "Documentation/Standards/CENTRAL_ARTIFACT_REGISTRY_POLICY.md",
    "policy_target": ".ai/foundation/CENTRAL_ARTIFACT_REGISTRY_POLICY.md",
    "schema_targets": [".ai/foundation/schemas/artifact-registry-v2.schema.json"],
    "profile": "foundation-artifact-registry/v2",
    "complete_records_in_single_registry": True,
    "human_reference_is_object_key": True,
    "persist_next_sequence": False,
    "allocation_derivation": "max_existing_sequence_plus_one",
    "persist_global_registry_revision": False,
    "git_revision_is_concurrency_token": True,
    "object_level_three_way_merge_required": True,
    "git_merge_result_must_equal_semantic_merge": True,
    "cross_pr_preflight_recommended": True,
    "generated_views_supported": True,
    "legacy_profile": "foundation-artifact-registry/v1",
}
RULE_CONTEXT_CACHE_CONTRACT = {
    "policy_source": "Documentation/Standards/RULE_CONTEXT_CACHE_POLICY.md",
    "policy_target": ".ai/foundation/RULE_CONTEXT_CACHE_POLICY.md",
    "schema_targets": [".ai/foundation/schemas/rule-context-cache.schema.json"],
    "profile": "foundation-rule-context-cache/v1",
    "native_instruction_discovery_per_run": True,
    "repository_files_are_source_of_truth": True,
    "statuses": ["CACHE_HIT", "PARTIAL_INVALIDATION", "CACHE_MISS"],
    "head_only_hit_prohibited": True,
    "dirty_worktree_inputs": ["staged", "unstaged", "untracked"],
    "partial_invalidation": "changed_sources_plus_transitive_dependents",
    "uncertainty_behavior": "CACHE_MISS",
    "semantic_analysis_storage": "session_local_by_analysis_key",
    "persistent_record_content": "fingerprints_and_dependency_metadata_only",
    "persistent_record_authority": "none",
    "persistent_record_version_control": "prohibited",
    "atomic_write_and_lock_required": True,
    "reference_implementation": "optional_capability",
}
MODEL_ROUTING_CONTRACT = {
    "foundation_tiers": ["LOCAL", "ECONOMICAL", "BALANCED", "FRONTIER"],
    "target_policy_may_be_more_detailed": True,
    "semantic_mapping_required_when_overlapping": True,
    "concrete_models_are_runtime_facts": True,
}
VALIDATION_MAP_MARKERS = [
    "label: FOUNDATION_INTEGRITY",
    "label: PROJECT_SEMANTIC",
    "label: RUNTIME_EMPIRICAL",
    "foundation_integrity_does_not_replace_project_validation: true",
    "target_extensions_allowed: true",
    "reserved_meanings_may_not_be_redefined: true",
]
INTEGRATION_MAP_MARKERS = [
    ".ai/foundation/SEMANTIC_INTEGRATION_POLICY.md",
    "project_governance_must_be_transitively_discoverable: true",
    "stricter_project_rules: compatible",
    "adapter_governance_migration: preserve_then_rehome_then_thin",
    "project_repo_map_behavior: preserve_and_optionally_bridge",
    "orphaned_authority_is_integration_defect: true",
    "semantic_mapping_when_overlapping: required",
]
IDENTITY_MAP_MARKERS = [
    ".ai/foundation/PERSISTENT_IDENTITY_POLICY.md",
    "default_machine_identifier: rfc9562_uuidv7_as_urn_uuid",
    "default_human_reference: flat_typed_project_local",
    "existing_project_default_mode: PRESERVE",
    "adoption_modes: PRESERVE_ADOPT_FORWARD_MIGRATE_EXPLICIT",
    "migration_requires_explicit_decision: true",
    "unknown_existing_project_choice: PRESERVE",
    "hierarchy_and_status: metadata_not_canonical_identity",
]
REGISTRATION_MAP_MARKERS = [
    ".ai/foundation/ARTIFACT_REGISTRATION_POLICY.md",
    "same_authority_for_humans_and_ai: true",
    "implementation_language: project_selectable",
    "python_required: false",
    "powershell_supported: true",
    "allocation_modes: DIRECT_DEFERRED",
    "default_registry_profile: foundation-artifact-registry/v2",
    "reference_clients: optional_capability",
]
CENTRAL_REGISTRY_MAP_MARKERS = [
    ".ai/foundation/CENTRAL_ARTIFACT_REGISTRY_POLICY.md",
    "profile: foundation-artifact-registry/v2",
    "persist_next_sequence: false",
    "allocation_derivation: max_existing_sequence_plus_one",
    "persist_global_registry_revision: false",
    "object_level_three_way_merge_required: true",
    "git_merge_result_must_equal_semantic_merge: true",
    "cross_pr_preflight_recommended: true",
]
RULE_CONTEXT_CACHE_MAP_MARKERS = [
    ".ai/foundation/RULE_CONTEXT_CACHE_POLICY.md",
    ".ai/foundation/schemas/rule-context-cache.schema.json",
    "native_instruction_discovery_per_run: required",
    "source_of_truth: repository_files",
    "statuses: CACHE_HIT_PARTIAL_INVALIDATION_CACHE_MISS",
    "head_only_hit: prohibited",
    "dirty_worktree_inputs: staged_unstaged_untracked",
    "partial_invalidation: changed_sources_plus_transitive_dependents",
    "uncertainty_behavior: CACHE_MISS",
    "semantic_analysis_storage: session_local_by_analysis_key",
    "persistent_record_version_control: prohibited",
    "atomic_write_and_lock: required",
    "optional_reference_capability: rule-context-cache",
]

results: list[dict] = []


def add(severity: str, code: str, path: str, message: str) -> None:
    results.append({"severity": severity, "code": code, "path": path, "message": message})


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def parse_selection(manifest: dict, raw: str, *, section: str, default_key: str) -> list[str]:
    if raw == "default":
        names = list(manifest.get(default_key, []))
    elif raw == "none":
        names = []
    else:
        names = [part.strip() for part in raw.split(",") if part.strip()]
    unknown = sorted(set(names) - set(manifest.get(section, {})))
    if unknown:
        raise ValueError(f"unknown {section.rstrip('s')}(s): {', '.join(unknown)}")
    return names


def selected_rows(manifest: dict, adapter_selection: str, capability_selection: str = "none") -> list[dict]:
    adapters = parse_selection(manifest, adapter_selection, section="adapters", default_key="default_adapters")
    capabilities = parse_selection(manifest, capability_selection, section="capabilities", default_key="default_capabilities")
    rows = list(manifest.get("core", []))
    for name in adapters:
        rows.extend(manifest["adapters"][name])
    for name in capabilities:
        rows.extend(manifest.get("capabilities", {})[name])
    return rows


def scan_text(path: Path, display: str) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return
    if CONFLICT.search(text):
        add("ERROR", "MERGE_CONFLICT", display, "merge conflict marker found")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            add("BLOCKING", "POSSIBLE_SECRET", display, "possible secret pattern found")
    for pattern in ABSOLUTE_PATHS:
        if pattern.search(text):
            add("WARNING", "ABSOLUTE_USER_PATH", display, "possible local user path found")
    if PLACEHOLDER.search(text):
        add("WARNING", "PLACEHOLDER", display, "unresolved template placeholder found")


def validate_markers(text: str, display: str, code: str, markers: list[str]) -> None:
    for marker in markers:
        if marker not in text:
            add("ERROR", code, display, f"required marker missing: {marker}")


def validate_manifest(manifest: dict) -> None:
    if manifest.get("schema_version") != 1:
        add("ERROR", "MANIFEST_SCHEMA", "foundation/manifest.json", "schema_version must be 1")
    if not manifest.get("ruleset_version"):
        add("ERROR", "MANIFEST_VERSION", "foundation/manifest.json", "ruleset_version is required")

    validation_contract = manifest.get("validation_contract")
    if not isinstance(validation_contract, dict):
        add("BLOCKING", "VALIDATION_CONTRACT", "foundation/manifest.json", "validation_contract is required")
    else:
        for key, expected in VALIDATION_CONTRACT.items():
            if validation_contract.get(key) != expected:
                add("ERROR", "VALIDATION_CONTRACT", "foundation/manifest.json", f"{key} must be {expected!r}")

    integration_contract = manifest.get("integration_contract")
    if not isinstance(integration_contract, dict):
        add("BLOCKING", "INTEGRATION_CONTRACT", "foundation/manifest.json", "integration_contract is required")
    else:
        for key, expected in INTEGRATION_CONTRACT.items():
            if integration_contract.get(key) != expected:
                add("ERROR", "INTEGRATION_CONTRACT", "foundation/manifest.json", f"{key} must be {expected!r}")
        if integration_contract.get("compatibility_classes") != INTEGRATION_COMPATIBILITY_CLASSES:
            add("ERROR", "INTEGRATION_CLASSES", "foundation/manifest.json", "compatibility_classes do not match the canonical ordered set")

    identity_contract = manifest.get("identity_contract")
    if not isinstance(identity_contract, dict):
        add("BLOCKING", "IDENTITY_CONTRACT", "foundation/manifest.json", "identity_contract is required")
    else:
        for key, expected in IDENTITY_CONTRACT.items():
            if identity_contract.get(key) != expected:
                add("ERROR", "IDENTITY_CONTRACT", "foundation/manifest.json", f"{key} must be {expected!r}")

    registration_contract = manifest.get("registration_contract")
    if not isinstance(registration_contract, dict):
        add("BLOCKING", "REGISTRATION_CONTRACT", "foundation/manifest.json", "registration_contract is required")
    else:
        for key, expected in REGISTRATION_CONTRACT.items():
            if registration_contract.get(key) != expected:
                add("ERROR", "REGISTRATION_CONTRACT", "foundation/manifest.json", f"{key} must be {expected!r}")

    central_registry_contract = manifest.get("central_registry_contract")
    if not isinstance(central_registry_contract, dict):
        add("BLOCKING", "CENTRAL_REGISTRY_CONTRACT", "foundation/manifest.json", "central_registry_contract is required")
    else:
        for key, expected in CENTRAL_REGISTRY_CONTRACT.items():
            if central_registry_contract.get(key) != expected:
                add("ERROR", "CENTRAL_REGISTRY_CONTRACT", "foundation/manifest.json", f"{key} must be {expected!r}")

    rule_context_cache_contract = manifest.get("rule_context_cache_contract")
    if not isinstance(rule_context_cache_contract, dict):
        add("BLOCKING", "RULE_CONTEXT_CACHE_CONTRACT", "foundation/manifest.json", "rule_context_cache_contract is required")
    else:
        for key, expected in RULE_CONTEXT_CACHE_CONTRACT.items():
            if rule_context_cache_contract.get(key) != expected:
                add("ERROR", "RULE_CONTEXT_CACHE_CONTRACT", "foundation/manifest.json", f"{key} must be {expected!r}")

    model_contract = manifest.get("model_routing_contract")
    if not isinstance(model_contract, dict):
        add("BLOCKING", "MODEL_ROUTING_CONTRACT", "foundation/manifest.json", "model_routing_contract is required")
    else:
        for key, expected in MODEL_ROUTING_CONTRACT.items():
            if model_contract.get(key) != expected:
                add("ERROR", "MODEL_ROUTING_CONTRACT", "foundation/manifest.json", f"{key} must be {expected!r}")

    targets: set[str] = set()
    rows = list(manifest.get("core", []))
    for section_name in ["adapters", "capabilities"]:
        for name, section_rows in manifest.get(section_name, {}).items():
            if not isinstance(section_rows, list):
                add("ERROR", "MODULE_SCHEMA", f"{section_name}:{name}", "module value must be a list")
                continue
            rows.extend(section_rows)

    for row in rows:
        source = row.get("source", "")
        target = row.get("target", "")
        if not source or not target:
            add("ERROR", "MANIFEST_ENTRY", "foundation/manifest.json", "source and target are required")
            continue
        if target in targets:
            add("ERROR", "DUPLICATE_TARGET", target, "manifest target occurs more than once")
        targets.add(target)
        if target in FORBIDDEN_TARGETS:
            add("BLOCKING", "PROJECT_ARTIFACT_TARGET", target, "Foundation project artifact must not be transferred")
        if target.startswith("Documentation/Architecture/") or target.startswith("Documentation/Quality/"):
            add("BLOCKING", "PROJECT_STATE_TARGET", target, "Foundation project architecture/quality state must not be transferred")
        source_path = ROOT / source
        if not source_path.is_file():
            add("ERROR", "MISSING_SOURCE", source, "manifest source does not exist")

    integration_rows = [row for row in rows if row.get("source") == INTEGRATION_CONTRACT["policy_source"] and row.get("target") == INTEGRATION_CONTRACT["policy_target"]]
    if len(integration_rows) != 1:
        add("BLOCKING", "INTEGRATION_POLICY_MAPPING", "foundation/manifest.json", "semantic integration policy must be transferred exactly once")

    identity_rows = [row for row in rows if row.get("source") == IDENTITY_CONTRACT["policy_source"] and row.get("target") == IDENTITY_CONTRACT["policy_target"]]
    if len(identity_rows) != 1:
        add("BLOCKING", "IDENTITY_POLICY_MAPPING", "foundation/manifest.json", "persistent identity policy must be transferred exactly once")

    registration_rows = [row for row in rows if row.get("source") == REGISTRATION_CONTRACT["policy_source"] and row.get("target") == REGISTRATION_CONTRACT["policy_target"]]
    if len(registration_rows) != 1:
        add("BLOCKING", "REGISTRATION_POLICY_MAPPING", "foundation/manifest.json", "artifact registration policy must be transferred exactly once")
    for schema_target in REGISTRATION_CONTRACT["schema_targets"]:
        if sum(row.get("target") == schema_target for row in rows) != 1:
            add("BLOCKING", "REGISTRATION_SCHEMA_MAPPING", schema_target, "registration schema must be transferred exactly once")

    central_rows = [row for row in rows if row.get("source") == CENTRAL_REGISTRY_CONTRACT["policy_source"] and row.get("target") == CENTRAL_REGISTRY_CONTRACT["policy_target"]]
    if len(central_rows) != 1:
        add("BLOCKING", "CENTRAL_REGISTRY_POLICY_MAPPING", "foundation/manifest.json", "central artifact registry policy must be transferred exactly once")
    for schema_target in CENTRAL_REGISTRY_CONTRACT["schema_targets"]:
        if sum(row.get("target") == schema_target for row in rows) != 1:
            add("BLOCKING", "CENTRAL_REGISTRY_SCHEMA_MAPPING", schema_target, "central registry schema must be transferred exactly once")

    cache_rows = [row for row in rows if row.get("source") == RULE_CONTEXT_CACHE_CONTRACT["policy_source"] and row.get("target") == RULE_CONTEXT_CACHE_CONTRACT["policy_target"]]
    if len(cache_rows) != 1:
        add("BLOCKING", "RULE_CONTEXT_CACHE_POLICY_MAPPING", "foundation/manifest.json", "rule-context cache policy must be transferred exactly once")
    for schema_target in RULE_CONTEXT_CACHE_CONTRACT["schema_targets"]:
        if sum(row.get("target") == schema_target for row in rows) != 1:
            add("BLOCKING", "RULE_CONTEXT_CACHE_SCHEMA_MAPPING", schema_target, "rule-context cache schema must be transferred exactly once")

    for adapter in manifest.get("default_adapters", []):
        if adapter not in manifest.get("adapters", {}):
            add("ERROR", "DEFAULT_ADAPTER", adapter, "default adapter is not defined")
    for capability in manifest.get("default_capabilities", []):
        if capability not in manifest.get("capabilities", {}):
            add("ERROR", "DEFAULT_CAPABILITY", capability, "default capability is not defined")

    attribution = manifest.get("attribution")
    if not isinstance(attribution, dict) or not attribution.get("required"):
        add("BLOCKING", "ATTRIBUTION_CONFIG", "foundation/manifest.json", "required attribution configuration is missing")
        return

    attr_source = attribution.get("source")
    attr_target = attribution.get("target")
    matching = [row for row in rows if row.get("kind") == "attribution"]
    if len(matching) != 1:
        add("BLOCKING", "ATTRIBUTION_ENTRY", "foundation/manifest.json", "exactly one attribution transfer entry is required")
        return
    row = matching[0]
    if row.get("source") != attr_source or row.get("target") != attr_target:
        add("BLOCKING", "ATTRIBUTION_MAPPING", "foundation/manifest.json", "attribution metadata and transfer entry do not match")
    if attr_target in FORBIDDEN_TARGETS or attr_target == "LICENSE":
        add("BLOCKING", "ATTRIBUTION_ROOT_LICENSE", str(attr_target), "Foundation attribution must not replace the target root license")

    source_path = ROOT / str(attr_source)
    license_path = ROOT / "LICENSE"
    if source_path.is_file() and license_path.is_file():
        required_notice = license_path.read_text(encoding="utf-8")
        if required_notice not in source_path.read_text(encoding="utf-8"):
            add("BLOCKING", "ATTRIBUTION_SOURCE", str(attr_source), "attribution source does not contain the complete Foundation MIT notice")


def validate_foundation(profile: str) -> None:
    for rel in PROJECT_REQUIRED:
        path = ROOT / rel
        if not path.is_file():
            add("ERROR", "MISSING_REQUIRED", rel, "required Foundation-project file is missing")
        elif not path.read_text(encoding="utf-8").strip():
            add("ERROR", "EMPTY_REQUIRED", rel, "required file is empty")

    try:
        manifest = load_manifest()
    except (OSError, json.JSONDecodeError) as exc:
        add("BLOCKING", "MANIFEST_READ", "foundation/manifest.json", str(exc))
        return
    validate_manifest(manifest)

    repo_map = ROOT / ".ai" / "repo_map.yaml"
    if repo_map.is_file():
        text = repo_map.read_text(encoding="utf-8")
        for rel in [
            "Documentation/Standards/DOCUMENTATION_POLICY.md",
            "Documentation/Standards/SOURCE_AND_EVIDENCE_POLICY.md",
            "Documentation/Standards/DEPENDENCY_POLICY.md",
            "Documentation/Standards/SEMANTIC_INTEGRATION_POLICY.md",
            "Documentation/Standards/PERSISTENT_IDENTITY_POLICY.md",
            "Documentation/Standards/ARTIFACT_REGISTRATION_POLICY.md",
            "Documentation/Standards/CENTRAL_ARTIFACT_REGISTRY_POLICY.md",
            "Documentation/Standards/RULE_CONTEXT_CACHE_POLICY.md",
            "Documentation/Architecture/DECISIONS.md",
        ]:
            if rel not in text:
                add("ERROR", "AUTHORITY_MAP", ".ai/repo_map.yaml", f"authoritative source missing from map: {rel}")

    target_map_template = ROOT / "foundation" / "repo_map.template.yaml"
    if target_map_template.is_file():
        map_text = target_map_template.read_text(encoding="utf-8")
        validate_markers(map_text, "foundation/repo_map.template.yaml", "VALIDATION_SCOPE_MAP", VALIDATION_MAP_MARKERS)
        validate_markers(map_text, "foundation/repo_map.template.yaml", "INTEGRATION_SCOPE_MAP", INTEGRATION_MAP_MARKERS)
        validate_markers(map_text, "foundation/repo_map.template.yaml", "IDENTITY_SCOPE_MAP", IDENTITY_MAP_MARKERS)
        validate_markers(map_text, "foundation/repo_map.template.yaml", "REGISTRATION_SCOPE_MAP", REGISTRATION_MAP_MARKERS)
        validate_markers(map_text, "foundation/repo_map.template.yaml", "CENTRAL_REGISTRY_SCOPE_MAP", CENTRAL_REGISTRY_MAP_MARKERS)
        validate_markers(map_text, "foundation/repo_map.template.yaml", "RULE_CONTEXT_CACHE_SCOPE_MAP", RULE_CONTEXT_CACHE_MAP_MARKERS)

    agents_template = ROOT / "foundation" / "AGENTS.template.md"
    if agents_template.is_file():
        agents_text = agents_template.read_text(encoding="utf-8")
        if "transitively discoverable" not in agents_text or "SEMANTIC_INTEGRATION_POLICY.md" not in agents_text:
            add("ERROR", "DISCOVERY_CONTRACT", "foundation/AGENTS.template.md", "root discovery/integration contract is missing")

    for rel in [".github/copilot-instructions.md", "CLAUDE.md", "GEMINI.md"]:
        path = ROOT / rel
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            if len(text) > 1000 or "AGENTS.md" not in text:
                add("WARNING", "ADAPTER_NOT_THIN", rel, "adapter may duplicate governance")

    if profile != "quick":
        for path in sorted(ROOT.rglob("*")):
            if not path.is_file() or ".git" in path.parts or ".local" in path.parts or "__pycache__" in path.parts:
                continue
            scan_text(path, path.relative_to(ROOT).as_posix())

    if profile == "release":
        status = ROOT / ".ai" / "PROJECT_STATUS.md"
        if status.is_file() and ("not executed" in status.read_text(encoding="utf-8") or "pending manual validation" in status.read_text(encoding="utf-8")):
            add("ERROR", "PENDING_RELEASE_VALIDATION", ".ai/PROJECT_STATUS.md", "release profile still contains pending validation")


def validate_target(target: Path, adapter_selection: str, capability_selection: str, profile: str) -> None:
    try:
        manifest = load_manifest()
        rows = selected_rows(manifest, adapter_selection, capability_selection)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        add("BLOCKING", "MANIFEST_READ", "foundation/manifest.json", str(exc))
        return

    add("INFO", "PROJECT_VALIDATION_OUT_OF_SCOPE", ".", "Foundation validator covers FOUNDATION_INTEGRITY only. PROJECT_SEMANTIC and RUNTIME_EMPIRICAL validation remain target-project responsibilities when affected.")
    add("INFO", "PROJECT_GOVERNANCE_DISCOVERY_SEMANTIC", "AGENTS.md", "Foundation validator can verify the discovery contract is installed but cannot prove that every active target-specific authority in an arbitrary repository was semantically inventoried and linked. Existing-repository integration must review this under PROJECT_SEMANTIC.")
    add("INFO", "PROJECT_IDENTITY_SEMANTICS_OUT_OF_SCOPE", ".", "Foundation validator verifies the installed identity contract but cannot prove that an arbitrary target's historical identifiers, aliases, relations, or migration mappings are semantically correct. Review them under PROJECT_SEMANTIC and RUNTIME_EMPIRICAL when affected.")
    add("INFO", "PROJECT_REGISTRATION_AUTHORITY_OUT_OF_SCOPE", ".", "Foundation validator verifies the installed registration/central-registry contracts and selected capability files, but cannot prove that a target-specific issue tracker, service, database, registry path, or allocator is the correct serialized Registration Authority. Review that under PROJECT_SEMANTIC/RUNTIME_EMPIRICAL.")

    selected_paths: list[Path] = []
    required_mit_notice = (ROOT / "LICENSE").read_text(encoding="utf-8")
    for row in rows:
        source = ROOT / row["source"]
        destination = target / row["target"]
        display = row["target"]
        if not destination.is_file():
            add("ERROR", "MISSING_TARGET_RULE", display, "selected Foundation rule/adapter/capability is missing")
            continue
        selected_paths.append(destination)
        text = destination.read_text(encoding="utf-8", errors="replace")
        if display == "AGENTS.md":
            if "AI_REPOSITORY_FOUNDATION" not in text:
                add("ERROR", "ENTRYPOINT_BRIDGE", display, "Foundation bridge marker is missing")
            if "transitively discoverable" not in text:
                add("ERROR", "DISCOVERY_CONTRACT", display, "Foundation project-governance discovery contract is missing")
        if row.get("kind") == "adapter" and "AGENTS.md" not in text:
            add("ERROR", "ADAPTER_DISCOVERY", display, "adapter does not lead to AGENTS.md")
        if row.get("kind") == "attribution" and required_mit_notice not in text:
            add("BLOCKING", "ATTRIBUTION_NOTICE", display, "installed attribution file does not preserve the complete Foundation MIT notice")
        if display == ".ai/foundation/repo_map.yaml":
            validate_markers(text, display, "VALIDATION_SCOPE_MAP", VALIDATION_MAP_MARKERS)
            validate_markers(text, display, "INTEGRATION_SCOPE_MAP", INTEGRATION_MAP_MARKERS)
            validate_markers(text, display, "IDENTITY_SCOPE_MAP", IDENTITY_MAP_MARKERS)
            validate_markers(text, display, "REGISTRATION_SCOPE_MAP", REGISTRATION_MAP_MARKERS)
            validate_markers(text, display, "CENTRAL_REGISTRY_SCOPE_MAP", CENTRAL_REGISTRY_MAP_MARKERS)
            validate_markers(text, display, "RULE_CONTEXT_CACHE_SCOPE_MAP", RULE_CONTEXT_CACHE_MAP_MARKERS)
        if display.startswith(".ai/foundation/") and source.is_file() and not files_equivalent(destination, source):
            add("WARNING", "LOCAL_OVERRIDE_OR_DRIFT", display, "installed Foundation rule/provenance/capability file differs from current source after portable text-EOL normalization; this detects drift only and does not establish semantic correctness of the override")

    if profile != "quick":
        for path in selected_paths:
            scan_text(path, path.relative_to(target).as_posix())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, help="validate installed rules in another repository")
    parser.add_argument("--adapters", default="default", help="default, none, or comma-separated adapter names")
    parser.add_argument("--capabilities", default="none", help="default, none, or comma-separated optional capability names")
    parser.add_argument("--profile", choices=["quick", "commit", "full", "release"], default="full")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args(argv)

    results.clear()
    if args.target:
        validate_target(args.target.resolve(), args.adapters, args.capabilities, args.profile)
        validation_scope = "FOUNDATION_INTEGRITY"
    else:
        validate_foundation(args.profile)
        validation_scope = "FOUNDATION_PROJECT_INTEGRITY"

    counts = {severity: sum(item["severity"] == severity for item in results) for severity in ["INFO", "WARNING", "ERROR", "BLOCKING"]}
    payload = {"schema_version": 1, "validation_scope": validation_scope, "counts": counts, "results": results}
    if args.json_output:
        print(json.dumps(payload, indent=2))
    else:
        for item in results:
            print(f"[{item['severity']}] {item['code']} {item['path']}: {item['message']}")
        print(f"[SCOPE] {validation_scope}")
        print("[SUMMARY] " + " ".join(f"{key.lower()}={value}" for key, value in counts.items()))

    if counts["BLOCKING"]:
        return 2
    if counts["ERROR"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
