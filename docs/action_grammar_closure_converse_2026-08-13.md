# Exact action-grammar closure converse — 2026-08-13

> **Status:** exact characterization for the same-plant, one-state action-grammar expansion subclass. This closes a delimited positive/negative CCOC boundary. It is not a novelty claim for Myhill–Nerode theory, right congruences, DFA minimization, or partition-refinement algorithms.

## 1. Setting

Let

\[
F=(X,A,T,O)
\]

be a finite deterministic controlled output system. The physical state set, output map, and transition map are held fixed.

Choose two action subsets

\[
A_C\subseteq A_O\subseteq A.
\]

The closed and open future grammars are the one-state partial grammars

\[
L_C=A_C^*,
\qquad
L_O=A_O^*.
\]

Thus composition opening changes only which primitive actions are legal. It does not resynthesize the plant.

For a legal language `L`, write `P_L` for the canonical exact response quotient: two states are equivalent exactly when every legal future word gives the same output trace.

Let

\[
P_C=P_{L_C},
\qquad
P_O=P_{L_O}.
\]

Because `L_C subset L_O`, grammar monotonicity gives

\[
P_O\preceq P_C,
\]

where `preceq` means “is a refinement of”.

## 2. Open-congruence refinement operator

For any partition `P` of `X`, define `R_O(P)` by

\[
x\equiv_{R_O(P)}y
\]

iff

1. `x` and `y` are already in the same `P` block; and
2. for every action `a in A_O`, the successors `T(x,a)` and `T(y,a)` lie in the same `P` block.

Start from the exact closed quotient

\[
P^{(0)}=P_C
\]

and iterate

\[
P^{(r+1)}=R_O(P^{(r)}).
\]

Each step only splits blocks, so the sequence is monotone under refinement. Since `X` is finite, it reaches a fixed point. Call it

\[
P^*.
\]

The executable implementation is `causal_model.action_grammar_closure`.

---

## 3. Theorem — stable closure equals the exact open quotient

### Theorem

For every finite plant and every one-state action expansion `A_C subseteq A_O`,

\[
\boxed{P^*=P_O.}
\]

Therefore the minimal exact open interface size can be computed by starting from the already-compressed closed quotient and closing it under the newly available open dynamics.

### Proof

First, `P_C` preserves the current output by definition. Every later `P^(r)` refines `P_C`, so every later block also has constant current output.

At the fixed point,

\[
P^*=R_O(P^*).
\]

Hence whenever `x` and `y` lie in one `P*` block, their successors under every `a in A_O` also lie in one `P*` block. Thus `P*` is an output-preserving right congruence for every open action.

Induction on word length now shows that equal `P*` labels imply equal output traces for every word in `A_O*`. Therefore `P*` is an exact open interface.

Since `P_O` is the coarsest exact open response quotient,

\[
P_O\preceq P^*.
\]

For the reverse direction, `P_O` itself refines `P_C`, because every closed word is also open-legal. Moreover `P_O` is already a right congruence for every action in `A_O`: if two states are open-equivalent, prefixing any open action preserves equivalence of all remaining open suffixes. Therefore

\[
R_O(P_O)=P_O.
\]

So `P_O` is a fixed point of `R_O` that refines `P_C`.

The iteration from `P_C` constructs the coarsest fixed-point refinement of `P_C`: at each step it introduces only distinctions forced by the current open-successor labels. Any fixed point refining `P_C` must therefore refine every `P^(r)` by induction, and hence must refine `P*`. Applying this to `P_O` gives

\[
P^*\preceq P_O.
\]

Combining the two refinement relations yields

\[
P^*=P_O.
\]

`□`

---

## 4. Corollary — exact zero-inflation criterion

Let

\[
A_N=A_O\setminus A_C
\]

be the newly legal primitive actions.

### Corollary

The following are equivalent.

1. Opening produces no exact interface inflation:

   \[
   P_O=P_C.
   \]

2. The closed quotient is already a fixed point of the open refinement operator:

   \[
   R_O(P_C)=P_C.
   \]

3. Every newly legal action descends to a well-defined map on the closed quotient:

   \[
   x\sim_C y
   \Longrightarrow
   T(x,a)\sim_C T(y,a)
   \quad
   \forall a\in A_N.
   \]

### Proof

`1 iff 2` follows from the theorem because `P_O=P*` and the refinement sequence starts at `P_C`.

For `2 iff 3`, every closed action already descends on `P_C` because `P_C` is the exact closed right congruence. Therefore the only possible failure of open congruence at `P_C` comes from newly legal actions. `□`

This is the exact converse missing from the earlier one-way fiber-split statement in this restricted grammar class.

---

## 5. Constructive obstruction when descent fails

Suppose a newly legal action `a` fails to descend on `P_C`. Then there exist

