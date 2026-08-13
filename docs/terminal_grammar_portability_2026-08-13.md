# Terminal-stage criterion for exact grammar-chain portability — 2026-08-13

> **Status:** exact finite criterion for a fixed plant under a chain of globally-new-action-symbol grammar expansions. This builds on the corrected closure theorem and the existing conservative macro-schema theorem. It is not a novelty claim for nested partition refinement or terminal-stage minimization by itself.

## 1. Setting

Fix a finite deterministic controlled output system

\[
F=(X,A,T,O).
\]

Let

\[
G_0,G_1,\ldots,G_r
\]

be finite prefix grammars on the same action alphabet `A`, the same grammar-state set `Q`, and the same initial grammar state.

Require each adjacent transition

\[
G_t\to G_{t+1}
\]

to satisfy the corrected **globally-new-symbol expansion** contract:

- every action symbol already available anywhere in `G_t` keeps its complete grammar transition column unchanged in `G_{t+1}`;
- a symbol illegal at every state of `G_t` may become legal state-dependently in `G_{t+1}`;
- once introduced, its transition column is frozen in all later stages.

Let

\[
P_t
\]

be the canonical exact grammar-aware response quotient of the common product domain

\[
Z=X\times Q
\]

under grammar `G_t`.

The corrected grammar-expansion theorem implies

\[
P_{t+1}\preceq P_t
\]

for every adjacent pair.

## 2. Theorem — terminal quotient is the minimal uniform exact interface

### Theorem

The canonical terminal quotient

\[
P_r
\]

is an exact interface for **every** stage `G_t`. Moreover, among all single labelings of `Z` that are exact interfaces for every stage, `P_r` has the minimum possible number of blocks.

Therefore

\[
\boxed{
\min\{|M|:M\text{ is one exact interface for all stages}\}
=|P_r|.
}
\]

Equivalently, for any integer budget `B>=1`,

\[
\boxed{
\exists\text{ one exact interface with at most }B\text{ states for the whole chain}
\iff
|P_r|\le B.
}
\]

### Proof — lower bound

Let `M` be one labeling that is exact for every stage. In particular, `M` is exact for the terminal constrained system `(F,G_r)`.

By definition, `P_r` is the coarsest exact interface for that terminal system. Hence every exact terminal interface refines `P_r`. Therefore

\[
|M|\ge |P_r|.
\]

This gives the lower bound.

### Proof — upper bound

It remains to show that the terminal labeling itself is exact at every earlier stage.

Because each grammar step introduces only globally new symbols and never alters any old transition column, every action legal at stage `t` remains legal with identical grammar transition semantics at every later stage. Hence the legal transition structure of `G_t` is a restriction of that of `G_r`.

Take two states in one terminal quotient block. Terminal exactness implies:

1. equal current output;
2. identical terminal enabled-action rows;
3. equal terminal quotient labels after every terminal-enabled action.

At an earlier stage, globally later-introduced action symbols are absent **at every grammar state**, so removing them from the terminal action rows preserves equality of the earlier enabled rows. Every action that remains legal at stage `t` has exactly the same plant and grammar successor as at the terminal stage, so its successors still have equal terminal labels.

Thus the terminal labeling satisfies the grammar-aware local exactness conditions at every earlier stage. Therefore `P_r` itself is one exact interface for the whole chain.

Combining with the lower bound gives equality. `□`

## 3. Corollary — path independence of the uniform memory budget

Suppose two valid globally-new-symbol expansion chains have the same initial plant/domain and the same terminal grammar `G_r`, but introduce the globally new symbols in different orders.

Their intermediate canonical quotients may differ. Nevertheless their minimal uniform exact-interface size is the same:

\[
\boxed{|P_r|}.
\]

This follows immediately because the theorem depends only on the canonical quotient of the common terminal grammar.

Thus ordering new legal capabilities can change **when** distinctions appear, but not the smallest memory budget needed by one exact interface that must remain valid for the entire chain once the terminal contract is fixed.

