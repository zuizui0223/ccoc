"""Tests for one newly legal primitive action causing linear innovation."""

import pytest

import causal_model.portability_core as portability
from causal_model.constant_alphabet_relay import FIRE, GLOBAL_ACTION_ALPHABET
from causal_model.single_action_innovation import (
    CLOSED_PRIMITIVE_ACTIONS,
    NEWLY_LEGAL_PRIMITIVE_ACTIONS,
    closed_fire_free_words,
    certify_single_action_innovation,
)


def test_closed_grammar_has_real_routing_and_ticks_but_no_fire():
    certificate = certify_single_action_innovation(4)

    assert certificate.verify()
    assert FIRE not in CLOSED_PRIMITIVE_ACTIONS
    assert set(CLOSED_PRIMITIVE_ACTIONS) == {"0", "1", "tick"}
    assert NEWLY_LEGAL_PRIMITIVE_ACTIONS == (FIRE,)
    assert set(certificate.open_primitive_actions) == set(GLOBAL_ACTION_ALPHABET)
    assert all(FIRE not in word for word in certificate.closed_words)
    assert any("0" in word for word in certificate.closed_words)
    assert any("1" in word for word in certificate.closed_words)
    assert any("tick" in word for word in certificate.closed_words)


def test_one_new_action_accounts_for_all_linear_open_only_innovation():
    for module_count in (2, 4, 8):
        certificate = certify_single_action_innovation(module_count)

        assert certificate.closed_block_count == 2
        assert certificate.open_block_count == 2 ** (module_count + 1)
        assert certificate.decomposition.fibered_capacity_state_count == 2
        assert certificate.join_realizability_defect_bits == pytest.approx(0.0)
        assert certificate.open_only_innovation_bits == pytest.approx(module_count)
        assert certificate.total_gap_bits == pytest.approx(module_count)
        assert certificate.maximum_degree <= 3
        assert len(certificate.newly_legal_primitive_actions) == 1


def test_every_closed_trace_is_independent_of_all_dormant_memory_bits():
    certificate = certify_single_action_innovation(4)
    words = closed_fire_free_words(4)

    by_focal = {0: set(), 1: set()}
    for state, signature in zip(certificate.states, certificate.closed_labels):
        by_focal[state[0]].add(signature)
        for trace in signature:
            assert set(trace) == {state[0]}

    assert len(by_focal[0]) == 1
    assert len(by_focal[1]) == 1
    assert by_focal[0] != by_focal[1]
    assert words == certificate.closed_words


def test_each_open_addressed_word_reads_exactly_its_dormant_bit():
    certificate = certify_single_action_innovation(4)

    for state in certificate.states:
        for port, word in enumerate(certificate.open_probe_words):
            # The certificate's own exhaustive verification checks the full
            # trajectory. Here the final response is the exposed coordinate.
            from causal_model.single_action_innovation import _trace

            assert _trace(certificate.topology, state, word)[-1] == state[port + 1]


def test_positive_innovation_returns_a_core5_style_local_split_witness():
    certificate = certify_single_action_innovation(4)
    witness = certificate.first_split_witness

    assert witness is not None
    assert witness.verify(certificate.topology, certificate.closed_words)
    assert FIRE in witness.separating_word
    assert witness.left_state[0] == witness.right_state[0]
    assert witness.left_trace != witness.right_trace


def test_probe_word_length_is_logarithmic_and_global_alphabet_stays_constant():
    for module_count in (2, 4, 8):
        certificate = certify_single_action_innovation(module_count)
        depth = module_count.bit_length() - 1

        assert all(len(word) == 2 * depth + 2 for word in certificate.open_probe_words)
        assert certificate.open_primitive_actions == GLOBAL_ACTION_ALPHABET
        assert len(certificate.open_primitive_actions) == 4


@pytest.mark.parametrize("bad_count", [0, 1, 3, 6, -2, True, 4.0, "4"])
def test_invalid_family_sizes_fail_closed(bad_count):
    with pytest.raises(ValueError, match="power of two"):
        certify_single_action_innovation(bad_count)


def test_single_action_certificate_is_public_portability_surface():
    assert portability.certify_single_action_innovation is certify_single_action_innovation
    assert "SingleActionInnovationCertificate" in portability.__all__
    assert "RelayInnovationSplitWitness" in portability.__all__
