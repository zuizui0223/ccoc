# Research priorities: current conclusions and remaining goals

> **Status date:** 2026-08-13. This file is the canonical active agenda after the
> post-reopening CORE-2/CORE-3 strengthening pass. It replaces the earlier agenda
> in which weakening the product assumption, building constrained codebooks, and
> removing the growing primitive-port alphabet were still future work.

## Governing rule

RACH/CCOC is an active theorem-development repository. The July 2026 paper-core
freeze remains a reproducibility checkpoint, not the current mathematical state.
New work must occur on a branch and enter `main` through pull request.

The first-paper conceptual spine is still deliberately small:

\[
\text{exact grammar-aware interface}
\; + \;
\text{cross-grammar extension--compression obstruction}
\; + \;
\text{sharp constrained realization}
\; + \;
\text{conservative portability boundary}.
\]

Post-reopening results strengthen that spine; they do not create a new list of
headline theorems.

RACH remains mathematical ecology on supplied finite formal models. It contains
no empirical ecological validation, field inference, fitted biological
parameters, or automatic discovery of the correct open-composition grammar.

## 1. What is now established

### 1.1 Exact finite interface substrate

For a supplied finite deterministic controlled system and a declared legal future
grammar, the exact interface is the coarsest response quotient preserving current
output, legal-action rows, and successor labels.

This is fixed-grammar minimization substrate, not the novelty claim.

### 1.2 The product premise has already been weakened

`CORE-2` now has an arbitrary finite **addressable codebook** strengthening. For a
jointly realizable codebook

\[
C\subseteq A_0\times\cdots\times A_q,
\]

if declared legal future words uniformly recover the relevant coordinates, the
open response quotient is discrete on that comparison domain:

\[
\boxed{K_{\mathrm{open}}(D_C)=\log_2|C|.}
\]

If closed context `j` factors on the same domain through its retained coordinate
projection, then

\[
K_{\mathrm{closed},j}(D_C)\le \log_2|\pi_j(C)|,
\]

so

\[
\boxed{
K_{\mathrm{open}}(D_C)-\max_j K_{\mathrm{closed},j}(D_C)
\ge
\log_2|C|-\max_j\log_2|\pi_j(C)|.
}
\]

The historical full Cartesian product theorem is a special case. Constrained
families therefore no longer sit outside the theorem.

Implemented examples include parity and fixed-richness codebooks. At fixed
richness `k`, the exact restricted-domain gap is

\[
\Delta_{m,k}=\log_2\binom{m}{k}-1,
\]

so for `k` proportional to `m` the gap remains linear up to the usual logarithmic
correction. Full independence is therefore sufficient but not necessary for
large cross-grammar inflation.

### 1.3 The static and dynamic sources of inflation are separated

For the delimited class where the open grammar is the union of closed grammars,
the exact open quotient is the common refinement of the closed response
quotients. With a shared base partition and fibered join capacity `C`, the
realizability defect is

\[
\delta_{\mathrm{join}}
=
\log_2 C-\log_2|P_U|\ge0.
\]

When the actual open grammar contains genuinely new future words, define

\[
\iota_{\mathrm{new}}
=
\log_2|P_O|-\log_2|P_U|\ge0.
\]

The exact accounting is

\[
\boxed{
\Delta_{\mathrm{total}}
=
\Delta_{\mathrm{capacity}}
-
\delta_{\mathrm{join}}
+
\iota_{\mathrm{new}}.
}
\]

The first two terms have natural-join/common-refinement ancestry. The manuscript
novelty budget therefore belongs, if anywhere, to the same-system **cross-grammar
response comparison** and the dynamic `iota_new` realization, not to the algebraic
identity itself.

### 1.4 One newly legal primitive action can realize the absolute maximum innovation

The strengthened binary relay uses one fixed primitive action alphabet

\[
\{0,1,\mathsf{fire},\mathsf{tick}\}.
\]

Every fixed closed grammar already permits real address routing and `tick`; only
`fire` is withheld. Thus the closed dynamics are not an identity construction.
The closed union still has only the focal bit:

\[
|P_U|=2.
\]

Opening legalizes only `fire`. Address words can then reveal every dormant leaf
bit, so on

