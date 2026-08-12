# Cross-grammar quantitative prior-art boundary — 2026-08-12

> **Purpose.** This memo isolates the prior-art gate for the manuscript's Tier A
> claim: the exact response-interface gap caused by enlarging a declared future
> grammar. It distinguishes three ideas that must not be conflated:
>
> 1. context/input restriction can reduce a minimum finite-state model;
> 2. a small change in a partial/don't-care representation can cause exponential
>    state cost;
> 3. CCOC's specific same-system comparison of exact response quotients under two
>    nested legal future grammars.
>
> The first two have strong prior art. The third remains the narrower manuscript
> candidate. This is a negative-search/claim-control result, not proof of priority.

## 1. Context-restricted exact minimization is classical

Larrauri & Bloem (2021), *Minimization and Synthesis of the Tail in Sequential
Compositions of Mealy Machines* (`arXiv:2105.10292`), formulate a cascade of two
Mealy machines `H` and `T`. For tail minimization the replacement only needs to
match the tail on the input sequences that the fixed head can actually produce.
Their paper explicitly places this problem in the lineage of Kim & Newborn (1972)
and incompletely specified Mealy-machine minimization.

This is already enough to prohibit the broad novelty claim

> “a machine/component may have a smaller exact state description when its legal
> input context is restricted.”

That is substrate.

Larrauri & Bloem also show exponential phenomena in the related synthesis problem:
a suitable missing tail can require exponential size even though existence is
polynomial-time decidable. This is not the same theorem as CCOC's restricted→open
response quotient, but it is another reason that “exponential finite-state growth”
by itself cannot carry novelty.

## 2. One small don't-care/partial-automaton change can already have exponential cost

A closer quantitative warning comes from **partial-word finite automata**.

Kutrib & Wendlandt's 2021/2025 work, *State Complexity of Partial Word Finite
Automata*, studies deterministic finite automata with a special `diamond` input
transition representing an unknown symbol / hole. The represented regular
language is obtained by substituting ordinary symbols for `diamond`, which gives a
restricted form of nondeterministic choice after substitution.

Their state-complexity hierarchy is organized by the number of productive
`diamond` transitions. For general regular languages, adjacent hierarchy levels
are separated by **exponential state costs**. The later finite-language paper
explicitly contrasts its quadratic finite-language hierarchy with the known
regular-language fact that even reducing one productive `diamond` transition can
cause exponential state explosion.

Therefore the following slogan is unsafe:

> “Changing only one admissible/unspecified transition can force an exponential
> increase in finite-state memory.”

A mathematically nearby automata model already has that phenomenon.

### Important non-equivalence

This does **not** directly subsume CCOC.

A partial-word DFA changes the automaton representation by using a wildcard-like
`diamond` transition whose substitution induces limited nondeterminism. CCOC keeps:

- one finite deterministic controlled system fixed;
- the same underlying state space and transition table fixed;
- the observation/output map fixed;
- the implementation hardware fixed in the explicit witness;

and changes only which future control words are declared legal in the response
grammar. The quotient change is therefore a change in the **observer / legal future
test family on one deterministic system**, not a conversion between a wildcard
partial automaton and an ordinary DFA.

That distinction is the relevant Tier A boundary.

## 3. What remains potentially manuscript-worthy

The safest remaining exact claim is not

- context-dependent minimization;
- exponential state blow-up;
- one-specification-change blow-up;
- ordinary pair distinguishability;
- common-refinement counting.

It is the following combined contract.

### Same-system nested-grammar comparison

A single deterministic controlled system `M` is evaluated under declared grammars

`L_closed,j ⊂ L_open`.

The exact interface is the response quotient induced by legal future traces. The
open lower bound is proved operationally: declared legal decoder words separate a
jointly realizable codebook/product of latent exterior coordinates.

For each fixed closed grammar a supplied exact factorization gives a small upper
bound. Under the open grammar, future addressability gives a large lower bound.

Thus the theorem compares **compression under different legal future test
families without changing the plant/system being compressed**.

### Quantitative extremal witness

The explicit one-action family further fixes one hardware family and has:

- every fixed closed context small;
- the union of closed response words still small;
- only one primitive action type newly legalized;
- the open response quotient discrete on the finite comparison domain;
- maximum finite-domain open-only innovation;
- a constrained local realization.

The novelty candidate is the exact cross-grammar formulation plus this unusually
clean extremal witness—not the generic existence of an exponential state tradeoff.

## 4. Direct-match search verdict

The literature pass has **not yet identified a directly stated theorem** with all
of the following simultaneously:

1. one fixed deterministic controlled system / transducer;
2. nested legal future-word grammars on that same system;
3. `O(1)` exact quotient/factorization in every declared fixed closed context;
4. a common/open grammar whose exact response quotient grows exponentially or by
   an additive `Omega(m)` number of bits;
5. a proof written as operational coordinate/codebook addressability rather than a
   representation conversion;
6. the explicit same-hardware one-new-action sharpness package.

This is a **search status**, not a theorem that no such result exists. The
manuscript must therefore avoid “first exponential blow-up” language and state its
novelty at the level of the precise cross-grammar contract.

## 5. Claim language after this audit

### Allowed

> Exact finite-state minimization under restricted input contexts and exponential
> state trade-offs in nearby partial/don't-care automata models are classical. We
> instead compare exact response interfaces of one fixed deterministic controlled
> system under nested legal future grammars. Under explicit operational
> addressability, every fixed closed context can admit a small exact interface
> while the declared open grammar forces additive exterior information to be
> retained. An explicit one-action local family attains the extremal finite-domain
> gap.

### Not allowed

- “We discover that input restrictions permit smaller finite-state machines.”
- “We give the first exponential blow-up caused by removing a don't-care or
  relaxing one specification constraint.”
- “Exponential state growth after a one-step specification change is new.”
- “No prior automata theory studies contextual state complexity.”

## 6. Remaining falsification target

The most dangerous still-unresolved result would be an old or modern theorem on
**promise/input-restricted Mealy machines** that already gives a worst-case family
on one fixed underlying transition system where expanding the allowed input-word
language from several small contexts to their open union forces the same exact
minimal quotient growth.

That is now the right search target. Broad searches for incomplete FSMs,
don't-cares, or state complexity are no longer informative enough.

## 7. Sources

Primary / publisher sources used for this boundary:

- Alberto Larrauri & Roderick Bloem (2021), *Minimization and Synthesis of the Tail
  in Sequential Compositions of Mealy Machines*, arXiv:2105.10292:
  <https://arxiv.org/abs/2105.10292>
- Martin Kutrib & Matthias Wendlandt (2021), *State Complexity of Partial Word
  Finite Automata*, DCFS 2021, LNCS 13037, pp. 113–124,
  DOI `10.1007/978-3-030-93489-7_10`.
- Martin Kutrib & Matthias Wendlandt (2025), *State Complexity of Partial Word
  Finite Automata*, International Journal of Foundations of Computer Science,
  DOI `10.1142/S0129054124420085`.
- Martin Kutrib & Matthias Wendlandt (2023), *State complexity of finite partial
  languages*, Theoretical Computer Science 966–967:114001,
  DOI `10.1016/j.tcs.2023.114001`.

The partial-word model is cited as a nearby quantitative warning, not presented as
an equivalent formulation of CCOC.