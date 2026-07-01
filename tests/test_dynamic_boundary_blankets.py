import math

import pytest

from causal_model.dynamic_boundary_blankets import (
    DynamicInterfaceCertificate,
    FiniteControlledOutputSystem,
    certify_dynamic_boundary_blanket,
    certify_finite_horizon_stabilization,
    certify_uniform_blanket_obstruction,
    delay_chain_system,
    redundant_boundary_system,
)


def test_delay_chain_reaches_its_exact_open_quotient_after_linear_counterfactual_depth():
    system = delay_chain_system(7)
    certificate = certify_finite_horizon_stabilization(system)
    assert certificate.verify()
    assert certificate.stabilization_horizon == 5
    assert certificate.state_count_bound == 6
    assert certificate.partition_block_counts == (2, 3, 4, 5, 6, 7, 7)
    assert certificate.canonical_block_count == 7
    assert math.isclose(certificate.open_interface_bits, math.log2(7))


def test_canonical_open_interface_is_a_dynamic_right_congruence():
    system = delay_chain_system(5)
    certificate = certify_finite_horizon_stabilization(system)
    canonical_labels = system.horizon_labels(certificate.stabilization_horizon)
    assert DynamicInterfaceCertificate(system, canonical_labels).verify()
    assert len(set(canonical_labels)) == certificate.canonical_block_count


def test_redundant_microstate_collapses_to_a_nontrivial_four_state_dynamic_blanket():
    system, inside, boundary = redundant_boundary_system()
    certificate = certify_dynamic_boundary_blanket(system, inside, boundary)
    assert certificate.verify()
    assert certificate.inside_cardinality == 2
    assert certificate.boundary_cardinality == 2
    assert certificate.realized_pair_cardinality == 4
    assert certificate.canonical_block_count == 4
    assert certificate.stabilization_horizon == 1
    assert certificate.realized_horizon_bound == 3
    assert certificate.product_horizon_bound == 3
    assert math.isclose(certificate.open_interface_bits, 2.0)
    assert math.isclose(certificate.blanket_upper_bound_bits, 2.0)


def test_static_inside_summary_that_fails_to_update_is_rejected():
    system, inside, _boundary = redundant_boundary_system()
    assert not DynamicInterfaceCertificate(system, inside).verify()


def test_uniform_blanket_obstruction_recovers_one_external_bit_per_binary_module():
    certificate = certify_uniform_blanket_obstruction((2, 2, 2, 2, 2))
    assert certificate.verify()
    assert certificate.required_boundary_state_count == 16
    assert certificate.required_boundary_bits == 4.0
    assert certificate.open_block_count == 32


def test_nonbinary_uniform_blanket_obstruction_is_product_valued():
    certificate = certify_uniform_blanket_obstruction((3, 2, 5))
    assert certificate.verify()
    assert certificate.required_boundary_state_count == 10
    assert math.isclose(certificate.required_boundary_bits, math.log2(10))
    assert certificate.open_block_count == 30


@pytest.mark.parametrize("bad_size", [0, 1, True, 2.5, "6"])
def test_delay_chain_size_validation_fails_closed(bad_size):
    with pytest.raises(ValueError):
        delay_chain_system(bad_size)


def test_invalid_transition_table_fails_closed():
    with pytest.raises(ValueError, match="transition targets"):
        FiniteControlledOutputSystem(
            actions=("a",),
            transition_table=((1,), (2,)),
            outputs=(0, 1),
        )


def test_invalid_summary_length_fails_closed():
    system = delay_chain_system(3)
    assert not DynamicInterfaceCertificate(system, (0, 1)).verify()