\[
D_m=\{0,1\}^{m+1}
\]

the open quotient is discrete:

\[
|P_O|=2^{m+1}.
\]

Hence

\[
\boxed{\iota_{\mathrm{new}}=m.}
\]

This saturates the finite-domain upper bound

\[
\iota_{\mathrm{new}}
\le
\log_2|D_m|-\log_2|P_U|=m.
\]

The construction simultaneously retains maximum degree three, pairwise
radius-one dynamics, a constant local node/message grammar, and the fixed
four-symbol global control alphabet.

### 1.5 The locality statement has been split into its correct two levels

For the explicit balanced selector-plus-return-path architecture,

\[
\boxed{
L_{\mathrm{query}}^{\mathrm{worst}}
=
2\log_2 m+2
}
\]

for powers of two, with zero slack against the architecture-specific lower bound.

For the broader bounded-local class, radius-one causal propagation and bounded
local state imply a causal-cone capacity bound. With fixed maximum degree
`Delta>=3` and fixed local-state bound `q`, realizing

\[
2^{\Theta(m)}
\]

focal response classes requires

\[
\boxed{T=\Omega(\log m).}
\]

The relay is therefore order-optimal in the broader local class. Bounded degree
alone is not sufficient; the radius-one causal-propagation contract is essential.

### 1.6 The positive boundary is already present

A finite conservative macro schema remains exact when old macro meanings are
preserved and every newly legal action is uniform in availability and macro
successor inside each macro fiber. A new future word that separates two states
inside a proposed fiber is the corresponding local obstruction.

This is a sufficient positive portability boundary, not a necessity theorem.

### 1.7 The finite-evidence no-go is already a companion result

The delayed-addressability line has already been strengthened to the adaptive
statement: for every finite-depth adaptive policy, a delay-gated closed/open pair
can agree on the entire finite transcript and diverge later. Thus finite
transcript-only evidence cannot uniformly certify closure without an independent
horizon/completion-grammar contract.

This remains `ID-1`, outside the first-paper theorem spine.

### 1.8 Exactness is not purely a zero-error artifact

A post-reopening companion applies Fano's inequality to an approximately decoded
addressable codebook. For one exact inside bit and `m` binary exterior coordinates
with fixed average decoding error `epsilon<1/2`,

\[
\boxed{
K_{\mathrm{open}}^{(\varepsilon)}
\ge
1+m\bigl(1-h_2(\varepsilon)\bigr).
}
\]

This is a robustness result, not a new approximate-abstraction framework and not
part of `CORE-1`--`CORE-5`.

## 2. Current scientific conclusion

The strongest defensible conclusion is now narrower and cleaner than the original
intuition:

> Exact compression in each fixed closed response/composition grammar does not in
> general commute with opening the legal future grammar. A positive-rate family of
> jointly realizable future distinctions can force the exact interface to retain a
> correspondingly large amount of information, even when the same fixed system has
> tiny closed quotients. One newly legal primitive action can attain the absolute
> finite-domain maximum response innovation under a degree-three, pairwise,
> constant-local-state realization.

The conceptual novelty is **not** fixed-grammar minimization, ordinary
Myhill--Nerode distinguishability, common refinement, generic exponential state
blow-up, or generic locality.

## 3. Remaining goals before submission

### Priority A — finish the Tier-A cross-grammar novelty gate

The main unresolved falsification target is a theorem in old or modern
promise/input-restricted/incompletely specified machine theory that already gives
essentially the same **same-system nested-grammar** worst-case comparison:

- one fixed deterministic controlled transition system;
- small exact quotient in every restricted/closed legal future grammar;
- a much larger exact quotient after opening the legal input/future-word language;
- no representation conversion or resynthesis needed to obtain the gap.

Broad searches for contextual minimization, incomplete machines, don't-cares, or
exponential state complexity are no longer enough. The target must match the
cross-grammar contract closely enough to test Tier A directly.

See `docs/cross_grammar_quantitative_prior_art_2026-08-12.md` and issue #99.

### Priority B — finish the historical universal-compiler source gate

The relay remains a **constrained sharpness witness**, not a firstness-bearing
realization claim, until the closest classical compiler constructions are checked
against the corrected four-resource contract:

