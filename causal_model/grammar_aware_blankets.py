"""Exact grammar-aware dynamic blanket certificates.

A finite prefix grammar is part of a boundary contract: it specifies which
counterfactual actions are legal from the present contract state.  A summary of
physical system state alone can therefore be insufficient even when all current
outputs agree.  This module gives the positive theorem complementing delayed
addressability:

* a summary on ``system_state x grammar_state`` is exact for all legal future
  traces precisely when it preserves output, enabled-action structure, and
  successor summary under every enabled action;
* the stable grammar-aware trace quotient is the coarsest such interface; and
* a finite grammar-aware blanket gives both a memory upper bound and a finite
  horizon bound for each fixed constrained system.

The grammar state is a declared contract state.  The theorem does not interpret
it automatically as an unobserved physical or biological variable.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import log2
from typing import Hashable, Iterable

from .delayed_addressability import (
    FIRE,
    WAIT,
    FinitePrefixGrammar,
    GrammarAwareControlledSystem,
    GrammarHorizonStabilizationCertificate,
    certify_grammar_horizon_stabilization,
)
from .dynamic_boundary_blankets import FiniteControlledOutputSystem

Action = str
GrammarState = int
ProductState = tuple[int, int]
SummaryLabel = Hashable
Partition = tuple[tuple[int, ...], ...]


def _validate_nonnegative_integer(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")


def _validate_positive_integer(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _canonical_labels(values: Iterable[Hashable]) -> tuple[int, ...]:
    labels: dict[Hashable, int] = {}
    result: list[int] = []
    for value in values:
        if value not in labels:
            labels[value] = len(labels)
        result.append(labels[value])
    return tuple(result)


def _partition_from_labels(labels: tuple[int, ...]) -> Partition:
    blocks: dict[int, list[int]] = {}
    for index, label in enumerate(labels):
        blocks.setdefault(label, []).append(index)
    return tuple(tuple(blocks[label]) for label in sorted(blocks))


def _validate_product_state(constrained_system: GrammarAwareControlledSystem, pair: ProductState) -> None:
    if not isinstance(pair, tuple) or len(pair) != 2:
        raise ValueError("product state must be a (system_state, grammar_state) pair")
    system_state, grammar_state = pair
    constrained_system.system.validate_state(system_state)
    constrained_system.grammar.validate_state(grammar_state)


def grammar_aware_output_trace(
    constrained_system: GrammarAwareControlledSystem,
    pair: ProductState,
    word: Iterable[Action],
) -> tuple[Hashable, ...]:
    """Exact window trace for a word legal from the pair's grammar state."""
    _validate_product_state(constrained_system, pair)
    system_state, grammar_state = pair
    normalized = constrained_system.grammar.normalize_legal_word(word, start_state=grammar_state)
    trace = [constrained_system.system.output(system_state)]
    for action in normalized:
        system_state = constrained_system.system.transition(system_state, action)
        grammar_state = constrained_system.grammar.transition(grammar_state, action)
        trace.append(constrained_system.system.output(system_state))
    return tuple(trace)


def explicit_grammar_aware_partition(
    constrained_system: GrammarAwareControlledSystem,
    horizon: int,
) -> Partition:
    """Partition product states by explicit legal-word trace signatures.

    The legal word itself is included in the signature.  This means two product
    states with different enabled future languages are not silently treated as
    equivalent merely because their currently available output values agree.
    """
    _validate_nonnegative_integer(horizon, "horizon")
    signatures = []
    for pair in constrained_system.product_states:
        _, grammar_state = pair
        words = constrained_system.grammar.legal_words_through(horizon, start_state=grammar_state)
        signatures.append(
            tuple((word, grammar_aware_output_trace(constrained_system, pair, word)) for word in words)
        )
    return _partition_from_labels(_canonical_labels(signatures))


