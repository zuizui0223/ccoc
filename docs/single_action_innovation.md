# One newly legal primitive action can force linear interface innovation

> **Status:** post-reopening dynamic sharpness candidate for the `iota_new` term in
> the causal interface inflation decomposition. The construction reuses the
> constant-alphabet, maximum-degree-three relay rather than introducing a new
> interaction model.

## 1. Question

The static closed-view part of interface inflation is now understood through the
common-refinement / natural-join capacity

\[
C
=
\sum_{B\in P_0}\prod_j r_j(B).
\]

That raises a sharper question:

> Can the open-only innovation term become large even when the entire static
> closed-view join capacity remains constant?

Yes. In fact one newly legal primitive action is enough.

## 2. Family

Take the existing binary-address relay with

\[
m=2^d
\]

binary dormant memory leaves. The quiescent macrostate is

\[
(y,b_1,\ldots,b_m)
\in
\{0,1\}^{m+1}.
\]

The relay topology has maximum degree three. Selector transfer and pulse transfer
are pairwise adjacent-node updates. Local selector/pulse/memory state alphabets do
not grow with `m`.

The full global action alphabet is the fixed four-symbol set

\[
A_O
=
\{0,1,\mathsf{fire},\mathsf{tick}\}.
\]

## 3. Closed grammar: routing exists, firing does not

The closed primitive-action set is

\[
A_C
=
\{0,1,\mathsf{tick}\}.
\]

Thus the only primitive action missing from the closed side is

\[
\boxed{
A_O\setminus A_C=\{\mathsf{fire}\}.
}
\]

The declared finite closed grammar contains every binary address prefix and idle
`tick` tails up to the relay depth bound. The selector therefore genuinely moves
through the tree under closed operation. The closed dynamics are not an identity
system.

However, no fire action is legal. The relay begins quiescent, address actions move
only the selector marker, and idle ticks have no pulse to propagate. Therefore no
dormant memory bit can enter the focal channel.

For every declared closed word `w`,

\[
\operatorname{Tr}((y,b_1,\ldots,b_m),w)
\]

is a repetition of `y` and is independent of all `b_j`.

Hence the exact closed quotient is

\[
\boxed{|P_C|=2}
\]

and

\[
K_C=1.
\]

If this one closed quotient is viewed through the three-term inflation
decomposition, its shared-base join/refinement capacity is also exactly two:

\[
C=2,
\qquad
\delta_{\rm join}=0.
\]

There is therefore no hidden static join capacity waiting to explain a later
blow-up.

## 4. Open grammar: enable one primitive action

Opening the system legalizes the one primitive action

\[
\mathsf{fire}.
\]

No new address symbols, tick symbols, node types, edge types, or global port
labels are added.

For leaf `j`, the already defined binary-address probe is

\[
w_j
=
\operatorname{addr}(j)
\;\mathsf{fire}\;
\mathsf{tick}^{d+1}.
\]

Its length is

\[
|w_j|=2d+2=2\log_2m+2.
\]

The final focal output is

\[
\operatorname{last}\operatorname{Tr}(s,w_j)=b_j.
\]

The empty/current response supplies `y`, and the `m` addressed words supply all
`m` dormant memory coordinates. Thus every pair of distinct macrostates is
separated by the full open grammar:

\[
\boxed{|P_O|=2^{m+1}}
\]

and

\[
K_O=m+1.
\]

## 5. Pure open-only innovation

Because the closed-union quotient and its join capacity both have two states,

\[
|P_U|=C=2.
\]

Therefore

\[
\delta_{\rm join}
=
\log_2C-\log_2|P_U|
=0.
\]

The open-only innovation is

\[
\boxed{
\iota_{\rm new}
=
\log_2|P_O|-\log_2|P_U|
=m.
}
\]

The total gap is likewise

\[
\boxed{
K_O-K_C=m.
}
\]

Thus the entire linear interface inflation lies outside the static natural-join
explanation of the closed response views.

## 6. CORE-5 as a local witness

Take two states with the same focal bit and different dormant memory at leaf `j`:

\[
s=(y,\ldots,b_j=0,\ldots),
\qquad
t=(y,\ldots,b_j=1,\ldots).
\]

Every closed word gives the same focal trace from `s` and `t`. The newly available
addressed word `w_j`, which necessarily contains `fire`, gives different traces.

This is exactly the logical form of the historical newly-legal-word / fiber-split
obstruction. In the new decomposition language, it is a local certificate that

\[
\iota_{\rm new}>0.
\]

The construction strengthens that local statement quantitatively: one newly
legal primitive action creates `m` bits of total innovation across the family.

## 7. Locality and alphabet contract

For every `m=2^d`:

- newly legal primitive action types: `1` (`fire` only);
- full global action alphabet size: `4`;
- maximum network degree: `3`;
- selector motion: pairwise parent--child;
- pulse motion: pairwise child--parent;
- local state/message alphabets: constant in `m`;
- worst-case addressed read length: `2 log2(m) + 2`.

The number of distinct addressed **words** is still `m`. The theorem does not
claim a constant number of queries or constant query length.

## 8. What is and is not being claimed

The following are not novelty claims:

- that adding an action can refine an observational equivalence;
- that an extra experiment can reveal previously hidden state;
- the logarithmic identity defining `iota_new`;
- binary routing itself.

The intended sharpness statement is the simultaneous combination:

> a single new primitive action can turn a constant exact closed interface into an
> interface requiring `m` additional bits, even though the routing actions were
> already legal, the static closed-view join capacity is constant, the global
> alphabet remains size four, and the realization uses only bounded-degree
> pairwise local dynamics with constant local grammar.

This should be treated as a novelty candidate only after comparison with automata
alphabet-extension/state-complexity results, interface refinement, active tests,
and causal abstraction under changing intervention sets.

## 9. Executable certificate

`causal_model.single_action_innovation` provides:

- `closed_fire_free_words(m)`: the finite routing/tick closed grammar;
- `open_addressed_probe_words(m)`: one read word per dormant leaf;
- `SingleActionInnovationCertificate`: exhaustive closed/open response signatures,
  the exact interface-inflation decomposition, degree/alphabet checks, and the
  `m`-bit innovation identity;
- `RelayInnovationSplitWitness`: one concrete closed-equivalent pair split by an
  addressed word containing the newly legal `fire` action.

Finite replay checks powers of two supplied to the certificate; the all-size
argument is the symbolic relay invariant above.
