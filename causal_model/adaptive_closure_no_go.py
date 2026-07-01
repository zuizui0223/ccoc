"""Adaptive finite-experiment no-go for exterior closure.

This module proves a deliberately narrow RACH statement.  A finite adaptive
policy may choose its next action from every prior output, but it has a finite
maximum depth.  Over one constant action alphabet, a delay-gated open system can
be chosen whose exterior effects begin only after that depth.  The policy then
has exactly the same transcript on a closed comparator and on an exterior-open
system, even though the latter has arbitrarily many canonical exterior response
classes.

The theorem concerns *exterior closure* -- a canonical blanket of size one --
not merely existence of a finite blanket.  Each fixed delayed open system below
has a finite blanket; the no-go is uniform across unbounded delay and address
families.

The proof is analytic.  Finite enumeration in certificates replays small
instances of the quantified construction; it is not the proof of the theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from typing import Callable, Iterable

Action = str
Output = int
OutputHistory = tuple[Output, ...]
GateState = tuple[int, tuple[int, ...], int]

TICK: Action = "tick"
BIT0: Action = "bit0"
BIT1: Action = "bit1"
FIRE: Action = "fire"
ACTIONS: tuple[Action, Action, Action, Action] = (TICK, BIT0, BIT1, FIRE)


def _nonnegative(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")


def _positive(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _bit(value: int, name: str) -> None:
    if value not in (0, 1):
        raise ValueError(f"{name} must be 0 or 1")


def _all_binary_histories(length: int) -> tuple[OutputHistory, ...]:
    _positive(length, "history length")
    return tuple(product((0, 1), repeat=length))


def _all_words_through(depth: int) -> tuple[tuple[Action, ...], ...]:
    _nonnegative(depth, "depth")
    return tuple(
        word
        for length in range(depth + 1)
        for word in product(ACTIONS, repeat=length)
    )


@dataclass(frozen=True)
class FiniteAdaptivePolicy:
    """A deterministic binary-output decision tree of fixed maximum depth.

    ``actions_by_history`` is total on every binary output history with lengths
    1 through ``depth``.  The initial output is the first history element.  This
    explicit table makes the policy genuinely adaptive without introducing a
    callable or hidden decision rule into a certificate.
    """

    depth: int
    actions_by_history: tuple[tuple[OutputHistory, Action], ...]

    def __post_init__(self) -> None:
        _nonnegative(self.depth, "depth")
        expected = tuple(history for length in range(1, self.depth + 1) for history in _all_binary_histories(length))
        received = tuple(history for history, _ in self.actions_by_history)
        if received != expected:
            raise ValueError("actions_by_history must be a canonical total binary decision table")
        if any(action not in ACTIONS for _, action in self.actions_by_history):
            raise ValueError("policy actions must belong to the fixed action alphabet")

    @classmethod
    def from_rule(
        cls,
        depth: int,
        rule: Callable[[OutputHistory], Action],
    ) -> "FiniteAdaptivePolicy":
        _nonnegative(depth, "depth")
        entries: list[tuple[OutputHistory, Action]] = []
        for length in range(1, depth + 1):
            for history in _all_binary_histories(length):
                action = rule(history)
                if action not in ACTIONS:
                    raise ValueError("policy rule returned an action outside the fixed alphabet")
                entries.append((history, action))
        return cls(depth=depth, actions_by_history=tuple(entries))

    @classmethod
    def constant(cls, depth: int, action: Action = TICK) -> "FiniteAdaptivePolicy":
        if action not in ACTIONS:
            raise ValueError("constant policy action must belong to the fixed alphabet")
        return cls.from_rule(depth, lambda _history: action)

    def action_for(self, history: OutputHistory) -> Action:
        if not isinstance(history, tuple) or not 1 <= len(history) <= self.depth:
            raise ValueError("history length is outside the policy decision tree")
        for known_history, action in self.actions_by_history:
            if history == known_history:
                return action
        raise AssertionError("validated policy table omitted a reachable binary history")

    def verify(self) -> bool:
        try:
            self.__post_init__()
            return True
        except (TypeError, ValueError):
            return False


@dataclass(frozen=True)
class AdaptiveTranscript:
    """Complete output/action transcript from one finite adaptive experiment."""

    initial_output: Output
    actions: tuple[Action, ...]
    outputs: OutputHistory

    def verify(self) -> bool:
        try:
            _bit(self.initial_output, "initial_output")
            if any(action not in ACTIONS for action in self.actions):
                return False
            if len(self.outputs) != len(self.actions) + 1:
                return False
            if not self.outputs or self.outputs[0] != self.initial_output:
                return False
            return all(output in (0, 1) for output in self.outputs)
        except TypeError:
            return False


@dataclass(frozen=True)
class DelayGatedExteriorSystem:
    """One finite constant-alphabet delayed closed/open comparator.

    Before ``delay`` actions, every action only advances a known protocol phase
    and leaves output unchanged.  Afterwards, a binary address of length
    ``address_bits`` followed by ``fire`` reads one exterior coordinate in the
    open version.  The closed version has the same protocol but ignores exterior
    bits.

    The phase counter and address buffer are known protocol state; blanket
    cardinality is stated on the declared initial phase slice.
    """

    delay: int
    address_bits: int
    exterior_bits: tuple[int, ...]
    is_open: bool
    initial_output: int = 0

    def __post_init__(self) -> None:
        _nonnegative(self.delay, "delay")
        _nonnegative(self.address_bits, "address_bits")
        expected_count = 2 ** self.address_bits
        if not isinstance(self.exterior_bits, tuple) or len(self.exterior_bits) != expected_count:
            raise ValueError("exterior_bits must contain exactly 2**address_bits binary coordinates")
        for index, value in enumerate(self.exterior_bits):
            _bit(value, f"exterior_bits[{index}]")
        if not isinstance(self.is_open, bool):
            raise ValueError("is_open must be boolean")
        _bit(self.initial_output, "initial_output")

    @property
    def exterior_coordinate_count(self) -> int:
        return 2 ** self.address_bits

    @property
    def canonical_blanket_count(self) -> int:
        return 2 ** self.exterior_coordinate_count if self.is_open else 1

    @property
    def initial_state(self) -> GateState:
        return 0, (), self.initial_output

    def validate_state(self, state: GateState) -> None:
        if not isinstance(state, tuple) or len(state) != 3:
            raise ValueError("gate state must be (phase, address_buffer, output)")
        phase, buffer, output = state
        if not isinstance(phase, int) or isinstance(phase, bool) or not 0 <= phase <= self.delay:
            raise ValueError("gate phase is outside range")
        if not isinstance(buffer, tuple) or len(buffer) > self.address_bits:
            raise ValueError("address buffer has invalid length")
        for index, value in enumerate(buffer):
            _bit(value, f"address_buffer[{index}]")
        _bit(output, "state output")

    def address_actions(self, coordinate: int) -> tuple[Action, ...]:
        if not isinstance(coordinate, int) or isinstance(coordinate, bool) or not 0 <= coordinate < self.exterior_coordinate_count:
            raise ValueError("exterior coordinate is outside range")
        text = format(coordinate, f"0{self.address_bits}b")
        return tuple(BIT1 if character == "1" else BIT0 for character in text)

    def read_word(self, coordinate: int) -> tuple[Action, ...]:
        return (TICK,) * self.delay + self.address_actions(coordinate) + (FIRE,)

    def _buffer_coordinate(self, buffer: tuple[int, ...]) -> int:
        if len(buffer) != self.address_bits:
            raise ValueError("address buffer is incomplete")
        value = 0
        for bit in buffer:
            value = 2 * value + bit
        return value

    def step(self, state: GateState, action: Action) -> GateState:
        self.validate_state(state)
        if action not in ACTIONS:
            raise ValueError("action is outside the fixed alphabet")
        phase, buffer, output = state
        if phase < self.delay:
            return phase + 1, (), output
        if action == BIT0 and len(buffer) < self.address_bits:
            return phase, buffer + (0,), output
        if action == BIT1 and len(buffer) < self.address_bits:
            return phase, buffer + (1,), output
        if action == FIRE and len(buffer) == self.address_bits:
            coordinate = self._buffer_coordinate(buffer)
            next_output = self.exterior_bits[coordinate] if self.is_open else output
            return phase, (), next_output
        return phase, buffer, output

    def trace(self, word: Iterable[Action], exterior_bits: tuple[int, ...] | None = None) -> OutputHistory:
        try:
            normalized = tuple(word)
        except TypeError as error:
            raise ValueError("word must be iterable") from error
        if exterior_bits is not None:
            substitute = DelayGatedExteriorSystem(
                delay=self.delay,
                address_bits=self.address_bits,
                exterior_bits=exterior_bits,
                is_open=self.is_open,
                initial_output=self.initial_output,
            )
            return substitute.trace(normalized)
        state = self.initial_state
        outputs = [state[2]]
        for action in normalized:
            state = self.step(state, action)
            outputs.append(state[2])
        return tuple(outputs)

    def run_policy(self, policy: FiniteAdaptivePolicy) -> AdaptiveTranscript:
        if not policy.verify():
            raise ValueError("policy must be valid")
        state = self.initial_state
        outputs: list[int] = [state[2]]
        actions: list[Action] = []
        for _ in range(policy.depth):
            action = policy.action_for(tuple(outputs))
            state = self.step(state, action)
            actions.append(action)
            outputs.append(state[2])
        transcript = AdaptiveTranscript(
            initial_output=self.initial_output,
            actions=tuple(actions),
            outputs=tuple(outputs),
        )
        if not transcript.verify():
            raise AssertionError("adaptive transcript did not verify")
        return transcript

    def verify(self) -> bool:
        try:
            self.__post_init__()
            for coordinate in range(self.exterior_coordinate_count):
                word = self.read_word(coordinate)
                if any(action not in ACTIONS for action in word):
                    return False
            return True
        except (TypeError, ValueError):
            return False


def closed_open_delayed_pair(delay: int, address_bits: int) -> tuple[DelayGatedExteriorSystem, DelayGatedExteriorSystem]:
    """A closed/open pair with same protocol and an open future separator at port 0."""
    _nonnegative(delay, "delay")
    _nonnegative(address_bits, "address_bits")
    coordinate_count = 2 ** address_bits
    actual_open_bits = (1,) + (0,) * (coordinate_count - 1)
    closed = DelayGatedExteriorSystem(
        delay=delay,
        address_bits=address_bits,
        exterior_bits=actual_open_bits,
        is_open=False,
        initial_output=0,
    )
    open_system = DelayGatedExteriorSystem(
        delay=delay,
        address_bits=address_bits,
        exterior_bits=actual_open_bits,
        is_open=True,
        initial_output=0,
    )
    return closed, open_system


@dataclass(frozen=True)
class CanonicalBlanketCardinalityCertificate:
    """Exact blanket cardinalities on the declared initial phase slice."""

    system: DelayGatedExteriorSystem
    claimed_blanket_count: int
    all_exterior_states_separated: bool

    def verify(self) -> bool:
        try:
            if not self.system.verify() or self.claimed_blanket_count != self.system.canonical_blanket_count:
                return False
            exterior_states = tuple(product((0, 1), repeat=self.system.exterior_coordinate_count))
            if not self.system.is_open:
                reference = self.system.trace((), exterior_states[0])
                # Closed transition is exterior-independent by construction; one
                # representative read at every port guards that implementation.
                for exterior in exterior_states:
                    for coordinate in range(self.system.exterior_coordinate_count):
                        if self.system.trace(self.system.read_word(coordinate), exterior) != self.system.trace(
                            self.system.read_word(coordinate), exterior_states[0]
                        ):
                            return False
                return self.claimed_blanket_count == 1 and not self.all_exterior_states_separated and reference == (0,)
            pairwise_separated = True
            for left, right in combinations(exterior_states, 2):
                differing = next(
                    index
                    for index in range(self.system.exterior_coordinate_count)
                    if left[index] != right[index]
                )
                if self.system.trace(self.system.read_word(differing), left) == self.system.trace(
                    self.system.read_word(differing), right
                ):
                    pairwise_separated = False
                    break
            return (
                self.claimed_blanket_count == len(exterior_states)
                and self.all_exterior_states_separated == pairwise_separated
                and pairwise_separated
            )
        except (StopIteration, TypeError, ValueError):
            return False


def certify_canonical_blanket_cardinality(system: DelayGatedExteriorSystem) -> CanonicalBlanketCardinalityCertificate:
    certificate = CanonicalBlanketCardinalityCertificate(
        system=system,
        claimed_blanket_count=system.canonical_blanket_count,
        all_exterior_states_separated=system.is_open,
    )
    if not certificate.verify():
        raise AssertionError("canonical blanket cardinality certificate did not verify")
    return certificate


@dataclass(frozen=True)
class PolicyLiftingCertificate:
    """Finite replay of the policy-lifting lemma for a chosen pair and depth."""

    policy: FiniteAdaptivePolicy
    left: DelayGatedExteriorSystem
    right: DelayGatedExteriorSystem
    common_prefix_depth: int
    all_word_prefix_agreement: bool
    left_transcript: AdaptiveTranscript
    right_transcript: AdaptiveTranscript

    def verify(self) -> bool:
        try:
            if not self.policy.verify() or not self.left.verify() or not self.right.verify():
                return False
            _nonnegative(self.common_prefix_depth, "common_prefix_depth")
            if self.common_prefix_depth < self.policy.depth:
                return False
            agreement = all(
                self.left.trace(word) == self.right.trace(word)
                for word in _all_words_through(self.common_prefix_depth)
            )
            if self.all_word_prefix_agreement != agreement or not agreement:
                return False
            left_transcript = self.left.run_policy(self.policy)
            right_transcript = self.right.run_policy(self.policy)
            return (
                self.left_transcript == left_transcript
                and self.right_transcript == right_transcript
                and left_transcript == right_transcript
            )
        except (TypeError, ValueError):
            return False


def certify_policy_lifting(
    policy: FiniteAdaptivePolicy,
    left: DelayGatedExteriorSystem,
    right: DelayGatedExteriorSystem,
    common_prefix_depth: int,
) -> PolicyLiftingCertificate:
    certificate = PolicyLiftingCertificate(
        policy=policy,
        left=left,
        right=right,
        common_prefix_depth=common_prefix_depth,
        all_word_prefix_agreement=all(
            left.trace(word) == right.trace(word)
            for word in _all_words_through(common_prefix_depth)
        ),
        left_transcript=left.run_policy(policy),
        right_transcript=right.run_policy(policy),
    )
    if not certificate.verify():
        raise AssertionError("policy lifting certificate did not verify")
    return certificate


@dataclass(frozen=True)
class AdaptiveClosureNoGoCertificate:
    """One finite policy cannot distinguish closed from delayed exterior-open behavior."""

    policy: FiniteAdaptivePolicy
    delay: int
    address_bits: int
    closed_system: DelayGatedExteriorSystem
    open_system: DelayGatedExteriorSystem
    policy_lifting: PolicyLiftingCertificate
    closed_blanket: CanonicalBlanketCardinalityCertificate
    open_blanket: CanonicalBlanketCardinalityCertificate
    future_separator_word: tuple[Action, ...]

    @property
    def open_blanket_count(self) -> int:
        return self.open_blanket.claimed_blanket_count

    def verify(self) -> bool:
        try:
            if not self.policy.verify():
                return False
            _nonnegative(self.delay, "delay")
            _nonnegative(self.address_bits, "address_bits")
            expected_closed, expected_open = closed_open_delayed_pair(self.delay, self.address_bits)
            if self.closed_system != expected_closed or self.open_system != expected_open:
                return False
            if self.delay <= self.policy.depth:
                return False
            if not self.policy_lifting.verify() or self.policy_lifting.policy != self.policy:
                return False
            if self.policy_lifting.left != self.closed_system or self.policy_lifting.right != self.open_system:
                return False
            if self.policy_lifting.common_prefix_depth != self.policy.depth:
                return False
            if not self.closed_blanket.verify() or not self.open_blanket.verify():
                return False
            if self.closed_blanket.system != self.closed_system or self.open_blanket.system != self.open_system:
                return False
            if self.closed_blanket.claimed_blanket_count != 1:
                return False
            if self.open_blanket.claimed_blanket_count != 2 ** (2 ** self.address_bits):
                return False
            expected_word = self.open_system.read_word(0)
            if self.future_separator_word != expected_word or len(expected_word) <= self.policy.depth:
                return False
            return self.closed_system.trace(expected_word) != self.open_system.trace(expected_word)
        except (TypeError, ValueError):
            return False


def certify_adaptive_closure_no_go(
    policy: FiniteAdaptivePolicy,
    address_bits: int = 1,
) -> AdaptiveClosureNoGoCertificate:
    """Construct a delayed closed/open pair invisible to one finite policy."""
    if not policy.verify():
        raise ValueError("policy must be valid")
    _nonnegative(address_bits, "address_bits")
    delay = policy.depth + 1
    closed, open_system = closed_open_delayed_pair(delay, address_bits)
    certificate = AdaptiveClosureNoGoCertificate(
        policy=policy,
        delay=delay,
        address_bits=address_bits,
        closed_system=closed,
        open_system=open_system,
        policy_lifting=certify_policy_lifting(policy, closed, open_system, policy.depth),
        closed_blanket=certify_canonical_blanket_cardinality(closed),
        open_blanket=certify_canonical_blanket_cardinality(open_system),
        future_separator_word=open_system.read_word(0),
    )
    if not certificate.verify():
        raise AssertionError("adaptive closure no-go certificate did not verify")
    return certificate


def address_bits_exceeding_upper_bound(upper_bound: int) -> int:
    """Smallest ell with 2**(2**ell) greater than a proposed finite bound."""
    _positive(upper_bound, "upper_bound")
    address_bits = 0
    while 2 ** (2 ** address_bits) <= upper_bound:
        address_bits += 1
    return address_bits


@dataclass(frozen=True)
class TranscriptUpperBoundRefutationCertificate:
    """A finite policy transcript is compatible with a blanket larger than U."""

    proposed_upper_bound: int
    no_go: AdaptiveClosureNoGoCertificate

    def verify(self) -> bool:
        try:
            _positive(self.proposed_upper_bound, "proposed_upper_bound")
            return self.no_go.verify() and self.no_go.open_blanket_count > self.proposed_upper_bound
        except (TypeError, ValueError):
            return False


def certify_transcript_upper_bound_refutation(
    policy: FiniteAdaptivePolicy,
    proposed_upper_bound: int,
) -> TranscriptUpperBoundRefutationCertificate:
    """Refute any finite transcript-only blanket upper certificate for one policy."""
    address_bits = address_bits_exceeding_upper_bound(proposed_upper_bound)
    certificate = TranscriptUpperBoundRefutationCertificate(
        proposed_upper_bound=proposed_upper_bound,
        no_go=certify_adaptive_closure_no_go(policy, address_bits),
    )
    if not certificate.verify():
        raise AssertionError("transcript upper-bound refutation did not verify")
    return certificate


def exhaustive_adaptive_no_go_summary(
    max_policy_depth: int,
    max_address_bits: int,
) -> tuple[AdaptiveClosureNoGoCertificate, ...]:
    """Deterministic finite replay of representative adaptive policies."""
    _nonnegative(max_policy_depth, "max_policy_depth")
    _nonnegative(max_address_bits, "max_address_bits")
    certificates: list[AdaptiveClosureNoGoCertificate] = []
    for depth in range(max_policy_depth + 1):
        policies = (
            FiniteAdaptivePolicy.constant(depth, TICK),
            FiniteAdaptivePolicy.from_rule(depth, lambda history: BIT1 if history[-1] else FIRE),
        )
        for policy in policies:
            for address_bits in range(max_address_bits + 1):
                certificates.append(certify_adaptive_closure_no_go(policy, address_bits))
    return tuple(certificates)
