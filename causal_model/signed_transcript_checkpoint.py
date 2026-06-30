"""Ed25519-signed checkpoints for append-only RACH admission transcripts.

A hash chain detects transcript mutation only relative to a known head digest.
This module makes that head externally attestable. An external signer signs a
strict, domain-separated checkpoint payload; any verifier holding the trusted
Ed25519 public key can then reject a transcript that does not contain the signed
prefix.

The module intentionally contains no private-key handling or signing API.
Private keys stay in an external signer, hardware token, CI secret, or other
operational key-management system. The bundled Ed25519 implementation is
verification-only and uses only public inputs; it is included to keep checking
of an attestation dependency-free and reproducible.

A signed checkpoint establishes signer-authenticated integrity of one transcript
prefix. It does not establish wall-clock time, universal transcript completeness,
or that a signer never signs conflicting checkpoints. The latter is detectable
when two conflicting valid attestations are compared.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256, sha512
from typing import Iterable

from .admission_transcript import (
    AdmissionTranscript,
    AdmissionTranscriptVerificationReport,
    verify_admission_transcript,
)
from .certificate_manifest import canonical_json


SIGNED_TRANSCRIPT_CHECKPOINT_FORMAT = "rach-signed-transcript-checkpoint/v1"
TRANSCRIPT_HEAD_CHECKPOINT_FORMAT = "rach-transcript-head-checkpoint/v1"
ED25519_ALGORITHM = "ed25519"

# RFC 8032 Edwards25519 parameters. This code verifies public signatures only.
_P = 2**255 - 19
_Q = 2**252 + 27742317777372353535851937790883648493
_D = (-121665 * pow(121666, -1, _P)) % _P
_I = pow(2, (_P - 1) // 4, _P)
_BASE_POINT = (
    15112221349535400772501151409588531511454012693041857206046113283949847762202,
    46316835694926478169428394003475163141307993866256225615783033603165251855960,
    1,
    15112221349535400772501151409588531511454012693041857206046113283949847762202
    * 46316835694926478169428394003475163141307993866256225615783033603165251855960
    % _P,
)
_IDENTITY = (0, 1, 1, 0)
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


def _decode_lower_hex(value: str, *, byte_length: int, name: str) -> bytes:
    if not isinstance(value, str) or len(value) != byte_length * 2:
        raise ValueError(f"{name} must be {byte_length} bytes encoded as lowercase hexadecimal")
    if any(character not in "0123456789abcdef" for character in value):
        raise ValueError(f"{name} must be {byte_length} bytes encoded as lowercase hexadecimal")
    return bytes.fromhex(value)


def _point_add(left: tuple[int, int, int, int], right: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """Add extended Edwards coordinates using complete addition formulas."""

    x1, y1, z1, t1 = left
    x2, y2, z2, t2 = right
    a = ((y1 - x1) * (y2 - x2)) % _P
    b = ((y1 + x1) * (y2 + x2)) % _P
    c = (2 * _D * t1 * t2) % _P
    d = (2 * z1 * z2) % _P
    e = (b - a) % _P
    f = (d - c) % _P
    g = (d + c) % _P
    h = (b + a) % _P
    return ((e * f) % _P, (g * h) % _P, (f * g) % _P, (e * h) % _P)


def _point_double(point: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """Double extended Edwards coordinates without an affine inversion."""

    x, y, z, _ = point
    a = (x * x) % _P
    b = (y * y) % _P
    c = (2 * z * z) % _P
    d = (-a) % _P
    e = ((x + y) * (x + y) - a - b) % _P
    g = (d + b) % _P
    f = (g - c) % _P
    h = (d - b) % _P
    return ((e * f) % _P, (g * h) % _P, (f * g) % _P, (e * h) % _P)


def _scalar_multiply(scalar: int, point: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    result = _IDENTITY
    addend = point
    while scalar:
        if scalar & 1:
            result = _point_add(result, addend)
        addend = _point_double(addend)
        scalar >>= 1
    return result


def _points_equal(left: tuple[int, int, int, int], right: tuple[int, int, int, int]) -> bool:
    return (
        (left[0] * right[2] - right[0] * left[2]) % _P == 0
        and (left[1] * right[2] - right[1] * left[2]) % _P == 0
    )


def _is_identity(point: tuple[int, int, int, int]) -> bool:
    return point[0] % _P == 0 and (point[1] - point[2]) % _P == 0


def _decode_point(encoded: bytes) -> tuple[int, int, int, int]:
    """Decode one canonical compressed Edwards25519 point or raise ValueError."""

    if len(encoded) != 32:
        raise ValueError("an Ed25519 encoded point must contain 32 bytes")
    sign = encoded[31] >> 7
    y = int.from_bytes(encoded, "little") & ((1 << 255) - 1)
    if y >= _P:
        raise ValueError("Ed25519 point uses a non-canonical field encoding")
    denominator = (_D * y * y + 1) % _P
    if denominator == 0:
        raise ValueError("Ed25519 point has invalid square-root denominator")
    x_squared = ((y * y - 1) * pow(denominator, _P - 2, _P)) % _P
    x = pow(x_squared, (_P + 3) // 8, _P)
    if (x * x - x_squared) % _P:
        x = (x * _I) % _P
    if (x * x - x_squared) % _P:
        raise ValueError("Ed25519 point is not on the curve")
    if x == 0 and sign:
        raise ValueError("Ed25519 point uses non-canonical negative zero")
    if (x & 1) != sign:
        x = _P - x
    return (x, y, 1, (x * y) % _P)


def verify_ed25519_signature(
    *,
    public_key: bytes,
    message: bytes,
    signature: bytes,
) -> bool:
    """Strictly verify one RFC 8032 Ed25519 detached signature.

    Public keys and signature point encodings must be canonical. The verifier
    rejects non-prime-subgroup public keys and ``R`` values, as well as scalars
    ``S >= q``. It operates only on public data and is not a signing routine.
    """

    if len(public_key) != 32 or len(signature) != 64:
        return False
    encoded_r = signature[:32]
    scalar_s = int.from_bytes(signature[32:], "little")
    if scalar_s >= _Q:
        return False
    try:
        point_a = _decode_point(public_key)
        point_r = _decode_point(encoded_r)
    except ValueError:
        return False
    # Exact prime-subgroup membership removes small-order acceptance ambiguity.
    if not _is_identity(_scalar_multiply(_Q, point_a)):
        return False
    if not _is_identity(_scalar_multiply(_Q, point_r)):
        return False
    scalar_h = int.from_bytes(sha512(encoded_r + public_key + message).digest(), "little") % _Q
    left = _scalar_multiply(scalar_s, _BASE_POINT)
    right = _point_add(point_r, _scalar_multiply(scalar_h, point_a))
    return _points_equal(left, right)


@dataclass(frozen=True)
class Ed25519VerifierKey:
    """A trusted public verification key, identified outside the transcript itself."""

    key_id: str
    public_key_hex: str

    def __post_init__(self) -> None:
        _require_nonempty(self.key_id, "key_id")
        _decode_lower_hex(self.public_key_hex, byte_length=32, name="public_key_hex")

    @property
    def public_key_bytes(self) -> bytes:
        return _decode_lower_hex(self.public_key_hex, byte_length=32, name="public_key_hex")

    @property
    def fingerprint(self) -> str:
        return sha256(self.public_key_bytes).hexdigest()


@dataclass(frozen=True)
class TranscriptHeadCheckpoint:
    """The exact transcript prefix that one external signer attests."""

    transcript_id: str
    genesis_digest: str
    head_digest: str
    entry_count: int
    last_look: int | None
    schema_context_digest: str
    canonical_manifest_digest: str | None
    checkpoint_sequence: int
    format_version: str = TRANSCRIPT_HEAD_CHECKPOINT_FORMAT

    def __post_init__(self) -> None:
        _require_nonempty(self.transcript_id, "transcript_id")
        if self.format_version != TRANSCRIPT_HEAD_CHECKPOINT_FORMAT:
            raise ValueError(f"unsupported transcript checkpoint format: {self.format_version!r}")
        for value, name in (
            (self.genesis_digest, "genesis_digest"),
            (self.head_digest, "head_digest"),
            (self.schema_context_digest, "schema_context_digest"),
        ):
            _require_digest(value, name)
        if self.canonical_manifest_digest is not None:
            _require_digest(self.canonical_manifest_digest, "canonical_manifest_digest")
        if not isinstance(self.entry_count, int) or self.entry_count < 0:
            raise ValueError("entry_count must be a non-negative integer")
        if not isinstance(self.checkpoint_sequence, int) or self.checkpoint_sequence < 1:
            raise ValueError("checkpoint_sequence must be a positive integer")
        if self.entry_count == 0:
            if self.last_look is not None or self.canonical_manifest_digest is not None:
                raise ValueError("an empty transcript checkpoint has no last look or manifest digest")
        else:
            if not isinstance(self.last_look, int) or self.last_look < 1:
                raise ValueError("a non-empty transcript checkpoint needs a positive last_look")
            if self.canonical_manifest_digest is None:
                raise ValueError("a non-empty transcript checkpoint needs a canonical_manifest_digest")


@dataclass(frozen=True)
class SignedTranscriptCheckpoint:
    """An external Ed25519 attestation over one exact transcript prefix."""

    checkpoint: TranscriptHeadCheckpoint
    signer_key_id: str
    signer_public_key_fingerprint: str
    signature_hex: str
    algorithm: str = ED25519_ALGORITHM
    format_version: str = SIGNED_TRANSCRIPT_CHECKPOINT_FORMAT

    def __post_init__(self) -> None:
        _require_nonempty(self.signer_key_id, "signer_key_id")
        _require_digest(self.signer_public_key_fingerprint, "signer_public_key_fingerprint")
        _decode_lower_hex(self.signature_hex, byte_length=64, name="signature_hex")
        if self.algorithm != ED25519_ALGORITHM:
            raise ValueError(f"unsupported checkpoint signature algorithm: {self.algorithm!r}")
        if self.format_version != SIGNED_TRANSCRIPT_CHECKPOINT_FORMAT:
            raise ValueError(f"unsupported signed checkpoint format: {self.format_version!r}")

    @property
    def signature_bytes(self) -> bytes:
        return _decode_lower_hex(self.signature_hex, byte_length=64, name="signature_hex")


@dataclass(frozen=True)
class SignedCheckpointVerificationReport:
    """Successful signature and transcript-prefix verification result."""

    transcript_id: str
    checkpoint_sequence: int
    signed_entry_count: int
    signed_last_look: int | None
    signed_head_digest: str
    signer_key_id: str
    signer_public_key_fingerprint: str


@dataclass(frozen=True)
class SignedCheckpointEquivocationEvidence:
    """Two valid signatures by one key for conflicting checkpoint payloads."""

    signer_key_id: str
    transcript_id: str
    genesis_digest: str
    checkpoint_sequence: int
    first: SignedTranscriptCheckpoint
    second: SignedTranscriptCheckpoint

    def __post_init__(self) -> None:
        if self.first.signer_key_id != self.signer_key_id or self.second.signer_key_id != self.signer_key_id:
            raise ValueError("equivocation evidence signer IDs must match")
        if self.first.checkpoint.transcript_id != self.transcript_id or self.second.checkpoint.transcript_id != self.transcript_id:
            raise ValueError("equivocation evidence transcript IDs must match")
        if self.first.checkpoint.genesis_digest != self.genesis_digest or self.second.checkpoint.genesis_digest != self.genesis_digest:
            raise ValueError("equivocation evidence genesis digests must match")
        if (
            self.first.checkpoint.checkpoint_sequence != self.checkpoint_sequence
            or self.second.checkpoint.checkpoint_sequence != self.checkpoint_sequence
        ):
            raise ValueError("equivocation evidence checkpoint sequences must match")
        if self.first.checkpoint == self.second.checkpoint:
            raise ValueError("equivocation evidence requires conflicting checkpoint payloads")


def _checkpoint_object(checkpoint: TranscriptHeadCheckpoint) -> dict[str, object]:
    return {
        "format_version": checkpoint.format_version,
        "transcript_id": checkpoint.transcript_id,
        "genesis_digest": checkpoint.genesis_digest,
        "head_digest": checkpoint.head_digest,
        "entry_count": checkpoint.entry_count,
        "last_look": checkpoint.last_look,
        "schema_context_digest": checkpoint.schema_context_digest,
        "canonical_manifest_digest": checkpoint.canonical_manifest_digest,
        "checkpoint_sequence": checkpoint.checkpoint_sequence,
    }


def checkpoint_signing_bytes(
    checkpoint: TranscriptHeadCheckpoint,
    *,
    verifier_key: Ed25519VerifierKey,
) -> bytes:
    """Return the exact domain-separated bytes an external signer must sign."""

    return canonical_json(
        {
            "format_version": SIGNED_TRANSCRIPT_CHECKPOINT_FORMAT,
            "algorithm": ED25519_ALGORITHM,
            "signer_key_id": verifier_key.key_id,
            "signer_public_key_fingerprint": verifier_key.fingerprint,
            "checkpoint": _checkpoint_object(checkpoint),
        }
    ).encode("utf-8")


def create_transcript_head_checkpoint(
    transcript: AdmissionTranscript,
    *,
    checkpoint_sequence: int,
) -> TranscriptHeadCheckpoint:
    """Derive one exact historical checkpoint from a verified transcript prefix."""

    report = verify_admission_transcript(transcript)
    last_entry = transcript.entries[-1] if transcript.entries else None
    return TranscriptHeadCheckpoint(
        transcript_id=transcript.header.transcript_id,
        genesis_digest=report.genesis_digest,
        head_digest=report.head_digest,
        entry_count=report.entry_count,
        last_look=None if last_entry is None else last_entry.look,
        schema_context_digest=transcript.header.schema_context_digest,
        canonical_manifest_digest=(
            None if last_entry is None else last_entry.canonical_manifest_digest
        ),
        checkpoint_sequence=checkpoint_sequence,
    )


def _verify_signature_only(
    signed_checkpoint: SignedTranscriptCheckpoint,
    *,
    trusted_key: Ed25519VerifierKey,
) -> None:
    if signed_checkpoint.signer_key_id != trusted_key.key_id:
        raise ValueError("signed checkpoint signer key ID does not match the trusted key")
    if signed_checkpoint.signer_public_key_fingerprint != trusted_key.fingerprint:
        raise ValueError("signed checkpoint public-key fingerprint does not match the trusted key")
    if not verify_ed25519_signature(
        public_key=trusted_key.public_key_bytes,
        message=checkpoint_signing_bytes(signed_checkpoint.checkpoint, verifier_key=trusted_key),
        signature=signed_checkpoint.signature_bytes,
    ):
        raise ValueError("Ed25519 signature does not verify for the checkpoint payload")


def verify_signed_transcript_checkpoint(
    transcript: AdmissionTranscript,
    signed_checkpoint: SignedTranscriptCheckpoint,
    *,
    trusted_key: Ed25519VerifierKey,
) -> SignedCheckpointVerificationReport:
    """Verify a signed checkpoint against the exact named transcript prefix.

    The supplied transcript may contain later entries. The checkpoint is checked
    against its claimed historical prefix, so a valid look-1 checkpoint remains
    usable after look 2 and beyond. A rolled-back transcript with fewer than the
    signed entries, or a modified/reordered prefix, is rejected.
    """

    checkpoint = signed_checkpoint.checkpoint
    if checkpoint.transcript_id != transcript.header.transcript_id:
        raise ValueError("signed checkpoint transcript ID does not match the transcript")
    if checkpoint.genesis_digest != transcript.header.genesis_digest:
        raise ValueError("signed checkpoint genesis digest does not match the transcript")
    if checkpoint.schema_context_digest != transcript.header.schema_context_digest:
        raise ValueError("signed checkpoint schema context does not match the transcript")
    if checkpoint.entry_count > len(transcript.entries):
        raise ValueError("signed checkpoint lies beyond the supplied transcript prefix")
    prefix = AdmissionTranscript(
        header=transcript.header,
        entries=transcript.entries[: checkpoint.entry_count],
    )
    prefix_report: AdmissionTranscriptVerificationReport = verify_admission_transcript(
        prefix,
        expected_head_digest=checkpoint.head_digest,
    )
    expected = create_transcript_head_checkpoint(
        prefix,
        checkpoint_sequence=checkpoint.checkpoint_sequence,
    )
    if expected != checkpoint:
        raise ValueError("signed checkpoint fields do not match the named transcript prefix")
    _verify_signature_only(signed_checkpoint, trusted_key=trusted_key)
    return SignedCheckpointVerificationReport(
        transcript_id=checkpoint.transcript_id,
        checkpoint_sequence=checkpoint.checkpoint_sequence,
        signed_entry_count=prefix_report.entry_count,
        signed_last_look=checkpoint.last_look,
        signed_head_digest=checkpoint.head_digest,
        signer_key_id=trusted_key.key_id,
        signer_public_key_fingerprint=trusted_key.fingerprint,
    )


def find_signed_checkpoint_equivocations(
    signed_checkpoints: Iterable[SignedTranscriptCheckpoint],
    *,
    trusted_key: Ed25519VerifierKey,
) -> tuple[SignedCheckpointEquivocationEvidence, ...]:
    """Return valid conflicting attestations for one signer/transcript sequence.

    This detects equivocation only when both signed attestations are available to
    compare. It cannot discover a hidden fork or prove external publication.
    """

    observed: dict[tuple[str, str, str, int], SignedTranscriptCheckpoint] = {}
    evidence: list[SignedCheckpointEquivocationEvidence] = []
    for signed in signed_checkpoints:
        _verify_signature_only(signed, trusted_key=trusted_key)
        checkpoint = signed.checkpoint
        key = (
            signed.signer_key_id,
            checkpoint.transcript_id,
            checkpoint.genesis_digest,
            checkpoint.checkpoint_sequence,
        )
        previous = observed.get(key)
        if previous is None:
            observed[key] = signed
        elif previous.checkpoint != checkpoint:
            evidence.append(
                SignedCheckpointEquivocationEvidence(
                    signer_key_id=signed.signer_key_id,
                    transcript_id=checkpoint.transcript_id,
                    genesis_digest=checkpoint.genesis_digest,
                    checkpoint_sequence=checkpoint.checkpoint_sequence,
                    first=previous,
                    second=signed,
                )
            )
    return tuple(evidence)
