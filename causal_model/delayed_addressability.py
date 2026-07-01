"""Delayed addressability and no-uniform-closure-horizon certificates.

For any fixed finite controlled grammar, an exact open quotient stabilizes after
finitely many counterfactual refinement rounds.  This module proves the
complementary family-level fact: no single finite observation/intervention
horizon certifies closure uniformly when exterior completions become legally
addressable only after an arbitrarily long declared delay.

The delayed witness has a constant abstract action alphabet ``{wait, fire}``.
A fixed context chooses a reader's *structural attachment* to one exterior
memory leaf; port identity is never sent as a growing action symbol.  Before the
reader is enabled, every legal trace is exterior-blind.  Once enabled, ``fire``
reveals the bit at that already attached leaf.

The module contains:

* a general finite prefix-grammar product quotient and stabilization certificate;
* the delayed addressability rectangle ``(memory, horizon) = (m, H + 1)``;
* a passive/finite-horizon closed-versus-open nonidentifiability certificate; and
* a degree-three relay-tree realization using the existing one-token protocol.

The finite replays check certificate implementations.  The lower bounds in the
documentation are analytic consequences of the declared delayed grammar and
concrete separating words; they are not simulation claims.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import log2
from typing import Hashable, Iterable

from .dynamic_boundary_blankets import FiniteControlledOutputSystem
from .relay_tree_compilation import (
    RelayTreeTopology,
    coordinate_state,
    is_quiescent,
    one_token_relay_grammar,
    quiescent_configuration,
    run_macro_probe,
    micro_step,
)

Action = str
CoordinateState = tuple[int, ...]
GrammarState = int
ProductState = tuple[int, int]
Partition = tuple[tuple[int, ...], ...]

WAIT: Action = "wait"
FIRE: Action = "fire"
LOCAL_ACTIONS: tuple[Action, Action] = (WAIT, FIRE)


def _validate_positive_integer(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _validate_nonnegative_integer(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")


def _validate_port(module_count: int, port: int) -> None:
    if not isinstance(port, int) or isinstance(port, bool) or not 0 <= port < module_count:
        raise ValueError(f"port must be an integer in [0, {module_count - 1}]")


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
    for state, label in enumerate(labels):
        blocks.setdefault(label, []).append(state)
    return tuple(tuple(blocks[label]) for label in sorted(blocks))


@dataclass(frozen=True)
class FinitePrefixGrammar:
    """A deterministic finite prefix-closed action grammar.

    Every grammar state is accepting.  A ``None`` transition marks an action as
    illegal at that grammar state, so all prefixes of legal words are legal.
    """

    actions: tuple[Action, ...]
    transition_table: tuple[tuple[int | None, ...], ...]
    initial_state: GrammarState = 0

    def __post_init__(self) -> None:
        if not isinstance(self.actions, tuple) or not self.actions:
            raise ValueError("actions must be a nonempty tuple")
        if any(not isinstance(action, str) or not action for action in self.actions):
            raise ValueError("actions must be nonempty strings")
        if len(set(self.actions)) != len(self.actions):
            raise ValueError("actions must be unique")
        if not isinstance(self.transition_table, tuple) or not self.transition_table:
            raise ValueError("transition_table must be a nonempty tuple")
        state_count = len(self.transition_table)
        if not isinstance(self.initial_state, int) or isinstance(self.initial_state, bool) or not 0 <= self.initial_state < state_count:
            raise ValueError("initial_state is outside the grammar state space")
        for row in self.transition_table:
            if not isinstance(row, tuple) or len(row) != len(self.actions):
                raise ValueError("every grammar transition row must match the action count")
            for target in row:
                if target is None:
                    continue
                if not isinstance(target, int) or isinstance(target, bool) or not 0 <= target < state_count:
                    raise ValueError("grammar transition targets must be valid states or None")

    @property
    def state_count(self) -> int:
        return len(self.transition_table)

    @property
    def states(self) -> tuple[GrammarState, ...]:
        return tuple(range(self.state_count))

    def action_index(self, action: Action) -> int:
        try:
            return self.actions.index(action)
        except ValueError as error:
            raise ValueError(f"unknown grammar action: {action!r}") from error

    def legal_actions(self, grammar_state: GrammarState) -> tuple[Action, ...]:
        self.validate_state(grammar_state)
        return tuple(
            action
            for action, target in zip(self.actions, self.transition_table[grammar_state])
            if target is not None
        )

    def transition(self, grammar_state: GrammarState, action: Action) -> GrammarState:
        self.validate_state(grammar_state)
        index = self.action_index(action)
        target = self.transition_table[grammar_state][index]
        if target is None:
            raise ValueError(f"action {action!r} is illegal at grammar state {grammar_state}")
        return target

    def validate_state(self, grammar_state: GrammarState) -> None:
        if not isinstance(grammar_state, int) or isinstance(grammar_state, bool) or not 0 <= grammar_state < self.state_count:
            raise ValueError("grammar state is outside the finite grammar")

    def normalize_legal_word(self, word: Iterable[Action], start_state: GrammarState | None = None) -> tuple[Action, ...]:
        try:
            normalized = tuple(word)
        except TypeError as error:
            raise ValueError("word must be an iterable of actions") from error
        current = self.initial_state if start_state is None else start_state
        self.validate_state(current)
        for action in normalized:
            current = self.transition(current, action)
        return normalized

    def legal_words_through(self, horizon: int, start_state: GrammarState | None = None) -> tuple[tuple[Action, ...], ...]:
        """Enumerate legal words of length at most ``horizon`` from one state."""
        _validate_nonnegative_integer(horizon, "horizon")
        initial = self.initial_state if start_state is None else start_state
        self.validate_state(initial)
        words: list[tuple[Action, ...]] = [()]
        frontier: list[tuple[GrammarState, tuple[Action, ...]]] = [(initial, ())]
        for _ in range(horizon):
            next_frontier: list[tuple[GrammarState, tuple[Action, ...]]] = []
            for state, prefix in frontier:
                for action in self.legal_actions(state):
                    next_state = self.transition(state, action)
                    word = prefix + (action,)
                    words.append(word)
                    next_frontier.append((next_state, word))
            frontier = next_frontier
        return tuple(words)


@dataclass(frozen=True)
class GrammarAwareControlledSystem:
    """Finite deterministic output system constrained by a prefix grammar.

    The all-word quotient is computed on the product state
    ``(system_state, grammar_state)``.  Grammar state is part of the boundary
    contract: it controls which future interventions are actually legal.
    """

    system: FiniteControlledOutputSystem
    grammar: FinitePrefixGrammar

    def __post_init__(self) -> None:
        if self.system.actions != self.grammar.actions:
            raise ValueError("system and grammar must use the same ordered action alphabet")

    @property
    def product_states(self) -> tuple[ProductState, ...]:
        return tuple(
            (system_state, grammar_state)
            for system_state in self.system.states
            for grammar_state in self.grammar.states
        )

    @property
    def product_state_count(self) -> int:
        return self.system.state_count * self.grammar.state_count

    def product_index(self, pair: ProductState) -> int:
        system_state, grammar_state = pair
        self.system.validate_state(system_state)
        self.grammar.validate_state(grammar_state)
        return system_state * self.grammar.state_count + grammar_state

    def horizon_labels(self, horizon: int) -> tuple[int, ...]:
        """Labels for agreement on all legal words of length at most ``horizon``."""
        _validate_nonnegative_integer(horizon, "horizon")
        pairs = self.product_states
        labels = _canonical_labels(self.system.output(system_state) for system_state, _ in pairs)
        for _ in range(horizon):
            labels = _canonical_labels(
                (
                    self.system.output(system_state),
                    tuple(
                        (
                            action,
                            labels[
                                self.product_index(
                                    (
                                        self.system.transition(system_state, action),
                                        self.grammar.transition(grammar_state, action),
                                    )
                                )
                            ],
                        )
                        for action in self.grammar.legal_actions(grammar_state)
                    ),
                )
                for system_state, grammar_state in pairs
            )
        return labels

    def product_partition(self, horizon: int) -> Partition:
        return _partition_from_labels(self.horizon_labels(horizon))

    def initial_labels(self, horizon: int) -> tuple[int, ...]:
        labels = self.horizon_labels(horizon)
        return tuple(labels[self.product_index((state, self.grammar.initial_state))] for state in self.system.states)

    def initial_partition(self, horizon: int) -> Partition:
        return _partition_from_labels(self.initial_labels(horizon))

    def first_product_stabilizing_horizon(self) -> int:
        for horizon in range(self.product_state_count):
            if self.horizon_labels(horizon) == self.horizon_labels(horizon + 1):
                return horizon
        raise AssertionError("grammar-aware partition refinement did not stabilize by the product-state bound")


@dataclass(frozen=True)
class GrammarHorizonStabilizationCertificate:
    """Exact finite stabilization certificate for a grammar-aware product quotient."""

    constrained_system: GrammarAwareControlledSystem
    stabilization_horizon: int
    product_block_counts: tuple[int, ...]
    canonical_product_block_count: int

    @property
    def product_state_bound(self) -> int:
        return self.constrained_system.product_state_count - 1

    def verify(self) -> bool:
        try:
            _validate_nonnegative_integer(self.stabilization_horizon, "stabilization_horizon")
            if self.stabilization_horizon > self.product_state_bound:
                return False
            expected_counts = tuple(
                len(self.constrained_system.product_partition(horizon))
                for horizon in range(self.stabilization_horizon + 2)
            )
            if self.product_block_counts != expected_counts:
                return False
            if self.product_block_counts[-1] != self.product_block_counts[-2]:
                return False
            if any(
                self.constrained_system.product_partition(horizon)
                == self.constrained_system.product_partition(horizon + 1)
                for horizon in range(self.stabilization_horizon)
            ):
                return False
            if self.canonical_product_block_count != self.product_block_counts[-2]:
                return False
            return self.constrained_system.horizon_labels(self.stabilization_horizon) == self.constrained_system.horizon_labels(
                self.stabilization_horizon + 1
            )
        except (AssertionError, ValueError):
            return False


def certify_grammar_horizon_stabilization(
    constrained_system: GrammarAwareControlledSystem,
) -> GrammarHorizonStabilizationCertificate:
    horizon = constrained_system.first_product_stabilizing_horizon()
    certificate = GrammarHorizonStabilizationCertificate(
        constrained_system=constrained_system,
        stabilization_horizon=horizon,
        product_block_counts=tuple(
            len(constrained_system.product_partition(step)) for step in range(horizon + 2)
        ),
        canonical_product_block_count=len(constrained_system.product_partition(horizon)),
    )
    if not certificate.verify():
        raise AssertionError("grammar-horizon stabilization certificate did not verify")
    return certificate


@dataclass(frozen=True)
class DelayedReaderGrammar:
    """Prefix grammar in which a fixed attached reader fires only after a delay.

    The only local symbols are ``wait`` and ``fire``.  The port is supplied by a
    structural reader attachment in a context, not by an action symbol.
    """

    delay: int

    def __post_init__(self) -> None:
        _validate_nonnegative_integer(self.delay, "delay")

    @property
    def initial_state(self) -> GrammarState:
        return 0

    @property
    def ready_state(self) -> GrammarState:
        return self.delay

    @property
    def terminal_state(self) -> GrammarState:
        return self.delay + 1

    @property
    def state_count(self) -> int:
        return self.delay + 2

    def as_prefix_grammar(self) -> FinitePrefixGrammar:
        rows: list[tuple[int | None, int | None]] = []
        for grammar_state in range(self.state_count):
            if grammar_state < self.ready_state:
                rows.append((grammar_state + 1, None))
            elif grammar_state == self.ready_state:
                rows.append((None, self.terminal_state))
            else:
                rows.append((None, None))
        return FinitePrefixGrammar(
            actions=LOCAL_ACTIONS,
            transition_table=tuple(rows),
            initial_state=self.initial_state,
        )

    def legal_words_through(self, horizon: int) -> tuple[tuple[Action, ...], ...]:
        return self.as_prefix_grammar().legal_words_through(horizon)

    @property
    def revealing_word(self) -> tuple[Action, ...]:
        return (WAIT,) * self.delay + (FIRE,)

    def verify(self) -> bool:
        try:
            grammar = self.as_prefix_grammar()
            if grammar.actions != LOCAL_ACTIONS or grammar.initial_state != 0:
                return False
            for grammar_state in range(self.ready_state):
                if grammar.legal_actions(grammar_state) != (WAIT,):
                    return False
            if grammar.legal_actions(self.ready_state) != (FIRE,):
                return False
            if grammar.legal_actions(self.terminal_state) != ():
                return False
            if self.revealing_word not in grammar.legal_words_through(self.delay + 1):
                return False
            if any(FIRE in word for word in grammar.legal_words_through(self.delay)):
                return False
            return True
        except ValueError:
            return False


def coordinate_states(module_count: int) -> tuple[CoordinateState, ...]:
    _validate_positive_integer(module_count, "module_count")
    return tuple(tuple(bits) for bits in product((0, 1), repeat=module_count + 1))


def _state_index(module_count: int, state: CoordinateState) -> int:
    if not isinstance(state, tuple) or len(state) != module_count + 1 or any(bit not in (0, 1) for bit in state):
        raise ValueError("coordinate state must contain one focal bit and one binary bit per exterior module")
    index = 0
    for bit in state:
        index = 2 * index + bit
    return index


def _probe_coordinate_state(module_count: int, state: CoordinateState, port: int) -> CoordinateState:
    _validate_port(module_count, port)
    _state_index(module_count, state)
    return (state[port + 1],) + state[1:]


@dataclass(frozen=True)
class DelayedReaderContext:
    """One closed context with one reader structurally attached to a fixed port."""

    module_count: int
    delay: int
    attached_port: int
    reveals_exterior: bool = True

    def __post_init__(self) -> None:
        _validate_positive_integer(self.module_count, "module_count")
        _validate_nonnegative_integer(self.delay, "delay")
        _validate_port(self.module_count, self.attached_port)
        if not isinstance(self.reveals_exterior, bool):
            raise ValueError("reveals_exterior must be boolean")

    @property
    def grammar(self) -> DelayedReaderGrammar:
        return DelayedReaderGrammar(self.delay)

    @property
    def states(self) -> tuple[CoordinateState, ...]:
        return coordinate_states(self.module_count)

    @property
    def action_alphabet(self) -> tuple[Action, Action]:
        return LOCAL_ACTIONS

    def controlled_system(self) -> FiniteControlledOutputSystem:
        states = self.states
        rows: list[tuple[int, int]] = []
        for state in states:
            wait_target = _state_index(self.module_count, state)
            fire_state = (
                _probe_coordinate_state(self.module_count, state, self.attached_port)
                if self.reveals_exterior
                else state
            )
            rows.append((wait_target, _state_index(self.module_count, fire_state)))
        return FiniteControlledOutputSystem(
            actions=LOCAL_ACTIONS,
            transition_table=tuple(rows),
            outputs=tuple(state[0] for state in states),
        )

    def constrained_system(self) -> GrammarAwareControlledSystem:
        return GrammarAwareControlledSystem(self.controlled_system(), self.grammar.as_prefix_grammar())

    def trace(self, state: CoordinateState, word: Iterable[Action]) -> tuple[int, ...]:
        state_index = _state_index(self.module_count, state)
        normalized = self.grammar.as_prefix_grammar().normalize_legal_word(word)
        return tuple(self.controlled_system().output_trace(state_index, normalized))

    def horizon_partition(self, horizon: int) -> tuple[tuple[CoordinateState, ...], ...]:
        _validate_nonnegative_integer(horizon, "horizon")
        blocks = self.constrained_system().initial_partition(horizon)
        states = self.states
        return tuple(tuple(states[index] for index in block) for block in blocks)

    def horizon_labels(self, horizon: int) -> tuple[int, ...]:
        _validate_nonnegative_integer(horizon, "horizon")
        return self.constrained_system().initial_labels(horizon)


@dataclass(frozen=True)
class DelayedSeparatingWordCertificate:
    """A legal delayed word exposing one externally stored bit in one context."""

    module_count: int
    delay: int
    port: int
    left: CoordinateState
    right: CoordinateState
    word: tuple[Action, ...]
    left_trace: tuple[int, ...]
    right_trace: tuple[int, ...]

    def verify(self) -> bool:
        try:
            _validate_positive_integer(self.module_count, "module_count")
            _validate_nonnegative_integer(self.delay, "delay")
            _validate_port(self.module_count, self.port)
            context = DelayedReaderContext(self.module_count, self.delay, self.port, reveals_exterior=True)
            if self.left == self.right or self.left[0] != self.right[0]:
                return False
            if any(self.left[index] != self.right[index] for index in range(1, self.module_count + 1) if index != self.port + 1):
                return False
            if self.left[self.port + 1] == self.right[self.port + 1]:
                return False
            if self.word != context.grammar.revealing_word:
                return False
            if self.left_trace != context.trace(self.left, self.word):
                return False
            if self.right_trace != context.trace(self.right, self.word):
                return False
            if self.left_trace[:-1] != self.right_trace[:-1]:
                return False
            return self.left_trace[-1] != self.right_trace[-1]
        except ValueError:
            return False


def delayed_separating_word_certificate(
    module_count: int,
    delay: int,
    port: int,
    focal_bit: int = 0,
) -> DelayedSeparatingWordCertificate:
    _validate_positive_integer(module_count, "module_count")
    _validate_nonnegative_integer(delay, "delay")
    _validate_port(module_count, port)
    if focal_bit not in (0, 1):
        raise ValueError("focal_bit must be 0 or 1")
    left_bits = [0] * module_count
    right_bits = [0] * module_count
    right_bits[port] = 1
    left = (focal_bit,) + tuple(left_bits)
    right = (focal_bit,) + tuple(right_bits)
    context = DelayedReaderContext(module_count, delay, port, reveals_exterior=True)
    certificate = DelayedSeparatingWordCertificate(
        module_count=module_count,
        delay=delay,
        port=port,
        left=left,
        right=right,
        word=context.grammar.revealing_word,
        left_trace=context.trace(left, context.grammar.revealing_word),
        right_trace=context.trace(right, context.grammar.revealing_word),
    )
    if not certificate.verify():
        raise AssertionError("constructed delayed separating-word certificate did not verify")
    return certificate


@dataclass(frozen=True)
class DelayedOpenFamily:
    """All structural reader attachments for one delayed exterior family.

    A context chooses the reader attachment ``attached_port``.  The action
    alphabet remains exactly ``(wait, fire)`` in every context.  The robust open
    partition is the common refinement over all allowed attachments.
    """

    module_count: int
    delay: int
    reveals_exterior: bool = True

    def __post_init__(self) -> None:
        _validate_positive_integer(self.module_count, "module_count")
        _validate_nonnegative_integer(self.delay, "delay")
        if not isinstance(self.reveals_exterior, bool):
            raise ValueError("reveals_exterior must be boolean")

    @property
    def grammar(self) -> DelayedReaderGrammar:
        return DelayedReaderGrammar(self.delay)

    @property
    def states(self) -> tuple[CoordinateState, ...]:
        return coordinate_states(self.module_count)

    @property
    def ports(self) -> tuple[int, ...]:
        return tuple(range(self.module_count))

    def context(self, port: int) -> DelayedReaderContext:
        return DelayedReaderContext(self.module_count, self.delay, port, self.reveals_exterior)

    def robust_labels(self, horizon: int) -> tuple[int, ...]:
        _validate_nonnegative_integer(horizon, "horizon")
        per_context_labels = tuple(self.context(port).horizon_labels(horizon) for port in self.ports)
        return _canonical_labels(
            tuple(labels[state_index] for labels in per_context_labels)
            for state_index in range(len(self.states))
        )

    def robust_partition(self, horizon: int) -> tuple[tuple[CoordinateState, ...], ...]:
        states = self.states
        return tuple(
            tuple(states[state_index] for state_index in block)
            for block in _partition_from_labels(self.robust_labels(horizon))
        )

    def robust_block_count(self, horizon: int) -> int:
        return len(self.robust_partition(horizon))

    def robust_trace_signature(self, state: CoordinateState, horizon: int) -> tuple[tuple[tuple[int, ...], ...], ...]:
        _validate_nonnegative_integer(horizon, "horizon")
        return tuple(
            tuple(context.trace(state, word) for word in self.grammar.legal_words_through(horizon))
            for context in (self.context(port) for port in self.ports)
        )


@dataclass(frozen=True)
class DelayedAddressabilityCertificate:
    """Certificate for the delayed memory/horizon rectangle.

    The exact conclusions are:

    ``K_closed = 2``, ``K_open = m + 1``, and ``H_star = delay + 1``.
    """

    module_count: int
    delay: int
    pre_reveal_open_block_count: int
    open_block_count: int
    closed_block_counts: tuple[int, ...]
    checked_separating_certificates: int

    @property
    def revealing_horizon(self) -> int:
        return self.delay + 1

    @property
    def closed_interface_bits(self) -> tuple[float, ...]:
        return tuple(log2(block_count) for block_count in self.closed_block_counts)

    @property
    def open_interface_bits(self) -> float:
        return log2(self.open_block_count)

    @property
    def counterfactual_delay(self) -> int:
        return self.revealing_horizon

    @property
    def expected_checked_separating_certificates(self) -> int:
        return 2 * self.module_count

    def verify(self) -> bool:
        try:
            _validate_positive_integer(self.module_count, "module_count")
            _validate_nonnegative_integer(self.delay, "delay")
            grammar = DelayedReaderGrammar(self.delay)
            if not grammar.verify():
                return False
            family = DelayedOpenFamily(self.module_count, self.delay, reveals_exterior=True)
            if self.pre_reveal_open_block_count != 2:
                return False
            if self.open_block_count != 2 ** (self.module_count + 1):
                return False
            if self.closed_block_counts != (4,) * self.module_count:
                return False
            if self.checked_separating_certificates != self.expected_checked_separating_certificates:
                return False
            for horizon in range(self.delay + 1):
                if family.robust_block_count(horizon) != 2:
                    return False
                for port in family.ports:
                    if len(family.context(port).horizon_partition(horizon)) != 2:
                        return False
            if family.robust_block_count(self.revealing_horizon) != self.open_block_count:
                return False
            if family.robust_block_count(self.revealing_horizon + 1) != self.open_block_count:
                return False
            if any(len(block) != 1 for block in family.robust_partition(self.revealing_horizon)):
                return False
            for port in family.ports:
                context = family.context(port)
                if len(context.horizon_partition(self.revealing_horizon)) != 4:
                    return False
                if len(context.horizon_partition(self.revealing_horizon + 1)) != 4:
                    return False
                for focal_bit in (0, 1):
                    if not delayed_separating_word_certificate(
                        self.module_count,
                        self.delay,
                        port,
                        focal_bit,
                    ).verify():
                        return False
                grammar_certificate = certify_grammar_horizon_stabilization(context.constrained_system())
                if not grammar_certificate.verify():
                    return False
            if any(abs(bits - 2.0) > 1e-12 for bits in self.closed_interface_bits):
                return False
            if abs(self.open_interface_bits - (self.module_count + 1)) > 1e-12:
                return False
            return True
        except (AssertionError, ValueError):
            return False


def certify_delayed_addressability(
    module_count: int,
    delay: int,
) -> DelayedAddressabilityCertificate:
    family = DelayedOpenFamily(module_count, delay, reveals_exterior=True)
    certificate = DelayedAddressabilityCertificate(
        module_count=module_count,
        delay=delay,
        pre_reveal_open_block_count=family.robust_block_count(delay),
        open_block_count=family.robust_block_count(delay + 1),
        closed_block_counts=tuple(
            len(family.context(port).horizon_partition(delay + 1)) for port in family.ports
        ),
        checked_separating_certificates=2 * module_count,
    )
    if not certificate.verify():
        raise AssertionError("delayed addressability certificate did not verify")
    return certificate


@dataclass(frozen=True)
class DelayedClosureNonidentifiabilityCertificate:
    """Closed/open model pair indistinguishable through a declared finite horizon."""

    module_count: int
    delay: int
    separating_port: int
    separating_state: CoordinateState
    shared_horizon: int
    separating_word: tuple[Action, ...]
    closed_trace: tuple[int, ...]
    open_trace: tuple[int, ...]

    @property
    def revealing_horizon(self) -> int:
        return self.delay + 1

    def verify(self) -> bool:
        try:
            _validate_positive_integer(self.module_count, "module_count")
            _validate_nonnegative_integer(self.delay, "delay")
            _validate_port(self.module_count, self.separating_port)
            if self.shared_horizon != self.delay:
                return False
            grammar = DelayedReaderGrammar(self.delay)
            if self.separating_word != grammar.revealing_word:
                return False
            open_family = DelayedOpenFamily(self.module_count, self.delay, reveals_exterior=True)
            closed_family = DelayedOpenFamily(self.module_count, self.delay, reveals_exterior=False)
            _state_index(self.module_count, self.separating_state)
            if self.separating_state[0] != 0 or self.separating_state[self.separating_port + 1] != 1:
                return False
            for port in open_family.ports:
                open_context = open_family.context(port)
                closed_context = closed_family.context(port)
                for state in open_family.states:
                    for word in grammar.legal_words_through(self.shared_horizon):
                        if open_context.trace(state, word) != closed_context.trace(state, word):
                            return False
            open_context = open_family.context(self.separating_port)
            closed_context = closed_family.context(self.separating_port)
            if self.open_trace != open_context.trace(self.separating_state, self.separating_word):
                return False
            if self.closed_trace != closed_context.trace(self.separating_state, self.separating_word):
                return False
            if self.open_trace == self.closed_trace:
                return False
            if open_family.robust_block_count(self.shared_horizon) != 2:
                return False
            if closed_family.robust_block_count(self.shared_horizon) != 2:
                return False
            if open_family.robust_block_count(self.revealing_horizon) != 2 ** (self.module_count + 1):
                return False
            if closed_family.robust_block_count(self.revealing_horizon) != 2:
                return False
            return True
        except ValueError:
            return False


def certify_delayed_closure_nonidentifiability(
    module_count: int,
    delay: int,
    port: int = 0,
) -> DelayedClosureNonidentifiabilityCertificate:
    _validate_positive_integer(module_count, "module_count")
    _validate_nonnegative_integer(delay, "delay")
    _validate_port(module_count, port)
    bits = [0] * module_count
    bits[port] = 1
    state = (0,) + tuple(bits)
    grammar = DelayedReaderGrammar(delay)
    open_context = DelayedReaderContext(module_count, delay, port, reveals_exterior=True)
    closed_context = DelayedReaderContext(module_count, delay, port, reveals_exterior=False)
    certificate = DelayedClosureNonidentifiabilityCertificate(
        module_count=module_count,
        delay=delay,
        separating_port=port,
        separating_state=state,
        shared_horizon=delay,
        separating_word=grammar.revealing_word,
        closed_trace=closed_context.trace(state, grammar.revealing_word),
        open_trace=open_context.trace(state, grammar.revealing_word),
    )
    if not certificate.verify():
        raise AssertionError("delayed closure nonidentifiability certificate did not verify")
    return certificate


@dataclass(frozen=True)
class DelayedRelayAttachmentCertificate:
    """Constant-local-grammar degree-three realization of one delayed context.

    Each ``wait`` is one quiescent microtick without a reader firing.  The final
    macro ``fire`` uses the existing reader-to-leaf attachment and relay settling
    protocol.  The attachment selects the port structurally; its identifier is
    not a local action token.
    """

    module_count: int
    delay: int
    port: int
    initial_state: CoordinateState
    wait_configurations: tuple[object, ...]
    final_configuration: object

    def verify(self) -> bool:
        try:
            _validate_positive_integer(self.module_count, "module_count")
            _validate_nonnegative_integer(self.delay, "delay")
            _validate_port(self.module_count, self.port)
            _state_index(self.module_count, self.initial_state)
            topology = RelayTreeTopology.balanced(self.module_count)
            local_grammar = one_token_relay_grammar()
            if not topology.verify() or not local_grammar.verify():
                return False
            if topology.maximum_degree_with_reader(self.port) > local_grammar.maximum_degree:
                return False
            if topology.reader_attachment_edge(self.port)[1] != topology.leaf_for_port(self.port):
                return False
            if len(self.wait_configurations) != self.delay + 1:
                return False
            initial = quiescent_configuration(topology, self.initial_state[0], self.initial_state[1:])
            if self.wait_configurations[0] != initial:
                return False
            current = initial
            for configuration in self.wait_configurations[1:]:
                current = micro_step(topology, current)
                if configuration != current or not is_quiescent(topology, configuration):
                    return False
                if configuration.focal_output != self.initial_state[0]:
                    return False
            expected_final = run_macro_probe(topology, current, self.port)
            if self.final_configuration != expected_final or not is_quiescent(topology, self.final_configuration):
                return False
            return coordinate_state(self.final_configuration) == _probe_coordinate_state(
                self.module_count,
                self.initial_state,
                self.port,
            )
        except (AssertionError, KeyError, ValueError):
            return False


def certify_delayed_relay_attachment(
    module_count: int,
    delay: int,
    port: int,
    initial_state: CoordinateState | None = None,
) -> DelayedRelayAttachmentCertificate:
    _validate_positive_integer(module_count, "module_count")
    _validate_nonnegative_integer(delay, "delay")
    _validate_port(module_count, port)
    state = initial_state if initial_state is not None else (0,) + (0,) * module_count
    _state_index(module_count, state)
    topology = RelayTreeTopology.balanced(module_count)
    current = quiescent_configuration(topology, state[0], state[1:])
    waits = [current]
    for _ in range(delay):
        current = micro_step(topology, current)
        waits.append(current)
    certificate = DelayedRelayAttachmentCertificate(
        module_count=module_count,
        delay=delay,
        port=port,
        initial_state=state,
        wait_configurations=tuple(waits),
        final_configuration=run_macro_probe(topology, current, port),
    )
    if not certificate.verify():
        raise AssertionError("delayed relay attachment certificate did not verify")
    return certificate


def exhaustive_delayed_addressability_summary(
    max_module_count: int = 6,
    max_delay: int = 6,
) -> tuple[DelayedAddressabilityCertificate, ...]:
    """Replay the delayed rectangle family over a finite declared range."""
    _validate_positive_integer(max_module_count, "max_module_count")
    _validate_nonnegative_integer(max_delay, "max_delay")
    return tuple(
        certify_delayed_addressability(module_count, delay)
        for module_count in range(1, max_module_count + 1)
        for delay in range(max_delay + 1)
    )