@dataclass(frozen=True)
class GrammarAwareDynamicInterfaceCertificate:
    """An exact partial macro-interface on system-state × grammar-state.

    Equal summary labels must have equal current output, exactly the same enabled
    action set, and equal summary labels after each enabled action.  These are the
    finite partial-transition right-congruence conditions for all legal words.
    """

    constrained_system: GrammarAwareControlledSystem
    summary_labels: tuple[SummaryLabel, ...]

    @property
    def canonical_summary_labels(self) -> tuple[int, ...]:
        return _canonical_labels(self.summary_labels)

    @property
    def summary_block_count(self) -> int:
        return len(set(self.canonical_summary_labels))

    @property
    def summary_partition(self) -> Partition:
        return _partition_from_labels(self.canonical_summary_labels)

    def product_pair_at(self, product_index: int) -> ProductState:
        if not isinstance(product_index, int) or isinstance(product_index, bool) or not 0 <= product_index < self.constrained_system.product_state_count:
            raise ValueError("product index is outside the grammar-aware product")
        return self.constrained_system.product_states[product_index]

    def representative_index(self, macrostate: int) -> int:
        if not isinstance(macrostate, int) or isinstance(macrostate, bool) or not 0 <= macrostate < self.summary_block_count:
            raise ValueError("macrostate is outside the summary quotient")
        return self.canonical_summary_labels.index(macrostate)

    def macro_output(self, macrostate: int) -> Hashable:
        system_state, _ = self.product_pair_at(self.representative_index(macrostate))
        return self.constrained_system.system.output(system_state)

    def macro_legal_actions(self, macrostate: int) -> tuple[Action, ...]:
        _, grammar_state = self.product_pair_at(self.representative_index(macrostate))
        return self.constrained_system.grammar.legal_actions(grammar_state)

    def macro_transition(self, macrostate: int, action: Action) -> int:
        product_index = self.representative_index(macrostate)
        system_state, grammar_state = self.product_pair_at(product_index)
        if action not in self.constrained_system.grammar.legal_actions(grammar_state):
            raise ValueError(f"action {action!r} is illegal at macrostate {macrostate}")
        successor = (
            self.constrained_system.system.transition(system_state, action),
            self.constrained_system.grammar.transition(grammar_state, action),
        )
        return self.canonical_summary_labels[self.constrained_system.product_index(successor)]

    def verify(self) -> bool:
        try:
            system = self.constrained_system.system
            grammar = self.constrained_system.grammar
            pairs = self.constrained_system.product_states
            if not isinstance(self.summary_labels, tuple) or len(self.summary_labels) != len(pairs):
                return False
            for label in self.summary_labels:
                hash(label)
            for left_index, (left_state, left_grammar) in enumerate(pairs):
                for right_index, (right_state, right_grammar) in enumerate(pairs):
                    if self.summary_labels[left_index] != self.summary_labels[right_index]:
                        continue
                    if system.output(left_state) != system.output(right_state):
                        return False
                    left_actions = grammar.legal_actions(left_grammar)
                    right_actions = grammar.legal_actions(right_grammar)
                    if left_actions != right_actions:
                        return False
                    for action in left_actions:
                        left_successor = self.constrained_system.product_index(
                            (system.transition(left_state, action), grammar.transition(left_grammar, action))
                        )
                        right_successor = self.constrained_system.product_index(
                            (system.transition(right_state, action), grammar.transition(right_grammar, action))
                        )
                        if self.summary_labels[left_successor] != self.summary_labels[right_successor]:
                            return False
            canonical = certify_grammar_aware_canonical_interface(self.constrained_system)
            for left_index in range(len(pairs)):
                for right_index in range(len(pairs)):
                    if self.summary_labels[left_index] == self.summary_labels[right_index] and canonical.canonical_labels[left_index] != canonical.canonical_labels[right_index]:
                        return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


@dataclass(frozen=True)
class GrammarAwareCanonicalInterfaceCertificate:
    """The coarsest exact interface for every legal future word on the product."""

    constrained_system: GrammarAwareControlledSystem
    stabilization: GrammarHorizonStabilizationCertificate
    canonical_labels: tuple[int, ...]

    @property
    def canonical_block_count(self) -> int:
        return len(set(self.canonical_labels))

    @property
    def stabilization_horizon(self) -> int:
        return self.stabilization.stabilization_horizon

    @property
    def product_state_bound(self) -> int:
        return self.constrained_system.product_state_count - 1

    @property
    def initial_slice_block_count(self) -> int:
        labels = tuple(
            self.canonical_labels[
                self.constrained_system.product_index((system_state, self.constrained_system.grammar.initial_state))
            ]
            for system_state in self.constrained_system.system.states
        )
        return len(set(labels))

    def verify(self) -> bool:
        try:
            if self.stabilization.constrained_system != self.constrained_system:
                return False
            if not self.stabilization.verify():
                return False
            expected = self.constrained_system.horizon_labels(self.stabilization_horizon)
            if self.canonical_labels != expected:
                return False
            if len(self.canonical_labels) != self.constrained_system.product_state_count:
                return False
            if self.canonical_block_count != self.stabilization.canonical_product_block_count:
                return False
            if self.stabilization_horizon > self.product_state_bound:
                return False
            return GrammarAwareDynamicInterfaceCertificate(self.constrained_system, self.canonical_labels).verify()
        except (AssertionError, TypeError, ValueError):
            return False


def certify_grammar_aware_canonical_interface(
    constrained_system: GrammarAwareControlledSystem,
) -> GrammarAwareCanonicalInterfaceCertificate:
    stabilization = certify_grammar_horizon_stabilization(constrained_system)
    certificate = GrammarAwareCanonicalInterfaceCertificate(
        constrained_system=constrained_system,
        stabilization=stabilization,
        canonical_labels=constrained_system.horizon_labels(stabilization.stabilization_horizon),
    )
    if not certificate.verify():
        raise AssertionError("grammar-aware canonical interface certificate did not verify")
    return certificate


