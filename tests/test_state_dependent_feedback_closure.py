from __future__ import annotations

import pytest

from causal_model.state_dependent_feedback_closure import (
    ModeDependentContextFeedbackSystem,
    build_mode_routed_context_family,
    certify_continuation_closure,
    certify_mode_routed_context_rank,
    continuation_rank,
    continuation_refinement_step,
    current_type_interface_is_exact,
    find_current_type_obstruction,
)


def _build_current_type_closed_example() -> ModeDependentContextFeedbackSystem:
    # Modes 0/2 share type 0 and modes 1/3 share type 1 in every context.
    # The type itself therefore evolves deterministically even though different
    # types may route to different contexts.
    actions = ("route", "advance")
    outputs = ((0,), (1,))
    feedback_types = (
        (0, 1, 0, 1),
        (0, 1, 0, 1),
    )
    context_transitions = (
        (
            (
                (0, 0),  # mode 0, type 0
                (1, 0),  # mode 1, type 1
                (0, 0),  # mode 2, type 0
                (1, 0),  # mode 3, type 1
            ),
        ),
        (
            (
                (1, 1),
                (1, 1),
                (1, 1),
                (1, 1),
            ),
        ),
    )
    macro_transitions = (
        (((0, 0), (0, 0), (0, 0), (0, 0)),),
        (((0, 0), (0, 0), (0, 0), (0, 0)),),
    )
    return ModeDependentContextFeedbackSystem(
        actions=actions,
        outputs=outputs,
        feedback_types=feedback_types,
        context_transitions=context_transitions,
        macro_transitions=macro_transitions,
    )


def test_current_feedback_type_exactness_has_a_one_step_iff_contract() -> None:
    system = _build_current_type_closed_example()
    assert current_type_interface_is_exact(system)
    assert find_current_type_obstruction(system) is None

    closure = certify_continuation_closure(system)
    assert closure.verify(system)
    assert closure.current_type_exact
    # Current type is exact but not necessarily minimal in contexts where its
    # distinction has no remaining effect; continuation closure may merge it.
    assert continuation_rank(closure.labels, 0, 0) == 2
    assert continuation_rank(closure.labels, 1, 0) == 1


def test_mode_routed_family_exposes_failure_of_current_type_closure() -> None:
    system = build_mode_routed_context_family(2)
    assert not current_type_interface_is_exact(system)
    obstruction = find_current_type_obstruction(system)
    assert obstruction is not None
    assert obstruction.left_mode != obstruction.right_mode
    assert obstruction.current_type == system.feedback_type(obstruction.context, obstruction.left_mode)

    closure = certify_continuation_closure(system)
    assert closure.verify(system)
    assert continuation_rank(closure.labels, 0, 0) == 4


def test_mode_routed_rank_family_is_sharp_for_small_ranks() -> None:
    for rank in range(1, 5):
        certificate = certify_mode_routed_context_rank(rank)
        assert certificate.verify()
        assert certificate.initial_continuation_rank == 2**rank
        assert certificate.initial_hidden_memory_bits == float(rank)
        assert certificate.stabilization_round == 2 * rank - 1
        assert certificate.last_bit_first_separating_horizon == 2 * rank - 1
        assert certificate.maximum_instantaneous_type_count == 2
        assert certificate.current_type_exact is (rank == 1)


def test_last_bit_pair_really_needs_the_full_routed_horizon() -> None:
    rank = 4
    system = build_mode_routed_context_family(rank)
    left = 0
    right = 1 << (rank - 1)
    route_to_last = (
        "route",
        "advance",
        "route",
        "advance",
        "route",
        "advance",
        "route",
    )
    assert len(route_to_last) == 2 * rank - 1
    assert system.output_trace(0, 0, left, route_to_last[:-1]) == system.output_trace(
        0, 0, right, route_to_last[:-1]
    )
    assert system.output_trace(0, 0, left, route_to_last) != system.output_trace(
        0, 0, right, route_to_last
    )


def test_continuation_refinement_rejects_wrong_shape() -> None:
    system = build_mode_routed_context_family(2)
    with pytest.raises(ValueError):
        continuation_refinement_step(system, ())


def test_invalid_rank_fails_closed() -> None:
    with pytest.raises(ValueError):
        build_mode_routed_context_family(0)