\[
x\sim_C y
\]

with

\[
T(x,a)\not\sim_C T(y,a).
\]

Because the successors are in different canonical closed response classes, by definition there exists a closed word

\[
v\in A_C^*
\]

whose output traces distinguish those successors.

Then

\[
w=av\in A_O^*
\]

is an open-legal word that distinguishes `x` and `y`.

Hence every failure of the zero-inflation descent condition has a concrete witness of the form

\[
\boxed{\text{new action} + \text{closed distinguishing suffix}}.
\]

`ActionDescentObstructionCertificate` constructs such a suffix by finite pair-state search.

This strengthens the interpretation of the historical `CORE-5` local split: in this subclass, a descent failure is not merely a sufficient obstruction to one proposed schema. It is exactly the obstruction to reusing the canonical closed quotient unchanged.

---

## 6. Exact bounded-interface criterion

Let

\[
k_C=|P_C|,
\qquad
k_O=|P_O|=|P^*|.
\]

Since `P_O` is the coarsest exact open interface, an exact open summary with at most `B` macro states exists if and only if

\[
\boxed{k_O\le B.}
\]

Equivalently, in information units,

\[
K_C=\log_2 k_C,
\qquad
K_O=\log_2 k_O,
\]

and the exact inflation is

\[
\boxed{\Delta K=\log_2|P^*|-\log_2|P_C|.}
\]

Thus the closure construction gives not only a zero/nonzero criterion but the exact minimal open response memory in the finite subclass.

---

## 7. Finite refinement-depth bound

Every strict application of `R_O` splits at least one existing block. Therefore the number of blocks increases by at least one at every strict round.

Starting from `|P_C|` blocks and never exceeding `|X|` singleton blocks gives

\[
\boxed{
\text{strict refinement rounds}
\le
|X|-|P_C|.
}
\]

This bound is sharp.

### Sharp cascade family

Fix an integer `r>=1`. Use states

\[
z,x_0,x_1,\ldots,x_r.
\]

Let

\[
O(z)=1,
\qquad
O(x_j)=0.
\]

Use one closed action `c` and one newly legal action `n`.

The closed action sends every state to `x_0`. Therefore the closed quotient is

\[
P_C=\{\{z\},\{x_0,\ldots,x_r\}\},
\]

so

\[
|P_C|=2.
\]

Define the new action by

\[
n(x_0)=x_0,
\qquad
n(x_1)=z,
\qquad
n(x_j)=x_{j-1}\;(j\ge2).
\]

The first refinement round separates `x_1`, because its `n` successor is `z`. The second separates `x_2`, because its successor `x_1` is now separate. Continuing inductively, round `j` separates `x_j`.

Thus exactly one new block is forced per round, and after `r` strict rounds the open quotient is discrete. Since

\[
|X|-|P_C|=(r+2)-2=r,
\]

the upper bound is attained with equality.

This shows that one newly legal primitive action can trigger a maximally deep cascade of inherited response distinctions even though only one grammar transition was added.

---

## 8. Relation to the fixed-regular extremal relay

The theorem in `docs/fixed_regular_extremal_theorem_2026-08-13.md` gives a different, locality-respecting extremal family: a single `fire` grammar transition exposes `m` dormant exterior bits while action alphabet, grammar size, degree, local alphabets, and focal/exterior cut remain bounded.

The present converse explains the positive boundary in the simpler full-state one-state-grammar setting:

- if the new action descends on the closed canonical quotient, the old compression survives exactly;
- if it does not, inflation is forced;
- subsequent open/closed transitions may propagate that first failure through additional refinement rounds.

The relay remains the sharp local construction. The closure theorem is the exact finite characterization of when action-language enlargement does or does not require quotient refinement.

---

## 9. Scope and novelty discipline

Do not claim novelty for:

- deterministic automaton minimization;
- Myhill–Nerode equivalence;
- right congruences;
- standard partition refinement;
- the fact that adding input symbols may refine a machine quotient.

The CCOC-specific value is organizational and theorem-boundary closure: the existing conservative sufficient condition and local new-action obstruction are turned into an explicit iff criterion for one fixed plant under one-state action-alphabet expansion.

This result should therefore be used as a **complete boundary theorem for a delimited subclass**, not as the manuscript's historical firstness claim.

## 10. Validation status

The repository tests cover positive descent, immediate obstruction, obstruction requiring a nonempty closed suffix, the sharp cascade family, and exhaustive enumeration of every two-state binary-output two-action plant.

An independent falsification pass before repository integration additionally checked:

- all 5,832 three-state binary-output two-action deterministic plants;
- all 1,048,576 four-state binary-output two-action deterministic plants.

No counterexample was found to the closure equality, zero-inflation equivalence, or refinement-round bound. Those enumerations are supporting evidence; the proof above is the quantified argument.