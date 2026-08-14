from fractions import Fraction
from itertools import product

import pytest

from causal_model.stochastic_ecological_portability import (
    certify_stochastic_capacity_family,
    certify_stochastic_depletion_exposure,
    certify_stochastic_guild_colonization,
)


def _proposal_table(levels=(1, 2)):
    macro_states = tuple(product(*(range(level + 1) for level in levels)))
    seed_rows = []
    pulse_rows = []
    for state in macro_states:
        seed_rows.append(
            (
                ((1, 0), Fraction(1, 2)),
                ((0, 1), Fraction(1, 2)),
            )
        )
        if state[0] == levels[0]:
            pulse_rows.append((((0, 1), Fraction(1, 1)),))
        else:
            pulse_rows.append(
                (
                    ((1, 1), Fraction(2, 3)),
                    ((0, 0), Fraction(1, 3)),
                )
            )
    return (tuple(seed_rows), tuple(pulse_rows))


def test_capped_colonization_is_exact_stochastic_macro_lumping() -> None:
    certificate = certify_stochastic_guild_colonization(
        capacities=(4, 7),
        saturation_levels=(1, 2),
        actions=("seed", "pulse"),
        proposal_table=_proposal_table(),
    )

    assert certificate.verify()
    assert certificate.macro_state_count == 6
    assert certificate.micro_state_count == 40
    for action_rows in certificate.macro_kernel:
        for row in action_rows:
            assert sum(row, Fraction(0, 1)) == 1


def test_stochastic_macro_kernel_is_portable_across_changing_capacities() -> None:
    certificate = certify_stochastic_capacity_family(
        capacities_by_stage=((1, 2), (3, 6), (8, 10)),
        saturation_levels=(1, 2),
        actions=("seed", "pulse"),
        proposal_table=_proposal_table(),
    )

    assert certificate.verify()
    assert certificate.macro_state_count == 6
    assert certificate.micro_state_counts == (6, 28, 99)
    assert all(stage.macro_kernel == certificate.macro_kernel for stage in certificate.stages)


def test_stochastic_colonization_rejects_invalid_proposal_law() -> None:
    table = list(_proposal_table())
    seed_rows = list(table[0])
    seed_rows[0] = (
        ((1, 0), Fraction(1, 4)),
        ((0, 1), Fraction(1, 4)),
    )
    table[0] = tuple(seed_rows)

    with pytest.raises(ValueError):
        certify_stochastic_guild_colonization(
            capacities=(2, 3),
            saturation_levels=(1, 2),
            actions=("seed", "pulse"),
            proposal_table=tuple(table),
        )


def test_positive_probability_depletion_exposes_hidden_oversaturation() -> None:
    certificate = certify_stochastic_depletion_exposure(
        capacity=7,
        saturation_level=2,
        depletion_probability=Fraction(1, 3),
    )

    assert certificate.verify()
    assert certificate.closed_class_count == 3
    assert certificate.open_exact_class_count == 8
    assert certificate.threshold_one_step_tv == Fraction(1, 3)
    assert certificate.minimum_common_one_step_tv_error == Fraction(1, 6)
    assert certificate.saturated_pair_witness(2, 3) == (
        1,
        Fraction(1, 3),
        Fraction(0, 1),
    )
    attempts, lower_probability, upper_probability = certificate.saturated_pair_witness(5, 7)
    assert attempts == 4
    assert lower_probability == Fraction(1, 81)
    assert upper_probability == 0


def test_deterministic_depletion_is_stochastic_boundary_at_p_one() -> None:
    certificate = certify_stochastic_depletion_exposure(5, 2, 1)
    assert certificate.verify()
    assert certificate.threshold_one_step_tv == 1
    assert certificate.minimum_common_one_step_tv_error == Fraction(1, 2)
    assert certificate.open_exact_class_count == 6


def test_zero_depletion_probability_has_no_exposure_and_is_rejected() -> None:
    with pytest.raises(ValueError):
        certify_stochastic_depletion_exposure(5, 2, 0)
