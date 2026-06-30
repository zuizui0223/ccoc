"""Exact closure and recurrence certificates for finite deterministic rule systems.

This module isolates a precise mathematical distinction needed for a theory of
complex ecological rules:

    local transition validity != global closure.

A finite deterministic rule system is a total map ``F: S -> S``.  Every local
transition can be perfectly specified, while repeated application of F can
still yield:

* global closure: every state reaches one fixed point;
* recurrent non-closure: at least one nontrivial directed cycle exists; or
* multistable non-closure: several fixed points exist without nontrivial
  recurrence.

The first two conclusions are backed by exact finite certificates:

* A ``GlobalClosureCertificate`` gives a fixed point x* and an integer ranking
  V with V(x*)=0 and V(F(x)) < V(x) for every x != x*.  This proves that every
  trajectory reaches x* in at most max(V) steps.
* A ``RecurrentCycleCertificate`` gives distinct states x_0,...,x_{p-1} with
  F(x_i)=x_{i+1 mod p}.  For p >= 2 this proves that global convergence to a
  single fixed point is false.

Because the state space is finite, the module can construct and independently
verify those certificates.  The exhaustive theorem checker enumerates all maps
on small labelled state spaces and confirms that exact classification agrees
with direct orbit analysis.  This is finite model checking, not a claim of
formal verification for arbitrary continuous or stochastic dynamics.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import product
from typing import Iterable, Mapping


class ClosureKind(str, Enum):
    """Exact finite-state long-run classifications."""

    GLOBAL_CLOSURE = "global_closure"
    RECURRENT_NONCLOSURE = "recurrent_nonclosure"
    MULTISTABLE_NONCLOSURE = "multistable_nonclosure"


@dataclass(frozen=True)
class FiniteDeterministicRuleSystem:
    """A total deterministic update rule on a finite labelled state space."""

    states: tuple[str, ...]
    successor_by_state: Mapping[str, str]
    rule_id: str = "finite-deterministic-rule"

    def __post_init__(self) -> None:
        if not self.states:
            raise ValueError("states must be non-empty")
        if len(set(self.states)) != len(self.states):
            raise ValueError("states must be unique")
        if any(not isinstance(state, str) or not state for state in self.states):
            raise ValueError("states must be non-empty strings")
        if not isinstance(self.rule_id, str) or not self.rule_id:
            raise ValueError("rule_id must be a non-empty string")
        state_set = set(self.states)
        if set(self.successor_by_state) != state_set:
            raise ValueError("successor_by_state must define exactly one successor for every state")
        if any(successor not in state_set for successor in self.successor_by_state.values()):
            raise ValueError("every successor must lie in the declared state space")

    def successor(self, state: str) -> str:
        try:
            return self.successor_by_state[state]
        except KeyError as error:
            raise ValueError(f"unknown state {state!r}") from error

    def iterate(self, state: str, steps: int) -> str:
        if not isinstance(steps, int) or steps < 0:
            raise ValueError("steps must be a non-negative integer")
        current = state
        for _ in range(steps):
            current = self.successor(current)
        return current

    @property
    def fixed_points(self) -> tuple[str, ...]:
        return tuple(state for state in self.states if self.successor(state) == state)


@dataclass(frozen=True)
class GlobalClosureCertificate:
    """A strict finite ranking certificate of global convergence to one fixed point."""

    attractor_state: str
    rank_by_state: Mapping[str, int]

    def __post_init__(self) -> None:
        if not isinstance(self.attractor_state, str) or not self.attractor_state:
            raise ValueError("attractor_state must be a non-empty string")
        if any(not isinstance(rank, int) or rank < 0 for rank in self.rank_by_state.values()):
            raise ValueError("closure ranks must be non-negative integers")


@dataclass(frozen=True)
class RecurrentCycleCertificate:
    """An exact nontrivial periodic orbit proving failure of global one-point closure."""

    cycle_states: tuple[str, ...]

    def __post_init__(self) -> None:
        if len(self.cycle_states) < 2:
            raise ValueError("a recurrent non-closure certificate needs period at least two")
        if len(set(self.cycle_states)) != len(self.cycle_states):
            raise ValueError("cycle states must be distinct before returning to the start")
        if any(not isinstance(state, str) or not state for state in self.cycle_states):
            raise ValueError("cycle states must be non-empty strings")


@dataclass(frozen=True)
class MultistabilityCertificate:
    """Two different exact fixed points proving failure of one-point global closure."""

    fixed_points: tuple[str, ...]

    def __post_init__(self) -> None:
        if len(self.fixed_points) < 2:
            raise ValueError("multistability certificate requires at least two fixed points")
        if len(set(self.fixed_points)) != len(self.fixed_points):
            raise ValueError("multistability fixed points must be distinct")


@dataclass(frozen=True)
class ClosureClassification:
    """One exact classification and its checkable certificate."""

    kind: ClosureKind
    global_closure: GlobalClosureCertificate | None = None
    recurrent_cycle: RecurrentCycleCertificate | None = None
    multistability: MultistabilityCertificate | None = None

    def __post_init__(self) -> None:
        certificates = sum(
            certificate is not None
            for certificate in (self.global_closure, self.recurrent_cycle, self.multistability)
        )
        if certificates != 1:
            raise ValueError("a closure classification must carry exactly one certificate")
        if self.kind is ClosureKind.GLOBAL_CLOSURE and self.global_closure is None:
            raise ValueError("global closure classification needs a closure certificate")
        if self.kind is ClosureKind.RECURRENT_NONCLOSURE and self.recurrent_cycle is None:
            raise ValueError("recurrent non-closure classification needs a cycle certificate")
        if self.kind is ClosureKind.MULTISTABLE_NONCLOSURE and self.multistability is None:
            raise ValueError("multistable non-closure classification needs a multistability certificate")


def _require_state_set(system: FiniteDeterministicRuleSystem, values: Iterable[str], name: str) -> tuple[str, ...]:
    result = tuple(values)
    unknown = set(result) - set(system.states)
    if unknown:
        raise ValueError(f"{name} contains states outside the system: {sorted(unknown)}")
    return result


def verify_global_closure_certificate(
    system: FiniteDeterministicRuleSystem,
    certificate: GlobalClosureCertificate,
) -> None:
    """Verify the finite Lyapunov/ranking proof of one globally attracting fixed point.

    The condition V(F(x)) < V(x) away from x* ensures that each trajectory
    strictly descends in a finite well-ordered set and hence reaches x*.  The
    certificate also requires F(x*)=x* and V(x*)=0.
    """

    if certificate.attractor_state not in system.states:
        raise ValueError("closure attractor must be a declared system state")
    if set(certificate.rank_by_state) != set(system.states):
        raise ValueError("closure rank must assign exactly one value to every state")
    attractor = certificate.attractor_state
    if system.successor(attractor) != attractor:
        raise ValueError("closure attractor is not a fixed point")
    if certificate.rank_by_state[attractor] != 0:
        raise ValueError("closure attractor must have rank zero")
    for state in system.states:
        rank = certificate.rank_by_state[state]
        successor_rank = certificate.rank_by_state[system.successor(state)]
        if state == attractor:
            continue
        if not successor_rank < rank:
            raise ValueError("closure rank must strictly decrease outside the attractor")


def verify_recurrent_cycle_certificate(
    system: FiniteDeterministicRuleSystem,
    certificate: RecurrentCycleCertificate,
) -> None:
    """Verify every edge of an exact period-p orbit, p >= 2."""

    cycle = _require_state_set(system, certificate.cycle_states, "cycle_states")
    for index, state in enumerate(cycle):
        expected = cycle[(index + 1) % len(cycle)]
        if system.successor(state) != expected:
            raise ValueError("cycle certificate edge does not match deterministic rule")


def verify_multistability_certificate(
    system: FiniteDeterministicRuleSystem,
    certificate: MultistabilityCertificate,
) -> None:
    """Verify two or more distinct fixed points."""

    fixed_points = _require_state_set(system, certificate.fixed_points, "fixed_points")
    if any(system.successor(state) != state for state in fixed_points):
        raise ValueError("multistability certificate contains a non-fixed state")


def orbit_until_repeat(
    system: FiniteDeterministicRuleSystem,
    start_state: str,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Return transient prefix and the eventual directed cycle from one start state."""

    if start_state not in system.states:
        raise ValueError("start_state must be declared")
    visited_index: dict[str, int] = {}
    orbit: list[str] = []
    current = start_state
    while current not in visited_index:
        visited_index[current] = len(orbit)
        orbit.append(current)
        current = system.successor(current)
    split = visited_index[current]
    return tuple(orbit[:split]), tuple(orbit[split:])


