"""Joint exterior--mechanism separation and universal open-law certificates.

This module joins two previously separate RACH questions without silently
adding their lower bounds.

1. A candidate-specific **dynamic interface** must preserve window output and
   update through every declared action.
2. A universal deterministic open law additionally requires the induced macro
   transition maps to agree across retained candidates.
3. Exterior memory and response-type memory are additive only under an explicit
   *joint operational separation* condition.  The canonical structural product
   witness supplies that condition using concrete permitted queries.

The structural witness keeps the local action alphabet fixed at
``{observe, read, intervene}``.  A port is selected by a structural attachment
context, not by a growing token such as ``read:port``.  Response type is a
candidate mechanism parameter; it is never injected as an action label.

The module deliberately keeps two levels distinct:

* ``OpenLawFamily`` is a general finite controlled candidate family with
  candidate-specific microstate spaces and a common macrostate space.
* ``JointOpenCandidateProduct`` is a canonical finite structural witness for the
  joint lower bound.

The executable replays validate finite objects.  The accompanying document
contains the all-parameter proofs and the exact scope boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import combinations, product
from math import log2, prod
from typing import Hashable, Iterable

from .dynamic_boundary_blankets import (
    DynamicInterfaceCertificate,
    FiniteControlledOutputSystem,
    certify_finite_horizon_stabilization,
)

Action = str
MacroState = int
ResponseType = int
CandidateIndex = int
StructuralState = tuple[int, ...]

OBSERVE: Action = "observe"
READ: Action = "read"
INTERVENE: Action = "intervene"
LOCAL_ACTIONS: tuple[Action, Action, Action] = (OBSERVE, READ, INTERVENE)


def _validate_positive_integer(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _validate_nonempty_tuple(values: object, name: str) -> tuple[object, ...]:
    if not isinstance(values, tuple) or not values:
        raise ValueError(f"{name} must be a nonempty tuple")
    return values


def _canonical_labels(values: Iterable[Hashable]) -> tuple[int, ...]:
    labels: dict[Hashable, int] = {}
    result: list[int] = []
    for value in values:
        if value not in labels:
            labels[value] = len(labels)
        result.append(labels[value])
    return tuple(result)


@dataclass(frozen=True)
class OpenLawCandidate:
    """One candidate's micro system and a proposed common dynamic macro interface.

    ``macro_labels`` maps candidate microstates into integer labels for one common
    macrostate space.  Every common macro label must be realized.  The
    ``macro_outputs`` tuple is shared by every candidate in an ``OpenLawFamily``;
    it is injective so the macrostate itself is observable at this theorem layer.

    This class validates representation shape.  Dynamic sufficiency is checked by
    ``DynamicInterfaceCertificate`` and exposed by ``is_dynamic_interface``.
    """

    candidate_id: str
    system: FiniteControlledOutputSystem
    macro_labels: tuple[MacroState, ...]
    macro_outputs: tuple[Hashable, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.candidate_id, str) or not self.candidate_id:
            raise ValueError("candidate_id must be a nonempty string")
        outputs = _validate_nonempty_tuple(self.macro_outputs, "macro_outputs")
        try:
            if len(set(outputs)) != len(outputs):
                raise ValueError("macro_outputs must be injective")
        except TypeError as error:
            raise ValueError("macro_outputs must be hashable") from error
        if not isinstance(self.macro_labels, tuple) or len(self.macro_labels) != self.system.state_count:
            raise ValueError("macro_labels must provide one label per microstate")
        macro_count = len(outputs)
        for label in self.macro_labels:
            if not isinstance(label, int) or isinstance(label, bool) or not 0 <= label < macro_count:
                raise ValueError("macro label is outside the common macrostate space")
        if set(self.macro_labels) != set(range(macro_count)):
            raise ValueError("every common macrostate must be realized by each candidate")
        expected_outputs = tuple(outputs[label] for label in self.macro_labels)
        if self.system.outputs != expected_outputs:
            raise ValueError("candidate outputs must equal the declared common macro output map")

    @property
    def macrostate_count(self) -> int:
        return len(self.macro_outputs)

    @property
    def macrostates(self) -> tuple[MacroState, ...]:
        return tuple(range(self.macrostate_count))

    @property
    def dynamic_interface_certificate(self) -> DynamicInterfaceCertificate:
        return DynamicInterfaceCertificate(self.system, self.macro_labels)

    @property
    def is_dynamic_interface(self) -> bool:
        return self.dynamic_interface_certificate.verify()

    def microstate_for_macrostate(self, macrostate: MacroState) -> int:
        self.validate_macrostate(macrostate)
        return next(state for state, label in enumerate(self.macro_labels) if label == macrostate)

    def validate_macrostate(self, macrostate: MacroState) -> None:
        if not isinstance(macrostate, int) or isinstance(macrostate, bool) or not 0 <= macrostate < self.macrostate_count:
            raise ValueError("macrostate is outside the common macrostate space")

    def induced_transition_table(self) -> tuple[tuple[MacroState, ...], ...]:
        """Return the candidate's macro map after dynamic sufficiency is checked."""
        if not self.is_dynamic_interface:
            raise ValueError("candidate macro labels are not an update-closed dynamic interface")
        return tuple(
            tuple(
                self.macro_labels[self.system.transition(self.microstate_for_macrostate(macrostate), action)]
                for action in self.system.actions
            )
            for macrostate in self.macrostates
        )


