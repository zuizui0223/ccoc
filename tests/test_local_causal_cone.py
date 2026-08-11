"""Tests for bounded-degree causal-cone response-capacity bounds."""

import math

import pytest

import causal_model.portability_core as portability
from causal_model.local_causal_cone import (
    certify_degree_bounded_causal_cone,
    certify_local_causal_cone_capacity,
    maximum_degree_ball_size,
    minimum_degree_bounded_horizon,
    radius_ball,
)


def test_radius_ball_and_heterogeneous_state_capacity_on_a_path():
    adjacency = (
        (1,),
        (0, 2),
        (1, 3),
        (2,),
    )
    cardinalities = (2, 3, 5, 7)

    assert radius_ball(adjacency, focal_node=0, radius=0) == (0,)
    assert radius_ball(adjacency, focal_node=0, radius=2) == (0, 1, 2)

    certificate = certify_local_causal_cone_capacity(
        adjacency=adjacency,
        state_cardinalities=cardinalities,
        focal_node=0,
        horizon=2,
        required_response_classes=30,
    )

    assert certificate.verify()
    assert certificate.ball_nodes == (0, 1, 2)
    assert certificate.ball_configuration_capacity == 2 * 3 * 5
    assert certificate.ball_information_capacity_bits == pytest.approx(math.log2(30))
    assert certificate.has_sufficient_local_capacity


def test_declared_horizon_can_be_certified_as_information_insufficient():
    adjacency = (
        (1,),
        (0, 2),
        (1,),
    )
    certificate = certify_local_causal_cone_capacity(
        adjacency=adjacency,
        state_cardinalities=(2, 2, 2),
        focal_node=0,
        horizon=1,
        required_response_classes=8,
    )

    assert certificate.verify()
    assert certificate.ball_nodes == (0, 1)
    assert certificate.ball_configuration_capacity == 4
    assert not certificate.has_sufficient_local_capacity
    assert certificate.required_interface_bits == 3.0
    assert certificate.ball_information_capacity_bits == 2.0


def test_universal_degree_ball_bounds_cover_path_and_branching_cases():
    assert [maximum_degree_ball_size(0, radius) for radius in range(4)] == [1, 1, 1, 1]
    assert [maximum_degree_ball_size(1, radius) for radius in range(4)] == [1, 2, 2, 2]
    assert [maximum_degree_ball_size(2, radius) for radius in range(4)] == [1, 3, 5, 7]
    assert [maximum_degree_ball_size(3, radius) for radius in range(4)] == [1, 4, 10, 22]
    assert [maximum_degree_ball_size(4, radius) for radius in range(4)] == [1, 5, 17, 53]


def test_minimum_horizon_matches_first_degree_state_capacity_that_can_hold_classes():
    required = 2**65
    horizon = minimum_degree_bounded_horizon(
        response_class_count=required,
        maximum_degree=3,
        local_state_bound=12,
    )

    assert horizon == 3
    previous = certify_degree_bounded_causal_cone(3, 12, horizon - 1, required)
    sufficient = certify_degree_bounded_causal_cone(3, 12, horizon, required)

    assert previous.verify()
    assert not previous.horizon_is_large_enough
    assert sufficient.verify()
    assert sufficient.horizon_is_large_enough
    assert sufficient.minimum_required_horizon == horizon


def test_constant_degree_and_local_state_force_logarithmic_horizon_for_exponential_classes():
    # If the exact response quotient contains 2^(m+1) classes, the local causal
    # cone must contain Omega(m) bits. A degree-three ball grows exponentially in
    # the horizon, so the inverse horizon is logarithmic in m.
    samples = []
    for exponent in range(4, 13):
        module_count = 2**exponent
        required = 2 ** (module_count + 1)
        horizon = minimum_degree_bounded_horizon(required, maximum_degree=3, local_state_bound=12)
        samples.append((module_count, horizon))

    # Doubling m eventually increases the minimum radius by at most a constant,
    # and over this exact power-of-two sequence the lower bound tracks log2(m).
    for module_count, horizon in samples:
        assert horizon >= math.log2(module_count) - 4
        assert horizon <= math.log2(module_count)


def test_existing_relay_query_length_is_order_optimal_under_general_causal_cone_bound():
    for module_count in (16, 32, 64, 128, 256, 512):
        required = 2 ** (module_count + 1)
        lower = minimum_degree_bounded_horizon(required, maximum_degree=3, local_state_bound=12)
        actual = 2 * int(math.log2(module_count)) + 2

        assert lower <= actual
        assert actual <= 3 * lower + 8


def test_graph_contract_rejects_asymmetric_edges_bad_cardinalities_and_bad_focal_node():
    with pytest.raises(ValueError, match="undirected"):
        certify_local_causal_cone_capacity(
            adjacency=((1,), ()),
            state_cardinalities=(2, 2),
            focal_node=0,
            horizon=1,
            required_response_classes=2,
        )

    with pytest.raises(ValueError, match="positive integer"):
        certify_local_causal_cone_capacity(
            adjacency=((1,), (0,)),
            state_cardinalities=(2, 0),
            focal_node=0,
            horizon=1,
            required_response_classes=2,
        )

    with pytest.raises(ValueError, match="focal_node"):
        certify_local_causal_cone_capacity(
            adjacency=((1,), (0,)),
            state_cardinalities=(2, 2),
            focal_node=3,
            horizon=1,
            required_response_classes=2,
        )


def test_causal_cone_certificates_are_public_portability_exports():
    assert portability.certify_local_causal_cone_capacity is certify_local_causal_cone_capacity
    assert portability.certify_degree_bounded_causal_cone is certify_degree_bounded_causal_cone
    assert portability.minimum_degree_bounded_horizon is minimum_degree_bounded_horizon
    assert "LocalCausalConeCapacityCertificate" in portability.__all__
    assert "DegreeBoundedCausalConeCertificate" in portability.__all__
