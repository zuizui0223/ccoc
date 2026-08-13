# Globally-new-action grammar expansion closure converse — 2026-08-13

> **Corrected scope:** exact finite characterization for adding globally new action symbols to a finite prefix grammar on a fixed controlled plant. The broader claim that arbitrary state-dependent `None -> target` completion can only refine the canonical quotient is false; an explicit coarsening counterexample is recorded below. This is not a novelty claim for automaton minimization, right congruences, or partition refinement.

## 1. Setting

Let

\[
F=(X,A,T,O)
\]

be a finite deterministic controlled output system. Keep the plant, action alphabet, grammar-state set `Q`, and initial grammar state fixed.

Let

\[
G_C=(Q,A,\delta_C,q_0),
\qquad
G_O=(Q,A,\delta_O,q_0).
\]

For each action symbol `a`, impose exactly one of two possibilities:

1. **old symbol:** its complete grammar transition column is unchanged,

   \[
   \delta_O(q,a)=\delta_C(q,a)
   \quad\forall q\in Q;
   \]

2. **globally new symbol:** it was illegal at every closed grammar state,

   \[
   \delta_C(q,a)=\bot
   \quad\forall q\in Q,
   \]

   and the open grammar may define it at any subset of grammar states, with state-dependent targets.

Thus opening never fills a missing transition of an action symbol that was already available somewhere on the closed side.

The common semantic state space is

\[
Z=X\times Q.
\]

Write `P_C` and `P_O` for the canonical exact grammar-aware response quotients under the closed and open contracts.

## 2. Why the symbol-level condition is necessary

Arbitrary cellwise transition completion is **not** monotone for the canonical grammar-aware quotient, because enabled-action structure is itself part of the response contract.

Take a one-state constant-output plant with actions `{a,b}` and two grammar states. Let the closed grammar be

- `q0`: `a -> q0`, `b` illegal;
- `q1`: `a -> q1`, `b -> q1`.

Then `q0` and `q1` are closed-distinct because their legal-action rows differ.

Now complete only the missing old `b` transition at `q0`:

- `q0`: `a -> q0`, `b -> q0`;
- `q1`: `a -> q1`, `b -> q1`.

With constant output, the two open grammar states are now behaviorally identical. Therefore

\[
|P_C|=2,
\qquad
|P_O|=1.
\]

So the open quotient can **coarsen**. The statement `P_O \preceq P_C` is false for arbitrary state-dependent completion.

The corrected theorem excludes exactly this failure mode: if an action is old anywhere, its entire transition column is frozen. Therefore every closed legal word remains open legal with exactly the same grammar and plant trajectory, so every closed distinction persists and

\[
\boxed{P_O\preceq P_C}.
\]

## 3. Open-row closure operator

For any partition `P` refining `P_C`, define the open row of `z=(x,q)` by

\[
\rho_P(z)=
\left(
[z]_P,
\left(a,[T(x,a),\delta_O(q,a)]_P\right)_{a\in\mathrm{Legal}_O(q)}
\right).
\]

Let `R_O(P)` identify exactly states with equal row signatures. Starting from

\[
P^{(0)}=P_C,
\]

iterate

\[
P^{(r+1)}=R_O(P^{(r)}).
\]

The current label is included in the signature, so each step can only split blocks. Finite `Z` guarantees a fixed point `P*`.

## 4. Theorem — stable closure equals the exact open quotient

Under globally-new-symbol expansion,

\[
\boxed{P^*=P_O.}
\]

### Proof

Every `P*` block has constant current output because `P*` refines `P_C`. At the fixed point, equal labels have equal open enabled-action rows and equal successor labels under every enabled action. Hence `P*` is an exact grammar-aware open interface, so the canonical coarsest open quotient satisfies

\[
P_O\preceq P^*.
\]

Conversely, the symbol-level expansion contract preserves every closed word and its semantics, hence `P_O \preceq P_C`. The canonical open quotient is itself stable under `R_O`. Any stable refinement of `P_C` refines every iterate `P^(r)`, so it refines their least stable limit `P*`. Applying this to `P_O` gives

\[
P^*\preceq P_O.
\]

Thus `P*=P_O`. `□`

## 5. Exact zero-inflation criterion

The following are equivalent:

1. `P_O=P_C`;
2. `R_O(P_C)=P_C`;
3. inside every `P_C` fiber:
   - the open legal-action row is uniform; and
   - for every common open-legal action, the open successors lie in one common `P_C` block.

Equivalently, every open partial transition row descends to a well-defined row on the canonical closed quotient.

Failure has exactly two first-step forms:

- **legality obstruction:** two closed-equivalent states acquire different open enabled-action rows;
- **successor obstruction:** their open legality rows agree, but a common enabled action reaches different closed quotient blocks.

If neither occurs, the closed quotient is already an exact open interface and, in this symbol-expansion class, remains the canonical minimal one.

## 6. Exact minimal memory and refinement depth

Let

\[
k_C=|P_C|,
\qquad
k_O=|P_O|=|P^*|.
\]

An exact open interface with at most `B` blocks exists iff

\[
\boxed{k_O\le B}.
\]

The exact response-memory change is

\[
\boxed{\Delta K=\log_2|P^*|-\log_2|P_C|\ge0}.
\]

Every strict closure round increases the block count, so

\[
\boxed{
\text{strict refinement rounds}
\le |X||Q|-|P_C|.
}
\]

The bound is already sharp in the one-state cascade family from `docs/action_grammar_closure_converse_2026-08-13.md`.

## 7. Relation to conservative portability

`ConservativeMacroSchema` requires uniform legal status and label-deterministic successors as actions become available. For the **canonical closed quotient** in the globally-new-symbol class, the present theorem shows those row conditions are not merely sufficient: they are necessary and sufficient for zero exact inflation.

For broader cellwise grammar completion, the correct question changes. The canonical open quotient may be finer, equal, or coarser than the closed quotient. One can still ask whether the old closed labeling remains an exact open interface, but that is a **reuse criterion**, not a monotone-inflation theorem. That broader reuse problem is kept separate from the result proved here.

## 8. Relation to the fixed-regular relay

The fixed-regular relay is a one-state special case. `fire` is illegal at the only closed grammar state, so it is globally new. Its successor-descent failure exposes the dormant exterior coordinates and yields

\[
|P_C|=2,
\qquad
|P_O|=2^{m+1}.
\]

Thus the relay remains inside the corrected theorem scope.

## 9. Validation

The correction tests include the explicit coarsening counterexample above. They also enumerate all `5^4=625` cellwise monotone closed/open transition-pairs for two grammar states and two actions on a one-state plant:

- **289** satisfy the globally-new-symbol contract and are checked against the closure theorem;
- **336** violate the contract and must be rejected.

This exhaustive regression is supporting falsification, not the analytic proof.

## 10. Claim discipline

Do not assign novelty to generic DFA minimization, grammar-state refinement, right congruences, or partition-refinement algorithms. The value here is a sharply scoped CCOC boundary theorem plus an explicit counterexample showing why the broader transition-completion formulation is invalid.