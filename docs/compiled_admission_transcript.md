# Compiler-admitted transcript and signed-history adapter

## Purpose

The finite-union motif compiler makes active and inactive query families
proof-carrying. The all-look compiler admission layer makes those families part
of an optional-stopping-safe \(\beta=\gamma=0\) path. This module adds the
missing audit layer: it records exactly which compiler plans and branch proofs
were used at every admitted look.

The generic transcript and signed-checkpoint layers already provide a tested hash
chain and Ed25519 checkpoint format. Rather than fork those protocols, the
adapter computes one compiler-evidence commitment and places its digest in the
existing generic entry's `admission_evidence_reference` under the reserved
prefix:

```text
compiler-admission-entry/v1:<sha256>
```

The generic entry hash and any existing signed checkpoint therefore bind the
compiler evidence automatically.

## Fixed header commitments

A compiler transcript header contains a generic `AdmissionTranscriptHeader` plus
these fixed compiler artifacts:

- a caller-supplied artifact committing the base exact-admission schema;
- a deterministic artifact committing the verified tagged polyhedral partition;
- the fixed compiler query namespace; and
- a deterministic aggregate artifact that commits the preceding items together
  with the compiler schema-context digest.

The schema-context digest includes the inner/outer target, motif vocabulary,
required cells, compiler namespace, verified partition digest, and all-look
solver/inclusion certificate declarations.

A transcript cannot be reused under a changed tagged partition or a changed
base schema without changing its genesis hash.

## Per-look evidence commitment

At each admitted look, the adapter derives—not accepts from the caller—these
artifacts from the #24 admitted object:

1. the same fixed partition artifact;
2. one compiled query-plan artifact for every
   \((\mathrm{tier},\mathrm{required\ cell})\); and
3. one complete branch-proof-family artifact for every

   \[
   (\mathrm{tier},\mathrm{cell},\mathrm{motif},\mathrm{role}),
   \qquad
   \mathrm{role}\in\{\mathrm{nonempty},\mathrm{active},\mathrm{inactive}\}.
   \]

For \(R\) required cells and \(M\) motifs, each entry must therefore contain
exactly

\[
2R
\]

plan artifacts and

\[
6RM
\]

role-proof-family artifacts. Missing, duplicated, substituted, or cross-tier
artifacts are rejected by the wrapper verifier.

The commitment also includes the original #24 admission and inclusion evidence
references plus the verifier identifier. The generic entry's status labels are
still recomputed through the #16 outer-envelope audit; no raw `INVARIANT` or
`EXTENSION_STABLE` string is trusted as input.

## Why this is tier-aware

Manifest v1 uses query keys of the form

```text
(look, cell, motif, role)
```

and has no `inner` / `outer` coordinate. It cannot faithfully bind both tier
families in one slot. The compiler transcript is intentionally the tier-aware
layer. The canonical manifest remains committed in the generic transcript entry
and continues to bind global candidate-space and coverage declarations, while
the compiler transcript binds both inner and outer query plans and proofs.

A future manifest revision may add a tier coordinate. This adapter does not
pretend the current manifest already has one.

## Signatures and checkpoints

A `CompiledAdmissionTranscript` contains an ordinary `AdmissionTranscript`
chain. After validating detailed compiler evidence, the adapter delegates to the
existing checkpoint functions:

```python
checkpoint = create_compiled_transcript_head_checkpoint(
    transcript,
    checkpoint_sequence=1,
)
```

The resulting `TranscriptHeadCheckpoint` is standard #22 data: its signed head
digest includes every compiler-entry commitment through the generic entry hash.
`verify_signed_compiled_transcript_checkpoint` first verifies compiler evidence,
then invokes the normal Ed25519 checkpoint verifier.

Thus no new signature algorithm, private-key handling, or checkpoint wire format
is introduced.

## Limits

The adapter provides integrity of committed artifacts, not a universal proof of
their semantics. Exact branch semantics are established when #24 constructs the
admitted look. A later verifier can detect changed or omitted artifact
commitments, but it does not re-run all Farkas proofs from opaque artifact bytes.

The transcript still cannot prove that every externally inspected look was
recorded. Rollback and hidden-fork detection still require an externally retained
or signed checkpoint head. The declared tagged union, motif tags, and external
all-look coverage remain explicit scientific and statistical assumptions.

## API

| Task | API |
|---|---|
| Create a compiler-aware chain | `create_compiled_admission_transcript` |
| Append a #24-admitted look | `append_compiled_admitted_look` |
| Verify chain and compiler evidence | `verify_compiled_admission_transcript` |
| Create standard signed-checkpoint payload | `create_compiled_transcript_head_checkpoint` |
| Verify compiler evidence and an Ed25519 checkpoint | `verify_signed_compiled_transcript_checkpoint` |
