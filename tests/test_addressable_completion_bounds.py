import math

import pytest

from causal_model.addressable_completion_bounds import (
    CanonicalAddressableProduct,
    certify_addressable_completion_product,
    certify_finite_boundary_blanket,
    certify_passive_closure_nonidentifiability,
    read_word,
    separating_word_certificate,
)


def test_binary_product_bound_recovers_linear_extension_compression_gap():
    certificate = certify_addressable_completion_product((2, 2, 2, 2))
    assert certificate.verify()
    assert certificate.passive_block_count == 2
    assert certificate.closed_block_counts == (4, 4, 4)
    assert certificate.open_block_count == 16
    assert certificate.passive_interface_bits == 1.0
    assert certificate.open_interface_bits == 4.0
    assert certificate.extension_compression_gap_bits == 2.0
    assert certificate.gap_lower_bound_bits == 2.0


def test_nonbinary_product_bound_is_exact_not_binary_specific():
    certificate = certify_addressable_completion_product((3, 2, 5))
    assert certificate.verify()
    assert certificate.closed_block_counts == (6, 15)
    assert certificate.open_block_count == 30
    assert math.isclose(certificate.open_interface_bits, math.log2(30))
    assert math.isclose(certificate.extension_compression_gap_bits, 1.0)
    assert math.isclose(certificate.gap_lower_bound_bits, 1.0)


def test_every_distinct_product_pair_has_a_concrete_separating_word():
    system = CanonicalAddressableProduct((2, 3, 2))
    for left_index, left in enumerate(system.states):
        for right in system.states[left_index + 1:]:
            certificate = separating_word_certificate(system.factor_cardinalities, left, right)
            assert certificate.verify()
            differing = next(index for index, pair in enumerate(zip(left, right)) if pair[0] != pair[1])
            assert certificate.word == ("observe" if differing == 0 else read_word(differing))


def test_closed_context_retains_only_inside_and_its_single_exterior_coordinate():
    system = CanonicalAddressableProduct((2, 2, 3, 5))
    assert len(system.closed_partition(1)) == 4
    assert len(system.closed_partition(2)) == 6
    assert len(system.closed_partition(3)) == 10
    assert all(len(block) > 1 for block in system.closed_partition(1))


def test_finite_boundary_blanket_is_a_constructive_upper_bound():
    certificate = certify_finite_boundary_blanket((2, 2, 3, 5), (1, 3))
    assert certificate.verify()
    assert certificate.boundary_cardinality == 10
    assert certificate.boundary_block_count == 20
    assert math.isclose(certificate.upper_bound_bits, math.log2(20))
    assert math.isclose(certificate.realized_interface_bits, math.log2(20))


def test_passive_data_cannot_distinguish_closed_and_open_model_pair():
    certificate = certify_passive_closure_nonidentifiability((2, 2, 3))
    assert certificate.verify()
    assert certificate.passive_block_count == 2
    assert certificate.closed_model_open_block_count == 2
    assert certificate.open_model_open_block_count == 12
    assert certificate.closed_response == (0,)
    assert certificate.open_response == (0, 1)


@pytest.mark.parametrize(
    "bad_factors",
    [
        (),
        (2,),
        (2, 1),
        (2, 0),
        (2, True),
        (2, 2.5),
    ],
)
def test_invalid_product_factors_fail_closed(bad_factors):
    with pytest.raises(ValueError):
        CanonicalAddressableProduct(bad_factors)


@pytest.mark.parametrize("bad_indices", [(0,), (2, 1), (1, 1), (4,)])
def test_invalid_blanket_indices_fail_closed(bad_indices):
    with pytest.raises(ValueError):
        certify_finite_boundary_blanket((2, 2, 3, 5), bad_indices)
