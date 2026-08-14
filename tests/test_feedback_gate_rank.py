from itertools import product

import pytest

from causal_model.feedback_gate_rank import (
    ACTIONS,
    SPREAD,
    TURNOVER,
    address_for,
    all_mode_profiles,
    certify_feedback_gate_rank,
    decode_mode_from_query,
    feedback_memory_bits,
    feedback_query_word,
    feedback_trace,
    first_feedback_separating_horizon,
    selector_depth,
    visible_initial_summary,
)


def _words_through(max_length: int):
    for length in range(max_length + 1):
        yield from product(ACTIONS, repeat=length)


def test_addresses_are_fixed_length_and_unique():
    for rank in range(1, 9):
        addresses = tuple(address_for(rank, i) for i in range(rank))
        assert len(set(addresses)) == rank
        assert {len(address) for address in addresses} == {selector_depth(rank)}


def test_feedback_queries_decode_every_mode_profile():
    for rank in range(1, 6):
        for profile in all_mode_profiles(rank):
            decoded = tuple(
                decode_mode_from_query(feedback_trace(profile, feedback_query_word(rank, i)))
                for i in range(rank)
            )
            assert decoded == profile


def test_visible_current_summary_is_constant_across_mode_profiles():
    for rank in range(1, 7):
        summaries = {visible_initial_summary(profile) for profile in all_mode_profiles(rank)}
        assert len(summaries) == 1


def test_mode_profiles_are_invisible_before_the_exact_feedback_horizon():
    # Exhaustive falsification on small ranks.  Analytic all-rank proof is in the docs.
    for rank in range(1, 5):
        horizon = first_feedback_separating_horizon(rank)
        baseline = (0,) * rank
        for i in range(rank):
            unit = tuple(1 if j == i else 0 for j in range(rank))
            for word in _words_through(horizon - 1):
                assert feedback_trace(baseline, word) == feedback_trace(unit, word)
            query = feedback_query_word(rank, i)
            assert len(query) == horizon
            assert feedback_trace(baseline, query) != feedback_trace(unit, query)


def test_breaking_either_feedback_arrow_erases_mode_information():
    # Finite replay through a horizon longer than the first full-feedback split.
    for rank in range(1, 4):
        profiles = all_mode_profiles(rank)
        horizon = first_feedback_separating_horizon(rank) + 1
        for word in _words_through(horizon):
            mode_blind = {
                feedback_trace(profile, word, mode_dependent_turnover=False)
                for profile in profiles
            }
            accessibility_blind = {
                feedback_trace(profile, word, accessibility_dependent_spread=False)
                for profile in profiles
            }
            assert len(mode_blind) == 1
            assert len(accessibility_blind) == 1
        assert feedback_memory_bits(rank, mode_dependent_turnover=False) == 0
        assert feedback_memory_bits(rank, accessibility_dependent_spread=False) == 0
        assert feedback_memory_bits(rank) == rank


def test_feedback_cycle_requires_alternation_not_one_step_hazard_readout():
    profile0 = (0,)
    profile1 = (1,)
    assert feedback_trace(profile0, (SPREAD,)) == feedback_trace(profile1, (SPREAD,))
    assert feedback_trace(profile0, (SPREAD, TURNOVER)) == feedback_trace(
        profile1, (SPREAD, TURNOVER)
    )
    assert feedback_trace(profile0, (SPREAD, TURNOVER, SPREAD)) != feedback_trace(
        profile1, (SPREAD, TURNOVER, SPREAD)
    )


def test_certificate_replays_scalable_formula():
    for rank in (1, 2, 3, 5, 8, 17):
        certificate = certify_feedback_gate_rank(rank)
        assert certificate.verify()
        assert certificate.full_feedback_memory_bits == rank
        assert certificate.mode_blind_memory_bits == 0
        assert certificate.accessibility_blind_memory_bits == 0
        assert certificate.query_length == selector_depth(rank) + 3


def test_invalid_rank_and_index_fail_closed():
    for invalid in (0, -1, True, 1.5):
        with pytest.raises(ValueError):
            selector_depth(invalid)
    with pytest.raises(ValueError):
        address_for(2, 2)
    with pytest.raises(ValueError):
        feedback_trace((0, 2), ())
