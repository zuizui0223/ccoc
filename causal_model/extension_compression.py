"""Exact finite witness for extension--compression noncommutation.

The theorem domain is deliberately narrow. A system has one focal output bit and
``m`` dormant boundary-memory bits. In a closed context only one declared port
can be probed; in the open context any declared port may be probed later.

For every fixed closed port, the coarsest exact causal interface has four states.
Across the open port grammar, every microstate is causally distinguishable.
This module proves that separation with explicit one-step trace witnesses.

This is an interface-level theorem. It does not yet compile the witness to a
bounded-degree local graph grammar, and it does not claim that a real ecosystem
is literally this finite system.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from math import log2
from typing import Mapping

State = tuple[int, ...]
Action = str

OBSERVE: Action = "observe"
IDLE: Action = "idle"


def _validate_module_count(module_count: int) -> None:
    if not isinstance(module_count, int) or isinstance(module_count, bool) or module_count < 1:
        raise ValueError("module_count must be a positive integer")


def _validate_state(module_count: int, state: State) -> None:
    _validate_module_count(module_count)
    if not isinstance(state, tuple) or len(state) != module_count + 1:
        raise ValueError("state must have focal output plus one bit per module")
    if any(bit not in (0, 1) for bit in state):
        raise ValueError("every state coordinate must be 0 or 1")


def probe_action(port: int) -> Action:
    if not isinstance(port, int) or isinstance(port, bool) or port < 0:
        raise ValueError("port must be a non-negative integer")
    return f"probe:{port}"


def _parse_probe_action(module_count: int, action: Action) -> int | None:
    if action in {OBSERVE, IDLE}:
        return None
    if not isinstance(action, str) or not action.startswith("probe:"):
        raise ValueError(f"unknown action: {action!r}")
    suffix = action.split(":", 1)[1]
    try:
        port = int(suffix)
    except ValueError as error:
        raise ValueError(f"invalid probe action: {action!r}") from error
    if not 0 <= port < module_count:
        raise ValueError(f"probe port {port} is outside [0, {module_count - 1}]")
    return port


def all_states(module_count: int) -> tuple[State, ...]:
    """Return the complete finite microstate space ``{0,1}^{m+1}``."""
    _validate_module_count(module_count)
    return tuple(tuple(bits) for bits in product((0, 1), repeat=module_count + 1))


def focal_output(module_count: int, state: State) -> int:
    _validate_state(module_count, state)
    return state[0]


def transition(module_count: int, state: State, action: Action) -> State:
    """Apply an observation, idle step, or an allowed port probe.

    ``probe:i`` copies dormant bit ``b_i`` into the focal outcome. All dormant
    bits remain unchanged. ``observe`` and ``idle`` leave the state unchanged.
    """
    _validate_state(module_count, state)
    port = _parse_probe_action(module_count, action)
    if port is None:
        return state
    return (state[port + 1],) + state[1:]


def output_trace(module_count: int, state: State, action: Action) -> tuple[int, ...]:
    """Return the focal-output trace before and after one declared action."""
    _validate_state(module_count, state)
    if action == OBSERVE:
        return (state[0],)
    successor = transition(module_count, state, action)
    return (state[0], successor[0])


def closed_actions(module_count: int, port: int) -> tuple[Action, ...]:
    """Actions allowed by the closed context whose only reachable port is ``port``."""
    _validate_module_count(module_count)
    _parse_probe_action(module_count, probe_action(port))
    return (OBSERVE, IDLE, probe_action(port))


def open_actions(module_count: int) -> tuple[Action, ...]:
    """Actions allowed by the declared open port grammar."""
    _validate_module_count(module_count)
    return (OBSERVE, IDLE) + tuple(probe_action(port) for port in range(module_count))


def closed_interface_signature(module_count: int, port: int, state: State) -> tuple[int, int]:
    """The four-state exact interface for a context closed at one port."""
    _validate_state(module_count, state)
    _parse_probe_action(module_count, probe_action(port))
    return (state[0], state[port + 1])


def open_trace_signature(module_count: int, state: State) -> tuple[int, ...]:
    """All outputs that an admissible future attachment can expose in one step."""
    _validate_state(module_count, state)
    return (state[0],) + tuple(
        output_trace(module_count, state, probe_action(port))[-1]
        for port in range(module_count)
    )


def partition_by_signature(
    module_count: int,
    signatures: Mapping[State, tuple[int, ...] | tuple[int, int]],
) -> tuple[tuple[State, ...], ...]:
    """Canonical partition representation, sorted only for deterministic tests."""
    _validate_module_count(module_count)
    buckets: dict[tuple[int, ...] | tuple[int, int], list[State]] = {}
    for state in all_states(module_count):
        try:
            signature = signatures[state]
        except KeyError as error:
            raise ValueError("signatures must cover the full state space") from error
        buckets.setdefault(signature, []).append(state)
    return tuple(sorted((tuple(states) for states in buckets.values()), key=lambda block: block[0]))


def closed_partition(module_count: int, port: int) -> tuple[tuple[State, ...], ...]:
    return partition_by_signature(
        module_count,
        {state: closed_interface_signature(module_count, port, state) for state in all_states(module_count)},
    )


def open_partition(module_count: int) -> tuple[tuple[State, ...], ...]:
    return partition_by_signature(
        module_count,
        {state: open_trace_signature(module_count, state) for state in all_states(module_count)},
    )


def is_closed_partition_sound(module_count: int, port: int) -> bool:
    """Check output and quotient-transition preservation for the four-state interface."""
    states = all_states(module_count)
    for left, right in combinations(states, 2):
        if closed_interface_signature(module_count, port, left) != closed_interface_signature(module_count, port, right):
            continue
        for action in closed_actions(module_count, port):
            if output_trace(module_count, left, action) != output_trace(module_count, right, action):
                return False
            left_next = transition(module_count, left, action)
            right_next = transition(module_count, right, action)
            if closed_interface_signature(module_count, port, left_next) != closed_interface_signature(module_count, port, right_next):
                return False
    return True


@dataclass(frozen=True)
class TraceSeparationCertificate:
    """A one-step action witness that two open-interface states cannot be merged."""

    module_count: int
    left: State
    right: State
    action: Action
    left_trace: tuple[int, ...]
    right_trace: tuple[int, ...]

    def verify(self) -> bool:
        try:
            _validate_state(self.module_count, self.left)
            _validate_state(self.module_count, self.right)
            if self.left == self.right or self.action not in open_actions(self.module_count):
                return False
            return (
                self.left_trace == output_trace(self.module_count, self.left, self.action)
                and self.right_trace == output_trace(self.module_count, self.right, self.action)
                and self.left_trace != self.right_trace
            )
        except ValueError:
            return False


def separating_trace_certificate(
    module_count: int,
    left: State,
    right: State,
) -> TraceSeparationCertificate:
    """Construct the exact open-port action that separates any distinct states."""
    _validate_state(module_count, left)
    _validate_state(module_count, right)
    if left == right:
        raise ValueError("a separation certificate requires two distinct states")
    if left[0] != right[0]:
        action = OBSERVE
    else:
        differing_ports = [port for port in range(module_count) if left[port + 1] != right[port + 1]]
        if not differing_ports:
            raise AssertionError("distinct binary states must differ in a focal coordinate or a port bit")
        action = probe_action(differing_ports[0])
    certificate = TraceSeparationCertificate(
        module_count=module_count,
        left=left,
        right=right,
        action=action,
        left_trace=output_trace(module_count, left, action),
        right_trace=output_trace(module_count, right, action),
    )
    if not certificate.verify():
        raise AssertionError("constructed separation certificate did not verify")
    return certificate


@dataclass(frozen=True)
class ExtensionCompressionCertificate:
    """Exact finite certificate for the ``2`` versus ``m+1`` interface separation."""

    module_count: int
    closed_block_counts: tuple[int, ...]
    open_block_count: int

    @property
    def closed_interface_bits(self) -> tuple[int, ...]:
        return tuple(int(log2(count)) for count in self.closed_block_counts)

    @property
    def open_interface_bits(self) -> int:
        return int(log2(self.open_block_count))

    @property
    def microstate_count(self) -> int:
        return 2 ** (self.module_count + 1)

    def verify(self) -> bool:
        try:
            _validate_module_count(self.module_count)
            if self.closed_block_counts != tuple(4 for _ in range(self.module_count)):
                return False
            if self.open_block_count != self.microstate_count:
                return False
            if self.closed_interface_bits != tuple(2 for _ in range(self.module_count)):
                return False
            if self.open_interface_bits != self.module_count + 1:
                return False
            for port in range(self.module_count):
                if not is_closed_partition_sound(self.module_count, port):
                    return False
                if len(closed_partition(self.module_count, port)) != 4:
                    return False
            if any(len(block) != 1 for block in open_partition(self.module_count)):
                return False
            for left, right in combinations(all_states(self.module_count), 2):
                if not separating_trace_certificate(self.module_count, left, right).verify():
                    return False
            return True
        except (ValueError, AssertionError):
            return False


def certify_extension_compression(module_count: int) -> ExtensionCompressionCertificate:
    """Build the theorem certificate for the declared finite witness family.

    The certificate states the exact separation

    ``max_i kappa(M_m || E_i) = 2`` and
    ``kappa_open(M_m; E_m) = m + 1``.
    """
    _validate_module_count(module_count)
    certificate = ExtensionCompressionCertificate(
        module_count=module_count,
        closed_block_counts=tuple(len(closed_partition(module_count, port)) for port in range(module_count)),
        open_block_count=len(open_partition(module_count)),
    )
    if not certificate.verify():
        raise AssertionError("extension--compression witness certificate did not verify")
    return certificate


def exhaustive_witness_summary(max_module_count: int = 6) -> tuple[ExtensionCompressionCertificate, ...]:
    """Verify every member of the explicit witness family up to a finite port bound."""
    if not isinstance(max_module_count, int) or isinstance(max_module_count, bool) or max_module_count < 1:
        raise ValueError("max_module_count must be a positive integer")
    return tuple(certify_extension_compression(module_count) for module_count in range(1, max_module_count + 1))
