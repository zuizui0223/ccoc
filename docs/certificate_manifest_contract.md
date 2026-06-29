# Certificate manifest contract

## Why this layer exists

The anytime symbolic theorem depends on several external objects referring to the
same formal target: a candidate-space encoding, motif predicates, required cells,
a look scope, a statistical coverage assertion, solver-validity evidence, and
individual query/proof artifacts.

A filename or prose label does not prevent a proof from being reused for a
different motif, cell, or look. This module records SHA-256 commitments to the
relevant bytes and metadata.

It does not prove a confidence theorem, parse a solver proof, validate a
scientific encoding, authenticate an author, or establish provenance.

## Manifest target

`ManifestTarget` binds:

```text
candidate-space description and encoding digest
one definition digest per motif
required cell IDs
finite look scope, or all positive integer looks
```

The candidate-space payload should be a formal encoding, not merely a title.
Each motif payload should contain the predicate definition or a canonical
reference to it. RACH can bind these bytes but cannot decide whether they model
nature correctly.

Canonical JSON sorts mapping keys and represents floating values by exact Python
hexadecimal floats before hashing. Mapping-key order therefore does not change
a digest; changing a target, bound, scope, predicate, or artifact byte does.

## Assertion and proof bindings

`ExternalAssertionBinding` binds the two theorem-level assertions:

```text
time-uniform-statistical-coverage
time-uniform-solver-semantic-validity
```

The lower bound, method, assumptions, and evidence artifact digest must exactly
match the live certificate objects.

`SolverQueryProofBinding` binds one decisive result by:

```text
look, cell ID, motif, query role, SAT/UNSAT status,
query-encoding digest, proof-artifact digest, verifier ID
```

A binding is rejected if its look is outside scope, if its motif or cell is not
in the target, or if another binding already uses the same
`(look, cell, motif, role)`. `UNKNOWN` is never a decisive proof binding.

## Verification

1. Build a `ManifestTarget` from exact candidate-space and motif payloads.
2. Bind external coverage and solver-validity evidence.
3. Bind every decisive query encoding and proof artifact.
4. Build the target-consistent manifest.
5. Verify context and recompute every content hash before using the theorem
   result.

`verify_manifest_context` checks the target against live theorem inputs.
`verify_manifest_artifacts` rejects missing, unexpected, or modified content.
`verify_anytime_symbolic_manifest` performs both checks.

## Trust boundary

The theorem remains

\[
P(\text{any false decisive result at any certified look})
\le \min(1,\alpha+\beta).
\]

The manifest makes its inputs auditable; it does not alter the bound. SHA-256 is
an integrity commitment under ordinary collision-resistance assumptions. It is
not a signature, timestamp, availability guarantee, proof of semantic validity,
or proof that the candidate universe contains nature.

A proof-carrying linear witness or Farkas certificate can be bound in this
format. The linear verifier addresses proof semantics; the manifest addresses
whether that proof was attached to the intended query, motif, cell, and look.
