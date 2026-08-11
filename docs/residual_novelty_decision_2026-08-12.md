# Residual CCOC novelty decision — 2026-08-12

> **Purpose.** Convert the August 2026 prior-art audit into a publication/research
> decision. This memo does not introduce a theorem. It states which claims are
> historical substrate, which are too risky to headline, and which residual claim
> is still worth carrying into a manuscript while the remaining primary sources
> are acquired.

## 1. Decision

### GO — carry the cross-grammar response-complexity theorem into the manuscript

The paper may continue to center the exact separation between:

- small exact interfaces under declared fixed closed composition grammars; and
- a much finer exact response interface under the declared open grammar.

The addressability/codebook proof gives a clean finite lower bound, and the
one-action relay gives an explicit extremal witness under strong implementation
constraints.

### CONDITIONAL GO — use the relay as sharpness, not as a firstness claim

The degree-three/fixed-control relay remains useful because it shows the response
separation is not merely an artifact of one centralized lookup table. But its
**historical realization novelty is unresolved**. Fixed-input uniform modular
realization, fixed modules with delay, repeated identical modules, bounded
fan-in/fan-out decompositions, and incomplete-specification synthesis all have
substantial classical ancestry.

Accordingly the relay belongs in the main paper as a sharpness/constrained
realization result, but not as the conceptual novelty headline and not with
“first” language.

### NO-GO — do not claim novelty for the fixed-grammar quotient machinery

Exact future-response quotients, minimization under a fixed observer/input family,
common refinement, and ordinary distinguishability are substrate adjacent to
Myhill–Nerode/transducer minimization, bisimulation/state abstraction,
input-restricted sequential-machine minimization, and regular-language/state-
complexity methods.

## 2. Current claim hierarchy

### Tier A — manuscript headline candidate

> **Compression under each fixed closed response grammar need not commute with
> opening the admissible response grammar.** Under a declared jointly realizable
> comparison family and operational future separation, the exact open interface
> can require much more memory than every fixed closed interface.

This should be sold as a **cross-grammar causal/interface statement with an exact
finite lower bound**, not as the invention of behavioral minimization.

### Tier B — strongest quantitative sharpening

On the current finite comparison family the one-action witness has:

\[
|P_U|=2,
\qquad
|P_O|=2^{m+1},
\qquad
\iota_{new}=m,
\]

so the newly legal response capacity saturates the finite-domain maximum.
Constrained codebooks show that large inflation persists without the full
Cartesian-product domain.

This is the cleanest quantitative result to emphasize after the theorem statement.
Generic pair distinguishability or the capacity identity itself is not a novelty
claim.

### Tier C — supporting realization theorem

The explicit relay simultaneously has:

- fixed primitive controls `{0,1,fire,tick}`;
- only `fire` newly legal in the open regime;
- closed routing dynamics already active;
- pairwise radius-one updates;
- maximum degree three;
- constant local node/message grammar;
- logarithmic addressed access.

This is an important **witness quality statement**. Historical priority for the
whole package is pending issue #122.

### Tier D — positive boundary

The conservative finite portability criterion should remain the constructive
counterpart: if outputs, legal-action rows, and successors factor coherently
through one finite schema as composition/action availability changes, exact
portability is retained.

This is a sufficient positive boundary, not a complete characterization of all
possible abstractions.

## 3. What the historical audit has already killed as standalone novelty

Do not headline any of the following:

1. contextual/input-restricted state minimization;
2. incomplete-specification state reduction;
3. exact behavioral quotient/minimal interface for one fixed grammar;
4. common refinement/product-capacity counting;
5. arbitrary sequential behavior realized by repeated identical modules;
6. bounded-fan-in/bounded-fan-out modular realization as a broad idea;
7. fixed-input uniform modular synthesis;
8. one fixed module with delay;
9. “one additional response word/action can distinguish previously merged states”;
10. the generic radius-`T` causal-cone/locality principle.

Several of these remain useful lemmas, proof substrates, or related-work anchors.
They are simply not where the manuscript should spend its novelty budget.

## 4. Remaining historical risk to Tier A

The current web/literature audit has **not found a directly stated classical
worst-case theorem matching the complete CCOC cross-grammar package**, but that is
a negative search result rather than proof of novelty.

The most dangerous possibility is that old input-restricted/incompletely specified
machine theory already contains, perhaps implicitly, a family with:

- `O(1)` minimum machine/interface under a restricted input/response regime;
- exponentially many distinguishable states after a tiny relaxation of the input
  specification; and
