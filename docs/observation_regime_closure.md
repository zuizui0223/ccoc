# Observation-regime closure: when a rule changes with the observer-coupled regime

## Narrow claim

This module does **not** claim that observation creates reality, and it does not
borrow any general conclusion from quantum measurement. It formalizes a finite,
operational statement:

\[
F^{(0)}:S\to S,
\qquad
F^{(1)}:S\to S,
\]

are two declared update rules on the same finite state space. The first is the
natural regime; the second is an observer-coupled regime in which measurement,
tracking, monitoring, management, or another declared observation action is
part of the update mechanism.

The only question is whether the two maps have the same exact global closure
class.

## Individual-regime certificates

Each regime uses the finite closure calculus:

- `GLOBAL_CLOSURE` is proved by an integer ranking \(V\) with strict descent
  outside one fixed point;
- `RECURRENT_NONCLOSURE` is proved by an exact directed cycle of period at least
  two; and
- `MULTISTABLE_NONCLOSURE` is proved by two distinct fixed points.

The pair-level module does not add a simulation heuristic. It only compares two
independently certified classifications.

## Exact pair verdicts

| Natural regime | Observer-coupled regime | Verdict |
|---|---|---|
| global closure | global closure | `OBSERVER_INDEPENDENT_CLOSURE` |
| non-closure | global closure | `OBSERVATION_INDUCED_CLOSURE` |
| global closure | recurrent non-closure | `OBSERVATION_INDUCED_RECURRENCE` |
| global closure | multistable non-closure | `OBSERVATION_INDUCED_MULTISTABILITY` |
| recurrent non-closure | recurrent non-closure | `OBSERVER_INDEPENDENT_RECURRENCE` |
| multistable non-closure | multistable non-closure | `OBSERVER_INDEPENDENT_MULTISTABILITY` |
| other non-closure transition | `REGIME_DEPENDENT_NONCLOSURE` |

For example,

\[
F^{(0)}\text{ recurrent},
\qquad
F^{(1)}\text{ globally closing}
\]

means that the declared observer-coupled update rule closes a system that the
declared natural update rule does not. It does **not** prove that a real-world
measurement is invasive unless the two maps and their regime interpretation are
empirically justified.

## RACH-style candidate uncertainty

A candidate is a pair

\[
\theta_i=(F_i^{(0)},F_i^{(1)}).
\]

A family-level conclusion is decisive only when every retained candidate pair
has the same pair verdict:

\[
\forall\theta_i\in C_t,
\quad
v(\theta_i)=v^\star.
\]

Then RACH can report \(v^\star\). If retained pairs disagree, it reports
`UNRESOLVED`. This prevents a single convenient observer-coupled model from
being mistaken for a conclusion robust to candidate uncertainty.

## Exhaustive theorem regression

The GitHub Actions workflow enumerates all labelled maps on one, two, and three
states. For three states there are

\[
3^3=27
\]

maps and hence

\[
(3^3)^2=729
\]

ordered natural/observer-coupled pairs. For every pair the workflow verifies
both finite closure classifications and checks that the regime verdict is the
one implied by the exact kind table. It uploads a deterministic JSON count
report.

This is exhaustive model checking in the finite deterministic theorem domain.
It is not a proof for continuous, stochastic, hidden-state, or empirically
unjustified observation-feedback systems.

## Why this is useful

The distinction is not whether a pattern is “real.” It is whether the claimed
rule is:

\[
\text{observer-independent},
\quad
\text{observer-stabilized},
\quad
\text{observer-destabilized},
\quad\text{or unresolved under candidate uncertainty}.
\]

That is a sharper question than merely asking whether the local transition rule
is valid at observed time points.
