# Bounded-degree relay-tree compilation

## Why this extension matters

The first extension--compression theorem used coordinates directly:

\[
(y,b_1,\ldots,b_m)
\xrightarrow{\mathrm{probe}:i}
(b_i,b_1,\ldots,b_m).
\]

That exact witness establishes the information-theoretic separation, but by
itself does not show that the rule can arise from a fixed local interaction
vocabulary. This document gives an exact compilation into a finite one-token
relay network.

The resulting theorem is still a deliberately narrow deterministic witness. Its
value is that the compression failure does **not** rely on a growing local rule
table, direct root access to all memory bits, or unbounded node degree.

## Constant grammar

Every system size uses the same four local module types.

| Module | Local state | Local update role |
|---|---:|---|
| Reader | `ready`, `fire` | A boundary intervention sets `fire` for one tick. |
| Memory leaf | \(b\in\{0,1\}\) and pulse \(p\in\{\varnothing,0,1\}\) | On `fire`, emit its stored bit upward once. |
| Relay | pulse \(p\in\{\varnothing,0,1\}\) | Copy the unique incoming child message upward one tick later. |
| Root output | \(y\in\{0,1\}\) | Replace \(y\) by its unique incoming message when one arrives. |

The message alphabet is fixed:

\[
\{\varnothing,0,1\}.
\]

There are no module types or local state alphabets indexed by \(m\).

## Topology and pairwise message semantics

For \(m\) dormant modules, construct a deterministic balanced binary tree with
\(m\) memory leaves, \(m-1\) relay nodes, and one output root above the tree
body. Directed messages travel only from child to parent.

- A reader has degree 1.
- A leaf with an attached reader has degree at most 2.
- An internal relay has two children and one parent, hence degree 3.
- The output root has degree 1.

Thus the maximum degree is three.

The update of a relay uses only the messages on its two child edges. The declared
one-token grammar permits at most one active reader between quiescent macro
states, so at most one of these pairwise messages is nonempty. A collision is
outside the action grammar and is fail-closed by the verifier. The construction
therefore uses edge-local pairwise messages, not a transition that directly
reads an unbounded set of leaf states.

## Quiescent macro-time

A macro state is a **quiescent** network configuration:

\[
Q(y,b_1,\ldots,b_m),
\]

where every transient leaf and relay pulse is empty. The root output is \(y\),
and leaf \(i\) stores \(b_i\).

A macro action `probe:i` means:

1. attach or use the declared reader at leaf \(i\);
2. set that reader to `fire` for one microtick;
3. evolve the fixed local dynamics with no further reader firing until the
   entire tree is quiescent again.

For a leaf at graph distance \(d\) from the output root, its one-token pulse
reaches the root after \(d+1\) microticks. Sampling after the maximum such
delay makes the protocol length uniform across all permitted ports.

## Protocol-conjugacy lemma

For every \(m\ge1\), every quiescent state \(Q(y,b_1,\ldots,b_m)\), and every
port \(i\), the completed relay protocol satisfies

\[
\operatorname{Probe}^{\mathrm{tree}}_i
\bigl(Q(y,b_1,\ldots,b_m)\bigr)
=
Q(b_i,b_1,\ldots,b_m).
\]

### Proof

At the firing tick, exactly leaf \(i\) contains pulse \(b_i\); every other
leaf pulse is empty. At each later microtick, the pulse advances over exactly
one child-to-parent edge. The one-token invariant guarantees that each relay
has at most one nonempty child message, so it copies that message unchanged.
When the pulse reaches the one child edge of the output root, the root replaces
its output by \(b_i\). All pulse registers then clear on the next local update
or have already cleared; after the declared maximum settling time all are empty.
The permanent leaf bits never change. \(\square\)

The map from quiescent tree states to coordinate states,

\[
Q(y,b_1,\ldots,b_m)
\longmapsto
(y,b_1,\ldots,b_m),
\]

therefore conjugates every completed tree macro probe to the original coordinate
probe.

## Corollary: bounded-degree extension--compression separation

Fixing a closed context with a reader only at port \(i\) leaves the exact
four-state quotient

\[
(y,b_i).
\]

Allowing any declared port to be attached and fired in a future context restores
the open action family \(\{\mathrm{probe}:1,\ldots,\mathrm{probe}:m\}\). By
protocol conjugacy, the coordinate witness lower bound applies verbatim:

\[
\boxed{
\max_i \kappa(M_m\parallel E_i)=2,
\qquad
\kappa_{\mathrm{open}}(M_m;\mathcal E_m)=m+1.
}
\]

Equivalently, every fixed closed context has a four-state macro-law, while the
quiescent interface safe for all declared future reader attachments has
\(2^{m+1}\) states.

## Scope boundary

The theorem does **not** say that every ecological interaction network behaves
like a relay tree. It says something narrower and sharper:

> Even with one fixed finite local grammar, edge-local pairwise messages, maximum
> degree three, and a sequential one-token intervention grammar, causal
> compression valid in every fixed closed extension need not survive the declared
> open composition.

Simultaneous reader firings, stochastic updates, continuous state spaces,
unbounded-degree hubs, and arbitrary unmodelled environments are not in the
claim. They require separate theorem domains.

## Executable regression

`causal_model.relay_tree_compilation` provides a replayable protocol certificate
for each state/port pair. The GitHub Actions regression enumerates all coordinate
states and all ports for \(m=1,\ldots,6\), checks macro conjugacy, verifies the
degree bound, and writes a deterministic JSON report.
