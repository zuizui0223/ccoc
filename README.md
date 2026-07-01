# RACH Causal Invariants

RACH is a theorem-first methods repository for one narrow question:

> **When may a rule discovered inside a finite observation window be promoted to
> a portable causal law, and which certificate is needed for that promotion?**

It contains no empirical data and makes no domain-specific causal claim.

## RACH is a promotion calculus

| Axis | Invalid automatic promotion | RACH response |
|---|---|---|
| Time | local update \(\Rightarrow\) one global endpoint | closure, recurrence, or multistability certificate |
| Window / outside | rule inside a passive observed window \(\Rightarrow\) rule under every allowed exterior completion | counterfactual completion and open-interface certificate |
| Knowledge | one convenient candidate \(\Rightarrow\) justified claim | unanimity across retained candidates or `UNRESOLVED` |

Read [the promotion calculus](docs/promotion_calculus.md) for the unifying
relation and [the asset map](docs/repository_asset_map.md) before extending an
older module.

## Current theory core

The focused public entrance is deliberately small:

```python
from causal_model.current_theory import (
    FiniteDeterministicRuleSystem,
    classify_closure,
    certify_observation_window_completion,
    certify_extension_compression,
    certify_bounded_degree_compilation,
    summarize_regime_candidates,
)
```

New theorem work should begin here, not from the broad legacy package exports.
See [the current architecture map](docs/current_architecture.md).

## What the core proves

### 1. Local transition truth does not imply global closure

For a finite total deterministic update map

\[
F:S\to S,
\]

RACH classifies the long-run behavior as exactly one of:

| Result | Exact certificate |
|---|---|
| `GLOBAL_CLOSURE` | strict integer ranking descending to one fixed point |
| `RECURRENT_NONCLOSURE` | a directed cycle of period \(p\ge2\) |
| `MULTISTABLE_NONCLOSURE` | two or more distinct fixed points |

Thus every local transition may be correct while repeated application fails to
produce one stable world-level endpoint. See the
[closure calculus](docs/causal_closure_calculus.md).

### 2. Finite passive observation does not certify causal closure

An observation window sees an inside output while exterior completion states
remain latent. In the explicit witness family, passive actions never reveal
those completion bits, but a declared future boundary action can.

For every \(m\ge1\),

\[
K_{\mathrm{passive}}=1,
\qquad
K_{\mathrm{open}}=m+1.
\]

Equivalently, each visible focal output is compatible with \(2^m\) exterior
completion states under arbitrarily long passive observation, while the
open-safe interface must retain all completion-relevant distinctions.

This proves an existence no-go, not a universal impossibility theorem:
within a fixed bounded-degree model class, passive traces alone cannot rule out
all future-relevant exterior completions. See
[observation-window completion](docs/observation_window_completion.md).

### 3. Closed-context compression need not survive open composition

The same coordinate family may be viewed as a focal system with \(m\) dormant
boundary modules. If a closed context permits one fixed port, its exact causal
interface has four states. If a future context may probe any declared port,
every microstate is distinguishable.

\[
\max_i \kappa(M_m\parallel E_i)=2,
\qquad
\kappa_{\mathrm{open}}(M_m;\mathcal E_m)=m+1.
\]

This is the extension--compression lower-bound family. See
[extension--compression noncommutation](docs/extension_compression_noncommutation.md).

### 4. The witness survives a bounded-degree local implementation

The coordinate witness is compiled into a one-token reader / memory-leaf /
relay / root protocol with:

- one fixed finite local grammar;
- edge-local child-to-parent pairwise messages;
- maximum graph degree three, including one attached reader; and
- quiescent macro-time between sequential probes.

The completed protocol exactly implements the coordinate probe action, so the
same lower bounds survive without a high-degree root or a growing local lookup
table. See [bounded-degree relay-tree compilation](docs/bounded_degree_relay_compilation.md).

### 5. Candidate consensus is the epistemic gate

RACH does not require complete model identification. Let \(C_t\) be retained
candidate systems and let \(v(\theta)\) be a claim-level verdict.

\[
\forall\theta\in C_t,
\quad v(\theta)=v^\star
\quad\Longrightarrow\quad
\text{report }v^\star.
\]

If retained candidates disagree, the output is `UNRESOLVED`.

This does not itself prove an open-system law. It prevents one selected candidate
from being promoted to a general conclusion without a retained-family
certificate.

### 6. Observation-regime comparison is an operational special case

`observation_regime_closure.py` compares two declared maps on the same state
space, for example a natural and an observer-coupled regime. It remains useful
when that exact two-regime question is the claim. In the current architecture it
is one way of changing a declared action grammar, rather than a generic claim
that observation changes ecosystems.

## Mathematical boundary

Current exact theorems apply to **finite labelled deterministic systems** with
explicitly declared state spaces, action alphabets, completion grammars, and—when
needed—admissible ports. They do not prove analogous facts for arbitrary
continuous, stochastic, hidden-state, simultaneous, or empirical systems.

For a finite theorem domain, RACH uses certificates rather than simulation
appearance:

\[
\text{simulation evidence}
\neq
\text{proof of closure or open-system validity}.
\]

A finite simulation can find a completion counterexample or exhaust a declared
finite grammar. It cannot establish validity against an unbounded outside without
a separate finite-boundary or blanket theorem.

## GitHub Actions theorem regression

Dedicated workflows model-check declared finite theorem domains:

- all labelled deterministic maps on one through four states:
  \[
  1^1+2^2+3^3+4^4=288;
  \]
- all ordered natural/observer-coupled map pairs on one through three states:
  \[
  (1^1)^2+(2^2)^2+(3^3)^2=746;
  \]
- the coordinate extension--compression family for one through six ports;
- the degree-three relay-tree compilation for one through six ports, every
  quiescent state, and every declared reader attachment; and
- the observation-window completion family for one through six exterior modules,
  every passive word through a declared finite horizon, both focal states, and
  every boundary port.

Each workflow runs targeted tests, certificate verification, and uploads a
deterministic JSON report. Passing these workflows is finite model checking of
the declared domain, not a general proof assistant.

## Supporting assets: where the old work belongs

The repository contains valuable earlier work. It is not all the current theory
core.

- **Evidence gateway:** confidence lifting, anytime lifting, symbolic candidate
  sets, and the finite-alphabet e-process work can eventually supply retained
  completion families from data.
- **Counterexample miner:** rational proof checking, polyhedral inclusion, and
  replayable exact artifacts can certify finite countermodels to bad blanket or
  preservation conjectures.
- **Adversarial model lab:** ecological-program grammars, failure modes,
  observation envelopes, design algorithms, and exact benchmarks can red-team
  completion-theorem assumptions.
- **Frozen provenance:** manifests, transcripts, signatures, and checkpoints
  preserve artifact identity but do not establish the scientific claim.

The [asset map](docs/repository_asset_map.md) names concrete modules and states
when each should be reused or frozen.

## Development rule

A new mathematical PR should contain:

1. a theorem statement and explicit scope boundary;
2. a verifier for its certificate object;
3. fail-closed counterexample tests;
4. exhaustive finite model checking when feasible; and
5. an Action artifact reporting the finite enumeration.

## Scope boundary

RACH is not a floral-trait, pollination, fitness, population-genetic,
site-level, or field-protocol model. All conclusions remain conditional on the
declared observation window, completion grammar, candidate systems, action
regime, certificate validity, and—when sequential evidence is used—the external
coverage assumptions.