def all_eventual_cycles(system: FiniteDeterministicRuleSystem) -> tuple[tuple[str, ...], ...]:
    """Return unique cycles, canonically rotated by declared state order."""

    index = {state: position for position, state in enumerate(system.states)}
    found: set[tuple[str, ...]] = set()
    for start in system.states:
        _, cycle = orbit_until_repeat(system, start)
        rotations = tuple(cycle[offset:] + cycle[:offset] for offset in range(len(cycle)))
        found.add(min(rotations, key=lambda item: tuple(index[state] for state in item)))
    return tuple(sorted(found, key=lambda item: tuple(index[state] for state in item)))


def build_global_closure_certificate(
    system: FiniteDeterministicRuleSystem,
) -> GlobalClosureCertificate | None:
    """Construct a ranking certificate exactly when every state reaches one fixed point."""

    cycles = all_eventual_cycles(system)
    if len(cycles) != 1 or len(cycles[0]) != 1:
        return None
    attractor = cycles[0][0]
    ranks: dict[str, int] = {attractor: 0}
    for state in system.states:
        if state == attractor:
            continue
        current = state
        distance = 0
        seen: set[str] = set()
        while current != attractor:
            if current in seen:
                return None
            seen.add(current)
            current = system.successor(current)
            distance += 1
            if distance > len(system.states):
                return None
        ranks[state] = distance
    certificate = GlobalClosureCertificate(attractor_state=attractor, rank_by_state=ranks)
    verify_global_closure_certificate(system, certificate)
    return certificate


