"""Regression checks for current and historical theorem retrieval entry points."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "theorem_registry.json"
ARCHIVE = ROOT / "docs" / "historical_theorem_archive.json"
ATLAS = ROOT / "docs" / "theorem_registry.md"
ARCHIVE_ATLAS = ROOT / "docs" / "historical_theorem_archive.md"

CURRENT_IDS = ["CORE-1", "CORE-2", "CORE-3", "CORE-4", "CORE-5"]
HISTORICAL_IDS = [
    "CORE-0",
    "EXT-1",
    "EXT-2",
    "EXT-3",
    "EXT-4",
    "ID-1",
    "ID-2",
    "ID-3",
    "LEGACY-1",
]


def test_executable_registry_contains_only_current_publication_ids():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    assert registry["registry_version"] == 2
    assert registry["required_ids"] == CURRENT_IDS
    assert [entry["id"] for entry in registry["entries"]] == CURRENT_IDS
    assert registry["historical_archive"] == "docs/historical_theorem_archive.json"


def test_historical_archive_preserves_retired_ids_and_recovery_pin():
    archive = json.loads(ARCHIVE.read_text(encoding="utf-8"))

    assert archive["archive_version"] == 1
    assert len(archive["pre_registry_cleanup_pin"]) == 40
    assert [entry["id"] for entry in archive["entries"]] == HISTORICAL_IDS


def test_human_indexes_separate_current_and_historical_ids():
    atlas = ATLAS.read_text(encoding="utf-8")
    archive_atlas = ARCHIVE_ATLAS.read_text(encoding="utf-8")

    for theorem_id in CURRENT_IDS:
        assert f"`{theorem_id}`" in atlas
    for theorem_id in HISTORICAL_IDS:
        assert f"`{theorem_id}`" in archive_atlas
