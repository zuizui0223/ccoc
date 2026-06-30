import json

import pytest

from causal_model.certificate_manifest import QueryRole
from causal_model.linear_proof_verifier import (
    FarkasInfeasibilityCertificate,
    LinearFeasibilityProof,
    LinearFeasibilityQuery,
    LinearInequality,
    RationalLinearSystem,
    RationalWitness,
)
from causal_model.replayable_exact_linear_proofs import (
    ExactLinearProofBundle,
    canonical_exact_linear_bundle_bytes,
    canonical_exact_linear_query_bytes,
    exact_linear_bundle_artifact,
    exact_linear_query_artifact,
    parse_canonical_exact_linear_bundle,
    parse_canonical_exact_linear_query,
    replay_exact_linear_bundle,
    replay_exact_linear_query,
)
from causal_model.symbolic_candidate_sets import FeasibilityStatus


def system(*rows):
    return RationalLinearSystem(("x",), tuple(rows))


def sat_query(query_id="sat"):
    return LinearFeasibilityQuery(
        query_id=query_id,
        system=system(LinearInequality((1,), "1/2")),
        proof=LinearFeasibilityProof(
            status=FeasibilityStatus.SAT,
            witness=RationalWitness(("0",)),
            evidence_reference=f"proof://{query_id}",
            producer="test backend",
        ),
        assumptions=("exact query fixture",),
    )


def unsat_query(query_id="unsat"):
    return LinearFeasibilityQuery(
        query_id=query_id,
        system=system(
            LinearInequality((-1,), "0"),
            LinearInequality((1,), "-1"),
        ),
        proof=LinearFeasibilityProof(
            status=FeasibilityStatus.UNSAT,
            farkas=FarkasInfeasibilityCertificate(("1", "1")),
            evidence_reference=f"proof://{query_id}",
            producer="test backend",
        ),
        assumptions=("exact query fixture",),
    )


def unknown_query(query_id="unknown"):
    return LinearFeasibilityQuery(
        query_id=query_id,
        system=system(LinearInequality((1,), "1")),
        proof=LinearFeasibilityProof(
            status=FeasibilityStatus.UNKNOWN,
            producer="test backend",
        ),
    )


def bundle(branches, status, bundle_id="bundle"):
    return ExactLinearProofBundle(
        bundle_id=bundle_id,
        plan_digest="a" * 64,
        partition_digest="b" * 64,
        motif="focal",
        role=QueryRole.INACTIVE,
        branches=tuple(branches),
        aggregate_status=status,
    )


def test_query_artifact_is_strict_canonical_and_replays_exact_sat_proof():
    query = sat_query()
    raw = canonical_exact_linear_query_bytes(query)
    artifact = exact_linear_query_artifact(query)
    replayed = replay_exact_linear_query(raw, expected_digest=artifact.sha256)

    assert replayed.certificate is not None
    assert replayed.certificate.status is FeasibilityStatus.SAT
    assert replayed.query.system.inequalities[0].bound.numerator == 1
    assert replayed.query.system.inequalities[0].bound.denominator == 2
    assert parse_canonical_exact_linear_query(raw).canonical_digest == artifact.sha256

    with pytest.raises(ValueError, match="not strict canonical"):
        parse_canonical_exact_linear_query(raw + b"\n")


def test_query_replay_rejects_noncanonical_rationals_and_a_canonical_but_invalid_witness():
    raw = canonical_exact_linear_query_bytes(sat_query())
    noncanonical = raw.replace(b'"1/2"', b'"2/4"')
    with pytest.raises(ValueError, match="canonical rational"):
        parse_canonical_exact_linear_query(noncanonical)

    object_value = json.loads(raw)
    object_value["query"]["proof"]["witness"] = ["1"]
    invalid_but_canonical = json.dumps(
        object_value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    with pytest.raises(ValueError, match="SAT witness violates"):
        replay_exact_linear_query(invalid_but_canonical)


def test_bundle_replays_every_branch_and_recomputes_exact_finite_union_status():
    sat_unsat = bundle((sat_query("a-sat"), unsat_query("b-unsat")), FeasibilityStatus.SAT)
    raw = canonical_exact_linear_bundle_bytes(sat_unsat)
    artifact = exact_linear_bundle_artifact(sat_unsat)
    replayed = replay_exact_linear_bundle(
        raw,
        expected_digest=artifact.sha256,
        expected_plan_digest="a" * 64,
        expected_partition_digest="b" * 64,
        expected_motif="focal",
        expected_role=QueryRole.INACTIVE,
    )
    assert replayed.replayed_aggregate_status is FeasibilityStatus.SAT
    assert set(replayed.branch_certificates or {}) == {"a-sat", "b-unsat"}

    all_unsat = bundle((unsat_query("first"), unsat_query("second")), FeasibilityStatus.UNSAT)
    assert replay_exact_linear_bundle(canonical_exact_linear_bundle_bytes(all_unsat)).replayed_aggregate_status is FeasibilityStatus.UNSAT

    mixed_unknown = bundle((unsat_query("first"), unknown_query("unknown")), FeasibilityStatus.UNKNOWN)
    assert replay_exact_linear_bundle(canonical_exact_linear_bundle_bytes(mixed_unknown)).replayed_aggregate_status is FeasibilityStatus.UNKNOWN

    empty = bundle((), FeasibilityStatus.UNSAT, bundle_id="empty")
    assert replay_exact_linear_bundle(canonical_exact_linear_bundle_bytes(empty)).replayed_aggregate_status is FeasibilityStatus.UNSAT


def test_bundle_rejects_declared_status_mismatch_duplicate_keys_and_wrong_digest():
    wrong = bundle((sat_query(),), FeasibilityStatus.UNSAT)
    with pytest.raises(ValueError, match="aggregate status"):
        canonical_exact_linear_bundle_bytes(wrong)

    raw = canonical_exact_linear_bundle_bytes(bundle((unsat_query(),), FeasibilityStatus.UNSAT))
    duplicate = raw.replace(b'"bundle_id":"bundle"', b'"bundle_id":"bundle","bundle_id":"bundle"')
    with pytest.raises(ValueError, match="duplicate JSON object key"):
        parse_canonical_exact_linear_bundle(duplicate)

    with pytest.raises(ValueError, match="does not match expected_digest"):
        replay_exact_linear_bundle(raw, expected_digest="0" * 64)
