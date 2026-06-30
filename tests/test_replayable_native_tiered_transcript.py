from dataclasses import replace

import pytest

from causal_model.anytime_symbolic_lifting import AnytimeSymbolicJointCoverageCertificate
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
from causal_model.replayable_native_tiered_transcript import (
    ReplayableArtifactRegistry,
    ReplayableNativeTieredAdmissionTranscript,
    append_replayable_native_tiered_admitted_look,
    create_replayable_native_tiered_admission_transcript,
    create_replayable_native_tiered_transcript_head_checkpoint,
    verify_replayable_native_tiered_admission_transcript,
)
from causal_model.symbolic_candidate_sets import FeasibilityStatus, SymbolicCandidateSpace


SPACE = SymbolicCandidateSpace("replay-native transcript space", ("focal",))


def row(coefficients, bound, label=""):
    return LinearInequality(tuple(coefficients), bound, label)


def system(*rows, description=""):
    return RationalLinearSystem(("x",), tuple(rows), description)


def true_system():
    return system(row((-1,), "0", "x >= 0"), description="true cell")


def false_system():
    return system(row((1,), "-1", "x <= -1"), description="false cell")


def base_inner():
    return system(row((-1,), "0", "x >= 0"), row((1,), "1", "x <= 1"), description="base")


def later_inner():
    return system(
        row((-1,), "0", "x >= 0"),
        row((1,), "1", "x <= 1"),
        row((1,), "3/4", "x <= 3/4"),
        description="later inner",
    )


def fixed_outer():
    return system(row((-1,), "0", "x >= 0"), row((1,), "2", "x <= 2"), description="outer")


