from dataclasses import replace

import pytest

from causal_model.admission_transcript import (
    AdmissionTranscript,
    AdmissionTranscriptEntry,
    append_admitted_look,
    create_admission_transcript_header,
    create_transcript_decision_anchor,
    verify_admission_transcript,
    verify_transcript_decision_anchor,
)
from causal_model.anytime_symbolic_lifting import AnytimeSymbolicJointCoverageCertificate
from causal_model.certificate_manifest import (
    ArtifactReference,
    ExternalAssertionBinding,
    ManifestTarget,
    build_anytime_symbolic_manifest,
)
from causal_model.exact_polyhedral_extension_admission import (
    ExactLinearProofCell,
    ExactPolyhedralExtensionAdmissionSchema,
    ExactPolyhedralExtensionLook,
    admit_exact_polyhedral_extension_look,
    verify_exact_polyhedral_extension_admission_schema,
)
from causal_model.linear_proof_verifier import (
    FarkasInfeasibilityCertificate,
    LinearFeasibilityProof,
    LinearFeasibilityQuery,
    LinearInequality,
    LinearMotifQueryBundle,
    RationalLinearSystem,
    RationalWitness,
)
from causal_model.online_polyhedral_inclusion_schema import MonotonePolyhedralInclusionSchema
from causal_model.rational_polyhedral_inclusion import (
    FarkasRowImplicationCertificate,
    RationalPolyhedralInclusionProof,
    RationalPolyhedralInclusionQuery,
)
from causal_model.symbolic_candidate_sets import FeasibilityStatus, SymbolicCandidateSpace


SPACE = SymbolicCandidateSpace("exact transcript candidate space", ("focal",))


def row(coefficients, bound, label=""):
    return LinearInequality(tuple(coefficients), bound, label)


def system(*rows, description=""):
    return RationalLinearSystem(("x",), tuple(rows), description)


def base_inner():
    return system(
        row((-1,), "-1/5", "x >= 1/5"),
        row((1,), 1, "x <= 1"),
        description="base inner",
    )


def fixed_outer():
    return system(
        row((-1,), 0, "x >= 0"),
        row((1,), 2, "x <= 2"),
        description="fixed outer",
    )


def later_inner():
    return system(
        row((-1,), "-1/5", "x >= 1/5"),
        row((1,), 1, "x <= 1"),
        row((1,), "3/4", "x <= 3/4"),
        description="later inner",
    )


def sat_query(query_id, linear_system, witness):
    return LinearFeasibilityQuery(
        query_id=query_id,
        system=linear_system,
        proof=LinearFeasibilityProof(
            status=FeasibilityStatus.SAT,
            witness=RationalWitness((witness,)),
            evidence_reference=f"proof://{query_id}",
        ),
    )


def unsat_query(query_id, linear_system, multipliers):
    return LinearFeasibilityQuery(
        query_id=query_id,
        system=linear_system,
        proof=LinearFeasibilityProof(
            status=FeasibilityStatus.UNSAT,
            farkas=FarkasInfeasibilityCertificate(tuple(multipliers)),
            evidence_reference=f"proof://{query_id}",
        ),
    )


def invariant_bundle(prefix, retained, *, inner):
    if inner:
        inactive = system(
            *retained.inequalities,
            row((1,), 0, "x <= 0"),
            description=f"{prefix} inactive",
        )
        inactive_multipliers = (1, 0, 0, 1)
        witness = "1/5"
    else:
        inactive = system(
            *retained.inequalities,
            row((1,), -1, "x <= -1"),
            description=f"{prefix} inactive",
        )
        inactive_multipliers = (1, 0, 1)
        witness = 0
    return LinearMotifQueryBundle(
        nonempty=sat_query(f"{prefix}/nonempty", retained, witness),
        active=sat_query(f"{prefix}/active", retained, witness),
        inactive=unsat_query(f"{prefix}/inactive", inactive, inactive_multipliers),
    )


