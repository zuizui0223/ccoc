# Bounded-degree causal-cone interface capacity

> **Status:** post-reopening locality closure for the CCOC sharpness family.
> The radius-`T` locality principle is classical distributed-computing substrate,
> not a novelty claim. The purpose here is to remove the selector/prefix-code
> assumptions from the **order** lower bound on CCOC query latency.

## 1. Why a more general locality statement is useful

The addressed relay already has an exact latency lower bound inside its specific
selector-plus-return-path architecture:

\[
L_{\rm query}^{\rm worst}
\ge
2\lceil\log_2m\rceil+2,
\]

with equality for the balanced power-of-two family.

That exact proof uses two architecture-specific facts:

1. terminal memories have prefix-free binary selector addresses; and
2. after selection, the memory pulse returns along the same local tree.

To establish that the logarithmic scale is not an artefact of that addressing
scheme, we can use a weaker and much more general local-causality premise.

## 2. Local controlled-network contract

Let

\[
G=(V,E)
\]

be a finite undirected graph with focal node `o`.
Node `v` has a finite local state set

\[
Q_v.
\]

At each synchronous round `t`, an externally supplied global control symbol
`a_t` may be visible to every node.  The control word is known to the experimenter
and does **not** contain hidden information about the unknown initial state.

The locality premise is:

> the next local state of node `v` depends only on `a_t`, the current state of
> `v`, and the current states/messages of neighbors of `v`.

The focal observable at each time is a function only of the focal node's current
local state.

This allows globally broadcast control but forbids instantaneous nonlocal transfer
of hidden initial-state information.

## 3. Causal-cone lemma

Let

\[
B_T(o)=\{v\in V:\operatorname{dist}(v,o)\le T\}.
\]

### Lemma

For every fixed control word `w` of length at most `T`, the focal output trace
under `w` is a function only of the initial configuration restricted to
`B_T(o)`.

### Proof

Induct on time.

At time zero, the focal output depends only on the initial state of `o`, hence on
`B_0(o)`.

Assume every node's state at time `t` depends only on initial states within graph
distance `t` of that node, together with the known control prefix.  At time
`t+1`, node `v` reads only itself and adjacent nodes.  Every such neighbor's time
`t` state depends only on initial nodes within distance `t` of that neighbor, all
of which lie within distance `t+1` of `v`.  Hence the time-`t+1` state of `v`
depends only on its radius-`t+1` initial neighborhood.

Taking `v=o` proves the claim for every focal output up to time `T`. `square`

### Immediate indistinguishability consequence

If two global initial states agree on `B_T(o)`, then **no collection of legal
control words of length at most `T`** can distinguish them by the focal response.
The words may be adaptive or chosen from a very large family; the initial hidden
information available to the focal response still lies inside the same causal
cone.

## 4. Horizon interface-capacity bound

Let `D` be a declared comparison domain of initial global states.  Define the
horizon-`T` exact response equivalence by agreement of focal traces for every
legal word of length at most `T`, and let `N_T` be the number of quotient classes.

The initial configuration on `B_T(o)` has at most

\[
\prod_{v\in B_T(o)}|Q_v|
\]

possible values.  Because the complete horizon-`T` response signature factors
through that local configuration,

\[
\boxed{
N_T
\le
\prod_{v\in B_T(o)}|Q_v|.
}
\]

Equivalently, with

\[
K_T=\log_2N_T,
\]

\[
\boxed{
K_T
\le
\sum_{v\in B_T(o)}\log_2|Q_v|.
}
\]

This heterogeneous form is the most precise finite statement.

If every local state set has size at most `q`, then

\[
\boxed{
K_T\le |B_T(o)|\log_2q.
}
\]

## 5. Maximum-degree ball growth

Let the graph have maximum degree `Delta`.

For `Delta=0`,

\[
|B_T(o)|\le1.
\]

For `Delta=1`,

\[
|B_0(o)|=1,
\qquad
|B_T(o)|\le2\quad(T\ge1).
\]

For `Delta=2`, the extremal ball is a path through the focal node:

\[
\boxed{|B_T(o)|\le1+2T.}
\]

