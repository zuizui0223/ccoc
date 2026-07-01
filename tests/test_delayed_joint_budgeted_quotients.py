import pytest

from causal_model.delayed_joint_nonidentifiability import DelayedJointAction, DelayedJointFamily
from causal_model.delayed_joint_budgeted_quotients import (
    canonical_covered_panel,
    certify_action_budget_frontier,
    certify_depth_budget_frontier,
    certify_marginal_probe_value,
    certify_panel_quotient,
    certify_trial_budget_frontier,
    exhaustive_budgeted_quotient_summary,
    terminal_probe_coverage,
)
from causal_model.delayed_joint_reset_panels import ResettableTrialPanel, required_terminal_words


def test_arbitrary_panel_quotient_is_exactly_its_covered_coordinate_projection():
    family = DelayedJointFamily(exterior_port_count=3, delay=2)
    read_zero, read_one, read_two, intervene = required_terminal_words(family)
    panel_words = (
        (DelayedJointAction.wait(),),
        read_two,
        read_zero,
        read_zero,
        (DelayedJointAction.wait(), DelayedJointAction.wait()),
        intervene,
    )
    certificate = certify_panel_quotient(family, panel_words)
    assert certificate.verify()
    assert certificate.coverage.read_ports == (0, 2)
    assert certificate.coverage.covers_intervention
    assert certificate.retained_interface_bits == 4
    assert certificate.signature_block_count == 16
    assert certificate.minimum_signature_block_cardinality == 4
    assert certificate.maximum_signature_block_cardinality == 4

    # Uncovered b_1 is exactly the remaining ambiguity factor.
    left = (0, 0, 0, 0, 0)
    right = (0, 0, 1, 0, 0)
    assert certificate.panel.signature(left) == certificate.panel.signature(right)
    # Covered b_0, b_2, and response type are separated.
    assert certificate.panel.signature(left) != certificate.panel.signature((0, 1, 0, 0, 0))
    assert certificate.panel.signature(left) != certificate.panel.signature((0, 0, 0, 1, 0))
    assert certificate.panel.signature(left) != certificate.panel.signature((0, 0, 0, 0, 1))


def test_empty_wait_only_and_duplicate_panels_all_have_only_the_focal_two_block_quotient():
    family = DelayedJointFamily(exterior_port_count=2, delay=2)
    read_zero, _, _ = required_terminal_words(family)
    panels = (
        (),
        ((DelayedJointAction.wait(),), (DelayedJointAction.wait(), DelayedJointAction.wait())),
        (read_zero, read_zero),
    )
    expected_bits = (1, 1, 2)
    for words, bits in zip(panels, expected_bits):
        certificate = certify_panel_quotient(family, words)
        assert certificate.verify()
        assert certificate.retained_interface_bits == bits
        assert certificate.signature_block_count == 2**bits


def test_coverage_extraction_ignores_trial_order_and_multiplicity():
    family = DelayedJointFamily(exterior_port_count=3, delay=1)
    read_zero, read_one, _, intervene = required_terminal_words(family)
    first = ResettableTrialPanel(family, (read_one, intervene, read_zero, read_zero))
    second = ResettableTrialPanel(family, (read_zero, read_one, intervene))
    first_coverage = terminal_probe_coverage(first)
    second_coverage = terminal_probe_coverage(second)
    assert first_coverage == second_coverage
    assert first_coverage.read_ports == (0, 1)
    assert first_coverage.covers_intervention


@pytest.mark.parametrize("trial_budget", range(0, 7))
def test_trial_budget_frontier_is_sharp(trial_budget):
    certificate = certify_trial_budget_frontier(exterior_port_count=3, delay=2, trial_budget=trial_budget)
    assert certificate.verify()
    expected_bits = 1 + min(trial_budget, 4)
    assert certificate.maximum_retained_interface_bits == expected_bits
    assert certificate.construction.retained_interface_bits == expected_bits
    assert certificate.construction.panel.trial_count <= trial_budget
    assert certificate.construction.expected_residual_block_cardinality == 2 ** (5 - expected_bits)


