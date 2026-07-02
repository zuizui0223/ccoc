"""Portable macro-laws across finite non-nested replacement families.

The nested portability ladder uses stage embeddings. Replacement, extinction,
and rewiring can instead move between finite controlled systems with no inclusion
map from one raw state space to the next.

This module contains two positive finite-domain certificates.

* ``ReplacementTransport`` verifies preservation of one already-supplied common
  macro-law across a declared replacement edge.
* ``TransportedTargetProjectionCertificate`` is stronger at one edge: from an
  exact source projection and a total, label-consistent, output/legal-action
  preserving, successor-closed transport relation, it *constructs* the exact
  target projection. The target labels are not supplied as an assumption.

The latter does not classify arbitrary rewiring. In particular, a newly legal
action may invalidate the equal-legality transport premise; the local
``ReplacementFiberSplitObstructionCertificate`` records that case without
claiming global memory growth.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable, Iterable

from .coherent_portable_macrolaw import PortableMacroDynamics, StageMacroProjection
from .grammar_aware_blankets import GrammarAwareDynamicInterfaceCertificate
from .shared_grammar import FinitePrefixGrammar, GrammarAwareControlledSystem
from .dynamic_boundary_blankets import FiniteControlledOutputSystem


Pair = tuple[int, int]


def _pair_at(system: GrammarAwareControlledSystem, index: int) -> tuple[int, int]:
    if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < system.product_state_count:
        raise ValueError("product index is outside the constrained system")
    return index // system.grammar.state_count, index % system.grammar.state_count


def _successor_index(system: GrammarAwareControlledSystem, index: int, action: str) -> int:
    state, grammar_state = _pair_at(system, index)
    return system.product_index((system.system.transition(state, action), system.grammar.transition(grammar_state, action)))


def _trace(system: GrammarAwareControlledSystem, index: int, word: tuple[str, ...]) -> tuple[Hashable, ...]:
    state, grammar_state = _pair_at(system, index)
    trace: list[Hashable] = [system.system.output(state)]
    for action in word:
        state = system.system.transition(state, action)
        grammar_state = system.grammar.transition(grammar_state, action)
        trace.append(system.system.output(state))
    return tuple(trace)


def _canonical_labels(labels: Iterable[int], count: int) -> tuple[int, ...]:
    try:
        values = tuple(labels)
    except TypeError as error:
        raise ValueError("summary labels must be iterable") from error
    if len(values) != count or not values:
        raise ValueError("summary labels must provide one nonempty entry per product state")
    if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in values):
        raise ValueError("summary labels must be non-negative integers")
    if tuple(sorted(set(values))) != tuple(range(max(values) + 1)):
        raise ValueError("summary labels must be canonical and contiguous")
    return values


def _normalize_relation(relation: Iterable[Pair]) -> tuple[Pair, ...]:
    try:
        pairs = tuple(relation)
    except TypeError as error:
        raise ValueError("transport relation must be iterable") from error
    if not pairs:
        raise ValueError("transport relation must be nonempty")
    if any(
        not isinstance(pair, tuple)
        or len(pair) != 2
        or any(not isinstance(index, int) or isinstance(index, bool) for index in pair)
        for pair in pairs
    ):
        raise ValueError("transport relation entries must be pairs of integer product indices")
    if tuple(sorted(set(pairs))) != pairs:
        raise ValueError("transport relation must be unique and lexicographically sorted")
    return pairs


@dataclass(frozen=True)
class ReplacementTransport:
    """A total successor-closed relation between two non-nested projected stages.

    The relation is allowed to be many-to-one or one-to-many. It is therefore a
    transport witness rather than an inclusion embedding. Every paired state must
    agree in output, legal actions, and macro label; every paired legal successor
    must again occur in the relation.
    """

    source: StageMacroProjection
    target: StageMacroProjection
    relation: tuple[Pair, ...]

    @property
    def source_indices(self) -> tuple[int, ...]:
        return tuple(source_index for source_index, _ in self.relation)

    @property
    def target_indices(self) -> tuple[int, ...]:
        return tuple(target_index for _, target_index in self.relation)

    @property
    def is_source_injective(self) -> bool:
        """Whether this transport happens to be a source-to-target injection."""
        return len(self.relation) == self.source.constrained_system.product_state_count and len(set(self.target_indices)) == len(self.target_indices)

    def verify(self) -> bool:
        try:
            if not self.source.verify() or not self.target.verify():
                return False
            if self.source.induced_macro() != self.target.induced_macro():
                return False
            relation = _normalize_relation(self.relation)
            if relation != self.relation:
                return False
            source_system = self.source.constrained_system
            target_system = self.target.constrained_system
            if source_system.system.actions != target_system.system.actions:
                return False
            if set(self.source_indices) != set(range(source_system.product_state_count)):
                return False
            if set(self.target_indices) != set(range(target_system.product_state_count)):
                return False
            relation_set = set(relation)
            for source_index, target_index in relation:
                source_state, source_grammar = _pair_at(source_system, source_index)
                target_state, target_grammar = _pair_at(target_system, target_index)
                if self.source.summary_labels[source_index] != self.target.summary_labels[target_index]:
                    return False
                if source_system.system.output(source_state) != target_system.system.output(target_state):
                    return False
                source_legal = source_system.grammar.legal_actions(source_grammar)
                target_legal = target_system.grammar.legal_actions(target_grammar)
                if source_legal != target_legal:
                    return False
                for action in source_legal:
                    if (_successor_index(source_system, source_index, action), _successor_index(target_system, target_index, action)) not in relation_set:
                        return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


@dataclass(frozen=True)
class TransportedTargetProjectionCertificate:
    """Construct an exact target projection from one exact source projection.

    Let ``q_source`` be the source summary. The relation must cover both declared
    product state spaces, preserve output and *equal* legal-action rows, and be
    successor-closed. In addition, every target state may relate only to source
    states with one common ``q_source`` label. The induced label

    ``q_target(t) = q_source(s)`` for any ``(s, t)`` in the relation

    is therefore well-defined. The certificate verifies that this constructed
    target label vector is a grammar-aware exact interface and induces precisely
    the source macro dynamics.
    """

    source: StageMacroProjection
    target_system: GrammarAwareControlledSystem
    relation: tuple[Pair, ...]

    @property
    def source_indices(self) -> tuple[int, ...]:
        return tuple(source_index for source_index, _ in self.relation)

    @property
    def target_indices(self) -> tuple[int, ...]:
        return tuple(target_index for _, target_index in self.relation)

    def _derive_target_labels(self) -> tuple[int, ...]:
        if not self.source.verify():
            raise ValueError("source must be an exact grammar-aware projection")
        relation = _normalize_relation(self.relation)
        if relation != self.relation:
            raise ValueError("transport relation must be canonical")
        source_system = self.source.constrained_system
        target_system = self.target_system
        if source_system.system.actions != target_system.system.actions:
            raise ValueError("source and target action alphabets must agree")
        if any(
            not 0 <= source_index < source_system.product_state_count
            or not 0 <= target_index < target_system.product_state_count
            for source_index, target_index in relation
        ):
            raise ValueError("transport relation contains an out-of-range product index")
        if set(self.source_indices) != set(range(source_system.product_state_count)):
            raise ValueError("transport relation must cover every source product state")
        if set(self.target_indices) != set(range(target_system.product_state_count)):
            raise ValueError("transport relation must cover every target product state")

        target_labels: list[int | None] = [None] * target_system.product_state_count
        relation_set = set(relation)
        for source_index, target_index in relation:
            source_state, source_grammar = _pair_at(source_system, source_index)
            target_state, target_grammar = _pair_at(target_system, target_index)
            source_label = self.source.summary_labels[source_index]
            existing = target_labels[target_index]
            if existing is None:
                target_labels[target_index] = source_label
            elif existing != source_label:
                raise ValueError("transport relation is not label-consistent on a target fiber")
            if source_system.system.output(source_state) != target_system.system.output(target_state):
                raise ValueError("transport relation must preserve current output")
            source_legal = source_system.grammar.legal_actions(source_grammar)
            target_legal = target_system.grammar.legal_actions(target_grammar)
            if source_legal != target_legal:
                raise ValueError("transport relation must preserve equal legal-action rows")
            for action in source_legal:
                successor_pair = (
                    _successor_index(source_system, source_index, action),
                    _successor_index(target_system, target_index, action),
                )
                if successor_pair not in relation_set:
                    raise ValueError("transport relation is not successor-closed")

        if any(label is None for label in target_labels):
            raise AssertionError("target coverage must assign one label to every target state")
        labels = tuple(int(label) for label in target_labels if label is not None)
        return _canonical_labels(labels, target_system.product_state_count)

    @property
    def target_labels(self) -> tuple[int, ...]:
        """The target labels constructed from source labels and the relation."""
        return self._derive_target_labels()

    @property
    def target_projection(self) -> StageMacroProjection:
        """The constructed exact target projection, available after verification."""
        projection = StageMacroProjection(self.target_system, self.target_labels)
        if not projection.verify():
            raise AssertionError("derived target labels failed exact-interface verification")
        return projection

    def verify(self) -> bool:
        try:
            if not self.source.verify():
                return False
            target = self.target_projection
            return target.induced_macro() == self.source.induced_macro()
        except (AssertionError, TypeError, ValueError):
            return False


def certify_transported_target_projection(
    source: StageMacroProjection,
    target_system: GrammarAwareControlledSystem,
    relation: Iterable[Pair],
) -> TransportedTargetProjectionCertificate:
    """Certify and return a target projection constructed by finite transport."""
    certificate = TransportedTargetProjectionCertificate(source, target_system, tuple(relation))
    if not certificate.verify():
        raise ValueError("source projection and transport do not construct an exact target projection")
    return certificate


@dataclass(frozen=True)
class TransportCoherentPortableMacroLawCertificate:
    """One macro-law shared across a connected declared replacement family."""

    macro: PortableMacroDynamics
    stages: tuple[StageMacroProjection, ...]
    transports: tuple[ReplacementTransport, ...]

    def verify(self) -> bool:
        try:
            if not self.macro.verify() or len(self.stages) < 2 or not self.transports:
                return False
            if any(not stage.verify() or stage.induced_macro() != self.macro for stage in self.stages):
                return False
            if len(set(id(stage) for stage in self.stages)) != len(self.stages):
                return False
            adjacency = {index: set() for index in range(len(self.stages))}
            for transport in self.transports:
                if not transport.verify():
                    return False
                try:
                    source_index = self.stages.index(transport.source)
                    target_index = self.stages.index(transport.target)
                except ValueError:
                    return False
                if source_index == target_index:
                    return False
                adjacency[source_index].add(target_index)
                adjacency[target_index].add(source_index)
            reached = {0}
            frontier = [0]
            while frontier:
                source_index = frontier.pop()
                for target_index in adjacency[source_index]:
                    if target_index not in reached:
                        reached.add(target_index)
                        frontier.append(target_index)
            return reached == set(range(len(self.stages)))
        except (AssertionError, TypeError, ValueError):
            return False


def certify_transport_coherent_portable_macro_law(
    macro: PortableMacroDynamics,
    stages: Iterable[StageMacroProjection],
    transports: Iterable[ReplacementTransport],
) -> TransportCoherentPortableMacroLawCertificate:
    """Certify a finite non-nested replacement family with one macro-law."""
    certificate = TransportCoherentPortableMacroLawCertificate(macro, tuple(stages), tuple(transports))
    if not certificate.verify():
        raise ValueError("stages and replacement transports do not realize one portable macro-law")
    return certificate


def non_nested_replacement_witness() -> TransportCoherentPortableMacroLawCertificate:
    """Positive witness with three old states replaced by two new states.

    There can be no source-to-target injection because the source has three
    product states and the target has two. The many-to-one relation nevertheless
    preserves the same two-state macro dynamics exactly.
    """
    actions = ("flip",)
    macro = PortableMacroDynamics(
        actions=actions,
        outputs=("low", "high"),
        legal_action_rows=(actions, actions),
        transition_rows=((1,), (0,)),
    )
    grammar = FinitePrefixGrammar(actions=actions, transition_table=((0,),))
    source = StageMacroProjection(
        GrammarAwareControlledSystem(
            FiniteControlledOutputSystem(
                actions=actions,
                transition_table=((2,), (2,), (0,)),
                outputs=("low", "low", "high"),
            ),
            grammar,
        ),
        (0, 0, 1),
    )
    target = StageMacroProjection(
        GrammarAwareControlledSystem(
            FiniteControlledOutputSystem(
                actions=actions,
                transition_table=((1,), (0,)),
                outputs=("low", "high"),
            ),
            grammar,
        ),
        (0, 1),
    )
    transport = ReplacementTransport(source=source, target=target, relation=((0, 0), (1, 0), (2, 1)))
    certificate = certify_transport_coherent_portable_macro_law(macro, (source, target), (transport,))
    if not certificate.verify() or transport.is_source_injective:
        raise AssertionError("non-nested replacement witness did not verify")
    return certificate


def transported_target_projection_witness() -> TransportedTargetProjectionCertificate:
    """Construct the old witness target projection without supplying target labels."""
    existing = non_nested_replacement_witness()
    transport = existing.transports[0]
    certificate = certify_transported_target_projection(
        transport.source,
        transport.target.constrained_system,
        transport.relation,
    )
    if (
        not certificate.verify()
        or certificate.target_labels != transport.target.summary_labels
        or certificate.target_projection.induced_macro() != transport.source.induced_macro()
    ):
        raise AssertionError("transported target projection witness did not verify")
    return certificate


@dataclass(frozen=True)
class ReplacementFiberSplitObstructionCertificate:
    """A newly legal word after replacement refutes one proposed carried merge.

    ``relation`` transports the old states that existed before replacement. It need
    not cover newly created target states. The certificate shows that two old
    states merged by the source summary and by a proposed target summary are
    separated by a word that was illegal before replacement and legal afterward.
    """

    source: StageMacroProjection
    target_system: GrammarAwareControlledSystem
    proposed_target_labels: tuple[int, ...]
    relation: tuple[Pair, ...]
    left_source_index: int
    right_source_index: int
    future_word: tuple[str, ...]

    def verify(self) -> bool:
        try:
            if not self.source.verify():
                return False
            source_system = self.source.constrained_system
            target_system = self.target_system
            if source_system.system.actions != target_system.system.actions:
                return False
            labels = _canonical_labels(self.proposed_target_labels, target_system.product_state_count)
            if labels != self.proposed_target_labels:
                return False
            relation = _normalize_relation(self.relation)
            if relation != self.relation or set(source_index for source_index, _ in relation) != set(range(source_system.product_state_count)):
                return False
            relation_map = dict(relation)
            if len(relation_map) != len(relation):
                return False
            for source_index, target_index in relation:
                source_state, source_grammar = _pair_at(source_system, source_index)
                target_state, target_grammar = _pair_at(target_system, target_index)
                if not 0 <= target_index < target_system.product_state_count:
                    return False
                if self.source.summary_labels[source_index] != labels[target_index]:
                    return False
                if source_system.system.output(source_state) != target_system.system.output(target_state):
                    return False
                source_legal = source_system.grammar.legal_actions(source_grammar)
                target_legal = target_system.grammar.legal_actions(target_grammar)
                if not set(source_legal).issubset(target_legal):
                    return False
                for action in source_legal:
                    if relation_map.get(_successor_index(source_system, source_index, action)) != _successor_index(target_system, target_index, action):
                        return False
            if self.left_source_index == self.right_source_index:
                return False
            if self.left_source_index not in relation_map or self.right_source_index not in relation_map:
                return False
            if self.source.summary_labels[self.left_source_index] != self.source.summary_labels[self.right_source_index]:
                return False
            left_target = relation_map[self.left_source_index]
            right_target = relation_map[self.right_source_index]
            if labels[left_target] != labels[right_target]:
                return False
            _, left_source_grammar = _pair_at(source_system, self.left_source_index)
            _, right_source_grammar = _pair_at(source_system, self.right_source_index)
            try:
                source_system.grammar.normalize_legal_word(self.future_word, left_source_grammar)
                source_system.grammar.normalize_legal_word(self.future_word, right_source_grammar)
                return False
            except ValueError:
                pass
            _, left_target_grammar = _pair_at(target_system, left_target)
            _, right_target_grammar = _pair_at(target_system, right_target)
            target_system.grammar.normalize_legal_word(self.future_word, left_target_grammar)
            target_system.grammar.normalize_legal_word(self.future_word, right_target_grammar)
            if GrammarAwareDynamicInterfaceCertificate(target_system, labels).verify():
                return False
            return _trace(target_system, left_target, self.future_word) != _trace(target_system, right_target, self.future_word)
        except (AssertionError, TypeError, ValueError):
            return False


def non_nested_rewiring_obstruction() -> ReplacementFiberSplitObstructionCertificate:
    """Negative witness: a non-nested replacement makes ``reveal`` newly legal."""
    actions = ("stay", "reveal")
    source = StageMacroProjection(
        GrammarAwareControlledSystem(
            FiniteControlledOutputSystem(
                actions=actions,
                transition_table=((0, 0), (1, 1), (2, 2), (3, 3)),
                outputs=(0, 0, 0, 0),
            ),
            FinitePrefixGrammar(actions=actions, transition_table=((0, None),)),
        ),
        (0, 0, 0, 0),
    )
    target = GrammarAwareControlledSystem(
        FiniteControlledOutputSystem(
            actions=actions,
            transition_table=((0, 0), (1, 2), (2, 2)),
            outputs=(0, 0, 1),
        ),
        FinitePrefixGrammar(actions=actions, transition_table=((0, 0),)),
    )
    certificate = ReplacementFiberSplitObstructionCertificate(
        source=source,
        target_system=target,
        proposed_target_labels=(0, 0, 1),
        relation=((0, 0), (1, 1), (2, 0), (3, 1)),
        left_source_index=0,
        right_source_index=1,
        future_word=("reveal",),
    )
    if not certificate.verify():
        raise AssertionError("non-nested rewiring obstruction did not verify")
    return certificate


__all__ = [
    "Pair",
    "ReplacementTransport",
    "TransportedTargetProjectionCertificate",
    "certify_transported_target_projection",
    "TransportCoherentPortableMacroLawCertificate",
    "certify_transport_coherent_portable_macro_law",
    "non_nested_replacement_witness",
    "transported_target_projection_witness",
    "ReplacementFiberSplitObstructionCertificate",
    "non_nested_rewiring_obstruction",
]
