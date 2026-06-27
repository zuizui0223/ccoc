from math import isinf

import pytest

from causal_model.replaceability import (
    Observation,
    StructuralModel,
    admissible_configurations,
    forced_off,
    forced_on,
    greedy_failure_witness,
    null_eliminated_mechanisms,
    structural_crc,
    theorem_a_certificate,
)


def _model() -> StructuralModel:
    return StructuralModel(
        mechanism_count=3,
        driver_sets={
            "shared": frozenset({0, 1, 2}),
            "private_1": frozenset({1}),
            "private_2": frozenset({2}),
        },
    )


def test_null_observation_eliminates_exact_driver_set() -> None:
    observation = Observation(present=("shared",), null=("private_1",))
    assert null_eliminated_mechanisms(_model(), observation) == frozenset({1})
    configs = admissible_configurations(_model(), observation)
    assert forced_off(configs, 1)
    assert not forced_off(configs, 0)
    assert not forced_off(configs, 2)


def test_last_driver_criterion_certifies_indispensability() -> None:
    observation = Observation(present=("shared",), null=("private_1", "private_2"))
    configs = admissible_configurations(_model(), observation)
    certificate = theorem_a_certificate(_model(), observation, 0)
    assert certificate.holds
    assert certificate.forced_on
    assert certificate.supporting_traits == ("shared",)
    assert isinf(structural_crc(0, configs))


def test_positive_shared_observation_does_not_make_any_driver_indispensable() -> None:
    configs = admissible_configurations(_model(), Observation(present=("shared",)))
    assert not any(forced_on(configs, mechanism) for mechanism in range(3))


def test_joint_elimination_has_greedy_failure_witness() -> None:
    assert greedy_failure_witness(2)
    assert greedy_failure_witness(5)


def test_contradictory_observation_has_empty_region_not_necessity() -> None:
    model = StructuralModel(1, {"trait": frozenset({0})})
    observation = Observation(present=("trait",), null=("trait",))
    with pytest.raises(ValueError, match="both present and null"):
        admissible_configurations(model, observation)


def test_invalid_driver_index_is_rejected() -> None:
    with pytest.raises(ValueError, match="invalid mechanism index"):
        StructuralModel(2, {"trait": frozenset({2})})