## 4. Constructive conservative macro-schema

The theorem has a stronger constructive form. Use the terminal labels `P_r` at every stage.

For each stage `t`, these labels define an exact `ConservativeStageProjection`. Let the macro output of each terminal label be its common plant output. Define the macro transition row for every action from the terminal stage.

Earlier stages realize restrictions of those rows:

- an action not yet introduced is unavailable;
- once an action is introduced, its complete grammar transition column is frozen;
- terminal-label successor semantics under every available action are therefore unchanged thereafter.

Because all stages use the same product domain, the identity map on `Z` is a trajectory embedding from each stage to the next: every old legal action remains legal and its successor is identical.

Consequently the terminal labels construct one

\[
\boxed{\text{ConservativeMacroSchema}}
\]

realized by every stage in the chain.

This connects the exact converse directly to the existing positive portability theorem rather than introducing a parallel notion of portability.

## 5. Resource interpretation

The terminal criterion converts a chain-wide exact portability question into one final-stage resource calculation.

Let

\[
K_t=\log_2|P_t|.
\]

Then

\[
K_0\le K_1\le\cdots\le K_r,
\]

and the smallest memory of one exact interface valid across the whole chain is

\[
\boxed{K_{\rm uniform}=K_r}.
\]

No sum of the intermediate inflations is needed to determine the final uniform state budget; the terminal canonical quotient already contains every distinction forced anywhere in the valid expansion chain.

This statement is about **one shared exact labeling on a common finite semantic domain**. It does not address communication complexity, online adaptation cost, changing state domains, or the cost of learning/updating the interface as the grammar evolves.

## 6. Sharp finite example

Take a one-state constant-output plant and three grammar states `q0,q1,q2` with actions

\[
\{\mathsf{stay},u,v\}.
\]

Initially only `stay` is legal everywhere, so all three grammar states are response-equivalent:

\[
|P_0|=1.
\]

Introduce globally new `u` only at `q0`. Then `q0` separates from `q1,q2`:

\[
|P_1|=2.
\]

Next introduce globally new `v` only at `q1`. All three states become distinct:

\[
|P_2|=3.
\]

Hence

\[
(|P_0|,|P_1|,|P_2|)=(1,2,3),
\]

and the exact uniform chain budget is three states.

If `v` is introduced before `u`, the middle two-block partition changes, but the terminal grammar and terminal three-block quotient are the same. This realizes the path-independence corollary.

## 7. Boundary of the theorem

The globally-new-symbol premise is essential for the terminal minimality argument in this form. If an old partially available action is completed at additional grammar states, old legality distinctions may disappear and canonical quotients can coarsen or become incomparable, as shown by the #163 counterexample and the general reuse theorem.

For that broader class, there need not be a monotone chain of canonical quotients, so “terminal canonical quotient = minimal uniform interface” is not automatic. One must instead solve the shared-interface intersection problem directly.

Likewise, if the plant state space or grammar-state domain changes between stages, identity embeddings are unavailable and this theorem does not apply.

## 8. Validation

`causal_model.terminal_grammar_portability` constructs a finite certificate that checks:

- every adjacent grammar pair satisfies globally-new-symbol expansion;
- canonical block counts are nondecreasing;
- terminal labels are exact at every stage;
- the terminal block count is the exact uniform budget;
- identity trajectory embeddings preserve every old transition;
- the terminal labels realize one `ConservativeMacroSchema` across the chain.

Regression tests include the `1 -> 2 -> 3` chain, alternative addition orders with one common terminal grammar, the single-stage limit, and rejection of partial completion of an old action symbol.

## 9. Claim discipline

The elementary lower-bound step “a shared interface must work at the terminal stage” and generic nested-partition logic are not novelty claims. The role of this theorem is to close a resource-bounded portability question in the corrected CCOC grammar-expansion class and to link the converse machinery directly to the pre-existing conservative positive theorem.