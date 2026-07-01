# RACH Causal Invariants

RACH is a theorem-first methods repository for one narrow question:

> **When may a rule discovered inside a finite observation window be promoted to
> a portable causal law, and which certificate is needed for that promotion?**

It contains no empirical data and makes no domain-specific causal claim.

## RACH is a promotion calculus

| Axis | Invalid automatic promotion | RACH response |
|---|---|---|
| Time | local update \(\Rightarrow\) one global endpoint | closure, recurrence, or multistability certificate |
| Window / outside | rule inside a passive observed window \(\Rightarrow\) rule under every allowed exterior completion | lower-bound, dynamic-blanket, and counterfactual-horizon certificates |
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
    certify_addressable_completion_product,
    certify_dynamic_boundary_blanket,
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

RACH classifies long-run behavior as exactly one of:

| Result | Exact certificate |
|---|---|
| `GLOBAL_CLOSURE` | strict integer ranking descending to one fixed point |
| `RECURRENT_NONCLOSURE` | a directed cycle of period \(p\ge2\) |
| `MULTISTABLE_NONCLOSURE` | two or more distinct fixed points |

Thus every local transition may be correct while repeated application fails to
produce one stable world-level endpoint. See the
[closure calculus](docs/causal_closure_calculus.md).

### 2. Finite passive observation does not certify causal closure

An observation window can hide exterior completion states. In the explicit
family, passive actions never reveal them, but a declared future boundary action
can.

\[
K_{\mathrm{passive}}=1,
\qquad
K_{\mathrm{open}}=m+1.
\]

Thus each visible focal output is compatible with \(2^m\) exterior completion
states even under arbitrarily long passive observation. This is an existence
no-go in a declared bounded-degree model class, not a universal claim that
passive data are useless. See
[observation-window completion](docs/observation_window_completion.md).

### 3. Closed-context compression need not survive open composition

For operationally addressable exterior coordinates

\[
I\times E_1\times\cdots\times E_q,
\]

concrete separating boundary words imply

\[
K_{\mathrm{open}}
\ge
\log_2|I|+
\sum_{j=1}^q\log_2|E_j|.
\]

If a fixed closed context reads only \(E_c\),

\[
K_{\mathrm{open}}-\max_cK_{\mathrm{closed},c}
\ge
\sum_j\log_2|E_j|-\max_c\log_2|E_c|.
\]

For binary exterior modules, the relay-tree family attains

\[
K_{\mathrm{open}}=q+1,
\qquad
\max_cK_{\mathrm{closed},c}=2.
\]

See [addressable-completion product bounds](docs/addressable_completion_product_bound.md).

### 4. The lower bound survives a bounded-degree local implementation

The coordinate witness is compiled into a one-token reader / memory-leaf /
relay / root protocol with:

- one fixed finite local grammar;
- edge-local child-to-parent pairwise messages;
- maximum graph degree three, including one attached reader; and
- quiescent macro-time between sequential probes.

The completed protocol exactly implements the coordinate probe action, so the
same lower bounds survive without a high-degree root or a growing local lookup
table. See [bounded-degree relay-tree compilation](docs/bounded_degree_relay_compilation.md).

### 5. Dynamic boundary blankets are the positive criterion

An exterior summary is an exact open interface only if it is dynamically closed:
equal summaries must have equal current outputs and must update to equal future
summaries under every allowed action.

For a finite controlled system, the all-word trace quotient is the coarsest exact
extension-stable deterministic interface. If an inside-plus-boundary pair
\((\alpha,\beta)\) is dynamically closed, then

\[
K_{\mathrm{open}}
\le
\log_2|\operatorname{im}(\alpha,\beta)|
\le
\log_2|I|+\log_2|B|.
\]

The same finite summary bounds the counterfactual depth needed to certify the
canonical quotient:

\[
H_\star\le |\operatorname{im}(\alpha,\beta)|-1.
\]

Conversely, the addressable binary family forces

\[
\log_2|B_m|\ge m,
\]

so no uniformly bounded blanket can serve every growing exterior-completion
family. See [dynamic boundary blankets](docs/dynamic_boundary_blankets.md).

### 6. Candidate consensus is the epistemic gate

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

### 7. Observation-regime comparison is an operational special case

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

A finite calculation can find a completion counterexample or replay a declared
certificate. It cannot establish validity against an unbounded outside without a
separate dynamic-boundary theorem.

## GitHub Actions theorem regression

Dedicated workflows replay declared finite theorem certificates for:

- all labelled deterministic maps on one through four states;
- all ordered natural/observer-coupled map pairs on one through three states;
- the coordinate extension--compression family for one through six ports;
- the degree-three relay-tree compilation for one through six ports;
- the observation-window completion family for one through six exterior modules;
- binary and nonbinary addressable-completion products; and
- finite-horizon stabilization, dynamic-blanket factorization, and uniform
  blanket obstruction families.

Each workflow runs targeted tests, certificate verification, and uploads a
deterministic JSON report. Passing these workflows is finite certificate replay
for the declared domain, not a general proof assistant.

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
4. exhaustive finite model checking only when it checks a declared certificate;
   and
5. an Action artifact reporting the deterministic replay.

## Scope boundary

RACH is not a floral-trait, pollination, fitness, population-genetic,
site-level, or field-protocol model. All conclusions remain conditional on the
declared observation window, completion grammar, candidate systems, action
regime, certificate validity, and—when sequential evidence is used—the external
coverage assumptions.
