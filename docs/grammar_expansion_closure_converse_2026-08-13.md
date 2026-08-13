# Grammar-aware expansion closure converse — 2026-08-13

> **Status:** exact finite characterization for monotone expansion of a finite prefix grammar on a fixed controlled plant. This generalizes the one-state action-grammar closure theorem. It is not a novelty claim for right congruences, automaton minimization, or partition refinement.

## 1. Setting

Let

\[
F=(X,A,T,O)
\]

be a finite deterministic controlled output system. Keep the plant state set, action alphabet, transition map, and output map fixed.

Let

\[
G_C=(Q,A,\delta_C,q_0),
\qquad
G_O=(Q,A,\delta_O,q_0)
\]

be finite prefix grammars on the **same** grammar-state set and initial grammar state. A missing transition is written `None`.

Assume opening is monotone:

\[
\delta_C(q,a)\text{ defined}
\Longrightarrow
\delta_O(q,a)=\delta_C(q,a).
\]

Thus opening may turn a previously illegal action into a legal transition, possibly to a grammar-state-dependent target, but it never changes the meaning of an already legal grammar transition.

The semantic state space for both contracts is the common finite product

\[
Z=X\times Q.
\]

Write

\[
P_C
\]

for the canonical exact grammar-aware response quotient under `G_C`, and

\[
P_O
\]

for the corresponding quotient under `G_O`.

Because every closed legal trajectory remains open legal with the same plant and grammar transitions, opening can only refine the response quotient:

\[
P_O\preceq P_C.
\]

## 2. Open-row closure operator

Let `P` be any partition of `Z` that refines `P_C`. For

\[
z=(x,q)\in Z,
\]

define its open row relative to `P` by

\[
\rho_P(z)
=
\left(
[z]_P,
\left(
 a,
 [T(x,a),\delta_O(q,a)]_P
\right)_{a\in \mathrm{Legal}_O(q)}
\right).
\]

The ordered action labels in this row encode both:

1. which actions are legal at the open grammar state; and
2. the current `P`-class of every legal open successor.

Define

\[
R_O(P)
\]

by equality of these row signatures.

Starting from

\[
P^{(0)}=P_C,
\]

iterate

\[
P^{(r+1)}=R_O(P^{(r)}).
\]

Each round only splits existing blocks. Since `Z` is finite, the sequence stabilizes. Write its fixed point as

\[
P^*.
\]

## 3. Theorem — stable grammar closure equals the exact open quotient

### Theorem

Under the monotone same-state-space grammar expansion above,

\[
\boxed{P^*=P_O.}
\]

### Proof

Every block of `P_C` has constant current output because `P_C` is an exact closed interface. Every later partition refines `P_C`, so current output remains constant on every later block.

At the fixed point,

\[
P^*=R_O(P^*).
\]

Hence if two product states lie in one `P*` block, they have exactly the same open enabled-action row, and for every enabled action their open successors lie in one common `P*` block. Therefore `P*` satisfies the local grammar-aware exactness conditions: equal current output, equal enabled actions, and equal successor summary under every enabled action.

Induction on legal open word length then shows that equal `P*` labels preserve every legal open response. Thus `P*` is an exact open interface. Since `P_O` is the coarsest exact open interface,

\[
P_O\preceq P^*.
\]

For the reverse direction, `P_O` refines `P_C` because every closed response is part of the open contract. Moreover `P_O` is already stable under `R_O`: open-equivalent states have the same enabled actions, and after every enabled open action their successors remain open-equivalent. Thus

\[
R_O(P_O)=P_O.
\]

Any fixed point of `R_O` refining `P_C` must refine each iterate `P^(r)`. This follows inductively because an `R_O`-stable partition already respects every distinction used to construct the next iterate. Therefore every such fixed point refines the least stable refinement `P*`.

Applying this to `P_O` yields

\[
P^*\preceq P_O.
\]

Combining both refinement relations gives

\[
P^*=P_O.
\]

`□`

## 4. Exact zero-inflation criterion

The theorem immediately gives a complete reuse criterion.

### Corollary

The following are equivalent:

1. opening creates no exact interface inflation,

   \[
   P_O=P_C;
   \]

2. `P_C` is already stable under the open-row closure,

   \[
   R_O(P_C)=P_C;
   \]