@dataclass(frozen=True)
class GrammarAwareRefinementCertificate:
    """Certificate that a proposed dynamic interface refines the canonical quotient."""

    interface: GrammarAwareDynamicInterfaceCertificate
    canonical: GrammarAwareCanonicalInterfaceCertificate

    def verify(self) -> bool:
        try:
            if self.interface.constrained_system != self.canonical.constrained_system:
                return False
            if not self.interface.verify() or not self.canonical.verify():
                return False
            for left_index in range(self.interface.constrained_system.product_state_count):
                for right_index in range(self.interface.constrained_system.product_state_count):
                    if self.interface.summary_labels[left_index] == self.interface.summary_labels[right_index]:
                        if self.canonical.canonical_labels[left_index] != self.canonical.canonical_labels[right_index]:
                            return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_grammar_aware_refinement(
    constrained_system: GrammarAwareControlledSystem,
    summary_labels: tuple[SummaryLabel, ...],
) -> GrammarAwareRefinementCertificate:
    interface = GrammarAwareDynamicInterfaceCertificate(constrained_system, summary_labels)
    if not interface.verify():
        raise ValueError("summary labels are not a grammar-aware dynamic interface")
    certificate = GrammarAwareRefinementCertificate(
        interface=interface,
        canonical=certify_grammar_aware_canonical_interface(constrained_system),
    )
    if not certificate.verify():
        raise AssertionError("grammar-aware refinement certificate did not verify")
    return certificate


@dataclass(frozen=True)
class GrammarAwareDynamicBlanketCertificate:
    """Finite positive blanket certificate for the product semantic state.

    ``summary_labels`` can be any finite summary of physical state, boundary
    state, and grammar-contract state.  Its block count upper-bounds the canonical
    legal-word interface, and therefore also bounds the finite refinement horizon.
    """

    constrained_system: GrammarAwareControlledSystem
    summary_labels: tuple[SummaryLabel, ...]
    canonical_block_count: int
    stabilization_horizon: int

    @property
    def summary_block_count(self) -> int:
        return len(set(_canonical_labels(self.summary_labels)))

    @property
    def canonical_interface_bits(self) -> float:
        return log2(self.canonical_block_count)

    @property
    def blanket_upper_bound_bits(self) -> float:
        return log2(self.summary_block_count)

    @property
    def summary_horizon_bound(self) -> int:
        return self.summary_block_count - 1

    def verify(self) -> bool:
        try:
            refinement = certify_grammar_aware_refinement(self.constrained_system, self.summary_labels)
            canonical = refinement.canonical
            if self.canonical_block_count != canonical.canonical_block_count:
                return False
            if self.stabilization_horizon != canonical.stabilization_horizon:
                return False
            if self.canonical_block_count > self.summary_block_count:
                return False
            if self.stabilization_horizon > self.summary_horizon_bound:
                return False
            if self.canonical_interface_bits > self.blanket_upper_bound_bits + 1e-12:
                return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_grammar_aware_dynamic_blanket(
    constrained_system: GrammarAwareControlledSystem,
    summary_labels: tuple[SummaryLabel, ...],
) -> GrammarAwareDynamicBlanketCertificate:
    canonical = certify_grammar_aware_canonical_interface(constrained_system)
    certificate = GrammarAwareDynamicBlanketCertificate(
        constrained_system=constrained_system,
        summary_labels=summary_labels,
        canonical_block_count=canonical.canonical_block_count,
        stabilization_horizon=canonical.stabilization_horizon,
    )
    if not certificate.verify():
        raise ValueError("summary labels are not a grammar-aware dynamic blanket")
    return certificate


@dataclass(frozen=True)
class EnabledActionMismatchCertificate:
    """One proposed merge that fails because its legal futures differ."""

    constrained_system: GrammarAwareControlledSystem
    summary_labels: tuple[SummaryLabel, ...]
    left: ProductState
    right: ProductState
    left_enabled_actions: tuple[Action, ...]
    right_enabled_actions: tuple[Action, ...]

    def verify(self) -> bool:
        try:
            _validate_product_state(self.constrained_system, self.left)
            _validate_product_state(self.constrained_system, self.right)
            if not isinstance(self.summary_labels, tuple) or len(self.summary_labels) != self.constrained_system.product_state_count:
                return False
            left_index = self.constrained_system.product_index(self.left)
            right_index = self.constrained_system.product_index(self.right)
            if self.summary_labels[left_index] != self.summary_labels[right_index]:
                return False
            if self.left_enabled_actions != self.constrained_system.grammar.legal_actions(self.left[1]):
                return False
            if self.right_enabled_actions != self.constrained_system.grammar.legal_actions(self.right[1]):
                return False
            return self.left_enabled_actions != self.right_enabled_actions
        except (TypeError, ValueError):
            return False


