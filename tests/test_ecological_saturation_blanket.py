from math import log2

import pytest

from causal_model.ecological_saturation_blanket import (
    certify_depletion_opening,
    certify_guild_saturation_blanket,
)


def test_fixed_saturation_blanket_is_independent_of_large_capacities() -> None:
    small = certify_guild_saturation_blanket(
        capacities=(3, 4),
        saturation_levels=(2, 1),
        colonization_increments=((1, 0), (0, 1), (1, 1)),
    )
    large = certify_guild_saturation_blanket(
        capacities=(12, 20),
        saturation_levels=(2, 1),
        colonization_increments=((1, 0), (0, 1), (1, 1)),
    )

    assert small.verify() and large.verify()
    assert small.blanket_state_count == large.blanket_state_count == 6
    assert small.blanket_memory_bits == large.blanket_memory_bits == log2(6)
    assert small.count_state_count == 20
    assert large.count_state_count == 273


def test_monotone_colonization_summary_is_exact_for_multistep_increments() -> None:
    certificate = certify_guild_saturation_blanket(
        capacities=(7, 8, 5),
        saturation_levels=(2, 3, 1),
        colonization_increments=((0, 0, 0), (2, 1, 0), (4, 0, 3)),
    )

    assert certificate.verify()
    assert certificate.blanket_state_count == 3 * 4 * 2
    assert certificate.interface.verify()


def test_depletion_opening_recovers_all_hidden_oversaturation() -> None:
    certificate = certify_depletion_opening(capacity=9, saturation_level=2)

    assert certificate.verify()
    assert certificate.closed_block_count == 3
    assert certificate.open_block_count == 10
    assert certificate.inflation_bits == pytest.approx(log2(10 / 3))
    assert certificate.closed_labels[2] == certificate.closed_labels[9]
    assert len(set(certificate.open_labels)) == 10


def test_fixed_saturation_depletion_inflation_grows_with_capacity() -> None:
    saturation = 1
    values = [
        certify_depletion_opening(capacity, saturation)
        for capacity in (2, 4, 8, 16)
    ]

    assert all(certificate.verify() for certificate in values)
    assert [certificate.closed_block_count for certificate in values] == [2, 2, 2, 2]
    assert [certificate.open_block_count for certificate in values] == [3, 5, 9, 17]
    assert all(
        right.inflation_bits > left.inflation_bits
        for left, right in zip(values, values[1:])
    )


def test_invalid_saturation_contracts_fail_closed() -> None:
    with pytest.raises(ValueError):
        certify_guild_saturation_blanket((3,), (4,), ((1,),))
    with pytest.raises(ValueError):
        certify_guild_saturation_blanket((3, 3), (1, 1), ((1,),))
    with pytest.raises(ValueError):
        certify_depletion_opening(capacity=2, saturation_level=2)
