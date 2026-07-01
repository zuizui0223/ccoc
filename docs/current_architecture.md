# Current RACH architecture

## Why this map exists

RACH contains several valid but differently purposed layers: finite causal
programs, open-interface witnesses, candidate-family logic, confidence-set
lifting, exact proof replay, and provenance. They should not be read as one
theorem.

The research entrance is [the theorem spine](theorem_spine.md). This document
maps that spine onto code, certificates, and workflows.

## Layer 1: active theorem core

`causal_model/current_theory.py` is the focused public entrance. It re-exports
the eight active finite theorem families below. New theorem work should begin
there, not from `causal_model.__init__`.

| Family | Module | Main exact object | Certificate / verifier |
|---|---|---|---|
| finite closure | `causal_closure_calculus.py` | global closure, recurrence, multistability | ranking, cycle, fixed-point certificates |
| passive-window completion | `observation_window_completion.py` | passive/open trace quotient | completion and separating-word certificates |
| closed/open compression | `extension_compression.py` | fixed-context versus open-port quotient | extension-compression certificate |
| addressable product bounds | `addressable_completion_bounds.py` | product lower bound and gap inequality | separating-word, blanket, nonidentifiability certificates |
| relay compilation | `relay_tree_compilation.py` | degree-three constant-local-grammar realization | protocol and macro-conjugacy certificates |
| dynamic blankets | `dynamic_boundary_blankets.py` | coarsest dynamic interface and finite upper bounds | stabilization and dynamic-interface certificates |
| delayed addressability | `delayed_addressability.py` | grammar-aware quotient and delayed no-go | prefix-grammar, delayed separator, relay-attachment certificates |
| candidate-safe laws | `candidate_safe_laws.py` | universal/candidate-safe/set-valued law distinction | agreement, obstruction, response-separator certificates |
| operational regime comparison | `observation_regime_closure.py` | two declared regime maps | regime classification and consensus certificates |

The regime module remains active but is an operational special case of changing
a declared action grammar, not an independent ecology ontology.

## The core dependency graph

```text
causal_closure_calculus
        -> time-promotion certificates

observation_window_completion
        -> passive/open no-go
        -> extension_compression
        -> addressable_completion_bounds
                -> dynamic_boundary_blankets
                -> relay_tree_compilation
                -> delayed_addressability

candidate_safe_laws
        -> candidate-induced macro maps
        -> universal / candidate-safe / set-valued verdict
        -> delayed_addressability (delayed discrimination grammar)

current_theory
        -> curated imports from all active theorem families
```

The arrows show conceptual reuse, not a claim that every module must be imported
by every other module.

## Core theorem roles

### Closure over time

`causal_closure_calculus.py` studies total finite maps

\[
F:S\to S.
\]

It distinguishes one globally closing endpoint from exact recurrence and
multistability. This proves a time-promotion statement only; it does not answer
whether a boundary summary is sufficient or whether a candidate family agrees.

### Window, exterior, and composition

`observation_window_completion.py` gives the passive/open no-go. The
extension/compression and addressable-product modules turn it into a sharp
interface-memory lower bound. `relay_tree_compilation.py` removes the objection
that a growing local lookup table or high-degree focal node created the effect.

### Dynamic positive criterion

`dynamic_boundary_blankets.py` gives the converse direction within its declared
finite deterministic controlled domain. A summary is valid only when it preserves
output and action-conditioned update. The all-word quotient is the coarsest such
exact deterministic interface.

### Delay as an independent axis

`delayed_addressability.py` adds a prefix grammar to control when a future action
is legal. It proves that each fixed finite grammar has a finite exact horizon,
while an expanding delayed family has no shared finite closure horizon.

### Candidate plurality

`candidate_safe_laws.py` starts after candidate-specific macro maps have been
specified. It asks whether they agree after candidate identity is forgotten.
The output is deliberately typed:

```text
all induced maps agree                 -> universal deterministic law
maps disagree, response type retained  -> candidate-safe deterministic law
maps disagree, response type forgotten -> set-valued law or UNRESOLVED
```

## Layer 2: retained-family and sequential evidence

This layer controls how data or solver output may remove candidate worlds. It
does not itself prove closure, open-interface sufficiency, or universal macro
dynamics.

Relevant modules include:

- `admissibility.py`;
- `confidence_lifting.py` and `anytime_confidence_lifting.py`;
- symbolic candidate-set lifting and exact rational feasibility verification; and
- the finite-alphabet e-process backend when its narrow stationary assumptions
  are appropriate.

The future bridge must have the form

\[
\text{data or solver output}
\to
\text{retained completion/mechanism family}
\to
\text{typed open-law verdict}.
\]

Until that bridge exists, this layer is support infrastructure, not evidence that
an exterior grammar or candidate family is correctly specified.

## Layer 3: certificates and regression

Each active theorem family supplies exact finite certificate objects. They are
not screenshots of a simulation. Typical certificates include:

- closure rankings, recurrence cycles, and multistability witnesses;
- passive-indistinguishable completions and future separating words;
- product-coordinate separators and blanket factorizations;
- relay micro-trajectories and macro conjugacy;
- grammar-aware delayed separators; and
- candidate transition agreement, obstruction, and response-type separators.

The corresponding GitHub Actions workflows replay finite declared families and
upload deterministic JSON reports. They test implementation invariants; their
success is not a general proof assistant for ecosystems outside the declared
domain.

## Layer 4: theorem red-team laboratory

The following modules are valuable when they falsify or sharpen a current theorem
premise:

- `ecological_program.py` and `failure_modes.py` for hostile finite grammars;
- `generative_benchmarks.py` and `benchmarks.py` for exact finite sweeps;
- `observation_envelope.py` for observation-channel ambiguity; and
- `observation_design.py`, `robust_panel_design.py`, and related panel benchmarks
  for later intervention-design corollaries.

They are not the default ontology for new theorem work. Their job is to find the
smallest counterexample that forces a sharper assumption.

## Layer 5: audit and provenance

Manifests, transcripts, signatures, checkpoints, and registries preserve proof
identity and history. They answer which artifact was used and whether it changed.
They do not establish which exterior completion is possible, whether a blanket is
sufficient, or whether a law is universal.

Keep this layer compatible and tested. Do not add to it absent a concrete
publication or audit requirement.

## Repository navigation rule

- Start a new theorem with [theorem spine](theorem_spine.md).
- Find modules and dependency roles here.
- Use [the asset map](repository_asset_map.md) before reusing legacy code.
- Use [the promotion calculus](promotion_calculus.md) to decide which promotion
  obligation the theorem is meant to settle.

## GitHub Actions policy

When a theorem is implemented over a finite declared domain, its pull request
should contain:

1. a written theorem statement and scope boundary;
2. an independently checkable certificate verifier;
3. targeted fail-closed and counterexample tests;
4. finite enumeration only as replay for the stated certificate; and
5. a deterministic workflow artifact.

Current theorem workflows cover closure, regime comparison, extension/compression,
relay compilation, observation-window completion, addressable bounds, dynamic
blankets, delayed addressability, and candidate-safe laws.