@dataclass(frozen=True)
class OpenLawFamily:
    """Retained candidate systems with one declared common macrostate space."""

    candidates: tuple[OpenLawCandidate, ...]

    def __post_init__(self) -> None:
        candidates = _validate_nonempty_tuple(self.candidates, "candidates")
        if any(not isinstance(candidate, OpenLawCandidate) for candidate in candidates):
            raise ValueError("candidates must contain OpenLawCandidate objects")
        identifiers = tuple(candidate.candidate_id for candidate in candidates)
        if len(set(identifiers)) != len(identifiers):
            raise ValueError("candidate identifiers must be unique")
        first = candidates[0]
        for candidate in candidates[1:]:
            if candidate.system.actions != first.system.actions:
                raise ValueError("all candidates must share the same ordered action alphabet")
            if candidate.macro_outputs != first.macro_outputs:
                raise ValueError("all candidates must share the same common macro output map")

    @property
    def actions(self) -> tuple[Action, ...]:
        return self.candidates[0].system.actions

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

    def verify_candidate_interfaces(self) -> bool:
        return all(candidate.is_dynamic_interface for candidate in self.candidates)

    def candidate_transition_table(self, candidate_index: CandidateIndex) -> tuple[tuple[MacroState, ...], ...]:
        if not isinstance(candidate_index, int) or isinstance(candidate_index, bool) or not 0 <= candidate_index < self.candidate_count:
            raise ValueError("candidate index is outside the retained family")
        return self.candidates[candidate_index].induced_transition_table()

    @property
    def response_type_labels(self) -> tuple[ResponseType, ...]:
        if not self.verify_candidate_interfaces():
            raise ValueError("all candidates require valid dynamic interfaces before response types are defined")
        return _canonical_labels(self.candidate_transition_table(index) for index in range(self.candidate_count))

    @property
    def response_type_count(self) -> int:
        return len(set(self.response_type_labels))

    @property
    def response_type_representatives(self) -> tuple[CandidateIndex, ...]:
        representatives: dict[ResponseType, CandidateIndex] = {}
        for candidate_index, response_type in enumerate(self.response_type_labels):
            representatives.setdefault(response_type, candidate_index)
        return tuple(representatives[response_type] for response_type in sorted(representatives))

    def type_of_candidate(self, candidate_index: CandidateIndex) -> ResponseType:
        if not isinstance(candidate_index, int) or isinstance(candidate_index, bool) or not 0 <= candidate_index < self.candidate_count:
            raise ValueError("candidate index is outside the retained family")
        return self.response_type_labels[candidate_index]

    def candidate_for_type(self, response_type: ResponseType) -> OpenLawCandidate:
        if not isinstance(response_type, int) or isinstance(response_type, bool) or not 0 <= response_type < self.response_type_count:
            raise ValueError("response type is outside the retained family")
        return self.candidates[self.response_type_representatives[response_type]]

    def transition_for_type(self, response_type: ResponseType, macrostate: MacroState, action: Action) -> MacroState:
        candidate = self.candidate_for_type(response_type)
        candidate.validate_macrostate(macrostate)
        try:
            action_index = self.actions.index(action)
        except ValueError as error:
            raise ValueError(f"unknown action: {action!r}") from error
        return candidate.induced_transition_table()[macrostate][action_index]

    @property
    def has_universal_open_law(self) -> bool:
        return self.verify_candidate_interfaces() and self.response_type_count == 1

    def universal_transition_table(self) -> tuple[tuple[MacroState, ...], ...]:
        if not self.has_universal_open_law:
            raise ValueError("retained candidates do not share a universal deterministic open law")
        return self.candidate_transition_table(0)

    def set_valued_successor(self, macrostate: MacroState, action: Action) -> frozenset[MacroState]:
        for candidate in self.candidates:
            candidate.validate_macrostate(macrostate)
        if action not in self.actions:
            raise ValueError(f"unknown action: {action!r}")
        return frozenset(
            self.transition_for_type(response_type, macrostate, action)
            for response_type in range(self.response_type_count)
        )

    def candidate_safe_system(self) -> FiniteControlledOutputSystem:
        """Exact deterministic construction on ``(response type, macrostate)``.

        This is a valid candidate-safe open law whenever all individual candidate
        interfaces are dynamic.  It is an explicit deterministic construction,
        not yet a lower-bound claim about the minimal quotient.
        """
        if not self.verify_candidate_interfaces():
            raise ValueError("candidate-safe construction requires dynamic interfaces in every retained candidate")
        rows: list[tuple[int, ...]] = []
        outputs: list[Hashable] = []
        for response_type in range(self.response_type_count):
            for macrostate in self.macrostates:
                rows.append(
                    tuple(
                        response_type * self.macrostate_count
                        + self.transition_for_type(response_type, macrostate, action)
                        for action in self.actions
                    )
                )
                outputs.append(self.macro_outputs[macrostate])
        return FiniteControlledOutputSystem(
            actions=self.actions,
            transition_table=tuple(rows),
            outputs=tuple(outputs),
        )

    def candidate_safe_state_index(self, response_type: ResponseType, macrostate: MacroState) -> int:
        if not isinstance(response_type, int) or isinstance(response_type, bool) or not 0 <= response_type < self.response_type_count:
            raise ValueError("response type is outside the retained family")
        if not isinstance(macrostate, int) or isinstance(macrostate, bool) or not 0 <= macrostate < self.macrostate_count:
            raise ValueError("macrostate is outside the common macrostate space")
        return response_type * self.macrostate_count + macrostate


