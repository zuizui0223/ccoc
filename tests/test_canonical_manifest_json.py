import json

import pytest

from causal_model.anytime_symbolic_lifting import (
    AnytimeSolverSemanticValidityCertificate,
    AnytimeSymbolicJointCoverageCertificate,
)
from causal_model.canonical_manifest_json import (
    CANONICAL_MANIFEST_JSON_FORMAT,
    canonical_manifest_bytes,
    canonical_manifest_digest,
    canonical_manifest_json,
    parse_canonical_manifest,
    serialize_canonical_manifest,
    verify_canonical_manifest,
)
from causal_model.certificate_manifest import (
    ExternalAssertionBinding,
    ManifestTarget,
    QueryRole,
    SolverQueryProofBinding,
    build_anytime_symbolic_manifest,
)
from causal_model.symbolic_candidate_sets import FeasibilityStatus, SymbolicCandidateSpace


SPACE = SymbolicCandidateSpace("polyhedral candidate space", ("focal",))


def manifest_with_proof_order(reverse=False):
    payloads = {
        "candidate-space": b'{"variables":["x"]}',
        "motif:focal": b'{"predicate":"x>=0"}',
        "coverage": b'{"kind":"coverage"}',
        "solver": b'{"kind":"solver"}',
        "active-query": b'{"query":"C and focal"}',
        "active-proof": b'{"witness":["1/5"]}',
        "inactive-query": b'{"query":"C and not focal"}',
        "inactive-proof": b'{"farkas":["1","1"]}',
    }
    coverage = AnytimeSymbolicJointCoverageCertificate(
        true_candidate_label="theta_star",
        required_cell_ids=("primary",),
        lower_bound=0.95,
        method="external confidence sequence",
        assumptions=("all looks covered",),
    )
    solver = AnytimeSolverSemanticValidityCertificate(
        required_cell_ids=("primary",),
        motifs=("focal",),
        lower_bound=1.0,
        method="exact proof verifier",
        assumptions=("exact parser trusted",),
    )
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
    solver_binding = ExternalAssertionBinding.from_payload(
        kind="time-uniform-solver-semantic-validity",
        lower_bound=solver.lower_bound,
        method=solver.method,
        assumptions=solver.assumptions,
        evidence_artifact_id="solver",
        evidence_payload=payloads["solver"],
    )
    active = SolverQueryProofBinding.from_payloads(
        look=2,
        cell_id="primary",
        motif="focal",
        role=QueryRole.ACTIVE,
        status=FeasibilityStatus.SAT,
        query_encoding_payload=payloads["active-query"],
        proof_payload=payloads["active-proof"],
        verifier_id="exact-rational-linear-proof-verifier",
        query_artifact_id="active-query",
        proof_artifact_id="active-proof",
    )
    inactive = SolverQueryProofBinding.from_payloads(
        look=1,
        cell_id="primary",
        motif="focal",
        role=QueryRole.INACTIVE,
        status=FeasibilityStatus.UNSAT,
        query_encoding_payload=payloads["inactive-query"],
        proof_payload=payloads["inactive-proof"],
        verifier_id="exact-rational-linear-proof-verifier",
        query_artifact_id="inactive-query",
        proof_artifact_id="inactive-proof",
    )
    proofs = (active, inactive) if reverse else (inactive, active)
    return build_anytime_symbolic_manifest(
        target=target,
        coverage_certificate=coverage,
        solver_certificate=solver,
        coverage_assertion=coverage_binding,
        solver_assertion=solver_binding,
        solver_query_proofs=proofs,
    )


def canonical_object(manifest):
    return json.loads(canonical_manifest_json(manifest))


