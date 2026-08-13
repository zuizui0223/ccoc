# Tier-A contextual-minimization primary audit — 2026-08-13

> **Purpose.** Test the broad CCOC/RACH novelty slogan against historical work that
> minimizes or abstracts the **same finite-state component under a restricted
> environment, input set, observer, or property**. This memo is claim control, not
> a new theorem.

## Decision

The broad phenomenon

> a fixed finite-state system can admit a coarser exact/minimum description when
> only a restricted context of inputs, environment behavior, observations, or
> properties is relevant

must be treated as established prior-art territory.

The remaining manuscript candidate is therefore **quantitative and simultaneous**:
CCOC compares many fixed closed grammars on one deterministic controlled system,
keeps every fixed closed quotient small, can keep the union of all closed response
words small, and then exhibits a tiny grammar expansion whose open response
quotient attains the maximum finite-domain innovation. The current relay realizes
that benchmark under additional bounded-local constraints.

This audit does **not** establish historical priority for that combined extremal
package. It narrows the claim that still needs falsification.

## 1. Kim–Newborn ancestry is stronger than a bibliographic analogy

Kim & Newborn (1972), *The Simplification of Sequential Machines with Input
Restrictions*, is already the direct classical lineage for minimizing a machine
when only a restricted set of input sequences can occur.

A later primary institutional report by Wang & Brayton (UC Berkeley ERL M93/64,
1993), *Input Don't Care Sequences in FSM Networks*, explicitly states that in a
cascade FSM network the Kim–Newborn procedure **exactly computes all input don't
care sequences for the driven machine**. Wang & Brayton generalize the computation
to a component in an arbitrary-topology FSM network through an abstract driving
machine.

Primary institutional record:

- https://www2.eecs.berkeley.edu/Pubs/TechRpts/1993/2420.html

Consequence for CCOC claim control:

- context-generated legal-input restriction is not new;
- exploiting that restriction to simplify the driven component is not new;
- the manuscript must not present “closed context allows a smaller exact machine”
  as the conceptual discovery.

The unresolved question is the **worst-case cross-grammar separation** under the
CCOC comparison contract, not the existence of contextual simplification.

## 2. Environment-dependent exact quotients on the same machine are explicit

Aziz, Singhal, Swamy & Brayton (UC Berkeley ERL M93/68, 1993), *Minimizing
Interacting Finite State Machines*, works directly with equivalence relations on
the state space of interacting FSMs.

The primary report states that environment information can be used to obtain
 greater minimization. It then defines behavior equivalence by equality of the
input/output behavior relation and states that the quotient under that relation is
a minimum-state machine behavior-compatible with the original machine. The same
report also emphasizes that useful equivalences depend on the environment and on
which property or outputs are being considered.

Primary report:

- https://www2.eecs.berkeley.edu/Pubs/TechRpts/1993/2425.html
- PDF: https://www2.eecs.berkeley.edu/Pubs/TechRpts/1993/Archive/ERL-93-68.pdf

This is close in spirit to a grammar/observer-conditioned exact response quotient.
It does not, in the reviewed passages, provide the CCOC extremal family or the
specific nested-grammar state-gap theorem. But it removes any remaining novelty
budget from the broad statement that a component's minimum exact representation
can depend on its environment or observation contract.

## 3. Property-dependent exact reduction is also established

The Berkeley compositional-model-checking line makes the same lesson explicit on
the observer/property axis. Aziz, Shiple & Singhal, *Formula-Dependent Equivalence
for Compositional CTL Model Checking* (CAV 1994), defines state equivalence with
respect to a given CTL formula; because it need not preserve all CTL formulae, it
can be coarser than bisimulation, and it is used to reduce component FSMs before
composition.

This is not an input-language theorem and therefore is not a direct match to CCOC.
It is nevertheless further primary/authoritative ancestry for **contract-dependent
state equivalence on a fixed transition system**.

Bibliographic/authoritative records:

- https://dblp.org/rec/conf/cav/AzizSS94
- https://www2.eecs.berkeley.edu/Pubs/Faculty/brayton.html

## 4. Permissible-behavior theory broadens the context further

Watanabe & Brayton (UC Berkeley ERL M93/61, 1993), *The Maximum Set of Permissible
Behaviors for FSM Networks*, asks for the complete set of component FSM behaviors
that can replace a component while preserving total-system behavior and represents
that set by an E-machine.

Primary institutional record:

- https://www2.eecs.berkeley.edu/Pubs/TechRpts/1993/2416.html

This is not the CCOC same-hardware nested-grammar quotient benchmark. It is strong
ancestry for the general idea that the surrounding network determines which local
sequential distinctions must be retained.

## 5. Modern exact tail minimization confirms the lineage

Larrauri & Bloem (2021), *Minimization and Synthesis of the Tail in Sequential
Compositions of Mealy Machines*, studies a known head and tail and asks for a
replacement tail with the minimum number of states. The relevant input context for
the tail is generated by the head. This modern formulation explicitly places
context-restricted minimization in the Kim–Newborn lineage.

Primary preprint:

- https://arxiv.org/abs/2105.10292

Again, this does not by itself match the current CCOC extremal benchmark; it makes
clear that **minimum implementation under an environment-generated input
language** is mature theory.

## 6. Revised novelty hierarchy

### Historical substrate — no novelty claim

Do not claim novelty for:

1. exact/minimum state reduction under input restrictions;
2. same-component minimization using environment-generated don't-care sequences;
3. property/observer-dependent state equivalence;
4. interacting-FSM contextual minimization;
5. the generic fact that enlarging a future-test family can split a quotient;
6. an exponential state gap without a closer same-system/nested-grammar contract.

### Remaining quantitative manuscript candidate

The source search has not yet located one theorem family that explicitly combines
all of the following:

\[
|P_j|=2\quad\forall j,\qquad |P_U|=2,\qquad |P_O|=2^{m+1},
\]

with:

- one fixed deterministic controlled system / hardware family;
- `m` separately declared closed contexts;
- real routing dynamics already legal before opening;
- exactly one newly legal primitive action type;
- open-only innovation `iota_new=m`, saturating the finite-domain upper bound;
- fixed four-symbol primitive control alphabet;
- bounded local state/message alphabets;
- pairwise radius-one dynamics and maximum degree three;
- logarithmic causal access.

This is a **negative search status**, not a priority proof.

## 7. Revised manuscript framing

The safe conceptual opening is now:

> Context-dependent sequential-machine reduction is classical. We ask a sharper
> quantitative question: how large can the exact response-interface penalty become
> when one keeps the plant fixed and enlarges only the legal future grammar? Under
> operational addressability we obtain a codebook lower bound, and an explicit
> family realizes the maximum open-only innovation while every fixed closed
> context and their union retain a one-bit response quotient.

The paper should therefore use **cross-grammar response complexity** as the formal
problem and the **extremal quantitative separation** as the candidate contribution,
not “open systems destroy compression” as a firstness-bearing slogan.

## 8. Remaining falsification target

The next search should be narrowly quantitative:

1. Find a Kim–Newborn descendant or promise/input-restricted transducer theorem
   with one fixed plant and a family of restricted legal-word languages whose
   minimum quotients are `O(1)` but whose relaxed/open quotient has `2^{Omega(m)}`
   states.
2. Check whether that relaxation can be caused by one newly legal primitive input
   symbol/action while all other routing/control behavior is already legal.
3. Separately finish the classical universal-compiler H1–H4 gate to determine
   whether the bounded-local relay is novel only as a clean explicit witness.

Until such a direct quantitative match is found, the combined extremal package
remains a defensible **candidate**, with no firstness language.
