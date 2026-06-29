# Exact observation-channel envelopes

## Purpose

RACH can be assessed before empirical data exist, but only as a conditional
methodological system.  This module asks a narrow, auditable question:

> Given a finite declared candidate universe, a declared known generator inside
> that universe, and declared binary observation channels, how often would RACH
> report each motif as invariant, excluded, unresolved, or unsupported?

The result is an **exact finite self-calibration**.  It is not an estimate from
field data and not a claim that the declared generator is true in nature.

## What is enumerated

For each robustness cell, declare binary observation channels:

```python
DetectionChannelDesign(
    trait="signal",
    trials=3,
    sensitivity=0.8,
    false_positive=0.1,
)
```

For a true program state, every count from zero through `trials` is a possible
reported outcome.  The module enumerates the Cartesian product across all cells
and channels and gives every outcome its exact binomial probability.  It then
runs the existing pipeline unchanged:

```text
repeated detections
  -> finite program likelihoods
  -> cell-level acceptance
  -> cross-cell RACH classification
  -> exact status probabilities
```

The output for each motif includes:

- probability of `invariant`, `excluded`, `unresolved`, and `unsupported`;
- false-invariant probability when the known true candidate lacks the motif;
- false-excluded probability when the known true candidate has the motif; and
- the corresponding correct decisive probabilities.

This makes the asymmetry of a decisive conclusion visible.  An apparently
strong invariant can be a false invariant under a sufficiently permissive
acceptance threshold, false-positive channel, or omitted candidate mechanism.

## Exactness boundary

The enumeration is exact only conditional on all of the following:

1. one declared finite candidate-program universe;
2. one candidate in that universe designated as the known generator;
3. one feasible true state for each cell;
4. independent binomial repeated-detection channels conditional on that state;
5. the specified cell acceptance thresholds; and
6. the stated coverage labels.

Enumerating all possible **observations** does not make a sampled candidate
universe exhaustive.  `coverage_mode` therefore continues to describe only the
completeness of the program-family search.

The algorithm rejects envelope calculations larger than `max_outcomes` rather
than silently using Monte Carlo.  Use this module for small transparent
universes, or develop a separate approximation/solver method with its own error
statement.

## Relation to the Campanula repository

This repository and `campanula-channel-identification` are complementary but
not interchangeable.

| RACH causal invariants | Campanula channel identification |
|---|---|
| General finite qualitative-program and robust-classification method | Domain-specific island floral-trait design model |
| Inputs: candidate grammars, Boolean states, binary observation channels, acceptance rules, coverage labels | Inputs: guide contrast, visitation, handling, pollen placement, selfing, recruitment, spatial/temporal and genetic layers |
| Output: conditional status and classifier-risk envelopes | Output: constrained life-history / scenario compatibility and prospective field measurement designs |
| Does not contain fitness, pollinator, floral, population-genetic, or site parameters | Explicitly models those biological quantities when their required intermediates are measured or calibrated |

A Campanula study may use RACH after translating a small, predeclared collection
of its biological scenarios into qualitative candidate programs and observation
clauses.  But RACH must not absorb the Campanula life-history model, and the
Campanula repository must not present RACH's finite self-calibration as
empirical validation of a floral mechanism.

## Minimal virtual example

Run:

```bash
python examples/exact_observation_envelope.py
```

The example defines two generic candidates: one asserts a `focal` motif and can
produce a binary signal; the other lacks the motif and cannot.  It sweeps a
single detection channel over several repeated-trial / false-positive settings.
It demonstrates a general fact: increasing repetitions can reduce a
false-invariant risk, but only relative to the declared observation model and
likelihood threshold.
