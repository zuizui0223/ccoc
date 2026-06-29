"""Reproduce the paper-facing exact finite benchmark tables.

Run from the repository root:

    python experiments/run_all_benchmarks.py --output results

The script uses no Monte Carlo sampling and no third-party dependencies. Every
reported probability is a finite weighted enumeration under an explicitly stated
benchmark family. The produced CSV files are intended as figure-ready inputs,
not as empirical estimates.
"""

from __future__ import annotations

import argparse
import csv
from itertools import product
from pathlib import Path
from typing import Iterable

from causal_model.failure_modes import BinaryObservationChannel, TruthTableModel
from causal_model.generative_benchmarks import sweep_two_driver_family
from causal_model.observation_design import NullObservationCandidate
from causal_model.panel_phase_benchmarks import sweep_panel_phase_family
from causal_model.replaceability import StructuralModel
from causal_model.robust_panel_design import (
    FinitePanelScenario,
    RobustObjective,
    choose_robust_panel,
    compare_panel_selection_strategies,
)


def _write_csv(path: Path, rows: Iterable[dict[str, object]]) -> int:
    materialized = list(rows)
    if not materialized:
        raise ValueError(f"cannot write empty benchmark table: {path.name}")
    fields = list(materialized[0])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(materialized)
    return len(materialized)


def _float_or_blank(value: float | None) -> str:
    return "" if value is None else f"{value:.12g}"


def two_driver_phase_rows() -> list[dict[str, object]]:
    """Latent route, detection, and inhibition surface for the two-driver family."""
    points = sweep_two_driver_family(
        {
            "latent_driver_prevalence": (0.0, 0.25, 0.5, 1.0),
            "witness_sensitivity": (1.0, 0.95, 0.9),
            "inhibition_prevalence": (0.0, 0.25, 0.5, 1.0),
            "conjunction_prevalence": (0.0, 1.0),
        }
    )
    rows: list[dict[str, object]] = []
    for point in points:
        p = point.parameters
        rows.append(
            {
                "latent_driver_prevalence": p.latent_driver_prevalence,
                "witness_sensitivity": p.witness_sensitivity,
                "inhibition_prevalence": p.inhibition_prevalence,
                "conjunction_prevalence": p.conjunction_prevalence,
                "compatibility_constraint_prevalence": p.compatibility_constraint_prevalence,
                "report_probability": _float_or_blank(point.reported_observation_probability),
                "false_necessity_risk": _float_or_blank(point.false_necessity_risk),
                "perfect_measurement_risk": _float_or_blank(point.perfect_measurement_focal_off_probability),
                "report_is_impossible": point.report_is_impossible,
            }
        )
    return rows


def multi_competitor_rows() -> list[dict[str, object]]:
    """Joint-panel versus strict-greedy results under correlated contexts."""
    comparisons = sweep_panel_phase_family(
        {
            "competitor_count": (2, 3),
            "latent_route_count": (0, 1),
            "competitor_on_probability_low": (0.0, 0.25),
            "competitor_on_probability_high": (0.75, 1.0),
            "latent_on_probability_low": (0.0,),
            "latent_on_probability_high": (0.0, 0.5),
            "inhibition_probability_low": (0.0,),
            "inhibition_probability_high": (0.0, 0.5),
            "witness_sensitivity": (1.0, 0.9),
        }
    )
    rows: list[dict[str, object]] = []
    for comparison in comparisons:
        p = comparison.parameters
        exact = comparison.exact
        greedy = comparison.strict_greedy
        rows.append(
            {
                "competitor_count": p.competitor_count,
                "latent_route_count": p.latent_route_count,
                "competitor_on_probability_low": p.competitor_on_probability_low,
                "competitor_on_probability_high": p.competitor_on_probability_high,
                "latent_on_probability_high": p.latent_on_probability_high,
                "inhibition_probability_high": p.inhibition_probability_high,
                "witness_sensitivity": p.witness_sensitivity,
                "exact_panel": ";".join(exact.selected_null_traits),
                "exact_declared_forced_on": exact.declared_forced_on,
                "exact_report_probability": _float_or_blank(exact.reported_panel_probability),
                "exact_false_necessity_risk": _float_or_blank(exact.false_necessity_risk),
                "strict_greedy_panel": ";".join(greedy.selected_null_traits),
                "strict_greedy_declared_forced_on": greedy.declared_forced_on,
                "strict_greedy_posterior_focal_off": _float_or_blank(greedy.posterior_focal_off_probability),
                "synergy_gap": comparison.synergy_gap,
            }
        )
    return rows


def _robust_declared_model() -> StructuralModel:
    return StructuralModel(
        mechanism_count=4,
        driver_sets={
            "target": frozenset({0, 1, 2}),
            "shared": frozenset({1, 2}),
            "witness_1": frozenset({1}),
            "witness_2": frozenset({2}),
        },
    )


def _robust_truth_model(*, shared_inhibited: bool) -> TruthTableModel:
    states = tuple(product((0, 1), repeat=4))
    return TruthTableModel(
        mechanism_count=4,
        trait_true_states={
            "target": frozenset(state for state in states if state[0] or state[1] or state[2]),
            "shared": frozenset(
                state
                for state in states
                if (state[1] or state[2]) and (not shared_inhibited or not state[3])
            ),
            "witness_1": frozenset(state for state in states if state[1]),
            "witness_2": frozenset(state for state in states if state[2]),
        },
    )