def canonical_dump(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def test_canonical_round_trip_preserves_manifest_and_digest():
    manifest = manifest_with_proof_order()
    document = serialize_canonical_manifest(manifest)
    parsed = parse_canonical_manifest(document.canonical_bytes)

    assert CANONICAL_MANIFEST_JSON_FORMAT == "rach-canonical-manifest-json/v1"
    assert parsed.manifest == manifest
    assert parsed.canonical_bytes == document.canonical_bytes
    assert parsed.canonical_digest == document.canonical_digest
    assert parsed.canonical_digest == canonical_manifest_digest(manifest)
    assert document.canonical_bytes == canonical_manifest_bytes(manifest)


def test_proof_binding_input_order_does_not_change_canonical_bytes_or_digest():
    ordered = manifest_with_proof_order()
    reversed_bindings = manifest_with_proof_order(reverse=True)

    assert canonical_manifest_bytes(ordered) == canonical_manifest_bytes(reversed_bindings)
    assert canonical_manifest_digest(ordered) == canonical_manifest_digest(reversed_bindings)
    parsed = parse_canonical_manifest(canonical_manifest_bytes(reversed_bindings))
    assert tuple(binding.look for binding in parsed.manifest.solver_query_proofs) == (1, 2)


def test_parser_rejects_valid_but_noncanonical_whitespace_and_key_order():
    manifest = manifest_with_proof_order()
    raw = canonical_manifest_bytes(manifest)

    with pytest.raises(ValueError, match="not strict canonical"):
        parse_canonical_manifest(raw + b"\n")

    reordered = {
        "target": canonical_object(manifest)["target"],
        "solver_query_proofs": canonical_object(manifest)["solver_query_proofs"],
        "solver_assertion": canonical_object(manifest)["solver_assertion"],
        "coverage_assertion": canonical_object(manifest)["coverage_assertion"],
        "format_version": canonical_object(manifest)["format_version"],
    }
    with pytest.raises(ValueError, match="not strict canonical"):
        parse_canonical_manifest(canonical_dump(reordered))


def test_parser_rejects_duplicate_unknown_and_missing_fields():
    manifest = manifest_with_proof_order()
    raw = canonical_manifest_json(manifest)
    duplicate_root = raw.replace(
        '"format_version":"rach-certificate-manifest/v1"',
        '"format_version":"rach-certificate-manifest/v1","format_version":"rach-certificate-manifest/v1"',
    )
    with pytest.raises(ValueError, match="duplicate JSON object key"):
        parse_canonical_manifest(duplicate_root)

    unknown = canonical_object(manifest)
    unknown["extra"] = "not allowed"
    with pytest.raises(ValueError, match="unknown"):
        parse_canonical_manifest(canonical_dump(unknown))

    missing = canonical_object(manifest)
    del missing["target"]
    with pytest.raises(ValueError, match="missing"):
        parse_canonical_manifest(canonical_dump(missing))


def test_parser_rejects_ambiguous_probability_encodings():
    manifest = manifest_with_proof_order()

    numeric_probability = canonical_object(manifest)
    numeric_probability["coverage_assertion"]["lower_bound"] = 0.95
    with pytest.raises(ValueError, match="must be a JSON object"):
        parse_canonical_manifest(canonical_dump(numeric_probability))

    noncanonical_hex = canonical_object(manifest)
    noncanonical_hex["coverage_assertion"]["lower_bound"] = {
        "__float_hex__": "0x1.e6666666666660p-1"
    }
    with pytest.raises(ValueError, match="canonical finite hexadecimal"):
        parse_canonical_manifest(canonical_dump(noncanonical_hex))


def test_parser_rejects_invalid_utf8_and_digest_mismatch():
    manifest = manifest_with_proof_order()
    raw = canonical_manifest_bytes(manifest)

    with pytest.raises(ValueError, match="valid UTF-8"):
        parse_canonical_manifest(b"\xff")
    with pytest.raises(ValueError, match="does not match expected_digest"):
        verify_canonical_manifest(raw, expected_digest="0" * 64)


def test_expected_digest_and_semantic_content_tampering_are_detected():
    manifest = manifest_with_proof_order()
    document = verify_canonical_manifest(
        canonical_manifest_bytes(manifest),
        expected_digest=canonical_manifest_digest(manifest),
    )
    assert document.manifest.target.candidate_space_description == SPACE.space_description

    tampered = canonical_object(manifest)
    tampered["target"]["candidate_space_artifact"]["sha256"] = "1" * 64
    with pytest.raises(ValueError, match="not strict canonical"):
        parse_canonical_manifest(canonical_dump(tampered))
