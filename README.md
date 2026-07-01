# RACH Causal Invariants

RACH is a theorem-first repository about one structural question:

> **When does a finite causal macro-law remain exact after the permitted outside of a focal window expands?**

Every result is conditional on an explicitly declared finite state space, action
or boundary grammar, completion family, and—when relevant—candidate mechanism
family. The repository contains no empirical dataset and makes no automatic
claim about real ecosystems.

## Start here

- [Portability core v1](docs/portability_core_v1.md) — the canonical structural
  theorem family.
- [Research priorities and theorem freeze](docs/research_priorities.md) — what
  is active, what is companion work, and what is deliberately paused.
- [Theorem spine](docs/theorem_spine.md) — detailed statements and scope.
- [Legacy shelf](docs/legacy/README.md) — valid but frozen experiment-design
  branches.

## The portability core in one page

### Positive side

A finite portable macro-law is possible when every allowed future effect factors
through one finite summary that preserves outputs, legal actions, and successor
summaries.

\[
\boxed{
\text{finite update-consistent boundary summary}
\Rightarrow
\text{exact macro-interface.}
}
\]

For growing composition, a common summary size only gives bounded memory. One
portable law further requires common macro dynamics and label-coherent embeddings.
If legal action rows grow, newly admitted actions must have one
label-deterministic macro meaning and old meanings must not change.

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
\log_2|I|+
\sum_j\log_2|E_j|.
}
\]

If each fixed closed context \(j\) factors through \((I,E_j)\), then

\[
\boxed{
K_{\mathrm{open}}-
\max_jK_{\mathrm{closed},j}
\ge
\sum_j\log_2|E_j|-
\max_j\log_2|E_j|.
}
\]

Thus a small law in every fixed closed context need not yield one small law
portable to future species addition, removal, reconnection, or newly permitted
interventions.

The bounded-degree relay tree is a sharpness witness for this lower bound; it is
not a separate headline theory.

## Companion programs

### Identifiability

Delayed-addressability and adaptive-experiment results ask what finite evidence
can establish about closure. Without an independently justified finite horizon
and grammar contract, the honest result can be

\[
\mathrm{UNRESOLVED}.
\]

Candidate-safe and joint exterior–mechanism laws ask whether retained mechanism
families share one macro transition. These are companion questions, not premises
of the portability core.

### Experimental design

Reset panels, evidence coverage, robustness, and common-mode failure results are
kept as executable legacy branches. They apply after a quotient or contract has
already been fixed.

## Certificate discipline

A passing finite workflow is not a claim about arbitrary ecosystems. Every active
mathematical result must state:

1. its finite domain and legal grammar;
2. whether it is an exact theorem, sufficient criterion, lower bound, or sharp
   witness;
3. an independently checkable certificate;
4. fail-closed and counterexample tests; and
5. finite replay only as verification inside the declared domain.

## Scope boundary

RACH does not prove that empirical ecosystems are finite deterministic systems,
that passive data are useless, or that arbitrary exterior conditions can be
exhausted. It gives precise finite-domain criteria for when a proposed macro-law
is certified, obstructed, candidate-safe, set-valued, or unresolved.