from math import isclose

from experiments.run_observation_envelope_grid import rows


def test_generic_observation_envelope_grid_has_expected_exact_anchor() -> None:
    table = rows()

    assert len(table) == 72
    anchor = next(
        row
        for row in table
        if row["required_cell_count"] == 2
        and row["sensitivity"] == 0.9
        and row["false_positive"] == 0.2
        and row["acceptance_log_likelihood"] == -0.5
    )
    assert anchor["outcome_count"] == 4
    assert isclose(float(anchor["false_invariant_probability"]), 0.04)
    assert isclose(float(anchor["correct_excluded_probability"]), 0.64)
    assert isclose(float(anchor["unresolved_probability"]), 0.32)