For `Delta\ge3`, a breadth-first tree gives

\[
|B_T(o)|
\le
1+\Delta\sum_{r=0}^{T-1}(\Delta-1)^r,
\]

so

\[
\boxed{
|B_T(o)|
\le
1+
\Delta\frac{(\Delta-1)^T-1}{\Delta-2}.
}
\]

Hence a system whose horizon-`T` focal quotient has `N_T` classes must satisfy

\[
\log_2N_T
\le
\left(
1+
\Delta\frac{(\Delta-1)^T-1}{\Delta-2}
\right)
\log_2q.
\]

For fixed `Delta>=3` and fixed `q`, if

\[
N_T=2^{\Theta(m)},
\]

then necessarily

\[
\boxed{T=\Omega(\log m).}
\]

This conclusion does not assume a binary selector, prefix-free addresses, or a
specific return route.

## 6. Relation to the CCOC single-action family

The CCOC relay realizes an open quotient on the quiescent comparison domain with

\[
N=2^{m+1}
\]

response classes after `fire` becomes legal.

Its declared distributed implementation has:

- maximum degree `Delta=3`;
- constant local node/message state alphabets;
- radius-one selector and pulse updates.

A conservative uniform local-state bound is `q=12` for the selector-augmented
leaf alphabet; relay and focal nodes use fewer states.

Therefore any realization satisfying the same **bounded-degree, bounded-local-
state, radius-one causal contract** requires horizon

\[
T=\Omega(\log m)
\]

to expose all `2^(m+1)` exact response classes at the focal output.

The current addressed relay uses

\[
T_{\rm relay}=2\log_2m+2,
\]

so it remains **order-optimal** in this broader locality class.

The earlier exact equality

\[
T=2\log_2m+2
\]

is stronger but applies only to the narrower selector-plus-same-tree-return
architecture.  The two claims should not be conflated.

## 7. Why bounded degree alone is insufficient

The causal-cone theorem depends on **local propagation**, not graph degree by
itself.

Consider two disconnected binary-state nodes, focal `o` and remote `r`.
The radius-one ball around `o` contains only `o`, so its local configuration has
two possibilities.  If one nevertheless permits a forbidden nonlocal update

\[
q_o(t+1)=q_r(t),
\]

then a one-step focal trace can expose the remote initial bit despite there being
no graph path at all.

Thus a degree bound without a local-update contract gives no propagation-speed
lower bound.  CCOC must continue to state the locality premise explicitly.

## 8. Relation to classical locality theory

This causal-cone statement is not novel.  It is the same basic locality principle
that underlies the LOCAL model of distributed graph algorithms.  Linial's 1992
paper formulates a model in which, in `t` time units, a processor can collect data
only from nodes at graph distance at most `t`.

CCOC therefore does **not** claim novelty for:

- radius-`T` dependence after `T` local rounds;
- graph-ball growth bounds;
- the resulting logarithmic latency lower bound for exponentially many local
  configurations.

Their role is to make the residual CCOC locality claim cleaner:

> the same one-new-action family that attains the absolute maximum exact
> interface innovation also realizes it in `O(log m)` rounds on a degree-three
> constant-local-state network, matching the generic bounded-local causal-cone
> lower bound in order.

Whether this **simultaneous extremal restricted-input + local realization** has a
direct historical FSM/circuit precedent remains the unresolved novelty question.

## 9. Executable certificates

`causal_model.local_causal_cone` provides:

- `LocalCausalConeCapacityCertificate`: exact finite graph ball, heterogeneous
  local-state information capacity, and a check of whether a claimed number of
  response classes could fit inside that causal cone;
- `DegreeBoundedCausalConeCertificate`: universal maximum-degree / uniform-local-
  state ball capacity and minimum compatible horizon;
- `radius_ball`, `maximum_degree_ball_size`, and
  `minimum_degree_bounded_horizon` utilities.

These certificates replay graph/state-capacity arithmetic.  They do not infer
that arbitrary transition code satisfies the radius-one locality premise; that is
an explicit model contract established separately by the construction/proof.
