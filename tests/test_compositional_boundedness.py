from math import log2

import pytest

from causal_model.compositional_boundedness import (
    UniformFactorizationStage,
    certify_binary_relay_growth,
    certify_cumulative_addressability_chain,
    certify_inert_attachment_boundedness,
    certify_uniform_dynamic_blanket_chain,
    inert_attachment_stage,
)


def test_uniform_dynamic_blanket_bounds_growing_inert_composition_by_one_state():
    certificate = certify_inert_attachment_boundedness(5)
    assert certificate.verify()
    assert certificate.summary_state_bound == 1
    assert certificate.canonical_block_counts == (1, 1, 1, 1, 1)
    assert certificate.summary_bits_bound == 0.0
    assert certificate.maximum_canonical_bits == 0.0
    assert [stage.constrained_system.system.state_count for stage in certificate.stages] == [2, 4, 8, 16, 32]


def test_uniform_factorization_uses_one_common_codomain_across_different_stage_domains():
    actions = ("observe", "connect")
    stages = tuple(inert_attachment_stage(m, actions) for m in (1, 3, 4))
    certificate = certify_uniform_dynamic_blanket_chain((0,), stages)
    assert certificate.verify()
    assert certificate.canonical_block_counts == (1, 1, 1)
    assert all(stage.used_summary_labels == (0,) for stage in stages)


def test_uniform_chain_rejects_a_label_outside_the_declared_common_summary_alphabet():
    stage = inert_attachment_stage(1, ("observe", "connect"))
    invalid = UniformFactorizationStage(
        constrained_system=stage.constrained_system,
        summary_labels=(0, 1),
    )
    with pytest.raises(ValueError, match="uniform grammar-aware"):
        certify_uniform_dynamic_blanket_chain((0,), (invalid,))


def test_cumulative_addressability_has_exact_product_prefix_lower_bounds():
    certificate = certify_cumulative_addressability_chain(2, (2, 3, 2))
    assert certificate.verify()
    assert certificate.open_state_lower_bounds == (4, 12, 24)
    assert certificate.open_bits_lower_bounds == (2.0, log2(12), log2(24))
    assert certificate.incremental_bits == (1.0, log2(3), 1.0)


def test_binary_modules_force_linear_growth_in_the_product_lower_bound():
    certificate = certify_cumulative_addressability_chain(2, (2, 2, 2, 2, 2))
    assert certificate.verify()
    assert certificate.open_bits_lower_bounds == (2.0, 3.0, 4.0, 5.0, 6.0)


@pytest.mark.parametrize("maximum_module_count", [1, 2, 3, 5])
def test_relay_tree_attains_the_cumulative_binary_product_bound(maximum_module_count):
    certificate = certify_binary_relay_growth(maximum_module_count)
    assert certificate.verify()
    assert certificate.addressability_chain.open_bits_lower_bounds == tuple(
        float(module_count + 1) for module_count in range(1, maximum_module_count + 1)
    )
    assert [relay.open_bits for relay in certificate.relay_stages] == list(
        certificate.addressability_chain.open_bits_lower_bounds
    )


def test_positive_and_negative_criteria_are_conditional_not_a_false_universal_partition():
    bounded = certify_inert_attachment_boundedness(4)
    growth = certify_cumulative_addressability_chain(2, (2, 2, 2, 2))
    assert bounded.verify() and growth.verify()
    assert bounded.maximum_canonical_bits == 0.0
    assert growth.open_bits_lower_bounds[-1] == 5.0


def test_invalid_cardinalities_and_empty_chains_fail_closed():
    with pytest.raises(ValueError, match="positive"):
        certify_inert_attachment_boundedness(0)
    with pytest.raises(ValueError, match="at least one"):
        certify_cumulative_addressability_chain(2, ())
    with pytest.raises(ValueError, match="at least two"):
        certify_cumulative_addressability_chain(2, (1, 2))
    with pytest.raises(ValueError, match="at least one"):
        certify_uniform_dynamic_blanket_chain((0,), ())
