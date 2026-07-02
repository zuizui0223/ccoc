"""Regression test for the single-command manuscript-core replay."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_paper_core.py"
REPORT = ROOT / "artifacts" / "paper_core_reproducibility_report.json"


def test_paper_core_replay_writes_a_scope_limited_deterministic_report():
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--write-report"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    report = json.loads(completed.stdout)

    assert REPORT.is_file()
    assert report["schema_version"] == 1
    assert report["scope"]["product_object"].startswith("declared product-indexed subset")
    assert report["core_1_exact_interface"]["refinement_verified"]
    assert report["core_2_operational_addressability"]["product_state_count"] == 12
    assert report["core_2_operational_addressability"]["gap_lower_bound"] == 1.0
    assert report["core_3_binary_sharpness"][-1] == {
        "module_count": 6,
        "closed_bits": 2,
        "open_bits": 7,
        "gap_bits": 5,
        "maximum_degree": 3,
    }
    assert report["core_4_5_portability_boundary"]["future_word_obstruction_verified"]
    assert report["core_4_5_portability_boundary"]["new_action_obstruction_verified"]
