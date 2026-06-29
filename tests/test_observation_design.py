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


def test_minimum_panel_matches_bruteforce_on_small_driver_models() -> None:
    from itertools import combinations, product

    from causal_model.replaceability import forced_on_by_theorem, observation_is_admissible

    all_nonempty_sets = tuple(
        frozenset(index for index, flag in enumerate(mask) if flag)
        for mask in product((0, 1), repeat=3)
        if any(mask)
    )
    witness_traits = ("witness_a", "witness_b", "witness_c")

    for witness_driver_sets in product(all_nonempty_sets, repeat=3):
        model = StructuralModel(
            mechanism_count=3,
            driver_sets={
                "shared": frozenset({0, 1, 2}),
                **dict(zip(witness_traits, witness_driver_sets)),
            },
        )
        candidates = tuple(NullObservationCandidate(trait) for trait in witness_traits)
        result = minimum_discriminating_panel(
            model,
            focal_mechanism=0,
            target_trait="shared",
            candidates=candidates,
        )

        expected: tuple[float, tuple[str, ...]] | None = None
        for size in range(len(candidates) + 1):
            for panel in combinations(candidates, size):
                traits = tuple(candidate.trait for candidate in panel)
                observation = Observation(present=("shared",), null=traits)
                if not observation_is_admissible(model, observation):
                    continue
                if not forced_on_by_theorem(model, observation, 0):
                    continue
                proposal = (float(size), traits)
                if expected is None or (proposal[0], len(proposal[1]), proposal[1]) < (
                    expected[0],
                    len(expected[1]),
                    expected[1],
                ):
                    expected = proposal

        if expected is None:
            assert result is None
        else:
            assert result is not None
            assert result.total_cost == expected[0]
            assert result.selected_null_traits == expected[1]