@dataclass(frozen=True)
class UniversalOpenLawCertificate:
    """Certificate for one dynamic open macro-law shared by all retained candidates."""

    family: OpenLawFamily
    universal_transition_table: tuple[tuple[MacroState, ...], ...]

    @property
    def macro_interface_bits(self) -> float:
        return log2(self.family.macrostate_count)

    def verify(self) -> bool:
        try:
            if not self.family.verify_candidate_interfaces():
                return False
            if not self.family.has_universal_open_law:
                return False
            if self.universal_transition_table != self.family.universal_transition_table():
                return False
            return all(
                candidate.induced_transition_table() == self.universal_transition_table
                for candidate in self.family.candidates
            )
        except ValueError:
            return False


def certify_universal_open_law(family: OpenLawFamily) -> UniversalOpenLawCertificate:
    certificate = UniversalOpenLawCertificate(
        family=family,
        universal_transition_table=family.universal_transition_table(),
    )
    if not certificate.verify():
        raise AssertionError("universal open-law certificate did not verify")
    return certificate


@dataclass(frozen=True)
class UniversalOpenLawObstructionCertificate:
    """One macrostate/action where two dynamic candidate interfaces disagree."""

    family: OpenLawFamily
    left_type: ResponseType
    right_type: ResponseType
    macrostate: MacroState
    action: Action
    left_successor: MacroState
    right_successor: MacroState

    def verify(self) -> bool:
        try:
            if not self.family.verify_candidate_interfaces() or self.left_type == self.right_type:
                return False
            if self.action not in self.family.actions:
                return False
            left = self.family.transition_for_type(self.left_type, self.macrostate, self.action)
            right = self.family.transition_for_type(self.right_type, self.macrostate, self.action)
            return (
                self.left_successor == left
                and self.right_successor == right
                and self.left_successor != self.right_successor
            )
        except ValueError:
            return False


def universal_open_law_obstruction_certificate(family: OpenLawFamily) -> UniversalOpenLawObstructionCertificate:
    """Produce a concrete transition disagreement when universality fails."""
    if not family.verify_candidate_interfaces():
        raise ValueError("all candidates require valid dynamic interfaces")
    if family.has_universal_open_law:
        raise ValueError("a universal open law exists; no obstruction certificate is available")
    for left_type, right_type in combinations(range(family.response_type_count), 2):
        for macrostate in family.macrostates:
            for action in family.actions:
                left = family.transition_for_type(left_type, macrostate, action)
                right = family.transition_for_type(right_type, macrostate, action)
                if left != right:
                    certificate = UniversalOpenLawObstructionCertificate(
                        family=family,
                        left_type=left_type,
                        right_type=right_type,
                        macrostate=macrostate,
                        action=action,
                        left_successor=left,
                        right_successor=right,
                    )
                    if not certificate.verify():
                        raise AssertionError("constructed universal open-law obstruction did not verify")
                    return certificate
    raise AssertionError("distinct response types had no induced-transition obstruction")


