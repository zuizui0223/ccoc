# Certificate-complete decision audit

## Purpose

A certificate manifest binds artifacts to one RACH theorem target. The decision
audit asks a stricter question:

> Does the concrete symbolic status reported at this look have every
> target-bound witness or proof needed for that status?

The audit runs after manifest context and payload verification. It compares the
live `FeasibilityCertificate` objects in a symbolic snapshot against the
manifest's `(look, cell, motif, role)` proof bindings. A source conclusion that
lacks a complete binding chain is downgraded to `UNSUPPORTED`.

## Required evidence

For each required cell `r`, look `t`, and motif `m`:

```text
INVARIANT:
  C[r,t] is nonempty                 SAT witness
  C[r,t] intersect {m = 0} is empty  UNSAT proof

EXCLUDED:
  C[r,t] is nonempty                 SAT witness
  C[r,t] intersect {m = 1} is empty  UNSAT proof
```

All of those live certificates must have the same status, query artifact ID,
proof artifact ID, and verifier ID as the relevant manifest bindings.

`UNRESOLVED` is also evidence-bearing. It is retained only when the required
cells contain both:

```text
one manifest-bound SAT witness with m = 1
one manifest-bound SAT witness with m = 0
```

Otherwise it becomes `UNSUPPORTED`. This separates a demonstrated coexistence
of incompatible candidates from a failure to finish a solver query.

## End-to-end gate

Use `verify_and_audit_anytime_symbolic_decisions` for the strict workflow:

1. verify the manifest target against live candidate-space and certificate data;
2. verify every supplied artifact payload against its SHA-256 commitment; and
3. audit each symbolic snapshot's source status against required bindings.

The output records both the source status and the audited status. A downgrade is
not evidence that the source conclusion is false. It says the submitted
artifact bundle is incomplete for a certificate-backed claim.

## Trust boundary

This layer does not establish statistical coverage, solver semantics, or the
scientific adequacy of a candidate space. It composes existing layers:

```text
coverage certificate       establishes alpha
solver proof/verifier      establishes beta or beta = 0
manifest                   binds artifacts to one target
decision audit             checks that each displayed conclusion uses its bindings
```

The anytime symbolic false-decisive bound remains unchanged:

\[
P(\text{any false decisive conclusion}) \le \min(1, \alpha + \beta).
\]

The audit prevents an incomplete artifact record from being presented as a
certificate-complete decisive or unresolved result. It does not alter the
mathematical assumptions behind alpha or beta.
