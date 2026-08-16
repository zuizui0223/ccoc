"""Validate the current CCOC theorem registry and immutable historical archive.

The executable registry contains only theorem surfaces that are required to exist
in the current tree. Historical theorem IDs live in a separate archive index with
an immutable recovery pin; their former source paths are provenance strings and
are deliberately not required to exist after cleanup.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs" / "theorem_registry.json"
ARCHIVE_PATH = ROOT / "docs" / "historical_theorem_archive.json"
ATLAS_PATH = ROOT / "docs" / "theorem_registry.md"
ARCHIVE_ATLAS_PATH = ROOT / "docs" / "historical_theorem_archive.md"
SCOPE_POLICY_PATH = ROOT / "docs" / "nonempirical_scope.md"
README_PATH = ROOT / "README.md"
REPORT_PATH = ROOT / "artifacts" / "theorem_registry_report.json"

CURRENT_IDS = ("CORE-1", "CORE-2", "CORE-3", "CORE-4", "CORE-5")
HISTORICAL_IDS = (
    "CORE-0",
    "EXT-1",
    "EXT-2",
    "EXT-3",
    "EXT-4",
    "ID-1",
    "ID-2",
    "ID-3",
    "LEGACY-1",
)

ALLOWED_STATUSES = {
    "exact finite theorem",
    "sufficient criterion",
    "lower-bound obstruction",
    "sharpness witness",
    "local obstruction",
}
REQUIRED_SCOPE_KEYS = {
    "discipline",
    "object",
    "allowed",
    "prohibited",
    "interpretation_boundary",
}
REQUIRED_ENTRY_KEYS = {
    "id",
    "title",
    "tier",
    "status",
    "domain",
    "assumptions",
    "conclusion",
    "modules",
    "tests",
    "documents",
    "certificates",
    "verification",
    "non_claim",
    "ecological_role",
}
REQUIRED_ARCHIVE_ENTRY_KEYS = {
    "id",
    "title",
    "former_status",
    "summary",
    "former_modules",
    "former_tests",
    "former_documents",
}


def _nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _nonempty_strings(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(_nonempty_text(item) for item in value)


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"{label} is not valid JSON: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"{label} root must be an object")
    return value


def _validate_repository_path(path_text: str, entry_id: str, field: str) -> None:
    if path_text.startswith(("/", "../")) or "\\" in path_text:
        raise ValueError(f"{entry_id}.{field} contains an unsafe repository path: {path_text}")
    path = ROOT / path_text
    if not path.is_file():
        raise ValueError(f"{entry_id}.{field} points to a missing current file: {path_text}")


def validate_registry(registry: dict[str, Any]) -> dict[str, Any]:
    if registry.get("registry_version") != 2:
        raise ValueError("registry_version must equal 2")
    if registry.get("historical_archive") != "docs/historical_theorem_archive.json":
        raise ValueError("historical_archive must point to docs/historical_theorem_archive.json")

    scope = registry.get("repository_scope")
    if not isinstance(scope, dict) or set(scope) != REQUIRED_SCOPE_KEYS:
        raise ValueError("repository_scope must contain exactly the required scope keys")
    if not _nonempty_text(scope["discipline"]) or not _nonempty_text(scope["object"]):
        raise ValueError("repository scope discipline and object must be nonempty text")
    if not _nonempty_strings(scope["allowed"]) or not _nonempty_strings(scope["prohibited"]):
        raise ValueError("repository scope allowed and prohibited lists must be nonempty text lists")
    if not _nonempty_text(scope["interpretation_boundary"]):
        raise ValueError("repository scope interpretation boundary must be nonempty text")

    required_ids = registry.get("required_ids")
    entries = registry.get("entries")
    if required_ids != list(CURRENT_IDS):
        raise ValueError(f"required_ids must equal current publication IDs: {CURRENT_IDS}")
    if not isinstance(entries, list) or len(entries) != len(CURRENT_IDS):
        raise ValueError("entries must contain exactly the current publication-core records")

    seen_ids: set[str] = set()
    tiers: dict[str, int] = {}
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != REQUIRED_ENTRY_KEYS:
            raise ValueError("each current entry must contain exactly the required registry keys")
        entry_id = entry["id"]
        if not _nonempty_text(entry_id) or entry_id in seen_ids:
            raise ValueError(f"invalid or duplicate theorem identifier: {entry_id}")
        seen_ids.add(entry_id)
        if not _nonempty_text(entry["title"]) or not _nonempty_text(entry["tier"]):
            raise ValueError(f"{entry_id} title and tier must be nonempty text")
        if entry["status"] not in ALLOWED_STATUSES:
            raise ValueError(f"{entry_id} has an unsupported current status: {entry['status']}")
        for key in ("domain", "assumptions", "conclusion", "non_claim", "ecological_role"):
            if not _nonempty_text(entry[key]):
                raise ValueError(f"{entry_id}.{key} must be nonempty text")
        for key in ("modules", "tests", "documents", "certificates", "verification"):
            if not _nonempty_strings(entry[key]):
                raise ValueError(f"{entry_id}.{key} must be a nonempty text list")
        for path_text in entry["modules"]:
            if not path_text.startswith("causal_model/"):
                raise ValueError(f"{entry_id}.modules must point into causal_model: {path_text}")
            _validate_repository_path(path_text, entry_id, "modules")
        for path_text in entry["tests"]:
            if not path_text.startswith("tests/"):
                raise ValueError(f"{entry_id}.tests must point into tests: {path_text}")
            _validate_repository_path(path_text, entry_id, "tests")
        for path_text in entry["documents"]:
            if not path_text.startswith("docs/"):
                raise ValueError(f"{entry_id}.documents must point into docs: {path_text}")
            _validate_repository_path(path_text, entry_id, "documents")
        if not all(command.startswith(("python ", "PYTHONPATH=")) for command in entry["verification"]):
            raise ValueError(f"{entry_id}.verification must contain reproducible Python commands")
        tiers[entry["tier"]] = tiers.get(entry["tier"], 0) + 1

    if tuple(seen_ids) and seen_ids != set(CURRENT_IDS):
        raise ValueError(f"current entry IDs differ from required IDs: {sorted(seen_ids)}")

    return {
        "registry_version": registry["registry_version"],
        "current_theorem_count": len(entries),
        "tiers": tiers,
        "statuses": {status: sum(entry["status"] == status for entry in entries) for status in sorted(ALLOWED_STATUSES)},
        "current_identifiers": list(CURRENT_IDS),
        "empirical_data_policy": "prohibited",
    }


def validate_historical_archive(archive: dict[str, Any]) -> dict[str, Any]:
    if archive.get("archive_version") != 1:
        raise ValueError("historical archive_version must equal 1")
    pin = archive.get("pre_registry_cleanup_pin")
    if not isinstance(pin, str) or re.fullmatch(r"[0-9a-f]{40}", pin) is None:
        raise ValueError("historical archive requires a 40-character lowercase Git recovery pin")
    if not _nonempty_text(archive.get("purpose")):
        raise ValueError("historical archive purpose must be nonempty text")

    entries = archive.get("entries")
    if not isinstance(entries, list) or len(entries) != len(HISTORICAL_IDS):
        raise ValueError("historical archive must contain exactly the declared historical IDs")

    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("historical archive entries must be objects")
        missing = REQUIRED_ARCHIVE_ENTRY_KEYS - set(entry)
        unexpected = set(entry) - (REQUIRED_ARCHIVE_ENTRY_KEYS | {"successor_repository"})
        if missing or unexpected:
            raise ValueError(f"invalid historical archive entry keys; missing={sorted(missing)}, unexpected={sorted(unexpected)}")
        entry_id = entry["id"]
        if entry_id in seen or entry_id not in HISTORICAL_IDS:
            raise ValueError(f"invalid historical theorem identifier: {entry_id}")
        seen.add(entry_id)
        for key in ("title", "former_status", "summary"):
            if not _nonempty_text(entry[key]):
                raise ValueError(f"{entry_id}.{key} must be nonempty text")
        for key in ("former_modules", "former_tests", "former_documents"):
            if not _nonempty_strings(entry[key]):
                raise ValueError(f"{entry_id}.{key} must be a nonempty historical path list")
        if "successor_repository" in entry and not _nonempty_text(entry["successor_repository"]):
            raise ValueError(f"{entry_id}.successor_repository must be nonempty when supplied")

    if seen != set(HISTORICAL_IDS):
        raise ValueError(f"historical archive IDs differ from expected IDs: {sorted(seen)}")

    return {
        "archive_version": archive["archive_version"],
        "historical_theorem_count": len(entries),
        "historical_identifiers": list(HISTORICAL_IDS),
        "recovery_pin": pin,
    }


def validate_human_entrypoints() -> None:
    atlas = ATLAS_PATH.read_text(encoding="utf-8")
    archive_atlas = ARCHIVE_ATLAS_PATH.read_text(encoding="utf-8")
    policy = SCOPE_POLICY_PATH.read_text(encoding="utf-8")
    readme = README_PATH.read_text(encoding="utf-8")

    for entry_id in CURRENT_IDS:
        if f"`{entry_id}`" not in atlas:
            raise ValueError(f"current theorem atlas does not expose {entry_id}")
    for entry_id in HISTORICAL_IDS:
        if f"`{entry_id}`" not in archive_atlas:
            raise ValueError(f"historical theorem atlas does not expose {entry_id}")
    for required_text in ("not empirical", "mathematical ecology", "finite"):
        if required_text not in policy.lower():
            raise ValueError(f"nonempirical scope policy is missing required wording: {required_text}")
    if "docs/theorem_registry.md" not in readme or "docs/nonempirical_scope.md" not in readme:
        raise ValueError("README must link the current theorem atlas and nonempirical scope policy")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate current registry, archive, and human entry points")
    parser.add_argument("--write-report", action="store_true", help="write a deterministic JSON validation report")
    args = parser.parse_args()

    registry = _load_json(REGISTRY_PATH, "registry")
    archive = _load_json(ARCHIVE_PATH, "historical archive")
    current_report = validate_registry(registry)
    archive_report = validate_historical_archive(archive)
    if args.check:
        validate_human_entrypoints()

    report = {
        **current_report,
        **archive_report,
    }
    if args.write_report:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