@dataclass(frozen=True)
class CandidateSafeOpenLawCertificate:
    """Deterministic open-law construction retaining response type explicitly."""

    family: OpenLawFamily
    candidate_safe_state_count: int
    canonical_block_count: int
    stabilization_horizon: int

    @property
    def response_type_count(self) -> int:
        return self.family.response_type_count

    @property
    def macrostate_count(self) -> int:
        return self.family.macrostate_count

    @property
    def expected_state_count(self) -> int:
        return self.response_type_count * self.macrostate_count

    @property
    def candidate_safe_interface_bits(self) -> float:
        return log2(self.candidate_safe_state_count)

    @property
    def macro_interface_bits(self) -> float:
        return log2(self.macrostate_count)

    @property
    def explicit_response_type_bits(self) -> float:
        return self.candidate_safe_interface_bits - self.macro_interface_bits

    def verify(self) -> bool:
        try:
            if not self.family.verify_candidate_interfaces():
                return False
            system = self.family.candidate_safe_system()
            if self.candidate_safe_state_count != self.expected_state_count:
                return False
            if system.state_count != self.candidate_safe_state_count:
                return False
            identity_labels = tuple(system.states)
            if not DynamicInterfaceCertificate(system, identity_labels).verify():
                return False
            stabilization = certify_finite_horizon_stabilization(system)
            if self.canonical_block_count != stabilization.canonical_block_count:
                return False
            if self.stabilization_horizon != stabilization.stabilization_horizon:
                return False
            if self.canonical_block_count > self.candidate_safe_state_count:
                return False
            return True
        except (AssertionError, ValueError):
            return False


def certify_candidate_safe_open_law(family: OpenLawFamily) -> CandidateSafeOpenLawCertificate:
    system = family.candidate_safe_system()
    stabilization = certify_finite_horizon_stabilization(system)
    certificate = CandidateSafeOpenLawCertificate(
        family=family,
        candidate_safe_state_count=system.state_count,
        canonical_block_count=stabilization.canonical_block_count,
        stabilization_horizon=stabilization.stabilization_horizon,
    )
    if not certificate.verify():
        raise AssertionError("candidate-safe open-law construction did not verify")
    return certificate


@dataclass(frozen=True)
class SetValuedOpenLawCertificate:
    """Exact candidate-forgetting successor relation on the common macrostate."""

    family: OpenLawFamily
    successor_sets: tuple[tuple[frozenset[MacroState], ...], ...]

    @property
    def is_deterministic(self) -> bool:
        return all(len(successors) == 1 for row in self.successor_sets for successors in row)

    def verify(self) -> bool:
        try:
            if not self.family.verify_candidate_interfaces():
                return False
            if len(self.successor_sets) != self.family.macrostate_count:
                return False
            for macrostate, row in enumerate(self.successor_sets):
                if not isinstance(row, tuple) or len(row) != len(self.family.actions):
                    return False
                for action, successors in zip(self.family.actions, row):
                    if successors != self.family.set_valued_successor(macrostate, action):
                        return False
            return self.is_deterministic == self.family.has_universal_open_law
        except ValueError:
            return False


def certify_set_valued_open_law(family: OpenLawFamily) -> SetValuedOpenLawCertificate:
    certificate = SetValuedOpenLawCertificate(
        family=family,
        successor_sets=tuple(
            tuple(family.set_valued_successor(macrostate, action) for action in family.actions)
            for macrostate in family.macrostates
        ),
    )
    if not certificate.verify():
        raise AssertionError("set-valued open-law certificate did not verify")
    return certificate


class OpenLawReportKind(str, Enum):
    """Typed report available after candidate dynamic interfaces are certified."""

    UNIVERSAL_DETERMINISTIC = "UNIVERSAL_DETERMINISTIC"
    CANDIDATE_SAFE_DETERMINISTIC = "CANDIDATE_SAFE_DETERMINISTIC"
    SET_VALUED = "SET_VALUED"


