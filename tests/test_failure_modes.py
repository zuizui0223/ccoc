import pytest

from causal_model.failure_modes import (
    BinaryObservationChannel,
    TheoremAuditStatus,
    TruthTableModel,
    audit_declared_theorem,
    compatibility_missed_necessity_counterexample,
    conjunction_contradiction_counterexample,
    inhibitory_null_counterexample,
    latent_competitor_counterexample,
    noisy_observation_audit,
    true_admissible_configurations,
)
from causal_model.replaceability import Observation, StructuralModel


def test_omitted_latent_competitor_produces_false_necessity() -> None:
    declared, truth, observation = latent_competitor_counterexample()
    audit = audit_declared_theorem(declared, truth, observation, focal_mechanism=0)
    assert audit.status is TheoremAuditStatus.FALSE_NECESSITY
    assert audit.declared_forced_on
    assert not audit.true_forced_on
    assert (0, 0, 1) in audit.true_admissible_states


def test_inhibitory_effect_makes_null_only_elimination_invalid() -> None:
    declared, truth, observation = inhibitory_null_counterexample()
    audit = audit_declared_theorem(declared, truth, observation, focal_mechanism=0)
    assert audit.status is TheoremAuditStatus.FALSE_NECESSITY
    assert audit.declared_forced_on
    assert (0, 1, 1) in audit.true_admissible_states


def test_conjunction_is_detected_as_true_model_contradiction() -> None:
    declared, truth, observation = conjunction_contradiction_counterexample()
    audit = audit_declared_theorem(declared, truth, observation, focal_mechanism=0)
    assert audit.status is TheoremAuditStatus.TRUE_MODEL_CONTRADICTION
    assert audit.declared_observation_admissible
    assert audit.declared_forced_on
    assert audit.true_admissible_states == ()


def test_hidden_compatibility_can_hide_true_necessity_from_last_driver_rule() -> None:
    declared, truth, observation = compatibility_missed_necessity_counterexample()
    audit = audit_declared_theorem(declared, truth, observation, focal_mechanism=0)
    assert audit.status is TheoremAuditStatus.MISSED_NECESSITY
    assert not audit.declared_forced_on
    assert audit.true_forced_on
    assert audit.true_admissible_states == ((1, 0), (1, 1))


def test_noisy_null_has_exact_false_necessity_risk_under_uniform_prior() -> None:
    model = StructuralModel(
        mechanism_count=2,
        driver_sets={
            "shared": frozenset({0, 1}),
            "witness_1": frozenset({1}),
        },
    )
    states = ((0, 0), (0, 1), (1, 0), (1, 1))
    truth = TruthTableModel(
        mechanism_count=2,
        trait_true_states={
            "shared": frozenset(state for state in states if state[0] or state[1]),
            "witness_1": frozenset(state for state in states if state[1]),
        },
    )
    observation = Observation(present=("shared",), null=("witness_1",))
    audit = noisy_observation_audit(
        model,
        truth,
        observation,
        focal_mechanism=0,
        channels={
            "witness_1": BinaryObservationChannel(
                present_if_true_present=0.9,
                present_if_true_null=0.0,
            )
        },
    )
    assert audit.declared_forced_on
    assert audit.report_probability == pytest.approx(0.3)
    assert audit.posterior_focal_off_probability == pytest.approx(1.0 / 12.0)
    assert audit.false_necessity_risk == pytest.approx(1.0 / 12.0)


def test_perfect_null_measurement_eliminates_noise_induced_false_necessity_risk() -> None:
    model = StructuralModel(
        mechanism_count=2,
        driver_sets={
            "shared": frozenset({0, 1}),
            "witness_1": frozenset({1}),
        },
    )
    states = ((0, 0), (0, 1), (1, 0), (1, 1))
    truth = TruthTableModel(
        mechanism_count=2,
        trait_true_states={
            "shared": frozenset(state for state in states if state[0] or state[1]),
            "witness_1": frozenset(state for state in states if state[1]),
        },
    )
    audit = noisy_observation_audit(
        model,
        truth,
        Observation(present=("shared",), null=("witness_1",)),
        focal_mechanism=0,
    )
    assert audit.false_necessity_risk == 0.0


def test_truth_table_validates_unknown_observations_and_invalid_states() -> None:
    model = TruthTableModel(
        mechanism_count=1,
        trait_true_states={"x": frozenset({(1,)})},
    )
    with pytest.raises(ValueError, match="unknown truth-table traits"):
        true_admissible_configurations(model, Observation(present=("unknown",)))
    with pytest.raises(ValueError, match="invalid Boolean state"):
        TruthTableModel(
            mechanism_count=1,
            trait_true_states={"x": frozenset({(2,)})},
        )


def test_noise_channels_and_priors_are_validated() -> None:
    with pytest.raises(ValueError, match="between zero and one"):
        BinaryObservationChannel(present_if_true_present=1.1)

    model = StructuralModel(mechanism_count=1, driver_sets={"x": frozenset({0})})
    truth = TruthTableModel(
        mechanism_count=1,
        trait_true_states={"x": frozenset({(1,)})},
    )
    with pytest.raises(ValueError, match="prior_weights"):
        noisy_observation_audit(
            model,
            truth,
            Observation(present=("x",)),
            focal_mechanism=0,
            prior_weights={(0,): 1.0},
        )
