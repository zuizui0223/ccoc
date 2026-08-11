"""Tests for absolute innovation capacity and local-query latency bounds."""

import math

import pytest

import causal_model.portability_core as portability
from causal_model.innovation_capacity_latency import (
    certify_innovation_capacity,
    certify_prefix_free_address_latency,
    certify_relay_local_latency,
    certify_single_action_sharpness_closure,
)


def test_absolute_innovation_capacity_has_exact_slack_identity():
    certificate = certify_innovation_capacity(
        domain_state_count=64,
        closed_union_block_count=4,
        open_block_count=16,
    )

    assert certificate.verify()
    assert certificate.actual_innovation_bits == pytest.approx(2.0)
    assert certificate.maximum_innovation_bits == pytest.approx(4.0)
    assert certificate.unused_innovation_capacity_bits == pytest.approx(2.0)
    assert not certificate.saturates_absolute_capacity
    assert certificate.maximum_innovation_bits == pytest.approx(
        certificate.actual_innovation_bits + certificate.unused_innovation_capacity_bits
    )


def test_absolute_capacity_is_saturated_exactly_by_discrete_open_quotient():
    saturated = certify_innovation_capacity(32, 2, 32)
    nonsaturated = certify_innovation_capacity(32, 2, 16)

    assert saturated.saturates_absolute_capacity
    assert saturated.actual_innovation_bits == pytest.approx(4.0)
    assert saturated.unused_innovation_capacity_bits == pytest.approx(0.0)
    assert not nonsaturated.saturates_absolute_capacity


@pytest.mark.parametrize(
    ("domain", "closed", "open_blocks"),
    [
        (0, 1, 1),
        (8, 0, 1),
        (8, 4, 2),
        (8, 2, 9),
        (True, 1, 1),
    ],
)
def test_invalid_innovation_counts_fail_closed(domain, closed, open_blocks):
    with pytest.raises(ValueError, match="innovation block counts"):
        certify_innovation_capacity(domain, closed, open_blocks)


def test_prefix_free_binary_addresses_meet_kraft_and_logarithmic_lower_bound():
    certificate = certify_prefix_free_address_latency(
        alphabet=("0", "1"),
        addresses=(("0", "0"), ("0", "1"), ("1", "0"), ("1", "1")),
    )

    assert certificate.verify()
    assert certificate.terminal_count == 4
    assert certificate.minimum_worst_case_address_length == 2
    assert certificate.actual_worst_case_address_length == 2
    assert certificate.latency_slack_steps == 0
    assert certificate.kraft_numerator == certificate.kraft_denominator


def test_prefix_free_variable_length_code_obeys_lower_bound_with_slack():
    certificate = certify_prefix_free_address_latency(
        alphabet=("0", "1"),
        addresses=(("0",), ("1", "0"), ("1", "1", "0"), ("1", "1", "1")),
    )

    assert certificate.verify()
    assert certificate.minimum_worst_case_address_length == 2
    assert certificate.actual_worst_case_address_length == 3
    assert certificate.latency_slack_steps == 1
    assert certificate.kraft_numerator == certificate.kraft_denominator


def test_non_prefix_free_addresses_fail_closed():
    with pytest.raises(ValueError, match="prefix-free"):
        certify_prefix_free_address_latency(
            alphabet=("0", "1"),
            addresses=(("0",), ("0", "1")),
        )


def test_balanced_relay_exactly_attains_local_architecture_latency_bound():
    for module_count in (2, 4, 8):
        certificate = certify_relay_local_latency(module_count)
        expected_depth = int(math.log2(module_count))

        assert certificate.verify()
        assert certificate.address_certificate.minimum_worst_case_address_length == expected_depth
        assert certificate.actual_worst_case_probe_length == 2 * expected_depth + 2
        assert certificate.architecture_asymptotic_lower_bound == 2 * expected_depth + 2
        assert certificate.saturates_architecture_latency_bound
        assert all(
            actual == lower
            for actual, lower in zip(
                certificate.actual_probe_lengths,
                certificate.per_port_local_lower_bounds,
            )
        )
        assert all(
            response_distance == address_depth + 1
            for response_distance, address_depth in zip(
                certificate.response_distances,
                certificate.selector_depths,
            )
        )


def test_single_action_family_saturates_both_memory_and_latency_bounds():
    for module_count in (2, 4, 8):
        certificate = certify_single_action_sharpness_closure(module_count)

        assert certificate.verify()
        assert certificate.capacity.saturates_absolute_capacity
        assert certificate.capacity.actual_innovation_bits == pytest.approx(module_count)
        assert certificate.capacity.maximum_innovation_bits == pytest.approx(module_count)
        assert certificate.latency.saturates_architecture_latency_bound
        assert certificate.innovation.open_only_innovation_bits == pytest.approx(module_count)
        assert certificate.innovation.closed_context_block_counts == (2,) * module_count


@pytest.mark.parametrize("bad_count", [0, 1, 3, 6, -2, True, 4.0, "4"])
def test_relay_latency_family_rejects_non_power_of_two_sizes(bad_count):
    with pytest.raises(ValueError, match="power of two"):
        certify_relay_local_latency(bad_count)


def test_capacity_latency_certificates_are_public_portability_exports():
    assert portability.certify_innovation_capacity is certify_innovation_capacity
    assert portability.certify_prefix_free_address_latency is certify_prefix_free_address_latency
    assert portability.certify_relay_local_latency is certify_relay_local_latency
    assert portability.certify_single_action_sharpness_closure is certify_single_action_sharpness_closure
    assert "InnovationCapacityCertificate" in portability.__all__
    assert "RelayLocalLatencyCertificate" in portability.__all__
    assert "SingleActionSharpnessClosureCertificate" in portability.__all__
