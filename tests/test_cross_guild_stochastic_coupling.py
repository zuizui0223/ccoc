from fractions import Fraction

import pytest

from causal_model.cross_guild_stochastic_coupling import (
    certify_cross_guild_capacity_family,
    certify_cross_guild_coupling,
)


def test_hidden_tail_constant_gives_exact_capped_lumping() -> None:
    certificate = certify_cross_guild_coupling(
        capacity_a=5,
        capacity_b=6,
        threshold_a=2,
        threshold_b=3,
        recruitment_hazards_by_a=(
            Fraction(1, 10),
            Fraction(1, 5),
            Fraction(1, 3),
            Fraction(1, 3),
            Fraction(1, 3),
            Fraction(1, 3),
        ),
    )
    assert certificate.verify()
    assert certificate.exact_capped_lumpable
    assert certificate.saturated_hazard_diameter == 0
    assert certificate.minimax_one_step_tv_error == 0
    assert certificate.exact_obstruction_pair() is None


def test_hidden_tail_variation_has_sharp_one_step_minimax_error() -> None:
    certificate = certify_cross_guild_coupling(
        capacity_a=5,
        capacity_b=5,
        threshold_a=2,
        threshold_b=2,
        recruitment_hazards_by_a=(
            Fraction(1, 10),
            Fraction(1, 5),
            Fraction(1, 5),
            Fraction(3, 5),
            Fraction(2, 5),
            Fraction(4, 5),
        ),
    )
    assert certificate.verify()
    assert not certificate.exact_capped_lumpable
    assert certificate.saturated_hazard_diameter == Fraction(3, 5)
    assert certificate.minimax_saturated_hazard == Fraction(1, 2)
    assert certificate.minimax_one_step_tv_error == Fraction(3, 10)
    assert certificate.obstruction_one_step_tv == Fraction(3, 5)
    pair = certificate.exact_obstruction_pair()
    assert pair is not None
    assert certificate.capped_state(pair[0]) == certificate.capped_state(pair[1]) == (2, 1)
    assert certificate.horizon_path_tv_upper_bound(3) == 1 - Fraction(7, 10) ** 3


def test_changing_capacity_family_shares_one_approximate_macro() -> None:
    family = certify_cross_guild_capacity_family(
        capacities_by_stage=((3, 2), (5, 10), (8, 20)),
        threshold_a=2,
        threshold_b=2,
        hazards_by_stage=(
            (
                Fraction(1, 10), Fraction(1, 5),
                Fraction(2, 5), Fraction(1, 2),
            ),
            (
                Fraction(1, 10), Fraction(1, 5),
                Fraction(3, 10), Fraction(2, 5), Fraction(1, 2), Fraction(3, 5),
            ),
            (
                Fraction(1, 10), Fraction(1, 5),
                Fraction(1, 5), Fraction(3, 10), Fraction(2, 5), Fraction(1, 2),
                Fraction(3, 5), Fraction(13, 20), Fraction(7, 10),
            ),
        ),
    )
    assert family.verify()
    assert family.macro_state_count == 9
    assert family.global_saturated_hazard_min == Fraction(1, 5)
    assert family.global_saturated_hazard_max == Fraction(7, 10)
    assert family.global_saturated_hazard_diameter == Fraction(1, 2)
    assert family.common_saturated_hazard == Fraction(9, 20)
    assert family.minimax_one_step_tv_error == Fraction(1, 4)
    assert not family.exact_common_macro_exists
    assert family.horizon_path_tv_upper_bound(4) == 1 - Fraction(3, 4) ** 4


def test_exact_common_macro_survives_changing_capacities_when_tail_hazard_is_constant() -> None:
    family = certify_cross_guild_capacity_family(
        capacities_by_stage=((2, 3), (5, 8), (12, 30)),
        threshold_a=2,
        threshold_b=2,
        hazards_by_stage=(
            (Fraction(1, 10), Fraction(1, 4), Fraction(1, 3)),
            (
                Fraction(1, 10), Fraction(1, 4),
                Fraction(1, 3), Fraction(1, 3), Fraction(1, 3), Fraction(1, 3),
            ),
            tuple(
                [Fraction(1, 10), Fraction(1, 4)]
                + [Fraction(1, 3)] * 11
            ),
        ),
    )
    assert family.verify()
    assert family.exact_common_macro_exists
    assert family.global_saturated_hazard_diameter == 0
    assert family.minimax_one_step_tv_error == 0


def test_below_threshold_hazards_must_match_for_one_family_macro() -> None:
    with pytest.raises(ValueError):
        certify_cross_guild_capacity_family(
            capacities_by_stage=((3, 3), (5, 5)),
            threshold_a=2,
            threshold_b=2,
            hazards_by_stage=(
                (Fraction(1, 10), Fraction(1, 5), Fraction(1, 3), Fraction(1, 3)),
                (
                    Fraction(1, 10), Fraction(1, 4),
                    Fraction(1, 3), Fraction(1, 3), Fraction(1, 3), Fraction(1, 3),
                ),
            ),
        )


def test_invalid_hazard_vector_is_rejected() -> None:
    with pytest.raises(ValueError):
        certify_cross_guild_coupling(
            capacity_a=3,
            capacity_b=3,
            threshold_a=2,
            threshold_b=2,
            recruitment_hazards_by_a=(0, Fraction(1, 2), 2, Fraction(1, 2)),
        )
