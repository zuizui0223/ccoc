from fractions import Fraction

import pytest

from causal_model.all_look_coverage_contract import verify_all_look_coverage_contract
from causal_model.certificate_manifest import ManifestTarget
from causal_model.exact_finite_eprocess_coverage import (
    EXACT_FINITE_EPROCESS_METHOD,
    ExactCandidatePMF,
    ExactFiniteEProcessChannel,
    ExactFiniteEProcessCoverageVerifier,
    ExactFiniteEProcessEncoder,
    ExactFiniteObservationChannel,
    ExactFiniteObservationModel,
    build_exact_finite_eprocess_coverage_package,
    canonical_exact_finite_eprocess_encoder_bytes,
    canonical_exact_finite_observation_model_bytes,
    exact_finite_eprocess_coverage_certificate,
    exact_finite_eprocess_snapshots,
    exact_finite_false_exclusion_probability_up_to_horizon,
)


def one_cell_model():
    return ExactFiniteObservationModel(
        candidate_ids=("theta0", "theta1", "theta2"),
        channels=(
            ExactFiniteObservationChannel(
                cell_id="primary",
                alphabet=("A", "B"),
                candidate_pmfs=(
                    ExactCandidatePMF("theta0", ("3/4", "1/4")),
                    ExactCandidatePMF("theta1", ("1/4", "3/4")),
                    ExactCandidatePMF("theta2", ("1/2", "1/2")),
                ),
            ),
        ),
    )


def one_cell_encoder(model):
    return ExactFiniteEProcessEncoder(
        observation_model_digest=__import__("hashlib").sha256(
            canonical_exact_finite_observation_model_bytes(model)
        ).hexdigest(),
        channels=(
            ExactFiniteEProcessChannel(
                cell_id="primary",
                alternative_probabilities=("1/4", "3/4"),
                error_budget="1/20",
            ),
        ),
    )


def two_cell_model():
    return ExactFiniteObservationModel(
        candidate_ids=("theta0", "theta1", "theta2"),
        channels=(
            ExactFiniteObservationChannel(
                cell_id="first",
                alphabet=("A", "B"),
                candidate_pmfs=(
                    ExactCandidatePMF("theta0", ("3/4", "1/4")),
                    ExactCandidatePMF("theta1", ("1/4", "3/4")),
                    ExactCandidatePMF("theta2", ("1/2", "1/2")),
                ),
            ),
            ExactFiniteObservationChannel(
                cell_id="second",
                alphabet=("A", "B"),
                candidate_pmfs=(
                    ExactCandidatePMF("theta0", ("2/3", "1/3")),
                    ExactCandidatePMF("theta1", ("1/3", "2/3")),
                    ExactCandidatePMF("theta2", ("1/2", "1/2")),
                ),
            ),
        ),
    )


def two_cell_encoder(model):
    return ExactFiniteEProcessEncoder(
        observation_model_digest=__import__("hashlib").sha256(
            canonical_exact_finite_observation_model_bytes(model)
        ).hexdigest(),
        channels=(
            ExactFiniteEProcessChannel("first", ("1/4", "3/4"), "1/40"),
            ExactFiniteEProcessChannel("second", ("1/3", "2/3"), "1/40"),
        ),
    )


def target_for(model):
    return ManifestTarget.from_payloads(
        space=__import__("causal_model.symbolic_candidate_sets", fromlist=["SymbolicCandidateSpace"]).SymbolicCandidateSpace(
            "exact finite e-process candidate space",
            ("focal",),
        ),
        candidate_space_payload=b'{"finite_candidates":["theta0","theta1","theta2"]}',
        motif_definition_payloads={"focal": b'{"focal":true}'},
        required_cell_ids=model.cell_ids,
        certified_looks=None,
    )


def test_hypothesis_recovery_is_nested_and_excludes_evidence_conflicted_candidates():
    model = one_cell_model()
    encoder = one_cell_encoder(model)
    snapshots = exact_finite_eprocess_snapshots(
        model,
        encoder,
        {"primary": ("B", "B", "B", "B")},
    )

    # For theta0, B contributes q(B)/p0(B)=3.  At look 3 it crosses 20.
    assert snapshots[0].current_evalues_by_cell["primary"]["theta0"] == Fraction(3)
    assert snapshots[2].running_max_evalues_by_cell["primary"]["theta0"] == Fraction(27)
    assert "theta0" not in snapshots[2].retained_candidate_ids_by_cell["primary"]
    assert "theta0" not in snapshots[3].retained_candidate_ids_by_cell["primary"]

    # theta1 equals the predeclared alternative and remains compatible.
    assert snapshots[-1].current_evalues_by_cell["primary"]["theta1"] == Fraction(1)
    assert "theta1" in snapshots[-1].globally_retained_candidate_ids


