from dataclasses import replace

import pytest

from causal_model.admission_transcript import (
    AdmissionTranscript,
    AdmissionTranscriptEntry,
    AdmissionTranscriptHeader,
)
from causal_model.certificate_manifest import ArtifactReference, sha256_digest
from causal_model.signed_transcript_checkpoint import (
    Ed25519VerifierKey,
    SignedTranscriptCheckpoint,
    TranscriptHeadCheckpoint,
    checkpoint_signing_bytes,
    create_transcript_head_checkpoint,
    find_signed_checkpoint_equivocations,
    verify_ed25519_signature,
    verify_signed_transcript_checkpoint,
)


PUBLIC_KEY_HEX = "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a"
SIGNER_KEY_ID = "checkpoint-key"
SIGNER_FINGERPRINT = "21fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9"
CHECKPOINT_SIGNATURE_HEX = (
    "ff63c3aa389be00b2b64a1397eecdfa016d9c70e95af9b82b88b387a021de52e"
    "fc5c3acabeff61bcb00d1f02a61246a061ad54f94965d6b60ea69d19bed3cb00"
)
CONFLICTING_SIGNATURE_HEX = (
    "2dbe4b9ea2b9611c9fbce09d4215208724036bffb7772f65e27fda34ea55df6c"
    "8ad0acc7e0504a4ec4de61d584a6cb7abfb95aa7fe09d5c1ed9ac0d3c47ae507"
)


def trusted_key():
    return Ed25519VerifierKey(SIGNER_KEY_ID, PUBLIC_KEY_HEX)


def transcript_with_one_entry():
    target_digest = sha256_digest("target")
    schema_digest = sha256_digest("schema")
    manifest_digest = sha256_digest("manifest")
    header = AdmissionTranscriptHeader(
        transcript_id="signed-run",
        target_digest=target_digest,
        motifs=("focal",),
        required_cell_ids=("primary",),
        admission_schema_artifact=ArtifactReference.from_payload(
            "schema",
            b"base proof",
            media_type="application/json",
        ),
        schema_context_digest=schema_digest,
    )
    first = AdmissionTranscriptEntry(
        sequence=1,
        look=1,
        previous_entry_digest=header.genesis_digest,
        canonical_manifest_digest=manifest_digest,
        schema_context_digest=schema_digest,
        admission_evidence_reference="proof://look-1",
        inclusion_evidence_reference="proof://inclusion-1",
        admission_verifier="exact-admission",
        outer_statuses={"focal": "invariant"},
        extension_statuses={"focal": "extension-stable"},
    )
    return AdmissionTranscript(header=header, entries=(first,))


def signed_checkpoint(transcript=None):
    transcript = transcript or transcript_with_one_entry()
    checkpoint = create_transcript_head_checkpoint(transcript, checkpoint_sequence=1)
    return SignedTranscriptCheckpoint(
        checkpoint=checkpoint,
        signer_key_id=SIGNER_KEY_ID,
        signer_public_key_fingerprint=SIGNER_FINGERPRINT,
        signature_hex=CHECKPOINT_SIGNATURE_HEX,
    )


def append_later_entry(transcript):
    first = transcript.entries[-1]
    second = AdmissionTranscriptEntry(
        sequence=2,
        look=2,
        previous_entry_digest=first.entry_digest,
        canonical_manifest_digest=sha256_digest("manifest-2"),
        schema_context_digest=transcript.header.schema_context_digest,
        admission_evidence_reference="proof://look-2",
        inclusion_evidence_reference="proof://inclusion-2",
        admission_verifier="exact-admission",
        outer_statuses={"focal": "invariant"},
        extension_statuses={"focal": "extension-stable"},
    )
    return AdmissionTranscript(header=transcript.header, entries=(*transcript.entries, second))


def test_rfc_8032_ed25519_vector_and_basic_tampering_rejection():
    public_key = bytes.fromhex(PUBLIC_KEY_HEX)
    signature = bytes.fromhex(
        "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e06522490155"
        "5fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b"
    )

    assert verify_ed25519_signature(public_key=public_key, message=b"", signature=signature)
    assert not verify_ed25519_signature(public_key=public_key, message=b"changed", signature=signature)
    assert not verify_ed25519_signature(
        public_key=public_key,
        message=b"",
        signature=signature[:-1] + bytes([signature[-1] ^ 1]),
    )


