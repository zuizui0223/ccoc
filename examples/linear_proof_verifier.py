"""Minimal proof-carrying linear RACH example.

The retained set is x in [1/5, 1]. A rational point proves feasibility and a
Farkas certificate proves that the retained set cannot also satisfy x <= 0.
No raw data and no optimisation solver are used here.

Run:
    python examples/linear_proof_verifier.py
"""

from causal_model.linear_proof_verifier import (
    FarkasInfeasibilityCertificate,
    LinearFeasibilityProof,
    LinearFeasibilityQuery,
    LinearInequality,
    LinearMotifQueryBundle,
    RationalLinearSystem,
    RationalWitness,
    linear_bundles_to_symbolic_cell,
)
from causal_model.symbolic_candidate_sets import (
    FeasibilityStatus,
    SymbolicCandidateSpace,
    classify_symbolic_candidate_sets,
)


def query(query_id, constraints, status, witness=None, multipliers=None):
    return LinearFeasibilityQuery(
        query_id=query_id,
        system=constraints,
        proof=LinearFeasibilityProof(
            status=status,
            witness=RationalWitness((witness,)) if witness is not None else None,
            farkas=FarkasInfeasibilityCertificate(tuple(multipliers)) if multipliers else None,
            evidence_reference=f"proof://{query_id}",
        ),
    )


def main() -> None:
    retained = RationalLinearSystem(
        ("x",),
        (
            LinearInequality((-1,), "-1/5"),
            LinearInequality((1,), 1),
        ),
    )
    incompatible = RationalLinearSystem(
        ("x",),
        (
            LinearInequality((-1,), "-1/5"),
            LinearInequality((1,), 0),
        ),
    )
    bundle = LinearMotifQueryBundle(
        nonempty=query("retained", retained, FeasibilityStatus.SAT, witness="1/5"),
        active=query("active", retained, FeasibilityStatus.SAT, witness="1/5"),
        inactive=query("inactive", incompatible, FeasibilityStatus.UNSAT, multipliers=(1, 1)),
    )
    cell = linear_bundles_to_symbolic_cell(
        cell_id="primary",
        description="verified rational interval",
        motif_bundles={"nonnegative": bundle},
    )
    report = classify_symbolic_candidate_sets(
        SymbolicCandidateSpace("x in Q", ("nonnegative",)),
        (cell,),
    )
    print(report.classifications["nonnegative"].status.value)


if __name__ == "__main__":
    main()
