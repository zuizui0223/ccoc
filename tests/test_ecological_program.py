from causal_model.admissibility import CoverageMode, MotifStatus
from causal_model.ecological_program import (
    AllOf,
    AnyOf,
    HardObservationCandidate,
    HardTraitObservation,
    Mechanism,
    NoisyObservationPanel,
    NoisyRobustnessCell,
    Not,
    QualitativeProgram,
    QualitativeProgramCandidate,
    TraitDetection,
    admissible_states,
    evaluate_candidate_universe,
    fit_program,
    mechanism_forced_on,
    minimum_boolean_panel,
)


def test_boolean_program_handles_conjunction_alternatives_and_inhibition() -> None:
    program = QualitativeProgram(
        3,
        {
            "signal": AllOf(
                (
                    AnyOf((Mechanism(0), Mechanism(1))),
                    Not(Mechanism(2)),
                )
            )
        },
    )
    assert program.trait_is_present("signal", (1, 0, 0))
    assert program.trait_is_present("signal", (0, 1, 0))
    assert not program.trait_is_present("signal", (0, 0, 0))
    assert not program.trait_is_present("signal", (1, 0, 1))


def test_noisy_null_is_probabilistic_not_hard_elimination() -> None:
    program = QualitativeProgram(1, {"trait": Mechanism(0)})
    panel = NoisyObservationPanel(
        (
            TraitDetection(
                "trait",
                detections=0,
                trials=3,
                sensitivity=0.9,
                false_positive=0.05,
            ),
        )
    )
    fit = fit_program(program, panel)
    assert fit.state_log_likelihoods[(0,)] > fit.state_log_likelihoods[(1,)]
    assert fit.state_log_likelihoods[(1,)] > float("-inf")


def test_candidate_universe_integrates_noisy_cells_with_robust_classification() -> None:
    selection = QualitativeProgramCandidate(
        "selection_program",
        frozenset({"selection"}),
        QualitativeProgram(2, {"color": Mechanism(0), "neutral": Mechanism(1)}),
    )
    drift = QualitativeProgramCandidate(
        "drift_program",
        frozenset({"drift"}),
        QualitativeProgram(2, {"color": Mechanism(1), "neutral": Mechanism(1)}),
    )
    observations = NoisyObservationPanel(
        (
            TraitDetection("color", 3, 3, sensitivity=0.9, false_positive=0.05),
            TraitDetection("neutral", 0, 3, sensitivity=0.9, false_positive=0.05),
        )
    )
    cell = NoisyRobustnessCell(
        "field",
        "high-power field cell",
        observations,
        acceptance_log_likelihood=-2.5,
        coverage_mode=CoverageMode.EXHAUSTIVE,
    )
    report = evaluate_candidate_universe((selection, drift), (cell,)).classify(
        ("selection", "drift")
    )
    assert report.classifications["selection"].status is MotifStatus.INVARIANT
    assert report.classifications["drift"].status is MotifStatus.EXCLUDED


def test_minimum_boolean_panel_finds_joint_witnesses_not_singletons() -> None:
    program = QualitativeProgram(
        3,
        {
            "shared": AnyOf((Mechanism(0), Mechanism(1), Mechanism(2))),
            "w1": Mechanism(1),
            "w2": Mechanism(2),
        },
    )
    base = HardTraitObservation(present=("shared",))
    assert not mechanism_forced_on(admissible_states(program, base), 0)

    panel = minimum_boolean_panel(
        program,
        focal_mechanism=0,
        base_observation=base,
        candidates=(
            HardObservationCandidate("w1", reported_present=False, cost=2.0),
            HardObservationCandidate("w2", reported_present=False, cost=3.0),
        ),
    )

    assert panel is not None
    assert panel.selected_traits == ("w1", "w2")
    assert panel.total_cost == 5.0
