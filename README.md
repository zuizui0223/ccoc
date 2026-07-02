# RACH Causal Invariants

RACH is a theorem-first repository about one structural question:

> **When does a finite causal macro-law remain exact after the permitted outside
> of a focal window expands?**

Every claim is conditional on an explicitly declared finite state space, action
or boundary grammar, completion family, and—where relevant—candidate mechanism
family. The repository contains no empirical data and makes no automatic claim
about real ecosystems.

## Start here

- [Portability core v1](docs/portability_core_v1.md) — the canonical structural
  theorem family.
- [Non-nested replacement portability](docs/non_nested_replacement_portability.md)
  — the one selected post-v1 structural extension.
- [Claim-status audit](docs/claim_status_audit.md) — theorem domains, sufficient
  criteria, lower bounds, witnesses, no-go results, and `UNRESOLVED` boundaries.
- [Research priorities](docs/research_priorities.md) — active branch and stop
  rules.
- [Theorem spine](docs/theorem_spine.md) — the core/extension/companion map.
- [Legacy shelf](docs/legacy/README.md) — valid but frozen experiment-design work.

## Public imports

```python
import causal_model.portability_core as rach
import causal_model.identifiability_companion as rach_id
```

`causal_model.current_theory` is a broad historical compatibility aggregate, not
a public entrance for new theorem work.

## Portability core v1

### Positive side

A finite portable macro-law is possible when every allowed future effect factors
through one finite summary that preserves outputs, legal actions, and successor
summaries:

\[
\boxed{
\text{finite update-consistent boundary summary}
\Rightarrow
\text{exact macro-interface.}
}
\]

For growing **nested** composition, a common summary alphabet only bounds memory.
One shared law additionally requires common macro dynamics and label-coherent
embeddings. When legal action rows grow, old macro meanings must remain fixed and
new actions must be label-deterministic.

### Negative side

When a reachable subsystem contains independently future-addressable exterior
factors,

\[
S^*\cong I\times E_1\times\cdots\times E_q,
\]

then every exact open interface obeys

\[
\boxed{
K_{\mathrm{open}}
\ge
\log_2|I|+\sum_j\log_2|E_j|.
}
\]

If each fixed closed context \(j\) factors through \((I,E_j)\), then

\[
\boxed{
K_{\mathrm{open}}-\max_jK_{\mathrm{closed},j}
\ge
\sum_j\log_2|E_j|-\max_j\log_2|E_j|.
}
\]

Thus a small law in every fixed closed context need not yield one small law
portable to future addition, removal, reconnection, or newly permitted actions.
The bounded-degree relay tree is a sharpness witness, not a separate headline
claim.

## Selected post-v1 extension: replacement without nesting

The repository's sole active structural extension handles finite replacement,
extinction, and rewiring families that have no raw-state inclusion map between
stages. A declared replacement edge may instead carry a total,
output/legal-action/label-preserving, successor-closed transport relation.

The current theorem is a **sufficient transport-coherence criterion**: every
stage must already factor through the same exact macro dynamics, and the declared
replacement graph must be connected. A many-to-one three-state-to-two-state
witness demonstrates that this is not merely an embedding restatement. A newly
legal word can also refute a proposed carried merge after rewiring.

It does **not** yet establish a necessary characterization, construct a target
projection solely from a source projection and transport, or infer a replacement
grammar from data.

## Companion programs

### Identifiability

Delayed-addressability and adaptive-experiment results ask what finite evidence
can establish about closure. Without an independently justified finite horizon and
grammar contract, the honest conclusion can be `UNRESOLVED`.

Candidate-safe and joint exterior–mechanism laws ask whether retained mechanism
families share one macro transition. They are companion questions, not premises
of the portability core.

### Experimental design

Reset panels, evidence coverage, robustness, and common-mode failure results are
executable legacy branches. They apply after a quotient or contract has already
been fixed.

## Certificate discipline

A passing finite workflow is not a claim about arbitrary ecosystems. Every active
result must state:

1. a finite domain and legal grammar;
2. whether it is an exact theorem, sufficient criterion, lower bound, sharp
   witness, no-go result, or `UNRESOLVED` boundary;
3. an independently checkable certificate;
4. fail-closed and counterexample tests; and
5. finite replay only inside the declared domain.

## Scope boundary

RACH does not prove that empirical ecosystems are finite deterministic systems,
that passive data are useless, or that arbitrary exterior conditions can be
exhausted. It gives precise finite-domain criteria for when a proposed macro-law
is certified, obstructed, candidate-safe, set-valued, or unresolved.