def base_query():
    return RationalPolyhedralInclusionQuery(
        query_id="base-in-outer",
        inner_system=base_inner(),
        outer_system=fixed_outer(),
        proof=RationalPolyhedralInclusionProof(
            inner_witness=RationalWitness(("1/5",)),
            row_certificates=(
                FarkasRowImplicationCertificate(0, (1, 0)),
                FarkasRowImplicationCertificate(1, (0, 1)),
            ),
            evidence_reference="proof://base-in-outer",
        ),
    )


def verified_schema():
    return verify_exact_polyhedral_extension_admission_schema(
        ExactPolyhedralExtensionAdmissionSchema(
            space=SPACE,
            required_cell_ids=("primary",),
            inclusion_schema=MonotonePolyhedralInclusionSchema(
                inner_tier_id="inner",
                outer_tier_id="outer",
                base_queries_by_cell={"primary": base_query()},
            ),
        )
    )


def admitted_look(look):
    return admit_exact_polyhedral_extension_look(
        verified_schema(),
        ExactPolyhedralExtensionLook(
            look=look,
            inner_cells_by_id={
                "primary": ExactLinearProofCell(
                    description=f"inner cell {look}",
                    motif_bundles={"focal": invariant_bundle(f"inner-{look}", later_inner(), inner=True)},
                )
            },
            outer_cells_by_id={
                "primary": ExactLinearProofCell(
                    description=f"outer cell {look}",
                    motif_bundles={"focal": invariant_bundle(f"outer-{look}", fixed_outer(), inner=False)},
                )
            },
            evidence_reference=f"proof://admitted-look-{look}",
        ),
    )


def coverage_certificate():
    return AnytimeSymbolicJointCoverageCertificate(
        true_candidate_label="theta_star",
        required_cell_ids=("primary",),
        lower_bound=0.95,
        method="external all-look coverage",
        assumptions=("all recorded looks are covered",),
    )


def manifest_for(schema, coverage):
    payloads = {
        "candidate-space": b'{"variables":["x"]}',
        "motif:focal": b'{"predicate":"focal"}',
        "coverage": b'{"method":"confidence-sequence"}',
        "solver": b'{"method":"exact-admission"}',
    }
    target = ManifestTarget.from_payloads(
        SPACE,
        candidate_space_payload=payloads["candidate-space"],
        motif_definition_payloads={"focal": payloads["motif:focal"]},
        required_cell_ids=("primary",),
        certified_looks=None,
    )
    coverage_binding = ExternalAssertionBinding.from_payload(
        kind="time-uniform-statistical-coverage",
        lower_bound=coverage.lower_bound,
        method=coverage.method,
        assumptions=coverage.assumptions,
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
        coverage_certificate=coverage,
        solver_certificate=solver,
        coverage_assertion=coverage_binding,
        solver_assertion=solver_binding,
    )


def transcript_fixture():
    schema = verified_schema()
    coverage = coverage_certificate()
    manifest = manifest_for(schema, coverage)
    header = create_admission_transcript_header(
        transcript_id="exact-admission-run",
        verified_schema=schema,
        manifest=manifest,
        coverage_certificate=coverage,
        admission_schema_artifact=ArtifactReference.from_payload(
            "exact-admission-schema",
            b"serialized base polyhedra and exact proof material",
            media_type="application/json",
        ),
    )
    return schema, coverage, manifest, AdmissionTranscript(header=header)


def append(transcript, schema, coverage, manifest, look):
    return append_admitted_look(
        transcript,
        verified_schema=schema,
        admitted_look=admitted_look(look),
        manifest=manifest,
        coverage_certificate=coverage,
    )


