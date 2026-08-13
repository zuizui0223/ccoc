# Fixed regular-grammar relay sharpness for arbitrary `m`

> **Status:** strengthening of the existing one-action maximal-innovation relay. This removes an `m`-dependent finite-word-list presentation and the power-of-two restriction. It does **not** claim novelty for regular languages, partial DFAs, binary trees, Boolean local updates, or input restriction.

## 1. Why this strengthening is needed

The post-reopening relay already removed the growing primitive-port alphabet:

\[
A=\{0,1,\mathsf{fire},\mathsf{tick}\}.
\]

The single-action theorem then made only `fire` newly legal and obtained maximal open-only innovation.

However, its finite certificate still presents the closed/open experiment families as explicit `m`-dependent sets of words, and the addressed selector theorem is written for `m=2^d`.

Those are construction-presentation caveats. They leave open an avoidable objection:

> perhaps the primitive alphabet is fixed only because the system size has been moved into the description of the allowed future-word family.

The present construction removes that caveat.

## 2. One fixed grammar schema for every system size

Use the common primitive alphabet

\[
A=\{0,1,\mathsf{fire},\mathsf{tick}\}.
\]

The **closed grammar** is the one-state partial DFA

\[
q\xrightarrow{0}q,
\qquad
q\xrightarrow{1}q,
\qquad
q\xrightarrow{\mathsf{tick}}q,
\]

with no `fire` transition. Therefore

\[
L_C=\{0,1,\mathsf{tick}\}^{*}.
\]

The **open grammar** adds exactly one loop,

\[
q\xrightarrow{\mathsf{fire}}q,
\]

so

\[
L_O=\{0,1,\mathsf{fire},\mathsf{tick}\}^{*}.
\]

Both partial DFAs have one state for every `m`. If complete DFAs over the common four-symbol alphabet are required, the closed language uses only one additional rejecting sink, while the open language remains one-state. Either representation has `O(1)` grammar description independent of system size.

Opening therefore changes exactly one primitive action / one partial-DFA transition.

## 3. Arbitrary-size balanced relay

For every integer

\[
m\ge1,
\]

use `RelayTreeTopology.balanced(m)`.

It has:

- `m` memory leaves;
- `m-1` binary relay nodes;
- one separate focal output node `ROOT` above the relay-body root;
- maximum degree at most three;
- an underlying undirected tree topology.

The selector is one local selected/unselected marker on the relay body. It starts at `body_root`.

Unlike the earlier power-of-two encoding, the address of leaf `j` is its **actual** left/right child sequence in this tree. Write it as

\[
a_j\in\{0,1\}^{d_j},
\]

where `d_j` is the selector depth of that leaf below `body_root`.

Because memory sites are terminal leaves, the family of addresses is prefix-free.

### Balanced-tree depth

Let `H(m)` be the maximum selector depth in the midpoint-recursive tree. Then

\[
H(1)=0,
\]

and for `m>1`,

\[
H(m)
=1+\max\{H(\lfloor m/2\rfloor),H(\lceil m/2\rceil)\}.
\]

Induction gives

\[
\boxed{H(m)=\lceil\log_2m\rceil.}
\]

The implementation uses the exact integer identity

`H(m) = (m-1).bit_length()`.

## 4. Total local action semantics

A fixed regular grammar is meaningful only if every word it accepts has a defined system trajectory. The old addressed implementation rejected several off-protocol actions using a global quiescence check. The strengthened construction instead defines all four actions on every declared microstate using a fixed local rule.

### Selector layer

- on `0` or `1`, a selected binary relay sends the selector marker to the corresponding child and becomes unselected;
- at a selected memory leaf, further `0/1` actions stutter;
- on `fire` or `tick`, the selector marker stays where it is.

Starting from one selected node, this preserves exactly one selector token. The rule depends only on the selected node, its adjacent child relation, and the globally supplied control symbol.

### Pulse layer

Every global action advances the pulse layer by one synchronous radius-one round.

- a selected leaf emits its permanent memory bit exactly when the action is `fire`;
- an internal selected relay emits no new pulse on `fire`;
- every leaf otherwise emits no new pulse;
- a relay receives the current pulses of its two children and stores their Boolean OR, with `empty` as the neutral no-message state;
- the focal root reads the current pulse of its only child and updates the focal output when a pulse is present.

The pulse alphabet remains

\[
\{\emptyset,0,1\}.
\]

The OR rule totalizes even off-protocol collision states. On every canonical one-token probe there is at most one nonempty child pulse at a relay, so OR agrees exactly with the historical one-token relay rule.

Crucially, the transition uses **no global quiescence oracle, no depth counter, and no `m`-valued port identifier**.

### Local-state bounds

As before, the selected/unselected marker only multiplies the finite relay/leaf state alphabets by two:

- selector-augmented relay state count: at most `6`;
- selector-augmented leaf state count: at most `12`;
- focal output state count: `2`.

All are independent of `m`.

## 5. Closed all-word theorem

Consider the comparison domain

\[
D_m=\{(y,b_1,\ldots,b_m):y,b_j\in\{0,1\}\},
\]

embedded as quiescent relay states with selector at `body_root`.

### Lemma — pulse-free closed invariant

