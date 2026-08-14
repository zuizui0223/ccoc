# Spatial dispersal reachability: future depth determines exact causal memory

> **Status:** exact spatial ecological structural theorem for monotone directed dispersal. The microstate is an arbitrary occupied-patch subset, so the state space has `2^|V|` elements. Under synchronous one-edge wave spread, focal response equivalence collapses to directed distance-to-focal. A finite legal future horizon yields a graph-size-independent exact grammar-aware interface; unlimited reachability depth destroys that uniform bound. Shortest paths and wavefront propagation are classical substrate; the CCOC-specific content is the future-grammar causal-memory interpretation.

## 1. Spatial model

Let

\[
G=(V,E)
\]

be a finite directed dispersal graph with focal patch

\[
o\in V.
\]

A microstate is an arbitrary occupied set

\[
S\subseteq V.
\]

Thus the microstate space has

\[
2^{|V|}
\]

states.

The focal response is

\[
Y(S)=\mathbf 1\{o\in S\}.
\]

One primitive dispersal action `spread` expands the occupied set by one directed edge:

\[
\Phi(S)
=
S\cup\{v:\exists u\in S\text{ with }(u,v)\in E\}.
\]

Occupancy is monotone: colonized patches remain occupied.

## 2. Directed distance summary

For a patch `v`, let

\[
d(v,o)
\]

be its shortest directed path length to the focal patch, with `infinity` if no directed path exists.

For an occupied set define

\[
d(S,o)=\min_{v\in S}d(v,o),
\]

again using `infinity` if no occupied patch can reach the focal target.

If `d(S,o)=d` is finite and positive, then

\[
\boxed{
d(\Phi(S),o)=d-1.}
\]

If `d=0`, it remains zero. If `d=infinity`, it remains infinite.

### Proof

Take an occupied patch on a shortest `d`-edge path to the focal target. Its first outgoing successor on that path is added by one spread step and has distance `d-1`, so the new occupied set has distance at most `d-1`.

It cannot have smaller finite distance: if one newly occupied successor had distance `<d-1`, its occupied predecessor would have had a path to the focal target shorter than `d`, contradicting minimality. Existing occupied patches also had distance at least `d`.

Unreachable occupied components cannot acquire a reachable successor, because an edge from an unreachable patch to a reachable patch would itself form a directed route to the focal target. `□`

Therefore the distance variable evolves autonomously under `spread`:

\[
d\mapsto
\begin{cases}
0,&d=0,\\
d-1,&1\le d<\infty,\\
\infty,&d=\infty.
\end{cases}
\]

## 3. Unlimited future theorem

Suppose `spread` may be repeated arbitrarily many times.

If `d(S,o)=d<infinity`, the focal response trace consists of `d` initial non-focal steps followed by focal presence forever. If `d=infinity`, the focal response remains zero forever.

Hence two occupied sets are future-response equivalent if and only if they have the same directed distance to the focal target.

Let

\[
D=\max\{d(v,o):d(v,o)<\infty\}.
\]

Every distance `0,1,...,D` occurs along a shortest path from a patch at distance `D`, and the empty occupied set supplies the unreachable class. Thus the canonical unlimited response quotient has exactly

\[
\boxed{|P_\infty|=D+2}
\]

classes:

\[
0,1,\ldots,D,\infty.
\]

The exact spatial interface is therefore independent of the number of occupancy configurations but not necessarily independent of directed reachability depth.

## 4. Finite future grammar

Now let the legal future grammar permit at most

\[
H
\]

spread actions.

The grammar state records the number `u` of spreads already used. The remaining future depth is

\[
h=H-u.
\]

Define the grammar-adaptive distance cap

\[
\boxed{
Z_u(S)
=
\min\{d(S,o),h+1\},
}
\]

where `infinity` is mapped to `h+1`.

Thus `Z_u=h+1` means only

> the focal patch cannot be reached within the remaining `h` spread actions.

It deliberately merges finite distances beyond the legal horizon with truly unreachable states, because the declared future cannot distinguish them.

## 5. Theorem — grammar-adaptive capped distance is exact

The pair

\[
\boxed{(u,Z_u)}
\]

is an exact grammar-aware dynamic interface.

When `u<H`, one spread action changes the grammar state to `u+1`, so the remaining horizon changes from `h` to `h-1`. The summary transition is

\[
\boxed{
(u,z)\mapsto(u+1,\max\{0,z-1\}).
}
\]