- **H1:** bounded local state and bounded connectivity;
- **H2:** one fixed context-independent external input encoding/distribution;
- **H3:** two-way response-trace faithfulness, with no spurious compiled
  distinctions on the embedded comparison domain;
- **H4:** explicit bounded source-step/network-round/output latency.

Ullman--Weiner (1969) now has primary-text OCR evidence for binary input, a fixed
module with delay, isomorphic realization language, and network-size-independent
input settling time. The remaining blocker is the construction text needed for
fan-out/degree, input distribution, formal output/isomorphism semantics, and exact
clock/latency accounting.

Do not re-open generic mirror searches; follow issue #137's acquisition stop rule
and issue #122's H1--H4 decision rule.

### Priority C — move from theorem archive to manuscript workspace

The theorem archive is mature enough for proof writing. The remaining publication
work is not another local inequality.

1. Create `zuizui0223/rach-open-composition-paper` (manual repository creation is
   tracked in issue #141).
2. Pin the exact CCOC source/replay provenance at transfer time.
3. Restate the codebook lower bound, one-action maximal-innovation witness,
   locality scope, and conservative portability criterion independently in LaTeX.
4. Build the four planned figures from declared synthetic models.
5. Convert the novelty audits into a page-checked Related Work section.
6. Keep the abstract/introduction within the Tier-A/Tier-B claim boundary.

Issue #99 remains the manuscript tracker.

### Priority D — resolve stale theorem-development trackers

Several older open issues describe goals that are now implemented and merged but
retain only CI/literature or naming checkboxes. Before the manuscript transfer,
reconcile those trackers against the current main branch so that completed
mathematics is not mistaken for unfinished theorem work. Do not keep theorem
issues open merely because the historical checklist predates the merged
strengthening.

## 4. Mathematical work worth doing after the submission gates

Do **not** add another defect, panel, robustness score, or nearby special-case
inequality. A new branch is justified only if it changes one of the following
questions materially.

### 4.1 A genuine converse / necessity theorem

Find a delimited cross-grammar model class in which open-interface inflation has a
nontrivial necessary-and-sufficient characterization not reducible to the
already-known common-refinement identity or ordinary fixed-grammar minimization.

The earlier zero-order codebook quantity

\[
\Delta_0(C)
=
\log_2|C|-\max_j\log_2|\pi_j(C)|
\]

is a useful sufficient lower-bound quantity, but it should not be promoted as a
necessary invariant without such a converse.

### 4.2 Approximate or stochastic **portability**, not only addressability

The Fano theorem shows that the lower-bound obstruction is robust to decoding
error. A genuinely stronger next result would characterize when one finite
approximate/stochastic macro schema remains portable as the legal composition
grammar expands, or prove an unavoidable memory/error tradeoff for that task.

### 4.3 A joint structural resource tradeoff

A new theorem is worthwhile if it couples response-interface inflation to a
resource not already inherited from classical coding/locality lemmas, for example
a sharp simultaneous tradeoff among memory, legal-control complexity, and causal
access under one explicit model class.

### 4.4 An ecological theorem rather than an ecological relabeling

The most valuable ecological extension would start from a mathematically specified
composition class—e.g. constrained colonization, dispersal, interaction-network,
or boundary-coupling rules—and **derive** an addressability lower bound or a finite
blanket upper bound from those ecological constraints. Merely renaming external
bits as species, mutualists, or colonists is not enough.

## 5. Explicit non-priorities

Until the submission gates above move materially, do not prioritize:

- another codebook special case;
- another partition defect or bookkeeping identity;
- more panel/reset/robustness variants;
- re-proving adaptive finite-evidence impossibility under a different toy policy;
- moving replacement/rewiring transport back from `zuizui0223/mltr`;
- empirical ecological inference inside this theorem repository.

## 6. Promotion rule

Every proposed new active result must identify exactly which canonical question it
changes:

\[
\text{exact interface},\qquad
\text{cross-grammar addressability obstruction},\qquad
\text{portable composition},\qquad
\text{or finite-evidence identifiability}.
\]

It must also state whether the change is a strict assumption weakening, stronger
conclusion, converse/necessity result, sharper constrained construction, or a new
model class. A nearby special case alone is not sufficient reason to expand the
theorem registry.