def test_signed_checkpoint_verifies_exact_transcript_prefix_and_signature():
    transcript = transcript_with_one_entry()
    signed = signed_checkpoint(transcript)
    report = verify_signed_transcript_checkpoint(transcript, signed, trusted_key=trusted_key())

    assert report.signed_entry_count == 1
    assert report.signed_last_look == 1
    assert report.signed_head_digest == transcript.head_digest
    assert signed.checkpoint == create_transcript_head_checkpoint(transcript, checkpoint_sequence=1)
    assert checkpoint_signing_bytes(signed.checkpoint, verifier_key=trusted_key()) == (
        b'{"algorithm":"ed25519","checkpoint":{"canonical_manifest_digest":"05b3abf2579a5eb66403cd78be557fd860633a1fe2103c7642030defe32c657f","checkpoint_sequence":1,"entry_count":1,"format_version":"rach-transcript-head-checkpoint/v1","genesis_digest":"0c8123c9a7aa270bcc825159da3d62a44c1c54662d598270bdb8653a706adb83","head_digest":"f81e7772f96b6ff5a8d849a97c9befb334b2fa8fec7c7d75dbcd53e82b10b31b","last_look":1,"schema_context_digest":"df0ad6e43880f09c90ebf95f19110178aba6890df0010ebda7485029e2b543b4","transcript_id":"signed-run"},"format_version":"rach-signed-transcript-checkpoint/v1","signer_key_id":"checkpoint-key","signer_public_key_fingerprint":"21fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9"}'
    )


def test_historical_signed_checkpoint_remains_valid_after_later_append():
    one = transcript_with_one_entry()
    signed = signed_checkpoint(one)
    two = append_later_entry(one)

    report = verify_signed_transcript_checkpoint(two, signed, trusted_key=trusted_key())
    assert report.signed_entry_count == 1
    assert report.signed_head_digest == one.head_digest


def test_signed_checkpoint_detects_rollback_and_prefix_tampering():
    one = transcript_with_one_entry()
    signed = signed_checkpoint(one)
    rolled_back = AdmissionTranscript(header=one.header)
    with pytest.raises(ValueError, match="beyond the supplied transcript prefix"):
        verify_signed_transcript_checkpoint(rolled_back, signed, trusted_key=trusted_key())

    tampered_entry = replace(one.entries[0], admission_evidence_reference="proof://substituted")
    tampered = AdmissionTranscript(header=one.header, entries=(tampered_entry,))
    with pytest.raises(ValueError, match="expected_head_digest"):
        verify_signed_transcript_checkpoint(tampered, signed, trusted_key=trusted_key())


def test_key_binding_and_signature_tampering_are_rejected():
    transcript = transcript_with_one_entry()
    signed = signed_checkpoint(transcript)
    wrong_key = Ed25519VerifierKey(
        "other-key",
        "3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c",
    )
    with pytest.raises(ValueError, match="key ID"):
        verify_signed_transcript_checkpoint(transcript, signed, trusted_key=wrong_key)

    tampered_signature = replace(signed, signature_hex="00" * 64)
    with pytest.raises(ValueError, match="signature does not verify"):
        verify_signed_transcript_checkpoint(transcript, tampered_signature, trusted_key=trusted_key())


def test_two_valid_conflicting_checkpoints_are_equivocation_evidence():
    transcript = transcript_with_one_entry()
    first = signed_checkpoint(transcript)
    conflicting_checkpoint = TranscriptHeadCheckpoint(
        transcript_id="signed-run",
        genesis_digest=first.checkpoint.genesis_digest,
        head_digest="cfcd8a409e61cd2380d2cb9f7766fab3dfb670eee1d5630625c9acc0bfd1ffef",
        entry_count=1,
        last_look=1,
        schema_context_digest=first.checkpoint.schema_context_digest,
        canonical_manifest_digest=first.checkpoint.canonical_manifest_digest,
        checkpoint_sequence=1,
    )
    second = SignedTranscriptCheckpoint(
        checkpoint=conflicting_checkpoint,
        signer_key_id=SIGNER_KEY_ID,
        signer_public_key_fingerprint=SIGNER_FINGERPRINT,
        signature_hex=CONFLICTING_SIGNATURE_HEX,
    )

    evidence = find_signed_checkpoint_equivocations((first, second), trusted_key=trusted_key())
    assert len(evidence) == 1
    assert evidence[0].checkpoint_sequence == 1
    assert evidence[0].first.checkpoint.head_digest != evidence[0].second.checkpoint.head_digest


def test_checkpoint_constructor_rejects_inconsistent_empty_history_shape():
    with pytest.raises(ValueError, match="empty transcript checkpoint"):
        TranscriptHeadCheckpoint(
            transcript_id="empty",
            genesis_digest="0" * 64,
            head_digest="1" * 64,
            entry_count=0,
            last_look=1,
            schema_context_digest="2" * 64,
            canonical_manifest_digest=None,
            checkpoint_sequence=1,
        )
