# Native v2 manifest integration for compiler-admitted transcripts

## Purpose

The compiler transcript adapter binds every inner/outer plan and role-proof
family into a hash chain. Manifest v2 independently gives tier-aware proof
identities. This module connects the two at the byte level.

For every admitted look, it derives a **per-look native v2 manifest** from the
actual #24 compiler-admitted snapshot, computes its strict canonical v2 bytes,
and puts the digest into the generic transcript entry commitment. The unchanged
Ed25519 checkpoint therefore signs a transcript head that directly commits to
that v2 manifest byte sequence.

## Why the manifest is per-look

A transcript entry records one admitted analysis state. The native manifest for
look \(t\) contains the plans and proof families used at exactly that look:

\[
\mathcal M_t^{\mathrm{v2}}.
\]

A cumulative manifest would repeat all earlier evidence inside every later entry
and would make it less clear which proof family supports which historical
conclusion. The transcript already provides cumulative order through its hash
chain:

\[
h_t = H(h_{t-1}, \mathrm{entry}_t).
\]

Thus each entry binds its own exact manifest and the chain binds their history.

## Source v1 continuity

The current all-look admission schema still receives its global target and
coverage/solver assertion declarations through a v1 manifest. Native v2 entries
therefore bind both:

```text
source_v1_manifest_digest
canonical_v2_manifest_digest
```

The generic base entry's `canonical_manifest_digest` must equal the recorded
source-v1 digest. The native v2 manifest reuses that v1 target and assertion
objects but adds:

- the fixed semantic partition artifact;
- plans keyed by `(tier, look, cell)`; and
- decisive proof families keyed by `(tier, look, cell, motif, role)`.

This preserves continuity with the historical v1 target while providing the
first-class tier coordinate needed for compiler evidence.

## Exact derivation at one look

The adapter accepts an admitted #24 look, not caller-supplied plan or proof
artifacts. It derives:

1. one inner and one outer plan artifact for every required cell;
2. one role-proof-family artifact for every
   `(tier, cell, motif, nonempty/active/inactive)`; and
3. the aggregate status of each role family.

A role with status `SAT` or `UNSAT` is included in the native v2 manifest as a
decisive `TieredSolverQueryProofBinding`. A role with status `UNKNOWN` remains
in the entry's explicit role-status table and compiler artifact commitment, but
is deliberately omitted from the v2 **decisive-proof** set.

This distinction prevents an unresolved branch family from being silently
upgraded to a theorem-supporting proof merely because it has a content-addressed
artifact.

## Entry commitment

The native entry commitment includes:

```text
compiler-evidence commitment artifact
source v1 canonical manifest digest
native v2 manifest artifact
native v2 canonical digest
all tier/cell/motif/role aggregate statuses
```

The generic `AdmissionTranscriptEntry.admission_evidence_reference` stores the
result under:

```text
native-tiered-admission-entry/v1:<sha256>
```

Changing the v2 manifest, source-v1 link, status table, compiler plans, or role
proof family changes this digest, then changes the generic entry hash, all later
hashes, and any signed checkpoint head.

## Checkpoint behavior

No new signature format is introduced. After native evidence verification,
`create_native_tiered_transcript_head_checkpoint` delegates to the established
checkpoint code. A signed checkpoint therefore attests the same generic head
format while that head now contains native-v2 manifest commitments.

The usual limits remain unchanged: a signature does not prove every externally
inspected look was recorded, prove publication time, or expose a hidden fork
without an external checkpoint/witness mechanism.

## Compatibility boundary

This is a new transcript variant. Existing #25 histories remain valid and are
not reinterpreted. They continue to use their original compiler-evidence
commitment. New native-v2 histories should start from a fresh transcript genesis
and use this adapter from their first entry.

No automatic conversion of a historical entry is provided: a historical v1
record may not contain enough tier/status structure to reconstruct a native v2
manifest without additional external artifacts.

## API

| Task | API |
|---|---|
| Derive one exact per-look v2 manifest | `build_native_tiered_manifest_for_admitted_look` |
| Create fresh native-v2 history | `create_native_tiered_admission_transcript` |
| Append #24 admitted look and v2 commitment | `append_native_tiered_admitted_look` |
| Verify generic chain and native-v2 evidence | `verify_native_tiered_admission_transcript` |
| Create standard signed checkpoint | `create_native_tiered_transcript_head_checkpoint` |
| Verify native history plus signed checkpoint | `verify_signed_native_tiered_transcript_checkpoint` |
