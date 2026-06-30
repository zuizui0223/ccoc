# Proof-carrying all-look coverage contracts

## Why this layer exists

RACH's core theorem is intentionally conditional. It consumes an external
all-look statement

\[
\Pr\left[
\forall t\in\mathcal T,\;
\theta^\star\in\bigcap_{r\in\mathcal R}C_{r,t}
\right]
\ge 1-\alpha.
\]

A bare lower bound, method name, and prose assumption list are not enough to
audit such a statement. In particular, they do not identify the exact
observation channel, the data-prefix-to-retained-set encoder, or the theorem
artifact that is meant to justify coverage.

`AllLookCoverageContract` makes those inputs first-class, content-addressed
objects.

## The contract

One contract fixes:

```text
contract ID
manifest target digest and candidate-space artifact
observation-channel artifact
retained-set encoder artifact
coverage proof artifact
true candidate label
required cell IDs
all-look or finite certified look scope
lower bound, method, and assumptions
method-specific coverage verifier ID
```

The event asserted by the format is fixed:

\[
\Pr\left[
\forall t\in\mathcal T,\;
\theta^\star\in\bigcap_{r\in\mathcal R}C_{r,t}
\right]
\ge \texttt{lower\_bound}.
\]

The contract digest is the SHA-256 of canonical bytes containing every field
above. Changing the encoder, channel, proof artifact, target, \(\alpha\), or
scope changes the digest.

## What RACH verifies itself

Before accepting an external coverage verifier, RACH checks that the contract
and live `AnytimeSymbolicJointCoverageCertificate` name exactly the same event:

- target digest and candidate-space artifact;
- required cells;
- look scope;
- true candidate label;
- lower bound;
- method; and
- assumptions.

RACH also verifies SHA-256 content identity for every artifact named by the
contract.

Thus a theorem for one retained-set encoder cannot be silently reused for a
different encoder that happens to claim the same numerical confidence level.

## Method-specific proof verification

There is no universal proof checker for arbitrary confidence sequences,
martingale arguments, conformal constructions, Bayesian procedures, or other
coverage methods. The interface therefore requires a method-specific
`CoverageProofVerifier`:

```python
receipt = verifier.verify_all_look_coverage(contract, artifact_payloads)
```

The returned receipt must bind the exact contract digest and the exact hashes of
its coverage proof, retained-set encoder, and observation channel. RACH rejects
a receipt with any mismatch.

The external verifier's mathematical correctness is an explicit trusted
computing-base assumption. This is honest: arbitrary statistical proof checking
cannot be made generic merely by wrapping a file in SHA-256.

## Binding coverage into v2 manifests and signed history

`CoverageBoundTieredManifest` combines a tier-aware v2 manifest with an exact
coverage-contract artifact. It requires that the v2 target and coverage
assertion match the contract's target, cells, scope, lower bound, method, and
assumptions.

For native v2 transcript histories,
`create_coverage_bound_native_tiered_admission_transcript` puts a canonical
aggregate of

```text
base exact-admission schema artifact
coverage-contract artifact
coverage-contract digest
```

into the transcript genesis. The generic append-only chain hashes genesis into
every entry, and the existing Ed25519 checkpoint signs the resulting head.

The all-look contract is fixed across the history, so binding it once in genesis
is sufficient. Every per-look v2 manifest is then checked to share that exact
coverage assertion before it can be appended.

The resulting path is:

\[
\text{coverage contract}
\to
\text{native v2 manifest consistency}
\to
\text{transcript genesis and entries}
\to
\text{signed checkpoint}.
\]

## Boundaries

This contract does not itself establish coverage. It does not infer the true
candidate, prove declared-universe adequacy, make a finite look guarantee
all-look, or replay arbitrary proof languages without a method-specific
verifier.

It strengthens the existing theorem by making the external \(\alpha\) premise
an explicit, auditable, content-addressed input with a named verification hook.
The final RACH bound remains conditional on the verified coverage method and the
other declared admission/compiler assumptions.

## API

| Task | API |
|---|---|
| Construct from a live coverage certificate | `coverage_contract_from_certificate` |
| Bind canonical contract bytes | `coverage_contract_artifact` |
| Verify target/certificate identity | `verify_all_look_coverage_contract_context` |
| Verify named artifact bytes | `verify_all_look_coverage_contract_artifacts` |
| Run method-specific proof verification | `verify_all_look_coverage_contract` |
| Bind coverage to a v2 manifest | `CoverageBoundTieredManifest` |
| Create coverage-bound native history | `create_coverage_bound_native_tiered_admission_transcript` |
| Verify / append coverage-bound history | `verify_coverage_bound_native_tiered_admission_transcript`, `append_coverage_bound_native_tiered_admitted_look` |