def _robust_candidates() -> tuple[NullObservationCandidate, ...]:
    return (
        NullObservationCandidate("shared", cost=0.5),
        NullObservationCandidate("witness_1", cost=1.0),
        NullObservationCandidate("witness_2", cost=1.0),
    )


def _robust_scenarios() -> tuple[FinitePanelScenario, ...]:
    return (
        FinitePanelScenario(
            "frequent_private_noise",
            _robust_truth_model(shared_inhibited=False),
            weight=10.0,
            channels={
                "witness_1": BinaryObservationChannel(present_if_true_present=0.9),
                "witness_2": BinaryObservationChannel(present_if_true_present=0.9),
            },
        ),
        FinitePanelScenario(
            "rare_shared_inhibition",
            _robust_truth_model(shared_inhibited=True),
            weight=1.0,
        ),
    )


def robust_design_rows() -> list[dict[str, object]]:
    """Budgeted cost, greedy, minimax, and weighted-mean design comparisons."""
    model = _robust_declared_model()
    candidates = _robust_candidates()
    scenarios = _robust_scenarios()
    rows: list[dict[str, object]] = []
    for budget in (0.5, 1.5, 2.0, 2.5):
        comparison = compare_panel_selection_strategies(
            model,
            focal_mechanism=0,
            target_trait="target",
            candidates=candidates,
            scenarios=scenarios,
            max_cost=budget,
        )
        selectors = {
            "minimum_cost": comparison.minimum_cost,
            "coverage_greedy": comparison.coverage_greedy,
            "minimax": comparison.minimax,
            "weighted_mean": comparison.weighted_mean,
        }
        for selector, result in selectors.items():
            rows.append(
                {
                    "budget": budget,
                    "selector": selector,
                    "selected_panel": "" if result is None else ";".join(result.selected_null_traits),
                    "total_cost": "" if result is None else f"{result.total_cost:.12g}",
                    "worst_case_risk": "" if result is None else f"{result.worst_case_risk:.12g}",
                    "weighted_mean_risk": "" if result is None else f"{result.weighted_mean_risk:.12g}",
                    "available": result is not None,
                }
            )
    return rows


def anchor_rows() -> list[dict[str, object]]:
    """Small canonical identities used in text, unit tests, and reviewer checks."""
    return [
        {
            "benchmark": "two_driver_baseline",
            "quantity": "false_necessity_risk",
            "exact_value": "0",
            "interpretation": "Declared OR grammar and perfect witness are correct.",
        },
        {
            "benchmark": "two_driver_sensitivity_0.9",
            "quantity": "false_necessity_risk",
            "exact_value": "1/12",
            "interpretation": "A 10% false-NULL rate yields 8.3% posterior false necessity.",
        },
        {
            "benchmark": "two_driver_latent_route",
            "quantity": "false_necessity_risk",
            "exact_value": "1/3",
            "interpretation": "An omitted alternative target route defeats declared necessity.",
        },
        {
            "benchmark": "multi_competitor_correlated_context",
            "quantity": "exact_joint_panel_risk",
            "exact_value": "1/102",
            "interpretation": "Joint NULLs identify a low-competitor environment under the canonical correlated model.",
        },
        {
            "benchmark": "robust_shared_witness",
            "quantity": "rare_shared_inhibition_risk",
            "exact_value": "3/8",
            "interpretation": "A cheap shared witness can be structurally fragile.",
        },
    ]


def _summary_markdown(counts: dict[str, int]) -> str:
    lines = [
        "# Exact benchmark output summary",
        "",
        "All files in this directory were generated by `experiments/run_all_benchmarks.py`.",
        "They are finite weighted enumerations under declared benchmark families; they are not empirical estimates and contain no Monte Carlo uncertainty.",
        "",
        "| File | Rows | Purpose |",
        "|---|---:|---|",
        f"| `two_driver_phase_grid.csv` | {counts['two_driver_phase_grid.csv']} | Candidate omission, sensitivity, inhibition, and conjunction surface. |",
        f"| `multi_competitor_panel_grid.csv` | {counts['multi_competitor_panel_grid.csv']} | Exact joint panels versus strict greedy under correlated contexts. |",
        f"| `robust_panel_design_grid.csv` | {counts['robust_panel_design_grid.csv']} | Cost-first, greedy, minimax, and mean-risk design under budgets. |",
        f"| `canonical_anchors.csv` | {counts['canonical_anchors.csv']} | Closed-form / canonical values cited by text and tests. |",
        "",
        "## Reproduction",
        "",
        "```bash",
        "python experiments/run_all_benchmarks.py --output results",
        "```",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate exact RACH benchmark tables.")
    parser.add_argument("--output", type=Path, default=Path("results"), help="Directory for generated CSV and Markdown files.")
    args = parser.parse_args()
    output = args.output
    output.mkdir(parents=True, exist_ok=True)

    tables = {
        "two_driver_phase_grid.csv": two_driver_phase_rows(),
        "multi_competitor_panel_grid.csv": multi_competitor_rows(),
        "robust_panel_design_grid.csv": robust_design_rows(),
        "canonical_anchors.csv": anchor_rows(),
    }
    counts = {name: _write_csv(output / name, rows) for name, rows in tables.items()}
    (output / "README.md").write_text(_summary_markdown(counts), encoding="utf-8")
    print(f"Wrote exact benchmark tables to {output.resolve()}")
    for name, count in counts.items():
        print(f"  {name}: {count} rows")


if __name__ == "__main__":
    main()
