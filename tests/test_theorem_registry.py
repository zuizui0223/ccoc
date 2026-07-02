"""Regression checks for the theorem retrieval registry."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "theorem_registry.json"
CHECKER = ROOT / "scripts" / "verify_theorem_registry.py"


def test_registry_has_the_frozen_public_theory_ids_and_no_empirical_scope():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    assert registry["required_ids"] == [
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
    prohibited = " ".join(registry["repository_scope"]["prohibited"]).lower()
    assert "empirical ecological datasets" in prohibited
    assert "field observations" in prohibited


def test_registry_checker_validates_the_human_atlas_and_scope_policy():
    completed = subprocess.run(
        [sys.executable, str(CHECKER), "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr + completed.stdout
    assert json.loads(completed.stdout)["theorem_count"] == 14
