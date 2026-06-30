# Append-only exact-admission transcript

## Purpose

The exact all-look admission gate establishes, for every look routed through it,
that the outer solver and inner-to-outer inclusion conditions are proof-carrying:

\[
\beta=\gamma=0.
\]

A stopped conclusion also needs a record of **which admitted look** supplied the
reported result. This module creates an append-only hash transcript for those
admitted looks.

It binds each record to:

- a fixed exact-admission schema context;
- a content-addressed external artifact for the serialized base systems and
  admission proof material;
- the strict canonical digest of a `CertificateManifest`;
- the immediately previous transcript entry; and
- outer / extension statuses recomputed from the actual admitted paired snapshot.

## Header and genesis commitment

One `AdmissionTranscriptHeader` fixes:

```text
transcript ID
manifest target digest
ordered motif vocabulary and required cells
admission-schema artifact SHA-256
exact beta/gamma-zero schema-context digest
```

The header yields a deterministic genesis digest. Every entry thereafter stores
its predecessor's digest.

\[
h_0=H(\mathrm{header}),
\qquad
h_i=H(\mathrm{entry}_i[h_{i-1}]).
\]

The hash input includes sequence index, recorded look, canonical manifest digest,
schema context digest, proof evidence references, verifier ID, outer statuses,
and extension statuses.

## Appending a look

`append_admitted_look` does not accept hand-written status labels. It requires a
`VerifiedExactPolyhedralExtensionLook` produced by the #19 gate and then:

1. rechecks that the manifest matches the live candidate space, coverage
   certificate, and exact all-look solver certificate;
2. rechecks that the admitted snapshot has the fixed transcript target;
3. rechecks the schema-context digest and look scope;
4. runs the existing anytime symbolic outer-envelope audit on that snapshot; and
5. records the resulting outer and extension status for every declared motif.

A transcript entry therefore cannot call a motif `extension-stable` unless the
existing exact-admission / outer-envelope audit returns that status.

## Integrity properties

Given a known header and a separately retained expected head digest, verification
detects:

- modification of an intermediate entry, because the next predecessor link no
  longer matches;
- modification of the terminal entry, because the computed head differs from the
  expected head;
- entry reordering, duplicate / non-increasing look IDs, or broken sequence
  numbers;
- cross-target or cross-schema transplant, because header context and entry
  context digests differ; and
- suffix deletion / rollback, when the original head digest is supplied as
  `expected_head_digest`.

A decision anchor names one historical decisive `EXTENSION_STABLE` entry by
sequence, look, motif, manifest digest, and entry digest. It remains valid when
later entries are appended because it verifies against the named prefix, not the
current head.

## What the hash chain cannot establish

The transcript is deliberately not oversold.

Without publishing or otherwise externally retaining a head digest, an attacker
can present a shorter valid prefix. Likewise, a hash chain alone cannot prove
that every analysis look actually performed by an external caller was recorded,
or that no alternate fork was created after a shared prefix.

The transcript therefore provides **integrity relative to an anchored head**, not
universal completeness or trusted chronology. Detecting rollback / equivocation
requires one or more external mechanisms, such as a signature, immutable object
store, public append-only registry, trusted timestamp, or independently retained
head digest.

It also does not re-run solver proofs from transcript entries. Exact semantic
verification happens at entry construction through the #19 admission gate.

## Relation to the optional-stopping theorem

For a look admitted through #19 and recorded in this transcript, the theorem
inputs are still:

\[
P(\text{false decisive outer conclusion or invalid extension stability at any
admitted look})\le\alpha,
\]

because \(\beta=\gamma=0\) on the exact gate's declared scope. The transcript
does not improve that probability bound. It makes a subsequent stopped claim
traceable to an immutable-in-context admitted prefix.

## API

| Object | API |
|---|---|
| Fixed transcript target | `AdmissionTranscriptHeader` |
| One chained admitted look | `AdmissionTranscriptEntry` |
| Immutable transcript prefix | `AdmissionTranscript` |
| Header construction | `create_admission_transcript_header` |
| Append one #19-admitted look | `append_admitted_look` |
| Verify chain / optional known head | `verify_admission_transcript` |
| Anchor a decisive stable conclusion | `create_transcript_decision_anchor` |
| Verify a historical anchor | `verify_transcript_decision_anchor` |