- a translation close enough to CCOC's same-state-space response quotient that the
  present lower bound becomes a repackaging.

Therefore the manuscript should avoid claims like “no previous theory shows a
large restricted-to-open state gap.” The defensible statement is narrower:

> we formulate and prove an exact cross-grammar response-interface lower bound
> under explicit operational separation assumptions, and give a constrained
> extremal realization; we do not claim the underlying phenomenon of
> context-dependent state reduction is new.

## 5. Remaining historical risk to Tier C

The local realization is at especially high risk from the classical modular
synthesis lineage:

- Hsieh–Tan–Newborn (1968): fixed-input uniform modular realization / unit-delay
  historical lead;
- Weiner–Hopcroft (1968): identical two-state modules with state-count-independent
  fan-in/fan-out in accessible abstract evidence;
- Ullman–Weiner (1969): binary-input machines, fixed module with delay, isomorphic
  realization in accessible abstract-style evidence;
- Newborn–Arnold (1972): bounded-signal-fanout universal modules;
- Williams (1975): incomplete specification plus uniform decomposition.

The decisive unresolved clauses remain:

- **C3:** exact external control/input distribution cost;
- **C5:** semantic source-step → local-network-round/output latency;
- **C6:** same hardware under restricted/open response grammars rather than
  recompilation.

If classical primary texts satisfy C1–C6 with comparable overhead, Tier C becomes
an explicit clean construction rather than a novel realization theorem.

## 6. Stop rule for further theorem proliferation

Until issue #122 or the cross-grammar quantitative literature gate materially
changes the verdict, do **not** add another theorem merely by defining a new defect,
panel, robustness score, or special-case inequality.

A new mathematical branch is justified only if it changes one of these questions:

1. **necessity/converse:** a nontrivial characterization not inherited from fixed-
   grammar minimization/common refinement;
2. **stronger model class:** stochastic, approximate, infinite, or otherwise beyond
   the present finite deterministic substrate with a genuinely nontrivial bound;
3. **joint structural tradeoff:** an exact lower bound that couples response
   inflation to a resource not already supplied by classical locality/coding
   lemmas;
4. **ecological theorem:** a mathematically specified ecological composition class
   whose constraints imply or preclude the addressability assumptions in a way
   that is not merely interpretive relabeling.

Otherwise the next work should be manuscript proof exposition and primary-source
verification, not theorem count.

## 7. Manuscript architecture implied by this decision

1. **Ecological/compositional question.** When can exact compression learned for
   fixed closed compositions be transported to an open composition grammar?
2. **Formal substrate.** Controlled response equivalence and exact interfaces,
   explicitly acknowledged as minimization substrate.
3. **Main theorem.** Cross-grammar addressability/codebook lower bound and
   extension–compression gap.
4. **Quantitative sharpness.** One-action maximal response innovation and
   constrained codebook families.
5. **Local realization.** Degree-three/fixed-control relay as an explicit sharp
   witness, with historical-priority caveat.
6. **Positive boundary.** Conservative finite portability.
7. **Related work.** Input restrictions/incomplete machines, automata quotients,
   causal/compositional abstraction, and classical modular sequential synthesis.
8. **Ecological interpretation.** Synthetic interpretation only; no empirical
   validation claim.

## 8. Publication go/no-go

### Ready now

- theorem/proof manuscript drafting under cautious novelty wording;
- figures explaining closed versus open response grammars and the sharp witness;
- reproducibility/traceability transfer from the theorem archive.

### Not ready

- firstness/priority language for the bounded-local relay;
- a final Related Work verdict on classical universal compilation;
- an empirical ecological claim;
- submission while the bibliography still misrepresents secondary historical
  evidence as primary proof.

### Hard blockers before submission

1. resolve as much of issue #122 as practical from primary sources;
2. explicitly compare the main cross-grammar quantitative claim against the
   closest input-restriction/incomplete-machine worst-case literature;
3. create/pin the separate manuscript repository and permanent theorem/replay
   provenance;
4. keep the final abstract and introduction within the Tier A/Tier B claim
   boundary above.

## 9. Bottom line

CCOC still has a coherent paper path, but the novelty center is **narrower than the
original intuition**:

> not “local systems suddenly need memory,” and not “a new action can cause a big
> machine,” but an explicitly quantified failure of fixed-composition exact
> compression to commute with opening the response/composition grammar, together
> with a particularly constrained extremal witness.

The historical audit should be allowed to demote the witness if necessary without
collapsing the manuscript's main structural question.