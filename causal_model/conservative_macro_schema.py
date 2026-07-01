"""Conservative portable macro-schemas under monotone grammar expansion.

PR #81 proves portability when old embedded states retain exactly the same legal
actions.  This module treats the missing case in which later stages make a
previously unavailable action legal.  A finite macro *schema* fixes output and
potential macro successor for every action; each stage realizes a restriction of
that schema.  Legal rows may expand, but old action meanings never change.

The theorem is conditional.  A newly legal action is portable only when it is
label-deterministic on the stage summary: every state in one macro fiber has the
same legal status and the same macro successor.  A concrete pair/action
certificate refutes a proposed merge when this fails.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable, Iterable

from .coherent_portable_macrolaw import TrajectoryEmbedding
from .delayed_addressability import FinitePrefixGrammar, GrammarAwareControlledSystem
from .dynamic_boundary_blankets import FiniteControlledOutputSystem
from .grammar_aware_blankets import GrammarAwareDynamicInterfaceCertificate


def _labels(labels: Iterable[int], count: int) -> tuple[int, ...]:
    try:
        values = tuple(labels)
    except TypeError as error:
        raise ValueError("labels must be iterable") from error
    if len(values) != count or not values:
        raise ValueError("labels must have one entry per product state")
    if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in values):
        raise ValueError("labels must be non-negative integers")
    return values


def _pair(system: GrammarAwareControlledSystem, index: int) -> tuple[int, int]:
    if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < system.product_state_count:
        raise ValueError("product index is outside system")
    return index // system.grammar.state_count, index % system.grammar.state_count


def _successor(system: GrammarAwareControlledSystem, index: int, action: str) -> int:
    state, grammar = _pair(system, index)
    return system.product_index((system.system.transition(state, action), system.grammar.transition(grammar, action)))


def _output_trace(system: GrammarAwareControlledSystem, index: int, word: tuple[str, ...]) -> tuple[Hashable, ...]:
    state, grammar = _pair(system, index)
    outputs: list[Hashable] = [system.system.output(state)]
    for action in word:
        state = system.system.transition(state, action)
        grammar = system.grammar.transition(grammar, action)
        outputs.append(system.system.output(state))
    return tuple(outputs)


@dataclass(frozen=True)
class ConservativeMacroSchema:
    """A finite macro state machine with optional action meanings.

    ``None`` means the schema does not promise a successor for that action.
    A stage may leave a schema-defined action unavailable; when it makes one
    available, it must realize exactly this successor.
    """

    actions: tuple[str, ...]
    outputs: tuple[Hashable, ...]
    transition_rows: tuple[tuple[int | None, ...], ...]

    @property
    def state_count(self) -> int:
        return len(self.outputs)

    def verify(self) -> bool:
        try:
            if not self.actions or len(set(self.actions)) != len(self.actions):
                return False
            if not self.outputs or len(self.transition_rows) != self.state_count:
                return False
            for output in self.outputs:
                hash(output)
            for row in self.transition_rows:
                if len(row) != len(self.actions):
                    return False
                for target in row:
                    if target is not None and (not isinstance(target, int) or isinstance(target, bool) or not 0 <= target < self.state_count):
                        return False
            return True
        except TypeError:
            return False

    def successor(self, label: int, action: str) -> int | None:
        if not self.verify() or not 0 <= label < self.state_count:
            raise ValueError("invalid macro state")
        try:
            return self.transition_rows[label][self.actions.index(action)]
        except ValueError as error:
            raise ValueError("unknown macro action") from error


@dataclass(frozen=True)
class ConservativeStageProjection:
    """An exact grammar-aware stage summary into a proposed schema state space."""

    constrained_system: GrammarAwareControlledSystem
    summary_labels: tuple[int, ...]

    @property
    def interface(self) -> GrammarAwareDynamicInterfaceCertificate:
        return GrammarAwareDynamicInterfaceCertificate(self.constrained_system, self.summary_labels)

    @property
    def label_count(self) -> int:
        return max(self.summary_labels) + 1

    def stage_rows(self) -> tuple[tuple[int | None, ...], ...]:
        if not self.interface.verify():
            raise ValueError("stage summary is not an exact grammar-aware interface")
        actions = self.constrained_system.system.actions
        rows: list[tuple[int | None, ...]] = []
        for label in range(self.label_count):
            members = [i for i, value in enumerate(self.summary_labels) if value == label]
            if not members:
                raise ValueError("labels must be contiguous")
            representative = members[0]
            _, grammar = _pair(self.constrained_system, representative)
            legal = self.constrained_system.grammar.legal_actions(grammar)
            rows.append(tuple(
                None if action not in legal else self.summary_labels[_successor(self.constrained_system, representative, action)]
                for action in actions
            ))
        return tuple(rows)

    def verify(self) -> bool:
        try:
            labels = _labels(self.summary_labels, self.constrained_system.product_state_count)
            return (
                labels == self.summary_labels
                and tuple(sorted(set(labels))) == tuple(range(self.label_count))
                and self.interface.verify()
            )
        except (TypeError, ValueError):
            return False


@dataclass(frozen=True)
class ConservativeSchemaChainCertificate:
    """A nested chain realizing one schema while legal action rows only expand."""

    schema: ConservativeMacroSchema
    stages: tuple[ConservativeStageProjection, ...]
    embeddings: tuple[TrajectoryEmbedding, ...]

    def verify(self) -> bool:
        try:
            if not self.schema.verify() or not self.stages:
                return False
            if len(self.embeddings) != len(self.stages) - 1:
                return False
            previous_rows: tuple[tuple[int | None, ...], ...] | None = None
            for stage in self.stages:
                if not stage.verify() or stage.label_count != self.schema.state_count:
                    return False
                system = stage.constrained_system
                if system.system.actions != self.schema.actions:
                    return False
                rows = stage.stage_rows()
                for label, row in enumerate(rows):
                    members = [i for i, value in enumerate(stage.summary_labels) if value == label]
                    state, _ = _pair(system, members[0])
                    if system.system.output(state) != self.schema.outputs[label]:
                        return False
                    for action_index, target in enumerate(row):
                        if target is not None and target != self.schema.transition_rows[label][action_index]:
                            return False
                        if target is not None and self.schema.transition_rows[label][action_index] is None:
                            return False
                if previous_rows is not None:
                    for earlier, later in zip(previous_rows, rows):
                        for old_target, new_target in zip(earlier, later):
                            if old_target is not None and old_target != new_target:
                                return False
                            if old_target is not None and new_target is None:
                                return False
                previous_rows = rows
            for index, embedding in enumerate(self.embeddings):
                source = self.stages[index]
                target = self.stages[index + 1]
                if embedding.source_system != source.constrained_system or embedding.target_system != target.constrained_system:
                    return False
                if not embedding.verify(equal_legal_actions=False):
                    return False
                for source_index, target_index in enumerate(embedding.target_indices):
                    if source.summary_labels[source_index] != target.summary_labels[target_index]:
                        return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_conservative_macro_schema(
    schema: ConservativeMacroSchema,
    stages: Iterable[ConservativeStageProjection],
    embeddings: Iterable[TrajectoryEmbedding],
) -> ConservativeSchemaChainCertificate:
    certificate = ConservativeSchemaChainCertificate(schema, tuple(stages), tuple(embeddings))
    if not certificate.verify():
        raise ValueError("stages do not realize a conservative portable macro-schema")
    return certificate


def conservative_reveal_chain() -> ConservativeSchemaChainCertificate:
    """Positive two-stage witness: reveal becomes legal without changing old law."""
    actions = ("stay", "reveal")
    schema = ConservativeMacroSchema(
        actions=actions,
        outputs=(0, 1),
        transition_rows=((0, 1), (1, 1)),
    )
    # Stage 0 contains both macro labels, but reveal is not yet legal for label 0.
    old_system = FiniteControlledOutputSystem(actions, ((0, 1), (1, 1)), (0, 1))
    old_grammar = FinitePrefixGrammar(actions, ((0, None),))
    old = ConservativeStageProjection(GrammarAwareControlledSystem(old_system, old_grammar), (0, 1))
    # Stage 1 preserves old trajectories and activates reveal at label 0.
    new_system = FiniteControlledOutputSystem(actions, ((0, 1), (1, 1), (2, 2)), (0, 1, 1))
    new_grammar = FinitePrefixGrammar(actions, ((0, 0),))
    new = ConservativeStageProjection(GrammarAwareControlledSystem(new_system, new_grammar), (0, 1, 1))
    embedding = TrajectoryEmbedding(old.constrained_system, new.constrained_system, (0, 1))
    return certify_conservative_macro_schema(schema, (old, new), (embedding,))


@dataclass(frozen=True)
class NewActionMergeObstructionCertificate:
    """A new legal action distinguishes two states in one proposed summary fiber."""

    target_system: GrammarAwareControlledSystem
    proposed_labels: tuple[int, ...]
    left_index: int
    right_index: int
    newly_legal_action: str

    def verify(self) -> bool:
        try:
            labels = _labels(self.proposed_labels, self.target_system.product_state_count)
            if labels != self.proposed_labels or self.left_index == self.right_index:
                return False
            if not 0 <= self.left_index < self.target_system.product_state_count or not 0 <= self.right_index < self.target_system.product_state_count:
                return False
            if labels[self.left_index] != labels[self.right_index]:
                return False
            _, left_grammar = _pair(self.target_system, self.left_index)
            _, right_grammar = _pair(self.target_system, self.right_index)
            if self.newly_legal_action not in self.target_system.grammar.legal_actions(left_grammar):
                return False
            if self.newly_legal_action not in self.target_system.grammar.legal_actions(right_grammar):
                return False
            left_trace = _output_trace(self.target_system, self.left_index, (self.newly_legal_action,))
            right_trace = _output_trace(self.target_system, self.right_index, (self.newly_legal_action,))
            left_successor = labels[_successor(self.target_system, self.left_index, self.newly_legal_action)]
            right_successor = labels[_successor(self.target_system, self.right_index, self.newly_legal_action)]
            return left_trace != right_trace or left_successor != right_successor
        except (TypeError, ValueError):
            return False


def newly_legal_action_merge_obstruction() -> NewActionMergeObstructionCertificate:
    """A proposed old merge fails exactly when reveal is admitted."""
    actions = ("stay", "reveal")
    system = FiniteControlledOutputSystem(
        actions,
        ((0, 2), (1, 1), (2, 2)),
        (0, 0, 1),
    )
    grammar = FinitePrefixGrammar(actions, ((0, 0),))
    certificate = NewActionMergeObstructionCertificate(
        target_system=GrammarAwareControlledSystem(system, grammar),
        proposed_labels=(0, 0, 1),
        left_index=0,
        right_index=1,
        newly_legal_action="reveal",
    )
    if not certificate.verify():
        raise AssertionError("newly legal action obstruction did not verify")
    return certificate
