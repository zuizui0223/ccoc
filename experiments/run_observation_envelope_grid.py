"""Generate an exact generic observation-channel robustness grid for RACH.

This is a known-truth finite self-calibration benchmark. It does not represent a
species, a fitness model, or field data. The declared truth lacks the focal
motif; the grid reports how detector sensitivity, false-positive rate,
acceptance threshold, and the number of required independent cells alter the
probability of a false invariant, correct exclusion, unresolved result, or
unsupported result.

Run from repository root:

    python experiments/run_observation_envelope_grid.py --output results/observation_envelope_grid.csv
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from causal_model import (
    CoverageMode,
    DetectionChannelDesign,
    Mechanism,
    ObservationEnvelopeCell,
    QualitativeProgram,
    QualitativeProgramCandidate,
    evaluate_exact_observation_envelope,
)


def _candidates() -> tuple[QualitativeProgramCandidate, ...]:
    return (
        QualitativeProgramCandidate(
            "active_focal",
            frozenset({"focal"}),
            QualitativeProgram(
                mechanism_count=1,
                trait_rules={"signal": Mechanism(0)},
                feasible_states=frozenset({(1,)}),
            ),
        ),
        QualitativeProgramCandidate(
            "inactive_focal",
            frozenset(),
            QualitativeProgram(
                mechanism_count=1,
                trait_rules={"signal": Mechanism(0)},
                feasible_states=frozenset({(0,)}),
            ),
        ),
    )


def _cells(
    *,
    required_cell_count: int,
    sensitivity: float,
    false_positive: float,
    threshold: float,
) -> tuple[ObservationEnvelopeCell, ...]:
    return tuple(
        ObservationEnvelopeCell(
            cell_id=f"cell_{index}",
            description="generic independent binary observation channel",
            channels=(
                DetectionChannelDesign(
                    trait="signal",
                    trials=1,
                    sensitivity=sensitivity,
                    false_positive=false_positive,
                ),
            ),
            acceptance_log_likelihood=threshold,
            coverage_mode=CoverageMode.EXHAUSTIVE,
        )
        for index in range(1, required_cell_count + 1)
    )


def rows() -> list[dict[str, object]]:
    table: list[dict[str, object]] = []
    for required_cell_count in (1, 2, 3):
        for sensitivity in (0.6, 0.8, 0.9, 1.0):
            for false_positive in (0.0, 0.05, 0.2):
                for threshold in (-2.0, -0.5):
                    cells = _cells(
                        required_cell_count=required_cell_count,
                        sensitivity=sensitivity,
                        false_positive=false_positive,
                        threshold=threshold,
                    )
                    envelope = evaluate_exact_observation_envelope(
                        _candidates(),
                        ("focal",),
                        cells,
                        true_candidate_id="inactive_focal",
                        true_states={cell.cell_id: (0,) for cell in cells},
                    )
                    profile = envelope.profiles["focal"]
                    table.append(
                        {
                            "required_cell_count": required_cell_count,
                            "trials_per_cell": 1,
                            "sensitivity": sensitivity,
                            "false_positive": false_positive,
                            "acceptance_log_likelihood": threshold,
                            "outcome_count": envelope.total_outcome_count,
                            "invariant_probability": f"{profile.invariant_probability:.12g}",
                            "excluded_probability": f"{profile.excluded_probability:.12g}",
                            "unresolved_probability": f"{profile.unresolved_probability:.12g}",
                            "unsupported_probability": f"{profile.unsupported_probability:.12g}",
                            "false_invariant_probability": f"{profile.false_invariant_probability:.12g}",
                            "correct_excluded_probability": f"{profile.correct_excluded_probability:.12g}",
                        }
                    )
    return table


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an exact generic RACH observation-envelope grid.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results") / "observation_envelope_grid.csv",
        help="Destination CSV file.",
    )
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    table = rows()
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(table[0]))
        writer.writeheader()
        writer.writerows(table)
    print(f"Wrote {len(table)} exact envelope rows to {args.output.resolve()}")


if __name__ == "__main__":
    main()
