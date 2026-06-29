"""Exact pre-data robustness envelope for a generic finite RACH universe.

This intentionally has no species, fitness, floral, or pollinator semantics.
It asks how a false-positive binary channel can turn an inactive focal motif into
a false invariant, and how requiring agreement across independent robustness
cells changes that risk.

Run:
    python examples/exact_observation_envelope.py
"""

from causal_model import (
    CoverageMode,
    DetectionChannelDesign,
    Mechanism,
    ObservationEnvelopeCell,
    QualitativeProgram,
    QualitativeProgramCandidate,
    observation_envelope_table_markdown,
    sweep_exact_observation_envelopes,
)


ACTIVE = QualitativeProgramCandidate(
    "active_focal",
    frozenset({"focal"}),
    QualitativeProgram(
        mechanism_count=1,
        trait_rules={"signal": Mechanism(0)},
        feasible_states=frozenset({(1,)}),
    ),
)
INACTIVE = QualitativeProgramCandidate(
    "inactive_focal",
    frozenset(),
    QualitativeProgram(
        mechanism_count=1,
        trait_rules={"signal": Mechanism(0)},
        feasible_states=frozenset({(0,)}),
    ),
)


def channel_cell(cell_id: str) -> ObservationEnvelopeCell:
    return ObservationEnvelopeCell(
        cell_id=cell_id,
        description="generic independent binary observation channel",
        channels=(
            DetectionChannelDesign(
                trait="signal",
                trials=1,
                sensitivity=0.9,
                false_positive=0.2,
            ),
        ),
        acceptance_log_likelihood=-0.5,
        coverage_mode=CoverageMode.EXHAUSTIVE,
    )


def main() -> None:
    one_cell = sweep_exact_observation_envelopes(
        (ACTIVE, INACTIVE),
        ("focal",),
        {"one channel": (channel_cell("evidence"),)},
        true_candidate_id="inactive_focal",
        true_states={"evidence": (0,)},
    )
    two_cells = sweep_exact_observation_envelopes(
        (ACTIVE, INACTIVE),
        ("focal",),
        {
            "two independent required cells": (
                channel_cell("evidence_a"),
                channel_cell("evidence_b"),
            )
        },
        true_candidate_id="inactive_focal",
        true_states={"evidence_a": (0,), "evidence_b": (0,)},
    )
    print(observation_envelope_table_markdown((*one_cell, *two_cells), "focal", digits=4))


if __name__ == "__main__":
    main()
