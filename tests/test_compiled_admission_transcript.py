from dataclasses import replace

import pytest

from causal_model.admission_transcript import AdmissionTranscript
from causal_model.anytime_symbolic_lifting import AnytimeSymbolicJointCoverageCertificate
from causal_model.certificate_manifest import (
    ArtifactReference,
    ExternalAssertionBinding,
    ManifestTarget,
    build_anytime_symbolic_manifest,
)
from causal_model.compiled_admission_transcript import (
    CompiledAdmissionTranscript,
    append_compiled_admitted_look,
    create_compiled_admission_transcript,
    create_compiled_transcript_head_checkpoint,
    verify_compiled_admission_transcript,
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


SPACE = SymbolicCandidateSpace("compiled transcript candidate space", ("focal",))


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
            evidence_reference=f"proof://compiled-look-{look}",
        ),
    )


def coverage():
    return AnytimeSymbolicJointCoverageCertificate(
        true_candidate_label="theta_star",
        required_cell_ids=("primary",),
        lower_bound=0.95,
        method="external all-look coverage",
    )


def manifest_for(schema, coverage_certificate):
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
    coverage_binding = ExternalAssertionBinding.from_payload(
        kind="time-uniform-statistical-coverage",
        lower_bound=coverage_certificate.lower_bound,
        method=coverage_certificate.method,
        assumptions=coverage_certificate.assumptions,
        evidence_artifact_id="coverage",
        evidence_payload=payloads["coverage"],
    )
    solver = schema.all_look_solver_certificate
    solver_binding = ExternalAssertionBinding.from_payload(
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
        coverage_assertion=coverage_binding,
        solver_assertion=solver_binding,
    )


def transcript_fixture():
    schema = verified_schema()
    coverage_certificate = coverage()
    manifest = manifest_for(schema, coverage_certificate)
    transcript = create_compiled_admission_transcript(
        transcript_id="compiled-admission-run",
        verified_schema=schema,
        manifest=manifest,
        coverage_certificate=coverage_certificate,
        base_admission_schema_artifact=ArtifactReference.from_payload(
            "base-admission-schema",
            b"serialized exact base inclusion schema",
            media_type="application/json",
        ),
    )
    return schema, coverage_certificate, manifest, transcript


def append(transcript, schema, coverage_certificate, manifest, look, *, false_status="unsat"):
    return append_compiled_admitted_look(
        transcript,
        verified_schema=schema,
        admitted_look=admitted_look(schema, look, false_status=false_status),
        manifest=manifest,
        coverage_certificate=coverage_certificate,
    )


def test_compiler_transcript_binds_partition_plan_and_all_role_families_in_base_hash_chain():
    schema, coverage_certificate, manifest, transcript = transcript_fixture()
    one = append(transcript, schema, coverage_certificate, manifest, 1)
    two = append(one, schema, coverage_certificate, manifest, 2)

    report = verify_compiled_admission_transcript(two, expected_head_digest=two.head_digest)
    assert report.entry_count == 2
    assert report.recorded_looks == (1, 2)
    evidence = two.entries[0].evidence
    assert len(evidence.plan_artifacts) == 2
    assert len(evidence.role_proof_artifacts) == 6
    base = two.chain.entries[0]
    assert base.admission_evidence_reference == evidence.commitment_reference
    assert base.outer_statuses["focal"] == "invariant"
    assert base.extension_statuses["focal"] == "extension-stable"


def test_artifact_tampering_or_missing_role_family_breaks_the_adapter_verification():
    schema, coverage_certificate, manifest, transcript = transcript_fixture()
    transcript = append(transcript, schema, coverage_certificate, manifest, 1)
    entry = transcript.entries[0]

    altered_role = replace(entry.evidence.role_proof_artifacts[0], artifact=ArtifactReference.from_payload(
        "substituted",
        b"not the original branch proof family",
        media_type="application/json",
    ))
    altered_evidence = replace(
        entry.evidence,
        role_proof_artifacts=(altered_role, *entry.evidence.role_proof_artifacts[1:]),
    )
    altered = CompiledAdmissionTranscript(
        header=transcript.header,
        chain=transcript.chain,
        entries=(replace(entry, evidence=altered_evidence),),
    )
    with pytest.raises(ValueError, match="does not bind the compiler evidence"):
        verify_compiled_admission_transcript(altered)

    missing_evidence = replace(entry.evidence, role_proof_artifacts=entry.evidence.role_proof_artifacts[:-1])
    missing = CompiledAdmissionTranscript(
        header=transcript.header,
        chain=transcript.chain,
        entries=(replace(entry, evidence=missing_evidence),),
    )
    with pytest.raises(ValueError, match="exactly one role artifact"):
        verify_compiled_admission_transcript(missing)


def test_compiler_transcript_preserves_unknown_as_unsupported_and_supports_generic_signed_checkpoint_payloads():
    schema, coverage_certificate, manifest, transcript = transcript_fixture()
    transcript = append(transcript, schema, coverage_certificate, manifest, 1, false_status="unknown")

    assert transcript.chain.entries[0].outer_statuses["focal"] == "unsupported"
    assert transcript.chain.entries[0].extension_statuses["focal"] == "unsupported"
    checkpoint = create_compiled_transcript_head_checkpoint(transcript, checkpoint_sequence=1)
    assert checkpoint.head_digest == transcript.head_digest
    assert checkpoint.entry_count == 1


def test_header_cannot_be_reused_with_a_different_partition_or_schema_commitment():
    schema, coverage_certificate, manifest, transcript = transcript_fixture()
    forged_header = replace(
        transcript.header,
        schema_artifacts=replace(
            transcript.header.schema_artifacts,
            partition_artifact=ArtifactReference.from_payload(
                "different-partition",
                b"different tagged union",
                media_type="application/json",
            ),
        ),
    )
    forged = CompiledAdmissionTranscript(
        header=forged_header,
        chain=AdmissionTranscript(header=forged_header.transcript_header),
    )
    with pytest.raises(ValueError, match="chain header does not match"):
        verify_compiled_admission_transcript(forged)

    with pytest.raises(ValueError, match="partition artifact"):
        append_compiled_admitted_look(
            forged,
            verified_schema=schema,
            admitted_look=admitted_look(schema, 1),
            manifest=manifest,
            coverage_certificate=coverage_certificate,
        )
