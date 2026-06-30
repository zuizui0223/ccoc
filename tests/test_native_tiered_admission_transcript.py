from dataclasses import replace

import pytest

from causal_model.anytime_symbolic_lifting import AnytimeSymbolicJointCoverageCertificate
from causal_model.canonical_tiered_manifest_json import canonical_tiered_manifest_digest
from causal_model.certificate_manifest import (
    ArtifactReference,
    ExternalAssertionBinding,
    ManifestTarget,
    build_anytime_symbolic_manifest,
)
from causal_model.exact_compiled_polyhedral_extension_admission import (
    ExactCompiledPolyhedralExtensionAdmissionSchema,
    ExactCompiledPolyhedralExtensionLook,
    ExactCompiledPolyhedralProofCell,
    admit_exact_compiled_polyhedral_extension_look,
    compiled_query_plan_for_admission,
    verify_exact_compiled_polyhedral_extension_admission_schema,
)
from causal_model.linear_proof_verifier import (
    FarkasInfeasibilityCertificate,
    LinearFeasibilityProof,
    LinearFeasibilityQuery,
    LinearInequality,
    RationalLinearSystem,
    RationalWitness,
)
from causal_model.native_tiered_admission_transcript import (
    NativeTieredAdmissionTranscript,
    append_native_tiered_admitted_look,
    build_native_tiered_manifest_for_admitted_look,
    create_native_tiered_admission_transcript,
    create_native_tiered_transcript_head_checkpoint,
    verify_native_tiered_admission_transcript,
)
from causal_model.online_polyhedral_inclusion_schema import MonotonePolyhedralInclusionSchema
from causal_model.polyhedral_motif_compiler import (
    ConflictingCellOverlapProof,
    PolyhedralMotifPartition,
    TaggedPolyhedralCell,
    conjoin_linear_systems,
    verify_polyhedral_motif_partition,
)
from causal_model.rational_polyhedral_inclusion import (
    FarkasRowImplicationCertificate,
    RationalPolyhedralInclusionProof,
    RationalPolyhedralInclusionQuery,
)
from causal_model.symbolic_candidate_sets import FeasibilityStatus, SymbolicCandidateSpace
from causal_model.tiered_certificate_manifest import QueryTier


SPACE = SymbolicCandidateSpace("native v2 transcript candidate space", ("focal",))


def row(coefficients, bound, label=""):
    return LinearInequality(tuple(coefficients), bound, label)


def system(*rows, description=""):
    return RationalLinearSystem(("x",), tuple(rows), description)


def true_system():
    return system(row((-1,), 0, "x >= 0"), description="true partition cell")


def false_system():
    return system(row((1,), -1, "x <= -1"), description="false partition cell")


def base_inner():
    return system(row((-1,), 0, "x >= 0"), row((1,), 1, "x <= 1"), description="base")


def later_inner():
    return system(
        row((-1,), 0, "x >= 0"),
        row((1,), 1, "x <= 1"),
        row((1,), "3/4", "x <= 3/4"),
        description="later inner",
    )


def fixed_outer():
    return system(row((-1,), 0, "x >= 0"), row((1,), 2, "x <= 2"), description="outer")


def partition():
    false = TaggedPolyhedralCell("false", false_system(), {"focal": False})
    true = TaggedPolyhedralCell("true", true_system(), {"focal": True})
    overlap = LinearFeasibilityQuery(
        query_id="false-true-overlap",
        system=conjoin_linear_systems(false.system, true.system),
        proof=LinearFeasibilityProof(
            status=FeasibilityStatus.UNSAT,
            farkas=FarkasInfeasibilityCertificate((1, 1)),
            evidence_reference="proof://false-true-overlap",
        ),
    )
    return verify_polyhedral_motif_partition(
        PolyhedralMotifPartition(
            space=SPACE,
            cells=(false, true),
            conflicting_overlap_proofs=(ConflictingCellOverlapProof("false", "true", overlap),),
        )
    )


def inclusion_query():
    return RationalPolyhedralInclusionQuery(
        query_id="base-in-outer",
        inner_system=base_inner(),
        outer_system=fixed_outer(),
        proof=RationalPolyhedralInclusionProof(
            inner_witness=RationalWitness((0,)),
            row_certificates=(
                FarkasRowImplicationCertificate(0, (1, 0)),
                FarkasRowImplicationCertificate(1, (0, 1)),
            ),
            evidence_reference="proof://base-in-outer",
        ),
    )


def verified_schema():
    return verify_exact_compiled_polyhedral_extension_admission_schema(
        ExactCompiledPolyhedralExtensionAdmissionSchema(
            space=SPACE,
            required_cell_ids=("primary",),
            inclusion_schema=MonotonePolyhedralInclusionSchema(
                inner_tier_id="inner",
                outer_tier_id="outer",
                base_queries_by_cell={"primary": inclusion_query()},
            ),
            motif_partition=partition(),
        )
    )