From any pulse-free configuration and any selector position, applying one closed action

\[
a\in\{0,1,\mathsf{tick}\}
\]

preserves:

1. all permanent memory bits;
2. the focal output;
3. absence of every pulse.

Only the selector position may change.

### Proof

No closed action is `fire`, so no leaf can emit a memory pulse. If all current leaf/relay pulses are empty, every child-to-parent message is empty. The fixed local relay aggregation therefore produces empty next pulses everywhere, and the focal root receives no pulse and keeps its output. Address actions may move the selector, but that marker is independent of the memory bits. `square`

By induction on word length, the invariant holds for **every**

\[
w\in L_C.
\]

Hence the complete closed response trace from `(y,b_1,...,b_m)` depends only on `y`.

The empty word/current output distinguishes `y=0` from `y=1`, so

\[
\boxed{|P_C|=2,\qquad K_C=1.}
\]

This is an infinite-language statement; it does not follow from enumerating a finite set of closed words.

## 6. Canonical open probes

For leaf `j` at selector depth `d_j`, define

\[
w_j
=
a_j\,\mathsf{fire}\,\mathsf{tick}^{d_j+1}.
\]

The address moves the unique selector from `body_root` to leaf `j`. Before `fire` there are no pulses. `fire` places `b_j` in that leaf's pulse state. Each following tick moves the pulse one parent edge upward. The leaf is at focal-root distance `d_j+1`, so after exactly `d_j+1` ticks the focal output becomes `b_j` and the pulse layer is quiescent again.

Therefore

\[
\operatorname{finaloutput}(s,w_j)=b_j.
\]

Permanent memory is unchanged.

The open grammar accepts every `w_j`, since it accepts all words over the four-symbol alphabet.

## 7. Open quotient and maximal innovation

The current/empty response gives `y`, and the family `w_1,...,w_m` gives every memory coordinate. Thus every two distinct states in `D_m` differ in at least one declared open response.

Therefore

\[
\boxed{|P_O|=2^{m+1},\qquad K_O=m+1.}
\]

The open-only innovation relative to the closed grammar is

\[
\boxed{\iota_{\rm new}=K_O-K_C=m.}
\]

Since

\[
|D_m|=2^{m+1}
\]

and `|P_C|=2`, the general finite-domain capacity bound gives

\[
\iota_{\rm new}
\le
\log_2|D_m|-\log_2|P_C|
=m.
\]

Hence the fixed-grammar construction again attains the **absolute maximum possible** innovation on its comparison domain.

## 8. Arbitrary-`m` latency

A leaf at selector depth `d_j` uses

\[
|w_j|=d_j+1+(d_j+1)=2d_j+2
\]

actions: `d_j` address actions, one fire, and `d_j+1` propagation ticks.

Because

\[
\max_j d_j=\lceil\log_2m\rceil,
\]

the balanced arbitrary-size construction has

\[
\boxed{
L_{\rm query}^{\rm worst}
=2\lceil\log_2m\rceil+2.
}
\]

For `m=2^d`, all leaves have depth `d` and this reduces exactly to the historical `2 log2(m)+2` result.

## 9. Conservative compatibility with the historical relay

The new local rule changes only behavior outside the previously declared action protocols.

For the old power-of-two canonical addressed word:

1. address actions occur while the pulse layer is empty;
2. fire occurs at the selected leaf while pulses are empty;
3. only tick follows while the one pulse travels upward.

In that regime:

- the OR aggregation has at most one nonempty input and equals the old unique-input rule;
- the selector updates are identical;
- no old global quiescence rejection is encountered.

The implementation certificate therefore compares both the output trace and final microconfiguration against the historical addressed relay on every old canonical state/port pair for the finite regression sizes.

No historical theorem, registry ID, or replay semantics is changed.

## 10. Strengthened simultaneous package

For every integer `m>=1`, one explicit family now has simultaneously:

- one fixed deterministic hardware/topology family;
- closed exact quotient `2`;
- open exact quotient `2^(m+1)`;
- absolute-maximal open-only innovation `m` bits;
- primitive alphabet size `4`;
- one newly legal primitive action (`fire`);
- one-state partial closed grammar and one-state partial open grammar, both independent of `m`;
- no enumerated `m`-dependent legal future-word list in the theorem statement;
- arbitrary `m`, not only powers of two;
- bounded local state/message alphabets;
- pairwise radius-one edge communication;
- maximum degree three;
- tree interaction topology;
- worst canonical access `2 ceil(log2(m))+2`.

This removes two construction caveats from the current residual extremal/local package.

## 11. Novelty discipline

Do not claim novelty for:

- regular/partial finite automata;
- the languages `Sigma*` or alphabet restriction;
- totalizing a partial transition system;
- prefix-free tree paths;
- Boolean OR aggregation;
- generic state distinguishability.

The historical firstness question remains the same one controlled by issue #122: whether classical uniform sequential-machine compilation already yields the **whole simultaneous constrained realization package** with comparable control, locality, response-faithfulness, and timing resources.

The value of this strengthening is narrower and concrete: CCOC no longer needs system-size growth in either the primitive alphabet or the grammar automaton/word-family description to realize the maximal one-action response-interface inflation.