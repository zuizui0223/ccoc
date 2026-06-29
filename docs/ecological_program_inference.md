# Finite qualitative ecological-program inference

## What this layer adds

The original replaceability theorem is exact for a **complete monotone OR**
model.  This module deliberately does not relabel that theorem as a result for
arbitrary ecological mechanisms.  Instead, `causal_model.ecological_program`
adds a second, explicitly finite layer:

1. a declared Boolean trait grammar with `AllOf`, `AnyOf`, and `Not`;
2. an explicit finite feasible-state set, when biological compatibility rules
   rule out parts of the Boolean cube;
3. repeated binary observations with sensitivity and false-positive rates;
4. a bridge from accepted qualitative programs to the existing
   cross-cell robust-admissibility report; and
5. exact minimum-cost joint observation panels over a finite candidate library.

All conclusions are conditional on the declared program universe, feasible
states, observation channels, acceptance thresholds, and panel library.

## Why this matters ecologically

Ecological mechanisms commonly require conjunctions or are switched off by
context.  Examples include a phenotype requiring both a genetic variant and an
enabling environment, or a mutualistic outcome disappearing when an antagonist
is active.  These cannot be represented safely as a monotone OR driver set.

A `QualitativeProgram` therefore maps each observable trait to a Boolean
formula over binary mechanism switches.  The analyst may also supply
`feasible_states` to encode explicit incompatibilities such as mutually
exclusive dispersal regimes, a fixed resource budget, or a known life-history
constraint.  This is still a finite qualitative approximation, not a claim that
real biology is literally binary.

## Observation error and NULL results

A `TraitDetection` records:

- the trait name;
- detections and repeated trials;
- sensitivity, `P(reported present | truly present)`; and
- false-positive probability, `P(reported present | truly absent)`.

For a declared program state, the likelihood is binomial.  Consequently, a
zero-detection result has **lower** likelihood when a trait is truly present,
but does not force its probability to zero unless a perfect channel has been
predeclared.  The older hard-NULL API remains valid only for observations whose
absence is defensible as exact.

The likelihood threshold in `NoisyRobustnessCell` is deliberately an input.  It
must be set by an external calibration, posterior-predictive criterion,
pre-registered likelihood rule, or another documented acceptance procedure.
The module does not turn a convenient threshold into a universal truth claim.

## Robust invariance across cells

A `QualitativeProgramCandidate` combines a program with its asserted active
motifs.  `evaluate_candidate_universe` evaluates every candidate in every
`NoisyRobustnessCell` and returns ordinary `RobustnessCell` objects.  Therefore
`CandidateUniverseReport.classify(...)` uses the existing rules:

- `invariant`: present in every accepted candidate of every required cell;
- `excluded`: absent from every accepted candidate of every required cell;
- `unresolved`: accepted candidates disagree; and
- `unsupported`: a required cell accepts no candidate.

Use `CoverageMode.EXHAUSTIVE` only when the declared candidate universe has
actually been exhaustively enumerated.  A finite set of hand-written programs
is usually `CoverageMode.SAMPLED`, even if each individual program's state
space is enumerated exactly.

## Joint minimum observation panels

`minimum_boolean_panel` searches all subsets of a finite observation library.
It asks which observations make a focal mechanism ON in every non-empty state
consistent with the hard observations.  It therefore evaluates joint panels
rather than selecting observations by singleton gain.

Unlike the OR-only dynamic program, this general routine is exponential in the
number of candidate observations.  It is intended for small, auditable design
libraries.  Larger problems should move to a SAT/MaxSAT or integer-programming
backend while retaining the same declared program and observation semantics.

## Recommended empirical protocol

Before inspecting the decisive data:

1. Define the focal causal question and the competing motif vocabulary.
2. Write the trait rules and their biological justification, including every
   known alternative route and compatibility constraint.
3. Specify which observations are trusted hard observations and which use a
   detection channel, with sensitivity and false-positive assumptions.
4. Define required robustness cells: for example alternative observation
   channels, seasonal windows, population subsets, priors, or acceptance
   thresholds.
5. Record the candidate-program coverage status.  Do not call a hand-curated
   universe exhaustive.
6. Use the panel optimizer to choose feasible additional observations before
   field work, then lock the primary panel and acceptance rule.
7. Report accepted and rejected candidates, invariant/excluded/unresolved
   motifs, the empty-cell status, all chosen thresholds, and sensitivity
   analyses for omitted mechanisms and observation error.

The island-flower-colour folder provides a data contract and a scenario
skeleton for this workflow.  It is intentionally a **pre-analysis template**;
it does not claim that any empirical mechanism has been established.
