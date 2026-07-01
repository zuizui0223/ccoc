# Degree-three compilation of the binary joint witness

## What this theorem closes

The joint exterior–mechanism theorem establishes an exact lower bound for

\[
I\times E_1\times\cdots\times E_m\times R.
\]

Its canonical witness uses structural port contexts and a fixed action alphabet,
but the theorem intentionally did not claim a bounded-degree micro-realization
for arbitrary multi-valued `read` or response-type arithmetic.

This module closes the exact **binary** subfamily:

\[
(y,b_1,\ldots,b_m,r)\in\{0,1\}^{m+2}.
\]

It is not a hidden claim about the whole multi-valued theorem family.

## Binary joint macro law

There are three declared macro actions:

\[
\begin{array}{rcl}
\operatorname{observe}(y,b_1,\ldots,b_m,r)
&=&(y,b_1,\ldots,b_m,r),\\[4pt]
\operatorname{read}_i(y,b_1,\ldots,b_m,r)
&=&(b_i,b_1,\ldots,b_m,r),\\[4pt]
\operatorname{intervene}(y,b_1,\ldots,b_m,r)
&=&(y\oplus r,b_1,\ldots,b_m,r).
\end{array}
\]

Because the original canonical product uses addition modulo its inside
cardinality, this is exactly its

\[
I=E_i=R=2
\]

restriction:

\[
y+r\pmod2=y\oplus r.
\]

## Local architecture

Use a rooted balanced binary relay tree with:

- one exterior-memory leaf for each \(b_i\);
- one extra permanent response-type leaf holding \(r\);
- binary relay nodes; and
- a focal root holding \(y\).

At any macro boundary all transient tokens are empty. One declared macro action
starts at quiescence and the tree must settle before another action may start.

The fixed token alphabet is

\[
\boxed{
\{\varnothing,\operatorname{copy}\!\text{-}0,
\operatorname{copy}\!\text{-}1,
\operatorname{xor}\!\text{-}0,
\operatorname{xor}\!\text{-}1\}.
}
\]

Every relay simply forwards the unique nonempty child-to-parent token. The root
is the only node with two token interpretations:

\[
\operatorname{copy}\!\text{-}v:
\quad y\leftarrow v,
\]

\[
\operatorname{xor}\!\text{-}v:
\quad y\leftarrow y\oplus v.
\]

The local node and message grammar therefore remains finite as \(m\) grows.

## Structural contexts, not growing action labels

For `read`, a reader attaches to exterior leaf \(i\). The selected leaf emits

\[
\operatorname{copy}\!\text{-}b_i.
\]

For `intervene`, the reader attaches to the one fixed response-type leaf, which
emits

\[
\operatorname{xor}\!\text{-}r.
\]

The port is carried by graph attachment, not by a local action token such as
`read:i`. Response type is a stored mechanism bit, not an action label such as
`intervene:r`.

## Theorem — Binary joint relay compilation

For every \(m\ge1\), the binary joint macro law above has an exact sequential
micro-realization with:

\[
\boxed{
\begin{array}{c}
\text{one fixed finite local node/message grammar},\\
\text{edge-local child-to-parent pairwise tokens},\\
\max\deg\le3\text{ including the active reader edge},\\
\text{and quiescent macro-time conjugacy.}
\end{array}
}
\]

### Proof

Fix a quiescent configuration representing
\((y,b_1,\ldots,b_m,r)\).

For `read_i`, the attached reader starts exactly one token
\(\operatorname{copy}\!\text{-}b_i\) at leaf \(i\). Binary relays forward
that token along the unique leaf-to-root path. At the root, the copy rule sets
\(y\) to \(b_i\); all permanent leaf bits remain unchanged. After at most the
leaf-to-root distance plus one ticks, the token has been consumed and the tree
is quiescent again.

For `intervene`, the fixed response leaf starts
\(\operatorname{xor}\!\text{-}r\). The same pairwise relay propagation delivers
it to the root, which applies \(y\leftarrow y\oplus r\). Permanent exterior and
response bits again remain unchanged.

`observe` is the quiescent identity macro action. Hence every macro action has
exactly the stated successor. The tree is binary and each active leaf gains at
most one reader edge, so its maximum degree is three. \(\square\)

## Exact certification

`BinaryJointRelayCompilationCertificate` exhausts every quiescent binary macro
state and all declared actions:

\[
2^{m+2}
\]

states, with

\[
m\,2^{m+2}
\]

read protocols plus one observe and one intervene protocol per state. Each
protocol replays its local microtrajectory, verifies restored quiescence, checks
the degree bound, and compares its macro successor directly to the existing
`JointOpenCandidateProduct` restricted to the binary parameters.

The replay is a finite certificate check for the declared family, not evidence
for arbitrary ecosystems.

## What remains open

This theorem does **not** compile:

- arbitrary multi-valued exterior registers;
- a streamed multi-bit read protocol;
- general modular update \(y\leftarrow y+r\pmod I\) for \(I>2\); or
- simultaneous readers / multiple in-flight tokens.

Those require a further compiler theorem with a finite streaming token alphabet,
structural register layout, and a precise carry or modular-reduction protocol.
The binary result is valuable because it removes the high-degree and growing
lookup objections from the exact joint lower-bound subfamily without smuggling
in any of those stronger claims.

## Ecological projection

This remains a robustness theorem about a finite witness. It does not say a
field boundary or ecological interaction network is literally a binary tree.
Its role is narrower: the binary joint lower bound does not depend on a focal
node with unbounded degree or on a port-specific local action alphabet.