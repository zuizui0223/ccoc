"""Conservative macro-schema transport across finite non-nested replacement.

``TransportedTargetProjectionCertificate`` requires equal legal-action rows at
source and target. This module treats the one controlled relaxation: a target may
make an action newly legal only when that action is uniform and macro-successor
deterministic on every target fiber derived from the source projection.

The certificate starts with an exact source projection and a declared finite
relation. It derives target labels, constructs one ``ConservativeMacroSchema``,
and verifies that the source and target are respectively a restriction and a full
realization of that schema. It is a sufficient finite-domain theorem, not a
classification of arbitrary rewiring or action growth.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .coherent_portable_macrolaw import StageMacroProjection
from .conservative_macro_schema import ConservativeMacroSchema, ConservativeStageProjection
from .dynamic_boundary_blankets import FiniteControlledOutputSystem
from .shared_grammar import FinitePrefixGrammar, GrammarAwareControlledSystem


Pair = tuple[int, int]


def _pair_at(system: GrammarAwareControlledSystem, index: int) -> tuple[int, int]:
    if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < system.product_state_count:
        raise ValueError("product index is outside the constrained system")
    return index // system.grammar.state_count, index % system.grammar.state_count


def _successor_index(system: GrammarAwareControlledSystem, index: int, action: str) -> int:
    state, grammar_state = _pair_at(system, index)
    return system.product_index((system.system.transition(state, action), system.grammar.transition(grammar_state, action)))


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
class ConservativeTransportedSchemaCertificate:
    """Transport one exact source projection into a conservative target schema.

    The relation must cover both finite product state spaces and be
    target-fiber-label-consistent, output-preserving, and successor-closed for all
    actions already legal at the source. The target may add actions. For each
    derived target label, however, every newly legal action must have the same
    availability and target macro successor at every target state in that label.

    The source realizes a restriction of the constructed schema; the target
    realizes the whole schema. No stage embedding is required, and the relation may
    be many-to-one or one-to-many.
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

    def _derive_labels_and_source_macro(self) -> tuple[tuple[int, ...], object, tuple[Pair, ...]]:
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
        source_macro = self.source.induced_macro()
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
            if not set(source_legal).issubset(target_legal):
                raise ValueError("target legal rows must preserve all source-legal actions")
            for action in source_legal:
                successor_pair = (
                    _successor_index(source_system, source_index, action),
                    _successor_index(target_system, target_index, action),
                )
                if successor_pair not in relation_set:
                    raise ValueError("transport relation is not successor-closed on a source-legal action")

        if any(label is None for label in target_labels):
            raise AssertionError("target coverage must assign one label to every target state")
        labels = _canonical_labels(
            tuple(int(label) for label in target_labels if label is not None),
            target_system.product_state_count,
        )
        return labels, source_macro, relation

    @property
    def target_labels(self) -> tuple[int, ...]:
        """Target labels derived only from source labels and the relation."""
        labels, _, _ = self._derive_labels_and_source_macro()
        return labels

    def _derive_schema(self) -> ConservativeMacroSchema:
        labels, source_macro, _ = self._derive_labels_and_source_macro()
        source_system = self.source.constrained_system
        target_system = self.target_system
        actions = source_system.system.actions

        novel_actions: list[tuple[str, ...] | None] = [None] * source_macro.state_count
        novel_successors: list[dict[str, int]] = [dict() for _ in range(source_macro.state_count)]
        for target_index, label in enumerate(labels):
            _, target_grammar = _pair_at(target_system, target_index)
            target_legal = target_system.grammar.legal_actions(target_grammar)
            source_legal = source_macro.legal_action_rows[label]
            if not set(source_legal).issubset(target_legal):
                raise AssertionError("relation validation must preserve source-legal actions")
            current_novel = tuple(action for action in target_legal if action not in source_legal)
            previous_novel = novel_actions[label]
            if previous_novel is None:
                novel_actions[label] = current_novel
            elif previous_novel != current_novel:
                raise ValueError("target-only action availability is not uniform on a target fiber")
            for action in current_novel:
                successor_label = labels[_successor_index(target_system, target_index, action)]
                prior_successor = novel_successors[label].get(action)
                if prior_successor is None:
                    novel_successors[label][action] = successor_label
                elif prior_successor != successor_label:
                    raise ValueError("target-only action is not label-deterministic on a target fiber")

        rows: list[tuple[int | None, ...]] = []
        for label in range(source_macro.state_count):
            if novel_actions[label] is None:
                raise AssertionError("source coverage must realize every macro label at target")
            row: list[int | None] = []
            for action_index, action in enumerate(actions):
                old_successor = source_macro.transition_rows[label][action_index]
                if old_successor is not None:
                    row.append(old_successor)
                elif action in novel_actions[label]:
                    row.append(novel_successors[label][action])
                else:
                    row.append(None)
            rows.append(tuple(row))
        schema = ConservativeMacroSchema(actions, source_macro.outputs, tuple(rows))
        if not schema.verify():
            raise AssertionError("derived conservative macro schema did not verify")
        return schema

    @property
    def schema(self) -> ConservativeMacroSchema:
        """One schema with old source actions and derived target-only actions."""
        return self._derive_schema()

    @property
    def source_stage(self) -> ConservativeStageProjection:
        stage = ConservativeStageProjection(self.source.constrained_system, self.source.summary_labels)
        if not stage.verify():
            raise AssertionError("exact source projection must realize a conservative stage")
        return stage

    @property
    def target_stage(self) -> ConservativeStageProjection:
        stage = ConservativeStageProjection(self.target_system, self.target_labels)
        if not stage.verify():
            raise AssertionError("derived target labels must be an exact conservative stage")
        return stage

    @property
    def target_projection(self) -> StageMacroProjection:
        projection = StageMacroProjection(self.target_system, self.target_labels)
        if not projection.verify():
            raise AssertionError("derived target labels failed exact-interface verification")
        return projection

    def verify(self) -> bool:
        try:
            schema = self.schema
            source_stage = self.source_stage
            target_stage = self.target_stage
            if not self.target_projection.verify():
                return False
            if source_stage.label_count != schema.state_count or target_stage.label_count != schema.state_count:
                return False
            source_rows = source_stage.stage_rows()
            target_rows = target_stage.stage_rows()
            if target_rows != schema.transition_rows:
                return False
            for source_row, schema_row in zip(source_rows, schema.transition_rows):
                for source_successor, schema_successor in zip(source_row, schema_row):
                    if source_successor is not None and source_successor != schema_successor:
                        return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_conservative_transported_schema(
    source: StageMacroProjection,
    target_system: GrammarAwareControlledSystem,
    relation: Iterable[Pair],
) -> ConservativeTransportedSchemaCertificate:
    """Certify one source-to-target conservative non-nested transport."""
    certificate = ConservativeTransportedSchemaCertificate(source, target_system, tuple(relation))
    if not certificate.verify():
        raise ValueError("source projection and transport do not construct a conservative target schema")
    return certificate


