"""Coherent portable macro-laws over nested finite compositions.

A uniform bound on quotient size is weaker than one portable macro-law.  This
module requires a common finite macro dynamics and embeddings that preserve its
summary labels.  Under those premises every stage, and the direct union of the
nested stages, has the same exact macro transition system.

It also provides a concrete future-word obstruction: an old pair merged by a
proposed portable summary cannot remain merged if a newly legal word separates
their embedded images.
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
    grammar_count = system.grammar.state_count
    return index // grammar_count, index % grammar_count


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
                for target in row:
                    if target is not None and (not isinstance(target, int) or not 0 <= target < self.state_count):
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
            row: list[int | None] = []
            for action in actions:
                if action not in legal:
                    row.append(None)
                else:
                    row.append(self.summary_labels[_product_successor_index(self.constrained_system, representative, action)])
            transitions.append(tuple(row))
        macro = PortableMacroDynamics(actions, tuple(outputs), tuple(legal_rows), tuple(transitions))
        if not macro.verify():
            raise AssertionError("induced macro dynamics did not verify")
        return macro

    def verify(self) -> bool:
        try:
            labels = _canonical_labels(self.summary_labels, self.constrained_system.product_state_count)
            if labels != self.summary_labels or tuple(sorted(set(labels))) != tuple(range(self.summary_state_count)):
                return False
            return self.interface.verify() and self.induced_macro().verify()
        except (AssertionError, TypeError, ValueError):
            return False


@dataclass(frozen=True)
class StageEmbedding:
    """Injective embedding of old grammar-aware product states into the next stage."""

    source: StageMacroProjection
    target: StageMacroProjection
    target_indices: tuple[int, ...]

    def verify(self) -> bool:
        try:
            if not self.source.verify() or not self.target.verify():
                return False
            if self.source.constrained_system.system.actions != self.target.constrained_system.system.actions:
                return False
            if len(self.target_indices) != self.source.constrained_system.product_state_count:
                return False
            if len(set(self.target_indices)) != len(self.target_indices):
                return False
            if any(not isinstance(index, int) or not 0 <= index < self.target.constrained_system.product_state_count for index in self.target_indices):
                return False
            source_system = self.source.constrained_system
            target_system = self.target.constrained_system
            for source_index, target_index in enumerate(self.target_indices):
                source_state, source_grammar = _pair_at(source_system, source_index)
                target_state, target_grammar = _pair_at(target_system, target_index)
                if source_system.system.output(source_state) != target_system.system.output(target_state):
                    return False
                if source_system.grammar.legal_actions(source_grammar) != target_system.grammar.legal_actions(target_grammar):
                    return False
                for action in source_system.grammar.legal_actions(source_grammar):
                    if self.target_indices[_product_successor_index(source_system, source_index, action)] != _product_successor_index(target_system, target_index, action):
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
            if not self.macro.verify() or not self.stages:
                return False
            if len(self.embeddings) != len(self.stages) - 1:
                return False
            for stage in self.stages:
                if not stage.verify() or stage.induced_macro() != self.macro:
                    return False
            for index, embedding in enumerate(self.embeddings):
                if not embedding.verify() or embedding.source != self.stages[index] or embedding.target != self.stages[index + 1]:
                    return False
                for source_index, target_index in enumerate(embedding.target_indices):
                    if embedding.source.summary_labels[source_index] != embedding.target.summary_labels[target_index]:
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
    macro = PortableMacroDynamics(
        actions=actions,
        outputs=("inert-window",),
        legal_action_rows=(actions,),
        transition_rows=((0, 0),),
    )
    stages: list[StageMacroProjection] = []
    for module_count in range(1, max_module_count + 1):
        state_count = 2 ** module_count
        system = FiniteControlledOutputSystem(
            actions=actions,
            transition_table=tuple((state, state) for state in range(state_count)),
            outputs=("inert-window",) * state_count,
        )
        grammar = FinitePrefixGrammar(actions=actions, transition_table=((0, 0),))
        constrained = GrammarAwareControlledSystem(system, grammar)
        stages.append(StageMacroProjection(constrained, (0,) * constrained.product_state_count))
    embeddings = tuple(
        StageEmbedding(stages[index], stages[index + 1], tuple(range(stages[index].constrained_system.product_state_count)))
        for index in range(len(stages) - 1)
    )
    return certify_coherent_portable_macro_law(macro, tuple(stages), embeddings)


@dataclass(frozen=True)
class FutureWordObstructionCertificate:
    """A newly legal future word refutes one proposed coherent summary merge."""

    embedding: StageEmbedding
    left_source_index: int
    right_source_index: int
    future_word: tuple[str, ...]

    def verify(self) -> bool:
        try:
            if not self.embedding.verify():
                return False
            if self.left_source_index == self.right_source_index:
                return False
            source = self.embedding.source
            target = self.embedding.target
            if not 0 <= self.left_source_index < source.constrained_system.product_state_count:
                return False
            if not 0 <= self.right_source_index < source.constrained_system.product_state_count:
                return False
            if source.summary_labels[self.left_source_index] != source.summary_labels[self.right_source_index]:
                return False
            left_target = self.embedding.target_indices[self.left_source_index]
            right_target = self.embedding.target_indices[self.right_source_index]
            if target.summary_labels[left_target] != target.summary_labels[right_target]:
                return False
            target_system = target.constrained_system
            left_state, left_grammar = _pair_at(target_system, left_target)
            right_state, right_grammar = _pair_at(target_system, right_target)
            target_system.grammar.normalize_legal_word(self.future_word, left_grammar)
            target_system.grammar.normalize_legal_word(self.future_word, right_grammar)
            return _trace(target_system, left_target, self.future_word) != _trace(target_system, right_target, self.future_word)
        except (TypeError, ValueError):
            return False


def newly_legal_word_obstruction() -> FutureWordObstructionCertificate:
    """Two old states merge before a new legal action exposes their difference."""
    actions = ("stay", "reveal")
    old_system = FiniteControlledOutputSystem(
        actions=actions,
        transition_table=((0, 0), (1, 1)),
        outputs=(0, 0),
    )
    old_grammar = FinitePrefixGrammar(actions=actions, transition_table=((0, None),))
    old = StageMacroProjection(GrammarAwareControlledSystem(old_system, old_grammar), (0, 0))
    new_system = FiniteControlledOutputSystem(
        actions=actions,
        transition_table=((0, 0), (1, 2), (2, 2)),
        outputs=(0, 0, 1),
    )
    new_grammar = FinitePrefixGrammar(actions=actions, transition_table=((0, 0),))
    proposed = StageMacroProjection(GrammarAwareControlledSystem(new_system, new_grammar), (0, 0, 1))
    # The source's old legal behavior embeds exactly; the new action is newly legal.
    embedding = StageEmbedding(old, proposed, (0, 1))
    certificate = FutureWordObstructionCertificate(embedding, 0, 1, ("reveal",))
    if not certificate.verify():
        raise AssertionError("future-word obstruction certificate did not verify")
    return certificate