def proof_cell(schema, *, look, tier, retained, false_status="unsat"):
    plan = compiled_query_plan_for_admission(
        schema,
        look=look,
        tier=tier,
        cell_id="primary",
        retained_system=retained,
    )
    proofs = {}
    for template in plan.templates:
        if template.partition_cell_id == "true":
            proofs[template.query_id] = LinearFeasibilityProof(
                status=FeasibilityStatus.SAT,
                witness=RationalWitness((0,)),
                evidence_reference=f"proof://{template.query_id}",
            )
        elif false_status == "unknown":
            proofs[template.query_id] = LinearFeasibilityProof(status=FeasibilityStatus.UNKNOWN)
        else:
            multipliers = (1, *(0 for _ in range(len(template.system.inequalities) - 2)), 1)
            proofs[template.query_id] = LinearFeasibilityProof(
                status=FeasibilityStatus.UNSAT,
                farkas=FarkasInfeasibilityCertificate(multipliers),
                evidence_reference=f"proof://{template.query_id}",
            )
    return ExactCompiledPolyhedralProofCell(
        description=f"{tier} proof cell at {look}",
        retained_system=retained,
        proofs_by_query_id=proofs,
    )


def admitted_look(schema, look=1, *, false_status="unsat"):
    return admit_exact_compiled_polyhedral_extension_look(
        schema,
        ExactCompiledPolyhedralExtensionLook(
            look=look,
            inner_cells_by_id={
                "primary": proof_cell(
                    schema,
                    look=look,
                    tier="inner",
                    retained=later_inner(),
                    false_status=false_status,
                )
            },
            outer_cells_by_id={
                "primary": proof_cell(
                    schema,
                    look=look,
                    tier="outer",
                    retained=fixed_outer(),
                    false_status=false_status,
                )
            },
            evidence_reference=f"proof://native-tiered-look-{look}",
        ),
    )


def coverage():
    return AnytimeSymbolicJointCoverageCertificate(
        true_candidate_label="theta_star",
        required_cell_ids=("primary",),
        lower_bound=0.95,
        method="external all-look coverage",
    )


def source_v1_manifest(schema, coverage_certificate):
    payloads = {
        "candidate-space": b'{"variables":["x"]}',
        "motif": b'{"tagged_union":true}',
        "coverage": b'{"method":"confidence-sequence"}',
        "solver": b'{"method":"compiler-exact-admission"}',
    }
    target = ManifestTarget.from_payloads(
        SPACE,
        candidate_space_payload=payloads["candidate-space"],
        motif_definition_payloads={"focal": payloads["motif"]},
        required_cell_ids=("primary",),
        certified_looks=None,
    )
    coverage_assertion = ExternalAssertionBinding.from_payload(
        kind="time-uniform-statistical-coverage",
        lower_bound=coverage_certificate.lower_bound,
        method=coverage_certificate.method,
        assumptions=coverage_certificate.assumptions,
        evidence_artifact_id="coverage",
        evidence_payload=payloads["coverage"],
    )
    solver = schema.all_look_solver_certificate
    solver_assertion = ExternalAssertionBinding.from_payload(
        kind="time-uniform-solver-semantic-validity",
        lower_bound=solver.lower_bound,
        method=solver.method,
        assumptions=solver.assumptions,
        evidence_artifact_id="solver",
        evidence_payload=payloads["solver"],
    )
    return build_anytime_symbolic_manifest(
        target=target,
        coverage_certificate=coverage_certificate,
        solver_certificate=solver,
        coverage_assertion=coverage_assertion,
        solver_assertion=solver_assertion,
    )


def transcript_fixture():
    schema = verified_schema()
    coverage_certificate = coverage()
    source = source_v1_manifest(schema, coverage_certificate)
    transcript = create_native_tiered_admission_transcript(
        transcript_id="native-tiered-run",
        verified_schema=schema,
        source_v1_manifest=source,
        coverage_certificate=coverage_certificate,
        base_admission_schema_artifact=ArtifactReference.from_payload(
            "base-admission-schema",
            b"serialized exact base inclusion schema",
            media_type="application/json",
        ),
    )
    return schema, coverage_certificate, source, transcript


def append(transcript, schema, coverage_certificate, source, look, *, false_status="unsat"):
    return append_native_tiered_admitted_look(
        transcript,
        verified_schema=schema,
        admitted_look=admitted_look(schema, look, false_status=false_status),
        source_v1_manifest=source,
        coverage_certificate=coverage_certificate,
    )


