# Related Work — source-checked working draft

> Status: manuscript source file. This document deliberately separates established ancestry from the narrower CCOC comparison contract. It is not a priority claim.

## 1. Response equivalence and finite-state minimization

The response-interface formalism used in CCOC belongs to the broad family of continuation-based state equivalences. In the classical Myhill–Nerode viewpoint, two histories are equivalent when no admissible continuation distinguishes them, and the equivalence classes give the states of the minimum deterministic automaton. CCOC uses the same basic distinguishability logic for controlled response traces. For a declared legal future-word family `L`, its exact relation can be written as an intersection of response kernels,

\[
\sim_L=\bigcap_{w\in L}\ker R_w.
\]

Consequently, enlarging the legal future family can only refine the exact response quotient, and a pair-separating set of future words forces distinct response classes. These facts are mathematical substrate, not claimed contributions of CCOC.

The role of the formalism here is instead to make the ecological comparison explicit: the controlled plant is held fixed while the contract specifying which future words must be preserved is changed.

## 2. Incompletely specified machines and input-dependent minimization

Context-dependent state reduction long predates CCOC. Paull and Unger (1959) studied state minimization for incompletely specified sequential switching functions, where unspecified entries change which distinctions must be preserved. Their problem is not the same as the present closed/open response comparison, but it establishes that state reduction under a restricted behavioral specification is classical territory.

A later line on interacting finite-state-machine networks makes environmental restrictions even more explicit. Wang and Brayton (1993) describe input-don't-care sequences for a component embedded in an FSM network and state that the Kim–Newborn procedure exactly computes such sequences for the driven machine in a cascade. The surrounding network therefore constrains the input sequences relevant to minimizing a component. Aziz, Singhal, Swamy and Brayton (1993) likewise minimize interacting FSMs using equivalence relations that exploit behavior redundant with respect to the verification context, while avoiding direct construction of an enormous product machine. Watanabe and Brayton (1993) formulate the related problem of the complete set of component behaviors permissible while preserving total-system behavior.

These lines mean that CCOC should not claim that an environment, input restriction, or surrounding composition can make a component more compressible. The distinction sought here is narrower: one fixed controlled system is evaluated under explicitly nested legal future grammars, and the quantity of interest is the change in its canonical exact response-interface size.

## 3. State reduction versus realization and composition

The broad slogan that compression and composition need not commute is also classical. Hartmanis and Stearns (1962) showed that state reduction can destroy realizations of a sequential machine by sets of smaller machines and can thereby make the reduced machine harder to realize. They associated these effects with failures of distributive laws among the partitions used for reduction and realization.

Their theorem is not the CCOC theorem. Hartmanis–Stearns asks how reducing a sequential machine changes structural realizability. CCOC keeps the controlled plant fixed and changes the legal future-response grammar that defines exact equivalence. Nevertheless, the historical result is close enough that `compression and composition do not commute` cannot carry a firstness claim here.

Accordingly, the manuscript uses noncommutation only as intuition. The formal object reported by CCOC is the closed-to-open change in exact response classes under a declared grammar change.

## 4. Interacting-machine and permissible-behavior methods

The 1990s FSM-network literature further weakens any claim that composition-aware reduction is new. Wang and Brayton's input-don't-care work computes sequences that a component need not distinguish because of restrictions imposed by the rest of the network. Aziz et al. treat interacting-machine minimization hierarchically, and Watanabe and Brayton represent the complete set of component behaviors compatible with preservation of total-system behavior by an `E-machine` obtained through a fixed-point computation.

These methods and CCOC share a concern with which external behaviors are relevant to a component. Their optimization objective, representation, and system contract differ from CCOC's exact response quotient under nested legal future grammars. The manuscript therefore treats them as direct conceptual ancestry rather than as instances of the same theorem.

## 5. What remains specific to the CCOC comparison

After removing the classical substrate above, the first-paper comparison is deliberately narrow. The main explicit family simultaneously has

\[
|P_C|=2,
\qquad
|P_O|=2^{m+1},
\qquad
K_O-K_C=m,
\]

while the controlled plant is unchanged and opening adds only one primitive legal action. The same family uses a fixed four-symbol action alphabet, bounded local state and message alphabets, pairwise radius-one dynamics, maximum degree three, a one-edge focal/exterior cut, and logarithmic causal access.

The manuscript does **not** require a historical-firstness claim for bounded-local compilation. The relay is used as an explicit constrained extremal witness: it demonstrates directly that the maximum finite-domain response-memory increase is compatible with uniformly simple local implementation. Classical universal or modular sequential-machine synthesis may provide related implementation machinery; that history affects attribution of the realization technique, not the validity of the closed/open response calculation.

The safest contribution statement is therefore quantitative and contract-specific:

> We give an explicit fixed-plant family in which a minimal enlargement of the legal future grammar changes the canonical exact response interface from two classes to a discrete `2^(m+1)`-state quotient, attaining the maximum possible `m`-bit increase on the comparison domain, and we realize that equality under bounded-local structural constraints.

This wording does not claim that contextual minimization, continuation equivalence, pair separation, noncommutation, or modular realization is new in isolation.

## 6. Relation to ecological abstraction

The automata literature establishes why the mathematical ingredients should be treated conservatively. The ecological use of CCOC is to expose a state-choice question that those ingredients make precise: whether a coarse ecological state chosen under one set of admissible future interactions remains exact when colonization, reconnection, dispersal access, or rewiring enlarges that future contract.

The theorem does not infer those ecological grammars from observations. It says that once a contract is declared, future addressability can be separated from local-rule complexity as a source of exact state information. Empirical justification of the contract is therefore logically prior to applying the theorem to a real system.

## References verified in this pass

- Hartmanis, J. & Stearns, R. E. (1962). *Some Dangers in State Reduction of Sequential Machines*. Information and Control 5(3):252–260. DOI: 10.1016/S0019-9958(62)90588-0. Publisher abstract directly supports the state-reduction/realization noncommutation ancestry used above.
- Paull, M. C. & Unger, S. H. (1959). *Minimizing the Number of States in Incompletely Specified Sequential Switching Functions*. IRE Transactions on Electronic Computers EC-8(3):356–367. DOI: 10.1109/TEC.1959.5222697. Bibliographic record and abstract support the incomplete-specification minimization ancestry.
- Wang, H.-Y. & Brayton, R. K. (1993). *Input Don't Care Sequences in FSM Networks*. UCB/ERL M93/64. Berkeley archive abstract and report text support the network-imposed input-don't-care comparison and identify the Kim–Newborn cascade procedure as prior work.
- Aziz, A., Singhal, V., Swamy, G. M. & Brayton, R. K. (1993). *Minimizing Interacting Finite State Machines*. UCB/ERL M93/68. Berkeley archive abstract supports composition-aware minimization through equivalence relations and hierarchical procedures.
- Watanabe, Y. & Brayton, R. K. (1993). *The Maximum Set of Permissible Behaviors for FSM Networks*. UCB/ERL M93/61. Berkeley archive abstract supports the permissible-component-behavior / E-machine ancestry.

## Remaining bibliography work

Before journal submission, convert these verified records to the journal bibliography format and page-check any sentence that depends on a claim stronger than the source abstracts/report passages above. The older Kim–Newborn primary paper and the classical universal sequential-machine compilation line remain useful attribution work, but they are no longer blockers because the manuscript makes no historical-firstness claim for those mechanisms.