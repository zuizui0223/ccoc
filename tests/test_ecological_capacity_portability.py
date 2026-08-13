import pytest

from causal_model.ecological_capacity_portability import (
    certify_guild_capacity_family_portability,
)
from causal_model.ecological_saturation_blanket import certify_depletion_opening


def test_one_macro_law_survives_changing_capacity_domains() -> None:
    certificate = certify_guild_capacity_family_portability(
        capacities_by_stage=((2, 3), (5, 6), (8, 9)),
        saturation_levels=(1, 2),
        colonization_increments=((0, 0), (1, 0), (0, 2), (2, 1)),
    )

    assert certificate.verify()
    assert certificate.macro_state_count == 2 * 3
    assert certificate.stage_count_state_counts == (12, 42, 90)
    assert all(
        stage.blanket_state_count == certificate.macro_state_count
        for stage in certificate.stage_certificates
    )


def test_shared_macro_transition_is_independent_of_capacity() -> None:
    certificate = certify_guild_capacity_family_portability(
        capacities_by_stage=((2, 2), (4, 7)),
        saturation_levels=(2, 1),
        colonization_increments=((1, 0), (0, 3)),
    )

    assert certificate.verify()
    assert certificate.macro_successor((1, 1), 0) == (2, 1)
    assert certificate.macro_successor((2, 0), 0) == (2, 0)
    assert certificate.macro_successor((0, 0), 1) == (0, 1)


def test_capacity_family_rejects_stage_below_fixed_saturation_threshold() -> None:
    with pytest.raises(ValueError):
        certify_guild_capacity_family_portability(
            capacities_by_stage=((3, 3), (1, 3)),
            saturation_levels=(2, 1),
            colonization_increments=((1, 0),),
        )


def test_depletion_prevents_uniform_fixed_block_bound_as_capacity_grows() -> None:
    witnesses = [certify_depletion_opening(capacity, 1) for capacity in (2, 4, 8, 16)]

    assert all(witness.verify() for witness in witnesses)
    assert [witness.closed_block_count for witness in witnesses] == [2, 2, 2, 2]
    assert [witness.open_block_count for witness in witnesses] == [3, 5, 9, 17]
