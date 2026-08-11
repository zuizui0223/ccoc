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

> Can the open-only innovation term become large even when every fixed closed
> composition has a constant exact interface and their entire static join
> capacity remains constant?

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

There are `m` fixed closed contexts, one associated with each dormant module. The
relay topology is common to all contexts and has maximum degree three. Selector
transfer and pulse transfer are pairwise adjacent-node updates. Local
selector/pulse/memory state alphabets do not grow with `m`.

The full global action alphabet is the fixed four-symbol set

\[
A_O
=
\{0,1,\mathsf{fire},\mathsf{tick}\}.
\]

## 3. Fixed closed contexts: routing exists, firing does not

The closed primitive-action set is

\[
A_C
=
\{0,1,\mathsf{tick}\}.
\]

Thus the only primitive action missing from every closed context is

\[
\boxed{
A_O\setminus A_C=\{\mathsf{fire}\}.
}
\]

For closed context `j`, the declared finite word family contains every prefix of
the binary route from the relay-body root toward leaf `j`, together with bounded
idle `tick` tails. The selector therefore genuinely moves through the tree under
closed operation. The closed dynamics are not an identity system.

However, no fire action is legal in any fixed context. The relay begins
quiescent, address actions move only the selector marker, and idle ticks have no
pulse to propagate. Therefore no dormant memory bit can enter the focal channel.

For every fixed context `j` and every declared word `w in L_j`,

\[
\operatorname{Tr}((y,b_1,\ldots,b_m),w)
\]

is a repetition of `y` and is independent of all `b_k`.

Hence every exact fixed-context quotient is

\[
\boxed{|P_j|=2},
\qquad j=1,\ldots,m,
\]

and

\[
K_j=1.
\]

Taking the union of **all** fire-disabled closed grammars only makes all address
prefixes available together. Since no context contains `fire`, the closed-union
quotient is still

\[
\boxed{|P_U|=2}.
\]

Because every `P_j` equals the shared focal/base partition on response classes,
the fibered static join/refinement capacity is likewise

\[
\boxed{C=2}
\]

and

\[
\delta_{\rm join}=0.
\]

There is therefore no hidden multiplicative closed-view capacity waiting to
explain a later blow-up.

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

The current focal response supplies `y`, and the `m` addressed words supply all
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

Since

\[
|P_U|=C=2,
\]

we have

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

The total gap against the largest fixed closed interface is likewise

\[
\boxed{
K_O-\max_jK_j=m.
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

They are equivalent in every fixed closed context and under the union of all
closed grammars. The newly available addressed word `w_j`, which necessarily
contains `fire`, gives different focal traces.

This is exactly the logical form of the historical newly-legal-word / fiber-split
obstruction. In the new decomposition language, it is a local certificate that

\[
\iota_{\rm new}>0.
\]

The construction strengthens that local statement quantitatively: one newly
legal primitive action creates `m` bits of total innovation across the family.

## 7. Locality and alphabet contract

For every `m=2^d`:

- number of fixed closed contexts: `m`;
- exact states per closed context: `2`;
- exact states in their closed union: `2`;
- static shared-view join capacity: `2`;
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

> every fixed closed composition has a one-bit exact causal law, the union of all
> closed grammars is still one bit, and the static join capacity remains one bit,
> yet legalizing one primitive action creates `m` additional exact causal bits;
> this occurs even though routing dynamics were already legal and the realization
> uses a four-symbol global alphabet, bounded degree, pairwise locality, and
> constant local grammar.

This should be treated as a novelty candidate only after comparison with automata
alphabet-extension/state-complexity results, interface refinement, active tests,
and causal abstraction under changing intervention sets.

## 9. Executable certificate

`causal_model.single_action_innovation` provides:

- `closed_context_fire_free_words(m,j)`: one fixed fire-disabled closed grammar per
  dormant module;
- `closed_fire_free_words(m)`: the union of all fixed closed grammars;
- `open_addressed_probe_words(m)`: one read word per dormant leaf;
- `SingleActionInnovationCertificate`: exhaustive per-context, closed-union, and
  open response signatures; the exact interface-inflation decomposition;
  degree/alphabet checks; and the `m`-bit innovation identity;
- `RelayInnovationSplitWitness`: one concrete closed-union-equivalent pair split
  by an addressed word containing the newly legal `fire` action.

Finite replay checks powers of two supplied to the certificate; the all-size
argument is the symbolic relay invariant above.
