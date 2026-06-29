# Finite qualitative-program inference

## What this layer adds

The original replaceability theorem is exact for a **complete monotone OR**
model. This module deliberately does not relabel that theorem as a result for
arbitrary mechanisms. Instead, `causal_model.ecological_program` adds a second,
explicitly finite layer:

1. a declared Boolean trait grammar with `AllOf`, `AnyOf`, and `Not`;
2. an explicit finite feasible-state set when compatibility rules rule out parts
   of the Boolean cube;
3. repeated binary observations with sensitivity and false-positive rates;
4. a bridge from accepted qualitative programs to the existing cross-cell
   robust-admissibility report; and
5. exact minimum-cost joint observation panels over a finite candidate library.

All conclusions are conditional on the declared program universe, feasible
states, observation channels, acceptance thresholds, and panel library.

This is a **finite special case** of the more general
[confidence-set lifting theorem](confidence_set_lifting_theorem.md). The binary
likelihood specifies one way to turn observations into retained candidates. The
general theorem allows that step to be replaced by any external set-valued
procedure with a valid simultaneous coverage certificate.

## Why a Boolean grammar is still useful

Qualitative mechanisms can require conjunctions or be switched off by context.
Examples include one outcome requiring both a latent condition and an enabling
context, or a route disappearing under inhibition. These cannot be represented
safely as a monotone OR driver set.

A `QualitativeProgram` therefore maps each observable trait to a Boolean formula
over binary mechanism switches. The analyst may also supply `feasible_states` to
encode explicit incompatibilities, a fixed resource budget, or another declared
constraint. This is a finite qualitative approximation, not a claim that a
real-world process is literally binary.

## Observation error and NULL results

A `TraitDetection` records:

- the trait name;
- detections and repeated trials;
- sensitivity, `P(reported present | truly present)`; and
- false-positive probability, `P(reported present | truly absent)`.

For a declared program state, the likelihood is binomial. Consequently, a
zero-detection result has **lower** likelihood when a trait is truly present,
but does not force its probability to zero unless a perfect channel has been
predeclared. The older hard-NULL API remains valid only for observations whose
absence is defensible as exact.

The likelihood threshold in `NoisyRobustnessCell` is deliberately an input. It
must be supplied by an external calibration, a predeclared rule, or another
documented acceptance procedure. The module does not turn a convenient
threshold into a universal truth claim.

## Robust invariance across cells

A `QualitativeProgramCandidate` combines a program with its asserted active
motifs. `evaluate_candidate_universe` evaluates every candidate in every
`NoisyRobustnessCell` and returns ordinary `RobustnessCell` objects. Therefore
`CandidateUniverseReport.classify(...)` uses the existing rules:

- `invariant`: present in every accepted candidate of every required cell;
- `excluded`: absent from every accepted candidate of every required cell;
- `unresolved`: accepted candidates disagree; and
- `unsupported`: a required cell accepts no candidate.

Use `CoverageMode.EXHAUSTIVE` only when the declared candidate universe has
actually been exhaustively enumerated. A finite set of hand-written programs is
usually `CoverageMode.SAMPLED`, even if each individual program's state space is
enumerated exactly.

The confidence-set lifting theorem adds a distinct statistical statement: if an
external procedure retains the true candidate in all required cells with
probability at least `1 - alpha`, then any false decisive RACH conclusion has
probability at most `alpha`. Enumerating the Boolean states of one candidate
does not establish either statistical coverage or exhaustive candidate-universe
coverage.

## Joint minimum observation panels

`minimum_boolean_panel` searches all subsets of a finite observation library. It
asks which observations make a focal mechanism ON in every non-empty state
consistent with the hard observations. It therefore evaluates joint panels
rather than selecting observations by singleton gain.

Unlike the OR-only dynamic program, this general routine is exponential in the
number of candidate observations. It is intended for small, auditable design
libraries. Larger problems should move to a SAT/MaxSAT or integer-programming
backend while retaining the same declared program and observation semantics.

## Theoretical use contract

Before using this finite layer, declare:

1. the motif vocabulary and finite candidate programs;
2. the trait rules and feasible-state restrictions;
3. the observation channel or external confidence-set construction;
4. the required robustness cells and their acceptance rule;
5. the candidate-universe coverage label; and
6. whether the aim is a deterministic within-universe theorem, an exact
   finite known-truth benchmark, or a coverage-certified random-data guarantee.

No item on this list constitutes empirical validation. Domain-specific data,
field protocols, and applied causal claims belong in a separate application
repository, which may translate its own predeclared scenario set into this
finite interface when a logical audit is useful.
