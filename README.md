# RACH Causal Invariants

RACH is a theorem-first methods repository about one question:

> **When may a rule discovered inside a finite observation window be promoted to
> a portable causal law, and what certificate is required for that promotion?**

It contains no empirical dataset and makes no domain-specific ecological claim.
Every theorem is conditional on an explicitly declared finite state space, action
or boundary grammar, completion family, and—when relevant—retained candidate
family.

## The central result in one picture

```text
local rule
   |
   +-- time: does it close, cycle, or have multiple attractors?
   |
finite observation window
   |
   +-- outside memory: can unobserved completions be separated later?
   +-- outside delay: can a legal exterior event occur only after the horizon?
   +-- dynamic blanket: can outside influence be stored in an update-closed summary?
   |
retained candidate family
   |
   +-- do all candidates induce the same open macro transition?
           |
           +-- yes: universal deterministic open law
           +-- no, type retained: candidate-safe deterministic open law
           +-- no, type forgotten: set-valued law or UNRESOLVED
```

The authoritative map is [the theorem spine](docs/theorem_spine.md). Read it
before extending an older module.

## What is proved in the active core

### 1. Local truth does not imply global closure

A finite deterministic update map can have a recurrence or multiple fixed
points even when every local transition is specified. RACH certifies global
closure, recurrent nonclosure, or multistability exactly.

### 2. Passive agreement does not imply open-system validity

For the explicit window-completion family,

\[
K_{\mathrm{passive}}=1,
\qquad
K_{\mathrm{open}}=m+1.
\]

Distinct exterior completions can agree under every passive trace and be
separated by a declared future boundary action.

### 3. Closed-context compression need not survive open composition

For operationally addressable exterior coordinates,

\[
K_{\mathrm{open}}
\ge
\log_2|I|+
\sum_j\log_2|E_j|.
\]

For binary coordinates the bounded-degree relay-tree family attains

\[
K_{\mathrm{open}}=q+1,
\qquad
\max_iK_{\mathrm{closed},i}=2.
\]

### 4. A finite dynamic blanket is the positive criterion

An exterior summary is sufficient only when it preserves outputs **and** updates
consistently after every allowed action. Such a dynamic blanket gives a finite
exact open interface and a finite counterfactual-horizon bound for each fixed
finite system.

### 5. No horizon works uniformly across delayed outside families

The delayed-addressability family independently controls exterior memory and the
first legal time it can be revealed:

\[
K_{\mathrm{open}}=m+1,
\qquad
H_\star=H+1.
\]

Thus finite certification for every fixed system does not imply a common finite
closure horizon for an expanding family.

### 6. Instance laws need not form a universal law

Each retained candidate can have a small exact macro-law while inducing a
different macro transition from the same observable state. A universal
deterministic law exists exactly when all induced candidate maps agree.

Under uniform response separation,

\[
K_{\mathrm{candidate\text{-}safe}}
\ge
\log_2|Q|+
\log_2R.
\]

When response type is forgotten, the exact prediction is set-valued rather than
silently deterministic.

### 7. Exterior and mechanism information add only under joint separation

A universal **open** law requires both an update-closed interface in every
retained candidate and agreement of the induced macro maps across candidates.
For a jointly realizable product family with a concrete legal separator for each
unequal state,

\[
K_{\mathrm{joint\text{-}safe}}
\ge
\log_2|I|+
\sum_j\log_2|E_j|+
\log_2|R|.
\]

The canonical structural witness attains this bound using one fixed local action
alphabet. This is not an automatic sum of earlier lower bounds: the explicit
joint-separation premise is essential.

## Start here

The public theory entrance is intentionally small:

```python
from causal_model.current_theory import (
    classify_closure,
    certify_observation_window_completion,
    certify_addressable_completion_product,
    certify_dynamic_boundary_blanket,
    certify_delayed_addressability,
    certify_candidate_safe_product,
    certify_joint_exterior_mechanism_product,
)
```

`causal_model.__init__` remains broad for backwards compatibility. It is not the
research entrance for new theorem work.

## Reading order

1. [Theorem spine](docs/theorem_spine.md) — proved claims, scope, and frontier.
2. [Promotion calculus](docs/promotion_calculus.md) — how the claims fit together.
3. [Current architecture](docs/current_architecture.md) — code, certificate, and
   workflow map.
4. [Asset map](docs/repository_asset_map.md) — active core versus future gold and
   frozen infrastructure.
5. Individual theorem documents:
   - [observation-window completion](docs/observation_window_completion.md)
   - [addressable-completion product bound](docs/addressable_completion_product_bound.md)
   - [dynamic boundary blankets](docs/dynamic_boundary_blankets.md)
   - [delayed addressability](docs/delayed_addressability.md)
   - [candidate-safe universal laws](docs/candidate_safe_universal_laws.md)
   - [joint open-candidate laws](docs/joint_open_candidate_laws.md)

## Certificate discipline

A passing finite workflow is not a claim about arbitrary ecosystems. Every new
mathematical PR should provide:

1. a theorem statement and exact scope boundary;
2. an independently checkable certificate object;
3. fail-closed and counterexample tests;
4. finite enumeration only as certificate replay in a declared domain; and
5. a deterministic Action report.

## Scope boundary

RACH does not prove that empirical ecosystems are finite deterministic systems,
that passive data are useless, or that arbitrary exterior conditions can be
exhausted. It gives precise finite-domain statements about when a proposed
promotion is certified, obstructed, candidate-safe, or necessarily set-valued.