@dataclass(frozen=True)
class TypedOpenLawVerdictCertificate:
    """Report mode determined by map agreement and whether response type is retained."""

    family: OpenLawFamily
    retain_response_type: bool
    kind: OpenLawReportKind

    def verify(self) -> bool:
        try:
            if not self.family.verify_candidate_interfaces():
                return False
            expected = (
                OpenLawReportKind.UNIVERSAL_DETERMINISTIC
                if self.family.has_universal_open_law
                else (
                    OpenLawReportKind.CANDIDATE_SAFE_DETERMINISTIC
                    if self.retain_response_type
                    else OpenLawReportKind.SET_VALUED
                )
            )
            if self.kind is not expected:
                return False
            if self.kind is OpenLawReportKind.UNIVERSAL_DETERMINISTIC:
                return certify_universal_open_law(self.family).verify()
            if self.kind is OpenLawReportKind.CANDIDATE_SAFE_DETERMINISTIC:
                return certify_candidate_safe_open_law(self.family).verify()
            return certify_set_valued_open_law(self.family).verify() and not self.family.has_universal_open_law
        except (AssertionError, ValueError):
            return False


def classify_open_law_family(
    family: OpenLawFamily,
    *,
    retain_response_type: bool,
) -> TypedOpenLawVerdictCertificate:
    if not isinstance(retain_response_type, bool):
        raise ValueError("retain_response_type must be boolean")
    if not family.verify_candidate_interfaces():
        raise ValueError("all candidates require valid dynamic interfaces before reporting a law")
    kind = (
        OpenLawReportKind.UNIVERSAL_DETERMINISTIC
        if family.has_universal_open_law
        else (
            OpenLawReportKind.CANDIDATE_SAFE_DETERMINISTIC
            if retain_response_type
            else OpenLawReportKind.SET_VALUED
        )
    )
    certificate = TypedOpenLawVerdictCertificate(
        family=family,
        retain_response_type=retain_response_type,
        kind=kind,
    )
    if not certificate.verify():
        raise AssertionError("typed open-law verdict certificate did not verify")
    return certificate


@dataclass(frozen=True)
class StructuralQuery:
    """One local action executed after a reader is structurally attached to a port.

    ``port`` is a context attachment, not a symbol in the local action alphabet.
    Every context uses the same local actions in ``LOCAL_ACTIONS``.
    """

    port: int
    action: Action


