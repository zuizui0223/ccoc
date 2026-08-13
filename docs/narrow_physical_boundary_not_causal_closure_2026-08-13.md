# Narrow physical boundary does not imply causal closure — 2026-08-13

> **Status:** ecological interpretation / derived corollary of existing CCOC results. This document adds no theorem-registry claim. It combines the existing relay topology with the existing dynamic-blanket lower bound to make one ecological consequence explicit.

## Statement

A small physical interface between an observed region and its exterior does **not** imply that the exterior admits a small extension-stable causal summary.

The CCOC relay gives an exact finite separation. For every number `m` of binary exterior memories:

1. the focal output node `ROOT` is connected to the entire exterior relay tree through exactly one graph edge, `ROOT -- body_root`;
2. the interaction topology is a **tree** for every `m` (hence acyclic and treewidth one as an undirected graph);
3. every local node/message alphabet remains bounded independently of `m`;
4. the maximum graph degree remains three;
5. after the declared open grammar makes the exterior memories addressable, the exact open response quotient has `2^(m+1)` classes;
6. with the inside/focal bit treated separately, every extension-stable dynamic boundary summary must therefore carry at least `m` bits of exterior information.

Thus one has a family with

\[
\boxed{\text{focal--exterior edge cut}=1}
\]

and an acyclic tree interaction graph for all `m`, but

\[
\boxed{\log_2 |B|\ge m}
\]

for any exact dynamic boundary blanket `B` that supports the declared open future grammar.

Physical cut width and ordinary graph complexity remain minimal while the exact causal-interface memory diverges.

## Derivation from existing results

### Constant physical cut and tree topology

`RelayTreeTopology` constructs a rooted binary tree and then adds a separate focal node `ROOT` above the tree body:

```text
ROOT -> body_root
```

All memory leaves and internal relay nodes lie below `body_root`. Every non-root node has exactly one parent, every relay has two children, and no extra cross-links are added. Removing the one edge `ROOT -- body_root` disconnects the focal node from every exterior memory leaf.

This is true for every `module_count=m`. The construction therefore does not rely on dense connectivity, graph cycles, or growing treewidth.

### Dynamic blanket lower bound

The existing dynamic-boundary-blanket theorem says that when the exterior contains jointly realizable addressable factors

\[
E_1,\ldots,E_m,
\]

then any exact boundary summary used with the inside coordinate must satisfy

\[
|B|\ge \prod_{j=1}^m |E_j|.
\]

For binary exterior factors,

\[
|E_j|=2,
\]

so

\[
|B|\ge 2^m,
\qquad
\log_2|B|\ge m.
\]

The relay realizes the addressability premises while keeping the focal--exterior physical cut equal to one and the underlying interaction graph acyclic.

## What this does and does not mean

This is **not** a new graph-theoretic lower bound and is not claimed as historical firstness. A narrow channel can transmit different information at different times; static cut size alone is not a bound on the complete family of counterfactual response distinctions available over an unrestricted future grammar.

Likewise, acyclicity does not imply causal compressibility. The relay uses local dynamics on a tree, but different legal future control words can query different dormant exterior memories through that same tree.

The useful CCOC distinction is therefore between different notions of complexity:

- **physical boundary width:** how many simultaneous graph connections cross a spatial/interaction cut;
- **static graph complexity:** degree, density, cycles, or treewidth;
- **dynamic causal boundary complexity:** how many exterior response types must be retained so that all declared future interactions remain exactly predictable.

A system may have the first two uniformly bounded while the third grows without bound.

## Ecological interpretation

This blocks two tempting but unsafe inferences:

> a patch, island, population, or community has only a few physical connections to its surroundings, therefore the surroundings can be summarized by a few causal state variables;

and

> a sparse or tree-like interaction network should admit a correspondingly simple open-system macro-law.

The relay shows why both fail in principle. A single corridor, inlet, dispersal gateway, shoreline contact, or interaction interface can expose different exterior states under different future events. The number of simultaneous connections and the apparent static network complexity may stay small while the number of distinguishable future exterior responses grows.

Accordingly, descriptors such as

- edge length or edge count;
- corridor count;
- network density;
- cycle count or tree-likeness;
- number of current immigrants;
- number of currently active interaction links;
- one-time connectivity;

are not by themselves certificates of causal closure.

A closure certificate requires a **dynamic** statement: the exterior effects relevant to every allowed future colonization, reconnection, disturbance, or interaction event must factor through a finite boundary state whose update is itself closed.

## Why this belongs in the manuscript

This consequence gives a sharper ecological reading of the formal results without expanding the theorem spine.

The manuscript can state:

> Physical isolation, sparse topology, and causal compressibility are distinct. Even a single persistent connection in an acyclic interaction network can support an unbounded family of counterfactual exterior distinctions across alternative future interactions. What matters for an exact open-system macro-law is not present boundary width or graph sparsity alone, but whether all future exterior effects factor through a bounded dynamic boundary state.

The relay remains a synthetic witness, not evidence that a real corridor, island, or tree-like ecological network has large causal-interface memory.

## Relation to future ecological mathematics

The corollary also clarifies what a genuinely stronger ecological theorem would have to do. It cannot assume that a small graph cut, low degree, acyclicity, or low treewidth automatically gives a small blanket. It must add a biologically interpretable condition that prevents time-multiplexed exterior information from accumulating, for example a proved finite sufficient statistic, a finite-memory boundary process, or another explicit structural restriction that implies dynamic factorization.

Merely replacing `memory bit` with `species` or `corridor` is not sufficient.