def verified_partition():
    false = TaggedPolyhedralCell("false", false_system(), {"focal": False})
    true = TaggedPolyhedralCell("true", true_system(), {"focal": True})
    overlap = LinearFeasibilityQuery(
        query_id="false-true-overlap",
        system=conjoin_linear_systems(false.system, true.system),
        proof=LinearFeasibilityProof(
            status=FeasibilityStatus.UNSAT,
            farkas=FarkasInfeasibilityCertificate(("1", "1")),
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


def base_inclusion_query():
    return RationalPolyhedralInclusionQuery(
        query_id="base-in-outer",
        inner_system=base_inner(),
        outer_system=fixed_outer(),
        proof=RationalPolyhedralInclusionProof(
            inner_witness=RationalWitness(("0",)),
            row_certificates=(
                FarkasRowImplicationCertificate(0, ("1", "0")),
                FarkasRowImplicationCertificate(1, ("0", "1")),
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
                base_queries_by_cell={"primary": base_inclusion_query()},
            ),
            motif_partition=verified_partition(),
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
                witness=RationalWitness(("0",)),
                evidence_reference=f"proof://{template.query_id}",
            )
        elif false_status == "unknown":
            proofs[template.query_id] = LinearFeasibilityProof(status=FeasibilityStatus.UNKNOWN)
        else:
            multipliers = ("1", *("0" for _ in range(len(template.system.inequalities) - 2)), "1")
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


def admitted_look(schema, look, *, false_status="unsat"):
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
            evidence_reference=f"proof://replayable-look-{look}",
        ),
    )


def coverage():
    return AnytimeSymbolicJointCoverageCertificate(
        true_candidate_label="theta_star",
        required_cell_ids=("primary",),
        lower_bound=0.95,
        method="external all-look coverage",
    )


def source_manifest(schema, coverage_certificate):
    target = ManifestTarget.from_payloads(
        SPACE,
        candidate_space_payload=b'{"variables":["x"]}',
        motif_definition_payloads={"focal": b'{"tagged_union":true}'},
        required_cell_ids=("primary",),
        certified_looks=None,
    )
    coverage_assertion = ExternalAssertionBinding.from_payload(
        kind="time-uniform-statistical-coverage",
        lower_bound=coverage_certificate.lower_bound,
        method=coverage_certificate.method,
        assumptions=coverage_certificate.assumptions,
        evidence_artifact_id="coverage",
        evidence_payload=b'{"coverage":"all-look"}',
    )
    solver = schema.all_look_solver_certificate
    solver_assertion = ExternalAssertionBinding.from_payload(
        kind="time-uniform-solver-semantic-validity",
        lower_bound=solver.lower_bound,
        method=solver.method,
        assumptions=solver.assumptions,
        evidence_artifact_id="solver",
        evidence_payload=b'{"solver":"exact"}',
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
    manifest = source_manifest(schema, coverage_certificate)
    transcript = create_replayable_native_tiered_admission_transcript(
        transcript_id="replay-native-run",
        verified_schema=schema,
        source_v1_manifest=manifest,
        coverage_certificate=coverage_certificate,
        base_admission_schema_artifact=ArtifactReference.from_payload(
            "base-schema",
            b"exact base schema",
            media_type="application/json",
        ),
    )
    return schema, coverage_certificate, manifest, transcript


def append(transcript, schema, coverage_certificate, manifest, look, *, false_status="unsat"):
    return append_replayable_native_tiered_admitted_look(
        transcript,
        verified_schema=schema,
        admitted_look=admitted_look(schema, look, false_status=false_status),
        source_v1_manifest=manifest,
        coverage_certificate=coverage_certificate,
    )


def test_two_look_history_replays_every_plan_and_role_family_before_checkpoint():
    schema, coverage_certificate, manifest, transcript = transcript_fixture()
    one = append(transcript, schema, coverage_certificate, manifest, 1)
    two = append(one, schema, coverage_certificate, manifest, 2)

    report = verify_replayable_native_tiered_admission_transcript(two, expected_head_digest=two.head_digest)
    assert report.native_report.entry_count == 2
    assert report.replayed_plan_artifact_count == 4
    assert report.replayed_role_artifact_count == 12
    assert report.replayed_unknown_role_count == 0
    checkpoint = create_replayable_native_tiered_transcript_head_checkpoint(two, checkpoint_sequence=1)
    assert checkpoint.head_digest == two.head_digest


def test_registry_byte_tampering_is_rejected_before_replay_and_unknown_roles_are_replayed_nondecisively():
    schema, coverage_certificate, manifest, transcript = transcript_fixture()
    unknown = append(transcript, schema, coverage_certificate, manifest, 1, false_status="unknown")
    report = verify_replayable_native_tiered_admission_transcript(unknown)
    assert report.replayed_unknown_role_count == 2
    assert all(
        proof.role.value != "inactive"
        for proof in unknown.native_transcript.entries[0].evidence.tiered_bundle.manifest.solver_query_proofs
    )

    payloads = dict(unknown.registry.payloads)
    role_id = next(key for key in payloads if key.startswith("replayable-role:"))
    payloads[role_id] = b"{}"
    tampered = ReplayableNativeTieredAdmissionTranscript(
        native_transcript=unknown.native_transcript,
        registry=ReplayableArtifactRegistry(payloads),
    )
    with pytest.raises(ValueError, match="registry digest mismatch"):
        verify_replayable_native_tiered_admission_transcript(tampered)


def test_missing_replayable_plan_payload_or_live_manifest_drift_blocks_future_append():
    schema, coverage_certificate, manifest, transcript = transcript_fixture()
    one = append(transcript, schema, coverage_certificate, manifest, 1)

    missing = dict(one.registry.payloads)
    plan_id = next(key for key in missing if key.startswith("replayable-plan:"))
    del missing[plan_id]
    broken = ReplayableNativeTieredAdmissionTranscript(
        native_transcript=one.native_transcript,
        registry=ReplayableArtifactRegistry(missing),
    )
    with pytest.raises(ValueError, match="registry is missing"):
        verify_replayable_native_tiered_admission_transcript(broken)

    drifted = replace(
        manifest,
        target=replace(
            manifest.target,
            candidate_space_artifact=ArtifactReference.from_payload(
                "candidate-space",
                b'{"variables":["changed"]}',
                media_type="application/json",
            ),
        ),
    )
    with pytest.raises(ValueError, match="live compiler schema or source v1 manifest"):
        append_replayable_native_tiered_admitted_look(
            one,
            verified_schema=schema,
            admitted_look=admitted_look(schema, 2),
            source_v1_manifest=drifted,
            coverage_certificate=coverage_certificate,
        )
