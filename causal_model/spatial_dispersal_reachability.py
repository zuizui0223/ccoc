"""Exact spatial reachability blankets for monotone directed dispersal.

A finite directed patch graph has one focal target.  A microstate is an arbitrary
occupied-patch subset.  One controlled ``spread`` action adds every outgoing
neighbor of every occupied patch.  The focal response is whether the target is
occupied.

For unlimited spread futures, the exact response of an occupancy state depends
only on its minimum directed distance to the focal target (with one extra
unreachable class).  For a prefix grammar allowing at most H future spread
steps, the grammar-adaptive capped distance is an exact dynamic interface.  The
initial exact quotient has min(D,H)+2 classes, where D is the maximum finite
node-to-target distance.  Therefore fixed-H exact interfaces are uniformly
bounded across arbitrarily large graphs, while unlimited exact interfaces have
D+2 classes and can grow without bound as reachability depth grows.

Shortest paths and deterministic wavefront propagation are classical substrate.
The CCOC role is the future-grammar interpretation: causal memory is controlled by
how deeply the declared future can probe spatial reachability, not by graph size
or cut width alone.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Iterable

from .action_grammar_closure import canonical_action_quotient_labels
from .dynamic_boundary_blankets import FiniteControlledOutputSystem
from .grammar_aware_blankets import (
    GrammarAwareDynamicInterfaceCertificate,
    certify_grammar_aware_canonical_interface,
)
from .shared_grammar import FinitePrefixGrammar, GrammarAwareControlledSystem

Edge = tuple[int, int]
SPREAD = "spread"


def _positive_integer(value: int, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _nonnegative_integer(value: int, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")
    return value


def _normalize_edges(node_count: int, edges: Iterable[tuple[int, int]]) -> tuple[Edge, ...]:
    normalized = tuple(tuple(edge) for edge in edges)
    if any(len(edge) != 2 for edge in normalized):
        raise ValueError("every directed edge must contain (source,target)")
    result: list[Edge] = []
    for source, target in normalized:
        if (
            not isinstance(source, int)
            or isinstance(source, bool)
            or not isinstance(target, int)
            or isinstance(target, bool)
            or not 0 <= source < node_count
            or not 0 <= target < node_count
        ):
            raise ValueError("edge endpoint is outside the finite graph")
        result.append((source, target))
    if len(set(result)) != len(result):
        raise ValueError("directed edges must be unique")
    return tuple(result)


def _same_partition(left: tuple[object, ...], right: tuple[object, ...]) -> bool:
    if len(left) != len(right):
        return False
    for i in range(len(left)):
        for j in range(i + 1, len(left)):
            if (left[i] == left[j]) != (right[i] == right[j]):
                return False
    return True


@dataclass(frozen=True)
class SpatialDispersalReachabilityCertificate:
    """One graph and one finite spread-horizon grammar."""

    node_count: int
    focal_target: int
    edges: tuple[Edge, ...]
    spread_horizon: int

    @property
    def occupancy_state_count(self) -> int:
        return 1 << self.node_count

    @property
    def occupancy_states(self) -> tuple[int, ...]:
        return tuple(range(self.occupancy_state_count))

    @property
    def adjacency(self) -> tuple[tuple[int, ...], ...]:
        rows: list[list[int]] = [[] for _ in range(self.node_count)]
        for source, target in self.edges:
            rows[source].append(target)
        return tuple(tuple(sorted(row)) for row in rows)

    @property
    def reverse_adjacency(self) -> tuple[tuple[int, ...], ...]:
        rows: list[list[int]] = [[] for _ in range(self.node_count)]
        for source, target in self.edges:
            rows[target].append(source)
        return tuple(tuple(sorted(row)) for row in rows)

    @property
    def node_distances_to_focal(self) -> tuple[int | None, ...]:
        distances: list[int | None] = [None] * self.node_count
        distances[self.focal_target] = 0
        queue: deque[int] = deque([self.focal_target])
        reverse = self.reverse_adjacency
        while queue:
            current = queue.popleft()
            current_distance = distances[current]
            if current_distance is None:  # pragma: no cover - queue invariant
                raise AssertionError("distance queue contained an unreachable node")
            for predecessor in reverse[current]:
                if distances[predecessor] is None:
                    distances[predecessor] = current_distance + 1
                    queue.append(predecessor)
        return tuple(distances)

    @property
    def maximum_finite_distance(self) -> int:
        finite = [distance for distance in self.node_distances_to_focal if distance is not None]
        return max(finite)

    def output(self, occupancy_mask: int) -> int:
        if not 0 <= occupancy_mask < self.occupancy_state_count:
            raise ValueError("occupancy mask is outside the finite graph state space")
        return int(bool(occupancy_mask & (1 << self.focal_target)))

    def spread(self, occupancy_mask: int) -> int:
        if not 0 <= occupancy_mask < self.occupancy_state_count:
            raise ValueError("occupancy mask is outside the finite graph state space")
        result = occupancy_mask
        adjacency = self.adjacency
        for node in range(self.node_count):
            if occupancy_mask & (1 << node):
                for target in adjacency[node]:
                    result |= 1 << target
        return result

    def occupancy_distance_to_focal(self, occupancy_mask: int) -> int | None:
        if not 0 <= occupancy_mask < self.occupancy_state_count:
            raise ValueError("occupancy mask is outside the finite graph state space")
        distances = self.node_distances_to_focal
        finite = [
            distances[node]
            for node in range(self.node_count)
            if occupancy_mask & (1 << node) and distances[node] is not None
        ]
        return min(finite) if finite else None

    def capped_distance(self, occupancy_mask: int, grammar_state: int) -> int:
        if not 0 <= grammar_state <= self.spread_horizon:
            raise ValueError("grammar_state is outside the spread-horizon grammar")
        remaining = self.spread_horizon - grammar_state
        distance = self.occupancy_distance_to_focal(occupancy_mask)
        return remaining + 1 if distance is None else min(distance, remaining + 1)

    @property
    def system(self) -> FiniteControlledOutputSystem:
        return FiniteControlledOutputSystem(
            actions=(SPREAD,),
            transition_table=tuple((self.spread(state),) for state in self.occupancy_states),
            outputs=tuple(self.output(state) for state in self.occupancy_states),
        )

    @property
    def grammar(self) -> FinitePrefixGrammar:
        rows = tuple(
            (state + 1,) if state < self.spread_horizon else (None,)
            for state in range(self.spread_horizon + 1)
        )
        return FinitePrefixGrammar(actions=(SPREAD,), transition_table=rows)

    @property
    def constrained_system(self) -> GrammarAwareControlledSystem:
        return GrammarAwareControlledSystem(self.system, self.grammar)

    @property
    def grammar_adaptive_labels(self) -> tuple[tuple[int, int], ...]:
        return tuple(
            (grammar_state, self.capped_distance(occupancy_mask, grammar_state))
            for occupancy_mask, grammar_state in self.constrained_system.product_states
        )

    @property
    def interface(self) -> GrammarAwareDynamicInterfaceCertificate:
        return GrammarAwareDynamicInterfaceCertificate(
            self.constrained_system,
            self.grammar_adaptive_labels,
        )

    @property
    def initial_capped_labels(self) -> tuple[int, ...]:
        return tuple(self.capped_distance(state, 0) for state in self.occupancy_states)

    @property
    def canonical_initial_labels(self) -> tuple[int, ...]:
        canonical = certify_grammar_aware_canonical_interface(self.constrained_system)
        return tuple(
            canonical.canonical_labels[
                self.constrained_system.product_index((state, self.grammar.initial_state))
            ]
            for state in self.occupancy_states
        )

    @property
    def initial_exact_block_count(self) -> int:
        return len(set(self.canonical_initial_labels))

    @property
    def expected_initial_block_count(self) -> int:
        return min(self.maximum_finite_distance, self.spread_horizon) + 2

    @property
    def unlimited_labels(self) -> tuple[int, ...]:
        return canonical_action_quotient_labels(self.system, (SPREAD,))

    @property
    def unlimited_exact_block_count(self) -> int:
        return len(set(self.unlimited_labels))

    @property
    def expected_unlimited_block_count(self) -> int:
        return self.maximum_finite_distance + 2

    def macro_successor(self, grammar_state: int, capped_distance: int) -> tuple[int, int]:
        if not 0 <= grammar_state < self.spread_horizon:
            raise ValueError("no spread successor exists at the terminal grammar state")
        remaining = self.spread_horizon - grammar_state
        if not 0 <= capped_distance <= remaining + 1:
            raise ValueError("capped distance is outside the grammar-adaptive macro domain")
        return grammar_state + 1, max(0, capped_distance - 1)

    def verify(self) -> bool:
        try:
            _positive_integer(self.node_count, "node_count")
            _nonnegative_integer(self.spread_horizon, "spread_horizon")
            if (
                not isinstance(self.focal_target, int)
                or isinstance(self.focal_target, bool)
                or not 0 <= self.focal_target < self.node_count
            ):
                return False
            if _normalize_edges(self.node_count, self.edges) != self.edges:
                return False
            if self.node_distances_to_focal[self.focal_target] != 0:
                return False

            # Distance decreases exactly one step under monotone wave spread when
            # the focal target is finitely reachable; unreachable states stay
            # unreachable unless another occupied component is already reachable.
            for state in self.occupancy_states:
                distance = self.occupancy_distance_to_focal(state)
                next_distance = self.occupancy_distance_to_focal(self.spread(state))
                if distance is None:
                    if next_distance is not None:
                        return False
                elif distance == 0:
                    if next_distance != 0:
                        return False
                elif next_distance != distance - 1:
                    return False

            if not self.interface.verify():
                return False
            if not _same_partition(self.initial_capped_labels, self.canonical_initial_labels):
                return False
            if self.initial_exact_block_count != self.expected_initial_block_count:
                return False
            if self.unlimited_exact_block_count != self.expected_unlimited_block_count:
                return False

            for state in self.occupancy_states:
                for grammar_state in range(self.spread_horizon):
                    label = (grammar_state, self.capped_distance(state, grammar_state))
                    successor_state = self.spread(state)
                    expected = self.macro_successor(*label)
                    actual = (
                        grammar_state + 1,
                        self.capped_distance(successor_state, grammar_state + 1),
                    )
                    if actual != expected:
                        return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_spatial_dispersal_reachability(
    node_count: int,
    focal_target: int,
    edges: Iterable[tuple[int, int]],
    spread_horizon: int,
) -> SpatialDispersalReachabilityCertificate:
    certificate = SpatialDispersalReachabilityCertificate(
        node_count=_positive_integer(node_count, "node_count"),
        focal_target=focal_target,
        edges=_normalize_edges(node_count, edges),
        spread_horizon=_nonnegative_integer(spread_horizon, "spread_horizon"),
    )
    if not certificate.verify():
        raise ValueError("spatial dispersal reachability certificate did not verify")
    return certificate


def path_to_focal_graph(maximum_distance: int) -> tuple[int, int, tuple[Edge, ...]]:
    """Return target 0 and a directed chain D -> ... -> 1 -> 0."""
    distance = _nonnegative_integer(maximum_distance, "maximum_distance")
    node_count = distance + 1
    edges = tuple((node, node - 1) for node in range(1, node_count))
    return node_count, 0, edges


def certify_path_reachability(
    maximum_distance: int,
    spread_horizon: int,
) -> SpatialDispersalReachabilityCertificate:
    node_count, focal_target, edges = path_to_focal_graph(maximum_distance)
    return certify_spatial_dispersal_reachability(
        node_count,
        focal_target,
        edges,
        spread_horizon,
    )


@dataclass(frozen=True)
class SpatialReachabilityFamilyCertificate:
    """Changing graphs sharing one fixed finite future-horizon memory bound."""

    stages: tuple[SpatialDispersalReachabilityCertificate, ...]

    @property
    def spread_horizon(self) -> int:
        return self.stages[0].spread_horizon

    @property
    def uniform_initial_block_bound(self) -> int:
        return self.spread_horizon + 2

    @property
    def initial_block_counts(self) -> tuple[int, ...]:
        return tuple(stage.initial_exact_block_count for stage in self.stages)

    @property
    def unlimited_block_counts(self) -> tuple[int, ...]:
        return tuple(stage.unlimited_exact_block_count for stage in self.stages)

    def verify(self) -> bool:
        try:
            if not self.stages or any(not stage.verify() for stage in self.stages):
                return False
            if any(stage.spread_horizon != self.spread_horizon for stage in self.stages):
                return False
            if any(count > self.uniform_initial_block_bound for count in self.initial_block_counts):
                return False
            return True
        except (TypeError, ValueError):
            return False


def certify_spatial_reachability_family(
    graph_specs: Iterable[tuple[int, int, Iterable[tuple[int, int]]]],
    spread_horizon: int,
) -> SpatialReachabilityFamilyCertificate:
    specs = tuple(graph_specs)
    if not specs:
        raise ValueError("at least one graph is required")
    stages = tuple(
        certify_spatial_dispersal_reachability(
            node_count,
            focal_target,
            edges,
            spread_horizon,
        )
        for node_count, focal_target, edges in specs
    )
    certificate = SpatialReachabilityFamilyCertificate(stages)
    if not certificate.verify():
        raise AssertionError("spatial reachability family did not verify")
    return certificate


__all__ = [
    "Edge",
    "SPREAD",
    "SpatialDispersalReachabilityCertificate",
    "SpatialReachabilityFamilyCertificate",
    "certify_spatial_dispersal_reachability",
    "path_to_focal_graph",
    "certify_path_reachability",
    "certify_spatial_reachability_family",
]