@pytest.mark.parametrize("action_budget", range(0, 16))
def test_action_budget_frontier_is_sharp(action_budget):
    # With H=2, each information-bearing terminal probe costs exactly three actions.
    certificate = certify_action_budget_frontier(exterior_port_count=3, delay=2, action_budget=action_budget)
    assert certificate.verify()
    expected_probes = min(action_budget // 3, 4)
    assert certificate.maximum_retained_interface_bits == 1 + expected_probes
    assert certificate.construction.panel.total_action_count <= action_budget


@pytest.mark.parametrize("depth_budget", range(0, 6))
def test_depth_frontier_has_a_hard_gate_at_the_first_terminal_boundary(depth_budget):
    certificate = certify_depth_budget_frontier(exterior_port_count=2, delay=3, maximum_trial_horizon=depth_budget)
    assert certificate.verify()
    expected_bits = 1 if depth_budget < 4 else 4
    assert certificate.maximum_retained_interface_bits == expected_bits
    assert certificate.construction.retained_interface_bits == expected_bits


def test_new_terminal_probe_has_exact_one_bit_marginal_value_and_halves_ambiguity():
    family = DelayedJointFamily(exterior_port_count=2, delay=1)
    read_zero, read_one, intervene = required_terminal_words(family)

    first = certify_marginal_probe_value(family, (), read_zero)
    second = certify_marginal_probe_value(family, (read_zero,), intervene)
    third = certify_marginal_probe_value(family, (read_zero, intervene), read_one)
    for certificate, kind in ((first, "read"), (second, "intervene"), (third, "read")):
        assert certificate.verify()
        assert certificate.coverage_kind == kind
        assert certificate.delta_retained_interface_bits == 1
        assert certificate.residual_ambiguity_ratio == 2


def test_duplicate_or_wait_only_trial_has_zero_marginal_value():
    family = DelayedJointFamily(exterior_port_count=2, delay=1)
    read_zero, _, _ = required_terminal_words(family)
    duplicate = certify_marginal_probe_value(family, (read_zero,), read_zero)
    wait_only = certify_marginal_probe_value(family, (read_zero,), (DelayedJointAction.wait(),))
    for certificate in (duplicate, wait_only):
        assert certificate.verify()
        assert certificate.coverage_kind == "wait_or_duplicate"
        assert certificate.delta_retained_interface_bits == 0
        assert certificate.residual_ambiguity_ratio == 1


def test_marginal_value_saturates_after_full_identification():
    family = DelayedJointFamily(exterior_port_count=1, delay=2)
    read_zero, intervene = required_terminal_words(family)
    certificate = certify_marginal_probe_value(family, (read_zero, intervene), read_zero)
    assert certificate.verify()
    assert certificate.initial.coverage.is_full
    assert certificate.updated.coverage.is_full
    assert certificate.delta_retained_interface_bits == 0
    assert certificate.residual_ambiguity_ratio == 1


def test_canonical_covered_panels_trace_the_full_quotient_ladder():
    family = DelayedJointFamily(exterior_port_count=3, delay=1)
    bits = []
    residuals = []
    for probe_count in range(6):
        panel = canonical_covered_panel(family, probe_count)
        certificate = certify_panel_quotient(family, panel.trial_words)
        bits.append(certificate.retained_interface_bits)
        residuals.append(certificate.expected_residual_block_cardinality)
    assert bits == [1, 2, 3, 4, 5, 5]
    assert residuals == [16, 8, 4, 2, 1, 1]


def test_terminal_events_cannot_be_packed_into_one_nonreset_trial():
    family = DelayedJointFamily(exterior_port_count=1, delay=1)
    read_zero, intervene = required_terminal_words(family)
    with pytest.raises(ValueError, match="illegal"):
        certify_panel_quotient(family, (read_zero + intervene,))


def test_illegal_trial_words_fail_closed():
    family = DelayedJointFamily(exterior_port_count=1, delay=1)
    with pytest.raises((TypeError, ValueError)):
        certify_panel_quotient(family, ((DelayedJointAction.read(9),),))
    with pytest.raises((TypeError, ValueError)):
        certify_marginal_probe_value(family, (), ("not-an-action",))


def test_exhaustive_small_budgeted_quotient_certificate_replay():
    certificates = exhaustive_budgeted_quotient_summary(
        max_exterior_port_count=3,
        max_delay=2,
        max_budget=4,
    )
    assert certificates
    assert all(certificate.verify() for certificate in certificates)