def find_recurrent_cycle_certificate(
    system: FiniteDeterministicRuleSystem,
) -> RecurrentCycleCertificate | None:
    """Construct the first canonical nontrivial cycle certificate, if one exists."""

    for cycle in all_eventual_cycles(system):
        if len(cycle) >= 2:
            certificate = RecurrentCycleCertificate(cycle_states=cycle)
            verify_recurrent_cycle_certificate(system, certificate)
            return certificate
    return None


def build_multistability_certificate(
    system: FiniteDeterministicRuleSystem,
) -> MultistabilityCertificate | None:
    """Construct a certificate for two or more fixed-point attractors, if present."""

    fixed = tuple(cycle[0] for cycle in all_eventual_cycles(system) if len(cycle) == 1)
    if len(fixed) < 2:
        return None
    certificate = MultistabilityCertificate(fixed_points=fixed)
    verify_multistability_certificate(system, certificate)
    return certificate


def classify_closure(system: FiniteDeterministicRuleSystem) -> ClosureClassification:
    """Classify finite exact dynamics without simulation heuristics.

    Finite total maps always have an eventual cycle.  A unique singleton cycle
    yields global closure.  Any cycle of length at least two yields recurrent
    non-closure.  The remaining case has multiple fixed-point basins.
    """

    closure = build_global_closure_certificate(system)
    if closure is not None:
        return ClosureClassification(kind=ClosureKind.GLOBAL_CLOSURE, global_closure=closure)
    recurrent = find_recurrent_cycle_certificate(system)
    if recurrent is not None:
        return ClosureClassification(kind=ClosureKind.RECURRENT_NONCLOSURE, recurrent_cycle=recurrent)
    multistability = build_multistability_certificate(system)
    if multistability is None:
        raise AssertionError("finite deterministic map should have closure, recurrence, or multistability")
    return ClosureClassification(kind=ClosureKind.MULTISTABLE_NONCLOSURE, multistability=multistability)


def exhaustive_rule_systems(state_count: int) -> Iterable[FiniteDeterministicRuleSystem]:
    """Enumerate all labelled deterministic maps on ``state_count`` states.

    There are n**n such maps.  This is intentionally for small theorem-regression
    domains only; it is not an algorithm for large ecological state spaces.
    """

    if not isinstance(state_count, int) or state_count < 1:
        raise ValueError("state_count must be a positive integer")
    states = tuple(f"s{index}" for index in range(state_count))
    for targets in product(states, repeat=state_count):
        yield FiniteDeterministicRuleSystem(
            states=states,
            successor_by_state=dict(zip(states, targets)),
            rule_id=f"all-maps-{state_count}",
        )


def exhaustive_classification_summary(max_state_count: int = 4) -> Mapping[int, Mapping[ClosureKind, int]]:
    """Exhaustively classify all labelled maps up to the requested small size."""

    if not isinstance(max_state_count, int) or not 1 <= max_state_count <= 6:
        raise ValueError("max_state_count must be an integer in [1, 6]")
    report: dict[int, Mapping[ClosureKind, int]] = {}
    for state_count in range(1, max_state_count + 1):
        counts = {kind: 0 for kind in ClosureKind}
        for system in exhaustive_rule_systems(state_count):
            classification = classify_closure(system)
            counts[classification.kind] += 1
        report[state_count] = counts
    return report
