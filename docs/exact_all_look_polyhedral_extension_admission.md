# Exact all-look polyhedral extension admission

## Goal

The anytime outer-envelope theorem has three failure terms:

\[
\alpha \quad\text{(outer statistical coverage)},
\qquad
\beta \quad\text{(outer solver semantics)},
\qquad
\gamma \quad\text{(inner-to-outer inclusion)}.
\]

PR #18 gives \(\gamma=0\) for admitted looks when an inner polyhedron retains
a verified base system and the outer polyhedron is fixed. This module supplies
the matching proof-carrying solver gate and binds both checks to the **same
inner/outer symbolic snapshot**. For all admitted looks, it makes

\[
\beta=\gamma=0.
\]

## One retained system per cell

A symbolic RACH cell has one retained candidate set and one active/inactive
restriction per motif. An ordinary collection of linear motif queries can
accidentally give different motifs different ``nonempty`` systems, thereby
combining conclusions about incompatible candidate sets.

`ExactLinearProofCell` forbids that. For every motif in a cell:

```text
nonempty query system = one identical rational linear system
```

with equality checked by ordered variable vocabulary plus a label-insensitive
multiset of exact inequality rows. Active and inactive systems may add their
own motif restriction rows, but their semantic relation to the shared nonempty
system remains an explicit query-encoding assumption.

Every nonempty query must be a verified exact `SAT` proof with a rational
witness. `SAT` and `UNSAT` active/inactive results are independently checked by
the existing exact rational linear verifier; `UNKNOWN` remains non-decisive.

## Paired admission at one look

At one proposed look, the gate:

1. verifies every inner and outer linear motif-query bundle;
2. extracts the shared inner and outer retained systems from each cell;
3. sends those exact systems and the verified inner witness to the PR #18
   monotone inclusion admission gate;
4. constructs the `SymbolicUniverseTier` objects only after both validations
   pass; and
5. returns a `SequentialSymbolicUniverseExtensionSnapshot` built from those
   admitted tiers.

For every required cell, this proves the concrete chain

\[
C^{\mathrm{inner}}_{r,t}
\subseteq
P^{\mathrm{base}}_r
\subseteq
P^{\mathrm{outer}}_r
=
C^{\mathrm{outer}}_{r,t}.
\]

The equality on the right is structural: the outer retained system used in all
motif query bundles must be the same fixed outer system used by the inclusion
schema.

## All-look certificates

`verify_exact_polyhedral_extension_admission_schema` returns two certificates,
both with all-positive-integer scope:

```text
AnytimeSolverSemanticValidityCertificate(lower_bound=1.0)
AnytimeJointSymbolicInclusionCertificate(lower_bound=1.0)
```

They apply only to snapshots produced by
`admit_exact_polyhedral_extension_look`. The all-look assumptions are not a
claim that arbitrary future caller-supplied tiers are safe; a bypassed or
rejected look is outside the gate and cannot use its \(\beta=\gamma=0\)
conclusion.

Combined with any valid outer confidence sequence,

\[
P(\text{false decisive outer conclusion or invalid extension stability}
  \text{ at any admitted look})
\le \alpha.
\]

This remains safe under data-dependent stopping because both proof-carrying
certificates have all-look scope and the statistical procedure supplies the
all-look coverage event.

## Boundaries

The construction is deliberately restrictive:

- rational, non-strict, conjunction-only linear systems;
- fixed outer polyhedron;
- inner systems retain every base inequality and may only add rows;
- every claimed look is passed through the admission gate;
- trusted exact parser, verifier implementation, and declared query encodings.

It does not search for witnesses or Farkas multipliers, infer motif semantics,
prove candidate-universe coverage, support nonlinear/integer/disjunctive
systems, or authenticate an external caller who might bypass admission.

## API

| Object | API |
|---|---|
| One exact motif-query cell | `ExactLinearProofCell` |
| Proposed paired inner/outer look | `ExactPolyhedralExtensionLook` |
| Fixed all-look admission target | `ExactPolyhedralExtensionAdmissionSchema` |
| Verified \(\beta=\gamma=0\) target | `verify_exact_polyhedral_extension_admission_schema` |
| Exact paired snapshot admission | `admit_exact_polyhedral_extension_look` |
