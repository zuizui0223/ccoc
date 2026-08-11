"""Tests for exact union-grammar refinement capacity and correlation defect."""

import math
from itertools import product

import pytest

import causal_model.portability_core as portability
from causal_model.addressable_codebooks import build_canonical_operational_codebook, even_parity_codebook
from causal_model.codebook_families import fixed_weight_binary_codebook
from causal_model.union_grammar_refinement import (
    certify_partition_refinement_capacity,
    certify_union_grammar_refinement,
)


def _codebook_union_certificate(codebook):
    canonical = build_canonical_operational_codebook(codebook)
    base_words = (canonical.coordinate_words[0],)
    closed_word_families = tuple(
        (canonical.coordinate_words[0], canonical.coordinate_words[coordinate])
        for coordinate in range(1, len(canonical.coordinate_words))
    )
    return certify_union_grammar_refinement(
        system=canonical.system,
        domain_states=canonical.embedding,
        base_words=base_words,
        closed_word_families=closed_word_families,
    )


def test_union_grammar_is_exact_common_refinement_on_full_product():
    exterior_count = 3
    codebook = tuple(product((0, 1), repeat=exterior_count + 1))
    certificate = _codebook_union_certificate(codebook)

    assert certificate.verify()
    assert certificate.open_block_count == 2 ** (exterior_count + 1)
    assert certificate.closed_block_counts == (4,) * exterior_count
    assert certificate.fibered_capacity_state_count == 2 ** (exterior_count + 1)
    assert certificate.correlation_defect_bits == pytest.approx(0.0)
    assert certificate.exact_noncommutation_gap_bits == pytest.approx(exterior_count - 1)
    assert certificate.refinement_capacity.saturates_fibered_capacity


def test_even_parity_is_exactly_one_bit_below_fibered_capacity():
    exterior_count = 4
    certificate = _codebook_union_certificate(even_parity_codebook(exterior_count))

    assert certificate.open_block_count == 2**exterior_count
    assert certificate.fibered_capacity_state_count == 2 ** (exterior_count + 1)
    assert certificate.closed_block_counts == (4,) * exterior_count
    assert certificate.correlation_defect_bits == pytest.approx(1.0)
    assert certificate.exact_noncommutation_gap_bits == pytest.approx(exterior_count - 2)
    assert not certificate.refinement_capacity.saturates_fibered_capacity


def test_fixed_richness_gap_is_capacity_gap_minus_combinatorial_defect():
    exterior_count = 6
    weight = 3
    certificate = _codebook_union_certificate(fixed_weight_binary_codebook(exterior_count, weight))

    expected_open_states = 2 * math.comb(exterior_count, weight)
    expected_capacity = 2 ** (exterior_count + 1)
    expected_defect = math.log2(expected_capacity / expected_open_states)
    expected_gap = math.log2(math.comb(exterior_count, weight)) - 1

    assert certificate.open_block_count == expected_open_states
    assert certificate.fibered_capacity_state_count == expected_capacity
    assert certificate.closed_block_counts == (4,) * exterior_count
    assert certificate.correlation_defect_bits == pytest.approx(expected_defect)
    assert certificate.exact_noncommutation_gap_bits == pytest.approx(expected_gap)
    assert certificate.refinement_capacity.capacity_gap_bits == pytest.approx(exterior_count - 1)
    assert certificate.exact_noncommutation_gap_bits == pytest.approx(
        certificate.refinement_capacity.capacity_gap_bits - certificate.correlation_defect_bits
    )


def test_nonuniform_base_fibers_use_sum_of_local_cartesian_capacities():
    certificate = certify_partition_refinement_capacity(
        base_labels=("A", "A", "A", "B", "B", "B", "B"),
        closed_labels=(
            ("a0", "a0", "a1", "b0", "b0", "b0", "b0"),
            ("c0", "c1", "c0", "d0", "d0", "d1", "d1"),
        ),
    )

    assert certificate.verify()
    assert certificate.closed_block_counts == (3, 4)
    assert certificate.common_refinement_block_count == 5
    assert certificate.fibered_capacity_state_count == 6  # A: 2*2, B: 1*2
    assert certificate.correlation_defect_bits == pytest.approx(math.log2(6 / 5))
    assert certificate.exact_noncommutation_gap_bits == pytest.approx(math.log2(5 / 4))
    assert certificate.capacity_gap_bits == pytest.approx(math.log2(6 / 4))
    assert certificate.base_block_saturates_capacity("A") is False
    assert certificate.base_block_saturates_capacity("B") is True


def test_partition_certificate_rejects_closed_partition_that_crosses_base_blocks():
    with pytest.raises(ValueError, match="shared-base refinement"):
        certify_partition_refinement_capacity(
            base_labels=("A", "A", "B", "B"),
            closed_labels=(("x", "y", "x", "z"),),
        )


def test_union_certificate_requires_base_words_inside_every_closed_grammar():
    canonical = build_canonical_operational_codebook(tuple(product((0, 1), repeat=3)))

    with pytest.raises(ValueError, match="union-grammar refinement"):
        certify_union_grammar_refinement(
            system=canonical.system,
            domain_states=canonical.embedding,
            base_words=(canonical.coordinate_words[0],),
            closed_word_families=(
                (canonical.coordinate_words[1],),
                (canonical.coordinate_words[0], canonical.coordinate_words[2]),
            ),
        )


def test_refinement_certificates_are_public_portability_exports():
    assert portability.certify_partition_refinement_capacity is certify_partition_refinement_capacity
    assert portability.certify_union_grammar_refinement is certify_union_grammar_refinement
    assert "PartitionRefinementCapacityCertificate" in portability.__all__
    assert "UnionGrammarRefinementCertificate" in portability.__all__
