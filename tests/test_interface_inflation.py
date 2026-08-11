"""Tests for the exact causal-interface inflation decomposition."""

import math
from itertools import product

import pytest

import causal_model.portability_core as portability
from causal_model.addressable_codebooks import build_canonical_operational_codebook
from causal_model.interface_inflation import (
    certify_interface_inflation_decomposition,
    certify_operational_interface_inflation,
)


def _operational_certificate(codebook, closed_coordinates, open_only_coordinates):
    canonical = build_canonical_operational_codebook(codebook)
    base_words = (canonical.coordinate_words[0],)
    closed_word_families = tuple(
        (canonical.coordinate_words[0], canonical.coordinate_words[coordinate])
        for coordinate in closed_coordinates
    )
    open_only_words = tuple(canonical.coordinate_words[coordinate] for coordinate in open_only_coordinates)
    return certify_operational_interface_inflation(
        system=canonical.system,
        domain_states=canonical.embedding,
        base_words=base_words,
        closed_word_families=closed_word_families,
        open_only_words=open_only_words,
    )


def test_hidden_open_only_bit_adds_innovation_beyond_closed_join_capacity():
    # State = (inside y, closed bit b1, closed bit b2, hidden-open bit h).
    codebook = tuple(product((0, 1), repeat=4))
    certificate = _operational_certificate(codebook, closed_coordinates=(1, 2), open_only_coordinates=(3,))

    assert certificate.verify()
    assert certificate.decomposition.closed_block_counts == (4, 4)
    assert certificate.decomposition.fibered_capacity_state_count == 8
    assert certificate.decomposition.union_block_count == 8
    assert certificate.decomposition.open_block_count == 16
    assert certificate.join_realizability_defect_bits == pytest.approx(0.0)
    assert certificate.new_word_innovation_bits == pytest.approx(1.0)
    assert certificate.total_noncommutation_gap_bits == pytest.approx(2.0)

    witness = certificate.first_open_only_split_witness
    assert witness is not None
    assert witness.verify(certificate.system)
    assert witness.separating_word == certificate.open_only_words[0]


def test_join_defect_and_new_word_innovation_are_independent_terms():
    # (y,b1,b2) is even parity, while hidden h is free.
    codebook = tuple(
        bits + (hidden,)
        for bits in product((0, 1), repeat=3)
        if sum(bits) % 2 == 0
        for hidden in (0, 1)
    )
    certificate = _operational_certificate(codebook, closed_coordinates=(1, 2), open_only_coordinates=(3,))

    # Closed capacity: 2 shared-base states * 2 * 2 refinements = 8.
    # Closed union realizes only the four parity-compatible (y,b1,b2) tuples.
    # The open-only h read doubles those four union blocks to eight.
    assert certificate.decomposition.fibered_capacity_state_count == 8
    assert certificate.decomposition.union_block_count == 4
    assert certificate.decomposition.open_block_count == 8
    assert certificate.join_realizability_defect_bits == pytest.approx(1.0)
    assert certificate.new_word_innovation_bits == pytest.approx(1.0)
    assert certificate.decomposition.capacity_gap_bits == pytest.approx(1.0)
    assert certificate.total_noncommutation_gap_bits == pytest.approx(1.0)
    assert certificate.total_noncommutation_gap_bits == pytest.approx(
        certificate.decomposition.capacity_gap_bits
        - certificate.join_realizability_defect_bits
        + certificate.new_word_innovation_bits
    )


def test_no_open_only_words_means_zero_innovation_and_no_split_witness():
    codebook = tuple(product((0, 1), repeat=3))
    certificate = _operational_certificate(codebook, closed_coordinates=(1, 2), open_only_coordinates=())

    assert certificate.verify()
    assert certificate.new_word_innovation_bits == pytest.approx(0.0)
    assert certificate.first_open_only_split_witness is None
    assert certificate.decomposition.open_block_count == certificate.decomposition.union_block_count


def test_partition_level_certificate_detects_positive_innovation_iff_open_splits_union_fiber():
    # Shared base y, two closed views (y,b1), (y,b2), then hidden h in open labels.
    states = tuple(product((0, 1), repeat=4))
    base = tuple(state[0] for state in states)
    closed = (
        tuple((state[0], state[1]) for state in states),
        tuple((state[0], state[2]) for state in states),
    )
    open_labels = tuple(state for state in states)
    certificate = certify_interface_inflation_decomposition(base, closed, open_labels)

    assert certificate.verify()
    assert certificate.join_realizability_defect_bits == pytest.approx(0.0)
    assert certificate.new_word_innovation_bits == pytest.approx(1.0)
    assert certificate.has_new_word_innovation
    assert certificate.first_innovation_split_indices is not None


def test_open_partition_cannot_merge_states_already_separated_by_closed_union():
    base = (0, 0, 0, 0)
    closed = ((0, 0, 1, 1),)
    # Open labels merge indices 0 and 2 although the closed union separates them.
    with pytest.raises(ValueError, match="does not refine"):
        certify_interface_inflation_decomposition(base, closed, ("x", "y", "x", "z"))


def test_open_only_word_must_actually_be_new_relative_to_closed_union():
    codebook = tuple(product((0, 1), repeat=3))
    canonical = build_canonical_operational_codebook(codebook)
    read_inside = canonical.coordinate_words[0]
    read_b1 = canonical.coordinate_words[1]

    with pytest.raises(ValueError, match="does not verify"):
        certify_operational_interface_inflation(
            system=canonical.system,
            domain_states=canonical.embedding,
            base_words=(read_inside,),
            closed_word_families=((read_inside, read_b1),),
            open_only_words=(read_b1,),
        )


def test_inflation_certificates_are_public_portability_exports():
    assert portability.certify_interface_inflation_decomposition is certify_interface_inflation_decomposition
    assert portability.certify_operational_interface_inflation is certify_operational_interface_inflation
    assert "InterfaceInflationDecompositionCertificate" in portability.__all__
    assert "OperationalInterfaceInflationCertificate" in portability.__all__
