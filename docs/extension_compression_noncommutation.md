# Extension--compression noncommutation

## The question

A system can admit a small causal interface after its future ecological context is
fixed, yet require its full microstate when it must remain correct under every
future connection allowed by a declared port grammar.

The result in this document is intentionally finite and deterministic. It is a
no-go witness, not a claim that all ecosystems have this form.

## Declared finite domain

For every integer \(m\ge1\), define

\[
X_m=\{0,1\}^{m+1}.
\]

Write a state as

\[
x=(y,b_1,\ldots,b_m),
\]

where \(y\) is the focal boundary output and \(b_i\) is dormant memory at
attachable port \(i\). The declared output is \(Y(x)=y\).

The action `probe:i` copies bit \(b_i\) into the focal output:

\[
F_i(y,b_1,\ldots,b_m)
=
(b_i,b_1,\ldots,b_m).
\]

`observe` and `idle` leave the state unchanged.

A **closed context** \(E_i\) permits only `observe`, `idle`, and `probe:i`.
The declared **open port grammar** permits `observe`, `idle`, and every
`probe:i` for \(i=1,\ldots,m\). This is the only sense in which the theorem
uses “open”: it does not quantify over unspecified arbitrary environments.

## Exact causal interfaces

An interface is sound for a declared action set when equal interface states have
identical output traces under each allowed action and transition to equal
interface states afterwards.

For a closed context \(E_i\), the map

\[
\phi_i(y,b_1,\ldots,b_m)=(y,b_i)
\]

is sound. Its quotient dynamics are

\[
(y,b)\xrightarrow{\mathrm{idle}}(y,b),
\qquad
(y,b)\xrightarrow{\mathrm{probe}:i}(b,b).
\]

All four pairs \((y,b)\in\{0,1\}^2\) occur and are distinguishable by either
current output or the probe response. Thus the closed quotient is exactly four
states, requiring two bits.

For the open grammar, two distinct states are always separated in one step:

- if their \(y\) coordinates differ, `observe` separates them;
- otherwise some \(b_i\) differs, and `probe:i` separates them through the
  next focal output.

Therefore every sound open interface must be injective on \(X_m\).

## Theorem: extension--compression noncommutation witness

For every \(m\ge1\), there is a finite deterministic focal-bit system with
\(m\) declared attachable ports such that

\[
\max_{1\le i\le m}
\kappa(M_m\parallel E_i)=2,
\qquad
\kappa_{\mathrm{open}}(M_m;\mathcal E_m)=m+1,
\]

where \(\kappa\) is the base-two logarithm of the number of blocks in the
coarsest sound causal-interface partition.

Equivalently,

\[
\text{every fixed closed context has a four-state macro-law},
\]

while

\[
\text{the interface safe for all permitted future attachments has }
2^{m+1}\text{ states}.
\]

### Proof

The closed upper bound follows from \(\phi_i=(y,b_i)\). The closed lower bound
follows because the four values of \((y,b_i)\) differ in either current output
or in the output after `probe:i`.

For the open lower bound, take distinct \(x,x'\in X_m\). If \(y\ne y'\),
`observe` gives distinct traces. If \(y=y'\), some \(b_i\ne b_i'\), so
`probe:i` gives distinct next focal outputs. Hence no two distinct states may be
merged by an open-safe interface. The identity partition is itself sound, so it
is the coarsest open-safe partition. \(\square\)

## Constant-grammar bounded-degree implementation

The coordinate witness is now compiled by
[`relay_tree_compilation.py`](../causal_model/relay_tree_compilation.py) into a
one-token binary relay tree. It uses one fixed finite grammar—reader, memory
leaf, relay, and focal root—together with child-to-parent pairwise messages and
maximum graph degree three.

At **quiescent macro-time**, firing a reader at port \(i\) and allowing the tree
to settle implements exactly the coordinate action \(F_i\). The compiled
protocol therefore preserves the four-state closed quotients and the
\(2^{m+1}\)-state open quotient by exact macro-time conjugacy. See
[bounded-degree relay-tree compilation](bounded_degree_relay_compilation.md).

The declared action grammar remains sequential: one reader may fire, the tree
must settle, and only then may the next reader fire. Simultaneous reader
activations are intentionally outside the theorem domain.

## What is—and is not—shown

This result shows that causal compression for every fixed closed extension need
not yield a small interface for the corresponding declared open composition.
It does not show that open-system abstraction is impossible in general.

It also does not claim that every ecological network has relay-tree dynamics.
The theorem is a sharp existence witness: the noncommutation persists despite a
fixed finite grammar, pairwise edge-local messages, and bounded degree. A
separate theorem would be needed for stochastic, continuous, simultaneous, or
empirically calibrated ecological systems.

Finally, an extension-safe interface is not automatically a single
candidate-independent deterministic macro update. The latter needs a separate
uniform-dynamics condition.

## Executable finite regression

`causal_model.extension_compression` provides explicit one-step
`TraceSeparationCertificate` objects for every unequal coordinate-state pair.
`causal_model.relay_tree_compilation` provides replayable protocol certificates
that prove each completed relay-tree macro probe equals its coordinate action.
The workflows verify both witness families for \(m=1,\ldots,6\), writing
deterministic JSON artifacts. These finite regressions check declared families;
the written proofs supply the all-\(m\) arguments.
