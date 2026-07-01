"""Exact finite witness for observation-window completion and counterfactual inflation.

The active window observes only a focal output bit ``y``.  The exterior contains
``m`` dormant binary completion bits ``b_i``.  Passive observation actions never
expose those completion bits, whereas a declared future boundary action
``probe:i`` can expose ``b_i`` at the focal output.

This gives a deliberately narrow but exact theorem family:

* every finite passive observation word has the same window trace for many
  distinct exterior completions;
* the same completions can be separated by one admissible counterfactual
  boundary action; and
* the minimal interface safe for the declared open grammar has ``m`` more bits
  than the passive-observation interface.

The coordinate witness is linked to the existing constant-grammar,
bounded-degree relay-tree compilation.  The theorem does *not* claim that every
finite empirical observation fails to certify closure under every possible model
class.  It proves that passive traces alone do not certify closure in this
explicit, bounded-degree family unless a boundary contract is added.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from math import log2
from typing import Iterable

from .extension_compression import (
    IDLE,
    OBSERVE,
    Action,
    State,
    all_states,
    focal_output,
    open_actions,
    open_partition,
    output_trace,
    partition_by_signature,
    probe_action,
    transition,
)
from .relay_tree_compilation import (
    RelayTreeTopology,
    certify_bounded_degree_compilation,
    is_quiescent,
    micro_step,
    one_token_relay_grammar,
    quiescent_configuration,
    run_macro_probe,
)

PassiveWord = tuple[Action, ...]
PASSIVE_ACTIONS: tuple[Action, Action] = (OBSERVE, IDLE)


def _validate_module_count(module_count: int) -> None:
    if not isinstance(module_count, int) or isinstance(module_count, bool) or module_count < 1:
        raise ValueError("module_count must be a positive integer")


def _validate_horizon(horizon: int) -> None:
    if not isinstance(horizon, int) or isinstance(horizon, bool) or horizon < 0:
        raise ValueError("horizon must be a non-negative integer")


def _validate_passive_word(word: PassiveWord | Iterable[Action]) -> PassiveWord:
    try:
        normalized = tuple(word)
    except TypeError as error:
        raise ValueError("passive word must be an iterable of actions") from error
    if any(action not in PASSIVE_ACTIONS for action in normalized):
        raise ValueError("passive words may contain only observe and idle actions")
    return normalized


def passive_words_through(horizon: int) -> tuple[PassiveWord, ...]:
    """Enumerate all declared passive action words of length at most ``horizon``."""
    _validate_horizon(horizon)
    return tuple(
        word
        for length in range(horizon + 1)
        for word in product(PASSIVE_ACTIONS, repeat=length)
    )


def passive_window_trace(module_count: int, state: State, word: PassiveWord | Iterable[Action]) -> tuple[int, ...]:
    """Return the focal trace seen by the finite window under a passive protocol."""
    _validate_module_count(module_count)
    normalized = _validate_passive_word(word)
    current = state
    trace = [focal_output(module_count, current)]
    for action in normalized:
        current = transition(module_count, current, action)
        trace.append(focal_output(module_count, current))
    return tuple(trace)


def passive_window_signature(module_count: int, state: State) -> tuple[int]:
    """Coarsest passive signature: only the current focal output is visible."""
    return (focal_output(module_count, state),)


def passive_window_partition(module_count: int) -> tuple[tuple[State, ...], ...]:
    """Partition states by all passive future traces in this witness family."""
    _validate_module_count(module_count)
    return partition_by_signature(
        module_count,
        {state: passive_window_signature(module_count, state) for state in all_states(module_count)},
    )


def is_passive_window_partition_sound(module_count: int) -> bool:
    """Check that equal passive signatures preserve every declared passive trace."""
    _validate_module_count(module_count)
    states = all_states(module_count)
    for left, right in combinations(states, 2):
        if passive_window_signature(module_count, left) != passive_window_signature(module_count, right):
            continue
        for action in PASSIVE_ACTIONS:
            if output_trace(module_count, left, action) != output_trace(module_count, right, action):
                return False
            left_next = transition(module_count, left, action)
            right_next = transition(module_count, right, action)
            if passive_window_signature(module_count, left_next) != passive_window_signature(module_count, right_next):
                return False
    return True


@dataclass(frozen=True)
class CounterfactualCompletionCertificate:
    """Two passive-indistinguishable completions separated by a boundary action."""

    module_count: int
    passive_word: PassiveWord
    left_completion: State
    right_completion: State
    boundary_action: Action
    left_passive_trace: tuple[int, ...]
    right_passive_trace: tuple[int, ...]
    left_counterfactual_trace: tuple[int, ...]
    right_counterfactual_trace: tuple[int, ...]

    @property
    def port(self) -> int:
        if not self.boundary_action.startswith("probe:"):
            raise ValueError("certificate boundary action is not a probe")
        return int(self.boundary_action.split(":", 1)[1])

    def verify(self) -> bool:
        try:
            _validate_module_count(self.module_count)
            word = _validate_passive_word(self.passive_word)
            if self.left_completion == self.right_completion:
                return False
            if focal_output(self.module_count, self.left_completion) != focal_output(self.module_count, self.right_completion):
                return False
            if self.boundary_action not in open_actions(self.module_count):
                return False
            if self.boundary_action in PASSIVE_ACTIONS:
                return False
            if self.left_passive_trace != passive_window_trace(self.module_count, self.left_completion, word):
                return False
            if self.right_passive_trace != passive_window_trace(self.module_count, self.right_completion, word):
                return False
            if self.left_passive_trace != self.right_passive_trace:
                return False
            if self.left_counterfactual_trace != output_trace(
                self.module_count,
                self.left_completion,
                self.boundary_action,
            ):
                return False
            if self.right_counterfactual_trace != output_trace(
                self.module_count,
                self.right_completion,
                self.boundary_action,
            ):
                return False
            return self.left_counterfactual_trace != self.right_counterfactual_trace
        except (TypeError, ValueError):
            return False


def completion_counterexample_certificate(
    module_count: int,
    passive_word: PassiveWord | Iterable[Action],
    port: int,
    focal_bit: int = 0,
) -> CounterfactualCompletionCertificate:
    """Construct a counterfactual completion pair for any passive protocol.

    Both worlds have the same window state ``y``.  They differ only in one
    exterior completion bit, which remains invisible under every passive word
    and is revealed by the declared future boundary action ``probe:port``.
    """
    _validate_module_count(module_count)
    word = _validate_passive_word(passive_word)
    if focal_bit not in (0, 1):
        raise ValueError("focal_bit must be 0 or 1")
    if not isinstance(port, int) or isinstance(port, bool) or not 0 <= port < module_count:
        raise ValueError(f"port must be an integer in [0, {module_count - 1}]")

    left_bits = [0] * module_count
    right_bits = [0] * module_count
    right_bits[port] = 1
    left = (focal_bit,) + tuple(left_bits)
    right = (focal_bit,) + tuple(right_bits)
    action = probe_action(port)
    certificate = CounterfactualCompletionCertificate(
        module_count=module_count,
        passive_word=word,
        left_completion=left,
        right_completion=right,
        boundary_action=action,
        left_passive_trace=passive_window_trace(module_count, left, word),
        right_passive_trace=passive_window_trace(module_count, right, word),
        left_counterfactual_trace=output_trace(module_count, left, action),
        right_counterfactual_trace=output_trace(module_count, right, action),
    )
    if not certificate.verify():
        raise AssertionError("counterfactual completion certificate did not verify")
    return certificate


@dataclass(frozen=True)
class RelayCompletionCertificate:
    """Bounded-degree relay implementation of one window-completion counterexample."""

    module_count: int
    passive_microticks: int
    port: int
    left_initial_bits: tuple[int, ...]
    right_initial_bits: tuple[int, ...]
    left_passive_trace: tuple[int, ...]
    right_passive_trace: tuple[int, ...]
    left_counterfactual_output: int
    right_counterfactual_output: int

    def verify(self) -> bool:
        try:
            _validate_module_count(self.module_count)
            _validate_horizon(self.passive_microticks)
            if not isinstance(self.port, int) or isinstance(self.port, bool) or not 0 <= self.port < self.module_count:
                return False
            if len(self.left_initial_bits) != self.module_count or len(self.right_initial_bits) != self.module_count:
                return False
            if any(bit not in (0, 1) for bit in self.left_initial_bits + self.right_initial_bits):
                return False
            if self.left_initial_bits[self.port] == self.right_initial_bits[self.port]:
                return False
            topology = RelayTreeTopology.balanced(self.module_count)
            grammar = one_token_relay_grammar()
            if not topology.verify() or not grammar.verify():
                return False
            if topology.maximum_degree_with_reader(self.port) > grammar.maximum_degree:
                return False
            left = quiescent_configuration(topology, 0, self.left_initial_bits)
            right = quiescent_configuration(topology, 0, self.right_initial_bits)
            left_trace = [left.focal_output]
            right_trace = [right.focal_output]
            for _ in range(self.passive_microticks):
                left = micro_step(topology, left)
                right = micro_step(topology, right)
                left_trace.append(left.focal_output)
                right_trace.append(right.focal_output)
            if not is_quiescent(topology, left) or not is_quiescent(topology, right):
                return False
            if tuple(left_trace) != self.left_passive_trace or tuple(right_trace) != self.right_passive_trace:
                return False
            if self.left_passive_trace != self.right_passive_trace:
                return False
            left_final = run_macro_probe(topology, left, self.port)
            right_final = run_macro_probe(topology, right, self.port)
            if left_final.focal_output != self.left_counterfactual_output:
                return False
            if right_final.focal_output != self.right_counterfactual_output:
                return False
            return self.left_counterfactual_output != self.right_counterfactual_output
        except (AssertionError, KeyError, ValueError):
            return False


def relay_completion_certificate(
    module_count: int,
    passive_microticks: int,
    port: int,
) -> RelayCompletionCertificate:
    """Construct the degree-three relay certificate for a hidden external bit."""
    _validate_module_count(module_count)
    _validate_horizon(passive_microticks)
    if not isinstance(port, int) or isinstance(port, bool) or not 0 <= port < module_count:
        raise ValueError(f"port must be an integer in [0, {module_count - 1}]")
    left_bits = (0,) * module_count
    right_bits_list = [0] * module_count
    right_bits_list[port] = 1
    right_bits = tuple(right_bits_list)
    topology = RelayTreeTopology.balanced(module_count)
    left = quiescent_configuration(topology, 0, left_bits)
    right = quiescent_configuration(topology, 0, right_bits)
    left_trace = [left.focal_output]
    right_trace = [right.focal_output]
    for _ in range(passive_microticks):
        left = micro_step(topology, left)
        right = micro_step(topology, right)
        left_trace.append(left.focal_output)
        right_trace.append(right.focal_output)
    left_final = run_macro_probe(topology, left, port)
    right_final = run_macro_probe(topology, right, port)
    certificate = RelayCompletionCertificate(
        module_count=module_count,
        passive_microticks=passive_microticks,
        port=port,
        left_initial_bits=left_bits,
        right_initial_bits=right_bits,
        left_passive_trace=tuple(left_trace),
        right_passive_trace=tuple(right_trace),
        left_counterfactual_output=left_final.focal_output,
        right_counterfactual_output=right_final.focal_output,
    )
    if not certificate.verify():
        raise AssertionError("relay completion certificate did not verify")
    return certificate


@dataclass(frozen=True)
class ObservationWindowCompletionCertificate:
    """Exact certificate for passive indistinguishability and open inflation.

    The passive window observes only the focal bit, giving two interface states.
    The open grammar can later probe any external completion bit, making every
    coordinate state distinguishable.
    """

    module_count: int
    passive_horizon_checked: int
    passive_block_count: int
    open_block_count: int
    checked_counterfactual_certificates: int

    @property
    def passive_interface_bits(self) -> int:
        return int(log2(self.passive_block_count))

    @property
    def open_interface_bits(self) -> int:
        return int(log2(self.open_block_count))

    @property
    def counterfactual_inflation_bits(self) -> int:
        return self.open_interface_bits - self.passive_interface_bits

    @property
    def hidden_completion_count_per_window_value(self) -> int:
        return 2 ** self.module_count

    @property
    def expected_checked_counterfactual_certificates(self) -> int:
        return 2 * self.module_count * len(passive_words_through(self.passive_horizon_checked))

    def verify(self) -> bool:
        try:
            _validate_module_count(self.module_count)
            _validate_horizon(self.passive_horizon_checked)
            if self.passive_block_count != 2:
                return False
            if self.open_block_count != 2 ** (self.module_count + 1):
                return False
            if self.passive_interface_bits != 1:
                return False
            if self.open_interface_bits != self.module_count + 1:
                return False
            if self.counterfactual_inflation_bits != self.module_count:
                return False
            if self.checked_counterfactual_certificates != self.expected_checked_counterfactual_certificates:
                return False
            if len(passive_window_partition(self.module_count)) != self.passive_block_count:
                return False
            if not is_passive_window_partition_sound(self.module_count):
                return False
            if len(open_partition(self.module_count)) != self.open_block_count:
                return False
            if any(len(block) != 1 for block in open_partition(self.module_count)):
                return False
            for word in passive_words_through(self.passive_horizon_checked):
                for focal_bit in (0, 1):
                    for port in range(self.module_count):
                        if not completion_counterexample_certificate(
                            self.module_count,
                            word,
                            port,
                            focal_bit,
                        ).verify():
                            return False
            for port in range(self.module_count):
                if not relay_completion_certificate(
                    self.module_count,
                    self.passive_horizon_checked,
                    port,
                ).verify():
                    return False
            if not certify_bounded_degree_compilation(self.module_count).verify():
                return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_observation_window_completion(
    module_count: int,
    passive_horizon_checked: int = 6,
) -> ObservationWindowCompletionCertificate:
    """Certify the finite observation-window completion theorem family.

    The theorem statement is:

    ``K_passive = 1`` and ``K_open = m + 1``.

    The finite horizon in the certificate is a regression enumeration.  The
    written proof establishes passive indistinguishability for every finite
    passive word because both passive actions leave the focal bit unchanged.
    """
    _validate_module_count(module_count)
    _validate_horizon(passive_horizon_checked)
    certificate = ObservationWindowCompletionCertificate(
        module_count=module_count,
        passive_horizon_checked=passive_horizon_checked,
        passive_block_count=len(passive_window_partition(module_count)),
        open_block_count=len(open_partition(module_count)),
        checked_counterfactual_certificates=(
            2 * module_count * len(passive_words_through(passive_horizon_checked))
        ),
    )
    if not certificate.verify():
        raise AssertionError("observation-window completion certificate did not verify")
    return certificate


def exhaustive_observation_window_summary(
    max_module_count: int = 6,
    passive_horizon_checked: int = 6,
) -> tuple[ObservationWindowCompletionCertificate, ...]:
    """Verify the explicit completion family over a declared finite size range."""
    _validate_module_count(max_module_count)
    _validate_horizon(passive_horizon_checked)
    return tuple(
        certify_observation_window_completion(module_count, passive_horizon_checked)
        for module_count in range(1, max_module_count + 1)
    )
