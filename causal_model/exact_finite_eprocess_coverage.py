"""Exact finite-alphabet e-process confidence sequences for RACH.

This module supplies one concrete, proof-carrying implementation of the
otherwise external all-look coverage premise.  It is intentionally narrow and
fully auditable:

* a finite declared candidate set;
* a finite alphabet in each required cell;
* strictly positive stationary rational candidate PMFs; and
* a predeclared stationary rational alternative PMF per cell.

For candidate ``theta`` and cell ``r`` the process is

    E[r,theta,t] = product_{i=1}^t q[r](X[r,i]) / p[r,theta](X[r,i]).

Under theta, this is a nonnegative martingale because the one-step conditional
mean is exactly ``sum_x q[r](x) = 1``.  Ville's inequality yields

    P_theta(sup_t E[r,theta,t] >= 1/alpha_r) <= alpha_r.

A candidate is retained at cell r only while its *running maximum* stays below
that threshold.  This makes retained sets nested over time.  Across cells the
union bound gives simultaneous all-look coverage with error at most
``sum_r alpha_r``; no independence between cells is required for that union
bound once each individual e-process is valid.

The model, encoder, and theorem claim each have strict canonical JSON bytes.
``ExactFiniteEProcessCoverageVerifier`` parses those exact bytes and recomputes
the local martingale identity, the global error budget, and every contract
binding.  It is therefore a real backend for the proof-carrying coverage
contract rather than an opaque example.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from typing import Any, Mapping

from .all_look_coverage_contract import (
    AllLookCoverageContract,
    CoverageProofVerificationReceipt,
    coverage_contract_from_certificate,
)
from .anytime_symbolic_lifting import AnytimeSymbolicJointCoverageCertificate
from .certificate_manifest import ArtifactReference, ManifestTarget, sha256_digest


EXACT_FINITE_EPROCESS_METHOD = "exact-finite-alphabet-e-process/v1"
EXACT_FINITE_EPROCESS_VERIFIER_ID = "exact-finite-alphabet-e-process-verifier/v1"
EXACT_FINITE_OBSERVATION_MODEL_FORMAT = "rach-exact-finite-observation-model/v1"
EXACT_FINITE_EPROCESS_ENCODER_FORMAT = "rach-exact-finite-eprocess-encoder/v1"
EXACT_FINITE_EPROCESS_PROOF_FORMAT = "rach-exact-finite-eprocess-ville-proof/v1"
_HEX_DIGEST_LENGTH = 64


def _require_nonempty(value: str, name: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a non-empty string")


def _require_digest(value: str, name: str) -> None:
    if (
        not isinstance(value, str)
        or len(value) != _HEX_DIGEST_LENGTH
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ValueError(f"{name} must be a lowercase SHA-256 hexadecimal digest")


def _fraction(value: Fraction | int | str, name: str) -> Fraction:
    if isinstance(value, float):
        raise TypeError(f"{name} must not use binary floating point")
    try:
        return Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError) as error:
        raise ValueError(f"{name} is not an exact rational") from error


def _fraction_string(value: Fraction | int | str, name: str) -> str:
    return str(_fraction(value, name))


def _parse_fraction(value: Any, name: str) -> Fraction:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a non-empty canonical rational string")
    parsed = _fraction(value, name)
    if str(parsed) != value:
        raise ValueError(f"{name} is not a canonical rational string")
    return parsed


def _expect_mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a JSON object")
    return value


def _expect_exact_keys(value: Any, expected: set[str], name: str) -> Mapping[str, Any]:
    mapping = _expect_mapping(value, name)
    missing = expected - set(mapping)
    unexpected = set(mapping) - expected
    if missing:
        raise ValueError(f"{name} is missing fields: {sorted(missing)}")
    if unexpected:
        raise ValueError(f"{name} has unknown fields: {sorted(unexpected)}")
    return mapping


def _expect_string(value: Any, name: str, *, nonempty: bool = False) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a JSON string")
    if nonempty and not value:
        raise ValueError(f"{name} must be non-empty")
    return value


def _duplicate_key_rejecting_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def _reject_nonfinite_json_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant is not allowed: {value}")


def _decode_payload(payload: str | bytes) -> tuple[str, bytes]:
    if isinstance(payload, bytes):
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError("exact finite e-process payload must be valid UTF-8") from error
        raw = payload
    elif isinstance(payload, str):
        text = payload
        raw = payload.encode("utf-8")
    else:
        raise TypeError("exact finite e-process payload must be str or bytes")
    if text.startswith("\ufeff"):
        raise ValueError("exact finite e-process payload must not contain a UTF-8 BOM")
    return text, raw


def _strict_json(payload: str | bytes) -> tuple[Any, bytes]:
    text, raw = _decode_payload(payload)
    try:
        value = json.loads(
            text,
            object_pairs_hook=_duplicate_key_rejecting_object,
            parse_constant=_reject_nonfinite_json_constant,
        )
    except json.JSONDecodeError as error:
        raise ValueError("exact finite e-process payload is not valid JSON") from error
    return value, raw


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


@dataclass(frozen=True)
class ExactCandidatePMF:
    """One strictly positive exact PMF aligned to a declared finite alphabet."""

    candidate_id: str
    probabilities: tuple[Fraction | int | str, ...]

    def __post_init__(self) -> None:
        _require_nonempty(self.candidate_id, "candidate_id")
        normalized = tuple(_fraction(value, "candidate probability") for value in self.probabilities)
        if not normalized:
            raise ValueError("candidate probabilities must not be empty")
        if any(value <= 0 for value in normalized):
            raise ValueError("candidate probabilities must be strictly positive")
        if sum(normalized) != 1:
            raise ValueError("candidate probabilities must sum exactly to one")
        object.__setattr__(self, "probabilities", normalized)


@dataclass(frozen=True)
class ExactFiniteObservationChannel:
    """Stationary finite-alphabet candidate laws for one required RACH cell."""

    cell_id: str
    alphabet: tuple[str, ...]
    candidate_pmfs: tuple[ExactCandidatePMF, ...]

    def __post_init__(self) -> None:
        _require_nonempty(self.cell_id, "cell_id")
        if not self.alphabet or len(set(self.alphabet)) != len(self.alphabet):
            raise ValueError("alphabet must be non-empty and contain unique symbols")
        if any(not isinstance(symbol, str) or not symbol for symbol in self.alphabet):
            raise ValueError("alphabet symbols must be non-empty strings")
        if not self.candidate_pmfs:
            raise ValueError("candidate_pmfs must not be empty")
        ids = tuple(pmf.candidate_id for pmf in self.candidate_pmfs)
        if len(set(ids)) != len(ids):
            raise ValueError("candidate PMF IDs must be unique in a channel")
        if any(len(pmf.probabilities) != len(self.alphabet) for pmf in self.candidate_pmfs):
            raise ValueError("every candidate PMF must align to the channel alphabet")

    def pmf_for(self, candidate_id: str) -> ExactCandidatePMF:
        for pmf in self.candidate_pmfs:
            if pmf.candidate_id == candidate_id:
                return pmf
        raise ValueError(f"candidate {candidate_id!r} is absent from channel {self.cell_id!r}")


@dataclass(frozen=True)
class ExactFiniteObservationModel:
    """Shared finite hypothesis universe and its stationary laws across cells."""

    candidate_ids: tuple[str, ...]
    channels: tuple[ExactFiniteObservationChannel, ...]

    def __post_init__(self) -> None:
        if not self.candidate_ids or len(set(self.candidate_ids)) != len(self.candidate_ids):
            raise ValueError("candidate_ids must be non-empty and unique")
        if any(not isinstance(candidate, str) or not candidate for candidate in self.candidate_ids):
            raise ValueError("candidate IDs must be non-empty strings")
        if not self.channels:
            raise ValueError("observation model must contain at least one channel")
        cell_ids = tuple(channel.cell_id for channel in self.channels)
        if len(set(cell_ids)) != len(cell_ids):
            raise ValueError("observation channel cell IDs must be unique")
        for channel in self.channels:
            observed_ids = tuple(pmf.candidate_id for pmf in channel.candidate_pmfs)
            if observed_ids != self.candidate_ids:
                raise ValueError("every channel must use the model candidate IDs in identical order")

    @property
    def cell_ids(self) -> tuple[str, ...]:
        return tuple(channel.cell_id for channel in self.channels)

    def channel_for(self, cell_id: str) -> ExactFiniteObservationChannel:
        for channel in self.channels:
            if channel.cell_id == cell_id:
                return channel
        raise ValueError(f"unknown observation channel {cell_id!r}")


@dataclass(frozen=True)
class ExactFiniteEProcessChannel:
    """Predeclared alternative PMF and alpha budget for one observation cell."""

    cell_id: str
    alternative_probabilities: tuple[Fraction | int | str, ...]
    error_budget: Fraction | int | str

    def __post_init__(self) -> None:
        _require_nonempty(self.cell_id, "cell_id")
        alternative = tuple(_fraction(value, "alternative probability") for value in self.alternative_probabilities)
        if not alternative:
            raise ValueError("alternative probabilities must not be empty")
        if any(value < 0 for value in alternative):
            raise ValueError("alternative probabilities must be non-negative")
        if sum(alternative) != 1:
            raise ValueError("alternative probabilities must sum exactly to one")
        budget = _fraction(self.error_budget, "error_budget")
        if not 0 < budget < 1:
            raise ValueError("each e-process error budget must lie strictly between zero and one")
        object.__setattr__(self, "alternative_probabilities", alternative)
        object.__setattr__(self, "error_budget", budget)


@dataclass(frozen=True)
class ExactFiniteEProcessEncoder:
    """The candidate-retention rule paired with one observation-model digest."""

    observation_model_digest: str
    channels: tuple[ExactFiniteEProcessChannel, ...]

    def __post_init__(self) -> None:
        _require_digest(self.observation_model_digest, "observation_model_digest")
        if not self.channels:
            raise ValueError("e-process encoder must contain at least one channel")
        cell_ids = tuple(channel.cell_id for channel in self.channels)
        if len(set(cell_ids)) != len(cell_ids):
            raise ValueError("e-process encoder cell IDs must be unique")

    @property
    def cell_ids(self) -> tuple[str, ...]:
        return tuple(channel.cell_id for channel in self.channels)

    @property
    def total_error_budget(self) -> Fraction:
        return sum((channel.error_budget for channel in self.channels), Fraction(0))

    @property
    def lower_bound(self) -> Fraction:
        return Fraction(1) - self.total_error_budget

    def channel_for(self, cell_id: str) -> ExactFiniteEProcessChannel:
        for channel in self.channels:
            if channel.cell_id == cell_id:
                return channel
        raise ValueError(f"unknown e-process channel {cell_id!r}")


@dataclass(frozen=True)
class ExactFiniteEProcessProof:
    """Model-specific declaration of the exact Ville/union-bound theorem instance."""

    observation_model_digest: str
    encoder_digest: str
    lower_bound: Fraction | int | str
    theorem_id: str = EXACT_FINITE_EPROCESS_METHOD

    def __post_init__(self) -> None:
        _require_digest(self.observation_model_digest, "observation_model_digest")
        _require_digest(self.encoder_digest, "encoder_digest")
        lower = _fraction(self.lower_bound, "proof lower_bound")
        if not 0 <= lower <= 1:
            raise ValueError("proof lower_bound must lie in [0, 1]")
        if self.theorem_id != EXACT_FINITE_EPROCESS_METHOD:
            raise ValueError("unsupported finite e-process theorem identifier")
        object.__setattr__(self, "lower_bound", lower)


@dataclass(frozen=True)
class ExactFiniteEProcessSnapshot:
    """Exact current/running evidence and nested retained hypotheses at one look."""

    look: int
    current_evalues_by_cell: Mapping[str, Mapping[str, Fraction]]
    running_max_evalues_by_cell: Mapping[str, Mapping[str, Fraction]]
    retained_candidate_ids_by_cell: Mapping[str, tuple[str, ...]]

    @property
    def globally_retained_candidate_ids(self) -> tuple[str, ...]:
        cells = tuple(self.retained_candidate_ids_by_cell.values())
        if not cells:
            return ()
        retained = set(cells[0])
        for values in cells[1:]:
            retained &= set(values)
        return tuple(candidate for candidate in cells[0] if candidate in retained)

    @property
    def globally_excluded_candidate_ids(self) -> tuple[str, ...]:
        retained = set(self.globally_retained_candidate_ids)
        candidates = next(iter(self.current_evalues_by_cell.values()), {})
        return tuple(candidate for candidate in candidates if candidate not in retained)


@dataclass(frozen=True)
class ExactFiniteEProcessCoveragePackage:
    """Concrete coverage certificate/contract plus all exact artifact payloads."""

    observation_model: ExactFiniteObservationModel
    encoder: ExactFiniteEProcessEncoder
    proof: ExactFiniteEProcessProof
    coverage_certificate: AnytimeSymbolicJointCoverageCertificate
    coverage_contract: AllLookCoverageContract
    artifact_payloads: Mapping[str, bytes]


def _pmf_object(pmf: ExactCandidatePMF) -> dict[str, Any]:
    return {
        "candidate_id": pmf.candidate_id,
        "probabilities": [_fraction_string(value, "candidate probability") for value in pmf.probabilities],
    }


def _observation_model_object(model: ExactFiniteObservationModel) -> dict[str, Any]:
    return {
        "candidate_ids": list(model.candidate_ids),
        "channels": [
            {
                "alphabet": list(channel.alphabet),
                "candidate_pmfs": [_pmf_object(pmf) for pmf in channel.candidate_pmfs],
                "cell_id": channel.cell_id,
            }
            for channel in model.channels
        ],
        "format_version": EXACT_FINITE_OBSERVATION_MODEL_FORMAT,
    }


def canonical_exact_finite_observation_model_bytes(model: ExactFiniteObservationModel) -> bytes:
    if not isinstance(model, ExactFiniteObservationModel):
        raise TypeError("model must be an ExactFiniteObservationModel")
    return _canonical_bytes(_observation_model_object(model))


def exact_finite_observation_model_artifact(
    model: ExactFiniteObservationModel,
    *,
    artifact_id: str = "exact-finite-observation-model",
) -> ArtifactReference:
    return ArtifactReference.from_payload(
        artifact_id,
        canonical_exact_finite_observation_model_bytes(model),
        media_type="application/json",
    )


def _encoder_object(encoder: ExactFiniteEProcessEncoder) -> dict[str, Any]:
    return {
        "channels": [
            {
                "alternative_probabilities": [
                    _fraction_string(value, "alternative probability")
                    for value in channel.alternative_probabilities
                ],
                "cell_id": channel.cell_id,
                "error_budget": _fraction_string(channel.error_budget, "error_budget"),
            }
            for channel in encoder.channels
        ],
        "format_version": EXACT_FINITE_EPROCESS_ENCODER_FORMAT,
        "observation_model_digest": encoder.observation_model_digest,
    }


def canonical_exact_finite_eprocess_encoder_bytes(encoder: ExactFiniteEProcessEncoder) -> bytes:
    if not isinstance(encoder, ExactFiniteEProcessEncoder):
        raise TypeError("encoder must be an ExactFiniteEProcessEncoder")
    return _canonical_bytes(_encoder_object(encoder))


def exact_finite_eprocess_encoder_artifact(
    encoder: ExactFiniteEProcessEncoder,
    *,
    artifact_id: str = "exact-finite-eprocess-encoder",
) -> ArtifactReference:
    return ArtifactReference.from_payload(
        artifact_id,
        canonical_exact_finite_eprocess_encoder_bytes(encoder),
        media_type="application/json",
    )


def _proof_object(proof: ExactFiniteEProcessProof) -> dict[str, Any]:
    return {
        "encoder_digest": proof.encoder_digest,
        "format_version": EXACT_FINITE_EPROCESS_PROOF_FORMAT,
        "lower_bound": _fraction_string(proof.lower_bound, "proof lower_bound"),
        "observation_model_digest": proof.observation_model_digest,
        "theorem_id": proof.theorem_id,
    }


def canonical_exact_finite_eprocess_proof_bytes(proof: ExactFiniteEProcessProof) -> bytes:
    if not isinstance(proof, ExactFiniteEProcessProof):
        raise TypeError("proof must be an ExactFiniteEProcessProof")
    return _canonical_bytes(_proof_object(proof))


def exact_finite_eprocess_proof_artifact(
    proof: ExactFiniteEProcessProof,
    *,
    artifact_id: str = "exact-finite-eprocess-ville-proof",
) -> ArtifactReference:
    return ArtifactReference.from_payload(
        artifact_id,
        canonical_exact_finite_eprocess_proof_bytes(proof),
        media_type="application/json",
    )


def _parse_observation_model(payload: str | bytes) -> ExactFiniteObservationModel:
    value, raw = _strict_json(payload)
    root = _expect_exact_keys(value, {"candidate_ids", "channels", "format_version"}, "observation_model")
    if _expect_string(root["format_version"], "observation_model.format_version", nonempty=True) != EXACT_FINITE_OBSERVATION_MODEL_FORMAT:
        raise ValueError("unsupported exact finite observation-model format")
    if not isinstance(root["candidate_ids"], list):
        raise ValueError("observation_model.candidate_ids must be a JSON array")
    candidate_ids = tuple(
        _expect_string(item, f"observation_model.candidate_ids[{index}]", nonempty=True)
        for index, item in enumerate(root["candidate_ids"])
    )
    if not isinstance(root["channels"], list):
        raise ValueError("observation_model.channels must be a JSON array")
    channels: list[ExactFiniteObservationChannel] = []
    for index, raw_channel in enumerate(root["channels"]):
        name = f"observation_model.channels[{index}]"
        channel = _expect_exact_keys(raw_channel, {"alphabet", "candidate_pmfs", "cell_id"}, name)
        if not isinstance(channel["alphabet"], list):
            raise ValueError(f"{name}.alphabet must be a JSON array")
        alphabet = tuple(
            _expect_string(symbol, f"{name}.alphabet[{position}]", nonempty=True)
            for position, symbol in enumerate(channel["alphabet"])
        )
        if not isinstance(channel["candidate_pmfs"], list):
            raise ValueError(f"{name}.candidate_pmfs must be a JSON array")
        pmfs: list[ExactCandidatePMF] = []
        for pmf_index, raw_pmf in enumerate(channel["candidate_pmfs"]):
            pmf_name = f"{name}.candidate_pmfs[{pmf_index}]"
            pmf = _expect_exact_keys(raw_pmf, {"candidate_id", "probabilities"}, pmf_name)
            if not isinstance(pmf["probabilities"], list):
                raise ValueError(f"{pmf_name}.probabilities must be a JSON array")
            pmfs.append(
                ExactCandidatePMF(
                    candidate_id=_expect_string(pmf["candidate_id"], f"{pmf_name}.candidate_id", nonempty=True),
                    probabilities=tuple(
                        _parse_fraction(item, f"{pmf_name}.probabilities[{position}]")
                        for position, item in enumerate(pmf["probabilities"])
                    ),
                )
            )
        channels.append(
            ExactFiniteObservationChannel(
                cell_id=_expect_string(channel["cell_id"], f"{name}.cell_id", nonempty=True),
                alphabet=alphabet,
                candidate_pmfs=tuple(pmfs),
            )
        )
    model = ExactFiniteObservationModel(candidate_ids=candidate_ids, channels=tuple(channels))
    if raw != canonical_exact_finite_observation_model_bytes(model):
        raise ValueError("observation-model JSON is valid but not strict canonical JSON")
    return model


def _parse_encoder(payload: str | bytes) -> ExactFiniteEProcessEncoder:
    value, raw = _strict_json(payload)
    root = _expect_exact_keys(value, {"channels", "format_version", "observation_model_digest"}, "encoder")
    if _expect_string(root["format_version"], "encoder.format_version", nonempty=True) != EXACT_FINITE_EPROCESS_ENCODER_FORMAT:
        raise ValueError("unsupported exact finite e-process encoder format")
    if not isinstance(root["channels"], list):
        raise ValueError("encoder.channels must be a JSON array")
    channels: list[ExactFiniteEProcessChannel] = []
    for index, raw_channel in enumerate(root["channels"]):
        name = f"encoder.channels[{index}]"
        channel = _expect_exact_keys(raw_channel, {"alternative_probabilities", "cell_id", "error_budget"}, name)
        if not isinstance(channel["alternative_probabilities"], list):
            raise ValueError(f"{name}.alternative_probabilities must be a JSON array")
        channels.append(
            ExactFiniteEProcessChannel(
                cell_id=_expect_string(channel["cell_id"], f"{name}.cell_id", nonempty=True),
                alternative_probabilities=tuple(
                    _parse_fraction(item, f"{name}.alternative_probabilities[{position}]")
                    for position, item in enumerate(channel["alternative_probabilities"])
                ),
                error_budget=_parse_fraction(channel["error_budget"], f"{name}.error_budget"),
            )
        )
    encoder = ExactFiniteEProcessEncoder(
        observation_model_digest=_expect_string(root["observation_model_digest"], "encoder.observation_model_digest", nonempty=True),
        channels=tuple(channels),
    )
    if raw != canonical_exact_finite_eprocess_encoder_bytes(encoder):
        raise ValueError("e-process encoder JSON is valid but not strict canonical JSON")
    return encoder


def _parse_proof(payload: str | bytes) -> ExactFiniteEProcessProof:
    value, raw = _strict_json(payload)
    root = _expect_exact_keys(
        value,
        {"encoder_digest", "format_version", "lower_bound", "observation_model_digest", "theorem_id"},
        "proof",
    )
    if _expect_string(root["format_version"], "proof.format_version", nonempty=True) != EXACT_FINITE_EPROCESS_PROOF_FORMAT:
        raise ValueError("unsupported exact finite e-process proof format")
    proof = ExactFiniteEProcessProof(
        observation_model_digest=_expect_string(root["observation_model_digest"], "proof.observation_model_digest", nonempty=True),
        encoder_digest=_expect_string(root["encoder_digest"], "proof.encoder_digest", nonempty=True),
        lower_bound=_parse_fraction(root["lower_bound"], "proof.lower_bound"),
        theorem_id=_expect_string(root["theorem_id"], "proof.theorem_id", nonempty=True),
    )
    if raw != canonical_exact_finite_eprocess_proof_bytes(proof):
        raise ValueError("e-process proof JSON is valid but not strict canonical JSON")
    return proof


def validate_exact_finite_eprocess_backend(
    model: ExactFiniteObservationModel,
    encoder: ExactFiniteEProcessEncoder,
) -> None:
    """Verify exact local martingale conditions and global cellwise error budget."""

    model_digest = sha256(canonical_exact_finite_observation_model_bytes(model)).hexdigest()
    if encoder.observation_model_digest != model_digest:
        raise ValueError("encoder does not bind the exact observation-model digest")
    if encoder.cell_ids != model.cell_ids:
        raise ValueError("encoder channels must equal observation-model cells in identical order")
    if encoder.total_error_budget > 1:
        raise ValueError("sum of cellwise e-process error budgets must not exceed one")
    for observation_channel, e_channel in zip(model.channels, encoder.channels):
        if len(e_channel.alternative_probabilities) != len(observation_channel.alphabet):
            raise ValueError("alternative PMF must align to its observation alphabet")
        for candidate in model.candidate_ids:
            candidate_pmf = observation_channel.pmf_for(candidate).probabilities
            # Strictly positive candidate PMFs make all likelihood ratios finite.
            local_mean = sum(
                p * (q / p)
                for p, q in zip(candidate_pmf, e_channel.alternative_probabilities)
            )
            if local_mean != 1:
                raise ValueError("exact e-process one-step martingale identity failed")


def build_exact_finite_eprocess_proof(
    model: ExactFiniteObservationModel,
    encoder: ExactFiniteEProcessEncoder,
) -> ExactFiniteEProcessProof:
    validate_exact_finite_eprocess_backend(model, encoder)
    return ExactFiniteEProcessProof(
        observation_model_digest=sha256(canonical_exact_finite_observation_model_bytes(model)).hexdigest(),
        encoder_digest=sha256(canonical_exact_finite_eprocess_encoder_bytes(encoder)).hexdigest(),
        lower_bound=encoder.lower_bound,
    )


def exact_finite_eprocess_assumptions() -> tuple[str, ...]:
    """The precise statistical conditions under which the Ville theorem is invoked."""

    return (
        "The true candidate belongs to the declared finite candidate universe.",
        "For each required cell and each positive look, the observation has the declared stationary candidate PMF conditional on that cell's past.",
        "Alternative PMFs and cellwise error budgets are fixed before observing the stream.",
        "The e-process likelihood-ratio construction is evaluated at every claimed look.",
    )


def exact_finite_eprocess_coverage_certificate(
    model: ExactFiniteObservationModel,
    encoder: ExactFiniteEProcessEncoder,
    *,
    true_candidate_label: str,
) -> AnytimeSymbolicJointCoverageCertificate:
    """Return the genuine all-positive-integer coverage certificate for this backend."""

    validate_exact_finite_eprocess_backend(model, encoder)
    if true_candidate_label not in model.candidate_ids:
        raise ValueError("true_candidate_label must be one declared finite candidate")
    return AnytimeSymbolicJointCoverageCertificate(
        true_candidate_label=true_candidate_label,
        required_cell_ids=model.cell_ids,
        lower_bound=float(encoder.lower_bound),
        method=EXACT_FINITE_EPROCESS_METHOD,
        assumptions=exact_finite_eprocess_assumptions(),
        certified_looks=None,
    )


def _evalue_for_prefix(
    observation_channel: ExactFiniteObservationChannel,
    e_channel: ExactFiniteEProcessChannel,
    candidate_id: str,
    observations: tuple[str, ...],
) -> Fraction:
    index_by_symbol = {symbol: index for index, symbol in enumerate(observation_channel.alphabet)}
    pmf = observation_channel.pmf_for(candidate_id).probabilities
    value = Fraction(1)
    for look, symbol in enumerate(observations, start=1):
        try:
            index = index_by_symbol[symbol]
        except KeyError as error:
            raise ValueError(
                f"unknown outcome {symbol!r} at cell {observation_channel.cell_id!r}, look {look}"
            ) from error
        value *= e_channel.alternative_probabilities[index] / pmf[index]
    return value


def exact_finite_eprocess_snapshots(
    model: ExactFiniteObservationModel,
    encoder: ExactFiniteEProcessEncoder,
    observations_by_cell: Mapping[str, tuple[str, ...]],
) -> tuple[ExactFiniteEProcessSnapshot, ...]:
    """Compute nested candidate confidence sets at every common positive look."""

    validate_exact_finite_eprocess_backend(model, encoder)
    if tuple(observations_by_cell) != model.cell_ids:
        raise ValueError("observations_by_cell keys must equal model cells in declared order")
    lengths = {len(observations_by_cell[cell_id]) for cell_id in model.cell_ids}
    if len(lengths) != 1:
        raise ValueError("all required cells need the same number of sequential looks")
    horizon = next(iter(lengths))
    if horizon < 1:
        raise ValueError("at least one sequential look is required")

    running = {
        cell_id: {candidate: Fraction(1) for candidate in model.candidate_ids}
        for cell_id in model.cell_ids
    }
    snapshots: list[ExactFiniteEProcessSnapshot] = []
    for look in range(1, horizon + 1):
        current_by_cell: dict[str, dict[str, Fraction]] = {}
        retained_by_cell: dict[str, tuple[str, ...]] = {}
        for observation_channel, e_channel in zip(model.channels, encoder.channels):
            cell_id = observation_channel.cell_id
            prefix = observations_by_cell[cell_id][:look]
            current = {
                candidate: _evalue_for_prefix(observation_channel, e_channel, candidate, prefix)
                for candidate in model.candidate_ids
            }
            current_by_cell[cell_id] = current
            for candidate, value in current.items():
                running[cell_id][candidate] = max(running[cell_id][candidate], value)
            threshold = Fraction(1, 1) / e_channel.error_budget
            retained_by_cell[cell_id] = tuple(
                candidate
                for candidate in model.candidate_ids
                if running[cell_id][candidate] < threshold
            )
        snapshots.append(
            ExactFiniteEProcessSnapshot(
                look=look,
                current_evalues_by_cell={cell_id: dict(values) for cell_id, values in current_by_cell.items()},
                running_max_evalues_by_cell={cell_id: dict(values) for cell_id, values in running.items()},
                retained_candidate_ids_by_cell=retained_by_cell,
            )
        )
    return tuple(snapshots)


def exact_finite_false_exclusion_probability_up_to_horizon(
    model: ExactFiniteObservationModel,
    encoder: ExactFiniteEProcessEncoder,
    *,
    true_candidate_label: str,
    horizon: int,
) -> Fraction:
    """Exact finite-horizon audit for one cell; the theorem itself remains all-look."""

    validate_exact_finite_eprocess_backend(model, encoder)
    if len(model.channels) != 1:
        raise ValueError("finite-horizon exact enumeration currently supports exactly one cell")
    if true_candidate_label not in model.candidate_ids:
        raise ValueError("true_candidate_label must be declared")
    if not isinstance(horizon, int) or horizon < 1:
        raise ValueError("horizon must be a positive integer")
    channel = model.channels[0]
    e_channel = encoder.channels[0]
    true_pmf = channel.pmf_for(true_candidate_label).probabilities
    total = Fraction(0)
    for sequence in product(channel.alphabet, repeat=horizon):
        probability = Fraction(1)
        for symbol in sequence:
            probability *= true_pmf[channel.alphabet.index(symbol)]
        snapshots = exact_finite_eprocess_snapshots(model, encoder, {channel.cell_id: sequence})
        if any(true_candidate_label not in snapshot.retained_candidate_ids_by_cell[channel.cell_id] for snapshot in snapshots):
            total += probability
    return total


def build_exact_finite_eprocess_coverage_package(
    *,
    contract_id: str,
    target: ManifestTarget,
    candidate_space_payload: bytes,
    true_candidate_label: str,
    model: ExactFiniteObservationModel,
    encoder: ExactFiniteEProcessEncoder,
) -> ExactFiniteEProcessCoveragePackage:
    """Create a concrete all-look certificate, contract, exact proof, and payload registry."""

    if sha256_digest(candidate_space_payload) != target.candidate_space_artifact.sha256:
        raise ValueError("candidate_space_payload does not match the manifest target artifact")
    proof = build_exact_finite_eprocess_proof(model, encoder)
    observation_artifact = exact_finite_observation_model_artifact(model)
    encoder_artifact = exact_finite_eprocess_encoder_artifact(encoder)
    proof_artifact = exact_finite_eprocess_proof_artifact(proof)
    certificate = exact_finite_eprocess_coverage_certificate(
        model,
        encoder,
        true_candidate_label=true_candidate_label,
    )
    contract = coverage_contract_from_certificate(
        contract_id=contract_id,
        target=target,
        coverage_certificate=certificate,
        observation_channel_artifact=observation_artifact,
        retained_set_encoder_artifact=encoder_artifact,
        coverage_proof_artifact=proof_artifact,
        coverage_verifier_id=EXACT_FINITE_EPROCESS_VERIFIER_ID,
    )
    return ExactFiniteEProcessCoveragePackage(
        observation_model=model,
        encoder=encoder,
        proof=proof,
        coverage_certificate=certificate,
        coverage_contract=contract,
        artifact_payloads={
            target.candidate_space_artifact.artifact_id: candidate_space_payload,
            observation_artifact.artifact_id: canonical_exact_finite_observation_model_bytes(model),
            encoder_artifact.artifact_id: canonical_exact_finite_eprocess_encoder_bytes(encoder),
            proof_artifact.artifact_id: canonical_exact_finite_eprocess_proof_bytes(proof),
        },
    )


class ExactFiniteEProcessCoverageVerifier:
    """Method-specific proof verifier for the stationary rational e-process backend."""

    verifier_id = EXACT_FINITE_EPROCESS_VERIFIER_ID

    def verify_all_look_coverage(
        self,
        contract: AllLookCoverageContract,
        artifact_payloads: Mapping[str, str | bytes],
    ) -> CoverageProofVerificationReceipt:
        observation_payload = artifact_payloads[contract.observation_channel_artifact.artifact_id]
        encoder_payload = artifact_payloads[contract.retained_set_encoder_artifact.artifact_id]
        proof_payload = artifact_payloads[contract.coverage_proof_artifact.artifact_id]
        model = _parse_observation_model(observation_payload)
        encoder = _parse_encoder(encoder_payload)
        proof = _parse_proof(proof_payload)
        validate_exact_finite_eprocess_backend(model, encoder)

        model_digest = sha256(canonical_exact_finite_observation_model_bytes(model)).hexdigest()
        encoder_digest = sha256(canonical_exact_finite_eprocess_encoder_bytes(encoder)).hexdigest()
        expected_proof = build_exact_finite_eprocess_proof(model, encoder)
        if proof != expected_proof:
            raise ValueError("finite e-process proof does not match the exact model and encoder")
        if contract.method != EXACT_FINITE_EPROCESS_METHOD:
            raise ValueError("coverage contract method does not name the exact finite e-process backend")
        if contract.coverage_verifier_id != self.verifier_id:
            raise ValueError("coverage contract verifier ID does not name the exact finite e-process verifier")
        if contract.true_candidate_label not in model.candidate_ids:
            raise ValueError("coverage contract true candidate label is absent from the finite hypothesis universe")
        if contract.required_cell_ids != model.cell_ids:
            raise ValueError("coverage contract required cells do not match the finite e-process model")
        if contract.certified_looks is not None:
            raise ValueError("exact finite e-process backend is all-positive-integer only")
        if contract.lower_bound != float(encoder.lower_bound):
            raise ValueError("coverage contract lower bound does not match exact e-process error budgets")
        if contract.assumptions != exact_finite_eprocess_assumptions():
            raise ValueError("coverage contract assumptions do not match exact finite e-process theorem assumptions")
        if proof.observation_model_digest != model_digest or proof.encoder_digest != encoder_digest:
            raise ValueError("finite e-process proof digest links are inconsistent")
        return CoverageProofVerificationReceipt(
            contract_digest=contract.contract_digest,
            verifier_id=self.verifier_id,
            coverage_proof_artifact_sha256=contract.coverage_proof_artifact.sha256,
            retained_set_encoder_artifact_sha256=contract.retained_set_encoder_artifact.sha256,
            observation_channel_artifact_sha256=contract.observation_channel_artifact.sha256,
        )
