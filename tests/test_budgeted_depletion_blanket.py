import pytest
from causal_model.budgeted_depletion_blanket import budgeted_depletion_grammar, certify_budgeted_depletion_blanket


def test_zero_budget_recovers_saturation_blanket():
    certificate = certify_budgeted_depletion_blanket(8, 2, 0)
    assert certificate.verify()
    assert certificate.initial_interface_state_count == 3
    assert certificate.expected_product_block_count == 3
    assert certificate.disturbance_memory_inflation_bits == 0.0


def test_each_future_depletion_adds_one_initial_abundance_class():
    certificates = [certify_budgeted_depletion_blanket(10, 2, budget) for budget in range(5)]
    assert all(certificate.verify() for certificate in certificates)
    assert [certificate.initial_interface_state_count for certificate in certificates] == [3, 4, 5, 6, 7]


def test_budget_covering_oversaturation_recovers_full_abundance():
    certificate = certify_budgeted_depletion_blanket(9, 2, 7)
    assert certificate.verify()
    assert certificate.initial_interface_state_count == 10


def test_product_quotient_tracks_remaining_budget():
    certificate = certify_budgeted_depletion_blanket(8, 2, 3)
    assert certificate.verify()
    assert certificate.initial_interface_state_count == 6
    assert certificate.expected_product_block_count == 3 + 4 + 5 + 6


def test_grammar_spends_depletion_budget():
    grammar = budgeted_depletion_grammar(2)
    assert grammar.legal_actions(0) == ("colonize", "deplete")
    assert grammar.legal_actions(2) == ("colonize",)
    assert grammar.transition(0, "deplete") == 1
    assert grammar.transition(1, "deplete") == 2
    with pytest.raises(ValueError):
        grammar.transition(2, "deplete")


def test_capacity_must_cover_threshold_plus_budget():
    with pytest.raises(ValueError):
        certify_budgeted_depletion_blanket(4, 2, 3)
