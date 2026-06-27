from itertools import product

from causal_model.replaceability import (
    Observation,
    StructuralModel,
    admissible_configurations,
    forced_off,
    forced_on,
    forced_on_by_theorem,
    is_last_driver_standing,
    null_eliminated_mechanisms,
    observation_is_admissible,
    theorem_a_certificate,
)


def _all_observations(traits: tuple[str, ...]):
    # 0=unobserved, 1=required present, 2=required null.
    for statuses in product((0, 1, 2), repeat=len(traits)):
        present = tuple(trait for trait, status in zip(traits, statuses) if status == 1)
        null = tuple(trait for trait, status in zip(traits, statuses) if status == 2)
        yield Observation(present=present, null=null)


def test_theorem_a_and_null_only_elimination_exhaustively_match_enumeration() -> None:
    # Every model with one or two traits and up to three mechanisms, crossed with
    # every non-contradictory observation pattern. This is intentionally small but
    # checks overlapping driver sets rather than only canonical examples.
    for mechanism_count in range(1, 4):
        traits = ("trait_a", "trait_b")
        nonempty_driver_sets = tuple(
            frozenset(index for index, flag in enumerate(mask) if flag)
            for mask in product((0, 1), repeat=mechanism_count)
            if any(mask)
        )
        for chosen_driver_sets in product(nonempty_driver_sets, repeat=len(traits)):
            model = StructuralModel(
                mechanism_count=mechanism_count,
                driver_sets=dict(zip(traits, chosen_driver_sets)),
            )
            for observation in _all_observations(traits):
                configurations = admissible_configurations(model, observation)
                assert observation_is_admissible(model, observation) is bool(configurations)
                eliminated = null_eliminated_mechanisms(model, observation)
                for mechanism in range(mechanism_count):
                    if configurations:
                        assert forced_off(configurations, mechanism) is (mechanism in eliminated)
                    else:
                        assert not forced_off(configurations, mechanism)
                    assert forced_on_by_theorem(model, observation, mechanism) is forced_on(
                        configurations, mechanism
                    )
                    certificate = theorem_a_certificate(model, observation, mechanism)
                    if configurations:
                        assert certificate.holds
                        assert forced_on(configurations, mechanism) is bool(
                            is_last_driver_standing(model, observation, mechanism)
                        )
                    else:
                        assert not certificate.holds
