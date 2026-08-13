"""Exact abundance memory under a bounded future depletion grammar.

One guild has abundance n in {0,...,M} and threshold response min(L,n).
Colonization is always legal. Depletion is legal at most D times in the future;
the prefix grammar records how many depletion actions have already been used.
At grammar state u, with remaining budget d=D-u, the exact summary is

    (u, min(L+d, n)).

Thus the initial exact response interface has L+D+1 states when M>=L+D.
This interpolates between the monotone saturation blanket (D=0) and the full
abundance interface (D=M-L).
"""
from __future__ import annotations
from dataclasses import dataclass
from math import log2

from .dynamic_boundary_blankets import FiniteControlledOutputSystem
from .grammar_aware_blankets import (
    GrammarAwareDynamicInterfaceCertificate,
    certify_grammar_aware_canonical_interface,
)
from .shared_grammar import FinitePrefixGrammar, GrammarAwareControlledSystem


def budgeted_depletion_grammar(depletion_budget: int) -> FinitePrefixGrammar:
    if not isinstance(depletion_budget, int) or isinstance(depletion_budget, bool) or depletion_budget < 0:
        raise ValueError("depletion_budget must be a non-negative integer")
    rows = []
    for used in range(depletion_budget + 1):
        rows.append((used, used + 1 if used < depletion_budget else None))
    return FinitePrefixGrammar(
        actions=("colonize", "deplete"),
        transition_table=tuple(rows),
    )


@dataclass(frozen=True)
class BudgetedDepletionBlanketCertificate:
    capacity: int
    saturation_level: int
    depletion_budget: int

    @property
    def system(self) -> FiniteControlledOutputSystem:
        actions = ("colonize", "deplete")
        rows = tuple(
            (min(self.capacity, abundance + 1), max(0, abundance - 1))
            for abundance in range(self.capacity + 1)
        )
        outputs = tuple(
            min(self.saturation_level, abundance)
            for abundance in range(self.capacity + 1)
        )
        return FiniteControlledOutputSystem(actions, rows, outputs)

    @property
    def grammar(self) -> FinitePrefixGrammar:
        return budgeted_depletion_grammar(self.depletion_budget)

    @property
    def constrained_system(self) -> GrammarAwareControlledSystem:
        return GrammarAwareControlledSystem(self.system, self.grammar)

    @property
    def summary_labels(self) -> tuple[tuple[int, int], ...]:
        labels = []
        for abundance, used in self.constrained_system.product_states:
            remaining = self.depletion_budget - used
            labels.append(
                (used, min(self.saturation_level + remaining, abundance))
            )
        return tuple(labels)

    @property
    def interface(self) -> GrammarAwareDynamicInterfaceCertificate:
        return GrammarAwareDynamicInterfaceCertificate(
            self.constrained_system,
            self.summary_labels,
        )

    @property
    def initial_interface_state_count(self) -> int:
        return self.saturation_level + self.depletion_budget + 1

    @property
    def initial_interface_memory_bits(self) -> float:
        return log2(self.initial_interface_state_count)

    @property
    def monotone_baseline_state_count(self) -> int:
        return self.saturation_level + 1

    @property
    def disturbance_memory_inflation_bits(self) -> float:
        return log2(
            self.initial_interface_state_count / self.monotone_baseline_state_count
        )

    @property
    def expected_product_block_count(self) -> int:
        # Grammar state u has remaining budget D-u and therefore
        # L+(D-u)+1 possible exact abundance summaries.
        return sum(
            self.saturation_level + remaining + 1
            for remaining in range(self.depletion_budget + 1)
        )

    def verify(self) -> bool:
        try:
            if not isinstance(self.capacity, int) or isinstance(self.capacity, bool):
                return False
            if not isinstance(self.saturation_level, int) or isinstance(self.saturation_level, bool):
                return False
            if not isinstance(self.depletion_budget, int) or isinstance(self.depletion_budget, bool):
                return False
            if self.saturation_level < 1 or self.depletion_budget < 0:
                return False
            if self.capacity < self.saturation_level + self.depletion_budget:
                return False
            if not self.interface.verify():
                return False

            canonical = certify_grammar_aware_canonical_interface(self.constrained_system)
            if not canonical.verify():
                return False
            if canonical.initial_slice_block_count != self.initial_interface_state_count:
                return False
            if canonical.canonical_block_count != self.expected_product_block_count:
                return False

            # Direct local closure for both action types.
            labels = self.summary_labels
            for index, (abundance, used) in enumerate(self.constrained_system.product_states):
                label_used, capped = labels[index]
                if label_used != used:
                    return False
                colonize_index = self.constrained_system.product_index(
                    (min(self.capacity, abundance + 1), used)
                )
                colonize_expected = (
                    used,
                    min(
                        self.saturation_level + self.depletion_budget - used,
                        capped + 1,
                    ),
                )
                if labels[colonize_index] != colonize_expected:
                    return False
                if used < self.depletion_budget:
                    next_used = used + 1
                    deplete_index = self.constrained_system.product_index(
                        (max(0, abundance - 1), next_used)
                    )
                    next_cap = self.saturation_level + self.depletion_budget - next_used
                    deplete_expected = (next_used, min(next_cap, max(0, capped - 1)))
                    if labels[deplete_index] != deplete_expected:
                        return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_budgeted_depletion_blanket(
    capacity: int,
    saturation_level: int,
    depletion_budget: int,
) -> BudgetedDepletionBlanketCertificate:
    certificate = BudgetedDepletionBlanketCertificate(
        capacity=capacity,
        saturation_level=saturation_level,
        depletion_budget=depletion_budget,
    )
    if not certificate.verify():
        raise ValueError("budgeted depletion blanket did not verify")
    return certificate


__all__ = [
    "BudgetedDepletionBlanketCertificate",
    "budgeted_depletion_grammar",
    "certify_budgeted_depletion_blanket",
]
