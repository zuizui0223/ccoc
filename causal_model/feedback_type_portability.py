"""Exact feedback portability under bounded interaction types.

Each interaction type may contain arbitrarily many exchangeable physical gate
copies.  Copy identities are not individually addressed: type-level ``spread``
and ``turnover`` actions act synchronously on all copies of one type.  On the
reachable domain generated from target-empty initial states, every type has an
exact five-state causal quotient independent of its replication count.

For a fixed number q of interaction types, the product quotient therefore has
exactly 5**q states across arbitrary replication vectors.  This is the positive
counterpart to the individually addressable feedback-rank family.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from itertools import product
from math import log2

SPREAD = "spread"
TURNOVER = "turnover"
TYPE_ACTIONS: tuple[str, ...] = (SPREAD, TURNOVER)

EMPTY = "empty-unreachable"
READY_RESILIENT = "ready-resilient"
READY_FRAGILE = "ready-fragile"
OCCUPIED_RESILIENT = "occupied-resilient"
OCCUPIED_NO_RECOVERY = "occupied-no-recovery"
TYPE_MACRO_STATES: tuple[str, ...] = (
    EMPTY,
    READY_RESILIENT,
    READY_FRAGILE,
    OCCUPIED_RESILIENT,
    OCCUPIED_NO_RECOVERY,
)


def _validate_replication(replication: int) -> None:
    if not isinstance(replication, int) or isinstance(replication, bool) or replication < 1:
        raise ValueError("replication must be a positive integer")


@dataclass(frozen=True)
class FeedbackTypeState:
    """Microstate for one exchangeable feedback type."""

    mode: int
    facilitators: tuple[int, ...]
    targets: tuple[int, ...]

    @property
    def replication(self) -> int:
        return len(self.facilitators)

    def validate(self) -> None:
        if self.mode not in (0, 1):
            raise ValueError("mode must be binary")
        _validate_replication(self.replication)
        if len(self.targets) != self.replication:
            raise ValueError("facilitator and target vectors must have equal length")
        if any(bit not in (0, 1) for bit in self.facilitators + self.targets):
            raise ValueError("gate state coordinates must be binary")
        if any(target and not facilitator for facilitator, target in zip(self.facilitators, self.targets)):
            raise ValueError("reachable target occupancy must be supported by a facilitator")
        if any(self.targets) and self.targets != self.facilitators:
            raise ValueError("reachable occupied states have targets equal to facilitator support")


def type_output(state: FeedbackTypeState) -> int:
    state.validate()
    return int(any(state.targets))


def type_macro_label(state: FeedbackTypeState) -> str:
    """Canonical five-state feedback label on the reachable domain."""
    state.validate()
    facilitator_present = any(state.facilitators)
    occupied = any(state.targets)
    if not facilitator_present:
        return EMPTY
    if not occupied:
        return READY_FRAGILE if state.mode else READY_RESILIENT
    return OCCUPIED_NO_RECOVERY if state.mode else OCCUPIED_RESILIENT


def type_step(state: FeedbackTypeState, action: str) -> FeedbackTypeState:
    """Apply one synchronous type-level spread or turnover action."""
    state.validate()
    if action not in TYPE_ACTIONS:
        raise ValueError(f"unknown type action: {action!r}")
    if action == SPREAD:
        return FeedbackTypeState(
            mode=state.mode,
            facilitators=state.facilitators,
            targets=state.facilitators,
        )

    # TURNOVER
    if not any(state.targets):
        return state
    if state.mode:
        facilitators = (0,) * state.replication
    else:
        facilitators = state.facilitators
    return FeedbackTypeState(
        mode=state.mode,
        facilitators=facilitators,
        targets=(0,) * state.replication,
    )


def type_macro_output(label: str) -> int:
    if label not in TYPE_MACRO_STATES:
        raise ValueError("unknown feedback macro state")
    return int(label in (OCCUPIED_RESILIENT, OCCUPIED_NO_RECOVERY))


def type_macro_step(label: str, action: str) -> str:
    """Capacity-free five-state macro transition law."""
    if label not in TYPE_MACRO_STATES:
        raise ValueError("unknown feedback macro state")
    if action not in TYPE_ACTIONS:
        raise ValueError(f"unknown type action: {action!r}")
    if label == EMPTY:
        return EMPTY
    if label == READY_RESILIENT:
        return OCCUPIED_RESILIENT if action == SPREAD else READY_RESILIENT
    if label == READY_FRAGILE:
        return OCCUPIED_NO_RECOVERY if action == SPREAD else READY_FRAGILE
    if label == OCCUPIED_RESILIENT:
        return OCCUPIED_RESILIENT if action == SPREAD else READY_RESILIENT
    return OCCUPIED_NO_RECOVERY if action == SPREAD else EMPTY


def reachable_type_states(replication: int) -> tuple[FeedbackTypeState, ...]:
    """Enumerate the exact domain reachable from arbitrary target-empty starts."""
    _validate_replication(replication)
    states: set[FeedbackTypeState] = set()
    for mode in (0, 1):
        for facilitator_bits in product((0, 1), repeat=replication):
            facilitators = tuple(facilitator_bits)
            states.add(
                FeedbackTypeState(
                    mode=mode,
                    facilitators=facilitators,
                    targets=(0,) * replication,
                )
            )
            if any(facilitators):
                states.add(
                    FeedbackTypeState(
                        mode=mode,
                        facilitators=facilitators,
                        targets=facilitators,
                    )
                )
    return tuple(sorted(states, key=lambda s: (s.mode, s.facilitators, s.targets)))


def reachable_type_state_count(replication: int) -> int:
    """Closed form for the one-type reachable microstate count."""
    _validate_replication(replication)
    return 2 ** (replication + 2) - 2


def type_representative(label: str, replication: int) -> FeedbackTypeState:
    """Return one concrete microstate for each canonical macro label."""
    _validate_replication(replication)
    if label not in TYPE_MACRO_STATES:
        raise ValueError("unknown feedback macro state")
    zero = (0,) * replication
    one = (1,) + (0,) * (replication - 1)
    if label == EMPTY:
        return FeedbackTypeState(mode=0, facilitators=zero, targets=zero)
    if label == READY_RESILIENT:
        return FeedbackTypeState(mode=0, facilitators=one, targets=zero)
    if label == READY_FRAGILE:
        return FeedbackTypeState(mode=1, facilitators=one, targets=zero)
    if label == OCCUPIED_RESILIENT:
        return FeedbackTypeState(mode=0, facilitators=one, targets=one)
    return FeedbackTypeState(mode=1, facilitators=one, targets=one)


def type_macro_distinguishing_word(left: str, right: str) -> tuple[str, ...]:
    """Return a shortest word separating two distinct five-state macro labels."""
    if left not in TYPE_MACRO_STATES or right not in TYPE_MACRO_STATES:
        raise ValueError("unknown feedback macro state")
    if left == right:
        raise ValueError("distinct macro states are required")
    queue: deque[tuple[str, str, tuple[str, ...]]] = deque([(left, right, ())])
    visited = {(left, right)}
    while queue:
        a, b, word = queue.popleft()
        if type_macro_output(a) != type_macro_output(b):
            return word
        for action in TYPE_ACTIONS:
            next_a = type_macro_step(a, action)
            next_b = type_macro_step(b, action)
            pair = (next_a, next_b)
            if pair not in visited:
                visited.add(pair)
                queue.append((next_a, next_b, word + (action,)))
    raise AssertionError("the declared five-state macro should be minimal")


def type_action(kind: str, type_index: int) -> str:
    if kind not in TYPE_ACTIONS:
        raise ValueError("kind must be spread or turnover")
    if not isinstance(type_index, int) or isinstance(type_index, bool) or type_index < 0:
        raise ValueError("type index must be a non-negative integer")
    return f"{kind}:{type_index}"


def _parse_type_action(action: str, type_count: int) -> tuple[str, int]:
    if not isinstance(action, str) or ":" not in action:
        raise ValueError(f"invalid type action: {action!r}")
    kind, suffix = action.split(":", 1)
    if kind not in TYPE_ACTIONS:
        raise ValueError(f"invalid type action: {action!r}")
    try:
        index = int(suffix)
    except ValueError as error:
        raise ValueError(f"invalid type action: {action!r}") from error
    if not 0 <= index < type_count:
        raise ValueError("type action index outside declared type range")
    return kind, index


def product_action_alphabet(type_count: int) -> tuple[str, ...]:
    if not isinstance(type_count, int) or isinstance(type_count, bool) or type_count < 1:
        raise ValueError("type_count must be a positive integer")
    return tuple(
        type_action(kind, index)
        for index in range(type_count)
        for kind in TYPE_ACTIONS
    )


ProductState = tuple[FeedbackTypeState, ...]
ProductMacroLabel = tuple[str, ...]


def product_output(state: ProductState) -> tuple[int, ...]:
    if not state:
        raise ValueError("product state must contain at least one type")
    return tuple(type_output(component) for component in state)


def product_macro_label(state: ProductState) -> ProductMacroLabel:
    if not state:
        raise ValueError("product state must contain at least one type")
    return tuple(type_macro_label(component) for component in state)


def product_step(state: ProductState, action: str) -> ProductState:
    if not state:
        raise ValueError("product state must contain at least one type")
    kind, index = _parse_type_action(action, len(state))
    components = list(state)
    components[index] = type_step(components[index], kind)
    return tuple(components)


def product_macro_step(label: ProductMacroLabel, action: str) -> ProductMacroLabel:
    if not label:
        raise ValueError("product macro label must contain at least one type")
    kind, index = _parse_type_action(action, len(label))
    labels = list(label)
    labels[index] = type_macro_step(labels[index], kind)
    return tuple(labels)


def product_reachable_state_count(replications: tuple[int, ...]) -> int:
    if not isinstance(replications, tuple) or not replications:
        raise ValueError("replications must be a non-empty tuple")
    count = 1
    for replication in replications:
        count *= reachable_type_state_count(replication)
    return count


def product_macro_state_count(type_count: int) -> int:
    if not isinstance(type_count, int) or isinstance(type_count, bool) or type_count < 1:
        raise ValueError("type_count must be a positive integer")
    return 5**type_count


@dataclass(frozen=True)
class FeedbackTypePortabilityCertificate:
    """Changing-domain portability certificate for fixed interaction-type count."""

    replication_vectors: tuple[tuple[int, ...], ...]
    type_count: int
    macro_state_count: int
    action_alphabet_size: int
    physical_state_counts: tuple[int, ...]

    @property
    def macro_memory_bits(self) -> float:
        return self.type_count * log2(5)

    def verify(self) -> bool:
        try:
            if not self.replication_vectors:
                return False
            if self.type_count < 1:
                return False
            for vector in self.replication_vectors:
                if len(vector) != self.type_count:
                    return False
                for replication in vector:
                    _validate_replication(replication)
            if self.macro_state_count != product_macro_state_count(self.type_count):
                return False
            if self.action_alphabet_size != 2 * self.type_count:
                return False
            expected_counts = tuple(product_reachable_state_count(v) for v in self.replication_vectors)
            if self.physical_state_counts != expected_counts:
                return False

            # Verify the capacity-free local transition table on one representative
            # of every macro state at every replication count that appears.
            for replication in sorted({n for vector in self.replication_vectors for n in vector}):
                empty_fragile = FeedbackTypeState(
                    mode=1,
                    facilitators=(0,) * replication,
                    targets=(0,) * replication,
                )
                if type_macro_label(empty_fragile) != EMPTY:
                    return False
                for label in TYPE_MACRO_STATES:
                    representative = type_representative(label, replication)
                    if type_macro_label(representative) != label:
                        return False
                    if type_output(representative) != type_macro_output(label):
                        return False
                    for action in TYPE_ACTIONS:
                        successor = type_step(representative, action)
                        if type_macro_label(successor) != type_macro_step(label, action):
                            return False

            for left in TYPE_MACRO_STATES:
                for right in TYPE_MACRO_STATES:
                    if left == right:
                        continue
                    word = type_macro_distinguishing_word(left, right)
                    a, b = left, right
                    trace_a = [type_macro_output(a)]
                    trace_b = [type_macro_output(b)]
                    for action in word:
                        a = type_macro_step(a, action)
                        b = type_macro_step(b, action)
                        trace_a.append(type_macro_output(a))
                        trace_b.append(type_macro_output(b))
                    if tuple(trace_a) == tuple(trace_b):
                        return False
            return True
        except ValueError:
            return False


def certify_feedback_type_portability(
    replication_vectors: tuple[tuple[int, ...], ...],
) -> FeedbackTypePortabilityCertificate:
    if not isinstance(replication_vectors, tuple) or not replication_vectors:
        raise ValueError("replication_vectors must be a non-empty tuple")
    type_count = len(replication_vectors[0])
    if type_count < 1:
        raise ValueError("replication vectors must contain at least one interaction type")
    for vector in replication_vectors:
        if len(vector) != type_count:
            raise ValueError("all replication vectors must have the same type count")
        for replication in vector:
            _validate_replication(replication)
    certificate = FeedbackTypePortabilityCertificate(
        replication_vectors=replication_vectors,
        type_count=type_count,
        macro_state_count=product_macro_state_count(type_count),
        action_alphabet_size=len(product_action_alphabet(type_count)),
        physical_state_counts=tuple(product_reachable_state_count(v) for v in replication_vectors),
    )
    if not certificate.verify():
        raise AssertionError(f"feedback type portability certificate failed: {certificate!r}")
    return certificate
