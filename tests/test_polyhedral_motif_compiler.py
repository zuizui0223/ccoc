from dataclasses import replace

import pytest

from causal_model.admissibility import MotifStatus
from causal_model.certificate_manifest import QueryRole
from causal_model.linear_proof_verifier import (
    FarkasInfeasibilityCertificate,
    LinearFeasibilityProof,
    LinearFeasibilityQuery,
    LinearInequality,
    RationalLinearSystem,
    RationalWitness,
)
from causal_model.polyhedral_motif_compiler import (
    ConflictingCellOverlapProof,
    PolyhedralMotifPartition,
    TaggedPolyhedralCell,
    bind_compiled_polyhedral_motif_proofs,
    compiled_polyhedral_motif_plan_artifact,
    compiled_polyhedral_motif_symbolic_cell,
    compiled_role_proof_bundle_artifact,
    compile_polyhedral_motif_query_plan,
    conjoin_linear_systems,
    polyhedral_motif_partition_artifact,
    verify_compiled_polyhedral_motif_proofs,
    verify_polyhedral_motif_partition,
)
from causal_model.symbolic_candidate_sets import (
    FeasibilityStatus,
    SymbolicCandidateSpace,
    classify_symbolic_candidate_sets,
)


SPACE = SymbolicCandidateSpace("declared tagged polyhedral union", ("focal",))


def row(coefficients, bound, label=""):
    return LinearInequality(tuple(coefficients), bound, label)


def system(*rows, description=""):
    return RationalLinearSystem(("x",), tuple(rows), description)


def positive_cell_system():
    return system(row((-1,), 0, "x >= 0"), description="positive region")


def negative_cell_system():
    return system(row((1,), -1, "x <= -1"), description="negative region")


def sat_proof(query_id, witness):
    return LinearFeasibilityProof(
        status=FeasibilityStatus.SAT,
        witness=RationalWitness((witness,)),
        evidence_reference=f"proof://{query_id}",
    )


def unsat_proof(query_id, multipliers):
    return LinearFeasibilityProof(
        status=FeasibilityStatus.UNSAT,
        farkas=FarkasInfeasibilityCertificate(tuple(multipliers)),
        evidence_reference=f"proof://{query_id}",
    )


def verified_partition(reverse_cells=False):
    negative = TaggedPolyhedralCell(
        cell_id="negative",
        system=negative_cell_system(),
        motif_values={"focal": False},
    )
    positive = TaggedPolyhedralCell(
        cell_id="positive",
        system=positive_cell_system(),
        motif_values={"focal": True},
    )
    overlap = LinearFeasibilityQuery(
        query_id="partition/negative-positive-overlap",
        system=conjoin_linear_systems(negative.system, positive.system),
        proof=unsat_proof("partition/negative-positive-overlap", (1, 1)),
    )
    cells = (positive, negative) if reverse_cells else (negative, positive)
    return verify_polyhedral_motif_partition(
        PolyhedralMotifPartition(
            space=SPACE,
            cells=cells,
            conflicting_overlap_proofs=(
                ConflictingCellOverlapProof("negative", "positive", overlap),
            ),
        )
    )


def plan_for(retained, prefix="run"):
    return compile_polyhedral_motif_query_plan(
        verified_partition(),
        retained_system=retained,
        query_prefix=prefix,
    )


def proofs_from_cell_statuses(plan, *, positive_status, negative_status):
    proofs = {}
    for template in plan.templates:
        status = positive_status if template.partition_cell_id == "positive" else negative_status
        if status == "sat-positive":
            proofs[template.query_id] = sat_proof(template.query_id, 0)
        elif status == "sat-negative":
            proofs[template.query_id] = sat_proof(template.query_id, -1)
        elif status == "unsat":
            proofs[template.query_id] = unsat_proof(template.query_id, (1, 1))
        elif status == "unknown":
            proofs[template.query_id] = LinearFeasibilityProof(status=FeasibilityStatus.UNKNOWN)
        else:
            raise AssertionError(f"unknown fixture status {status}")
    return proofs


def classification_for(plan, proofs):
    bound = bind_compiled_polyhedral_motif_proofs(plan, proofs_by_query_id=proofs)
    verified = verify_compiled_polyhedral_motif_proofs(bound)
    cell = compiled_polyhedral_motif_symbolic_cell(
        verified,
        cell_id="primary",
        description="compiler-derived retained union",
    )
    return verified, classify_symbolic_candidate_sets(SPACE, (cell,))


def test_compiler_generates_complementary_branch_families_from_one_partition():
    # Retain x >= 0. The negative partition branch is exactly infeasible.
    retained = system(row((-1,), 0, "retain x >= 0"), description="retained")
    plan = plan_for(retained)

    assert tuple(template.partition_cell_id for template in plan.nonempty_templates) == ("negative", "positive")
    assert tuple(template.partition_cell_id for template in plan.active_templates["focal"]) == ("positive",)
    assert tuple(template.partition_cell_id for template in plan.inactive_templates["focal"]) == ("negative",)

    proofs = proofs_from_cell_statuses(plan, positive_status="sat-positive", negative_status="unsat")
    verified, report = classification_for(plan, proofs)

    assert verified.motif_queries["focal"].nonempty.status is FeasibilityStatus.SAT
    assert verified.motif_queries["focal"].active.status is FeasibilityStatus.SAT
    assert verified.motif_queries["focal"].inactive.status is FeasibilityStatus.UNSAT
    assert report.classifications["focal"].status is MotifStatus.INVARIANT


