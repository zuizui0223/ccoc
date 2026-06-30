# Proof-carrying polyhedral motif-query compiler

## Problem closed by this layer

The exact rational linear verifier proves that a supplied system is feasible or
infeasible. By itself it cannot know whether a caller's three systems really
mean

\[
C,
\qquad
C\cap\{m=1\},
\qquad
C\cap\{m=0\}.
\]

A malformed or adversarial query encoder could attach a valid Farkas proof to an
unrelated inactive system and thereby manufacture an invalid `INVARIANT`
conclusion. This is not a solver error; it is a motif-encoding error.

This module removes that manual active/inactive encoding step for a restricted
but expressive universe class.

## Declared universe: a finite tagged polyhedral union

The declared candidate universe is **defined** as

\[
\Theta=\bigcup_{j=1}^{J}U_j,
\]

where each \(U_j\) is a rational polyhedron and every cell carries one Boolean
value for every motif:

\[
v_j(m)\in\{0,1\}.
\]

For motif \(m\), define

\[
M_m=\bigcup_{j:v_j(m)=1}U_j,
\qquad
\Theta\setminus M_m
=\bigcup_{j:v_j(m)=0}U_j.
\]

The complement equality is not assumed from prose. Whenever two cells give any
motif different values, the partition must include an exact Farkas certificate
that their overlap is empty:

\[
U_j\cap U_k=\varnothing.
\]

Therefore a point in the declared union cannot receive contradictory motif tags.
Exhaustiveness requires no further geometric proof because the candidate universe
is, by definition, the union of the submitted cells. The external coverage claim
must of course concern this declared union.

Overlapping cells with identical tag vectors are allowed: they do not make any
motif ambiguous.

## Compiler output

For a retained rational polyhedron \(C\), the compiler creates only systems of
the form

\[
C\cap U_j.
\]

It then creates finite query families:

\[
\begin{aligned}
Q_{\mathrm{nonempty}} &= \{C\cap U_j\}_{j=1}^J,\\
Q_{\mathrm{active},m} &= \{C\cap U_j: v_j(m)=1\},\\
Q_{\mathrm{inactive},m} &= \{C\cap U_j: v_j(m)=0\}.
\end{aligned}
\]

No caller supplies an arbitrary active or inactive system. The only external
input after compilation is one `LinearFeasibilityProof` per generated branch ID.
The system, variable order, tag, role, and query ID are reconstructed from the
compiler plan before exact verification.

## Exact finite-union aggregation

For any finite family of branch sets \(B_1,\ldots,B_K\),

\[
\bigcup_{k=1}^K B_k=\varnothing
\quad\Longleftrightarrow\quad
\forall k,\;B_k=\varnothing.
\]

The compiler therefore returns:

- `SAT` if any exact branch witness is feasible;
- `UNSAT` if every branch has an exact Farkas infeasibility certificate;
- `UNKNOWN` when no witness exists and at least one branch is unknown.

A role with no tagged cells is structurally `UNSAT`, because the union over an
empty index family is empty. This is a compiler proof, not a hand-written
inactive query.

The resulting `SymbolicMotifQueries` satisfy the intended meaning exactly over
the declared polyhedral union:

\[
\begin{aligned}
\text{nonempty} &\iff C\cap\Theta\neq\varnothing,\\
\text{active} &\iff C\cap M_m\neq\varnothing,\\
\text{inactive} &\iff C\cap(\Theta\setminus M_m)\neq\varnothing.
\end{aligned}
\]

Thus, conditional on exact rational proof verification and the declared union
semantics, the `active` / `inactive` complement relation is no longer an
unverified caller assertion.

## Manifest binding

Two artifacts are available for the existing manifest layer:

1. `polyhedral_motif_partition_artifact` commits the tagged cells and every
   conflict-separation proof.
2. `compiled_polyhedral_motif_plan_artifact` commits every generated branch
   system and its role.

A manifest's existing single `(look, cell, motif, role)` proof-artifact slot can
bind a full branch family through
`compiled_role_proof_bundle_artifact`. That artifact contains every branch
system and proof used by the role, so no branch can be silently omitted or
replaced after the manifest commitment.

## Important scope boundaries

This is not a generic compiler for arbitrary Boolean formulas over arbitrary
continuous linear systems. The complement of a general polyhedral conjunction is
usually a union involving strict inequalities, so pretending it is one
non-strict conjunction would be unsound.

The supported language is deliberately narrower:

- finite union of rational, non-strict, conjunction-only polyhedral cells;
- a total Boolean tag vector attached to every declared cell;
- exact UNSAT separation for every pair with incompatible tags;
- a rational conjunction-only retained system; and
- exact witness / Farkas verification for every generated branch.

The compiler does not establish statistical coverage, prove that the declared
union captures nature, infer semantic motif tags from data, support nonlinear or
integer constraints, or prove that a caller uses the compiler rather than an
older manual-query path.

## Relation to the all-look exact admission layer

This PR closes the semantic gap at the `SymbolicMotifQueries` level. The current
all-look #19 admission gate still accepts one conjunction-only retained system
per inner/outer cell. A future extension can lift its retained representation
from one polyhedron to a finite compiler-generated union and apply the same
base-row / fixed-outer admission rule branchwise.

Until then, the strongest end-to-end `beta=gamma=0` all-look path remains the
single-polyhedron backend. The compiler gives a stronger semantic query contract
for finite-union symbolic cells and provides manifest-bindable artifacts for the
next admission-layer lift.

## API

| Task | API |
|---|---|
| Declare one tagged region | `TaggedPolyhedralCell` |
| Prove conflicting cells do not overlap | `ConflictingCellOverlapProof` |
| Declare / verify a tagged union | `PolyhedralMotifPartition`, `verify_polyhedral_motif_partition` |
| Compile branch query systems | `compile_polyhedral_motif_query_plan` |
| Bind external proofs without accepting systems | `bind_compiled_polyhedral_motif_proofs` |
| Verify and aggregate branch proofs | `verify_compiled_polyhedral_motif_proofs` |
| Convert to normal RACH symbolic cell | `compiled_polyhedral_motif_symbolic_cell` |
| Bind partition, plan, or role proof family in a manifest | `polyhedral_motif_partition_artifact`, `compiled_polyhedral_motif_plan_artifact`, `compiled_role_proof_bundle_artifact` |
