"""Candidate-safe macro-laws and ensemble--instance separation certificates.

A finite candidate family can have a small exact macro-law in every candidate
while lacking one candidate-independent deterministic macro-law.  This module
separates four distinct objects:

* an **instance law**, valid after a candidate mechanism is fixed;
* a **universal deterministic law**, valid after the candidate is forgotten;
* a **candidate-safe deterministic law**, which stores a response type together
  with the shared macrostate; and
* a **set-valued law**, the honest candidate-forgetting prediction when a
  universal deterministic law does not exist.

The main lower bound is conditional on *uniform response separation*: every two
response types can be distinguished by a declared future word from every shared
macrostate.  Under that operational condition, a candidate-safe interface has
at least ``|Q| * R`` states, where ``R`` is the number of distinct induced
response types.  The proof is an injection via concrete separating words, not a
cardinality assertion made in advance.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from math import log2
from typing import Hashable, Iterable

from .delayed_addressability import DelayedReaderGrammar
from .dynamic_boundary_blankets import (
    FiniteControlledOutputSystem,
    certify_finite_horizon_stabilization,
)

Action = str
MacroState = int
CandidateIndex = int
ResponseType = int
Word = tuple[Action, ...]


def _validate_nonempty_tuple(values: object, name: str) -> tuple[object, ...]:
    if not isinstance(values, tuple) or not values:
        raise ValueError(f"{name} must be a nonempty tuple")
    return values


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


@dataclass(frozen=True)
class CandidateInducedLaw:
    """One candidate's exact deterministic law on a declared common macrostate.

    ``transition_table[q][a_index]`` is the candidate-specific macro successor
    after action ``actions[a_index]``.  ``macro_outputs`` must be injective: the
    macrostate itself is observable at this theorem layer.
    """

    candidate_id: str
    actions: tuple[Action, ...]
    transition_table: tuple[tuple[MacroState, ...], ...]
    macro_outputs: tuple[Hashable, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.candidate_id, str) or not self.candidate_id:
            raise ValueError("candidate_id must be a nonempty string")
        actions = _validate_nonempty_tuple(self.actions, "actions")
        if any(not isinstance(action, str) or not action for action in actions):
            raise ValueError("actions must be nonempty strings")
        if len(set(actions)) != len(actions):
            raise ValueError("actions must be unique")
        outputs = _validate_nonempty_tuple(self.macro_outputs, "macro_outputs")
        try:
            if len(set(outputs)) != len(outputs):
                raise ValueError("macro_outputs must be injective")
        except TypeError as error:
            raise ValueError("macro_outputs must be hashable") from error
        if not isinstance(self.transition_table, tuple) or len(self.transition_table) != len(outputs):
            raise ValueError("transition_table must provide one row per macrostate")
        for row in self.transition_table:
            if not isinstance(row, tuple) or len(row) != len(actions):
                raise ValueError("every transition row must match the action count")
            for target in row:
                if not isinstance(target, int) or isinstance(target, bool) or not 0 <= target < len(outputs):
                    raise ValueError("macro transition targets must be valid macrostate indices")

    @property
    def macrostate_count(self) -> int:
        return len(self.macro_outputs)

    @property
    def macrostates(self) -> tuple[MacroState, ...]:
        return tuple(range(self.macrostate_count))

    def action_index(self, action: Action) -> int:
        try:
            return self.actions.index(action)
        except ValueError as error:
            raise ValueError(f"unknown action: {action!r}") from error

    def transition(self, macrostate: MacroState, action: Action) -> MacroState:
        self.validate_macrostate(macrostate)
        return self.transition_table[macrostate][self.action_index(action)]

    def output(self, macrostate: MacroState) -> Hashable:
        self.validate_macrostate(macrostate)
        return self.macro_outputs[macrostate]

    def validate_macrostate(self, macrostate: MacroState) -> None:
        if not isinstance(macrostate, int) or isinstance(macrostate, bool) or not 0 <= macrostate < self.macrostate_count:
            raise ValueError("macrostate is outside the common macrostate space")

    def normalize_word(self, word: Iterable[Action]) -> Word:
        try:
            normalized = tuple(word)
        except TypeError as error:
            raise ValueError("word must be an iterable of actions") from error
        for action in normalized:
            self.action_index(action)
        return normalized

    def final_macrostate(self, macrostate: MacroState, word: Iterable[Action]) -> MacroState:
        current = macrostate
        for action in self.normalize_word(word):
            current = self.transition(current, action)
        return current

    def output_trace(self, macrostate: MacroState, word: Iterable[Action]) -> tuple[Hashable, ...]:
        current = macrostate
        trace = [self.output(current)]
        for action in self.normalize_word(word):
            current = self.transition(current, action)
            trace.append(self.output(current))
        return tuple(trace)

    @property
    def response_signature(self) -> tuple[tuple[MacroState, ...], ...]:
        """Complete induced deterministic response map over the one-step grammar."""
        return self.transition_table


@dataclass(frozen=True)
class CandidateLawFamily:
    """Retained candidate mechanisms sharing one observable macrostate space."""

    candidates: tuple[CandidateInducedLaw, ...]

    def __post_init__(self) -> None:
        candidates = _validate_nonempty_tuple(self.candidates, "candidates")
        if any(not isinstance(candidate, CandidateInducedLaw) for candidate in candidates):
            raise ValueError("candidates must contain CandidateInducedLaw objects")
        ids = tuple(candidate.candidate_id for candidate in candidates)
        if len(set(ids)) != len(ids):
            raise ValueError("candidate identifiers must be unique")
        first = candidates[0]
        for candidate in candidates[1:]:
            if candidate.actions != first.actions:
                raise ValueError("all candidates must share the same ordered action alphabet")
            if candidate.macro_outputs != first.macro_outputs:
                raise ValueError("all candidates must share the same observable macrostate space")

    @property
    def actions(self) -> tuple[Action, ...]:
        return self.candidates[0].actions

    @property
    def macro_outputs(self) -> tuple[Hashable, ...]:
        return self.candidates[0].macro_outputs

    @property
    def macrostate_count(self) -> int:
        return len(self.macro_outputs)

    @property
    def macrostates(self) -> tuple[MacroState, ...]:
        return tuple(range(self.macrostate_count))

    @property
    def candidate_count(self) -> int:
        return len(self.candidates)

    @property
    def response_type_labels(self) -> tuple[ResponseType, ...]:
        return _canonical_labels(candidate.response_signature for candidate in self.candidates)

    @property
    def response_type_count(self) -> int:
        return len(set(self.response_type_labels))

    @property
    def response_type_representatives(self) -> tuple[CandidateIndex, ...]:
        representatives: dict[ResponseType, CandidateIndex] = {}
        for index, response_type in enumerate(self.response_type_labels):
            representatives.setdefault(response_type, index)
        return tuple(representatives[response_type] for response_type in sorted(representatives))

    def candidate_for_type(self, response_type: ResponseType) -> CandidateInducedLaw:
        if not isinstance(response_type, int) or isinstance(response_type, bool) or not 0 <= response_type < self.response_type_count:
            raise ValueError("response type is outside the retained family")
        return self.candidates[self.response_type_representatives[response_type]]

    def type_of_candidate(self, candidate_index: CandidateIndex) -> ResponseType:
        if not isinstance(candidate_index, int) or isinstance(candidate_index, bool) or not 0 <= candidate_index < self.candidate_count:
            raise ValueError("candidate index is outside the retained family")
        return self.response_type_labels[candidate_index]

    def set_valued_successor(self, macrostate: MacroState, action: Action) -> frozenset[MacroState]:
        for candidate in self.candidates:
            candidate.validate_macrostate(macrostate)
            candidate.action_index(action)
        return frozenset(candidate.transition(macrostate, action) for candidate in self.candidates)

    @property
    def has_universal_deterministic_law(self) -> bool:
        return self.response_type_count == 1

    def universal_transition_table(self) -> tuple[tuple[MacroState, ...], ...]:
        if not self.has_universal_deterministic_law:
            raise ValueError("retained candidates do not share a deterministic universal macro-law")
        return self.candidates[0].transition_table

    def augmented_candidate_safe_system(self) -> FiniteControlledOutputSystem:
        """System on (response type, macrostate), with type preserved by updates."""
        type_count = self.response_type_count
        macro_count = self.macrostate_count
        rows: list[tuple[int, ...]] = []
        outputs: list[Hashable] = []
        for response_type in range(type_count):
            candidate = self.candidate_for_type(response_type)
            for macrostate in range(macro_count):
                rows.append(
                    tuple(
                        response_type * macro_count + candidate.transition(macrostate, action)
                        for action in self.actions
                    )
                )
                outputs.append(candidate.output(macrostate))
        return FiniteControlledOutputSystem(
            actions=self.actions,
            transition_table=tuple(rows),
            outputs=tuple(outputs),
        )

    def augmented_state_index(self, response_type: ResponseType, macrostate: MacroState) -> int:
        if not isinstance(response_type, int) or isinstance(response_type, bool) or not 0 <= response_type < self.response_type_count:
            raise ValueError("response type is outside the retained family")
        if not isinstance(macrostate, int) or isinstance(macrostate, bool) or not 0 <= macrostate < self.macrostate_count:
            raise ValueError("macrostate is outside the common macrostate space")
        return response_type * self.macrostate_count + macrostate


def _words_through(actions: tuple[Action, ...], horizon: int) -> tuple[Word, ...]:
    _validate_positive_integer(horizon + 1, "horizon plus one")
    return tuple(
        word
        for length in range(horizon + 1)
        for word in product(actions, repeat=length)
    )


@dataclass(frozen=True)
class CandidateResponseSeparationCertificate:
    """Concrete future word separating two response types at one macrostate."""

    family: CandidateLawFamily
    left_type: ResponseType
    right_type: ResponseType
    macrostate: MacroState
    word: Word
    left_trace: tuple[Hashable, ...]
    right_trace: tuple[Hashable, ...]

    def verify(self) -> bool:
        try:
            if self.left_type == self.right_type:
                return False
            left = self.family.candidate_for_type(self.left_type)
            right = self.family.candidate_for_type(self.right_type)
            left.validate_macrostate(self.macrostate)
            right.validate_macrostate(self.macrostate)
            normalized = left.normalize_word(self.word)
            if normalized != right.normalize_word(self.word):
                return False
            if self.left_trace != left.output_trace(self.macrostate, normalized):
                return False
            if self.right_trace != right.output_trace(self.macrostate, normalized):
                return False
            return self.left_trace != self.right_trace
        except ValueError:
            return False


def find_candidate_response_separator(
    family: CandidateLawFamily,
    left_type: ResponseType,
    right_type: ResponseType,
    macrostate: MacroState,
) -> CandidateResponseSeparationCertificate | None:
    """Find a shortest explicit word separating two response types at one state.

    The bounded search depth is the exact finite-state bound for the candidate-
    augmented system.  Failure is informative: the family does not satisfy the
    uniform response-separation premise required by the product lower bound.
    """
    if left_type == right_type:
        raise ValueError("a response separator requires distinct response types")
    left = family.candidate_for_type(left_type)
    right = family.candidate_for_type(right_type)
    left.validate_macrostate(macrostate)
    right.validate_macrostate(macrostate)
    bound = family.response_type_count * family.macrostate_count - 1
    for word in _words_through(family.actions, bound):
        left_trace = left.output_trace(macrostate, word)
        right_trace = right.output_trace(macrostate, word)
        if left_trace != right_trace:
            certificate = CandidateResponseSeparationCertificate(
                family=family,
                left_type=left_type,
                right_type=right_type,
                macrostate=macrostate,
                word=word,
                left_trace=left_trace,
                right_trace=right_trace,
            )
            if not certificate.verify():
                raise AssertionError("constructed candidate response separator did not verify")
            return certificate
    return None


@dataclass(frozen=True)
class UniversalMacroLawCertificate:
    """Certificate that every retained candidate induces the same macro transition."""

    family: CandidateLawFamily
    universal_transition_table: tuple[tuple[MacroState, ...], ...]

    @property
    def macro_interface_bits(self) -> float:
        return log2(self.family.macrostate_count)

    def verify(self) -> bool:
        try:
            if not self.family.has_universal_deterministic_law:
                return False
            if self.universal_transition_table != self.family.universal_transition_table():
                return False
            for candidate in self.family.candidates:
                if candidate.transition_table != self.universal_transition_table:
                    return False
            return True
        except ValueError:
            return False


def certify_universal_macro_law(family: CandidateLawFamily) -> UniversalMacroLawCertificate:
    certificate = UniversalMacroLawCertificate(
        family=family,
        universal_transition_table=family.universal_transition_table(),
    )
    if not certificate.verify():
        raise AssertionError("universal macro-law certificate did not verify")
    return certificate


@dataclass(frozen=True)
class UniversalLawObstructionCertificate:
    """One shared macrostate/action whose successors disagree across candidates."""

    family: CandidateLawFamily
    left_type: ResponseType
    right_type: ResponseType
    macrostate: MacroState
    action: Action
    left_successor: MacroState
    right_successor: MacroState

    def verify(self) -> bool:
        try:
            if self.left_type == self.right_type:
                return False
            left = self.family.candidate_for_type(self.left_type)
            right = self.family.candidate_for_type(self.right_type)
            left.validate_macrostate(self.macrostate)
            left.action_index(self.action)
            if self.left_successor != left.transition(self.macrostate, self.action):
                return False
            if self.right_successor != right.transition(self.macrostate, self.action):
                return False
            return self.left_successor != self.right_successor
        except ValueError:
            return False


def universal_law_obstruction_certificate(family: CandidateLawFamily) -> UniversalLawObstructionCertificate:
    """Produce a one-step witness that a shared deterministic macro-law cannot exist."""
    if family.has_universal_deterministic_law:
        raise ValueError("a universal law exists; no obstruction certificate is available")
    for left_type, right_type in combinations(range(family.response_type_count), 2):
        left = family.candidate_for_type(left_type)
        right = family.candidate_for_type(right_type)
        for macrostate in family.macrostates:
            for action in family.actions:
                left_successor = left.transition(macrostate, action)
                right_successor = right.transition(macrostate, action)
                if left_successor != right_successor:
                    certificate = UniversalLawObstructionCertificate(
                        family=family,
                        left_type=left_type,
                        right_type=right_type,
                        macrostate=macrostate,
                        action=action,
                        left_successor=left_successor,
                        right_successor=right_successor,
                    )
                    if not certificate.verify():
                        raise AssertionError("universal-law obstruction certificate did not verify")
                    return certificate
    raise AssertionError("distinct response types did not yield a transition obstruction")


@dataclass(frozen=True)
class SetValuedMacroLawCertificate:
    """Candidate-forgetting, possibly nondeterministic macro prediction."""

    family: CandidateLawFamily
    successor_sets: tuple[tuple[frozenset[MacroState], ...], ...]

    @property
    def is_deterministic(self) -> bool:
        return all(len(successors) == 1 for row in self.successor_sets for successors in row)

    def verify(self) -> bool:
        try:
            if len(self.successor_sets) != self.family.macrostate_count:
                return False
            for macrostate, row in enumerate(self.successor_sets):
                if not isinstance(row, tuple) or len(row) != len(self.family.actions):
                    return False
                for action, successors in zip(self.family.actions, row):
                    if successors != self.family.set_valued_successor(macrostate, action):
                        return False
            return self.is_deterministic == self.family.has_universal_deterministic_law
        except ValueError:
            return False


def certify_set_valued_macro_law(family: CandidateLawFamily) -> SetValuedMacroLawCertificate:
    certificate = SetValuedMacroLawCertificate(
        family=family,
        successor_sets=tuple(
            tuple(family.set_valued_successor(macrostate, action) for action in family.actions)
            for macrostate in family.macrostates
        ),
    )
    if not certificate.verify():
        raise AssertionError("set-valued macro-law certificate did not verify")
    return certificate


@dataclass(frozen=True)
class CandidateSafeProductCertificate:
    """Product lower bound from uniformly addressable response types.

    The premise is checked by a concrete separating word for every response-type
    pair and every shared macrostate.  Since macro outputs are injective,
    unequal macrostates are separated immediately.  These witnesses inject the
    product ``Q x R`` into the exact candidate-safe trace quotient.
    """

    family: CandidateLawFamily
    candidate_safe_block_count: int
    stabilization_horizon: int
    checked_type_state_separators: int

    @property
    def response_type_count(self) -> int:
        return self.family.response_type_count

    @property
    def macrostate_count(self) -> int:
        return self.family.macrostate_count

    @property
    def expected_block_count(self) -> int:
        return self.response_type_count * self.macrostate_count

    @property
    def expected_separator_count(self) -> int:
        return self.macrostate_count * self.response_type_count * (self.response_type_count - 1) // 2

    @property
    def instance_interface_bits(self) -> float:
        return log2(self.macrostate_count)

    @property
    def candidate_safe_interface_bits(self) -> float:
        return log2(self.candidate_safe_block_count)

    @property
    def response_type_inflation_bits(self) -> float:
        return self.candidate_safe_interface_bits - self.instance_interface_bits

    @property
    def product_lower_bound_bits(self) -> float:
        return log2(self.macrostate_count) + log2(self.response_type_count)

    def verify(self) -> bool:
        try:
            augmented = self.family.augmented_candidate_safe_system()
            stabilization = certify_finite_horizon_stabilization(augmented)
            if self.candidate_safe_block_count != stabilization.canonical_block_count:
                return False
            if self.stabilization_horizon != stabilization.stabilization_horizon:
                return False
            if self.checked_type_state_separators != self.expected_separator_count:
                return False
            for macrostate in self.family.macrostates:
                for left_type, right_type in combinations(range(self.response_type_count), 2):
                    certificate = find_candidate_response_separator(
                        self.family,
                        left_type,
                        right_type,
                        macrostate,
                    )
                    if certificate is None or not certificate.verify():
                        return False
            if self.candidate_safe_block_count != self.expected_block_count:
                return False
            if abs(self.candidate_safe_interface_bits - self.product_lower_bound_bits) > 1e-12:
                return False
            return True
        except (AssertionError, ValueError):
            return False


def certify_candidate_safe_product(family: CandidateLawFamily) -> CandidateSafeProductCertificate:
    augmented = family.augmented_candidate_safe_system()
    stabilization = certify_finite_horizon_stabilization(augmented)
    certificate = CandidateSafeProductCertificate(
        family=family,
        candidate_safe_block_count=stabilization.canonical_block_count,
        stabilization_horizon=stabilization.stabilization_horizon,
        checked_type_state_separators=(
            family.macrostate_count * family.response_type_count * (family.response_type_count - 1) // 2
        ),
    )
    if not certificate.verify():
        raise AssertionError(
            "candidate-safe product certificate failed: the family may lack uniform response separation"
        )
    return certificate


def binary_identity_flip_family() -> CandidateLawFamily:
    """Two one-bit instance laws with incompatible induced intervention maps."""
    return CandidateLawFamily(
        candidates=(
            CandidateInducedLaw(
                candidate_id="identity",
                actions=("passive", "intervene"),
                transition_table=((0, 0), (1, 1)),
                macro_outputs=(0, 1),
            ),
            CandidateInducedLaw(
                candidate_id="flip",
                actions=("passive", "intervene"),
                transition_table=((0, 1), (1, 0)),
                macro_outputs=(0, 1),
            ),
        )
    )


def binary_agreement_family() -> CandidateLawFamily:
    """Duplicate mechanisms demonstrating the positive universal-law case."""
    return CandidateLawFamily(
        candidates=(
            CandidateInducedLaw(
                candidate_id="identity-a",
                actions=("passive", "intervene"),
                transition_table=((0, 0), (1, 1)),
                macro_outputs=(0, 1),
            ),
            CandidateInducedLaw(
                candidate_id="identity-b",
                actions=("passive", "intervene"),
                transition_table=((0, 0), (1, 1)),
                macro_outputs=(0, 1),
            ),
        )
    )


@dataclass(frozen=True)
class DelayedCandidateDiscriminationCertificate:
    """Candidate response types that remain unresolved until a delayed legal word."""

    delay: int
    family: CandidateLawFamily
    shared_horizon: int
    revealing_word: Word
    left_trace: tuple[Hashable, ...]
    right_trace: tuple[Hashable, ...]

    @property
    def revealing_horizon(self) -> int:
        return self.delay + 1

    def verify(self) -> bool:
        try:
            _validate_positive_integer(self.delay + 1, "delay plus one")
            grammar = DelayedReaderGrammar(self.delay)
            if self.family.actions != ("wait", "fire"):
                return False
            if self.family.response_type_count != 2 or self.family.macrostate_count != 2:
                return False
            if self.shared_horizon != self.delay or self.revealing_word != grammar.revealing_word:
                return False
            left = self.family.candidate_for_type(0)
            right = self.family.candidate_for_type(1)
            for macrostate in self.family.macrostates:
                for word in grammar.legal_words_through(self.shared_horizon):
                    if left.output_trace(macrostate, word) != right.output_trace(macrostate, word):
                        return False
            if self.left_trace != left.output_trace(0, self.revealing_word):
                return False
            if self.right_trace != right.output_trace(0, self.revealing_word):
                return False
            if self.left_trace == self.right_trace:
                return False
            product_certificate = certify_candidate_safe_product(self.family)
            return product_certificate.verify() and product_certificate.candidate_safe_block_count == 4
        except (AssertionError, ValueError):
            return False


def delayed_identity_flip_family() -> CandidateLawFamily:
    return CandidateLawFamily(
        candidates=(
            CandidateInducedLaw(
                candidate_id="delayed-identity",
                actions=("wait", "fire"),
                transition_table=((0, 0), (1, 1)),
                macro_outputs=(0, 1),
            ),
            CandidateInducedLaw(
                candidate_id="delayed-flip",
                actions=("wait", "fire"),
                transition_table=((0, 1), (1, 0)),
                macro_outputs=(0, 1),
            ),
        )
    )


def certify_delayed_candidate_discrimination(delay: int) -> DelayedCandidateDiscriminationCertificate:
    if not isinstance(delay, int) or isinstance(delay, bool) or delay < 0:
        raise ValueError("delay must be a non-negative integer")
    family = delayed_identity_flip_family()
    grammar = DelayedReaderGrammar(delay)
    left = family.candidate_for_type(0)
    right = family.candidate_for_type(1)
    certificate = DelayedCandidateDiscriminationCertificate(
        delay=delay,
        family=family,
        shared_horizon=delay,
        revealing_word=grammar.revealing_word,
        left_trace=left.output_trace(0, grammar.revealing_word),
        right_trace=right.output_trace(0, grammar.revealing_word),
    )
    if not certificate.verify():
        raise AssertionError("delayed candidate discrimination certificate did not verify")
    return certificate
