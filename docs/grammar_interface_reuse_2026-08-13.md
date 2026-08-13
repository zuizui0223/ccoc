# Closed-interface reuse under arbitrary same-domain grammar change — 2026-08-13

> **Status:** exact reuse characterization on a fixed controlled plant and common grammar-state domain. Unlike the globally-new-action closure theorem, no monotone relation between the canonical closed/open quotients is assumed or concluded.

## Theorem

Let a finite controlled plant be fixed. Let closed and open finite prefix grammars use the same ordered action alphabet, the same grammar-state set, and the same initial grammar state, but allow arbitrary changes to the grammar transition table.

Let `P_C` be the canonical exact closed grammar-aware quotient on the common product state space, and `P_O` the canonical exact open quotient.

Then the closed canonical labeling `P_C` is itself an exact interface for the open contract if and only if, inside every `P_C` fiber,

1. all states have the same open enabled-action row; and
2. for every common open-legal action, all successors lie in one common `P_C` fiber.

Equivalently,

\[
\boxed{
P_C\text{ reusable as an exact open interface}
\iff
\text{the open partial transition row descends on }P_C.
}
\]

### Proof

The canonical closed quotient has constant current output on each fiber because the plant is fixed. The grammar-aware exact-interface theorem states that a labeling is exact for a given contract precisely when equal labels also have equal enabled-action sets and equal successor labels under every enabled action. Applying that theorem to the open constrained system with the closed canonical labels gives the stated equivalence directly. `□`

This is a **reuse theorem**, not a claim about minimal quotient monotonicity.

## Canonical quotient relation has four regimes

Because grammar mutation can erase old legality distinctions while creating new ones, the minimal canonical partitions can have any of four relations.

### Equal

If the grammar is unchanged, or if a change descends perfectly on the closed quotient,

\[
P_C=P_O.
\]

The closed interface is reusable.

### Open coarser

Use the two-state coarsening counterexample from the corrected grammar-expansion theorem:

- closed `q0`: `a` self-loop, `b` illegal;
- closed `q1`: `a,b` self-loops;
- open: complete `b` at `q0`, making both rows identical.

Then

\[
|P_C|=2,
\qquad
|P_O|=1.
\]

The closed two-block interface is still reusable: it is simply a nonminimal refinement of the one-block open canonical quotient.

Thus **coarsening is not a portability failure**.

### Open finer

Start from two closed-equivalent grammar states and enable an action at only one after opening. Then

\[
P_O\prec P_C.
\]

The old closed merge is no longer exact, so reuse fails by a legality obstruction.

### Incomparable

With three grammar states and actions `{a,b}`, take a constant-output plant and

- closed: `q0` no legal actions; `q1` no legal actions; `q2` has `b -> q0`;
- open: `q0` no legal actions; `q1` has `b -> q0`; `q2` has `b -> q0`.

Then

\[
P_C=\{\{q_0,q_1\},\{q_2\}\},
\]

while

\[
P_O=\{\{q_0\},\{q_1,q_2\}\}.
\]

Neither partition refines the other. Reuse fails because the old fiber `{q0,q1}` has different open legality rows.

Therefore, outside a language-preserving expansion class, a scalar signed quantity such as “interface inflation” does not capture the whole structural change.

## Two complete reuse obstructions

If `P_C` cannot be reused, some pair in one closed fiber violates exactly one of the local exactness requirements:

- **legality obstruction:** different open enabled-action rows;
- **successor obstruction:** equal open legal rows but an enabled action reaches different closed fibers.

These are complete for reuse because current output is already constant on every canonical closed fiber.

## Relation to the corrected closure theorem

The globally-new-action theorem adds a stronger premise: every old action symbol keeps its entire grammar transition column, and only symbols globally absent on the closed side may be activated. Under that premise every closed distinction persists, so `P_O` must refine `P_C`; the reuse criterion then specializes to the zero-inflation criterion, and repeated open-row refinement recovers the minimal open quotient.

Without that premise, the present reuse theorem is the correct general statement.

This gives a clean hierarchy:

\[
\boxed{
\text{arbitrary same-domain grammar change}
\Rightarrow
\text{exact reuse iff row descent}
}
\]

and

\[
\boxed{
\text{globally-new-symbol expansion}
\Rightarrow
P_O\preceq P_C
\text{ and stable closure computes }P_O.
}
\]

The one-state action expansion theorem and the fixed-regular relay lie in the second class.

## Claim discipline

This result is a direct structural consequence of the existing grammar-aware exact-interface theorem. It is not a historical novelty claim for automata or congruence theory. Its CCOC role is to prevent a conceptual error: **portability of a chosen interface and monotonicity of the canonical minimal quotient are different questions once the legal-future automaton itself changes state-dependently.**