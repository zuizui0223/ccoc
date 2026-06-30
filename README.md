# RACH Causal Invariants

RACH is a theorem-first methods repository for a narrow question:

> **When can locally valid causal rules be promoted to a world-level conclusion, and when must candidate uncertainty leave the conclusion unresolved?**

It contains no empirical data and makes no domain-specific causal claim.

## Current theory core

The active core is:

\[
\text{retained candidate dynamics}
\to
\text{exact closure / recurrence certificates}
\to
\text{candidate consensus}
\to
\text{decisive conclusion or UNRESOLVED}.
\]

The focused import surface is:

```python
from causal_model.current_theory import (
    FiniteDeterministicRuleSystem,
    classify_closure,
    ObservationRegimeRulePair,
    classify_observation_regime_pair,
    summarize_regime_candidates,
)
```

Read the [current architecture map](docs/current_architecture.md) before using
older modules.

## What the core proves

### 1. Local transition truth does not imply global closure

For a finite total deterministic update map

\[
F:S\to S,
\]

RACH classifies the long-run world-level behavior as exactly one of:

| Result | Exact certificate |
|---|---|
| `GLOBAL_CLOSURE` | strict integer ranking descending to one fixed point |
| `RECURRENT_NONCLOSURE` | a directed cycle of period \(p\ge2\) |
| `MULTISTABLE_NONCLOSURE` | two or more distinct fixed points |

Thus every local transition may be correct while repeated application fails to
produce one stable global endpoint. See the [closure calculus](docs/causal_closure_calculus.md).

### 2. Rules can differ between natural and observer-coupled regimes

A candidate may declare two maps on the same state space:

\[
F^{(0)} \quad\text{(natural regime)},
\qquad
F^{(1)} \quad\text{(observer-coupled regime)}.
\]

RACH compares their certified closure classes and can report, for example:

- `OBSERVER_INDEPENDENT_CLOSURE`;
- `OBSERVATION_INDUCED_CLOSURE`;
- `OBSERVATION_INDUCED_RECURRENCE`; or
- `REGIME_DEPENDENT_NONCLOSURE`.

This is an operational statement about two declared dynamics. It does **not**
claim that observation creates reality, nor that empirical observation is
necessarily invasive. See [observation-regime closure](docs/observation_regime_closure.md).

### 3. Candidate consensus is the RACH rule

RACH does not require complete model identification. Let \(C_t\) be retained
candidate systems and let \(v(\theta)\) be a claim-level verdict.

\[
\forall\theta\in C_t,
\quad v(\theta)=v^\star
\quad\Longrightarrow\quad
\text{report }v^\star.
\]

If retained candidates disagree, the output is `UNRESOLVED`.

This is the central discipline: a single convenient model must not be promoted
to a general causal conclusion.

## Mathematical boundary

Current exact closure theorems apply to **finite labelled total deterministic
maps**. They do not prove analogous facts for arbitrary continuous, stochastic,
hidden-state, or empirical systems.

For a finite theorem domain, RACH uses certificates rather than simulation
appearance:

\[
\text{simulation evidence}
\neq
\text{proof of closure or recurrence}.
\]

A valid certificate proves only the conclusion and scope it explicitly states.

## GitHub Actions theorem regression

Two dedicated workflows model-check the current finite theorem domains:

- all labelled deterministic maps on one through four states:
  \[
  1^1+2^2+3^3+4^4=288;
  \]
- all ordered natural/observer-coupled map pairs on one through three states:
  \[
  (1^1)^2+(2^2)^2+(3^3)^2=746.
  \]

Each workflow runs targeted tests, exhaustive enumeration, certificate
verification, and uploads a deterministic JSON report. Passing these workflows
is finite model checking of the declared domain, not a general proof assistant.

## Supporting layers

The repository also contains useful supporting methods. They are not all part
of the current theory core.

### Sequential evidence

Confidence-set lifting and anytime lifting provide a conditional bridge from
random observations to retained candidate sets:

\[
\Pr[\theta^\star\text{ remains retained at all certified looks}]
\ge1-\alpha
\]

can lift to a false-decisive conclusion bound. These modules control how safely
candidate systems are removed as data accumulate; they do not by themselves
prove closure.

### Exact solver certificates

Rational SAT witnesses, Farkas infeasibility certificates, finite polyhedral
motif compilers, and replayable proof artifacts are available when a problem
really fits their restricted grammar.

### Audit and provenance

Manifests, append-only transcripts, replay registries, signed checkpoints, and
canonical artifact formats preserve evidence identity and history. They are an
optional audit shell, not the scientific theorem itself.

### Earlier finite-program and design modules

The repository retains disjunctive theorem families, ecological-program
inference, exact observation envelopes, observation-panel design, and benchmark
suites. They remain supported tools, but should be used only where they serve
the closure-and-consensus question rather than by default.

## Development rule

A new mathematical PR should contain:

1. a theorem statement and explicit scope boundary;
2. a verifier for its certificate object;
3. fail-closed counterexample tests;
4. exhaustive finite model checking when feasible; and
5. an Action artifact reporting the finite enumeration.

The architecture document explains where new code belongs:
[core, sequential evidence, certificates, or audit](docs/current_architecture.md).

## Scope boundary

RACH is not a floral-trait, pollination, fitness, population-genetic,
site-level, or field-protocol model. All conclusions remain conditional on the
declared candidate systems, observation regime, certificate validity, and—when
sequential evidence is used—the external coverage assumptions.
