"""Delayed joint exterior--mechanism nonidentifiability certificates.

The static joint product theorem shows that independently addressable exterior
coordinates and response type may require additive open-interface memory.  The
delayed-addressability theorem shows that an exterior coordinate may be legally
revealed only after an arbitrarily long prefix.  This module composes those two
facts in one exact binary family.

For each exterior-port count ``m`` and delay ``H`` the macro state is

    (y, b_1, ..., b_m, r) in {0, 1}^{m + 2}.

The declared action kinds are the fixed alphabet ``{wait, read, intervene}``.
A read port is a structural attachment context, not a growing action label.  For
``H`` steps only ``wait`` is legal.  At readiness,

* ``read`` attached to port ``i`` applies ``y <- b_i``; and
* ``intervene`` applies ``y <- y xor r``.

Thus all legal words through horizon ``H`` see only ``y``, whereas words of
length ``H + 1`` separate both exterior coordinates and response type.  The
module proves the exact initial-slice quotient jump

    K_<=H = 1,
    K_full = m + 2,
    H_star = H + 1.

For each fixed finite grammar the quotient remains finite, as required by the
positive grammar-aware blanket theorem.  The no-go is only family-level: no one
finite horizon works uniformly as the delay grows.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from math import log2
from typing import Hashable, Iterable

ActionKind = str
DelayedJointState = tuple[int, ...]

WAIT: ActionKind = "wait"
READ: ActionKind = "read"
INTERVENE: ActionKind = "intervene"
ACTION_KINDS: tuple[ActionKind, ActionKind, ActionKind] = (WAIT, READ, INTERVENE)


def _validate_positive_integer(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _validate_nonnegative_integer(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")


def _validate_bit(value: int, name: str) -> None:
    if value not in (0, 1):
        raise ValueError(f"{name} must be 0 or 1")


def _canonical_labels(values: Iterable[Hashable]) -> tuple[int, ...]:
    labels: dict[Hashable, int] = {}
    result: list[int] = []
    for value in values:
        if value not in labels:
            labels[value] = len(labels)
        result.append(labels[value])
    return tuple(result)


def _partition_from_labels(labels: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    blocks: dict[int, list[int]] = {}
    for state_index, label in enumerate(labels):
        blocks.setdefault(label, []).append(state_index)
    return tuple(tuple(blocks[label]) for label in sorted(blocks))


@dataclass(frozen=True)
class DelayedJointAction:
    """One action kind plus a structural attachment context for ``read``."""

    kind: ActionKind
    read_port: int | None = None

    @classmethod
    def wait(cls) -> "DelayedJointAction":
        return cls(WAIT)

    @classmethod
    def read(cls, port: int) -> "DelayedJointAction":
        return cls(READ, port)

    @classmethod
    def intervene(cls) -> "DelayedJointAction":
        return cls(INTERVENE)

    def validate(self, exterior_port_count: int) -> None:
        _validate_positive_integer(exterior_port_count, "exterior_port_count")
        if self.kind == WAIT:
            if self.read_port is not None:
                raise ValueError("wait has no reader attachment")
            return
        if self.kind == READ:
            if not isinstance(self.read_port, int) or isinstance(self.read_port, bool):
                raise ValueError("read requires one structural exterior port")
            if not 0 <= self.read_port < exterior_port_count:
                raise ValueError("read port is outside the exterior-port range")
            return
        if self.kind == INTERVENE:
            if self.read_port is not None:
                raise ValueError("intervene uses the fixed response-type attachment")
            return
        raise ValueError("action kind must be wait, read, or intervene")


@dataclass(frozen=True)
class DelayedJointGrammar:
    """Finite prefix grammar with delayed structural reads and intervention."""

    delay: int
    exterior_port_count: int

    def __post_init__(self) -> None:
        _validate_nonnegative_integer(self.delay, "delay")
        _validate_positive_integer(self.exterior_port_count, "exterior_port_count")

    @property
    def initial_state(self) -> int:
        return 0

    @property
    def ready_state(self) -> int:
        return self.delay

    @property
    def terminal_state(self) -> int:
        return self.delay + 1

    @property
    def state_count(self) -> int:
        return self.delay + 2

    def validate_state(self, grammar_state: int) -> None:
        if not isinstance(grammar_state, int) or isinstance(grammar_state, bool) or not 0 <= grammar_state < self.state_count:
            raise ValueError("grammar state is outside the delayed joint grammar")

    def legal_actions(self, grammar_state: int) -> tuple[DelayedJointAction, ...]:
        self.validate_state(grammar_state)
        if grammar_state < self.ready_state:
            return (DelayedJointAction.wait(),)
        if grammar_state == self.ready_state:
            return tuple(DelayedJointAction.read(port) for port in range(self.exterior_port_count)) + (
                DelayedJointAction.intervene(),
            )
        return ()

    def transition(self, grammar_state: int, action: DelayedJointAction) -> int:
        self.validate_state(grammar_state)
        if not isinstance(action, DelayedJointAction):
            raise ValueError("action must be a DelayedJointAction")
        action.validate(self.exterior_port_count)
        if grammar_state < self.ready_state and action == DelayedJointAction.wait():
            return grammar_state + 1
        if grammar_state == self.ready_state and action in self.legal_actions(grammar_state):
            return self.terminal_state
        raise ValueError(f"action {action!r} is illegal at grammar state {grammar_state}")

    def normalize_legal_word(
        self,
        word: Iterable[DelayedJointAction],
        start_state: int | None = None,
    ) -> tuple[DelayedJointAction, ...]:
        try:
            normalized = tuple(word)
        except TypeError as error:
            raise ValueError("word must be iterable") from error
        grammar_state = self.initial_state if start_state is None else start_state
        self.validate_state(grammar_state)
        for action in normalized:
            grammar_state = self.transition(grammar_state, action)
        return normalized

    def legal_words_through(
        self,
        horizon: int,
        start_state: int | None = None,
    ) -> tuple[tuple[DelayedJointAction, ...], ...]:
        _validate_nonnegative_integer(horizon, "horizon")
        initial = self.initial_state if start_state is None else start_state
        self.validate_state(initial)
        words: list[tuple[DelayedJointAction, ...]] = [()]
        frontier: list[tuple[int, tuple[DelayedJointAction, ...]]] = [(initial, ())]
        for _ in range(horizon):
            next_frontier: list[tuple[int, tuple[DelayedJointAction, ...]]] = []
            for grammar_state, prefix in frontier:
                for action in self.legal_actions(grammar_state):
                    next_state = self.transition(grammar_state, action)
                    word = prefix + (action,)
                    words.append(word)
                    next_frontier.append((next_state, word))
            frontier = next_frontier
        return tuple(words)

    def revealing_read_word(self, port: int) -> tuple[DelayedJointAction, ...]:
        action = DelayedJointAction.read(port)
        action.validate(self.exterior_port_count)
        word = (DelayedJointAction.wait(),) * self.delay + (action,)
        self.normalize_legal_word(word)
        return word

    @property
    def revealing_intervene_word(self) -> tuple[DelayedJointAction, ...]:
        word = (DelayedJointAction.wait(),) * self.delay + (DelayedJointAction.intervene(),)
        self.normalize_legal_word(word)
        return word

    def verify(self) -> bool:
        try:
            if self.state_count != self.delay + 2:
                return False
            for grammar_state in range(self.ready_state):
                if self.legal_actions(grammar_state) != (DelayedJointAction.wait(),):
                    return False
            expected_ready = tuple(DelayedJointAction.read(port) for port in range(self.exterior_port_count)) + (
                DelayedJointAction.intervene(),
            )
            if self.legal_actions(self.ready_state) != expected_ready:
                return False
            if self.legal_actions(self.terminal_state) != ():
                return False
            if len(self.legal_words_through(self.delay)) != self.delay + 1:
                return False
            return all(len(word) == self.delay + 1 for word in (self.revealing_intervene_word,) + tuple(
                self.revealing_read_word(port) for port in range(self.exterior_port_count)
            ))
        except ValueError:
            return False


@dataclass(frozen=True)
class DelayedJointFamily:
    """Binary joint macro system under one delayed structural grammar."""

    exterior_port_count: int
    delay: int

    def __post_init__(self) -> None:
        _validate_positive_integer(self.exterior_port_count, "exterior_port_count")
        _validate_nonnegative_integer(self.delay, "delay")

    @property
    def grammar(self) -> DelayedJointGrammar:
        return DelayedJointGrammar(self.delay, self.exterior_port_count)

    @property
    def state_count(self) -> int:
        return 2 ** (self.exterior_port_count + 2)

    @property
    def states(self) -> tuple[DelayedJointState, ...]:
        return tuple(product((0, 1), repeat=self.exterior_port_count + 2))

    @property
    def early_horizon(self) -> int:
        return self.delay

    @property
    def first_revealing_horizon(self) -> int:
        return self.delay + 1

    @property
    def early_interface_bits(self) -> float:
        return 1.0

    @property
    def full_interface_bits(self) -> float:
        return float(self.exterior_port_count + 2)

    def validate_state(self, state: DelayedJointState) -> None:
        if not isinstance(state, tuple) or len(state) != self.exterior_port_count + 2:
            raise ValueError("state has the wrong number of binary joint coordinates")
        for index, bit in enumerate(state):
            _validate_bit(bit, f"state[{index}]")

    def output(self, state: DelayedJointState) -> int:
        self.validate_state(state)
        return state[0]

    def exterior_bit(self, state: DelayedJointState, port: int) -> int:
        self.validate_state(state)
        DelayedJointAction.read(port).validate(self.exterior_port_count)
        return state[port + 1]

    def response_type(self, state: DelayedJointState) -> int:
        self.validate_state(state)
        return state[-1]

    def state_transition(self, state: DelayedJointState, action: DelayedJointAction) -> DelayedJointState:
        self.validate_state(state)
        action.validate(self.exterior_port_count)
        y = self.output(state)
        exterior = state[1:-1]
        response = self.response_type(state)
        if action.kind == WAIT:
            return state
        if action.kind == READ:
            assert action.read_port is not None
            return (exterior[action.read_port],) + exterior + (response,)
        if action.kind == INTERVENE:
            return (y ^ response,) + exterior + (response,)
        raise AssertionError("validated action had no state transition")

    def run(
        self,
        state: DelayedJointState,
        word: Iterable[DelayedJointAction],
        start_grammar_state: int | None = None,
    ) -> tuple[DelayedJointState, int]:
        self.validate_state(state)
        normalized = self.grammar.normalize_legal_word(word, start_state=start_grammar_state)
        current_state = state
        grammar_state = self.grammar.initial_state if start_grammar_state is None else start_grammar_state
        for action in normalized:
            current_state = self.state_transition(current_state, action)
            grammar_state = self.grammar.transition(grammar_state, action)
        return current_state, grammar_state

    def trace(self, state: DelayedJointState, word: Iterable[DelayedJointAction]) -> tuple[int, ...]:
        self.validate_state(state)
        normalized = self.grammar.normalize_legal_word(word)
        current_state = state
        grammar_state = self.grammar.initial_state
        values = [self.output(current_state)]
        for action in normalized:
            current_state = self.state_transition(current_state, action)
            grammar_state = self.grammar.transition(grammar_state, action)
            values.append(self.output(current_state))
        return tuple(values)

    def horizon_signature(self, state: DelayedJointState, horizon: int) -> tuple[tuple[tuple[DelayedJointAction, ...], tuple[int, ...]], ...]:
        _validate_nonnegative_integer(horizon, "horizon")
        self.validate_state(state)
        return tuple((word, self.trace(state, word)) for word in self.grammar.legal_words_through(horizon))

    def horizon_labels(self, horizon: int) -> tuple[int, ...]:
        return _canonical_labels(self.horizon_signature(state, horizon) for state in self.states)

    def horizon_partition(self, horizon: int) -> tuple[tuple[int, ...], ...]:
        return _partition_from_labels(self.horizon_labels(horizon))

    def separator_for_pair(self, left: DelayedJointState, right: DelayedJointState) -> "DelayedJointSeparatorCertificate":
        self.validate_state(left)
        self.validate_state(right)
        if left == right:
            raise ValueError("a separator requires two distinct states")
        if left[0] != right[0]:
            reason = "inside"
            word: tuple[DelayedJointAction, ...] = ()
        else:
            differing_port = next(
                (port for port in range(self.exterior_port_count) if self.exterior_bit(left, port) != self.exterior_bit(right, port)),
                None,
            )
            if differing_port is not None:
                reason = "exterior"
                word = self.grammar.revealing_read_word(differing_port)
            else:
                if self.response_type(left) == self.response_type(right):
                    raise AssertionError("distinct binary joint states had no differing coordinate")
                reason = "response"
                word = self.grammar.revealing_intervene_word
        certificate = DelayedJointSeparatorCertificate(self, left, right, reason, word)
        if not certificate.verify():
            raise AssertionError("constructed delayed joint separator did not verify")
        return certificate


@dataclass(frozen=True)
class DelayedJointSeparatorCertificate:
    """Concrete legal word that separates one unequal delayed joint state pair."""

    family: DelayedJointFamily
    left: DelayedJointState
    right: DelayedJointState
    reason: str
    word: tuple[DelayedJointAction, ...]

    @property
    def left_trace(self) -> tuple[int, ...]:
        return self.family.trace(self.left, self.word)

    @property
    def right_trace(self) -> tuple[int, ...]:
        return self.family.trace(self.right, self.word)

    def verify(self) -> bool:
        try:
            self.family.validate_state(self.left)
            self.family.validate_state(self.right)
            if self.left == self.right:
                return False
            normalized = self.family.grammar.normalize_legal_word(self.word)
            if normalized != self.word:
                return False
            if self.reason == "inside":
                if self.left[0] == self.right[0] or self.word != ():
                    return False
            elif self.reason == "exterior":
                if len(self.word) != self.family.first_revealing_horizon:
                    return False
                final = self.word[-1]
                if final.kind != READ or final.read_port is None:
                    return False
                if self.family.exterior_bit(self.left, final.read_port) == self.family.exterior_bit(self.right, final.read_port):
                    return False
            elif self.reason == "response":
                if len(self.word) != self.family.first_revealing_horizon:
                    return False
                if self.word != self.family.grammar.revealing_intervene_word:
                    return False
                if self.left[0] != self.right[0] or self.response_bits_equal():
                    return False
            else:
                return False
            return self.left_trace != self.right_trace
        except (AssertionError, ValueError):
            return False

    def response_bits_equal(self) -> bool:
        return self.family.response_type(self.left) == self.family.response_type(self.right)


@dataclass(frozen=True)
class DelayedJointQuotientJumpCertificate:
    """Exact early/full quotient jump for one delayed joint family member."""

    family: DelayedJointFamily
    early_block_count: int
    full_block_count: int
    first_revealing_horizon: int
    all_pair_separator_count: int

    @property
    def expected_early_block_count(self) -> int:
        return 2

    @property
    def expected_full_block_count(self) -> int:
        return self.family.state_count

    @property
    def expected_separator_count(self) -> int:
        return self.family.state_count * (self.family.state_count - 1) // 2

    def verify(self) -> bool:
        try:
            if not self.family.grammar.verify():
                return False
            if self.first_revealing_horizon != self.family.first_revealing_horizon:
                return False
            if self.early_block_count != len(self.family.horizon_partition(self.family.early_horizon)):
                return False
            if self.full_block_count != len(self.family.horizon_partition(self.first_revealing_horizon)):
                return False
            if self.early_block_count != self.expected_early_block_count:
                return False
            if self.full_block_count != self.expected_full_block_count:
                return False
            if self.all_pair_separator_count != self.expected_separator_count:
                return False
            early_labels = self.family.horizon_labels(self.family.early_horizon)
            for left_index, left in enumerate(self.family.states):
                for right_index in range(left_index + 1, self.family.state_count):
                    right = self.family.states[right_index]
                    if left[0] == right[0] and early_labels[left_index] != early_labels[right_index]:
                        return False
                    if left[0] != right[0] and early_labels[left_index] == early_labels[right_index]:
                        return False
                    if not self.family.separator_for_pair(left, right).verify():
                        return False
            if len(self.family.horizon_partition(self.family.first_revealing_horizon - 1)) != 2:
                return False
            return self.family.full_interface_bits == log2(self.full_block_count)
        except (AssertionError, ValueError):
            return False


def certify_delayed_joint_quotient_jump(
    exterior_port_count: int,
    delay: int,
) -> DelayedJointQuotientJumpCertificate:
    family = DelayedJointFamily(exterior_port_count=exterior_port_count, delay=delay)
    certificate = DelayedJointQuotientJumpCertificate(
        family=family,
        early_block_count=len(family.horizon_partition(family.early_horizon)),
        full_block_count=len(family.horizon_partition(family.first_revealing_horizon)),
        first_revealing_horizon=family.first_revealing_horizon,
        all_pair_separator_count=family.state_count * (family.state_count - 1) // 2,
    )
    if not certificate.verify():
        raise AssertionError("delayed joint quotient-jump certificate did not verify")
    return certificate


@dataclass(frozen=True)
class DelayedJointNoUniformHorizonCertificate:
    """For one proposed horizon, a later joint exterior/type separator exists."""

    proposed_horizon: int
    exterior_port_count: int
    family: DelayedJointFamily
    left: DelayedJointState
    right: DelayedJointState
    exterior_separator: DelayedJointSeparatorCertificate
    response_separator: DelayedJointSeparatorCertificate

    def verify(self) -> bool:
        try:
            _validate_nonnegative_integer(self.proposed_horizon, "proposed_horizon")
            _validate_positive_integer(self.exterior_port_count, "exterior_port_count")
            if self.family != DelayedJointFamily(self.exterior_port_count, self.proposed_horizon):
                return False
            self.family.validate_state(self.left)
            self.family.validate_state(self.right)
            if self.left[0] != self.right[0]:
                return False
            if self.family.horizon_signature(self.left, self.proposed_horizon) != self.family.horizon_signature(
                self.right, self.proposed_horizon
            ):
                return False
            if not self.exterior_separator.verify() or not self.response_separator.verify():
                return False
            if self.exterior_separator.left != self.left or self.exterior_separator.right != self.right:
                return False
            if self.response_separator.left != self.left or self.response_separator.right != self.right:
                return False
            if self.exterior_separator.reason != "exterior" or self.response_separator.reason != "response":
                return False
            if len(self.exterior_separator.word) != self.proposed_horizon + 1:
                return False
            if len(self.response_separator.word) != self.proposed_horizon + 1:
                return False
            return True
        except (AssertionError, ValueError):
            return False


def certify_delayed_joint_no_uniform_horizon(
    exterior_port_count: int,
    proposed_horizon: int,
) -> DelayedJointNoUniformHorizonCertificate:
    _validate_positive_integer(exterior_port_count, "exterior_port_count")
    _validate_nonnegative_integer(proposed_horizon, "proposed_horizon")
    family = DelayedJointFamily(exterior_port_count, proposed_horizon)
    left = (0,) + (0,) * exterior_port_count + (0,)
    right = (0,) + (1,) + (0,) * (exterior_port_count - 1) + (1,)
    certificate = DelayedJointNoUniformHorizonCertificate(
        proposed_horizon=proposed_horizon,
        exterior_port_count=exterior_port_count,
        family=family,
        left=left,
        right=right,
        exterior_separator=family.separator_for_pair(left, right),
        response_separator=DelayedJointSeparatorCertificate(
            family=family,
            left=left,
            right=(0,) + (0,) * exterior_port_count + (1,),
            reason="response",
            word=family.grammar.revealing_intervene_word,
        ),
    )
    if not certificate.verify():
        raise AssertionError("delayed joint no-uniform-horizon certificate did not verify")
    return certificate


def exhaustive_delayed_joint_summary(
    max_exterior_port_count: int,
    max_delay: int,
) -> tuple[DelayedJointQuotientJumpCertificate, ...]:
    _validate_positive_integer(max_exterior_port_count, "max_exterior_port_count")
    _validate_nonnegative_integer(max_delay, "max_delay")
    return tuple(
        certify_delayed_joint_quotient_jump(exterior_port_count, delay)
        for exterior_port_count in range(1, max_exterior_port_count + 1)
        for delay in range(max_delay + 1)
    )
