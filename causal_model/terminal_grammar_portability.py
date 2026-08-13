"""Terminal-stage criterion for bounded exact portability across grammar chains.

Consider one fixed finite controlled plant and a finite chain of prefix grammars on
the same action alphabet and grammar-state set. Each step is a valid globally-new-
action-symbol expansion: every previously available action column is frozen, while
an action symbol illegal at every current grammar state may be introduced state-
dependently and is then frozen in all later stages.

Canonical exact response quotients therefore refine monotonically along the chain.
The canonical quotient of the terminal grammar is an exact interface for every
earlier stage. It is also the smallest possible single labeling that is exact for
all stages, because any shared exact interface must in particular be exact at the
terminal stage and hence refine its canonical quotient.

The same terminal labeling realizes one ConservativeMacroSchema across the chain.
Thus a uniform exact interface with at most B states exists iff the terminal
canonical quotient has at most B blocks.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .coherent_portable_macrolaw import TrajectoryEmbedding
from .conservative_macro_schema import (
    ConservativeMacroSchema,
    ConservativeSchemaChainCertificate,
    ConservativeStageProjection,
    certify_conservative_macro_schema,
)
from .dynamic_boundary_blankets import FiniteControlledOutputSystem
from .grammar_aware_blankets import (
    GrammarAwareDynamicInterfaceCertificate,
    certify_grammar_aware_canonical_interface,
)
from .grammar_expansion_closure import globally_new_action_symbols
from .shared_grammar import FinitePrefixGrammar, GrammarAwareControlledSystem


def _refines(fine: tuple[int, ...], coarse: tuple[int, ...]) -> bool:
    if len(fine) != len(coarse):
        return False
    return all(
        fine[i] != fine[j] or coarse[i] == coarse[j]
        for i in range(len(fine))
        for j in range(i + 1, len(fine))
    )


def _normalize_grammars(
    grammars: Iterable[FinitePrefixGrammar],
) -> tuple[FinitePrefixGrammar, ...]:
    try:
        normalized = tuple(grammars)
    except TypeError as error:
        raise ValueError("grammars must be iterable") from error
    if not normalized:
        raise ValueError("at least one grammar stage is required")
    if any(not isinstance(grammar, FinitePrefixGrammar) for grammar in normalized):
        raise ValueError("every stage must be a FinitePrefixGrammar")
    return normalized


@dataclass(frozen=True)
class TerminalGrammarPortabilityCertificate:
    """Exact terminal criterion and conservative shared schema for one chain."""

    plant: FiniteControlledOutputSystem
    grammars: tuple[FinitePrefixGrammar, ...]
    canonical_labels_by_stage: tuple[tuple[int, ...], ...]
    terminal_labels: tuple[int, ...]

    @property
    def stage_count(self) -> int:
        return len(self.grammars)

    @property
    def product_state_count(self) -> int:
        return self.plant.state_count * self.grammars[0].state_count

    @property
    def stage_block_counts(self) -> tuple[int, ...]:
        return tuple(len(set(labels)) for labels in self.canonical_labels_by_stage)

    @property
    def terminal_block_count(self) -> int:
        return len(set(self.terminal_labels))

    @property
    def minimal_uniform_interface_block_count(self) -> int:
        return self.terminal_block_count

    @property
    def introduced_symbols_by_step(self) -> tuple[tuple[str, ...], ...]:
        return tuple(
            globally_new_action_symbols(source, target)
            for source, target in zip(self.grammars, self.grammars[1:])
        )

    def uniform_interface_exists_with_at_most(self, block_bound: int) -> bool:
        if not isinstance(block_bound, int) or isinstance(block_bound, bool) or block_bound < 1:
            raise ValueError("block_bound must be a positive integer")
        return self.terminal_block_count <= block_bound

    @property
    def constrained_systems(self) -> tuple[GrammarAwareControlledSystem, ...]:
        return tuple(
            GrammarAwareControlledSystem(self.plant, grammar)
            for grammar in self.grammars
        )

    @property
    def conservative_schema_certificate(self) -> ConservativeSchemaChainCertificate:
        systems = self.constrained_systems
        stages = tuple(
            ConservativeStageProjection(system, self.terminal_labels)
            for system in systems
        )
        final_rows = stages[-1].stage_rows()

        outputs: list[object] = []
        for label in range(self.terminal_block_count):
            representative = self.terminal_labels.index(label)
            system_state, _ = systems[-1].product_states[representative]
            outputs.append(self.plant.output(system_state))

        schema = ConservativeMacroSchema(
            actions=self.plant.actions,
            outputs=tuple(outputs),
            transition_rows=final_rows,
        )
        identity = tuple(range(self.product_state_count))
        embeddings = tuple(
            TrajectoryEmbedding(source, target, identity)
            for source, target in zip(systems, systems[1:])
        )
        return certify_conservative_macro_schema(schema, stages, embeddings)

    def verify(self) -> bool:
        try:
            grammars = _normalize_grammars(self.grammars)
            if grammars != self.grammars:
                return False
            if grammars[0].actions != self.plant.actions:
                return False
            if any(grammar.actions != self.plant.actions for grammar in grammars):
                return False

            for source, target in zip(grammars, grammars[1:]):
                globally_new_action_symbols(source, target)

            systems = self.constrained_systems
            expected_labels = tuple(
                certify_grammar_aware_canonical_interface(system).canonical_labels
                for system in systems
            )
            if self.canonical_labels_by_stage != expected_labels:
                return False
            if self.terminal_labels != expected_labels[-1]:
                return False
            if tuple(sorted(set(self.terminal_labels))) != tuple(
                range(self.terminal_block_count)
            ):
                return False

            for earlier, later in zip(expected_labels, expected_labels[1:]):
                if not _refines(later, earlier):
                    return False
            if any(
                later < earlier
                for earlier, later in zip(
                    self.stage_block_counts, self.stage_block_counts[1:]
                )
            ):
                return False

            # Upper bound: terminal labels are exact at every earlier stage.
            for system in systems:
                if not GrammarAwareDynamicInterfaceCertificate(
                    system, self.terminal_labels
                ).verify():
                    return False

            # Constructive positive boundary: the same terminal labels realize one
            # conservative macro schema across the whole grammar chain.
            conservative = self.conservative_schema_certificate
            if not conservative.verify():
                return False
            if conservative.schema.state_count != self.terminal_block_count:
                return False
            if len(conservative.stages) != self.stage_count:
                return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_terminal_grammar_portability(
    plant: FiniteControlledOutputSystem,
    grammars: Iterable[FinitePrefixGrammar],
) -> TerminalGrammarPortabilityCertificate:
    """Certify terminal-stage minimality for a globally-new-symbol grammar chain."""
    normalized = _normalize_grammars(grammars)
    systems = tuple(
        GrammarAwareControlledSystem(plant, grammar) for grammar in normalized
    )
    labels = tuple(
        certify_grammar_aware_canonical_interface(system).canonical_labels
        for system in systems
    )
    certificate = TerminalGrammarPortabilityCertificate(
        plant=plant,
        grammars=normalized,
        canonical_labels_by_stage=labels,
        terminal_labels=labels[-1],
    )
    if not certificate.verify():
        raise ValueError(
            "grammar chain does not satisfy terminal exact-portability conditions"
        )
    return certificate


__all__ = [
    "TerminalGrammarPortabilityCertificate",
    "certify_terminal_grammar_portability",
]
