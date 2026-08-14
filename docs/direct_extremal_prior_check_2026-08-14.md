# Direct extremal prior-art check — 2026-08-14

> **Question:** after demoting generic automata minimization and generic exponential descriptional-complexity gaps, is there a direct antecedent for the specific CCOC extremal construction: same controlled plant, fixed primitive alphabet, one newly legal action, closed exact response quotient of size two, and discrete open quotient of size `2^(m+1)`?

This is a targeted closest-prior check, not a proof of historical absence.

## 1. Exponential automata blow-up is not novel

Descriptional-complexity theory contains many exponential and even larger succinctness gaps. Examples include exponential costs of regular-language operations for restricted automata and exponential changes induced by changing automaton representation or computational model.

Therefore CCOC must **not** claim novelty for:

- exponential state complexity;
- an exponentially more succinct restricted representation;
- exponential blow-up under determinization, complementation, concatenation, star, or other standard language operations;
- exponential complexity created by moving acceptance information between transitions and states.

Those are broad classical/modern descriptional-complexity themes.

## 2. Alphabet restriction and partial-machine semantics are also standard

Modern partial-Mealy-machine literature explicitly uses restriction notation such as restricting a machine to a subset of its input alphabet. Input restrictions and incompletely specified sequential machines are also classical topics.

Therefore CCOC must not claim that “restrict the input/action alphabet and later restore actions” is itself a new formal operation.

## 3. What was not found in the targeted check

The inspected closest-primary literature did not surface a theorem/construction with the following simultaneous contract:

1. **same deterministic controlled plant** before and after opening;
2. **same fixed primitive alphabet** independent of the hidden-state parameter;
3. closed versus open difference is only **legality of one primitive action / one grammar transition**;
4. closed legal future gives the canonical exact response quotient
   \[
   |P_C|=2;
   \]
5. open legal future gives the discrete quotient
   \[
   |P_O|=2^{m+1};
   \]
6. hence exact open-only innovation is exactly `m` bits and saturates finite-domain capacity;
7. the same witness is realized with bounded local state/message resources, degree three, cut width one, and explicit logarithmic selected access.

Search hits with exponential state complexity involved **different operations**: language operations, machine-model simulations, acceptance-structure transformations, or other changes to the represented language/system. Hits using alphabet restriction did not directly quantify the change in the **coarsest exact response equivalence on one unchanged plant** caused by expanding the declared legal future.

This does not establish firstness. It does sharpen what a direct counter-prior must contain.

## 4. The right comparison object

A prior result should count as a direct antecedent only if it matches the semantic object closely enough to reproduce the CCOC claim:

- state equivalence is induced by equality of declared observable response traces/counterfactuals;
- the micro-transition plant is fixed;
- the closed/open change is in admissible future controls/language rather than resynthesizing the plant;
- the state-complexity comparison is between the two canonical exact response interfaces;
- for the strongest local claim, the realization constraints are part of the same construction or follow from a verified compiler.

A theorem that merely shows an exponential minimal-DFA blow-up after another language operation is ancestry for descriptional complexity, not the same theorem.

## 5. Residual claim strengthened by this check

The strongest current first-paper wording remains:

> The contribution is not exponential automata complexity or action restriction in isolation. It is a fixed-plant, fixed-grammar-schema extremal response-interface separation under one-action legal-future expansion, together with an explicit constrained local equality witness.

A manuscript may say that the targeted audit did not identify a direct antecedent satisfying this simultaneous contract. It should not yet say “first”.

## 6. Sources / adjacent anchors inspected

The targeted check included:

- descriptional-complexity results with exponential lower bounds for regular-language operations and simulations of restricted automata;
- work comparing transition-based and state-based automata where representation conversion can incur exponential state blow-up;
- partial Mealy-machine work that explicitly treats restrictions to subalphabets;
- the existing CCOC classical sequential-machine input-restriction / incomplete-machine audit.

These sources strengthen the non-claims around generic exponential blow-up and alphabet restriction while leaving the simultaneous CCOC contract as the live residual candidate.

## 7. Stop rule

A future hit should demote the residual claim only when its theorem statement and construction are mapped explicitly to the seven-item contract above. Do not treat keyword overlap such as “alphabet extension”, “state complexity”, “input restriction”, or “bounded fan-out” as equivalence by itself.