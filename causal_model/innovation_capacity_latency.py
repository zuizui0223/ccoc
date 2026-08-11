"""Absolute innovation capacity and local-query latency bounds for CCOC.

This module deliberately separates three mathematical layers.

1. ``InnovationCapacityCertificate`` is completely general for one finite
   comparison domain: an open quotient refining a closed-union quotient can add
   at most enough blocks to make the domain discrete.
2. ``PrefixFreeAddressLatencyCertificate`` is a coding statement: a prefix-free
   address family over a fixed alphabet needs worst-case length at least the
   ceiling logarithm of the number of addressed terminals.
3. ``RelayLocalLatencyCertificate`` applies only to the explicit CCOC addressed
   relay architecture.  Selector motion is at most one parent-child edge per
   address symbol; ``fire`` injects one pulse at the selected leaf; afterwards
   the pulse moves at most one child-parent edge per ``tick`` toward the focal
   output.  Under that contract, the current balanced power-of-two relay attains
   the architecture-level latency lower bound exactly.

The capacity inequality, Kraft/tree counting, and finite-speed graph propagation
are mathematical substrate rather than novelty claims.  Their role is to close
the sharpness statement of the existing one-action innovation construction.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import log2
from typing import Iterable

from .constant_alphabet_relay import (
    ADDRESS_ONE,
    ADDRESS_ZERO,
    address_bits_for_port,
    addressed_probe_word,
)
from .relay_tree_compilation import ROOT, RelayTreeTopology
from .single_action_innovation import SingleActionInnovationCertificate, certify_single_action_innovation

AddressSymbol = str
AddressWord = tuple[AddressSymbol, ...]


def _positive_integer(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _ceil_log_base(count: int, base: int) -> int:
    _positive_integer(count, "count")
    if not isinstance(base, int) or isinstance(base, bool) or base < 2:
        raise ValueError("base must be an integer of at least two")
    depth = 0
    capacity = 1
    while capacity < count:
        capacity *= base
        depth += 1
    return depth


def _normalize_alphabet(alphabet: Iterable[AddressSymbol]) -> tuple[AddressSymbol, ...]:
    try:
        normalized = tuple(alphabet)
    except TypeError as error:
        raise ValueError("alphabet must be iterable") from error
    if len(normalized) < 2:
        raise ValueError("address alphabet must contain at least two symbols")
    if any(not isinstance(symbol, str) or not symbol for symbol in normalized):
        raise ValueError("address symbols must be nonempty strings")
    if len(set(normalized)) != len(normalized):
        raise ValueError("address alphabet symbols must be unique")
    return normalized


def _normalize_addresses(
    addresses: Iterable[Iterable[AddressSymbol]],
    alphabet: tuple[AddressSymbol, ...],
) -> tuple[AddressWord, ...]:
    try:
        normalized = tuple(tuple(word) for word in addresses)
    except TypeError as error:
        raise ValueError("addresses must be an iterable of words") from error
    if not normalized:
        raise ValueError("at least one address is required")
    if len(set(normalized)) != len(normalized):
        raise ValueError("addresses must be unique")
    allowed = set(alphabet)
    for word in normalized:
        if any(symbol not in allowed for symbol in word):
            raise ValueError("address contains a symbol outside the declared alphabet")
    return normalized


def _is_prefix(left: AddressWord, right: AddressWord) -> bool:
    return len(left) <= len(right) and right[: len(left)] == left


@dataclass(frozen=True)
class InnovationCapacityCertificate:
    """Absolute finite-domain capacity for open-only interface innovation."""

    domain_state_count: int
    closed_union_block_count: int
    open_block_count: int

    @property
    def actual_innovation_bits(self) -> float:
        return log2(self.open_block_count / self.closed_union_block_count)

    @property
    def maximum_innovation_bits(self) -> float:
        return log2(self.domain_state_count / self.closed_union_block_count)

    @property
    def unused_innovation_capacity_bits(self) -> float:
        return log2(self.domain_state_count / self.open_block_count)

    @property
    def saturates_absolute_capacity(self) -> bool:
        return self.open_block_count == self.domain_state_count

    def verify(self) -> bool:
        try:
            _positive_integer(self.domain_state_count, "domain_state_count")
            _positive_integer(self.closed_union_block_count, "closed_union_block_count")
            _positive_integer(self.open_block_count, "open_block_count")
            if self.closed_union_block_count > self.open_block_count:
                return False
            if self.open_block_count > self.domain_state_count:
                return False
            if self.actual_innovation_bits < -1e-12:
                return False
            if self.actual_innovation_bits > self.maximum_innovation_bits + 1e-12:
                return False
            if self.unused_innovation_capacity_bits < -1e-12:
                return False
            if abs(
                self.maximum_innovation_bits
                - self.actual_innovation_bits
                - self.unused_innovation_capacity_bits
            ) > 1e-12:
                return False
            if self.saturates_absolute_capacity != (
                abs(self.unused_innovation_capacity_bits) <= 1e-12
            ):
                return False
            return True
        except (TypeError, ValueError):
            return False


def certify_innovation_capacity(
    domain_state_count: int,
    closed_union_block_count: int,
    open_block_count: int,
) -> InnovationCapacityCertificate:
    """Certify the absolute finite-domain innovation upper bound."""
    certificate = InnovationCapacityCertificate(
        domain_state_count=domain_state_count,
        closed_union_block_count=closed_union_block_count,
        open_block_count=open_block_count,
    )
    if not certificate.verify():
        raise ValueError("declared innovation block counts do not form a valid refinement")
    return certificate


@dataclass(frozen=True)
class PrefixFreeAddressLatencyCertificate:
    """Kraft/tree-counting lower bound for one finite terminal address family."""

    alphabet: tuple[AddressSymbol, ...]
    addresses: tuple[AddressWord, ...]

    @property
    def alphabet_size(self) -> int:
        return len(self.alphabet)

    @property
    def terminal_count(self) -> int:
        return len(self.addresses)

    @property
    def actual_worst_case_address_length(self) -> int:
        return max(len(word) for word in self.addresses)

    @property
    def minimum_worst_case_address_length(self) -> int:
        return _ceil_log_base(self.terminal_count, self.alphabet_size)

    @property
    def latency_slack_steps(self) -> int:
        return self.actual_worst_case_address_length - self.minimum_worst_case_address_length

    @property
    def is_prefix_free(self) -> bool:
        for left, right in combinations(self.addresses, 2):
            if _is_prefix(left, right) or _is_prefix(right, left):
                return False
        return True

    @property
    def kraft_numerator(self) -> int:
        """Integer numerator of the Kraft sum at common max-length denominator."""
        maximum = self.actual_worst_case_address_length
        base = self.alphabet_size
        return sum(base ** (maximum - len(word)) for word in self.addresses)

    @property
    def kraft_denominator(self) -> int:
        return self.alphabet_size ** self.actual_worst_case_address_length

    def verify(self) -> bool:
        try:
            alphabet = _normalize_alphabet(self.alphabet)
            if alphabet != self.alphabet:
                return False
            addresses = _normalize_addresses(self.addresses, alphabet)
            if addresses != self.addresses:
                return False
            if not self.is_prefix_free:
                return False
            if self.kraft_numerator > self.kraft_denominator:
                return False
            if self.actual_worst_case_address_length < self.minimum_worst_case_address_length:
                return False
            if self.latency_slack_steps < 0:
                return False
            return True
        except (TypeError, ValueError):
            return False


def certify_prefix_free_address_latency(
    alphabet: Iterable[AddressSymbol],
    addresses: Iterable[Iterable[AddressSymbol]],
) -> PrefixFreeAddressLatencyCertificate:
    """Certify one prefix-free finite address family and its worst-case lower bound."""
    normalized_alphabet = _normalize_alphabet(alphabet)
    normalized_addresses = _normalize_addresses(addresses, normalized_alphabet)
    certificate = PrefixFreeAddressLatencyCertificate(
        alphabet=normalized_alphabet,
        addresses=normalized_addresses,
    )
    if not certificate.verify():
        raise ValueError("declared address family is not a valid prefix-free code")
    return certificate


@dataclass(frozen=True)
class RelayLocalLatencyCertificate:
    """Exact latency accounting for the current one-edge-per-step relay contract."""

    module_count: int
    topology: RelayTreeTopology
    addresses: tuple[AddressWord, ...]
    probe_words: tuple[tuple[str, ...], ...]

    @property
    def address_certificate(self) -> PrefixFreeAddressLatencyCertificate:
        return certify_prefix_free_address_latency(
            (ADDRESS_ZERO, ADDRESS_ONE),
            self.addresses,
        )

    @property
    def selector_depths(self) -> tuple[int, ...]:
        return tuple(len(address) for address in self.addresses)

    @property
    def response_distances(self) -> tuple[int, ...]:
        return tuple(self.topology.distance_to_root(leaf) for leaf in self.topology.leaves)

    @property
    def per_port_local_lower_bounds(self) -> tuple[int, ...]:
        # address steps + one fire step + one edge per response tick to focal root
        return tuple(
            address_depth + 1 + response_distance
            for address_depth, response_distance in zip(
                self.selector_depths,
                self.response_distances,
            )
        )

    @property
    def actual_probe_lengths(self) -> tuple[int, ...]:
        return tuple(len(word) for word in self.probe_words)

    @property
    def worst_case_local_lower_bound(self) -> int:
        return max(self.per_port_local_lower_bounds)

    @property
    def actual_worst_case_probe_length(self) -> int:
        return max(self.actual_probe_lengths)

    @property
    def architecture_asymptotic_lower_bound(self) -> int:
        """Binary terminal selection plus same-tree return path lower bound."""
        depth = self.address_certificate.minimum_worst_case_address_length
        return 2 * depth + 2

    @property
    def saturates_architecture_latency_bound(self) -> bool:
        return self.actual_worst_case_probe_length == self.architecture_asymptotic_lower_bound

    def verify(self) -> bool:
        try:
            _positive_integer(self.module_count, "module_count")
            if self.module_count < 2 or self.module_count & (self.module_count - 1):
                return False
            if self.topology != RelayTreeTopology.balanced(self.module_count):
                return False
            if not self.topology.verify():
                return False
            if len(self.addresses) != self.module_count or len(self.probe_words) != self.module_count:
                return False
            if not self.address_certificate.verify():
                return False

            expected_addresses = tuple(
                address_bits_for_port(self.module_count, port)
                for port in range(self.module_count)
            )
            expected_probes = tuple(
                addressed_probe_word(self.module_count, port)
                for port in range(self.module_count)
            )
            if self.addresses != expected_addresses:
                return False
            if self.probe_words != expected_probes:
                return False

            # In the balanced relay body the selector depth equals the leaf depth
            # below body_root; the focal ROOT is one extra edge above body_root.
            for address, leaf, response_distance in zip(
                self.addresses,
                self.topology.leaves,
                self.response_distances,
            ):
                if response_distance != len(address) + 1:
                    return False
                if self.topology.parent_by_node[self.topology.body_root] != ROOT:
                    return False
                if self.topology.distance_to_root(leaf) != response_distance:
                    return False

            if any(
                actual < lower
                for actual, lower in zip(
                    self.actual_probe_lengths,
                    self.per_port_local_lower_bounds,
                )
            ):
                return False
            if self.actual_worst_case_probe_length < self.architecture_asymptotic_lower_bound:
                return False
            if not self.saturates_architecture_latency_bound:
                return False
            return True
        except (AssertionError, KeyError, TypeError, ValueError):
            return False


def certify_relay_local_latency(module_count: int) -> RelayLocalLatencyCertificate:
    """Certify exact query-latency optimality of the balanced addressed relay."""
    if not isinstance(module_count, int) or isinstance(module_count, bool) or module_count < 2:
        raise ValueError("module_count must be a power of two of at least two")
    if module_count & (module_count - 1):
        raise ValueError("module_count must be a power of two of at least two")
    topology = RelayTreeTopology.balanced(module_count)
    certificate = RelayLocalLatencyCertificate(
        module_count=module_count,
        topology=topology,
        addresses=tuple(address_bits_for_port(module_count, port) for port in range(module_count)),
        probe_words=tuple(addressed_probe_word(module_count, port) for port in range(module_count)),
    )
    if not certificate.verify():
        raise AssertionError("relay local-latency certificate did not verify")
    return certificate


@dataclass(frozen=True)
class SingleActionSharpnessClosureCertificate:
    """The current single-action family saturates both memory and latency bounds."""

    innovation: SingleActionInnovationCertificate
    capacity: InnovationCapacityCertificate
    latency: RelayLocalLatencyCertificate

    @property
    def module_count(self) -> int:
        return self.innovation.module_count

    def verify(self) -> bool:
        try:
            if not self.innovation.verify():
                return False
            if not self.capacity.verify() or not self.latency.verify():
                return False
            if self.latency.module_count != self.module_count:
                return False
            if self.capacity.domain_state_count != len(self.innovation.states):
                return False
            if self.capacity.closed_union_block_count != self.innovation.closed_block_count:
                return False
            if self.capacity.open_block_count != self.innovation.open_block_count:
                return False
            if not self.capacity.saturates_absolute_capacity:
                return False
            if abs(self.capacity.actual_innovation_bits - self.module_count) > 1e-12:
                return False
            if abs(self.innovation.open_only_innovation_bits - self.capacity.actual_innovation_bits) > 1e-12:
                return False
            if not self.latency.saturates_architecture_latency_bound:
                return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_single_action_sharpness_closure(
    module_count: int,
) -> SingleActionSharpnessClosureCertificate:
    """Certify simultaneous absolute-memory and local-latency sharpness."""
    innovation = certify_single_action_innovation(module_count)
    capacity = certify_innovation_capacity(
        domain_state_count=len(innovation.states),
        closed_union_block_count=innovation.closed_block_count,
        open_block_count=innovation.open_block_count,
    )
    latency = certify_relay_local_latency(module_count)
    certificate = SingleActionSharpnessClosureCertificate(
        innovation=innovation,
        capacity=capacity,
        latency=latency,
    )
    if not certificate.verify():
        raise AssertionError("single-action sharpness closure certificate did not verify")
    return certificate


__all__ = [
    "AddressSymbol",
    "AddressWord",
    "InnovationCapacityCertificate",
    "certify_innovation_capacity",
    "PrefixFreeAddressLatencyCertificate",
    "certify_prefix_free_address_latency",
    "RelayLocalLatencyCertificate",
    "certify_relay_local_latency",
    "SingleActionSharpnessClosureCertificate",
    "certify_single_action_sharpness_closure",
]
