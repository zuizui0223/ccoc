# Reactive-environment equivalence prior — 2026-08-14

> **Purpose:** correct the novelty boundary after finding a close formal-semantics antecedent in which behavioral equivalence is explicitly indexed by the set of actions currently allowed by an environment. This further narrows, rather than weakens, the defensible CCOC contribution.

## 1. Close primary antecedent

Rob van Glabbeek, *Reactive bisimulation semantics for a process algebra with timeouts* (Acta Informatica, published online 2022; volume 60, 2023) studies labelled transition systems interacting synchronously with an environment.

The paper explicitly assumes:

- a visible action alphabet `A`;
- at any time the environment allows a subset `X ⊆ A` and blocks the other visible actions;
- the environment may change the allowed-action set at discrete moments;
- an observable action occurrence can trigger a change in the environment's allowed-action set.

Its strong `X`-bisimilarity requires matching visible transitions only for actions `a ∈ X`, because actions outside `X` cannot occur in that environment. The paper also develops a reactive bisimilarity robust to triggered changes in the allowed set.

This is a direct prior for **environment-relative behavioral equivalence under action blocking/allowing**.

## 2. Consequence for CCOC non-claims

CCOC must not claim firstness for any of the following broad ideas:

- behavioral equivalence depending on which visible actions an environment currently permits;
- environment-specific bisimulation/equivalence;
- an environment changing the set of enabled/allowed actions over time;
- blocked actions being irrelevant to equivalence in a context where they cannot occur;
- contextual/reactive semantics induced by an environment's action permissions.

Assume–guarantee verification and environment-assumption synthesis provide further broad ancestry for restricting environmental traces/moves.

Therefore the novelty ladder should **not** sell “legal-future-sensitive equivalence” as a wholly new semantic idea.

## 3. Remaining difference in object and question

The CCOC first-paper residual target is more specific and quantitative.

### 3.1 Declared future language, not only current allowed set

CCOC uses a finite grammar/automaton for legal future words. The semantic context can therefore encode history-dependent future legality, not merely one instantaneous subset `X` of visible actions.

This is an important modeling distinction, but regular/environment-history semantics is itself not enough for a firstness claim.

### 3.2 Canonical exact response interface and its cardinality

CCOC's central quantity is the **coarsest exact response quotient/interface for the declared legal future**, and especially how its size changes when the future grammar is opened.

The targeted inspection of reactive-bisimulation and assume–guarantee sources did not reveal a matching theorem whose main object is the closed-to-open change

\[
|P_C| \longrightarrow |P_O|
\]

or the corresponding exact interface-memory innovation under one fixed plant.

This is the first defensible residual distinction after accounting for the close semantic prior.

### 3.3 Extremal one-action separation

The explicit CCOC family proves

\[
|P_C|=2,
\qquad
|P_O|=2^{m+1},
\qquad
K_O-K_C=m,
\]

while opening exactly one primitive action in a fixed four-symbol grammar schema.

The open quotient is discrete on the finite semantic domain, so the separation saturates the available finite-domain memory capacity.

The targeted formal-semantics prior check found no direct antecedent giving this canonical-interface cardinality extremum under one-action legal-future opening of the same plant.

### 3.4 Same extremal family under explicit locality constraints

The CCOC witness additionally realizes the exact equality case with bounded local state/message alphabets, radius-one dynamics, maximum degree three, cut width one, and explicit logarithmic selected access.

Historical firstness of **bounded-local realization existence** is still controlled by H1–H4. The simultaneous constrained equality witness remains a separate construction comparison.

## 4. Revised claim ladder

### Level A — unconditional theorem statement

Safe:

> CCOC defines grammar-relative exact response interfaces and proves closed/open interface separation, a fixed-grammar one-action extremal family, and positive portability criteria.

### Level B — prior-aware framing

Replace any broad claim that context-sensitive equivalence is new with:

> CCOC focuses on the **quantitative portability of the canonical exact response interface** when the declared legal future language of a fixed controlled plant is enlarged.

This wording distinguishes the measured object without denying environment-relative equivalence prior art.

### Level C — targeted-audit residual construction claim

Currently defensible with `to our knowledge` / `in the inspected literature` qualification:

> The inspected literature does not provide the same one-action maximal closed/open canonical-interface separation together with the explicit degree-three, cut-one local realization.

### Level D — historical firstness

Still not established. H1–H4 decides whether bounded-local existence is already inherited from classical sequential-machine compilation; a direct constrained-witness comparison is additionally required before claiming “first such extremal construction”.

## 5. Why this is a useful correction

Finding reactive bisimulation removes a weak novelty argument and makes the stronger one clearer:

- **not:** equivalence depends on allowed actions;
- **not:** the environment may change allowed actions;
- **not:** action restriction/refinement exists;
- **but:** exact compression portability is quantified by the change in the canonical response-interface memory, and CCOC supplies a maximal one-action separation under simultaneous explicit locality constraints.

This is the novelty object to protect.

## 6. Primary adjacency anchors

- Rob van Glabbeek (2022/2023), *Reactive bisimulation semantics for a process algebra with timeouts*, Acta Informatica 60:11–57.
- Assume–guarantee/environment-assumption synthesis literature as broad ancestry for restricting environment moves/traces.
- Fecher & Huth (2008), *Model Checking for Action Abstraction*, as an additional action-extension/refinement adjacency anchor.

## 7. Stop rule

Do not treat reactive bisimulation as a direct counterexample to the CCOC extremal theorem unless a source also supplies the relevant canonical interface-size comparison or a construction that maps to the fixed-plant one-action extremal contract. Conversely, do not claim novelty for environment-relative equivalence now that this prior is explicit.