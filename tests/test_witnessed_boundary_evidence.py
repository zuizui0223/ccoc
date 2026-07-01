import pytest

from causal_model.canonical_boundary_blankets import redundant_exterior_response_table
from causal_model.witnessed_boundary_evidence import (
    certify_completion_coverage,
    certify_evidence_chain,
    certify_free_completion_extension,
    certify_witnessed_boundary_lower_bound,
)


def test_observed_separation_has_a_witnessed_lower_bound_on_canonical_blanket_size():
    system = redundant_exterior_response_table()
    certificate = certify_witnessed_boundary_lower_bound(
        system,
        ("observe", "read"),
        (0, 2),
        ((0, "read"),),
    )
    assert certificate.verify()
    assert certificate.observed_labels == (0, 1)
    assert certificate.observed_class_count == 2
    assert certificate.canonical_blanket_count == 2
    assert certificate.lower_bound_bits == 1.0
    assert len(certificate.separation_witnesses) == 1
    witness = certificate.separation_witnesses[0]
    assert witness.inside == 0
    assert witness.word == "read"
    assert witness.left_response != witness.right_response


def test_partial_panel_yields_a_valid_strict_lower_bound_not_an_exactness_claim():
    system = redundant_exterior_response_table()
    certificate = certify_witnessed_boundary_lower_bound(
        system,
        ("observe", "read"),
        (0, 2),
        ((0, "observe"),),
    )
    assert certificate.verify()
    assert certificate.observed_class_count == 1
    assert certificate.canonical_blanket_count == 2
    assert certificate.lower_bound_bits == 0.0
    assert not certificate.separation_witnesses


def test_witnessed_lower_bound_is_monotone_under_nested_samples_and_panels():
    system = redundant_exterior_response_table()
    chain = certify_evidence_chain(
        system,
        ("observe", "read"),
        (
            ((0,), ((0, "observe"),)),
            ((0, 2), ((0, "observe"),)),
            ((0, 2), ((0, "observe"), (0, "read"))),
            ((0, 1, 2, 3), ((0, "observe"), (0, "read"))),
        ),
    )
    assert chain.verify()
    assert chain.lower_bound_counts == (1, 1, 2, 2)


def test_nonnested_evidence_chain_is_rejected():
    system = redundant_exterior_response_table()
    with pytest.raises(AssertionError, match="certificate did not verify"):
        certify_evidence_chain(
            system,
            ("observe", "read"),
            (
                ((0, 2), ((0, "observe"), (0, "read"))),
                ((0,), ((0, "observe"), (0, "read"))),
            ),
        )


def test_completion_coverage_plus_full_grammar_panel_proves_exact_blanket_size():
    system = redundant_exterior_response_table()
    coverage = certify_completion_coverage(system, ("observe", "read"), (0, 2))
    assert coverage.verify()
    assert coverage.sampled_canonical_labels == (0, 1)
    assert coverage.canonical_blanket_count == 2
    assert coverage.exact_observed_class_count == 2
    assert coverage.observed_cells == (
        (0, "observe"),
        (0, "read"),
        (1, "observe"),
        (1, "read"),
    )


def test_missing_canonical_class_cannot_be_mislabeled_as_completion_coverage():
    system = redundant_exterior_response_table()
    with pytest.raises(ValueError, match="do not cover"):
        certify_completion_coverage(system, ("observe", "read"), (0,))


@pytest.mark.parametrize("fresh_count", [1, 2, 5])
def test_free_completion_extension_preserves_transcript_but_adds_exactly_requested_new_blanket_classes(fresh_count):
    system = redundant_exterior_response_table()
    certificate = certify_free_completion_extension(
        system,
        sampled_exteriors=(0, 2),
        observed_cells=((0, "observe"), (0, "read")),
        baseline_exterior=0,
        fresh_completion_count=fresh_count,
    )
    assert certificate.verify()
    assert certificate.original_blanket_count == 2
    assert certificate.extended_blanket_count == 2 + fresh_count
    assert len(certificate.fresh_words) == fresh_count
    assert len(certificate.new_exteriors) == fresh_count

    # All newly admitted completions have exactly the baseline transcript on the
    # finite tested panel, despite becoming new response classes under fresh words.
    for exterior in certificate.new_exteriors:
        for inside, word in certificate.observed_cells:
            assert certificate.extended_system.response(inside, exterior, word) == system.response(
                inside, certificate.baseline_exterior, word
            )


def test_free_completion_no_go_can_outgrow_any_observed_lower_bound():
    system = redundant_exterior_response_table()
    lower = certify_witnessed_boundary_lower_bound(
        system,
        ("observe", "read"),
        (0,),
        ((0, "observe"),),
    )
    extension = certify_free_completion_extension(
        system,
        sampled_exteriors=(0,),
        observed_cells=((0, "observe"),),
        baseline_exterior=0,
        fresh_completion_count=7,
    )
    assert lower.verify() and extension.verify()
    assert lower.observed_class_count == 1
    assert extension.extended_blanket_count == 9


def test_extension_requires_baseline_to_be_in_the_observed_sample():
    system = redundant_exterior_response_table()
    with pytest.raises(ValueError, match="among sampled"):
        certify_free_completion_extension(
            system,
            sampled_exteriors=(1, 2),
            observed_cells=((0, "observe"),),
            baseline_exterior=0,
            fresh_completion_count=2,
        )


def test_invalid_samples_panels_and_grammar_membership_fail_closed():
    system = redundant_exterior_response_table()
    with pytest.raises(ValueError, match="sorted"):
        certify_witnessed_boundary_lower_bound(
            system,
            ("observe", "read"),
            (2, 0),
            ((0, "read"),),
        )
    with pytest.raises(ValueError, match="unique"):
        certify_witnessed_boundary_lower_bound(
            system,
            ("observe", "read"),
            (0, 2),
            ((0, "read"), (0, "read")),
        )
    with pytest.raises(ValueError, match="declared grammar"):
        certify_witnessed_boundary_lower_bound(
            system,
            ("observe",),
            (0, 2),
            ((0, "read"),),
        )
