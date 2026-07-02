"""Tests for system-specific addressability and closed-context certificates."""

import math

import pytest

import causal_model.portability_core as portability
from causal_model.operational_addressability import (
    certify_canonical_operational_product,
    certify_operational_closed_context_factorization,
    standard_closed_projection,
)


def test_operational_product_certificate_checks_real_decoder_traces():
    certificate = certify_canonical_operational_product(inside_cardinality=2, exterior_cardinalities=(2, 3))

    assert certificate.verify()
    assert certificate.product_state_count == 12
    assert certificate.open_state_lower_bound == 12
    assert certificate.open_bits_lower_bound == math.log2(12)
    assert certificate.checked_distinct_pairs == 66

    # Coordinate decoders must work independently of all other coordinates.
    assert certificate.inside_decoder(certificate.trace((1, 0, 2), certificate.inside_word)) == 1
    assert certificate.exterior_decoders[0](certificate.trace((1, 0, 2), certificate.exterior_words[0])) == 0
    assert certificate.exterior_decoders[1](certificate.trace((1, 0, 2), certificate.exterior_words[1])) == 2


def test_standard_closed_context_factorizations_recover_the_noncommutation_gap():
    open_certificate = certify_canonical_operational_product(inside_cardinality=2, exterior_cardinalities=(2, 3))

    closed = certify_operational_closed_context_factorization(
        open_certificate=open_certificate,
        closed_words=(
            ((), open_certificate.inside_word, open_certificate.exterior_words[0]),
            ((), open_certificate.inside_word, open_certificate.exterior_words[1]),
        ),
        closed_factor_maps=(standard_closed_projection(0), standard_closed_projection(1)),
    )

    assert closed.verify()
    assert closed.factor_label_counts == (4, 6)
    assert closed.closed_interface_upper_bits == (2.0, math.log2(6))
    assert closed.noncommutation_gap_lower_bound == pytest.approx(1.0)


def test_factorization_rejects_a_summary_that_forgets_a_readable_closed_coordinate():
    open_certificate = certify_canonical_operational_product(inside_cardinality=2, exterior_cardinalities=(2, 2))

    with pytest.raises(ValueError, match="factorization"):
        certify_operational_closed_context_factorization(
            open_certificate=open_certificate,
            closed_words=(
                ((), open_certificate.inside_word, open_certificate.exterior_words[0]),
                ((), open_certificate.inside_word, open_certificate.exterior_words[1]),
            ),
            closed_factor_maps=(lambda _state: "collapsed", standard_closed_projection(1)),
        )


def test_operational_certificates_are_part_of_the_portability_public_surface():
    assert portability.certify_canonical_operational_product is certify_canonical_operational_product
    assert portability.certify_operational_closed_context_factorization is certify_operational_closed_context_factorization
    assert "OperationalAddressableProductCertificate" in portability.__all__
    assert "OperationalClosedContextFactorizationCertificate" in portability.__all__
