# RACH Causal Invariants

RACH is a theorem-first methods repository for one narrow question:

> **When may a local or conditional causal statement be promoted to a portable
> macro-law, and which certificate is needed for that promotion?**

It contains no empirical data and makes no domain-specific causal claim.

## RACH is a promotion calculus

A causal statement can fail to promote along four distinct axes:

| Axis | Invalid automatic promotion | RACH response |
|---|---|---|
| Time | local update rule \(\Rightarrow\) one global endpoint | closure, recurrence, or multistability certificate |
| Regime | natural-regime law \(\Rightarrow\) observer-coupled law | paired-regime verdict |
| Composition | small law in every fixed closed context \(\Rightarrow\) small law in an open system | open-safe interface certificate |
| Knowledge | one convenient candidate \(\Rightarrow\) justified claim | unanimity across retained candidates or `UNRESOLVED` |

Read [the promotion calculus](docs/promotion_calculus.md) for the unifying
relation, and [the asset map](docs/repository_asset_map.md) before extending an
older module.

## Current theory core

The focused public entrance is deliberately small:

```python
from causal_model.current_theory import (
    FiniteDeterministicRuleSystem,
    classify_closure,
    ObservationRegimeRulePair,
    classify_observation_regime_pair,
    summarize_regime_candidates,
    certify_extension_compression,
    certify_bounded_degree_compilation,
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

This is an operational comparison of declared dynamics. It does **not** claim
that observation creates reality or that empirical observation is necessarily
invasive. See [observation-regime closure](docs/observation_regime_closure.md).

### 3. Candidate consensus is the RACH epistemic rule

RACH does not require complete model identification. Let \(C_t\) be retained
candidate systems and let \(v(\theta)\) be a claim-level verdict.

\[
\forall\theta\in C_t,
\quad v(\theta)=v^\star
\quad\Longrightarrow\quad
\text{report }v^\star.
\]

If retained candidates disagree, the output is `UNRESOLVED`.

This is not the open-composition theorem itself. It is the rule that prevents
one selected candidate from being promoted to a general conclusion without a
retained-family certificate.

### 4. Compression need not survive declared ecological extension

For every \(m\ge1\), the extension--compression witness contains a focal output
bit and \(m\) dormant boundary-memory bits. If a closed context permits access
to only one fixed port, its exact causal interface has four states. If the
future context may access any declared port, every microstate is distinguishable
by either current output or one allowed probe.

\[
\max_i \kappa(M_m\parallel E_i)=2,
\qquad
\kappa_{\mathrm{open}}(M_m;\mathcal E_m)=m+1.
\]

Equivalently, each fixed closed extension has a four-state macro-law, while the
open interface requires \(2^{m+1}\) states. This is a finite no-go witness for
assuming that local or closed-system causal compression automatically transfers
to an open system. See
[extension--compression noncommutation](docs/extension_compression_noncommutation.md).

### 5. The separation survives a bounded-degree local compilation

The coordinate witness is compiled into a one-token reader / memory-leaf /
relay / root protocol with:

- one fixed finite local grammar;
- edge-local child-to-parent pairwise messages;
- maximum graph degree three, including one attached reader; and
- quiescent macro-time between sequential probes.

The completed protocol exactly implements the coordinate probe action, so the
same \(2\) versus \(m+1\) separation survives without a high-degree root or a
growing local lookup table. See
[bounded-degree relay-tree compilation](docs/bounded_degree_relay_compilation.md).

## Mathematical boundary

Current exact theorems apply to **finite labelled deterministic systems** with
explicitly declared state spaces, action alphabets, and—in the extension
theorem—explicitly declared admissible ports. They do not prove analogous facts
for arbitrary continuous, stochastic, hidden-state, simultaneous, or empirical
systems.

For a finite theorem domain, RACH uses certificates rather than simulation
appearance:

\[
\text{simulation evidence}
\neq
\text{proof of closure, recurrence, or an interface lower bound}.
\]

A valid certificate proves only the conclusion and scope it explicitly states.

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
- the explicit coordinate extension--compression family for one through six
  ports; and
- the degree-three relay-tree compilation for one through six ports, every
  quiescent state, and every declared reader attachment.

Each workflow runs targeted tests, certificate verification, and uploads a
deterministic JSON report. Passing these workflows is finite model checking of
the declared domain, not a general proof assistant.

## Supporting assets: where the old work belongs

The repository contains valuable earlier work. It is not all the current theory
core.

- **Evidence gateway:** confidence-set lifting, anytime lifting, symbolic
  candidate sets, and the finite-alphabet e-process work can eventually supply
  retained composition families from data.
- **Counterexample miner:** rational proof checking, polyhedral inclusion, and
  replayable exact artifacts can certify finite countermodels to bad conjectures.
- **Adversarial model lab:** ecological-program grammars, failure modes,
  observation envelopes, design algorithms, and exact benchmarks can red-team
  theorem assumptions.
- **Frozen provenance:** manifests, transcripts, signatures, and checkpoints
  preserve artifact identity but do not establish the scientific claim.

The [asset map](docs/repository_asset_map.md) names the concrete modules and
states when each should be reused or frozen.

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
declared candidate systems, observation regime, action grammar, certificate
validity, and—when sequential evidence is used—the external coverage
assumptions.
