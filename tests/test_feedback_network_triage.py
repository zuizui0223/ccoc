from experiments.feedback_network_nonreducibility import (
    ACTIONS,
    DISTINGUISHING_WORD,
    STATE_INDEX,
    WITNESS_LEFT,
    WITNESS_RIGHT,
    baseline_label,
    build_system,
    certify_feedback_network_triage,
    feedback_label,
)


def test_feedback_network_triage_certificate() -> None:
    certificate = certify_feedback_network_triage()
    assert certificate.verify()
    assert certificate.canonical_block_count == 5
    assert certificate.stabilization_horizon == 3
    assert certificate.baseline_block_count == 4
    assert certificate.feedback_block_count == 5
    assert not certificate.baseline_dynamic
    assert certificate.feedback_dynamic
    assert certificate.feedback_matches_canonical


def test_witness_is_latent_until_alternating_feedback_word() -> None:
    system = build_system()
    left = STATE_INDEX[WITNESS_LEFT]
    right = STATE_INDEX[WITNESS_RIGHT]

    assert baseline_label(WITNESS_LEFT) == baseline_label(WITNESS_RIGHT)
    assert feedback_label(WITNESS_LEFT) != feedback_label(WITNESS_RIGHT)

    # Every response word through length two is identical; neither one-step
    # movement nor one-step turnover exposes the latent interaction mode.
    for first in ((),) + tuple((a,) for a in ACTIONS):
        assert system.output_trace(left, first) == system.output_trace(right, first)
    for first in ACTIONS:
        for second in ACTIONS:
            word = (first, second)
            assert system.output_trace(left, word) == system.output_trace(right, word)

    assert system.output_trace(left, DISTINGUISHING_WORD) != system.output_trace(
        right, DISTINGUISHING_WORD
    )
