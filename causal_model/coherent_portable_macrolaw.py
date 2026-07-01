"""Coherent portable macro-laws over nested finite compositions.

A uniform bound on quotient size is weaker than one portable macro-law. This
module requires common finite macro dynamics and embeddings that preserve summary
labels. Under those premises every stage has the same exact macro system.

A separate trajectory embedding handles the negative case: a newly legal word
can refute a proposed merge before that proposed target summary is itself exact.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable, Iterable

from .delayed_addressability import FinitePrefixGrammar, GrammarAwareControlledSystem
from .dynamic_boundary_blankets import FiniteControlledOutputSystem
from .grammar_aware_blankets import GrammarAwareDynamicInterfaceCertificate


def _canonical_labels(labels: Iterable[int], count: int) -> tuple[int, ...]:
    try:
        values = tuple(labels)
    except TypeError as error:
        raise ValueError("summary labels must be iterable") from error
    if len(values) != count or not values:
        raise ValueError("summary labels must provide one nonempty entry per product state")
    if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in values):
        raise ValueError("summary labels must be non-negative integers")
    return values


def _pair_at(system: GrammarAwareControlledSystem, index: int) -> tuple[int, int]:
    if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < system.product_state_count:
        raise ValueError("product index is outside the constrained system")
    return index // system.grammar.state_count, index % system.grammar.state_count


def _product_successor_index(system: GrammarAwareControlledSystem, index: int, action: str) -> int:
    state, grammar_state = _pair_at(system, index)
    return system.product_index((system.system.transition(state, action), system.grammar.transition(grammar_state, action)))


def _trace(system: GrammarAwareControlledSystem, index: int, word: tuple[str, ...]) -> tuple[Hashable, ...]:
    state, grammar_state = _pair_at(system, index)
    outputs: list[Hashable] = [system.system.output(state)]
    for action in word:
        state = system.system.transition(state, action)
        grammar_state = system.grammar.transition(grammar_state, action)
        outputs.append(system.system.output(state))
    return tuple(outputs)


@dataclass(frozen=True)
class PortableMacroDynamics:
    """One finite macro output / legality / transition system."""

    actions: tuple[str, ...]
    outputs: tuple[Hashable, ...]
    legal_action_rows: tuple[tuple[str, ...], ...]
    transition_rows: tuple[tuple[int | None, ...], ...]

    @property
    def state_count(self) -> int:
        return len(self.outputs)

    def verify(self) -> bool:
        try:
            if not self.actions or len(set(self.actions)) != len(self.actions):
                return False
            if not self.outputs or len(self.legal_action_rows) != self.state_count or len(self.transition_rows) != self.state_count:
                return False
            for output in self.outputs:
                hash(output)
            for legal, row in zip(self.legal_action_rows, self.transition_rows):
                if tuple(action for action, target in zip(self.actions, row) if target is not None) != legal:
                    return False
                if any(action not in self.actions for action in legal):
                    return False
                if any(target is not None and (not isinstance(target, int) or not 0 <= target < self.state_count) for target in row):
                    return False
            return True
        except (TypeError, ValueError):
            return False


@dataclass(frozen=True)
class StageMacroProjection:
    """One exact stage projection into a candidate common macro system."""

    constrained_system: GrammarAwareControlledSystem
    summary_labels: tuple[int, ...]

    @property
    def interface(self) -> GrammarAwareDynamicInterfaceCertificate:
        return GrammarAwareDynamicInterfaceCertificate(self.constrained_system, self.summary_labels)

    @property
    def summary_state_count(self) -> int:
        return max(self.summary_labels) + 1

    def induced_macro(self) -> PortableMacroDynamics:
        if not self.interface.verify():
            raise ValueError("stage summary must be a grammar-aware dynamic interface")
        actions = self.constrained_system.system.actions
        outputs: list[Hashable] = []
        legal_rows: list[tuple[str, ...]] = []
        transitions: list[tuple[int | None, ...]] = []
        for label in range(self.summary_state_count):
            members = [index for index, value in enumerate(self.summary_labels) if value == label]
            if not members:
                raise ValueError("summary labels must be canonical and contiguous")
            representative = members[0]
            state, grammar_state = _pair_at(self.constrained_system, representative)
            outputs.append(self.constrained_system.system.output(state))
            legal = self.constrained_system.grammar.legal_actions(grammar_state)
            legal_rows.append(legal)
            transitions.append(tuple(
                None if action not in legal else self.summary_labels[_product_successor_index(self.constrained_system, representative, action)]
                for action in actions
            ))
        macro = PortableMacroDynamics(actions, tuple(outputs), tuple(legal_rows), tuple(transitions))
        if not macro.verify():
            raise AssertionError("induced macro dynamics did not verify")
        return macro

    def verify(self) -> bool:
        try:
            labels = _canonical_labels(self.summary_labels, self.constrained_system.product_state_count)
            return (
                labels == self.summary_labels
                and tuple(sorted(set(labels))) == tuple(range(self.summary_state_count))
                and self.interface.verify()
                and self.induced_macro().verify()
            )
        except (AssertionError, TypeError, ValueError):
            return False


@dataclass(frozen=True)
class StageEmbedding:
    """Exact embedding of one projected stage into the next projected stage."""

    source: StageMacroProjection
    target: StageMacroProjection
    target_indices: tuple[int, ...]

    def verify(self) -> bool:
        try:
            if not self.source.verify() or not self.target.verify():
                return False
            trajectory = TrajectoryEmbedding(self.source.constrained_system, self.target.constrained_system, self.target_indices)
            if not trajectory.verify(equal_legal_actions=True):
                return False
            return True
        except (TypeError, ValueError):
            return False


@dataclass(frozen=True)
class TrajectoryEmbedding:
    """Embedding preserving old outputs and all trajectories legal at the old stage."""

    source_system: GrammarAwareControlledSystem
    target_system: GrammarAwareControlledSystem
    target_indices: tuple[int, ...]

    def verify(self, equal_legal_actions: bool = False) -> bool:
        try:
            if self.source_system.system.actions != self.target_system.system.actions:
                return False
            if len(self.target_indices) != self.source_system.product_state_count:
                return False
            if len(set(self.target_indices)) != len(self.target_indices):
                return False
            if any(not isinstance(index, int) or not 0 <= index < self.target_system.product_state_count for index in self.target_indices):
                return False
            for source_index, target_index in enumerate(self.target_indices):
                source_state, source_grammar = _pair_at(self.source_system, source_index)
                target_state, target_grammar = _pair_at(self.target_system, target_index)
                if self.source_system.system.output(source_state) != self.target_system.system.output(target_state):
                    return False
                source_legal = self.source_system.grammar.legal_actions(source_grammar)
                target_legal = self.target_system.grammar.legal_actions(target_grammar)
                if not set(source_legal).issubset(target_legal):
                    return False
                if equal_legal_actions and source_legal != target_legal:
                    return False
                for action in source_legal:
                    if self.target_indices[_product_successor_index(self.source_system, source_index, action)] != _product_successor_index(self.target_system, target_index, action):
                        return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


@dataclass(frozen=True)
class CoherentPortableMacroLawCertificate:
    """Common macro dynamics and coherent embeddings prove one portable law."""

    macro: PortableMacroDynamics
    stages: tuple[StageMacroProjection, ...]
    embeddings: tuple[StageEmbedding, ...]

    def verify(self) -> bool:
        try:
            if not self.macro.verify() or not self.stages or len(self.embeddings) != len(self.stages) - 1:
                return False
            if any(not stage.verify() or stage.induced_macro() != self.macro for stage in self.stages):
                return False
            for index, embedding in enumerate(self.embeddings):
                if not embedding.verify() or embedding.source != self.stages[index] or embedding.target != self.stages[index + 1]:
                    return False
                if any(embedding.source.summary_labels[source_index] != embedding.target.summary_labels[target_index] for source_index, target_index in enumerate(embedding.target_indices)):
                    return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_coherent_portable_macro_law(
    macro: PortableMacroDynamics,
    stages: Iterable[StageMacroProjection],
    embeddings: Iterable[StageEmbedding],
) -> CoherentPortableMacroLawCertificate:
    certificate = CoherentPortableMacroLawCertificate(macro, tuple(stages), tuple(embeddings))
    if not certificate.verify():
        raise ValueError("stages and embeddings do not realize one coherent portable macro-law")
    return certificate


def inert_portable_chain(max_module_count: int) -> CoherentPortableMacroLawCertificate:
    """Positive witness: growing inert configurations with one unchanged macro-law."""
    if not isinstance(max_module_count, int) or isinstance(max_module_count, bool) or max_module_count < 1:
        raise ValueError("max_module_count must be positive")
    actions = ("observe", "connect")
    macro = PortableMacroDynamics(actions, ("inert-window",), (actions,), ((0, 0),))
    stages: list[StageMacroProjection] = []
    for module_count in range(1, max_module_count + 1):
        state_count = 2 ** module_count
        system = FiniteControlledOutputSystem(actions, tuple((state, state) for state in range(state_count)), ("inert-window",) * state_count)
        grammar = FinitePrefixGrammar(actions, ((0, 0),))
        constrained = GrammarAwareControlledSystem(system, grammar)
        stages.append(StageMacroProjection(constrained, (0,) * constrained.product_state_count))
    embeddings = tuple(StageEmbedding(stages[index], stages[index + 1], tuple(range(stages[index].constrained_system.product_state_count))) for index in range(len(stages) - 1))
    return certify_coherent_portable_macro_law(macro, tuple(stages), embeddings)


@dataclass(frozen=True)
class FutureWordObstructionCertificate:
    """A newly legal future word refutes one proposed coherent summary merge."""

    trajectory_embedding: TrajectoryEmbedding
    source_labels: tuple[int, ...]
    target_labels: tuple[int, ...]
    left_source_index: int
    right_source_index: int
    future_word: tuple[str, ...]

    def verify(self) -> bool:
        try:
            if not self.trajectory_embedding.verify(equal_legal_actions=False):
                return False
            source = self.trajectory_embedding.source_system
            target = self.trajectory_embedding.target_system
            source_labels = _canonical_labels(self.source_labels, source.product_state_count)
            target_labels = _canonical_labels(self.target_labels, target.product_state_count)
            if source_labels != self.source_labels or target_labels != self.target_labels:
                return False
            if self.left_source_index == self.right_source_index:
                return False
            if not 0 <= self.left_source_index < source.product_state_count or not 0 <= self.right_source_index < source.product_state_count:
                return False
            if source_labels[self.left_source_index] != source_labels[self.right_source_index]:
                return False
            left_target = self.trajectory_embedding.target_indices[self.left_source_index]
            right_target = self.trajectory_embedding.target_indices[self.right_source_index]
            if target_labels[left_target] != target_labels[right_target]:
                return False
            _, left_grammar = _pair_at(target, left_target)
            _, right_grammar = _pair_at(target, right_target)
            target.grammar.normalize_legal_word(self.future_word, left_grammar)
            target.grammar.normalize_legal_word(self.future_word, right_grammar)
            return _trace(target, left_target, self.future_word) != _trace(target, right_target, self.future_word)
        except (TypeError, ValueError):
            return False


def newly_legal_word_obstruction() -> FutureWordObstructionCertificate:
    """Two old states merge before a new legal action exposes their difference."""
    actions = ("stay", "reveal")
    old_system = FiniteControlledOutputSystem(actions, ((0, 0), (1, 1)), (0, 0))
    old_grammar = FinitePrefixGrammar(actions, ((0, None),))
    new_system = FiniteControlledOutputSystem(actions, ((0, 0), (1, 2), (2, 2)), (0, 0, 1))
    new_grammar = FinitePrefixGrammar(actions, ((0, 0),))
    trajectory = TrajectoryEmbedding(
        GrammarAwareControlledSystem(old_system, old_grammar),
        GrammarAwareControlledSystem(new_system, new_grammar),
        (0, 1),
    )
    certificate = FutureWordObstructionCertificate(
        trajectory_embedding=trajectory,
        source_labels=(0, 0),
        target_labels=(0, 0, 1),
        left_source_index=0,
        right_source_index=1,
        future_word=("reveal",),
    )
    if not certificate.verify():
        raise AssertionError("future-word obstruction certificate did not verify")
    return certificate