def conservative_non_nested_replacement_witness() -> ConservativeTransportedSchemaCertificate:
    """Many-to-one replacement where target-only ``reveal`` is macro-deterministic."""
    actions = ("flip", "reveal")
    source = StageMacroProjection(
        GrammarAwareControlledSystem(
            FiniteControlledOutputSystem(
                actions=actions,
                transition_table=((2, 0), (2, 1), (0, 2)),
                outputs=("low", "low", "high"),
            ),
            FinitePrefixGrammar(actions=actions, transition_table=((0, None),)),
        ),
        (0, 0, 1),
    )
    target = GrammarAwareControlledSystem(
        FiniteControlledOutputSystem(
            actions=actions,
            transition_table=((1, 1), (0, 1)),
            outputs=("low", "high"),
        ),
        FinitePrefixGrammar(actions=actions, transition_table=((0, 0),)),
    )
    certificate = certify_conservative_transported_schema(source, target, ((0, 0), (1, 0), (2, 1)))
    if (
        not certificate.verify()
        or certificate.target_labels != (0, 1)
        or certificate.schema.transition_rows != ((1, 1), (0, 1))
    ):
        raise AssertionError("conservative non-nested replacement witness did not verify")
    return certificate


__all__ = [
    "Pair",
    "ConservativeTransportedSchemaCertificate",
    "certify_conservative_transported_schema",
    "conservative_non_nested_replacement_witness",
]
