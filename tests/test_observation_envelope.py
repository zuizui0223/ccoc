from math import isclose

import pytest

from causal_model import (
    CoverageMode,
    DetectionChannelDesign,
    Mechanism,
    ObservationEnvelopeCell,
    QualitativeProgram,
    QualitativeProgramCandidate,
    evaluate_exact_observation_envelope,
    observation_envelope_table_markdown,
    sweep_exact_observation_envelopes,
)


def active_candidate() -> QualitativeProgramCandidate:
    return QualitativeProgramCandidate(
        "active",
        frozenset({"focal"}),
        QualitativeProgram(
            mechanism_count=1,
            trait_rules={"signal": Mechanism(0)},
            feasible_states=frozenset({(1,)}),
        ),
    )


def inactive_candidate() -> QualitativeProgramCandidate:
    return QualitativeProgramCandidate(
        "inactive",
        frozenset(),
        QualitativeProgram(
            mechanism_count=1,
            trait_rules={"signal": Mechanism(0)},
            feasible_states=frozenset({(0,)}),
        ),
    )


def cell(*, trials: int = 1, sensitivity: float = 1.0, false_positive: float = 0.0) -> ObservationEnvelopeCell:
    return ObservationEnvelopeCell(
        cell_id="evidence",
        description="generic binary evidence channel",
        channels=(
            DetectionChannelDesign(
                trait="signal",
                trials=trials,
                sensitivity=sensitivity,
                false_positive=false_positive,
            ),
        ),
        acceptance_log_likelihood=-0.5,
        coverage_mode=CoverageMode.EXHAUSTIVE,
    )


def test_perfect_channel_recovers_the_true_active_motif_exactly() -> None:
    envelope = evaluate_exact_observation_envelope(
        (active_candidate(), inactive_candidate()),
        ("focal",),
        (cell(),),
        true_candidate_id="active",
        true_states={"evidence": (1,)},
    )
    profile = envelope.profiles["focal"]

    assert envelope.total_outcome_count == 2
    assert isclose(envelope.total_probability, 1.0)
    assert profile.true_active
    assert profile.invariant_probability == 1.0
    assert profile.correct_invariant_probability == 1.0
    assert profile.decisive_error_probability == 0.0


def test_false_positive_rate_becomes_exact_false_invariant_risk() -> None:
    envelope = evaluate_exact_observation_envelope(
        (active_candidate(), inactive_candidate()),
        ("focal",),
        (cell(sensitivity=0.9, false_positive=0.2),),
        true_candidate_id="inactive",
        true_states={"evidence": (0,)},
    )
    profile = envelope.profiles["focal"]

    # A reported detection occurs with probability 0.2 under the inactive truth.
    # At the declared threshold it accepts only the active candidate, producing a
    # false invariant. A reported NULL has probability 0.8 and correctly excludes
    # the focal motif.
    assert not profile.true_active
    assert isclose(profile.false_invariant_probability, 0.2)
    assert isclose(profile.correct_excluded_probability, 0.8)
    assert isclose(profile.invariant_probability + profile.excluded_probability, 1.0)
    assert profile.unresolved_probability == 0.0


def test_sweep_and_markdown_table_preserve_exact_profiles() -> None:
    points = sweep_exact_observation_envelopes(
        (active_candidate(), inactive_candidate()),
        ("focal",),
        {
            "perfect": (cell(),),
            "false-positive": (cell(sensitivity=0.9, false_positive=0.2),),
        },
        true_candidate_id="inactive",
        true_states={"evidence": (0,)},
    )

    assert [point.label for point in points] == ["perfect", "false-positive"]
    assert points[0].envelope.profiles["focal"].correct_excluded_probability == 1.0
    assert isclose(points[1].envelope.profiles["focal"].false_invariant_probability, 0.2)
    table = observation_envelope_table_markdown(points, "focal", digits=3)
    assert "false-positive" in table
    assert "0.200" in table


def test_exact_envelope_refuses_a_larger_than_declared_outcome_space() -> None:
    with pytest.raises(ValueError, match="above max_outcomes"):
        evaluate_exact_observation_envelope(
            (active_candidate(), inactive_candidate()),
            ("focal",),
            (cell(trials=3),),
            true_candidate_id="active",
            true_states={"evidence": (1,)},
            max_outcomes=3,
        )
