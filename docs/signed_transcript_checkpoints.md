# Ed25519-signed transcript checkpoints

## Purpose

An append-only transcript hash chain detects mutation only relative to a known
head digest. A **signed checkpoint** turns that head into a portable,
public-key-verifiable commitment.

An external Ed25519 signer signs a domain-separated payload containing one exact
transcript prefix. Any party with the trusted public key can then verify that the
transcript still contains that signed prefix.

The private key is intentionally outside RACH. It may live in a hardware token,
CI secret, offline signing service, or institutional key-management system. RACH
contains only verification logic over public inputs.

## Exact signed payload

A `TranscriptHeadCheckpoint` records:

```text
transcript ID
genesis digest
head digest
entry count
last recorded look
schema-context digest
canonical manifest digest at the head
checkpoint sequence
```

The signer message is canonical JSON with a distinct format identifier:

```text
rach-signed-transcript-checkpoint/v1
```

and binds additionally:

```text
algorithm = ed25519
signer key ID
SHA-256 fingerprint of the signer public key
```

Thus a signature for one transcript, schema, signer identity, or historical
prefix cannot be reused as a valid signature for another payload.

## Verification

`verify_signed_transcript_checkpoint` performs four checks:

1. The transcript prefix with exactly the signed `entry_count` is internally
   valid and has the signed head digest.
2. The signed checkpoint fields equal the checkpoint recomputed from that exact
   prefix.
3. The attestation key ID and public-key fingerprint match the externally
   trusted `Ed25519VerifierKey`.
4. The detached Ed25519 signature verifies over the canonical domain-separated
   payload.

A signed checkpoint at look 1 remains verifiable after later entries are
appended: verification selects the named historical prefix rather than requiring
the checkpoint to equal the current transcript head.

Conversely, a transcript shorter than the signed prefix is rejected. This gives
the hash chain the external head anchor it lacked in the prior layer.

## Ed25519 verifier scope

The included verification-only implementation follows RFC 8032’s Ed25519
verification equation and rejects:

- non-canonical public-key and ``R`` point encodings;
- non-canonical scalar values \(S\ge q\); and
- points outside the prime-order subgroup.

It operates only on public values. It is not a signing routine, private-key
store, or side-channel-hardened secret-key implementation. The test suite uses
an RFC 8032 vector plus a precomputed signature over a fixed checkpoint payload.

## Equivocation evidence

A signature proves that one key signed one checkpoint; it does not prevent the
key holder from signing two conflicting checkpoints. If two valid attestations
are available with the same:

```text
signer key ID
transcript ID
genesis digest
checkpoint sequence
```

but different checkpoint payloads, `find_signed_checkpoint_equivocations`
returns both signatures as explicit equivocation evidence.

This detects equivocation only after both attestations are observed. It does not
force publication, prove a chronology, or reveal a hidden fork.

## Boundaries

Signed checkpoints strengthen auditability but do not change the RACH inference
bound:

\[
P(\text{false decisive outer conclusion or invalid stability at an admitted look})
\le\alpha
\]

when the exact admission layer supplies \(\beta=\gamma=0\).

They also do not prove that every external analysis look was recorded, establish
a trusted timestamp, provide a transparency log, or identify the real-world
person or institution behind a public key. Those require operational key trust,
external publication, or an additional witness/registry layer.

## API

| Object | API |
|---|---|
| Trusted public key | `Ed25519VerifierKey` |
| Exact signed transcript prefix | `TranscriptHeadCheckpoint` |
| Detached attestation | `SignedTranscriptCheckpoint` |
| Signing payload bytes | `checkpoint_signing_bytes` |
| Create checkpoint from a transcript | `create_transcript_head_checkpoint` |
| Verify raw RFC 8032 signature | `verify_ed25519_signature` |
| Verify signature and transcript prefix | `verify_signed_transcript_checkpoint` |
| Compare two valid conflicting checkpoints | `find_signed_checkpoint_equivocations` |
