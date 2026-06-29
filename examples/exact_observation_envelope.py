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
    designs = {
        "one channel": (channel_cell("evidence"),),
        "two independent required cells": (
            channel_cell("evidence_a"),
            channel_cell("evidence_b"),
        ),
    }
    points = sweep_exact_observation_envelopes(
        (ACTIVE, INACTIVE),
        ("focal",),
        designs,
        true_candidate_id="inactive_focal",
        true_states={"evidence": (0,)},
    )

    # The two-cell design has different cell IDs, so evaluate it separately with
    # matching true states rather than silently assuming contexts are identical.
    two_cell = sweep_exact_observation_envelopes(
        (ACTIVE, INACTIVE),
        ("focal",),
        {"two independent required cells": designs["two independent required cells"]},
        true_candidate_id="inactive_focal",
        true_states={"evidence_a": (0,), "evidence_b": (0,)},
    )
    one_cell = points[:1]
    print(observation_envelope_table_markdown((*one_cell, *two_cell), "focal", digits=4))


if __name__ == "__main__":
    main()
