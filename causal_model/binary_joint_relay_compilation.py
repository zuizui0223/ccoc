"""Degree-three compilation of the binary joint exterior--mechanism witness.

The general joint product theorem has macro states

    (inside, exterior_1, ..., exterior_m, response_type)

and distinguishes exterior read from response-type intervention.  Its initial
structural witness is intentionally abstract.  This module compiles the exact
binary subfamily

    (y, b_1, ..., b_m, r) in {0, 1}^{m + 2}

into a bounded-degree, pairwise, constant-local-grammar relay protocol:

* ``observe`` leaves ``y`` unchanged;
* a reader structurally attached to exterior port ``i`` sends ``copy-b_i`` and
  realizes ``y <- b_i``; and
* one fixed response-type leaf sends ``xor-r`` and realizes ``y <- y xor r``.

The local token alphabet is always

    {empty, copy-0, copy-1, xor-0, xor-1}.

It does not grow with the number of exterior ports.  Port identity is a reader
attachment context, not a token or action label.  The response type is stored in
a permanent leaf bit and is encoded only in the constant token value.

This is an exact degree-three compilation of the `I = E_i = R = 2` subfamily of
``joint_open_candidate_laws``: in that subfamily, addition modulo two is XOR.
It deliberately does *not* claim a compiler for arbitrary multi-valued streaming
reads or general modular arithmetic.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import log2
from typing import Mapping

from .joint_open_candidate_laws import (
    INTERVENE,
    OBSERVE,
    READ,
    JointOpenCandidateProduct,
    StructuralQuery,
)
from .relay_tree_compilation import ROOT, RelayTreeTopology

Token = str | None
BinaryJointState = tuple[int, ...]

COPY_0 = "copy-0"
COPY_1 = "copy-1"
XOR_0 = "xor-0"
XOR_1 = "xor-1"
TOKEN_ALPHABET: tuple[Token, str, str, str, str] = (None, COPY_0, COPY_1, XOR_0, XOR_1)


def _validate_positive_integer(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _validate_bit(value: int, name: str) -> None:
    if value not in (0, 1):
        raise ValueError(f"{name} must be 0 or 1")


def copy_token(bit: int) -> str:
    _validate_bit(bit, "copy bit")
    return COPY_1 if bit else COPY_0


def xor_token(bit: int) -> str:
    _validate_bit(bit, "xor bit")
    return XOR_1 if bit else XOR_0


def token_kind(token: Token) -> str | None:
    if token is None:
        return None
    if token in (COPY_0, COPY_1):
        return "copy"
    if token in (XOR_0, XOR_1):
        return "xor"
    raise ValueError("token is outside the fixed binary joint grammar")


def token_bit(token: Token) -> int:
    if token in (COPY_0, XOR_0):
        return 0
    if token in (COPY_1, XOR_1):
        return 1
    raise ValueError("only nonempty fixed-grammar tokens carry a bit")


@dataclass(frozen=True)
class BinaryJointRelayGrammar:
    """One fixed local grammar for every number of exterior ports."""

    reader_states: tuple[str, str] = ("ready", "fire")
    token_alphabet: tuple[Token, str, str, str, str] = TOKEN_ALPHABET
    exterior_leaf_state_count: int = 10  # permanent bit times transient token
    response_leaf_state_count: int = 10
    relay_state_count: int = 5
    root_state_count: int = 2
    maximum_degree: int = 3

    def verify(self) -> bool:
        return (
            self.reader_states == ("ready", "fire")
            and self.token_alphabet == TOKEN_ALPHABET
            and self.exterior_leaf_state_count == 10
            and self.response_leaf_state_count == 10
            and self.relay_state_count == 5
            and self.root_state_count == 2
            and self.maximum_degree == 3
        )


def binary_joint_relay_grammar() -> BinaryJointRelayGrammar:
    grammar = BinaryJointRelayGrammar()
    if not grammar.verify():
        raise AssertionError("binary joint relay grammar did not verify")
    return grammar


@dataclass(frozen=True)
class BinaryJointRelayTopology:
    """Binary relay tree with exterior leaves plus one fixed response-type leaf."""

    exterior_port_count: int
    tree: RelayTreeTopology

    def __post_init__(self) -> None:
        _validate_positive_integer(self.exterior_port_count, "exterior_port_count")
        if self.tree.module_count != self.exterior_port_count + 1:
            raise ValueError("tree must contain one exterior leaf per port plus one response leaf")
        if not self.tree.verify():
            raise ValueError("underlying relay tree topology must verify")

    @classmethod
    def balanced(cls, exterior_port_count: int) -> "BinaryJointRelayTopology":
        _validate_positive_integer(exterior_port_count, "exterior_port_count")
        topology = cls(
            exterior_port_count=exterior_port_count,
            tree=RelayTreeTopology.balanced(exterior_port_count + 1),
        )
        if not topology.verify():
            raise AssertionError("constructed binary joint relay topology did not verify")
        return topology

    @property
    def exterior_leaves(self) -> tuple[str, ...]:
        return self.tree.leaves[: self.exterior_port_count]

    @property
    def response_leaf(self) -> str:
        return self.tree.leaves[self.exterior_port_count]

    @property
    def response_leaf_index(self) -> int:
        return self.exterior_port_count

    @property
    def settling_ticks(self) -> int:
        return self.tree.settling_ticks

    def validate_read_port(self, port: int) -> None:
        if not isinstance(port, int) or isinstance(port, bool) or not 0 <= port < self.exterior_port_count:
            raise ValueError(f"read port must be an integer in [0, {self.exterior_port_count - 1}]")

    def reader_attachment_edge(self, port: int) -> tuple[str, str]:
        self.validate_read_port(port)
        return self.tree.reader_attachment_edge(port)

    @property
    def response_attachment_edge(self) -> tuple[str, str]:
        return self.tree.reader_attachment_edge(self.response_leaf_index)

    def maximum_degree_for_read(self, port: int) -> int:
        self.validate_read_port(port)
        return self.tree.maximum_degree_with_reader(port)

    @property
    def maximum_degree_for_intervene(self) -> int:
        return self.tree.maximum_degree_with_reader(self.response_leaf_index)

    def verify(self) -> bool:
        try:
            _validate_positive_integer(self.exterior_port_count, "exterior_port_count")
            if not self.tree.verify():
                return False
            if self.tree.module_count != self.exterior_port_count + 1:
                return False
            if self.exterior_leaves != tuple(f"leaf:{index}" for index in range(self.exterior_port_count)):
                return False
            if self.response_leaf != f"leaf:{self.exterior_port_count}":
                return False
            if any(self.maximum_degree_for_read(port) > 3 for port in range(self.exterior_port_count)):
                return False
            return self.maximum_degree_for_intervene <= 3
        except ValueError:
            return False


@dataclass(frozen=True)
class BinaryJointRelayConfiguration:
    """Micro configuration; only quiescent configurations are macro states."""

    focal_output: int
    exterior_bits: tuple[int, ...]
    response_type: int
    leaf_tokens: tuple[Token, ...]
    relay_tokens: tuple[Token, ...]


def validate_configuration(
    topology: BinaryJointRelayTopology,
    configuration: BinaryJointRelayConfiguration,
) -> None:
    if not topology.verify():
        raise ValueError("topology must verify before configurations can be used")
    _validate_bit(configuration.focal_output, "focal_output")
    _validate_bit(configuration.response_type, "response_type")
    if len(configuration.exterior_bits) != topology.exterior_port_count:
        raise ValueError("exterior_bits must contain one bit per exterior port")
    if len(configuration.leaf_tokens) != topology.tree.module_count:
        raise ValueError("leaf_tokens must contain one token per exterior/response leaf")
    if len(configuration.relay_tokens) != topology.tree.relay_count:
        raise ValueError("relay_tokens must contain one token per relay")
    for index, bit in enumerate(configuration.exterior_bits):
        _validate_bit(bit, f"exterior_bits[{index}]")
    for index, token in enumerate(configuration.leaf_tokens):
        if token not in TOKEN_ALPHABET:
            raise ValueError(f"leaf_tokens[{index}] is outside the fixed token alphabet")
    for index, token in enumerate(configuration.relay_tokens):
        if token not in TOKEN_ALPHABET:
            raise ValueError(f"relay_tokens[{index}] is outside the fixed token alphabet")


def quiescent_configuration(
    topology: BinaryJointRelayTopology,
    focal_output: int,
    exterior_bits: tuple[int, ...],
    response_type: int,
) -> BinaryJointRelayConfiguration:
    configuration = BinaryJointRelayConfiguration(
        focal_output=focal_output,
        exterior_bits=tuple(exterior_bits),
        response_type=response_type,
        leaf_tokens=(None,) * topology.tree.module_count,
        relay_tokens=(None,) * topology.tree.relay_count,
    )
    validate_configuration(topology, configuration)
    return configuration


def is_quiescent(topology: BinaryJointRelayTopology, configuration: BinaryJointRelayConfiguration) -> bool:
    validate_configuration(topology, configuration)
    return all(token is None for token in configuration.leaf_tokens) and all(
        token is None for token in configuration.relay_tokens
    )


def macro_state(configuration: BinaryJointRelayConfiguration) -> BinaryJointState:
    return (configuration.focal_output,) + configuration.exterior_bits + (configuration.response_type,)


def configuration_from_macro_state(
    topology: BinaryJointRelayTopology,
    state: BinaryJointState,
) -> BinaryJointRelayConfiguration:
    if not isinstance(state, tuple) or len(state) != topology.exterior_port_count + 2:
        raise ValueError("binary joint macro state has the wrong number of coordinates")
    focal_output, *rest = state
    exterior_bits = tuple(rest[:-1])
    response_type = rest[-1]
    return quiescent_configuration(topology, focal_output, exterior_bits, response_type)


def _token_at_node(
    topology: BinaryJointRelayTopology,
    configuration: BinaryJointRelayConfiguration,
    node: str,
) -> Token:
    tree = topology.tree
    if node in tree.leaves:
        return configuration.leaf_tokens[tree.leaves.index(node)]
    if node in tree.relays:
        return configuration.relay_tokens[tree.relays.index(node)]
    if node == ROOT:
        return None
    raise ValueError("node is not in the binary joint relay topology")


def directed_edge_tokens(
    topology: BinaryJointRelayTopology,
    configuration: BinaryJointRelayConfiguration,
) -> Mapping[tuple[str, str], Token]:
    validate_configuration(topology, configuration)
    return {
        (child, parent): _token_at_node(topology, configuration, child)
        for child, parent in topology.tree.message_edges
    }


def _unique_nonempty(tokens: tuple[Token, ...]) -> Token:
    nonempty = tuple(token for token in tokens if token is not None)
    if len(nonempty) > 1:
        raise ValueError("the declared one-token protocol forbids simultaneous incoming tokens")
    return nonempty[0] if nonempty else None


def _root_successor(current_output: int, token: Token) -> int:
    _validate_bit(current_output, "current root output")
    if token is None:
        return current_output
    kind = token_kind(token)
    value = token_bit(token)
    if kind == "copy":
        return value
    if kind == "xor":
        return current_output ^ value
    raise AssertionError("nonempty fixed token had no root interpretation")


@dataclass(frozen=True)
class BinaryJointMacroAction:
    """Declared macro action plus structural attachment context for a read."""

    kind: str
    read_port: int | None = None

    @classmethod
    def observe(cls) -> "BinaryJointMacroAction":
        return cls(OBSERVE)

    @classmethod
    def read(cls, port: int) -> "BinaryJointMacroAction":
        return cls(READ, port)

    @classmethod
    def intervene(cls) -> "BinaryJointMacroAction":
        return cls(INTERVENE)

    def validate(self, topology: BinaryJointRelayTopology) -> None:
        if self.kind == OBSERVE:
            if self.read_port is not None:
                raise ValueError("observe has no reader attachment")
            return
        if self.kind == READ:
            if self.read_port is None:
                raise ValueError("read requires one structural exterior-port attachment")
            topology.validate_read_port(self.read_port)
            return
        if self.kind == INTERVENE:
            if self.read_port is not None:
                raise ValueError("intervene uses the fixed response-type leaf, not an exterior port")
            return
        raise ValueError("macro action must be observe, read, or intervene")

    def source_leaf_index(self, topology: BinaryJointRelayTopology) -> int:
        self.validate(topology)
        if self.kind == READ:
            assert self.read_port is not None
            return self.read_port
        if self.kind == INTERVENE:
            return topology.response_leaf_index
        raise ValueError("observe has no source leaf")


def micro_step(
    topology: BinaryJointRelayTopology,
    configuration: BinaryJointRelayConfiguration,
    initiation: BinaryJointMacroAction | None = None,
) -> BinaryJointRelayConfiguration:
    """Advance one local synchronous tick of the declared sequential protocol."""
    validate_configuration(topology, configuration)
    if initiation is not None:
        initiation.validate(topology)
        if initiation.kind == OBSERVE:
            raise ValueError("observe is a quiescent macro no-op and starts no token protocol")
        if not is_quiescent(topology, configuration):
            raise ValueError("a reader or intervention token may start only at quiescence")

    messages = directed_edge_tokens(topology, configuration)
    if initiation is None:
        next_leaf_tokens = (None,) * topology.tree.module_count
    elif initiation.kind == READ:
        assert initiation.read_port is not None
        next_leaf_tokens = tuple(
            copy_token(configuration.exterior_bits[index]) if index == initiation.read_port else None
            for index in range(topology.tree.module_count)
        )
    else:
        next_leaf_tokens = tuple(
            xor_token(configuration.response_type) if index == topology.response_leaf_index else None
            for index in range(topology.tree.module_count)
        )

    next_relay_tokens: list[Token] = []
    for relay in topology.tree.relays:
        incoming = tuple(messages[(child, relay)] for child in topology.tree.children_by_node[relay])
        next_relay_tokens.append(_unique_nonempty(incoming))
    root_child = topology.tree.children_by_node[ROOT][0]
    next_output = _root_successor(configuration.focal_output, messages[(root_child, ROOT)])

    result = BinaryJointRelayConfiguration(
        focal_output=next_output,
        exterior_bits=configuration.exterior_bits,
        response_type=configuration.response_type,
        leaf_tokens=tuple(next_leaf_tokens),
        relay_tokens=tuple(next_relay_tokens),
    )
    validate_configuration(topology, result)
    return result


def protocol_trajectory(
    topology: BinaryJointRelayTopology,
    initial: BinaryJointRelayConfiguration,
    action: BinaryJointMacroAction,
) -> tuple[BinaryJointRelayConfiguration, ...]:
    """Run one non-observe macro action until its universal quiescent boundary."""
    action.validate(topology)
    validate_configuration(topology, initial)
    if action.kind == OBSERVE:
        return (initial,)
    if not is_quiescent(topology, initial):
        raise ValueError("a macro action must start at a quiescent configuration")
    trajectory = [initial]
    current = initial
    for tick in range(topology.settling_ticks):
        current = micro_step(topology, current, initiation=action if tick == 0 else None)
        trajectory.append(current)
    if not is_quiescent(topology, trajectory[-1]):
        raise AssertionError("declared settling horizon did not restore quiescence")
    return tuple(trajectory)


def run_macro_action(
    topology: BinaryJointRelayTopology,
    initial: BinaryJointRelayConfiguration,
    action: BinaryJointMacroAction,
) -> BinaryJointRelayConfiguration:
    return protocol_trajectory(topology, initial, action)[-1]


def binary_joint_product(exterior_port_count: int) -> JointOpenCandidateProduct:
    _validate_positive_integer(exterior_port_count, "exterior_port_count")
    return JointOpenCandidateProduct(
        inside_cardinality=2,
        exterior_cardinalities=(2,) * exterior_port_count,
        response_type_count=2,
    )


def expected_macro_successor(
    topology: BinaryJointRelayTopology,
    state: BinaryJointState,
    action: BinaryJointMacroAction,
) -> BinaryJointState:
    action.validate(topology)
    family = binary_joint_product(topology.exterior_port_count)
    if action.kind == OBSERVE:
        query = StructuralQuery(0, OBSERVE)
    elif action.kind == READ:
        assert action.read_port is not None
        query = StructuralQuery(action.read_port, READ)
    else:
        query = StructuralQuery(0, INTERVENE)
    return family.successor(state, query)


def all_binary_joint_states(exterior_port_count: int) -> tuple[BinaryJointState, ...]:
    _validate_positive_integer(exterior_port_count, "exterior_port_count")
    return tuple(product((0, 1), repeat=exterior_port_count + 2))


@dataclass(frozen=True)
class BinaryJointRelayProtocolCertificate:
    """Replayable macro-time conjugacy certificate for one state and one action."""

    topology: BinaryJointRelayTopology
    initial: BinaryJointRelayConfiguration
    action: BinaryJointMacroAction
    trajectory: tuple[BinaryJointRelayConfiguration, ...]
    expected_successor: BinaryJointState

    @property
    def source_leaf_index(self) -> int | None:
        if self.action.kind == OBSERVE:
            return None
        return self.action.source_leaf_index(self.topology)

    @property
    def final(self) -> BinaryJointRelayConfiguration:
        return self.trajectory[-1]

    def verify(self) -> bool:
        try:
            if not binary_joint_relay_grammar().verify() or not self.topology.verify():
                return False
            self.action.validate(self.topology)
            validate_configuration(self.topology, self.initial)
            if not is_quiescent(self.topology, self.initial):
                return False
            if self.expected_successor != expected_macro_successor(
                self.topology, macro_state(self.initial), self.action
            ):
                return False
            expected_trajectory = protocol_trajectory(self.topology, self.initial, self.action)
            if self.trajectory != expected_trajectory:
                return False
            if macro_state(self.final) != self.expected_successor:
                return False
            if not is_quiescent(self.topology, self.final):
                return False
            if self.action.kind == OBSERVE:
                return self.trajectory == (self.initial,)
            source_index = self.source_leaf_index
            assert source_index is not None
            if len(self.trajectory) != self.topology.settling_ticks + 1:
                return False
            first_step = self.trajectory[1]
            if sum(token is not None for token in first_step.leaf_tokens) != 1:
                return False
            if first_step.leaf_tokens[source_index] is None:
                return False
            if self.action.kind == READ and token_kind(first_step.leaf_tokens[source_index]) != "copy":
                return False
            if self.action.kind == INTERVENE and token_kind(first_step.leaf_tokens[source_index]) != "xor":
                return False
            if self.action.kind == READ:
                assert self.action.read_port is not None
                if self.topology.maximum_degree_for_read(self.action.read_port) > 3:
                    return False
            if self.action.kind == INTERVENE and self.topology.maximum_degree_for_intervene > 3:
                return False
            return True
        except (AssertionError, ValueError):
            return False


def certify_binary_joint_relay_protocol(
    topology: BinaryJointRelayTopology,
    state: BinaryJointState,
    action: BinaryJointMacroAction,
) -> BinaryJointRelayProtocolCertificate:
    action.validate(topology)
    initial = configuration_from_macro_state(topology, state)
    certificate = BinaryJointRelayProtocolCertificate(
        topology=topology,
        initial=initial,
        action=action,
        trajectory=protocol_trajectory(topology, initial, action),
        expected_successor=expected_macro_successor(topology, state, action),
    )
    if not certificate.verify():
        raise AssertionError("binary joint relay protocol certificate did not verify")
    return certificate


@dataclass(frozen=True)
class BinaryJointRelayCompilationCertificate:
    """Exact degree-three compilation certificate for the binary joint subfamily."""

    topology: BinaryJointRelayTopology
    checked_macro_state_count: int
    checked_observe_protocols: int
    checked_read_protocols: int
    checked_intervene_protocols: int

    @property
    def expected_macro_state_count(self) -> int:
        return 2 ** (self.topology.exterior_port_count + 2)

    @property
    def expected_read_protocol_count(self) -> int:
        return self.expected_macro_state_count * self.topology.exterior_port_count

    @property
    def joint_safe_interface_bits(self) -> float:
        return log2(self.expected_macro_state_count)

    @property
    def maximum_degree(self) -> int:
        return max(
            *(self.topology.maximum_degree_for_read(port) for port in range(self.topology.exterior_port_count)),
            self.topology.maximum_degree_for_intervene,
        )

    def verify(self) -> bool:
        try:
            if not binary_joint_relay_grammar().verify() or not self.topology.verify():
                return False
            if self.checked_macro_state_count != self.expected_macro_state_count:
                return False
            if self.checked_observe_protocols != self.expected_macro_state_count:
                return False
            if self.checked_read_protocols != self.expected_read_protocol_count:
                return False
            if self.checked_intervene_protocols != self.expected_macro_state_count:
                return False
            if self.maximum_degree > 3:
                return False
            states = all_binary_joint_states(self.topology.exterior_port_count)
            if len(states) != self.expected_macro_state_count:
                return False
            for state in states:
                if not certify_binary_joint_relay_protocol(
                    self.topology, state, BinaryJointMacroAction.observe()
                ).verify():
                    return False
                if not certify_binary_joint_relay_protocol(
                    self.topology, state, BinaryJointMacroAction.intervene()
                ).verify():
                    return False
                for port in range(self.topology.exterior_port_count):
                    if not certify_binary_joint_relay_protocol(
                        self.topology, state, BinaryJointMacroAction.read(port)
                    ).verify():
                        return False
            return True
        except (AssertionError, ValueError):
            return False


def certify_binary_joint_relay_compilation(
    exterior_port_count: int,
) -> BinaryJointRelayCompilationCertificate:
    topology = BinaryJointRelayTopology.balanced(exterior_port_count)
    certificate = BinaryJointRelayCompilationCertificate(
        topology=topology,
        checked_macro_state_count=2 ** (exterior_port_count + 2),
        checked_observe_protocols=2 ** (exterior_port_count + 2),
        checked_read_protocols=exterior_port_count * 2 ** (exterior_port_count + 2),
        checked_intervene_protocols=2 ** (exterior_port_count + 2),
    )
    if not certificate.verify():
        raise AssertionError("binary joint relay compilation certificate did not verify")
    return certificate


def exhaustive_binary_joint_compilation_summary(max_exterior_port_count: int) -> tuple[BinaryJointRelayCompilationCertificate, ...]:
    _validate_positive_integer(max_exterior_port_count, "max_exterior_port_count")
    return tuple(
        certify_binary_joint_relay_compilation(exterior_port_count)
        for exterior_port_count in range(1, max_exterior_port_count + 1)
    )
