# Current RACH architecture

## Why this map exists

RACH accumulated several valid but differently purposed layers: finite causal
programs, confidence-set lifting, exact proof replay, append-only transcripts,
and more recent closure dynamics.  They should not all be read as one theorem.

The active research core is now deliberately small:

\[
\text{retained candidate dynamics}
\to
\text{exact world-level certificates}
\to
\text{candidate consensus}
\to
\text{closure/regime conclusion or UNRESOLVED}.
\]

The rest remains useful supporting infrastructure, not the scientific claim.

## Layer 1: theory core

`causal_model/current_theory.py` is the focused public entrance.

### Finite deterministic closure

`causal_model/causal_closure_calculus.py` classifies a total finite map

\[
F:S\to S
\]

into one of:

- `GLOBAL_CLOSURE`, certified by strict integer ranking descent;
- `RECURRENT_NONCLOSURE`, certified by an exact directed cycle of period at
  least two; or
- `MULTISTABLE_NONCLOSURE`, certified by distinct fixed points.

The key separation is:

\[
\text{every local transition is specified}
\not\Rightarrow
\text{one globally closing world-level outcome}.
\]

### Observation-regime comparison

`causal_model/observation_regime_closure.py` compares two declared maps on the
same state space:

\[
F^{(0)}\quad\text{(natural regime)},
\qquad
F^{(1)}\quad\text{(observer-coupled regime)}.
\]

It can certify observer-independent closure, observation-induced closure,
observation-induced recurrence, and related nonclosure transitions. This is an
operational comparison of declared regime maps. It does not claim that
observation creates reality or that empirical observation is automatically
causally invasive.

### Candidate consensus

A decisive result requires all retained candidate systems to share the same
claim-level verdict. Candidate disagreement is `UNRESOLVED`.

\[
\forall\theta\in C_t,
\quad v(\theta)=v^\star
\quad\Longrightarrow\quad
\text{report }v^\star.
\]

This is the RACH contribution retained in the core: do not force a single model
winner when a structural conclusion can be shared, and do not force a
structural conclusion when retained candidates disagree.

## Layer 2: sequential evidence

The sequential layer is the bridge from random observations to retained
candidate sets. Its general theorem is conditional:

\[
\Pr\left[\theta^\star\in C_t\text{ for all certified cells and looks}\right]
\ge1-\alpha
\]

lifts to a false-decisive bound for conclusions calculated from those sets.

Relevant modules include:

- `confidence_lifting.py` and `anytime_confidence_lifting.py`;
- symbolic candidate-set lifting and exact rational feasibility verification;
- the finite-alphabet e-process backend, when its declared finite stationary
  assumptions are appropriate.

This layer does not decide closure by itself. It only controls how safely
candidate dynamics may be removed as data accumulate.

## Layer 3: certificates

Exact certificates prevent simulation output from being promoted directly to a
strong conclusion.

- finite closure rankings, cycles, and multistability certificates;
- rational SAT witnesses and Farkas infeasibility certificates;
- compiler-generated finite branch systems where the restricted grammar is
  applicable.

A certificate proves a stated result only in its stated mathematical domain.

## Layer 4: audit and provenance

Canonical manifests, replayable artifacts, append-only transcripts, signatures,
and checkpoints are an optional audit shell.

They answer:

\[
\text{which evidence and proof objects were used, and has their history changed?}
\]

They do not establish:

\[
\text{candidate-universe adequacy},
\quad
\text{empirical observation validity},
\quad
\text{or scientific truth}.
\]

This distinction matters: auditability is useful, but it is not the main
mathematical contribution.

## What is supporting, not current theory core

The following remain available but are not the main narrative for new work:

- disjunctive / ecological-program theorem families;
- minimum discriminating observation panels and benchmark suites;
- manifest v1/v2 adapters, transcript variants, and checkpoint plumbing;
- polyhedral admission machinery outside a problem that genuinely needs its
  restricted grammar.

They should be reused only when they serve the closure-and-consensus research
question, not because they already exist.

## GitHub Actions policy

When a theorem is implemented over a finite declared domain, its pull request
should contain:

1. a written theorem statement and scope boundary;
2. an independently checkable certificate verifier;
3. targeted counterexample and fail-closed tests;
4. exhaustive model checking whenever the declared domain is small enough; and
5. a workflow artifact containing the deterministic enumeration summary.

Current examples are:

- finite closure theorem regression over all maps on up to four states; and
- observation-regime theorem regression over all ordered map pairs on up to
  three states.

Passing CI is not a proof of a theorem outside its finite stated domain.