def test_append_chain_records_exact_admitted_statuses_and_manifest_digest():
    schema, coverage, manifest, transcript = transcript_fixture()
    first = append(transcript, schema, coverage, manifest, 1)
    second = append(first, schema, coverage, manifest, 2)

    report = verify_admission_transcript(second, expected_head_digest=second.head_digest)
    assert report.entry_count == 2
    assert report.recorded_looks == (1, 2)
    assert first.entries[0].previous_entry_digest == first.header.genesis_digest
    assert second.entries[1].previous_entry_digest == first.head_digest
    assert second.entries[0].outer_statuses["focal"] == "invariant"
    assert second.entries[0].extension_statuses["focal"] == "extension-stable"


def test_middle_entry_tampering_breaks_the_next_hash_link():
    schema, coverage, manifest, transcript = transcript_fixture()
    transcript = append(append(transcript, schema, coverage, manifest, 1), schema, coverage, manifest, 2)
    tampered_first = replace(transcript.entries[0], outer_statuses={"focal": "excluded"})
    tampered = AdmissionTranscript(header=transcript.header, entries=(tampered_first, transcript.entries[1]))

    with pytest.raises(ValueError, match="hash link is broken"):
        verify_admission_transcript(tampered)


def test_suffix_tampering_and_rollback_need_an_external_expected_head():
    schema, coverage, manifest, transcript = transcript_fixture()
    transcript = append(append(transcript, schema, coverage, manifest, 1), schema, coverage, manifest, 2)
    known_head = transcript.head_digest

    tampered_last = replace(transcript.entries[-1], admission_evidence_reference="proof://substituted")
    tampered = AdmissionTranscript(header=transcript.header, entries=(transcript.entries[0], tampered_last))
    verify_admission_transcript(tampered)
    with pytest.raises(ValueError, match="expected_head_digest"):
        verify_admission_transcript(tampered, expected_head_digest=known_head)

    rolled_back = AdmissionTranscript(header=transcript.header, entries=transcript.entries[:1])
    verify_admission_transcript(rolled_back)
    with pytest.raises(ValueError, match="expected_head_digest"):
        verify_admission_transcript(rolled_back, expected_head_digest=known_head)


def test_reordering_and_nonincreasing_look_append_are_rejected():
    schema, coverage, manifest, transcript = transcript_fixture()
    one = append(transcript, schema, coverage, manifest, 1)
    two = append(one, schema, coverage, manifest, 2)
    reordered = AdmissionTranscript(header=two.header, entries=(two.entries[1], two.entries[0]))
    with pytest.raises(ValueError, match="sequences"):
        verify_admission_transcript(reordered)
    with pytest.raises(ValueError, match="strictly later"):
        append(one, schema, coverage, manifest, 1)


def test_decision_anchor_remains_verifiable_after_later_append():
    schema, coverage, manifest, transcript = transcript_fixture()
    one = append(transcript, schema, coverage, manifest, 1)
    anchor = create_transcript_decision_anchor(one, look=1, motif="focal")
    two = append(one, schema, coverage, manifest, 2)

    verify_transcript_decision_anchor(two, anchor)
    altered = replace(anchor, outer_status="excluded")
    with pytest.raises(ValueError, match="does not match"):
        verify_transcript_decision_anchor(two, altered)


def test_entry_rejects_logically_inconsistent_extension_status():
    schema, coverage, manifest, transcript = transcript_fixture()
    first = append(transcript, schema, coverage, manifest, 1)
    with pytest.raises(ValueError, match="requires a decisive outer status"):
        AdmissionTranscriptEntry(
            sequence=2,
            look=2,
            previous_entry_digest=first.head_digest,
            canonical_manifest_digest=first.entries[0].canonical_manifest_digest,
            schema_context_digest=first.header.schema_context_digest,
            admission_evidence_reference="proof://inconsistent",
            inclusion_evidence_reference="proof://inconsistent-inclusion",
            admission_verifier="exact",
            outer_statuses={"focal": "unresolved"},
            extension_statuses={"focal": "extension-stable"},
        )
