# Exact rational linear proof verifier

## Purpose

The symbolic candidate-set layer permits arbitrary solver-backed feasibility
queries, but it intentionally does not trust a bare solver label. This module
implements the first concrete **proof-carrying** backend for RACH:

- candidate sets are finite conjunctions of rational linear inequalities;
- `SAT` is accepted only with an exact rational witness; and
- `UNSAT` is accepted only with an exact Farkas infeasibility certificate.

The module performs no optimisation search and reads no empirical data. It is a
small trusted checker placed between an external LP/SMT/constraint backend and
the generic symbolic RACH layer.

## Linear representation

A system represents

\[
A x \le b,
\]

where all entries of \(A\), \(b\), and any witness are Python
`fractions.Fraction` values. Integer and string literals such as `"-1/5"` are
converted exactly. Binary floating-point literals are rejected rather than
quietly interpreted as exact rationals.

Equalities must be encoded as two inequalities. Strict inequalities are not in
this first adapter; use a separate encoded margin, a verified transformation, or
an `UNKNOWN` result. A motif-active and motif-inactive query must be supplied
explicitly by the caller. The adapter verifies those linear systems, but it does
not infer whether they partition a scientific mechanism space correctly.

## SAT witnesses

For a query \(A x\le b\), a `SAT` proof contains a rational point
\(x_0\). The verifier checks each row exactly:

\[
a_i^\top x_0\le b_i.
\]

A purported witness that violates even one inequality is rejected. It is not
silently downgraded to `UNKNOWN`, because a malformed proof artifact is a
pipeline error rather than an absence of information.

## UNSAT certificates: Farkas lemma

For the same system, an `UNSAT` proof contains non-negative multipliers
\(\lambda\ge0\) satisfying

\[
\lambda^\top A = 0,
\qquad
\lambda^\top b < 0.
\]

Multiplying every row by its non-negative multiplier and summing gives

\[
0 = (\lambda^\top A)x \le \lambda^\top b < 0,
\]

which is impossible. The verifier checks the multiplier sign, every coefficient
of \(\lambda^\top A\), and the strict negativity of \(\lambda^\top b\) using
exact rational arithmetic.

### Minimal example

The retained set contains \(x\ge1/5\), and the inactive query adds
\(x\le0\):

\[
-x\le-1/5,
\qquad
x\le0.
\]

With multipliers \((1,1)\), the left-hand coefficients cancel and the bounds
sum to \(-1/5\). Therefore the inactive query is certified `UNSAT`; the motif
is `INVARIANT` in that cell if the retained and active queries are also
certified non-empty.

Run the executable version:

```bash
python examples/linear_proof_verifier.py
```

## Connection to symbolic RACH

A `LinearMotifQueryBundle` contains three independently verified systems:

```text
nonempty  retained set C
active    C intersect motif-active region
inactive  C intersect motif-inactive region
```

`linear_bundles_to_symbolic_cell` converts only verified results into the
existing `SymbolicMotifQueries` interface. The generic symbolic rule then
applies unchanged:

```text
inactive UNSAT + nonempty SAT  -> INVARIANT
active UNSAT + nonempty SAT    -> EXCLUDED
active SAT and inactive SAT    -> UNRESOLVED
any needed UNKNOWN             -> UNSUPPORTED
```

## Trust boundary and beta = 0

Conditional on all of the following,

1. the exact rational parser and verifier implementation are trusted;
2. the external query encoding faithfully represents the intended retained and
   motif-restricted sets; and
3. the provided witness / Farkas artifact is the one actually verified,

the proof checker is deterministic. It can therefore support the symbolic
lifting theorem with solver semantic error \(\beta=0\).

This is not a claim that the external search procedure never fails. A search
backend may return `UNKNOWN`, may fail to find an existing witness, or may
provide no certificate. RACH treats that as `UNSUPPORTED`, not as `UNSAT`.
Approximate numerical methods with unverifiable rounding should use an external
solver-validity certificate with an explicit nonzero \(\beta\), or should not
support decisive RACH conclusions.

## Scope limits

This adapter handles only rational, non-strict, conjunction-only linear systems.
It does not yet implement:

- an LP solver or proof generator;
- strict linear inequalities;
- disjunctions or mixed-integer branching;
- nonlinear or semialgebraic constraints;
- solver-proof file formats; or
- a universal semantic check that active/inactive query systems exactly encode a
  motif complement.

Those are separate extensions. The present contribution is intentionally small:
a concrete, exact, auditable way to turn a valid linear witness or Farkas proof
into a RACH feasibility certificate.
