# Minimum discriminating NULL-observation panels

## Goal

For a focal mechanism \(j\) that drives a target trait \(t^*\), find the cheapest feasible set of NULL observations that makes \(j\) structurally indispensable under the exact disjunctive model.

Each candidate NULL observation is a trait \(q\) with a non-negative acquisition cost \(c(q)\). Observing \(q\) as NULL eliminates all mechanisms in \(D(q)\).

Let \(O_0\) be a baseline observation and let \(P\) be the selected candidate panel. Its total elimination set is

\[
E(P)=\operatorname{NullOff}(O_0)\cup\bigcup_{q\in P}D(q).
\]

The panel is valid only if:

1. \(j\notin E(P)\): the focal mechanism is not itself eliminated;
2. \(D(t^*)\setminus E(P)=\{j\}\): the focal mechanism is the final surviving driver of the target trait;
3. every required-present trait in \(O_0\cup\{t^*\}\) retains at least one driver after elimination; and
4. no candidate is simultaneously required PRESENT and selected as NULL.

The optimization problem is

\[
\min_P \sum_{q\in P}c(q)
\]

subject to these validity conditions.

## Exact solver

`minimum_discriminating_panel` performs dynamic programming over **total eliminated-mechanism sets**. For every reachable elimination set, it retains the least-cost panel that produces it. This is exact because—in the stated monotone-OR model—feasibility and last-driver status depend on a panel only through its cumulative eliminated mechanisms and total cost.

Ties are broken deterministically by fewer observations and then trait name, so result objects are reproducible.

## Why this is not a greedy problem

In the canonical synergy case, each witness-null observation removes one competitor but leaves another. Every singleton therefore has zero immediate effect on the focal mechanism's forced-ON status, yet the full panel resolves it. The solver searches the joint panel space rather than stopping after uninformative singleton steps.

## Scope boundary

A returned panel is an exact design result **within the declared Boolean driver model**. It does not validate the candidate grammar, guarantee that a biological NULL result has adequate power, or make a real-world causal claim. Observation costs should therefore encode practical feasibility and expected reliability only after those inputs have been independently justified.
