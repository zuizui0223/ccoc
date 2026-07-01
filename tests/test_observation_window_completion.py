import pytest

from causal_model.extension_compression import IDLE, OBSERVE
from causal_model.observation_window_completion import (
    PASSIVE_ACTIONS,
    certify_observation_window_completion,
    completion_counterexample_certificate,
    exhaustive_observation_window_summary,
    is_passive_window_partition_sound,
    passive_window_partition,
    passive_window_trace,
    passive_words_through,
    relay_completion_certificate,
)


def test_every_passive_word_leaves_hidden_completions_indistinguishable():
    module_count = 4
    for word in passive_words_through(5):
        for focal_bit in (0, 1):
            for port in range(module_count):
                certificate = completion_counterexample_certificate(module_count, word, port, focal_bit)
                assert certificate.verify()
                assert certificate.left_passive_trace == certificate.right_passive_trace
                assert certificate.left_counterfactual_trace != certificate.right_counterfactual_trace
                assert certificate.boundary_action == f"probe:{port}"


def test_passive_window_has_two_states_but_open_counterfactuals_restore_full_microstate():
    module_count = 5
    assert len(passive_window_partition(module_count)) == 2
    assert is_passive_window_partition_sound(module_count)

    certificate = certify_observation_window_completion(module_count, passive_horizon_checked=5)
    assert certificate.verify()
    assert certificate.passive_interface_bits == 1
    assert certificate.open_interface_bits == 6
    assert certificate.counterfactual_inflation_bits == 5
    assert certificate.hidden_completion_count_per_window_value == 32


def test_mixed_observe_idle_protocol_is_passive_and_never_changes_the_focal_trace():
    state = (1, 0, 1, 0)
    word = (OBSERVE, IDLE, IDLE, OBSERVE, IDLE)
    assert passive_window_trace(3, state, word) == (1, 1, 1, 1, 1, 1)
    assert all(action in PASSIVE_ACTIONS for action in word)


def test_degree_three_relay_tree_realizes_the_same_hidden_completion_counterexample():
    certificate = relay_completion_certificate(module_count=6, passive_microticks=11, port=4)
    assert certificate.verify()
    assert certificate.left_passive_trace == certificate.right_passive_trace
    assert certificate.left_counterfactual_output == 0
    assert certificate.right_counterfactual_output == 1


def test_exhaustive_finite_family_has_exact_linear_counterfactual_inflation():
    certificates = exhaustive_observation_window_summary(max_module_count=6, passive_horizon_checked=4)
    assert [certificate.module_count for certificate in certificates] == [1, 2, 3, 4, 5, 6]
    assert [certificate.passive_interface_bits for certificate in certificates] == [1, 1, 1, 1, 1, 1]
    assert [certificate.open_interface_bits for certificate in certificates] == [2, 3, 4, 5, 6, 7]
    assert [certificate.counterfactual_inflation_bits for certificate in certificates] == [1, 2, 3, 4, 5, 6]


@pytest.mark.parametrize("bad_horizon", [-1, True, 1.5, "5"])
def test_invalid_passive_horizons_fail_closed(bad_horizon):
    with pytest.raises(ValueError, match="non-negative integer"):
        passive_words_through(bad_horizon)


@pytest.mark.parametrize("bad_word", [("probe:0",), ("unknown",), 3])
def test_nonpassive_protocols_fail_closed(bad_word):
    with pytest.raises(ValueError, match="passive"):
        completion_counterexample_certificate(2, bad_word, 0)
