"""Validate the canonical RACH theorem registry.

The registry is intentionally a retrieval and scope-control artifact, not a new
mathematical engine. Every public claim must point to finite-domain assumptions,
source code, regression evidence, documentation, and an explicit non-claim.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs" / "theorem_registry.json"
ATLAS_PATH = ROOT / "docs" / "theorem_registry.md"
SCOPE_POLICY_PATH = ROOT / "docs" / "nonempirical_scope.md"
README_PATH = ROOT / "README.md"
REPORT_PATH = ROOT / "artifacts" / "theorem_registry_report.json"

ALLOWED_STATUSES = {
    "exact finite theorem",
    "sufficient criterion",
    "sufficient finite-domain theorem",
    "lower-bound obstruction",
    "sharpness witness",
    "no-go theorem",
    "local obstruction",
    "frozen conditional design theorems",
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


def _nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _nonempty_strings(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(_nonempty_text(item) for item in value)


def _load_registry() -> dict[str, Any]:
    try:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"registry is not valid JSON: {error}") from error
    if not isinstance(registry, dict):
        raise ValueError("registry root must be an object")
    return registry


def _validate_repository_path(path_text: str, entry_id: str, field: str) -> None:
    if path_text.startswith(("/", "../")) or "\\" in path_text:
        raise ValueError(f"{entry_id}.{field} contains an unsafe repository path: {path_text}")
    path = ROOT / path_text
    if not path.is_file():
        raise ValueError(f"{entry_id}.{field} points to a missing file: {path_text}")


def validate_registry(registry: dict[str, Any]) -> dict[str, Any]:
    if registry.get("registry_version") != 1:
        raise ValueError("registry_version must equal 1")

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
    if not _nonempty_strings(required_ids):
        raise ValueError("required_ids must be a nonempty text list")
    if len(required_ids) != len(set(required_ids)):
        raise ValueError("required_ids must be unique")
    if not isinstance(entries, list) or not entries:
        raise ValueError("entries must be a nonempty list")

    seen_ids: set[str] = set()
    tiers: dict[str, int] = {}
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != REQUIRED_ENTRY_KEYS:
            raise ValueError("each entry must contain exactly the required registry keys")
        entry_id = entry["id"]
        if not _nonempty_text(entry_id):
            raise ValueError("entry id must be nonempty text")
        if entry_id in seen_ids:
            raise ValueError(f"duplicate theorem identifier: {entry_id}")
        seen_ids.add(entry_id)
        if not _nonempty_text(entry["title"]) or not _nonempty_text(entry["tier"]):
            raise ValueError(f"{entry_id} title and tier must be nonempty text")
        if entry["status"] not in ALLOWED_STATUSES:
            raise ValueError(f"{entry_id} has an unsupported status: {entry['status']}")
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

    if set(required_ids) != seen_ids:
        missing = sorted(set(required_ids) - seen_ids)
        unexpected = sorted(seen_ids - set(required_ids))
        raise ValueError(f"registry identifiers differ from required_ids; missing={missing}, unexpected={unexpected}")

    return {
        "registry_version": registry["registry_version"],
        "theorem_count": len(entries),
        "tiers": tiers,
        "statuses": {status: sum(entry["status"] == status for entry in entries) for status in sorted(ALLOWED_STATUSES)},
        "identifiers": sorted(seen_ids),
        "empirical_data_policy": "prohibited",
    }


def validate_human_entrypoints(registry: dict[str, Any]) -> None:
    atlas = ATLAS_PATH.read_text(encoding="utf-8")
    policy = SCOPE_POLICY_PATH.read_text(encoding="utf-8")
    readme = README_PATH.read_text(encoding="utf-8")
    for entry_id in registry["required_ids"]:
        if f"`{entry_id}`" not in atlas:
            raise ValueError(f"human atlas does not expose theorem identifier {entry_id}")
    for required_text in ("not empirical", "mathematical ecology", "finite"):
        if required_text not in policy.lower():
            raise ValueError(f"nonempirical scope policy is missing required wording: {required_text}")
    if "docs/theorem_registry.md" not in readme or "docs/nonempirical_scope.md" not in readme:
        raise ValueError("README must link both the theorem atlas and nonempirical scope policy")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate the registry and its human entry points")
    parser.add_argument("--write-report", action="store_true", help="write a deterministic JSON validation report")
    args = parser.parse_args()

    registry = _load_registry()
    report = validate_registry(registry)
    if args.check:
        validate_human_entrypoints(registry)
    if args.write_report:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
