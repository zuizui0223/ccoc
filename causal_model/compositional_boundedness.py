"""Compositional boundedness criteria for open causal interfaces.

This module joins two existing active results without asserting a false universal
dichotomy.

Positive criterion.  A chain of growing finite systems has uniformly bounded
exact interface memory when every stage factors through the *same finite summary
alphabet* and each stage map preserves output, legal actions, and successor
summary.  The stage domains may grow; the codomain does not.

Negative criterion.  A chain has cumulative interface growth when each newly
added exterior factor is jointly realizable with the previous factors and has a
legal future decoder word.  The addressable-product injection then gives a
cumulative lower bound.

The alternatives are conditional structural criteria.  A family satisfying
neither premise is deliberately left unresolved by this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import log2, prod
from typing import Iterable

from .dynamic_boundary_blankets import FiniteControlledOutputSystem
from .extension_compression_noncommutation import (
    AddressableProductLowerBoundCertificate,
    RelayTreeSharpnessCertificate,
    certify_addressable_product_lower_bound,
    certify_relay_tree_sharpness,
)
from .grammar_aware_blankets import GrammarAwareDynamicInterfaceCertificate
from .delayed_addressability import FinitePrefixGrammar, GrammarAwareControlledSystem


def _positive(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _canonical_alphabet(summary_alphabet: Iterable[int]) -> tuple[int, ...]:
    try:
        labels = tuple(summary_alphabet)
    except TypeError as error:
        raise ValueError("summary_alphabet must be iterable") from error
    if not labels or labels != tuple(range(len(labels))):
        raise ValueError("summary_alphabet must be the canonical tuple (0,...,B-1)")
    return labels


def _canonical_cards(exterior_cardinalities: Iterable[int]) -> tuple[int, ...]:
    try:
        cards = tuple(exterior_cardinalities)
    except TypeError as error:
        raise ValueError("exterior_cardinalities must be iterable") from error
    if not cards:
        raise ValueError("at least one exterior module is required")
    for index, cardinality in enumerate(cards):
        _positive(cardinality, f"exterior_cardinalities[{index}]")
    return cards


@dataclass(frozen=True)
class UniformFactorizationStage:
    """One finite stage factoring through a fixed shared summary alphabet."""

    constrained_system: GrammarAwareControlledSystem
    summary_labels: tuple[int, ...]

    @property
    def interface(self) -> GrammarAwareDynamicInterfaceCertificate:
        return GrammarAwareDynamicInterfaceCertificate(self.constrained_system, self.summary_labels)

    @property
    def used_summary_labels(self) -> tuple[int, ...]:
        return tuple(sorted(set(self.summary_labels)))

    def verify(self, summary_alphabet: tuple[int, ...]) -> bool:
        try:
            if any(label not in summary_alphabet for label in self.summary_labels):
                return False
            return self.interface.verify()
        except (TypeError, ValueError):
            return False


@dataclass(frozen=True)
class UniformDynamicBlanketChainCertificate:
    """A common finite codomain bounds exact quotients throughout a stage chain.

    The maps may have different finite domains because composition may add
    physical modules.  They are restrictions of one uniform summary *type*: all
    values lie in one fixed finite alphabet Q and each stage is a dynamic
    grammar-aware interface.  Thus every canonical quotient is no larger than Q.
    """

    summary_alphabet: tuple[int, ...]
    stages: tuple[UniformFactorizationStage, ...]
    canonical_block_counts: tuple[int, ...]

    @property
    def summary_state_bound(self) -> int:
        return len(self.summary_alphabet)

    @property
    def summary_bits_bound(self) -> float:
        return log2(self.summary_state_bound)

    @property
    def maximum_canonical_bits(self) -> float:
        return log2(max(self.canonical_block_counts))

    def verify(self) -> bool:
        try:
            alphabet = _canonical_alphabet(self.summary_alphabet)
            if alphabet != self.summary_alphabet or not self.stages:
                return False
            if len(self.canonical_block_counts) != len(self.stages):
                return False
            for stage, count in zip(self.stages, self.canonical_block_counts):
                if not stage.verify(alphabet):
                    return False
                if count != stage.interface.summary_block_count:
                    return False
                if count > self.summary_state_bound:
                    return False
            return self.maximum_canonical_bits <= self.summary_bits_bound + 1e-12
        except (TypeError, ValueError):
            return False


def certify_uniform_dynamic_blanket_chain(
    summary_alphabet: Iterable[int],
    stages: Iterable[UniformFactorizationStage],
) -> UniformDynamicBlanketChainCertificate:
    alphabet = _canonical_alphabet(summary_alphabet)
    try:
        normalized_stages = tuple(stages)
    except TypeError as error:
        raise ValueError("stages must be iterable") from error
    if not normalized_stages:
        raise ValueError("a uniform factorization chain needs at least one stage")
    certificate = UniformDynamicBlanketChainCertificate(
        summary_alphabet=alphabet,
        stages=normalized_stages,
        canonical_block_counts=tuple(stage.interface.summary_block_count for stage in normalized_stages),
    )
    if not certificate.verify():
        raise ValueError("stages do not form a uniform grammar-aware dynamic blanket chain")
    return certificate


def inert_attachment_stage(module_count: int, action_alphabet: tuple[str, ...]) -> UniformFactorizationStage:
    """Growing physical composition with no new response distinction.

    There are ``2**module_count`` physical configurations, but every action is
    inert and every output agrees.  The one-label summary is exact for the fixed
    full grammar.  This is not an ecological claim; it is the positive witness
    that adding modules alone does not force interface growth.
    """
    _positive(module_count, "module_count")
    if not isinstance(action_alphabet, tuple) or not action_alphabet:
        raise ValueError("action_alphabet must be a nonempty tuple")
    state_count = 2 ** module_count
    system = FiniteControlledOutputSystem(
        actions=action_alphabet,
        transition_table=tuple((state,) * len(action_alphabet) for state in range(state_count)),
        outputs=("inert-window",) * state_count,
    )
    grammar = FinitePrefixGrammar(
        actions=action_alphabet,
        transition_table=(tuple(0 for _ in action_alphabet),),
    )
    constrained = GrammarAwareControlledSystem(system=system, grammar=grammar)
    return UniformFactorizationStage(
        constrained_system=constrained,
        summary_labels=(0,) * constrained.product_state_count,
    )


def certify_inert_attachment_boundedness(max_module_count: int) -> UniformDynamicBlanketChainCertificate:
    """Positive witness: arbitrarily many inert attachments share one blanket type."""
    _positive(max_module_count, "max_module_count")
    actions = ("observe", "connect")
    return certify_uniform_dynamic_blanket_chain(
        (0,),
        tuple(inert_attachment_stage(module_count, actions) for module_count in range(1, max_module_count + 1)),
    )


@dataclass(frozen=True)
class CumulativeAddressabilityChainCertificate:
    """Prefix chain of jointly realizable independently decoded exterior factors."""

    inside_cardinality: int
    exterior_cardinalities: tuple[int, ...]
    prefix_lower_bounds: tuple[AddressableProductLowerBoundCertificate, ...]

    @property
    def stage_count(self) -> int:
        return len(self.exterior_cardinalities)

    @property
    def open_state_lower_bounds(self) -> tuple[int, ...]:
        return tuple(certificate.open_state_lower_bound for certificate in self.prefix_lower_bounds)

    @property
    def open_bits_lower_bounds(self) -> tuple[float, ...]:
        return tuple(certificate.open_bits_lower_bound for certificate in self.prefix_lower_bounds)

    @property
    def incremental_bits(self) -> tuple[float, ...]:
        return tuple(log2(cardinality) for cardinality in self.exterior_cardinalities)

    def verify(self) -> bool:
        try:
            _positive(self.inside_cardinality, "inside_cardinality")
            cards = _canonical_cards(self.exterior_cardinalities)
            if cards != self.exterior_cardinalities:
                return False
            if len(self.prefix_lower_bounds) != len(cards):
                return False
            for stage_index, certificate in enumerate(self.prefix_lower_bounds, start=1):
                if not certificate.verify():
                    return False
                if certificate.inside_cardinality != self.inside_cardinality:
                    return False
                if certificate.exterior_cardinalities != cards[:stage_index]:
                    return False
            expected = tuple(
                self.inside_cardinality * prod(cards[:stage_index])
                for stage_index in range(1, len(cards) + 1)
            )
            return self.open_state_lower_bounds == expected
        except (TypeError, ValueError):
            return False


def certify_cumulative_addressability_chain(
    inside_cardinality: int,
    exterior_cardinalities: Iterable[int],
) -> CumulativeAddressabilityChainCertificate:
    _positive(inside_cardinality, "inside_cardinality")
    cards = _canonical_cards(exterior_cardinalities)
    certificate = CumulativeAddressabilityChainCertificate(
        inside_cardinality=inside_cardinality,
        exterior_cardinalities=cards,
        prefix_lower_bounds=tuple(
            certify_addressable_product_lower_bound(inside_cardinality, cards[:stage_index])
            for stage_index in range(1, len(cards) + 1)
        ),
    )
    if not certificate.verify():
        raise AssertionError("cumulative addressability chain certificate did not verify")
    return certificate


@dataclass(frozen=True)
class BinaryRelayGrowthCertificate:
    """Sharp realization of cumulative binary growth by the relay-tree family."""

    maximum_module_count: int
    addressability_chain: CumulativeAddressabilityChainCertificate
    relay_stages: tuple[RelayTreeSharpnessCertificate, ...]

    def verify(self) -> bool:
        try:
            _positive(self.maximum_module_count, "maximum_module_count")
            if not self.addressability_chain.verify():
                return False
            if self.addressability_chain.inside_cardinality != 2:
                return False
            if self.addressability_chain.exterior_cardinalities != (2,) * self.maximum_module_count:
                return False
            if len(self.relay_stages) != self.maximum_module_count:
                return False
            for module_count, relay in enumerate(self.relay_stages, start=1):
                if not relay.verify() or relay.module_count != module_count:
                    return False
                if relay.open_bits != self.addressability_chain.open_bits_lower_bounds[module_count - 1]:
                    return False
            return True
        except (TypeError, ValueError):
            return False


def certify_binary_relay_growth(maximum_module_count: int) -> BinaryRelayGrowthCertificate:
    _positive(maximum_module_count, "maximum_module_count")
    chain = certify_cumulative_addressability_chain(2, (2,) * maximum_module_count)
    certificate = BinaryRelayGrowthCertificate(
        maximum_module_count=maximum_module_count,
        addressability_chain=chain,
        relay_stages=tuple(certify_relay_tree_sharpness(module_count) for module_count in range(1, maximum_module_count + 1)),
    )
    if not certificate.verify():
        raise AssertionError("binary relay growth certificate did not verify")
    return certificate
