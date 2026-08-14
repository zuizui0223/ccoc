import pytest

from causal_model.spatial_dispersal_reachability import (
    certify_path_reachability,
    certify_spatial_dispersal_reachability,
    certify_spatial_reachability_family,
    path_to_focal_graph,
)


def test_path_graph_future_horizon_caps_exact_reachability_memory() -> None:
    certificate = certify_path_reachability(maximum_distance=5, spread_horizon=2)
    assert certificate.verify()
    assert certificate.node_count == 6
    assert certificate.occupancy_state_count == 64
    assert certificate.maximum_finite_distance == 5
    assert certificate.initial_exact_block_count == 4
    assert certificate.expected_initial_block_count == 4
    assert certificate.unlimited_exact_block_count == 7
    assert certificate.expected_unlimited_block_count == 7


def test_zero_future_horizon_keeps_only_current_focal_occupancy() -> None:
    certificate = certify_path_reachability(maximum_distance=5, spread_horizon=0)
    assert certificate.verify()
    assert certificate.initial_exact_block_count == 2
    assert certificate.unlimited_exact_block_count == 7


def test_horizon_beyond_graph_depth_recovers_unlimited_quotient() -> None:
    certificate = certify_path_reachability(maximum_distance=4, spread_horizon=10)
    assert certificate.verify()
    assert certificate.initial_exact_block_count == 6
    assert certificate.unlimited_exact_block_count == 6


def test_unreachable_patches_form_one_future_silent_class() -> None:
    # 1 can reach focal 0.  Patches 2 and 3 form a disconnected directed component.
    certificate = certify_spatial_dispersal_reachability(
        node_count=4,
        focal_target=0,
        edges=((1, 0), (3, 2)),
        spread_horizon=4,
    )
    assert certificate.verify()
    assert certificate.node_distances_to_focal == (0, 1, None, None)
    assert certificate.maximum_finite_distance == 1
    assert certificate.initial_exact_block_count == 3
    assert certificate.unlimited_exact_block_count == 3

    unreachable_mask = (1 << 2) | (1 << 3)
    assert certificate.occupancy_distance_to_focal(unreachable_mask) is None
    assert certificate.occupancy_distance_to_focal(certificate.spread(unreachable_mask)) is None


def test_changing_graph_family_has_fixed_horizon_bound_but_growing_unlimited_memory() -> None:
    specs = tuple(path_to_focal_graph(distance) for distance in (1, 3, 5))
    family = certify_spatial_reachability_family(specs, spread_horizon=2)
    assert family.verify()
    assert family.uniform_initial_block_bound == 4
    assert family.initial_block_counts == (3, 4, 4)
    assert family.unlimited_block_counts == (3, 5, 7)


def test_grammar_adaptive_tail_moves_deterministically() -> None:
    certificate = certify_path_reachability(maximum_distance=5, spread_horizon=3)
    # Initial distance 5 is hidden in the >3-step tail: z=4.
    far_mask = 1 << 5
    assert certificate.capped_distance(far_mask, 0) == 4
    next_mask = certificate.spread(far_mask)
    assert certificate.capped_distance(next_mask, 1) == 3
    assert certificate.macro_successor(0, 4) == (1, 3)


def test_invalid_spatial_graph_is_rejected() -> None:
    with pytest.raises(ValueError):
        certify_spatial_dispersal_reachability(
            node_count=3,
            focal_target=0,
            edges=((1, 3),),
            spread_horizon=2,
        )
    with pytest.raises(ValueError):
        certify_spatial_dispersal_reachability(
            node_count=3,
            focal_target=0,
            edges=((1, 0), (1, 0)),
            spread_horizon=2,
        )
