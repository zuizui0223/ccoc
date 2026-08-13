# Narrow physical boundary does not imply causal closure — 2026-08-13

> **Status:** ecological interpretation / derived corollary of existing CCOC results. This document adds no theorem-registry claim. It combines the existing relay topology with the existing dynamic-blanket lower bound to make one ecological consequence explicit.

## Statement

A small physical interface between an observed region and its exterior does **not** imply that the exterior admits a small extension-stable causal summary.

The CCOC relay gives an exact finite separation. For every number `m` of binary exterior memories:

1. the focal output node `ROOT` is connected to the entire exterior relay tree through exactly one graph edge, `ROOT -- body_root`;
2. every local node/message alphabet remains bounded independently of `m`;
3. the maximum graph degree remains three;
4. after the declared open grammar makes the exterior memories addressable, the exact open response quotient has `2^(m+1)` classes;
5. with the inside/focal bit treated separately, every extension-stable dynamic boundary summary must therefore carry at least `m` bits of exterior information.

Thus one has a family with

\[
\boxed{\text{focal--exterior edge cut}=1}
\]

for all `m`, but

\[
\boxed{\log_2 |B|\ge m}
\]

for any exact dynamic boundary blanket `B` that supports the declared open future grammar.

The physical cut remains constant while the exact causal-interface memory diverges.

## Derivation from existing results

### Constant physical cut

`RelayTreeTopology` constructs a separate focal node `ROOT` with

```text
ROOT -> body_root
```

as its unique child edge. All leaves and internal relay nodes lie below `body_root`. Removing that one edge disconnects the focal node from every exterior memory leaf.

This is true for every `module_count=m`.

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

The relay realizes the addressability premises while keeping the focal--exterior physical cut equal to one.

## What this does and does not mean

This is **not** a new graph-theoretic lower bound and is not claimed as historical firstness. A narrow channel can transmit different information at different times; static cut size alone is not a bound on the complete family of counterfactual response distinctions available over an unrestricted future grammar.

The useful CCOC distinction is therefore between two very different notions of boundary size:

- **physical boundary width:** how many simultaneous graph connections cross a spatial/interaction cut;
- **dynamic causal boundary complexity:** how many exterior response types must be retained so that all declared future interactions remain exactly predictable.

A system may have the first uniformly bounded and the second unbounded.

## Ecological interpretation

This blocks a tempting but unsafe inference:

> a patch, island, population, or community has only a few physical connections to its surroundings, therefore the surroundings can be summarized by a few causal state variables.

The relay shows why the inference fails in principle. A single corridor, inlet, dispersal gateway, shoreline contact, or interaction interface can expose different exterior states under different future events. The number of simultaneous connections may stay small while the number of distinguishable future exterior responses grows.

Accordingly, descriptors such as

- edge length or edge count;
- corridor count;
- number of current immigrants;
- number of currently active interaction links;
- one-time connectivity;

are not by themselves certificates of causal closure.

A closure certificate requires a **dynamic** statement: the exterior effects relevant to every allowed future colonization, reconnection, disturbance, or interaction event must factor through a finite boundary state whose update is itself closed.

## Why this belongs in the manuscript

This consequence gives a sharper ecological reading of the formal results without expanding the theorem spine.

The manuscript can state:

> Physical isolation and causal compressibility are distinct. Even a single persistent connection between a focal system and its exterior can carry an unbounded family of counterfactual distinctions across alternative future interactions. What matters for an exact open-system macro-law is not the width of the present boundary alone, but whether all future exterior effects factor through a bounded dynamic boundary state.

The relay remains a synthetic witness, not evidence that a real corridor or island has large causal-interface memory.

## Relation to future ecological mathematics

The corollary also clarifies what a genuinely stronger ecological theorem would have to do. It cannot assume that a small graph cut automatically gives a small blanket. It must add a biologically interpretable condition that prevents time-multiplexed exterior information from accumulating, for example a proved finite sufficient statistic, a finite-memory boundary process, or another explicit structural restriction that implies dynamic factorization.

Merely replacing `memory bit` with `species` or `corridor` is not sufficient.