def test_native_builder_derives_v2_plan_and_decisive_role_bindings_from_admitted_look():
    schema, coverage_certificate, source, _ = transcript_fixture()
    evidence = build_native_tiered_manifest_for_admitted_look(
        verified_schema=schema,
        admitted_look=admitted_look(schema, 1),
        source_v1_manifest=source,
        coverage_certificate=coverage_certificate,
    )

    manifest = evidence.tiered_bundle.manifest
    assert len(manifest.tiered_query_plans) == 2
    assert len(manifest.solver_query_proofs) == 6
    assert {binding.tier for binding in manifest.solver_query_proofs} == {QueryTier.INNER, QueryTier.OUTER}
    assert evidence.tiered_bundle.canonical_digest == canonical_tiered_manifest_digest(manifest)
    assert evidence.tiered_bundle.manifest_artifact.sha256 == evidence.tiered_bundle.canonical_digest


def test_native_v2_digest_is_directly_anchored_in_entry_chain_and_checkpoint_head():
    schema, coverage_certificate, source, transcript = transcript_fixture()
    one = append(transcript, schema, coverage_certificate, source, 1)
    two = append(one, schema, coverage_certificate, source, 2)

    report = verify_native_tiered_admission_transcript(two, expected_head_digest=two.head_digest)
    assert report.entry_count == 2
    assert len(report.native_tiered_manifest_digests) == 2
    assert two.chain.entries[0].admission_evidence_reference == two.entries[0].evidence.commitment_reference
    assert two.entries[0].evidence.tiered_bundle.canonical_digest in two.entries[0].evidence.commitment_payload.decode("utf-8")
    checkpoint = create_native_tiered_transcript_head_checkpoint(two, checkpoint_sequence=1)
    assert checkpoint.head_digest == two.head_digest


def test_unknown_role_remains_in_status_table_but_is_not_a_v2_decisive_proof_binding():
    schema, coverage_certificate, source, transcript = transcript_fixture()
    one = append(transcript, schema, coverage_certificate, source, 1, false_status="unknown")
    entry = one.entries[0]

    inactive_statuses = [
        status
        for status in entry.evidence.tiered_bundle.role_statuses
        if status.role.value == "inactive"
    ]
    assert {status.status for status in inactive_statuses} == {FeasibilityStatus.UNKNOWN}
    assert all(
        binding.role.value != "inactive"
        for binding in entry.evidence.tiered_bundle.manifest.solver_query_proofs
    )
    assert one.chain.entries[0].outer_statuses["focal"] == "unsupported"
    verify_native_tiered_admission_transcript(one)


def test_tampering_native_v2_manifest_or_source_v1_digest_breaks_transcript_verification():
    schema, coverage_certificate, source, transcript = transcript_fixture()
    one = append(transcript, schema, coverage_certificate, source, 1)
    entry = one.entries[0]

    altered_manifest = replace(
        entry.evidence.tiered_bundle.manifest,
        semantic_partition_artifact=ArtifactReference.from_payload(
            "altered-partition",
            b"different partition",
            media_type="application/json",
        ),
    )
    altered_bundle = replace(entry.evidence.tiered_bundle, manifest=altered_manifest)
    altered_entry = replace(entry, evidence=replace(entry.evidence, tiered_bundle=altered_bundle))
    altered = NativeTieredAdmissionTranscript(
        header=one.header,
        chain=one.chain,
        entries=(altered_entry,),
    )
    with pytest.raises(ValueError, match="does not hash the canonical v2 manifest"):
        verify_native_tiered_admission_transcript(altered)

    changed_source = replace(
        entry.evidence.tiered_bundle,
        source_v1_manifest_digest="0" * 64,
    )
    changed_entry = replace(entry, evidence=replace(entry.evidence, tiered_bundle=changed_source))
    changed = NativeTieredAdmissionTranscript(
        header=one.header,
        chain=one.chain,
        entries=(changed_entry,),
    )
    with pytest.raises(ValueError, match="source v1 digest"):
        verify_native_tiered_admission_transcript(changed)


def test_live_source_v1_manifest_drift_rejects_future_append_without_rewriting_history():
    schema, coverage_certificate, source, transcript = transcript_fixture()
    one = append(transcript, schema, coverage_certificate, source, 1)
    drifted = replace(
        source,
        solver_assertion=replace(source.solver_assertion, method="different verifier assertion"),
    )
    with pytest.raises(ValueError, match="live compiler schema or source v1 manifest"):
        append_native_tiered_admitted_look(
            one,
            verified_schema=schema,
            admitted_look=admitted_look(schema, 2),
            source_v1_manifest=drifted,
            coverage_certificate=coverage_certificate,
        )