This formula also handles the tail state. If `z=h+1`, the true distance is at least `h+1` or infinite. After one spread it is at least `h` or infinite, and the new cap is exactly `h`.

Current focal output is determined by

\[
Y=1\iff z=0.
\]

Legal-action availability is determined by `u`, and the successor summary is determined by `(u,z)`. Hence the grammar-aware local exactness conditions hold, so all legal future response traces factor through this finite summary. `□`

## 6. Sharp initial quotient under H-step futures

At the initial grammar state `u=0`, the summary is

\[
Z_0(S)=\min\{d(S,o),H+1\}.
\]

Finite distance shells

\[
0,1,\ldots,\min(D,H)
\]

are distinguishable by the time at which focal occupancy first appears. Every finite distance greater than `H`, together with `infinity`, produces all-zero focal response through the entire legal horizon and belongs to one tail class.

Therefore the canonical initial quotient has exactly

\[
\boxed{
|P_H|=\min(D,H)+2.
}
\]

The executable certificate checks this formula against the canonical grammar-aware quotient, not only against the proposed summary.

Special cases:

- `H=0`: two classes, focal occupied now versus not occupied now;
- `0<H<D`: distance shells only through `H`, plus one future-silent tail;
- `H>=D`: the finite-horizon quotient equals the unlimited quotient `D+2`.

## 7. Changing-graph portability

Fix a legal future horizon `H`, but allow the directed graph, patch number, and maximum directed distance to change across systems.

Every graph has

\[
|P_H|\le H+2.
\]

Thus there is a system-size-independent exact initial memory bound

\[
\boxed{K_H\le\log_2(H+2)}
\]

for arbitrarily large spatial graphs and arbitrarily many occupancy configurations, provided the future grammar allows only `H` spread steps.

This is a changing-domain portability statement: different graphs have different vertex sets and microstate spaces, but the same grammar-adaptive distance semantics bounds their exact focal response interface.

By contrast, under unlimited spread futures,

\[
|P_\infty|=D+2.
\]

A family of directed path graphs with increasing path length `D` therefore has no uniform finite exact unlimited-horizon interface:

\[
\boxed{|P_\infty|\to\infty\quad\text{as }D\to\infty.}
\]

Yet for fixed `H`, the same path family saturates at only

\[
\boxed{H+2}
\]

initial response classes once `D>=H`.

## 8. Barrier interpretation

An occupied patch with no directed route to the focal target has distance `infinity`. All such unreachable occupancy configurations belong to one future-silent class for every spread horizon.

Therefore a **true directed dispersal barrier** can make arbitrarily complicated exterior occupancy causally irrelevant to the focal response. This is stronger than a small undirected cut or sparse topology: the relay theorem already showed those geometric properties alone do not imply a small causal interface.

The relevant spatial property is directional reachability under the declared ecological dynamics.

Likewise, a long but finite corridor is not equivalent to a barrier. It is invisible only when its directed distance exceeds the legal future horizon. Expanding the future grammar can eventually resolve deeper distance shells.

## 9. CCOC interpretation

The theorem gives a spatial counterpart to the abundance disturbance-budget result.

For abundance saturation,

\[
\text{memory cap}
=
\text{response threshold}
+
\text{maximum legal downward reach}.
\]

For spatial dispersal,

\[
\boxed{
\text{needed reachability depth}
=
\text{maximum spatial depth the legal future can probe}.
}
\]

A present occurrence does not merely say that a patch is environmentally admissible; under the declared spread dynamics it also carries information about **how many causal steps separate occupied exterior states from the focal location**.

The future grammar determines which of those spatial distinctions must be retained.

## 10. Relation to occurrence/reachability ideas

The result is deliberately mechanistic rather than an SDM claim. It does not infer a dispersal graph or barrier from occurrence data. But it formalizes a useful distinction:

- environmental suitability asks whether a state can persist at a location;
- directed reachability asks whether a currently occupied state can causally arrive at the focal location under allowed movement dynamics;
- the CCOC interface asks how much of that reachability structure must be remembered to preserve future focal responses.

This gives a mathematical route for later connecting occurrence-based spatial models to causal reachability without treating raster suitability alone as a transition law.

## 11. Claim discipline

Shortest-path distance, breadth-first search, graph reachability, and synchronous wave spread are classical. Do not claim those ingredients as new. The CCOC-specific contribution is the open-composition statement: an exponentially large occupancy state space admits an exact grammar-aware distance blanket whose size is controlled by legal future reachability depth, while removing the horizon bound restores dependence on graph depth.
