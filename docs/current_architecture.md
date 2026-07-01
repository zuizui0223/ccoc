# Current RACH architecture

## Why this map exists

RACH accumulated several valid but differently purposed layers: finite causal
programs, confidence-set lifting, exact proof replay, append-only transcripts,
closure dynamics, and open-interface witnesses. They should not all be read as
one theorem.

The active research core now has two finite structural questions:

\[
\text{local transition rules}
\to
\text{exact long-run certificates},
\]

and

\[
\text{rule inside a finite observation window}
\not\Rightarrow
\text{rule under every allowed ecosystem-outside completion}.
\]

Candidate consensus is the epistemic gate that decides whether such a structural
conclusion can be reported for a retained family of candidate worlds.

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

### Observation-window completion

`causal_model/observation_window_completion.py` makes the inside/outside
question explicit. A finite window observes a focal output. A declared
completion grammar specifies what hidden exterior modules and future boundary
actions may affect the window.

For the explicit family with \(m\) hidden binary exterior modules,

\[
K_{\mathrm{passive}}=1,
\qquad
K_{\mathrm{open}}=m+1.
\]

The module proves three things in its declared finite domain:

1. every finite passive observation word is shared by distinct exterior
   completions;
2. an allowed future boundary probe separates those completions; and
3. enlarging the action / completion grammar refines, never coarsens, the
   minimal safe trace quotient.

`CounterfactualCompletionCertificate` is the one-word separating object.
`ObservationWindowCompletionCertificate` verifies the exact passive-versus-open
partition and enumerates finite passive protocols. `RelayCompletionCertificate`
shows the same counterexample in the degree-three constant-grammar relay
implementation.

This does not claim that passive data are useless, that every empirical window
fails, or that arbitrary outsides can be simulated. It is an existence no-go:
passive traces alone cannot certify closure in a model class containing the
explicit completion family.

### Extension--compression lower-bound family

`causal_model/extension_compression.py` is now a special completion grammar. A
fixed context permits one port; a declared open context permits any port later.
For every \(m\ge1\),

\[
\max_i \kappa(M_m\parallel E_i)=2,
\qquad
\kappa_{\mathrm{open}}(M_m;\mathcal E_m)=m+1.
\]

Thus every fixed closed extension has a four-state interface, whereas the
open-safe interface is the full \(2^{m+1}\)-state partition.

`TraceSeparationCertificate` records the current observation or future port
probe that prevents two states from being merged.

### Bounded-degree relay-tree compilation

`causal_model/relay_tree_compilation.py` proves that the coordinate witnesses do
not rely on a growing local lookup table or high-degree focal node. It compiles
every size into a binary tree with one fixed grammar:

- reader states `ready` / `fire`;
- memory leaves with a permanent bit and three-valued transient pulse;
- three-valued relay pulses; and
- a binary focal root output.

Messages are directed along child-to-parent edges. With one attached reader,
every node has degree at most three. The declared sequential action grammar
allows one reader firing followed by return to quiescence.

`RelayProtocolCertificate` replays a complete micro-trajectory. The compilation
certificate checks every quiescent coordinate state and every port in the
declared finite range, proving that completed macro probes are conjugate to the
coordinate action.

### Candidate consensus

A decisive result requires all retained candidate systems to share a claim-level
verdict. Candidate disagreement is `UNRESOLVED`.

\[
\forall\theta\in C_t,
\quad v(\theta)=v^\star
\quad\Longrightarrow\quad
\text{report }v^\star.
\]

This is the RACH discipline: do not force a single model winner when a
structural conclusion can be shared, and do not force a structural conclusion
when retained candidates disagree.

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
operational comparison of declared action regimes. It is not the primary
inside/outside ontology and does not claim that observation automatically alters
an ecosystem.

## Layer 2: sequential evidence

The sequential layer bridges random observations to retained candidate sets. Its
general theorem is conditional:

\[
\Pr\left[\theta^\star\in C_t\text{ for all certified cells and looks}\right]
\ge1-\alpha
\]

lifts to a false-decisive bound for conclusions calculated from those sets.

Relevant modules include:

- `confidence_lifting.py` and `anytime_confidence_lifting.py`;
- symbolic candidate-set lifting and exact rational feasibility verification; and
- the finite-alphabet e-process backend when its declared finite stationary
  assumptions are appropriate.

This layer does not decide closure, outside invariance, or open-interface
complexity. It only controls how safely candidate worlds may be removed as data
accumulate.

## Layer 3: certificates

Exact certificates prevent simulation output from being promoted directly to a
strong conclusion.

- finite closure rankings, cycles, and multistability certificates;
- passive-indistinguishable completion and separating-boundary-word certificates;
- open-interface trace-separation certificates;
- bounded-degree relay protocol and macro-conjugacy certificates;
- rational SAT witnesses and Farkas infeasibility certificates; and
- compiler-generated finite branch systems where the restricted grammar applies.

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
\text{which exterior completions remain possible},
\quad
\text{whether a boundary blanket is sufficient},
\quad
\text{or scientific truth}.
\]

Auditability is useful, but it is not the main mathematical contribution.

## What is supporting, not current theory core

The following remain available but are not the main narrative for new work:

- disjunctive / ecological-program theorem families;
- minimum discriminating observation panels and benchmark suites;
- manifest v1/v2 adapters, transcript variants, and checkpoint plumbing; and
- polyhedral admission machinery outside a problem that genuinely needs its
  restricted grammar.

Reuse them only when they serve an active core question.

## GitHub Actions policy

When a theorem is implemented over a finite declared domain, its pull request
should contain:

1. a written theorem statement and explicit scope boundary;
2. an independently checkable certificate verifier;
3. targeted counterexample and fail-closed tests;
4. exhaustive model checking whenever the declared domain is small enough; and
5. a workflow artifact containing the deterministic enumeration summary.

Current examples are:

- finite closure regression over all maps on up to four states;
- observation-regime regression over all ordered map pairs on up to three states;
- extension--compression regression for the coordinate witness family with one
  through six ports;
- relay-tree compilation regression for one through six ports, all quiescent
  states, and all reader attachments; and
- observation-window completion regression for one through six exterior modules,
  all passive words through a declared finite horizon, both focal states, and all
  declared boundary ports.

Passing CI is not a proof outside the finite stated domain.
