import pytest

from causal_model.delayed_joint_nonidentifiability import DelayedJointAction, DelayedJointFamily
from causal_model.delayed_joint_reset_panels import (
    ResettableTrialPanel,
    canonical_reset_panel,
    certify_delayed_joint_reset_panel_complexity,
    certify_reset_panel_exactness,
    exhaustive_reset_panel_complexity_summary,
    find_missing_terminal_probe,
    required_terminal_words,
    terminal_probe_necessity_certificates,
)


def test_canonical_reset_panel_has_one_required_trial_per_exterior_coordinate_plus_response_type():
    family = DelayedJointFamily(exterior_port_count=3, delay=2)
    panel = canonical_reset_panel(family)
    assert panel.verify()
    assert panel.trial_words == required_terminal_words(family)
    assert panel.trial_count == 4
    assert panel.maximum_trial_horizon == 3
    assert panel.total_action_count == 12
    assert panel.is_exact


def test_panel_signature_is_injective_across_every_joint_state_under_reset_semantics():
    family = DelayedJointFamily(exterior_port_count=2, delay=1)
    panel = canonical_reset_panel(family)
    certificate = certify_reset_panel_exactness(family, panel.trial_words)
    assert certificate.verify()
    assert certificate.signature_count == family.state_count == 16
    assert panel.signature((0, 0, 0, 0)) != panel.signature((0, 1, 0, 0))
    assert panel.signature((0, 0, 0, 0)) != panel.signature((0, 0, 0, 1))
    assert panel.signature((0, 0, 0, 0)) != panel.signature((1, 0, 0, 0))


def test_required_terminal_probe_certificates_are_unique_for_each_coordinate():
    family = DelayedJointFamily(exterior_port_count=3, delay=2)
    certificates = terminal_probe_necessity_certificates(family)
    assert len(certificates) == 4
    assert all(certificate.verify() for certificate in certificates)
    assert [certificate.coordinate_kind for certificate in certificates] == [
        "exterior",
        "exterior",
        "exterior",
        "response",
    ]
    for certificate in certificates:
        legal_words = family.grammar.legal_words_through(family.first_revealing_horizon)
        separating = [
            word
            for word in legal_words
            if family.trace(certificate.left, word) != family.trace(certificate.right, word)
        ]
        assert separating == [certificate.required_word]


def test_every_missing_required_probe_has_an_explicit_nonexactness_obstruction():
    family = DelayedJointFamily(exterior_port_count=2, delay=3)
    complete = required_terminal_words(family)
    for missing_index in range(len(complete)):
        incomplete = complete[:missing_index] + complete[missing_index + 1 :]
        obstruction = find_missing_terminal_probe(family, incomplete)
        assert obstruction is not None
        assert obstruction.verify()
        assert obstruction.necessity.required_word == complete[missing_index]
        assert not obstruction.panel.is_exact
        with pytest.raises(ValueError, match="not exact"):
            certify_reset_panel_exactness(family, incomplete)


def test_duplicate_trial_does_not_replace_a_missing_distinct_terminal_probe():
    family = DelayedJointFamily(exterior_port_count=2, delay=1)
    read_zero, read_one, intervene = required_terminal_words(family)
    duplicate_panel = ResettableTrialPanel(
        family=family,
        trial_words=(read_zero, read_zero, intervene),
    )
    assert duplicate_panel.verify()
    assert duplicate_panel.trial_count == 3
    assert not duplicate_panel.is_exact
    obstruction = find_missing_terminal_probe(family, duplicate_panel.trial_words)
    assert obstruction is not None
    assert obstruction.necessity.required_word == read_one


@pytest.mark.parametrize(
    "exterior_port_count,delay",
    [(1, 0), (1, 4), (2, 3), (4, 1)],
)
def test_exact_resource_vector_matches_the_sharp_formula(exterior_port_count, delay):
    certificate = certify_delayed_joint_reset_panel_complexity(exterior_port_count, delay)
    assert certificate.verify()
    assert certificate.minimum_trial_count == exterior_port_count + 1
    assert certificate.minimum_maximum_trial_horizon == delay + 1
    assert certificate.minimum_total_action_count == (exterior_port_count + 1) * (delay + 1)
    assert certificate.parallel_wall_clock_lower_bound == delay + 1


def test_reset_assumption_is_explicit_terminal_events_cannot_be_concatenated_in_one_trial():
    family = DelayedJointFamily(exterior_port_count=1, delay=2)
    read_word, intervene_word = required_terminal_words(family)
    with pytest.raises(ValueError, match="illegal"):
        family.grammar.normalize_legal_word(read_word + intervene_word)
    with pytest.raises(ValueError, match="illegal"):
        ResettableTrialPanel(family=family, trial_words=(read_word + intervene_word,))


def test_empty_or_early_only_panel_is_not_exact():
    family = DelayedJointFamily(exterior_port_count=2, delay=2)
    empty = ResettableTrialPanel(family=family, trial_words=())
    early = ResettableTrialPanel(
        family=family,
        trial_words=((DelayedJointAction.wait(),), (DelayedJointAction.wait(), DelayedJointAction.wait())),
    )
    assert empty.verify() and early.verify()
    assert not empty.is_exact
    assert not early.is_exact
    assert find_missing_terminal_probe(family, empty.trial_words) is not None
    assert find_missing_terminal_probe(family, early.trial_words) is not None


def test_exhaustive_small_reset_panel_certificate_replay():
    certificates = exhaustive_reset_panel_complexity_summary(max_exterior_port_count=3, max_delay=3)
    assert len(certificates) == 12
    assert all(certificate.verify() for certificate in certificates)


@pytest.mark.parametrize(
    "bad_words",
    [
        ((DelayedJointAction.read(3),),),
        ((DelayedJointAction.wait(), DelayedJointAction.wait()),),
        (("not-an-action",),),
    ],
)
def test_illegal_trial_words_fail_closed(bad_words):
    family = DelayedJointFamily(exterior_port_count=1, delay=1)
    with pytest.raises((TypeError, ValueError)):
        ResettableTrialPanel(family=family, trial_words=bad_words)
