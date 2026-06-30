# Mandatory exact proof replay for native v2 transcripts

## Why this layer exists

A native v2 transcript binds a tier-aware manifest, compiler plans, and
role-proof-family artifact hashes into an append-only signed history. A hash
establishes identity, but it does not by itself re-execute a Farkas certificate
or prove that an artifact's branch systems are the same systems emitted by the
compiler.

This layer creates fresh native v2 histories in which each plan and role family
uses a strict replayable artifact format. Verification is incomplete unless it
obtains the referenced bytes from a registry and replays them.

## Fresh-history boundary

`ReplayableNativeTieredAdmissionTranscript` is forward-only. It does not
reinterpret older native v2 records because historical artifacts may be valid
hash commitments without being encoded in the strict replayable format.

A new replayable history begins from a fresh generic transcript genesis. It uses
the unchanged generic chain and checkpoint wire format, but every new entry
contains references to:

```text
one replayable compiler plan per (tier, cell)
one replayable branch bundle per (tier, cell, motif, role)
```

For \(R\) required cells and \(M\) motifs, an entry has exactly

\[
2R
\]

replayable plan artifacts and

\[
6RM
\]

replayable role artifacts.

## Registry model

The transcript stores artifact IDs and SHA-256 digests, not raw proof bytes. A
`ReplayableArtifactRegistry` supplies bytes for those identifiers during
verification.

Before parsing any bytes, the registry checks

\[
H(\text{payload}) = \text{artifact.sha256}.
\]

A missing artifact or a byte change is fail-closed. The registry is therefore
external storage, not an additional source of truth: its payloads must match the
history's committed references.

## Verification chain per role

For every tier/cell/motif/role family, including `UNKNOWN` families, verifier
execution is:

\[
\begin{aligned}
&\text{registry byte digest match}\\
&\to \text{strict replayable plan parse}\\
&\to \text{strict replayable branch-bundle parse}\\
&\to \text{exact SAT witness / Farkas replay}\\
&\to \text{finite-union SAT/UNSAT/UNKNOWN recomputation}\\
&\to \text{query-ID and linear-system equality with plan templates}\\
&\to \text{native v2 proof binding and status-table equality}.
\end{aligned}
\]

The plan artifact also carries a query prefix. It must equal the unique value
constructed from transcript header namespace, tier, look, and cell:

```text
<namespace>/<inner|outer>/look-<t>/cell-<cell_id>
```

This prevents a replayable plan from another look or tier being silently reused.

## Decisive and unresolved roles

A role with replayed `SAT` or `UNSAT` must occur exactly once as a decisive
`TieredSolverQueryProofBinding` in the native v2 manifest.

A role with replayed `UNKNOWN` must occur in the entry status table and must
**not** occur as a decisive v2 proof. It is still replayed, so absence from the
proof-binding list cannot disguise an omitted artifact.

## Signed checkpoints

`create_replayable_native_tiered_transcript_head_checkpoint` first replays all
stored plan and proof artifacts. Only then does it create the existing standard
head checkpoint.

Thus the signed head retains its original generic format, while its transcript
entry digests have been accepted only after full exact proof replay. The usual
limits remain: a checkpoint does not prove that no unrecorded look exists and
does not publish a timestamp by itself.

## Scope

This layer establishes replayability for the encoded rational linear query
systems and their compiler-template identities. It does not prove that the
finite tagged candidate universe contains nature, that motif tags capture the
intended scientific predicate, or that an external coverage method is valid.
Those remain separate declared assumptions and proof interfaces.

## API

| Task | API |
|---|---|
| External committed-byte registry | `ReplayableArtifactRegistry` |
| Create fresh replayable history | `create_replayable_native_tiered_admission_transcript` |
| Append an admitted look | `append_replayable_native_tiered_admitted_look` |
| Replay and verify full history | `verify_replayable_native_tiered_admission_transcript` |
| Create replay-verified checkpoint | `create_replayable_native_tiered_transcript_head_checkpoint` |
| Verify replay-verified signed checkpoint | `verify_signed_replayable_native_tiered_transcript_checkpoint` |
