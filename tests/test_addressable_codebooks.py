"""Tests for addressable codebook lower bounds and constrained witnesses."""

import math
from itertools import product

import pytest

import causal_model.portability_core as portability
from causal_model.addressable_codebooks import (
    build_canonical_operational_codebook,
    certify_canonical_operational_codebook,
    certify_operational_addressable_codebook,
    certify_operational_codebook_closed_context_factorization,
    even_parity_codebook,
    readout_symbol,
    standard_codebook_closed_projection,
)
from causal_model.codebook_families import (
    fixed_weight_binary_codebook,
    fixed_weight_binary_codebook_size,
)
from causal_model.relay_tree_compilation import (
    RelayTreeTopology,
    quiescent_configuration,
    run_macro_probe,
)


def _closed_contract(open_certificate):
    return certify_operational_codebook_closed_context_factorization(
        open_certificate=open_certificate,
        closed_words=tuple(
            ((), open_certificate.coordinate_words[0], open_certificate.coordinate_words[module_index + 1])
            for module_index in range(open_certificate.exterior_count)
        ),
        closed_factor_maps=tuple(
            standard_codebook_closed_projection(module_index)
            for module_index in range(open_certificate.exterior_count)
        ),
    )


def test_even_parity_codebook_is_not_a_full_product_but_has_linear_gap():
    exterior_count = 3
    codebook = even_parity_codebook(exterior_count)
    open_certificate = certify_canonical_operational_codebook(codebook)
    closed_certificate = _closed_contract(open_certificate)

    assert open_certificate.verify()
    assert open_certificate.codeword_count == 2**exterior_count
    assert open_certificate.coordinate_value_counts == (2, 2, 2, 2)
    assert open_certificate.ambient_cartesian_count == 2 ** (exterior_count + 1)
    assert not open_certificate.is_full_cartesian_codebook
    assert open_certificate.open_bits_lower_bound == exterior_count

    assert closed_certificate.verify()
    assert closed_certificate.factor_label_counts == (4, 4, 4)
    assert closed_certificate.closed_interface_upper_bits == (2.0, 2.0, 2.0)
    assert closed_certificate.noncommutation_gap_lower_bound == exterior_count - 2


def test_parity_family_scales_as_m_minus_two_for_m_at_least_two():
    for exterior_count in range(2, 7):
        open_certificate = certify_canonical_operational_codebook(even_parity_codebook(exterior_count))
        closed_certificate = _closed_contract(open_certificate)

        assert open_certificate.open_bits_lower_bound == exterior_count
        assert closed_certificate.factor_label_counts == (4,) * exterior_count
        assert closed_certificate.noncommutation_gap_lower_bound == pytest.approx(exterior_count - 2)


def test_fixed_weight_family_has_large_gap_under_exact_richness_constraint():
    exterior_count = 6
    weight = 3
    codebook = fixed_weight_binary_codebook(exterior_count, weight)
    open_certificate = certify_canonical_operational_codebook(codebook)
    closed_certificate = _closed_contract(open_certificate)

    assert len(codebook) == fixed_weight_binary_codebook_size(exterior_count, weight)
    assert len(codebook) == 2 * math.comb(exterior_count, weight)
    assert all(sum(codeword[1:]) == weight for codeword in codebook)
    assert not open_certificate.is_full_cartesian_codebook
    assert open_certificate.open_bits_lower_bound == pytest.approx(
        1.0 + math.log2(math.comb(exterior_count, weight))
    )
    assert closed_certificate.factor_label_counts == (4,) * exterior_count
    assert closed_certificate.noncommutation_gap_lower_bound == pytest.approx(
        math.log2(math.comb(exterior_count, weight)) - 1.0
    )


def test_fixed_weight_codebook_inherits_bounded_degree_relay_readout():
    exterior_count = 5
    weight = 2
    topology = RelayTreeTopology.balanced(exterior_count)

    assert all(topology.maximum_degree_with_reader(port) <= 3 for port in range(exterior_count))
    for codeword in fixed_weight_binary_codebook(exterior_count, weight):
        inside = codeword[0]
        exterior = codeword[1:]
        initial = quiescent_configuration(topology, inside, exterior)
        for port in range(exterior_count):
            final = run_macro_probe(topology, initial, port)
            assert final.focal_output == exterior[port]
            assert final.memory_bits == exterior


def test_full_cartesian_product_is_recovered_as_a_special_codebook():
    codebook = tuple(product((0, 1), repeat=3))
    open_certificate = certify_canonical_operational_codebook(codebook)
    closed_certificate = _closed_contract(open_certificate)

    assert open_certificate.is_full_cartesian_codebook
    assert open_certificate.codeword_count == 8
    assert open_certificate.open_bits_lower_bound == 3.0
    assert closed_certificate.factor_label_counts == (4, 4)
    assert closed_certificate.noncommutation_gap_lower_bound == 1.0


def test_codebook_certificate_rejects_a_decoder_that_does_not_recover_a_coordinate():
    canonical = build_canonical_operational_codebook(even_parity_codebook(2))

    with pytest.raises(ValueError, match="codebook witness"):
        certify_operational_addressable_codebook(
            system=canonical.system,
            codebook=canonical.codebook,
            embedding=canonical.embedding,
            coordinate_words=canonical.coordinate_words,
            coordinate_decoders=(readout_symbol, lambda _trace: 0, readout_symbol),
        )


def test_closed_factorization_rejects_collapsing_a_readable_projection():
    open_certificate = certify_canonical_operational_codebook(even_parity_codebook(3))

    with pytest.raises(ValueError, match="factorization"):
        certify_operational_codebook_closed_context_factorization(
            open_certificate=open_certificate,
            closed_words=tuple(
                ((), open_certificate.coordinate_words[0], open_certificate.coordinate_words[module_index + 1])
                for module_index in range(open_certificate.exterior_count)
            ),
            closed_factor_maps=(
                lambda _codeword: "collapsed",
                standard_codebook_closed_projection(1),
                standard_codebook_closed_projection(2),
            ),
        )


def test_codebook_certificates_are_exported_by_portability_core():
    assert portability.certify_canonical_operational_codebook is certify_canonical_operational_codebook
    assert portability.certify_operational_codebook_closed_context_factorization is certify_operational_codebook_closed_context_factorization
    assert portability.fixed_weight_binary_codebook is fixed_weight_binary_codebook
    assert "OperationalAddressableCodebookCertificate" in portability.__all__
    assert "OperationalCodebookClosedContextCertificate" in portability.__all__
    assert "fixed_weight_binary_codebook" in portability.__all__
