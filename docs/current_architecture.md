# Current RACH architecture

## Why this map exists

RACH accumulated several valid but differently purposed layers: finite causal
programs, confidence-set lifting, exact proof replay, append-only transcripts,
closure dynamics, and open-interface witnesses. They should not all be read as
one theorem.

The active research core now has two deliberately narrow finite theorem threads:

\[
\text{retained candidate dynamics}
\to
\text{exact world-level certificates}
\to
\text{candidate consensus}
\to
\text{closure/regime conclusion or UNRESOLVED},
\]

and

\[
\text{small causal interface for every fixed closed extension}
\not\Rightarrow
\text{small interface for a declared open composition}.
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

This is the RACH discipline: do not force a single model winner when a
structural conclusion can be shared, and do not force a structural conclusion
when retained candidates disagree.

### Extension--compression witness

`causal_model/extension_compression.py` formalizes a no-go question. It declares
a finite focal-bit system with attachable ports. A fixed closed context permits
one specified port; a declared open port grammar permits any specified port to
be probed in the future.

For each \(m\ge1\), its exact certificate proves

\[
\max_i \kappa(M_m\parallel E_i)=2,
\qquad
\kappa_{\mathrm{open}}(M_m;\mathcal E_m)=m+1.
\]

Thus every fixed closed extension has a four-state interface, whereas the
open-safe interface is the full \(2^{m+1}\)-state microstate partition.

`TraceSeparationCertificate` is the coordinate lower-bound object: for every
unequal pair of states it records either `observe` or a declared `probe:i`
action whose one-step focal-output traces differ. This is an explicit finite
proof object, not a simulation summary.

### Bounded-degree relay-tree compilation

`causal_model/relay_tree_compilation.py` proves that the coordinate witness is
not relying on a growing local lookup table or a high-degree focal node. It
compiles every size into a binary tree with one fixed grammar:

- reader states `ready` / `fire`;
- memory leaves with a permanent bit and a three-valued pulse;
- three-valued relay pulses; and
- a binary focal root output.

Messages are directed along child-to-parent edges. With one attached reader,
every node has degree at most three. The declared sequential action grammar
allows one reader firing followed by return to quiescence.

`RelayProtocolCertificate` replays the complete micro-trajectory for a state and
port. `BoundedDegreeCompilationCertificate` checks every quiescent coordinate
state and every port in the declared finite range, proving that the completed
macro probe is exactly conjugate to the coordinate action.

The existing \(2\) versus \(m+1\) separation therefore now holds under a
constant grammar, edge-local pairwise messages, bounded degree, and quiescent
macro-time. It still must not be described as a literal ecological model, and
the theorem does not cover simultaneous reader firings, stochasticity, or
undeclared environments.

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

This layer does not decide closure or open-interface complexity by itself. It
only controls how safely candidate dynamics may be removed as data accumulate.

## Layer 3: certificates

Exact certificates prevent simulation output from being promoted directly to a
strong conclusion.

- finite closure rankings, cycles, and multistability certificates;
- open-interface trace-separation certificates;
- bounded-degree relay protocol and macro-conjugacy certificates;
- rational SAT witnesses and Farkas infeasibility certificates; and
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
- manifest v1/v2 adapters, transcript variants, and checkpoint plumbing; and
- polyhedral admission machinery outside a problem that genuinely needs its
  restricted grammar.

They should be reused only when they serve an active core question, not because
they already exist.

## GitHub Actions policy

When a theorem is implemented over a finite declared domain, its pull request
should contain:

1. a written theorem statement and explicit scope boundary;
2. an independently checkable certificate verifier;
3. targeted counterexample and fail-closed tests;
4. exhaustive model checking whenever the declared domain is small enough; and
5. a workflow artifact containing the deterministic enumeration summary.

Current examples are:

- finite closure theorem regression over all maps on up to four states;
- observation-regime theorem regression over all ordered map pairs on up to
  three states;
- extension--compression regression for the explicit coordinate witness family
  with one through six ports; and
- relay-tree compilation regression for one through six ports, all quiescent
  states, and all declared reader attachments.

Passing CI is not a proof of a theorem outside its finite stated domain.