@dataclass(frozen=True)
class JointOpenCandidateProduct:
    """Canonical structural witness for joint exterior and response-type memory.

    A candidate-safe state is

    ``(inside, exterior_1, ..., exterior_q, response_type)``.

    In every fixed response type, the candidate-specific open macrostate is the
    first ``q + 1`` coordinates.  A structural context attaches a reader to one
    exterior port.  Local semantics are:

    * ``observe`` leaves the inside state unchanged;
    * ``read`` copies the attached exterior coordinate to the focal inside state;
      and
    * ``intervene`` applies the response-type shift ``inside -> inside + r mod I``.

    The mild cardinality condition ``I >= max(E_j, R)`` makes both copied exterior
    values and distinct response-type shifts representable in the focal output.
    """

    inside_cardinality: int
    exterior_cardinalities: tuple[int, ...]
    response_type_count: int

    def __post_init__(self) -> None:
        _validate_positive_integer(self.inside_cardinality, "inside_cardinality")
        exterior = _validate_nonempty_tuple(self.exterior_cardinalities, "exterior_cardinalities")
        for cardinality in exterior:
            if not isinstance(cardinality, int) or isinstance(cardinality, bool) or cardinality < 2:
                raise ValueError("every exterior cardinality must be an integer at least two")
        _validate_positive_integer(self.response_type_count, "response_type_count")
        if self.inside_cardinality < max((*exterior, self.response_type_count)):
            raise ValueError("inside_cardinality must encode every exterior value and response type")

    @property
    def local_actions(self) -> tuple[Action, Action, Action]:
        return LOCAL_ACTIONS

    @property
    def port_count(self) -> int:
        return len(self.exterior_cardinalities)

    @property
    def ports(self) -> tuple[int, ...]:
        return tuple(range(self.port_count))

    @property
    def candidate_macrostate_count(self) -> int:
        return self.inside_cardinality * prod(self.exterior_cardinalities)

    @property
    def joint_state_count(self) -> int:
        return self.candidate_macrostate_count * self.response_type_count

    @property
    def states(self) -> tuple[StructuralState, ...]:
        return tuple(
            product(
                range(self.inside_cardinality),
                *(range(cardinality) for cardinality in self.exterior_cardinalities),
                range(self.response_type_count),
            )
        )

    @property
    def candidate_macrostates(self) -> tuple[tuple[int, ...], ...]:
        return tuple(
            product(
                range(self.inside_cardinality),
                *(range(cardinality) for cardinality in self.exterior_cardinalities),
            )
        )

    @property
    def structural_queries(self) -> tuple[StructuralQuery, ...]:
        return tuple(StructuralQuery(port, action) for port in self.ports for action in self.local_actions)

    def validate_response_type(self, response_type: ResponseType) -> None:
        if not isinstance(response_type, int) or isinstance(response_type, bool) or not 0 <= response_type < self.response_type_count:
            raise ValueError("response type is outside the retained product family")

    def validate_port(self, port: int) -> None:
        if not isinstance(port, int) or isinstance(port, bool) or not 0 <= port < self.port_count:
            raise ValueError("port is outside the structural attachment range")

    def validate_query(self, query: StructuralQuery) -> None:
        if not isinstance(query, StructuralQuery):
            raise ValueError("query must be a StructuralQuery")
        self.validate_port(query.port)
        if query.action not in self.local_actions:
            raise ValueError("query action is outside the fixed local action alphabet")

    def validate_state(self, state: StructuralState) -> None:
        if not isinstance(state, tuple) or len(state) != self.port_count + 2:
            raise ValueError("joint state has the wrong number of coordinates")
        inside, *rest = state
        exterior = rest[:-1]
        response_type = rest[-1]
        if not isinstance(inside, int) or isinstance(inside, bool) or not 0 <= inside < self.inside_cardinality:
            raise ValueError("inside coordinate is outside its range")
        for value, cardinality in zip(exterior, self.exterior_cardinalities):
            if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value < cardinality:
                raise ValueError("exterior coordinate is outside its range")
        self.validate_response_type(response_type)

    def validate_candidate_macrostate(self, macrostate: tuple[int, ...]) -> None:
        if not isinstance(macrostate, tuple) or len(macrostate) != self.port_count + 1:
            raise ValueError("candidate macrostate has the wrong number of coordinates")
        state = macrostate + (0,)
        self.validate_state(state)

    def split_state(self, state: StructuralState) -> tuple[int, tuple[int, ...], ResponseType]:
        self.validate_state(state)
        return state[0], state[1:-1], state[-1]

    def output(self, state: StructuralState) -> int:
        self.validate_state(state)
        return state[0]

    def successor(self, state: StructuralState, query: StructuralQuery) -> StructuralState:
        self.validate_state(state)
        self.validate_query(query)
        inside, exterior, response_type = self.split_state(state)
        if query.action == OBSERVE:
            next_inside = inside
        elif query.action == READ:
            next_inside = exterior[query.port]
        else:
            next_inside = (inside + response_type) % self.inside_cardinality
        return (next_inside,) + exterior + (response_type,)

    def trace(self, state: StructuralState, query: StructuralQuery) -> tuple[int, int]:
        return self.output(state), self.output(self.successor(state, query))

    def candidate_successor(
        self,
        response_type: ResponseType,
        macrostate: tuple[int, ...],
        query: StructuralQuery,
    ) -> tuple[int, ...]:
        self.validate_response_type(response_type)
        self.validate_candidate_macrostate(macrostate)
        successor = self.successor(macrostate + (response_type,), query)
        return successor[:-1]

    def candidate_trace(
        self,
        response_type: ResponseType,
        macrostate: tuple[int, ...],
        query: StructuralQuery,
    ) -> tuple[int, int]:
        self.validate_response_type(response_type)
        self.validate_candidate_macrostate(macrostate)
        return self.trace(macrostate + (response_type,), query)

    def response_signature(self, state: StructuralState, queries: Iterable[StructuralQuery]) -> tuple[tuple[int, int], ...]:
        normalized = tuple(queries)
        if not normalized:
            raise ValueError("joint response grammar must contain at least one structural query")
        return tuple(self.trace(state, query) for query in normalized)

    def joint_partition(self) -> tuple[tuple[StructuralState, ...], ...]:
        buckets: dict[tuple[tuple[int, int], ...], list[StructuralState]] = {}
        for state in self.states:
            buckets.setdefault(self.response_signature(state, self.structural_queries), []).append(state)
        return tuple(sorted((tuple(block) for block in buckets.values()), key=lambda block: block[0]))

    def candidate_partition(self, response_type: ResponseType) -> tuple[tuple[tuple[int, ...], ...], ...]:
        self.validate_response_type(response_type)
        buckets: dict[tuple[tuple[int, int], ...], list[tuple[int, ...]]] = {}
        for macrostate in self.candidate_macrostates:
            signature = tuple(self.candidate_trace(response_type, macrostate, query) for query in self.structural_queries)
            buckets.setdefault(signature, []).append(macrostate)
        return tuple(sorted((tuple(block) for block in buckets.values()), key=lambda block: block[0]))

    def pairwise_separator(self, left: StructuralState, right: StructuralState) -> StructuralQuery:
        """Select a concrete structural query for every unequal joint state pair."""
        self.validate_state(left)
        self.validate_state(right)
        if left == right:
            raise ValueError("a joint separator requires distinct states")
        if left[0] != right[0]:
            return StructuralQuery(0, OBSERVE)
        for port, (left_value, right_value) in enumerate(zip(left[1:-1], right[1:-1])):
            if left_value != right_value:
                return StructuralQuery(port, READ)
        if left[-1] != right[-1]:
            return StructuralQuery(0, INTERVENE)
        raise AssertionError("unequal joint states had no distinguishing coordinate")

    @property
    def has_universal_open_law(self) -> bool:
        return self.response_type_count == 1


