from math import log2

import pytest

from causal_model.extension_compression_noncommutation import (
    certify_addressable_product_lower_bound,
    certify_closed_context_factorization,
    certify_relay_tree_sharpness,
    decoder_coordinate,
    exhaustive_noncommutation_summary,
)


def test_product_decoder_injection_uses_a_concrete_coordinate_for_every_distinct_pair():
    certificate = certify_addressable_product_lower_bound(3, (2, 4, 5))
    assert certificate.verify()
    assert certificate.open_state_lower_bound == 3 * 2 * 4 * 5
    assert certificate.checked_distinct_pairs == 120 * 119 // 2
    assert certificate.base_word_decodes_inside
    assert certificate.module_words_decode_exteriors == (True, True, True)


def test_decoder_coordinate_selects_inside_or_one_exterior_component():
    assert decoder_coordinate((0, 0, 0), (1, 0, 0)) == 0
    assert decoder_coordinate((1, 0, 0), (1, 1, 0)) == 1
    assert decoder_coordinate((1, 1, 0), (1, 1, 1)) == 2
    with pytest.raises(ValueError, match="distinct"):
        decoder_coordinate((1, 0), (1, 0))


def test_closed_context_factorization_yields_the_noncommutation_inequality():
    certificate = certify_closed_context_factorization(3, (2, 4, 8))
    assert certificate.verify()
    assert certificate.closed_context_state_counts == (6, 12, 24)
    assert certificate.product_certificate.open_state_lower_bound == 192
    assert certificate.product_certificate.open_bits_lower_bound == log2(192)
    assert certificate.expected_gap_lower_bound == 1.0 + 2.0 + 3.0 - 3.0
    assert certificate.noncommutation_gap_lower_bound == certificate.expected_gap_lower_bound


@pytest.mark.parametrize("module_count", [1, 2, 3, 4])
def test_binary_relay_tree_is_sharp_for_the_general_product_bound(module_count):
    certificate = certify_relay_tree_sharpness(module_count)
    assert certificate.verify()
    assert certificate.product_bound.open_state_lower_bound == 2 ** (module_count + 1)
    assert certificate.closed_factorization.closed_context_state_counts == (4,) * module_count
    assert certificate.coordinate_witness.open_interface_bits == module_count + 1
    assert certificate.relay_compilation.open_interface_bits == module_count + 1
    assert certificate.closed_bits == 2
    assert certificate.gap_bits == module_count - 1
    assert certificate.relay_compilation.grammar.maximum_degree == 3


def test_sharp_witness_uses_one_constant_local_grammar_at_all_sizes():
    certificates = [certify_relay_tree_sharpness(size) for size in (1, 2, 4)]
    grammar = certificates[0].relay_compilation.grammar
    assert all(certificate.relay_compilation.grammar == grammar for certificate in certificates)
    assert grammar.maximum_degree == 3
    assert grammar.reader_states == ("ready", "fire")


def test_exhaustive_small_family_replays_the_linear_gap():
    certificates = exhaustive_noncommutation_summary(4)
    assert [certificate.gap_bits for certificate in certificates] == [0, 1, 2, 3]
    assert all(certificate.verify() for certificate in certificates)


def test_invalid_cardinalities_fail_closed():
    with pytest.raises(ValueError, match="positive"):
        certify_addressable_product_lower_bound(0, (2,))
    with pytest.raises(ValueError, match="at least one"):
        certify_addressable_product_lower_bound(2, ())
    with pytest.raises(ValueError, match="positive"):
        certify_closed_context_factorization(2, (2, 0))