3. for every pair

   \[
   z,z'\in Z
   \quad\text{with}\quad
   z\sim_C z',
   \]

   both of the following hold:

   **legality uniformity**

   \[
   \mathrm{Legal}_O(z)=\mathrm{Legal}_O(z'),
   \]

   and **successor descent**

   \[
   T_O(z,a)\sim_C T_O(z',a)
   \qquad
   \forall a\in\mathrm{Legal}_O(z).
   \]

Thus the canonical closed interface survives the grammar expansion exactly iff every open row descends to a well-defined partial transition row on the closed quotient.

This is the grammar-state-dependent generalization of the one-state condition “every newly legal action descends on `P_C`”.

## 5. Two complete first-step obstruction types

If zero inflation fails, `P_C` is not a fixed point. Therefore some pair inside one closed fiber violates the open-row condition. There are exactly two possibilities.

### A. Legality obstruction

Two states satisfy

\[
z\sim_C z'
\]

but an action is open-legal at one and not the other:

\[
a\in\mathrm{Legal}_O(z)
\quad\text{and}\quad
a\notin\mathrm{Legal}_O(z').
\]

Then the closed fiber cannot remain one exact open macrostate because one macrostate cannot have two different legal-action rows.

### B. Successor-descent obstruction

The two states have the same open legality row, but for some common legal action

\[
T_O(z,a)\not\sim_C T_O(z',a).
\]

Then `a` does not induce a well-defined successor on the closed quotient. The fiber must split, possibly followed by further propagated splits in later refinement rounds.

`GrammarExpansionObstructionCertificate` returns one of these two obstruction kinds.

The two types are exhaustive because equality of the complete open row signature is exactly the fixed-point condition.

## 6. Exact bounded-interface criterion

Let

\[
k_C=|P_C|,
\qquad
k_O=|P_O|=|P^*|.
\]

Because `P_O` is the coarsest exact open interface, an exact open summary with at most `B` states exists iff

\[
\boxed{k_O\le B.}
\]

The exact information inflation is therefore

\[
\boxed{
\Delta K
=
\log_2|P^*|-
\log_2|P_C|.
}
\]

So the closure theorem provides the exact minimal open memory, not only a yes/no obstruction.

## 7. Finite refinement-depth bound

Every strict closure round increases the number of blocks by at least one. The common product domain has

\[
|Z|=|X||Q|
\]

states. Hence

\[
\boxed{
\text{strict refinement rounds}
\le
|X||Q|-|P_C|.
}
\]

This bound is sharp already in the one-state-grammar subclass through the cascade family proved in `docs/action_grammar_closure_converse_2026-08-13.md`. Therefore no better universal bound can follow merely from passing to multiple grammar states.

## 8. Relationship to the conservative macro-schema theorem

`ConservativeMacroSchema` supplies a positive sufficient condition for portability under monotone action growth. The present result identifies the exact local condition when the candidate summary is specifically the **canonical closed quotient** and the plant/grammar state spaces are held fixed.

The relationship is:

- conservative schema condition: a proposed macro labeling has uniform legal rows and label-deterministic successors as new actions appear;
- grammar-expansion converse: for the canonical closed labeling, those row conditions are not merely sufficient—they are **necessary and sufficient for zero inflation**.

If they fail, exact refinement is forced. If they hold, no refinement at all is needed.

This closes the intended positive/negative boundary for monotone same-state-space finite grammar expansion.

## 9. Relation to the CCOC extremal relay

The fixed-regular relay uses a one-state grammar, so it is a special case. Its newly legal `fire` transition fails successor descent maximally: dormant exterior coordinates become distinguishable, driving

\[
|P_C|=2
\quad\longrightarrow\quad
|P_O|=2^{m+1}.
\]

The extremal construction shows how large the forced refinement can be under fixed local/static resources. The present closure theorem says exactly **when any refinement is forced at all** in the wider finite-grammar class.

Together they give a cleaner boundary:

\[
\boxed{
\text{open-row descent}
\Longleftrightarrow
\text{exact portability of }P_C
}
\]

versus

\[
\boxed{
\text{open-row failure}
\Longrightarrow
\text{forced refinement, potentially extremal}.
}
\]

## 10. Validation and claim discipline

Repository tests cover:

- state-dependent grammar expansion with zero inflation;
- legality-row mismatch;
- successor-descent mismatch with identical open legal rows;
- rejection of modifications to old grammar transitions;
- exact bounded-interface criterion; and
- exhaustive enumeration of all `5^4 = 625` monotone closed/open transition-pairs for two grammar states and two actions on a one-state plant.

The exhaustive test is supporting falsification, not the proof.

Do not assign novelty to generic DFA minimization, grammar-state refinement, right congruences, or fixed-point partition algorithms. The CCOC contribution here is a delimited necessity/converse boundary aligned with its open-composition question.