@dataclass(frozen=True)
class JointStructuralSeparationCertificate:
    """Concrete structural-context query separating two joint product states."""

    product_family: JointOpenCandidateProduct
    left: StructuralState
    right: StructuralState
    query: StructuralQuery
    left_trace: tuple[int, int]
    right_trace: tuple[int, int]

    def verify(self) -> bool:
        try:
            self.product_family.validate_state(self.left)
            self.product_family.validate_state(self.right)
            if self.left == self.right:
                return False
            self.product_family.validate_query(self.query)
            if self.left_trace != self.product_family.trace(self.left, self.query):
                return False
            if self.right_trace != self.product_family.trace(self.right, self.query):
                return False
            return self.left_trace != self.right_trace
        except ValueError:
            return False


def joint_structural_separator_certificate(
    product_family: JointOpenCandidateProduct,
    left: StructuralState,
    right: StructuralState,
) -> JointStructuralSeparationCertificate:
    query = product_family.pairwise_separator(left, right)
    certificate = JointStructuralSeparationCertificate(
        product_family=product_family,
        left=left,
        right=right,
        query=query,
        left_trace=product_family.trace(left, query),
        right_trace=product_family.trace(right, query),
    )
    if not certificate.verify():
        raise AssertionError("joint structural separating certificate did not verify")
    return certificate


@dataclass(frozen=True)
class JointOpenLawObstructionCertificate:
    """A shared candidate macrostate with incompatible response-type successor."""

    product_family: JointOpenCandidateProduct
    left_type: ResponseType
    right_type: ResponseType
    macrostate: tuple[int, ...]
    query: StructuralQuery
    left_successor: tuple[int, ...]
    right_successor: tuple[int, ...]

    def verify(self) -> bool:
        try:
            self.product_family.validate_response_type(self.left_type)
            self.product_family.validate_response_type(self.right_type)
            if self.left_type == self.right_type:
                return False
            self.product_family.validate_candidate_macrostate(self.macrostate)
            self.product_family.validate_query(self.query)
            left = self.product_family.candidate_successor(self.left_type, self.macrostate, self.query)
            right = self.product_family.candidate_successor(self.right_type, self.macrostate, self.query)
            return (
                self.left_successor == left
                and self.right_successor == right
                and self.left_successor != self.right_successor
            )
        except ValueError:
            return False


def joint_open_law_obstruction_certificate(
    product_family: JointOpenCandidateProduct,
) -> JointOpenLawObstructionCertificate:
    if product_family.has_universal_open_law:
        raise ValueError("one response type gives a universal open law in the canonical family")
    macrostate = tuple(0 for _ in range(product_family.port_count + 1))
    query = StructuralQuery(0, INTERVENE)
    certificate = JointOpenLawObstructionCertificate(
        product_family=product_family,
        left_type=0,
        right_type=1,
        macrostate=macrostate,
        query=query,
        left_successor=product_family.candidate_successor(0, macrostate, query),
        right_successor=product_family.candidate_successor(1, macrostate, query),
    )
    if not certificate.verify():
        raise AssertionError("joint open-law obstruction certificate did not verify")
    return certificate


