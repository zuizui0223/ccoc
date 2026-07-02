"""Regression checks for theorem retrieval entry points."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "theorem_registry.json"
ATLAS = ROOT / "docs" / "theorem_registry.md"

EXPECTED_IDS = [
    "CORE-0",
    "CORE-1",
    "CORE-2",
    "CORE-3",
    "CORE-4",
    "CORE-5",
    "EXT-1",
    "EXT-2",
    "EXT-3",
    "EXT-4",
    "ID-1",
    "ID-2",
    "ID-3",
    "LEGACY-1",
]


def test_registry_exposes_the_frozen_public_theory_ids():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    assert registry["required_ids"] == EXPECTED_IDS
    assert len(registry["entries"]) == len(EXPECTED_IDS)


def test_every_registry_identifier_is_visible_in_the_human_atlas():
    atlas = ATLAS.read_text(encoding="utf-8")

    for theorem_id in EXPECTED_IDS:
        assert f"`{theorem_id}`" in atlas
