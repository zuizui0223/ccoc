# Replayable exact rational linear proof artifacts

## Problem

A manifest or transcript hash proves that an artifact's bytes have not changed
relative to a trusted digest. It does not, by itself, prove that those bytes can
still be interpreted as a valid rational SAT witness or Farkas infeasibility
certificate.

The exact linear verifier already checks these objects in memory:

\[
Ax\le b,
\]

with either

\[
x_0\in\mathbb Q^d,
\qquad
Ax_0\le b,
\]

or a Farkas certificate

\[
\lambda\ge 0,
\qquad
\lambda^\top A=0,
\qquad
\lambda^\top b<0.
\]

This layer makes the complete query and proof available as strict canonical
bytes, then reconstructs it and reruns that exact verification.

## Query artifact format

`rach-replayable-exact-linear-query/v1` contains:

```text
format version
query ID
ordered variable names
ordered inequality rows
canonical rational coefficients and bounds
proof status
rational witness or Farkas multiplier vector
producer, evidence reference, and assumptions
```

All rational values are JSON strings in exactly the spelling returned by
`str(Fraction(value))`.

Examples:

```text
"0"
"-3"
"1/2"
"-7/9"
```

Rejected spellings include:

```text
"2/4"       # not reduced
"01"        # noncanonical integer
"-0"        # canonical spelling is "0"
"1.0"       # decimal spelling is not canonical Fraction text
0.5          # JSON number / binary-float ambiguity
```

The parser also rejects UTF-8 BOMs, duplicate keys, unknown or missing fields,
nonfinite JSON constants, whitespace/newline variants, changed key order, and
any valid JSON that does not reserialize byte-for-byte to the unique canonical
form.

## Replay

`replay_exact_linear_query` performs three steps:

1. strict parse and canonical-byte equality;
2. optional SHA-256 equality against an expected artifact digest; and
3. exact re-execution of `verify_linear_query`.

A changed witness that still has canonical JSON spelling is therefore not merely
a new artifact; it is also rejected if it violates an inequality. A malformed
Farkas vector is rejected if it has a negative multiplier, fails to eliminate a
variable, or fails to derive a negative constant bound.

## Finite branch families

The motif compiler represents a union of polyhedral branches, not one falsely
collapsed conjunction. `rach-replayable-exact-linear-bundle/v1` records a finite
family of replayable queries together with its declared aggregate status.

Replay verifies every branch and recomputes:

\[
\operatorname{status}\left(\bigcup_j B_j\right)=
\begin{cases}
\mathrm{SAT}, & \exists j:\; B_j\neq\varnothing,\\
\mathrm{UNSAT}, & \forall j:\; B_j=\varnothing,\\
\mathrm{UNKNOWN}, & \text{otherwise}.
\end{cases}
\]

The empty branch family is structurally `UNSAT`, matching the empty union.
A declared aggregate status differing from replayed status is rejected.

## Compiler adapter

`replayable_compiled_role_artifacts` ties a replayed branch family back to an
exact compiled polyhedral plan. It requires agreement on:

```text
plan digest
partition digest
motif
role
exact branch query-ID set
exact branch linear systems
```

This is essential. A different system may have a perfectly valid Farkas
certificate yet still not represent the compiler-generated branch for the
claimed motif role. The adapter rejects that substitution after replay.

Thus the proof chain for a new role artifact is:

\[
\text{artifact bytes}
\to
\text{exact replay of each witness/Farkas proof}
\to
\text{finite-union aggregation}
\to
\text{compiler-template identity}.
\]

## Scope and compatibility

This format is forward-only. Existing historical proof artifacts remain valid
identity commitments, but are not retroactively declared replayable because they
may not include enough strict serialization metadata or an explicit artifact
format version.

The replay layer does not prove that a compiler plan represents nature, establish
statistical coverage, prove declared-universe adequacy, or replace the trusted
correctness of the Fraction parser and verifier implementation. It converts the
previously opaque exact linear artifact boundary into a replayable one.

## API

| Task | API |
|---|---|
| Canonical query bytes | `canonical_exact_linear_query_bytes` |
| Create query artifact | `exact_linear_query_artifact` |
| Strict parse / exact replay | `parse_canonical_exact_linear_query`, `replay_exact_linear_query` |
| Create finite branch bundle | `ExactLinearProofBundle` |
| Canonical bundle bytes / artifact | `canonical_exact_linear_bundle_bytes`, `exact_linear_bundle_artifact` |
| Strict bundle replay | `parse_canonical_exact_linear_bundle`, `replay_exact_linear_bundle` |
| Build compiler-linked bundle | `build_replayable_compiled_role_bundle` |
| Replay and bind to compiler plan | `replay_compiled_role_proof_bundle` |
