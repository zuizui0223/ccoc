# Constant-global-alphabet bounded-locality sharpness

> **Status:** post-reopening strengthening of the `CORE-3` sharpness witness.
> The historical relay construction kept the local node/message grammar and
> maximum degree fixed but used a globally selectable port set whose size grew
> with the number of exterior modules. This construction removes that caveat on
> the power-of-two subfamily.

## Statement

For every

\[
m=2^d,\qquad d\ge1,
\]

there is a finite deterministic controlled relay system with:

- `m` binary dormant exterior memories;
- one binary focal output;
- maximum graph degree three;
- pairwise edge messages only;
- constant-size local node state and message alphabets;
- one **constant global action alphabet**

\[
\boxed{A=\{0,1,\mathsf{fire},\mathsf{tick}\};}
\]

- and one addressed probe word `w_j` for every memory leaf `j`;

such that, on the quiescent comparison domain

\[
D_m=\{0,1\}^{m+1},
\]

all addressed words together induce the discrete open quotient, while each
single-address closed context has exactly four response classes:

\[
\boxed{
K_{\mathrm{open}}(D_m)=m+1,
\qquad
K_{\mathrm{closed},j}(D_m)=2.
}
\]

Hence

\[
\boxed{
K_{\mathrm{open}}(D_m)-
\max_jK_{\mathrm{closed},j}(D_m)
=m-1.
}
\]

The probe word length is logarithmic:

\[
\boxed{|w_j|=2\log_2m+2.}
\]

Thus the linear extension--compression gap survives simultaneously under bounded
degree, pairwise local interaction, constant local grammar, **and constant global
action alphabet**.

## Construction

Use the existing perfect binary relay tree on `m=2^d` memory leaves, with one
focal output node above the binary-tree body. The previous construction attached
an externally selected reader to leaf `j`. Replace that family of reader labels
with one mobile selector token.

The selector starts at the root of the binary-tree body. Each relay-body node has
two children. A global action `0` moves the unique selector token through the
left parent--child edge; action `1` moves it through the right edge. After `d`
address symbols the token is at exactly one memory leaf.

Action `fire` is local: only the selected memory leaf responds, emitting its
permanent bit into the same transient pulse state used by the historical relay.
Action `tick` advances the existing pairwise child-to-parent pulse dynamics by one
microtick.

No node needs to know the leaf index. The address is represented dynamically by
the position of one selector token.

## Constant local grammar

The historical relay grammar has:

- a permanent leaf bit;
- a transient pulse in `{empty,0,1}`;
- relay pulse state in `{empty,0,1}`; and
- binary focal output.

Adding a selected/unselected marker multiplies the relevant local state counts by
at most two. Thus one may take, independently of `m`,

\[
|Q_{\mathrm{relay}}|\le6,
\qquad
|Q_{\mathrm{leaf}}|\le12.
\]

The pulse alphabet stays `{empty,0,1}`. Selector motion is one parent-to-child
edge event; pulse motion is one child-to-parent edge event. Both are pairwise.
The original binary-tree core already has maximum degree three, and the new
construction no longer attaches a degree-one reader node, so the same degree
bound holds.

## Exact address length

The perfect binary body has depth `d=log_2 m`. Its memory leaf is at distance
`d+1` from the focal root-output node because the root-output node sits one edge
above the binary body. The historical relay therefore needs

\[
d+2
\]

microticks from reader firing through final quiescence: one firing microtick and
`d+1` upward propagation ticks.

The addressed construction first spends `d` actions selecting the leaf, then
uses the same `d+2` relay microticks. Therefore

\[
|w_j|=d+(d+2)=2d+2=2\log_2m+2.
\]

## Closed quotient

Fix one address `j`. The closed comparison grammar contains the empty word and
`w_j`. During the `d` address actions and all propagation actions before the
pulse reaches the focal node, the observable focal output remains the initial
inside bit `y`. At the end of the word it is `b_j`.

Thus the entire closed response trace factors through

\[
(y,b_j).
\]

Conversely the empty response recovers `y`, and the final output after `w_j`
recovers `b_j`. All four binary pairs occur on `D_m`, so

\[
K_{\mathrm{closed},j}(D_m)=\log_2 4=2.
\]

## Open quotient

The open comparison grammar contains the empty word and every addressed word

\[
\{w_0,\ldots,w_{m-1}\}.
\]

The empty word decodes `y`, while `w_j` decodes `b_j`. Therefore two distinct
binary macrostates differ in a coordinate exposed by one declared word. The open
quotient on `D_m` is discrete:

\[
K_{\mathrm{open}}(D_m)=\log_2 2^{m+1}=m+1.
\]

This is the same injection logic as `CORE-2`, but the implementation no longer
uses an `m`-symbol family of primitive global probe actions.

## Constrained composition inheritance

Any binary codebook

\[
C_m\subseteq\{0,1\}^{m+1}
\]

inherits the same addressed readout because the construction is correct on the
whole cube. In particular, the fixed-richness family

\[
C_{m,k}
=
\{(y,b):\sum_jb_j=k\}
\]

uses the same four-symbol alphabet, degree-three topology, and local grammar.
Its codebook gap remains

\[
\Delta_{m,k}=\log_2\binom{m}{k}-1
\]

under the decoder contracts in `composition_code_rate.md`.

Thus the two post-reopening strengthenings combine:

> a positive-rate constrained composition family can force linear exact
> interface inflation even when both the local grammar and the global control
> alphabet are constant.

## What this does not claim

- The number of **legal addressed words** still grows with `m`; only their
  generating action alphabet is constant.
- Probe word length grows logarithmically rather than remaining constant.
- The certificate is a finite deterministic construction, not an empirical
  ecological model.
- This construction does not show that four global action symbols are minimal.
- The power-of-two restriction is for a clean perfect-tree family; it is enough
  for asymptotic sharpness but is not claimed necessary.

## Executable certificate

`causal_model.constant_alphabet_relay` provides:

- binary root-to-leaf address words;
- explicit selector-token trajectories;
- replay through the existing local relay microdynamics;
- exhaustive closed/open response-signature checks at declared finite sizes; and
- `ConstantAlphabetRelaySharpnessCertificate`.

The finite replay checks the construction. The all-`m=2^d` statement follows from
the symbolic perfect-tree address argument and the previously established relay
pulse conjugacy.
