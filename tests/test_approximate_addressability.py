"""Tests for approximate codebook addressability and Fano robustness bounds."""

import math
from itertools import product

import pytest

from causal_model.approximate_addressability import (
    binary_entropy,
    certify_approximate_addressable_codebook,
    fano_codebook_lower_bound,
    fano_coordinate_penalty,
    full_binary_product_fano_lower_bound,
)


def test_exact_summary_recovers_exact_codebook_memory_bound():
    codebook = tuple(product((0, 1), repeat=3))
    certificate = certify_approximate_addressable_codebook(
        codebook=codebook,
        summary_labels=codebook,
        coordinate_decoders=(lambda label: label[0], lambda label: label[1], lambda label: label[2]),
        error_tolerances=(0.0, 0.0, 0.0),
    )

    assert certificate.verify()
    assert certificate.empirical_coordinate_errors == (0.0, 0.0, 0.0)
    assert certificate.summary_state_count == 8
    assert certificate.summary_bits == 3.0
    assert certificate.contract_open_bits_lower_bound == 3.0
    assert certificate.empirical_open_bits_lower_bound == 3.0
    assert certificate.minimum_summary_state_count_from_contract == 8
    assert certificate.information_slack_bits == 0.0


def test_dropping_one_binary_coordinate_saturates_the_fano_bound_at_half_error():
    codebook = tuple(product((0, 1), repeat=4))
    summary_labels = tuple(codeword[:3] for codeword in codebook)
    certificate = certify_approximate_addressable_codebook(
        codebook=codebook,
        summary_labels=summary_labels,
        coordinate_decoders=(
            lambda label: label[0],
            lambda label: label[1],
            lambda label: label[2],
            lambda _label: 0,
        ),
        error_tolerances=(0.0, 0.0, 0.0, 0.5),
    )

    assert certificate.empirical_coordinate_errors == (0.0, 0.0, 0.0, 0.5)
    assert certificate.summary_state_count == 8
    assert certificate.summary_bits == 3.0
    assert certificate.contract_fano_penalty_bits == 1.0
    assert certificate.contract_open_bits_lower_bound == 3.0
    assert certificate.empirical_open_bits_lower_bound == 3.0
    assert certificate.information_slack_bits == 0.0


def test_binary_full_product_retains_linear_memory_at_fixed_error():
    error = 0.1
    retained_bits_per_exterior = 1.0 - binary_entropy(error)

    for exterior_count in range(1, 9):
        bound = full_binary_product_fano_lower_bound(exterior_count, error)
        assert bound == pytest.approx(1.0 + exterior_count * retained_bits_per_exterior)

    assert retained_bits_per_exterior > 0.0


def test_general_codebook_bound_uses_actual_realized_coordinate_alphabets():
    codebook = (
        (0, "a", 0),
        (0, "b", 1),
        (1, "a", 1),
        (1, "b", 0),
    )
    error = 0.1
    expected = math.log2(len(codebook)) - 3 * binary_entropy(error)

    assert fano_codebook_lower_bound(codebook, (error, error, error)) == pytest.approx(expected)


def test_nonbinary_random_guess_ceiling_can_erase_one_coordinate_completely():
    codebook = tuple((inside, exterior) for inside in (0, 1) for exterior in range(4))
    summary_labels = tuple((inside,) for inside, _exterior in codebook)
    certificate = certify_approximate_addressable_codebook(
        codebook=codebook,
        summary_labels=summary_labels,
        coordinate_decoders=(lambda label: label[0], lambda _label: 0),
        error_tolerances=(0.0, 0.75),
    )

    assert certificate.empirical_coordinate_errors == (0.0, 0.75)
    assert fano_coordinate_penalty(0.75, 4) == pytest.approx(2.0)
    assert certificate.contract_open_bits_lower_bound == pytest.approx(1.0)
    assert certificate.summary_bits == pytest.approx(1.0)


def test_certificate_rejects_a_tolerance_smaller_than_the_measured_error():
    codebook = tuple(product((0, 1), repeat=3))
    summary_labels = tuple(codeword[:2] for codeword in codebook)

    with pytest.raises(ValueError, match="approximate addressability witness"):
        certify_approximate_addressable_codebook(
            codebook=codebook,
            summary_labels=summary_labels,
            coordinate_decoders=(lambda label: label[0], lambda label: label[1], lambda _label: 0),
            error_tolerances=(0.0, 0.0, 0.49),
        )


def test_binary_contract_rejects_error_above_random_guess_ceiling():
    with pytest.raises(ValueError, match="\[0, 0.5\]"):
        full_binary_product_fano_lower_bound(4, 0.5001)
