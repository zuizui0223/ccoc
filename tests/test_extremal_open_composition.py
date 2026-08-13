import pytest

import causal_model.portability_core as core
from causal_model.extremal_open_composition import (
    FixedRegularExtremalTheoremCertificate,
    certify_fixed_regular_extremal_theorem,
)


def test_extremal_theorem_certificate_aggregates_all_simultaneous_clauses() -> None:
    for module_count in (1, 2, 3, 4, 5):
        certificate = certify_fixed_regular_extremal_theorem(module_count)

        assert isinstance(certificate, FixedRegularExtremalTheoremCertificate)
        assert certificate.verify()
        assert certificate.comparison_domain_state_count == 2 ** (module_count + 1)
        assert certificate.action_alphabet_size == 4
        assert certificate.closed_grammar_state_count == 1
        assert certificate.open_grammar_state_count == 1
        assert certificate.newly_legal_action_count == 1
        assert certificate.grammar_transition_difference_count == 1
        assert certificate.closed_interface_state_count == 2
        assert certificate.open_interface_state_count == 2 ** (module_count + 1)
        assert certificate.open_only_innovation_bits == module_count
        assert certificate.finite_domain_maximum_innovation_bits == module_count
        assert certificate.innovation_slack_bits == 0
        assert certificate.exterior_response_lower_bound_bits == module_count
        assert certificate.exterior_response_lower_bound_state_count == 2 ** module_count
        assert certificate.maximum_degree <= 3
        assert certificate.focal_exterior_cut_width == 1
        assert certificate.is_tree_topology
        assert certificate.selector_augmented_relay_state_count <= 6
        assert certificate.selector_augmented_leaf_state_count <= 12
        assert certificate.worst_canonical_query_length == certificate.exact_worst_query_formula


def test_extremal_theorem_aggregation_is_public() -> None:
    assert core.FixedRegularExtremalTheoremCertificate is FixedRegularExtremalTheoremCertificate
    assert core.certify_fixed_regular_extremal_theorem is certify_fixed_regular_extremal_theorem


def test_extremal_theorem_fails_closed_on_invalid_m() -> None:
    with pytest.raises(ValueError):
        certify_fixed_regular_extremal_theorem(0)
