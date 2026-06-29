from fractions import Fraction

import pytest

from causal_model import (
    CoverageMode,
    FarkasInfeasibilityCertificate,
    FeasibilityStatus,
    LinearFeasibilityProof,
    LinearFeasibilityQuery,
    LinearInequality,
    LinearMotifQueryBundle,
    RationalLinearSystem,
    RationalWitness,
    SymbolicCandidateSpace,
    classify_symbolic_candidate_sets,
    linear_bundles_to_symbolic_cell,
    verify_linear_query,
)


def inequality(coefficients, bound, label="") -> LinearInequality:
    return LinearInequality(tuple(coefficients), bound, label)


def system(*inequalities: LinearInequality) -> RationalLinearSystem:
    return RationalLinearSystem(("x",), tuple(inequalities), "one-dimensional rational polytope")


def sat_query(query_id: str, linear_system: RationalLinearSystem, point) -> LinearFeasibilityQuery:
    return LinearFeasibilityQuery(
        query_id=query_id,
        system=linear_system,
        proof=LinearFeasibilityProof(
            status=FeasibilityStatus.SAT,
            witness=RationalWitness(tuple(point)),
            evidence_reference=f"witness://{query_id}",
        ),
    )


def unsat_query(query_id: str, linear_system: RationalLinearSystem, multipliers) -> LinearFeasibilityQuery:
    return LinearFeasibilityQuery(
        query_id=query_id,
        system=linear_system,
        proof=LinearFeasibilityProof(
            status=FeasibilityStatus.UNSAT,
            farkas=FarkasInfeasibilityCertificate(tuple(multipliers)),
            evidence_reference=f"farkas://{query_id}",
        ),
    )


def test_exact_rational_witness_is_verified_before_sat_is_exported() -> None:
    retained = system(
        inequality((-1,), "-1/5", "x >= 1/5"),
        inequality((1,), 1, "x <= 1"),
    )
    certificate = verify_linear_query(sat_query("retained", retained, ("1/5",)))

    assert certificate.status is FeasibilityStatus.SAT
    assert retained.holds_at((Fraction(1, 5),))


def test_invalid_sat_witness_is_rejected() -> None:
    retained = system(inequality((-1,), "-1/5", "x >= 1/5"))
    with pytest.raises(ValueError, match="violates"):
        verify_linear_query(sat_query("bad_witness", retained, (0,)))


def test_farkas_certificate_verifies_linear_infeasibility_exactly() -> None:
    # -x <= -1/5 and x <= 0 imply 0 <= -1/5 after summing with weights (1, 1).
    inactive = system(
        inequality((-1,), "-1/5", "x >= 1/5"),
        inequality((1,), 0, "x <= 0"),
    )
    certificate = verify_linear_query(unsat_query("inactive", inactive, (1, 1)))

    assert certificate.status is FeasibilityStatus.UNSAT


def test_invalid_farkas_certificate_is_rejected() -> None:
    inactive = system(
        inequality((-1,), "-1/5"),
        inequality((1,), 0),
    )
    with pytest.raises(ValueError, match="eliminate every variable"):
        verify_linear_query(unsat_query("bad_farkas", inactive, (1, 0)))


def test_verified_linear_bundle_adapts_to_symbolic_invariant() -> None:
    retained = system(
        inequality((-1,), "-1/5", "x >= 1/5"),
        inequality((1,), 1, "x <= 1"),
    )
    active = system(
        inequality((-1,), "-1/5", "x >= 1/5"),
        inequality((1,), 1, "x <= 1"),
        inequality((-1,), 0, "x >= 0"),
    )
    inactive = system(
        inequality((-1,), "-1/5", "x >= 1/5"),
        inequality((1,), 0, "x <= 0"),
    )
    bundle = LinearMotifQueryBundle(
        nonempty=sat_query("retained", retained, ("1/5",)),
        active=sat_query("retained_and_nonnegative", active, ("1/5",)),
        inactive=unsat_query("retained_and_negative", inactive, (1, 1)),
    )
    cell = linear_bundles_to_symbolic_cell(
        cell_id="primary",
        description="verified interval [1/5, 1]",
        motif_bundles={"nonnegative": bundle},
        coverage_mode=CoverageMode.SOLVER_BACKED,
    )
    report = classify_symbolic_candidate_sets(
        SymbolicCandidateSpace("theta in rational line", ("nonnegative",)),
        (cell,),
    )

    assert report.classifications["nonnegative"].status.value == "invariant"


def test_linear_queries_reject_binary_floating_point_literals() -> None:
    with pytest.raises(TypeError, match="floating-point"):
        inequality((1.0,), 1)