def test_single_truth_principle_needs_cellwise_not_candidatewise_bonferroni_budget():
    model = two_cell_model()
    encoder = two_cell_encoder(model)
    certificate = exact_finite_eprocess_coverage_certificate(
        model,
        encoder,
        true_candidate_label="theta0",
    )

    # Three hypotheses exist, but only two required-cell e-processes spend alpha.
    assert certificate.lower_bound == pytest.approx(0.95)
    assert certificate.miscoverage_upper_bound == pytest.approx(0.05)
    assert certificate.required_cell_ids == ("first", "second")
    assert certificate.certified_looks is None
    assert certificate.method == EXACT_FINITE_EPROCESS_METHOD


def test_exact_finite_horizon_enumeration_is_below_ville_budget_for_true_hypothesis():
    model = one_cell_model()
    encoder = one_cell_encoder(model)
    probability = exact_finite_false_exclusion_probability_up_to_horizon(
        model,
        encoder,
        true_candidate_label="theta0",
        horizon=4,
    )

    assert probability <= Fraction(1, 20)
    assert probability == Fraction(1, 64)


def test_concrete_coverage_contract_verifier_rechecks_model_encoder_proof_and_contract_bindings():
    model = two_cell_model()
    encoder = two_cell_encoder(model)
    target = target_for(model)
    candidate_payload = b'{"finite_candidates":["theta0","theta1","theta2"]}'
    package = build_exact_finite_eprocess_coverage_package(
        contract_id="finite-eprocess-run",
        target=target,
        candidate_space_payload=candidate_payload,
        true_candidate_label="theta0",
        model=model,
        encoder=encoder,
    )

    receipt = verify_all_look_coverage_contract(
        package.coverage_contract,
        target=target,
        coverage_certificate=package.coverage_certificate,
        artifact_payloads=package.artifact_payloads,
        verifier=ExactFiniteEProcessCoverageVerifier(),
    )
    assert receipt.contract_digest == package.coverage_contract.contract_digest
    assert receipt.verifier_id == ExactFiniteEProcessCoverageVerifier.verifier_id

    tampered = dict(package.artifact_payloads)
    tampered["exact-finite-eprocess-encoder"] = canonical_exact_finite_eprocess_encoder_bytes(encoder) + b"\n"
    with pytest.raises(ValueError, match="artifact digest mismatch"):
        verify_all_look_coverage_contract(
            package.coverage_contract,
            target=target,
            coverage_certificate=package.coverage_certificate,
            artifact_payloads=tampered,
            verifier=ExactFiniteEProcessCoverageVerifier(),
        )


def test_backend_rejects_nonpositive_candidate_support_and_budget_overrun():
    with pytest.raises(ValueError, match="strictly positive"):
        ExactCandidatePMF("bad", ("1", "0"))

    model = one_cell_model()
    with pytest.raises(ValueError, match="must not exceed one"):
        ExactFiniteEProcessEncoder(
            observation_model_digest=__import__("hashlib").sha256(
                canonical_exact_finite_observation_model_bytes(model)
            ).hexdigest(),
            channels=(
                ExactFiniteEProcessChannel("primary", ("1/4", "3/4"), "3/4"),
                # Duplicate cell IDs reject first, so use a separate model error below.
            ),
        )

    # A model/encoder cell mismatch is also fail-closed.
    mismatched = ExactFiniteEProcessEncoder(
        observation_model_digest=__import__("hashlib").sha256(
            canonical_exact_finite_observation_model_bytes(model)
        ).hexdigest(),
        channels=(ExactFiniteEProcessChannel("other", ("1/4", "3/4"), "1/20"),),
    )
    with pytest.raises(ValueError, match="channels must equal"):
        exact_finite_eprocess_snapshots(model, mismatched, {"primary": ("A",)})
