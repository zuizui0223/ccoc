import pytest

from causal_model.observation_design import (
    NullObservationCandidate,
    minimum_discriminating_panel,
)
from causal_model.replaceability import Observation, StructuralModel


def _model() -> StructuralModel:
    return StructuralModel(
        mechanism_count=3,
        driver_sets={
            "shared": frozenset({0, 1, 2}),
            "witness_1": frozenset({1}),
            "witness_2": frozenset({2}),
            "joint_witness": frozenset({1, 2}),
        },
    )


def test_finds_jointly_necessary_witness_panel() -> None:
    result = minimum_discriminating_panel(
        _model(),
        focal_mechanism=0,
        target_trait="shared",
        candidates=(
            NullObservationCandidate("witness_1"),
            NullObservationCandidate("witness_2"),
        ),
    )
    assert result is not None
    assert result.selected_null_traits == ("witness_1", "witness_2")
    assert result.total_cost == 2.0
    assert result.observation == Observation(present=("shared",), null=("witness_1", "witness_2"))
    assert result.eliminated_mechanisms == frozenset({1, 2})


def test_chooses_minimum_cost_panel_not_fewest_observations() -> None:
    result = minimum_discriminating_panel(
        _model(),
        focal_mechanism=0,
        target_trait="shared",
        candidates=(
            NullObservationCandidate("witness_1", cost=0.2),
            NullObservationCandidate("witness_2", cost=0.2),
            NullObservationCandidate("joint_witness", cost=1.0),
        ),
    )
    assert result is not None
    assert result.selected_null_traits == ("witness_1", "witness_2")
    assert result.total_cost == 0.4


def test_excludes_witnesses_that_eliminate_the_focal_mechanism() -> None:
    model = StructuralModel(
        mechanism_count=3,
        driver_sets={
            "shared": frozenset({0, 1, 2}),
            "bad": frozenset({0, 1}),
            "witness_2": frozenset({2}),
        },
    )
    result = minimum_discriminating_panel(
        model,
        focal_mechanism=0,
        target_trait="shared",
        candidates=(NullObservationCandidate("bad"), NullObservationCandidate("witness_2")),
    )
    assert result is None


def test_returns_none_when_base_present_constraints_make_design_infeasible() -> None:
    model = StructuralModel(
        mechanism_count=3,
        driver_sets={
            "shared": frozenset({0, 1, 2}),
            "other_required": frozenset({1}),
            "witness_1": frozenset({1}),
            "witness_2": frozenset({2}),
        },
    )
    result = minimum_discriminating_panel(
        model,
        focal_mechanism=0,
        target_trait="shared",
        base_observation=Observation(present=("other_required",)),
        candidates=(NullObservationCandidate("witness_1"), NullObservationCandidate("witness_2")),
    )
    assert result is None


def test_rejects_candidate_that_conflicts_with_required_present_trait() -> None:
    with pytest.raises(ValueError, match="conflicts with required-present"):
        minimum_discriminating_panel(
            _model(),
            focal_mechanism=0,
            target_trait="shared",
            candidates=(NullObservationCandidate("shared"),),
        )
