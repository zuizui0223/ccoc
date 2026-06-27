# RACH Causal Invariants

A theorem-first framework for reasoning about **which causal motifs are indispensable within a declared qualitative model class**, and about why the observations needed to establish that fact may be synergistic.

## Core question

Given a causal-program grammar, a set of biological constraints, and an observation set, distinguish:

```text
possible explanation
≠
robustly admissible explanation
```

The immediate theorem core works under a finite disjunctive structural model:

```text
cline(t)  <=>  at least one driver of trait t is active.
```

It proves, within that declared candidate set:

1. **Null-only elimination.** Positive observations cannot force a mechanism off; NULL observations eliminate the mechanisms that generate the null trait.
2. **Last-driver criterion.** A mechanism is indispensable exactly when it is the only surviving driver of at least one required-present trait.
3. **Synergistic observation design.** A set of individually uninformative competitor-witness observations can jointly make a mechanism indispensable. Therefore greedy one-step observation selection has no general guarantee.

## Scope boundary

This repository is the active methods home for RACH causal invariants. It does **not** claim that an inferred motif is universally true in nature. Every conclusion is conditional on the declared candidate mechanisms, observation fidelity, and program grammar.

The initial theorem core is a clean extraction from the earlier `microdonta` work. Generic demos, field-case code, UI prototypes, and historical ABMs are intentionally not copied here.

## Development roadmap

```text
exact disjunctive theorem core
-> robust-admissibility over qualitative program families
-> benchmarked causal-invariant extraction
-> minimum discriminating observation / intervention panels
```
