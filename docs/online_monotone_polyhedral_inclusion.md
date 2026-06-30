# Online monotone polyhedral inclusion schema

## Why this exists

The exact rational polyhedral verifier can prove

\[
P_{\mathrm{inner}}\subseteq P_{\mathrm{outer}}
\]

for one static comparison or a finite list of looks. A finite list cannot prove
inclusion at every future analysis time, so it cannot by itself set the all-look
inclusion error \(\gamma\) to zero.

This module supplies a restricted but genuine all-look proof schema. It applies
when the outer envelope is fixed and each sequential inner retained set only
**adds constraints** to one verified base inner polyhedron.

## Schema

For each required cell \(r\), first establish exactly

\[
P^{\mathrm{base}}_r\subseteq P^{\mathrm{outer}}_r.
\]

The base inclusion uses the exact rational Farkas row-implication verifier. At
look \(t\), submit systems only through the admission gate, which checks:

1. the current inner system uses the same ordered variables;
2. every base inequality remains as an exact row of the current inner system;
3. the outer system is identical to the fixed verified outer system, ignoring
   row order and descriptive labels; and
4. a supplied exact rational witness satisfies every current inner inequality.

The first two conditions imply

\[
P^{\mathrm{inner}}_{r,t}\subseteq P^{\mathrm{base}}_r,
\]

and the verified base proof supplies

\[
P^{\mathrm{base}}_r\subseteq P^{\mathrm{outer}}_r.
\]

Thus every admitted look has

\[
P^{\mathrm{inner}}_{r,t}
\subseteq P^{\mathrm{base}}_r
\subseteq P^{\mathrm{outer}}_r.
\]

The witness prevents an admitted inner set from being empty and therefore avoids
using vacuous inclusion as an extension-stability argument.

## All-look guarantee

The schema verifier is deterministic. Conditional on the trusted rational
parser, verifier implementation, and the fact that every presented look is
admitted through this gate, the inclusion relation holds at every admitted
positive integer look. It creates

```text
AnytimeJointSymbolicInclusionCertificate(
  lower_bound=1.0,
  certified_looks=None,
)
```

so the inclusion contribution is

\[
\gamma=0.
\]

Combined with a proof-carrying outer solver \((\beta=0)\) and a valid all-look
outer confidence sequence, the anytime outer-envelope theorem reduces to

\[
P(\text{false decisive outer conclusion or invalid stability at any admitted look})
\le\alpha.
\]

The word **admitted** matters. The verifier cannot prove that an external caller
will route every future inference through it. A bypassed or rejected look is
outside this schema's certificate scope and must not be presented as
extension-stable under the schema.

## Conservatism and scope

The schema intentionally accepts only a simple update pattern:

```text
fixed outer polyhedron
fixed base inner polyhedron
current inner = every base row + zero or more extra rows
```

It rejects a changed outer bound, a removed base row, variable-order drift, or a
current witness that violates the inner system. It does not try to solve whether
a changed arbitrary inner system logically implies the base system; that would
be a separate exact inclusion proof problem at the new look.

Supported systems remain rational, non-strict, conjunction-only linear
inequalities. Strict inequalities, unions/disjunctions, integer constraints,
nonlinear systems, and outer envelopes that themselves evolve require other
proof schemas.

## API

| Object | API |
|---|---|
| Fixed base-to-outer all-look target | `MonotonePolyhedralInclusionSchema` |
| Proposed current polyhedral state | `MonotonePolyhedralInclusionLook` |
| Verified schema and all-look certificate | `verify_monotone_polyhedral_inclusion_schema` |
| Exact per-look admission gate | `verify_monotone_polyhedral_inclusion_look` |
| Method ID | `EXACT_MONOTONE_POLYHEDRAL_INCLUSION_SCHEMA_VERIFIER` |