def test_compiler_preserves_excluded_and_unresolved_outcomes_exactly():
    # Retain x <= -1: only the false-tagged cell survives.
    excluded_plan = plan_for(system(row((1,), -1, "retain x <= -1")))
    _, excluded = classification_for(
        excluded_plan,
        proofs_from_cell_statuses(
            excluded_plan,
            positive_status="unsat",
            negative_status="sat-negative",
        ),
    )
    assert excluded.classifications["focal"].status is MotifStatus.EXCLUDED

    # Retain x <= 2: both tagged regions have an exact witness.
    unresolved_plan = plan_for(system(row((1,), 2, "retain x <= 2")))
    _, unresolved = classification_for(
        unresolved_plan,
        proofs_from_cell_statuses(
            unresolved_plan,
            positive_status="sat-positive",
            negative_status="sat-negative",
        ),
    )
    assert unresolved.classifications["focal"].status is MotifStatus.UNRESOLVED


def test_conflicting_tags_require_exact_nonoverlap_proof():
    positive = TaggedPolyhedralCell(
        cell_id="positive",
        system=positive_cell_system(),
        motif_values={"focal": True},
    )
    contradictory = TaggedPolyhedralCell(
        cell_id="contradictory",
        system=positive_cell_system(),
        motif_values={"focal": False},
    )
    missing = PolyhedralMotifPartition(
        space=SPACE,
        cells=(contradictory, positive),
    )
    with pytest.raises(ValueError, match="exactly one overlap-UNSAT"):
        verify_polyhedral_motif_partition(missing)

    malformed_overlap = LinearFeasibilityQuery(
        query_id="partition/contradictory-positive-overlap",
        system=conjoin_linear_systems(contradictory.system, positive.system),
        proof=unsat_proof("partition/contradictory-positive-overlap", (1, 1)),
    )
    malformed = PolyhedralMotifPartition(
        space=SPACE,
        cells=(contradictory, positive),
        conflicting_overlap_proofs=(
            ConflictingCellOverlapProof("contradictory", "positive", malformed_overlap),
        ),
    )
    with pytest.raises(ValueError, match="does not eliminate"):
        verify_polyhedral_motif_partition(malformed)


def test_tagged_union_is_canonical_under_cell_input_order_and_manifest_bindable():
    first = verified_partition()
    second = verified_partition(reverse_cells=True)
    retained = system(row((-1,), 0, "retain x >= 0"))
    first_plan = compile_polyhedral_motif_query_plan(first, retained_system=retained, query_prefix="run")
    second_plan = compile_polyhedral_motif_query_plan(second, retained_system=retained, query_prefix="run")

    assert first.partition_digest == second.partition_digest
    assert first_plan.plan_digest == second_plan.plan_digest
    assert polyhedral_motif_partition_artifact(first).sha256 == polyhedral_motif_partition_artifact(second).sha256
    assert compiled_polyhedral_motif_plan_artifact(first_plan).sha256 == compiled_polyhedral_motif_plan_artifact(second_plan).sha256


def test_binding_accepts_only_compiler_template_ids_and_role_artifacts_commit_all_branches():
    plan = plan_for(system(row((-1,), 0, "retain x >= 0")))
    proofs = proofs_from_cell_statuses(plan, positive_status="sat-positive", negative_status="unsat")
    with pytest.raises(ValueError, match="exactly every compiler-generated"):
        bind_compiled_polyhedral_motif_proofs(plan, proofs_by_query_id={})

    bound = bind_compiled_polyhedral_motif_proofs(plan, proofs_by_query_id=proofs)
    verified = verify_compiled_polyhedral_motif_proofs(bound)
    inactive = compiled_role_proof_bundle_artifact(
        verified,
        motif="focal",
        role=QueryRole.INACTIVE,
    )
    active = compiled_role_proof_bundle_artifact(
        verified,
        motif="focal",
        role=QueryRole.ACTIVE,
    )
    assert inactive.sha256 != active.sha256

    changed_proof = replace(
        proofs[next(query_id for query_id in proofs if "/inactive/" in query_id)],
        evidence_reference="proof://changed-inactive-evidence",
    )
    changed = dict(proofs)
    changed[next(query_id for query_id in proofs if "/inactive/" in query_id)] = changed_proof
    changed_verified = verify_compiled_polyhedral_motif_proofs(
        bind_compiled_polyhedral_motif_proofs(plan, proofs_by_query_id=changed)
    )
    assert (
        compiled_role_proof_bundle_artifact(changed_verified, motif="focal", role=QueryRole.INACTIVE).sha256
        != inactive.sha256
    )


def test_empty_tag_family_is_structurally_unsat_without_a_manual_inactive_system():
    only_true = TaggedPolyhedralCell(
        cell_id="only-true",
        system=positive_cell_system(),
        motif_values={"focal": True},
    )
    partition = verify_polyhedral_motif_partition(
        PolyhedralMotifPartition(space=SPACE, cells=(only_true,))
    )
    plan = compile_polyhedral_motif_query_plan(
        partition,
        retained_system=positive_cell_system(),
        query_prefix="only-true",
    )
    assert plan.inactive_templates["focal"] == ()
    proofs = {
        template.query_id: sat_proof(template.query_id, 0)
        for template in plan.templates
    }
    verified, report = classification_for(plan, proofs)
    assert verified.motif_queries["focal"].inactive.status is FeasibilityStatus.UNSAT
    assert report.classifications["focal"].status is MotifStatus.INVARIANT


def test_unknown_branch_prevents_overclaim_when_the_union_cannot_be_decided():
    plan = plan_for(system(row((1,), 2, "retain x <= 2")))
    proofs = proofs_from_cell_statuses(plan, positive_status="sat-positive", negative_status="unknown")
    _, report = classification_for(plan, proofs)
    assert report.classifications["focal"].status is MotifStatus.UNSUPPORTED