def find_enabled_action_mismatch(
    constrained_system: GrammarAwareControlledSystem,
    summary_labels: tuple[SummaryLabel, ...],
) -> EnabledActionMismatchCertificate | None:
    """Return a concrete enabled-action obstruction for an invalid proposed merge."""
    if not isinstance(summary_labels, tuple) or len(summary_labels) != constrained_system.product_state_count:
        raise ValueError("summary_labels must provide one label per product state")
    for left_index, left in enumerate(constrained_system.product_states):
        for right_index in range(left_index + 1, constrained_system.product_state_count):
            right = constrained_system.product_states[right_index]
            if summary_labels[left_index] != summary_labels[right_index]:
                continue
            left_actions = constrained_system.grammar.legal_actions(left[1])
            right_actions = constrained_system.grammar.legal_actions(right[1])
            if left_actions != right_actions:
                certificate = EnabledActionMismatchCertificate(
                    constrained_system=constrained_system,
                    summary_labels=summary_labels,
                    left=left,
                    right=right,
                    left_enabled_actions=left_actions,
                    right_enabled_actions=right_actions,
                )
                if not certificate.verify():
                    raise AssertionError("enabled-action mismatch certificate did not verify")
                return certificate
    return None


def delayed_prefix_grammar(delay: int) -> FinitePrefixGrammar:
    """A finite grammar with exactly ``wait^delay fire`` as the revealing word."""
    _validate_nonnegative_integer(delay, "delay")
    rows = []
    for state in range(delay):
        rows.append((state + 1, None))
    rows.append((None, delay + 1))
    rows.append((None, None))
    return FinitePrefixGrammar(actions=(WAIT, FIRE), transition_table=tuple(rows))


def constant_output_delayed_system(delay: int) -> GrammarAwareControlledSystem:
    """One physical state, one constant output, but multiple legal-future states."""
    _validate_positive_integer(delay, "delay")
    system = FiniteControlledOutputSystem(
        actions=(WAIT, FIRE),
        transition_table=((0, 0),),
        outputs=("constant-window-output",),
    )
    return GrammarAwareControlledSystem(system=system, grammar=delayed_prefix_grammar(delay))


@dataclass(frozen=True)
class GrammarStateNecessityCertificate:
    """A constant physical system whose grammar state cannot be omitted."""

    delay: int
    constrained_system: GrammarAwareControlledSystem
    omitted_grammar_summary_labels: tuple[SummaryLabel, ...]
    enabled_action_obstruction: EnabledActionMismatchCertificate
    canonical: GrammarAwareCanonicalInterfaceCertificate

    def verify(self) -> bool:
        try:
            _validate_positive_integer(self.delay, "delay")
            expected = constant_output_delayed_system(self.delay)
            if self.constrained_system != expected:
                return False
            if self.constrained_system.system.state_count != 1:
                return False
            if len(set(self.constrained_system.system.outputs)) != 1:
                return False
            if self.omitted_grammar_summary_labels != ("omit-grammar",) * self.constrained_system.product_state_count:
                return False
            if GrammarAwareDynamicInterfaceCertificate(
                self.constrained_system, self.omitted_grammar_summary_labels
            ).verify():
                return False
            if not self.enabled_action_obstruction.verify():
                return False
            if self.enabled_action_obstruction.left != (0, 0):
                return False
            if self.enabled_action_obstruction.right != (0, self.delay):
                return False
            if self.enabled_action_obstruction.left_enabled_actions != (WAIT,):
                return False
            if self.enabled_action_obstruction.right_enabled_actions != (FIRE,):
                return False
            if not self.canonical.verify():
                return False
            return self.canonical.canonical_block_count == self.constrained_system.grammar.state_count
        except (AssertionError, TypeError, ValueError):
            return False


def certify_grammar_state_necessity(delay: int) -> GrammarStateNecessityCertificate:
    constrained_system = constant_output_delayed_system(delay)
    omitted_labels = ("omit-grammar",) * constrained_system.product_state_count
    obstruction = find_enabled_action_mismatch(constrained_system, omitted_labels)
    if obstruction is None:
        raise AssertionError("constant grammar witness did not expose enabled-action mismatch")
    certificate = GrammarStateNecessityCertificate(
        delay=delay,
        constrained_system=constrained_system,
        omitted_grammar_summary_labels=omitted_labels,
        enabled_action_obstruction=obstruction,
        canonical=certify_grammar_aware_canonical_interface(constrained_system),
    )
    if not certificate.verify():
        raise AssertionError("grammar-state necessity certificate did not verify")
    return certificate
