import csv
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "experiments" / "run_all_benchmarks.py"


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_exact_benchmark_runner_writes_complete_reproducible_tables(tmp_path: Path) -> None:
    output = tmp_path / "results"
    completed = subprocess.run(
        [sys.executable, str(RUNNER), "--output", str(output)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Wrote exact benchmark tables" in completed.stdout

    expected = {
        "two_driver_phase_grid.csv",
        "multi_competitor_panel_grid.csv",
        "robust_panel_design_grid.csv",
        "canonical_anchors.csv",
        "README.md",
    }
    assert {path.name for path in output.iterdir()} == expected

    two_driver = _read_rows(output / "two_driver_phase_grid.csv")
    assert len(two_driver) == 96
    assert any(
        row["witness_sensitivity"] == "0.9"
        and row["latent_driver_prevalence"] == "0.0"
        and row["inhibition_prevalence"] == "0.0"
        and row["conjunction_prevalence"] == "0.0"
        and row["false_necessity_risk"] == "0.0833333333333"
        for row in two_driver
    )

    multi = _read_rows(output / "multi_competitor_panel_grid.csv")
    assert len(multi) == 128
    assert all(row["exact_declared_forced_on"] == "True" for row in multi)
    assert all(row["strict_greedy_declared_forced_on"] == "False" for row in multi)

    robust = _read_rows(output / "robust_panel_design_grid.csv")
    assert len(robust) == 16
    minimax_budget_two = next(
        row for row in robust if row["budget"] == "2.0" and row["selector"] == "minimax"
    )
    assert minimax_budget_two["selected_panel"] == "witness_1;witness_2"

    anchors = _read_rows(output / "canonical_anchors.csv")
    assert {row["exact_value"] for row in anchors} >= {"0", "1/12", "1/3", "1/102", "3/8"}
    assert "finite weighted enumerations" in (output / "README.md").read_text(encoding="utf-8")
