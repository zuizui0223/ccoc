# Classical noncommutation and quotient substrate — 2026-08-13

> **Purpose.** Tighten the CCOC/RACH novelty boundary after the contextual-FSM
> audit. This memo distinguishes (i) classical state-reduction/composition
> noncommutation ancestry, (ii) the elementary quotient mathematics underlying the
> abstract cross-grammar bound, and (iii) the much narrower quantitative/local
> package that remains a possible contribution.

## Decision

Two more broad novelty formulations should be retired.

1. **Do not claim that noncommutation between state reduction/compression and
   realization/composition is new.** Hartmanis & Stearns (1962) explicitly study
   cases where reducing a sequential machine destroys realizations by smaller
   machines and makes the reduced machine harder to realize. Their abstract
   attributes the phenomenon to failures of distributive laws between partitions
   used for reduction and partitions used for realization.
2. **Do not claim novelty for the abstract fact that enlarging a legal future-test
   family refines an exact response quotient, or that a pair-separating codebook
   forces a large quotient.** That step is an elementary intersection-of-kernels /
   Myhill--Nerode-style distinguishability argument.

Neither observation says that the present constrained relay family was published
before. They remove novelty budget from the broad conceptual slogan and from the
bare inequality.

## 1. Historical noncommutation ancestry

Juris Hartmanis & Richard E. Stearns, *Some Dangers in State Reduction of
Sequential Machines*, Information and Control 5(3):252--260 (1962), states in its
publisher abstract that state reduction can destroy realizations of a sequential
machine from sets of smaller machines and thereby produce a machine that is harder
to realize. The abstract further says that the undesirable effects are closely
associated with failures of distributive laws between the partitions used for
state reduction and those used for realization.

This is not the same theorem as CCOC:

- Hartmanis--Stearns changes the structural realization/decomposition properties
  after state reduction;
- CCOC holds a deterministic controlled plant fixed and changes the declared legal
  future-response grammar used to define an exact interface;
- CCOC's current extremal witness measures exact response-class growth and then
  realizes it under a bounded-local controlled network contract.

Nevertheless the historical result is too close to the broad phrase
"compression and composition do not commute" for that phrase to carry a
firstness claim.

A still earlier classical line is Paull & Unger (1959), *Minimizing the Number of
States in Incompletely Specified Sequential Switching Functions*, which treats
minimum-state reduction when part of the sequential behavior is unspecified.
Later Kim--Newborn and interacting-FSM work makes environment/input-dependent
reduction explicit. Together these sources make contextual state reduction and
reduction/realization interaction mature historical territory.

## 2. The abstract CCOC quotient is an elementary response-kernel object

Fix a finite comparison domain `D`. For every declared legal future word `w`, let

\[
R_w:D\to Y_w
\]

be the complete response signature required by the interface contract (for
example output trace together with any declared legality information).

For a word family `L`, exact response equivalence is

\[
s\sim_L t
\iff
R_w(s)=R_w(t)\quad\text{for every }w\in L.
\]

Hence

\[
\boxed{
\sim_L=\bigcap_{w\in L}\ker R_w.
}
\]

This immediately gives the grammar-monotonicity statement. If

\[
L_1\subseteq L_2,
\]

then

\[
\sim_{L_2}\subseteq\sim_{L_1},
\]

so the `L_2` quotient is at least as fine as the `L_1` quotient.

Now let `C\subseteq D` be a finite codebook. If for every two distinct codewords
`s,t in C` there exists one allowed future word `w` such that

\[
R_w(s)\ne R_w(t),
\]

then the `L` quotient is discrete on `C`, and therefore

\[
\boxed{|Q_L|\ge |C|.}
\]

The coordinate-decoder version used by the CCOC addressable-codebook theorem is a
convenient sufficient way to establish this pair separation. The state-count
lower bound itself is therefore distinguishability substrate, not a novelty claim.

## 3. Why the closed/open gap is still useful but not firstness-bearing by itself

Suppose every closed grammar `L_j` admits a supplied small factorization on the
same comparison domain while the open grammar contains a pair-separating family
for a much larger codebook. Combining the closed upper bounds with the open
pair-separation lower bound yields the familiar closed/open gap.

Mathematically this is useful because it gives a clean operational contract for
CCOC. But after the historical and quotient audits, the manuscript should not
argue that the **existence** of such a gap, or the fact that grammar enlargement
can refine a quotient dramatically, is itself the new discovery.

In particular, the elementary centralized `fire` construction already shows that
one newly legal primitive action can expose many dormant distinctions once routing
words are available. Such a construction is naturally expressible in classical
input-don't-care / incompletely specified sequential-machine language. Its role in
CCOC is a seed witness, not a novelty-bearing theorem.

## 4. Remaining candidate: simultaneous extremal/local package

The residual benchmark is now deliberately narrow. On one family the current CCOC
relay has

\[
|P_j|=2\quad\forall j,
\qquad
|P_U|=2,
\qquad
|P_O|=2^{m+1},
\qquad
\iota_{\rm new}=m,
\]

with `iota_new=m` equal to the absolute finite-domain innovation capacity, while
simultaneously retaining:

- one newly legal primitive action type (`fire`);
- a fixed four-symbol primitive control alphabet;
- real address-routing dynamics already legal before opening;
- pairwise radius-one updates;
- maximum degree three;
- local state/message alphabets bounded independently of `m`;
- logarithmic causal access, and exact `2 log2(m)+2` query length in the declared
  selector-plus-return architecture.

No reviewed source has yet been shown to match this entire simultaneous package.
That remains a **negative search status**, not proof of priority.

The universal-compiler gate is therefore decisive. If a classical fixed-input
sequential-machine compiler satisfies the CCOC H1--H4 contract with comparable
resource overhead, even the existence of a bounded-local witness can be compiled
from the elementary centralized seed. The explicit relay would then remain a
particularly transparent extremal construction, but not a firstness-bearing
existence theorem.

## 5. Consequence for manuscript strategy

The first paper can still use the cross-grammar quotient theorem as its formal
language, because it makes the ecological/compositional question precise and gives
an auditable lower-bound contract. But the paper should separate **formalism** from
**novelty**:

- fixed-grammar quotients: substrate;
- contextual/input-restricted minimization: prior art;
- reduction/composition noncommutation as a broad phenomenon: prior art;
- pair-separating/codebook cardinality bound: substrate;
- one-new-action centralized blow-up: elementary witness;
- simultaneous extremal bounded-local construction: residual candidate pending
  H1--H4 and the remaining quantitative search.

If the residual construction is subsumed by classical compilation, the correct
next research move is not to defend the old slogan. It is to seek a genuinely new
necessity/converse result, a coupled resource tradeoff, or an ecological structural
theorem that derives addressability or finite-blanket conditions from a specified
composition class.

## Source-status discipline

Primary/publisher records used for this decision include Hartmanis--Stearns (1962)
and the longstanding incomplete-machine minimization lineage. The exact historical
relationship is one of ancestry, not theorem identity. No claim is made that
Hartmanis--Stearns proves the CCOC open-grammar bound or that Paull--Unger uses the
same response-interface definition.

This memo changes claim control only. It does not change any theorem code,
certificate, registry identifier, or replay contract.