@dataclass(frozen=True)
class JointExteriorMechanismProductCertificate:
    """Exact joint lower bound under structural-port and mechanism separation.

    The certificate verifies every pair of jointly realizable states by a concrete
    structural query.  This proves an injection of

    ``I x E_1 x ... x E_q x R``

    into the exact joint-safe trace quotient.  The canonical family attains the
    bound exactly.
    """

    product_family: JointOpenCandidateProduct
    fixed_candidate_block_counts: tuple[int, ...]
    joint_block_count: int
    checked_joint_pairs: int

    @property
    def candidate_macrostate_count(self) -> int:
        return self.product_family.candidate_macrostate_count

    @property
    def joint_state_count(self) -> int:
        return self.product_family.joint_state_count

    @property
    def expected_pair_count(self) -> int:
        return self.joint_state_count * (self.joint_state_count - 1) // 2

    @property
    def fixed_candidate_interface_bits(self) -> float:
        return log2(self.candidate_macrostate_count)

    @property
    def joint_safe_interface_bits(self) -> float:
        return log2(self.joint_block_count)

    @property
    def response_type_inflation_bits(self) -> float:
        return self.joint_safe_interface_bits - self.fixed_candidate_interface_bits

    @property
    def joint_product_lower_bound_bits(self) -> float:
        return (
            log2(self.product_family.inside_cardinality)
            + sum(log2(cardinality) for cardinality in self.product_family.exterior_cardinalities)
            + log2(self.product_family.response_type_count)
        )

    def verify(self) -> bool:
        try:
            family = self.product_family
            expected_fixed = tuple(
                len(family.candidate_partition(response_type))
                for response_type in range(family.response_type_count)
            )
            if self.fixed_candidate_block_counts != expected_fixed:
                return False
            if self.fixed_candidate_block_counts != tuple(
                family.candidate_macrostate_count for _ in range(family.response_type_count)
            ):
                return False
            partition = family.joint_partition()
            if self.joint_block_count != len(partition):
                return False
            if self.joint_block_count != family.joint_state_count:
                return False
            if any(len(block) != 1 for block in partition):
                return False
            if self.checked_joint_pairs != self.expected_pair_count:
                return False
            for left, right in combinations(family.states, 2):
                certificate = joint_structural_separator_certificate(family, left, right)
                if not certificate.verify():
                    return False
            if abs(self.joint_safe_interface_bits - self.joint_product_lower_bound_bits) > 1e-12:
                return False
            if abs(self.response_type_inflation_bits - log2(family.response_type_count)) > 1e-12:
                return False
            if family.response_type_count > 1 and not joint_open_law_obstruction_certificate(family).verify():
                return False
            return True
        except (AssertionError, ValueError):
            return False


def certify_joint_exterior_mechanism_product(
    inside_cardinality: int,
    exterior_cardinalities: Iterable[int],
    response_type_count: int,
) -> JointExteriorMechanismProductCertificate:
    try:
        exterior = tuple(exterior_cardinalities)
    except TypeError as error:
        raise ValueError("exterior_cardinalities must be iterable") from error
    family = JointOpenCandidateProduct(
        inside_cardinality=inside_cardinality,
        exterior_cardinalities=exterior,
        response_type_count=response_type_count,
    )
    certificate = JointExteriorMechanismProductCertificate(
        product_family=family,
        fixed_candidate_block_counts=tuple(
            len(family.candidate_partition(response_type))
            for response_type in range(family.response_type_count)
        ),
        joint_block_count=len(family.joint_partition()),
        checked_joint_pairs=family.joint_state_count * (family.joint_state_count - 1) // 2,
    )
    if not certificate.verify():
        raise AssertionError("joint exterior-mechanism product certificate did not verify")
    return certificate


def agreeing_open_law_family() -> OpenLawFamily:
    """Two distinct micro-realizations with one common flip macro-law."""
    left = OpenLawCandidate(
        candidate_id="two-state-flip",
        system=FiniteControlledOutputSystem(
            actions=("step",),
            transition_table=((1,), (0,)),
            outputs=(0, 1),
        ),
        macro_labels=(0, 1),
        macro_outputs=(0, 1),
    )
    right = OpenLawCandidate(
        candidate_id="redundant-three-state-flip",
        system=FiniteControlledOutputSystem(
            actions=("step",),
            transition_table=((2,), (2,), (0,)),
            outputs=(0, 0, 1),
        ),
        macro_labels=(0, 0, 1),
        macro_outputs=(0, 1),
    )
    return OpenLawFamily((left, right))


def conflicting_open_law_family() -> OpenLawFamily:
    """Two dynamic candidates with incompatible induced maps on the same Q."""
    flip = OpenLawCandidate(
        candidate_id="flip",
        system=FiniteControlledOutputSystem(
            actions=("step",),
            transition_table=((1,), (0,)),
            outputs=(0, 1),
        ),
        macro_labels=(0, 1),
        macro_outputs=(0, 1),
    )
    identity = OpenLawCandidate(
        candidate_id="identity",
        system=FiniteControlledOutputSystem(
            actions=("step",),
            transition_table=((0,), (1,)),
            outputs=(0, 1),
        ),
        macro_labels=(0, 1),
        macro_outputs=(0, 1),
    )
    return OpenLawFamily((flip, identity))
