"""Aggregate certificate for the strongest fixed-grammar CCOC relay theorem.

This module does not introduce a new witness family.  It composes the already
verified fixed-regular-grammar relay facts into one certificate matching the
analytic theorem statement used for manuscript transfer:

* one constant four-symbol action alphabet;
* one-state closed/open grammar schemas differing by one ``fire`` transition;
* two closed response classes versus ``2**(m+1)`` open response classes;
* absolute-maximal ``m``-bit open-only innovation on ``D_m``;
* bounded local state, degree at most three, tree topology, and focal/exterior
  cut width one; and
* worst canonical access ``2*ceil(log2(m))+2`` for every positive ``m``.

The finite certificate is a replay/consistency object.  The all-``m`` theorem is
proved analytically in ``docs/fixed_regular_extremal_theorem_2026-08-13.md``.
"""

from __future__ import annotations

from dataclasses import dataclass

from .constant_alphabet_relay import FIRE, GLOBAL_ACTION_ALPHABET
from .fixed_regular_grammar_relay import (
    FixedRegularGrammarRelayCertificate,
    balanced_tree_max_selector_depth,
    certify_fixed_regular_grammar_relay,
)
from .relay_tree_compilation import ROOT


@dataclass(frozen=True)
class FixedRegularExtremalTheoremCertificate:
    """One finite-``m`` certificate for the simultaneous extremal package."""

    relay: FixedRegularGrammarRelayCertificate

    @property
    def module_count(self) -> int:
        return self.relay.module_count

    @property
    def comparison_domain_state_count(self) -> int:
        return 2 ** (self.module_count + 1)

    @property
    def action_alphabet_size(self) -> int:
        return len(GLOBAL_ACTION_ALPHABET)

    @property
    def closed_grammar_state_count(self) -> int:
        return self.relay.closed_grammar.state_count

    @property
    def open_grammar_state_count(self) -> int:
        return self.relay.open_grammar.state_count

    @property
    def newly_legal_action_count(self) -> int:
        return len(
            set(self.relay.open_grammar.legal_actions(0))
            - set(self.relay.closed_grammar.legal_actions(0))
        )

    @property
    def grammar_transition_difference_count(self) -> int:
        closed = self.relay.closed_grammar.transition_table
        opened = self.relay.open_grammar.transition_table
        return sum(
            closed_state != open_state
            for closed_row, open_row in zip(closed, opened, strict=True)
            for closed_state, open_state in zip(closed_row, open_row, strict=True)
        )

    @property
    def closed_interface_state_count(self) -> int:
        return self.relay.closed_interface_state_count

    @property
    def open_interface_state_count(self) -> int:
        return self.relay.open_interface_state_count

    @property
    def open_only_innovation_bits(self) -> int:
        return self.relay.open_only_innovation_bits

    @property
    def finite_domain_maximum_innovation_bits(self) -> int:
        # log2 |D_m| - log2 |P_C| = (m+1) - 1.
        return self.module_count

    @property
    def innovation_slack_bits(self) -> int:
        return self.finite_domain_maximum_innovation_bits - self.open_only_innovation_bits

    @property
    def exterior_response_lower_bound_bits(self) -> int:
        """Bits forced for exterior response labels when the focal bit is separate."""
        return self.module_count

    @property
    def exterior_response_lower_bound_state_count(self) -> int:
        return 2 ** self.exterior_response_lower_bound_bits

    @property
    def maximum_degree(self) -> int:
        return self.relay.maximum_degree

    @property
    def focal_exterior_cut_width(self) -> int:
        return len(self.relay.topology.children_by_node[ROOT])

    @property
    def is_tree_topology(self) -> bool:
        topology = self.relay.topology
        return topology.verify() and len(topology.message_edges) == len(topology.nodes) - 1

    @property
    def selector_augmented_relay_state_count(self) -> int:
        return self.relay.selector_augmented_relay_state_count

    @property
    def selector_augmented_leaf_state_count(self) -> int:
        return self.relay.selector_augmented_leaf_state_count

    @property
    def worst_canonical_query_length(self) -> int:
        return self.relay.worst_canonical_query_length

    @property
    def exact_worst_query_formula(self) -> int:
        return 2 * balanced_tree_max_selector_depth(self.module_count) + 2

    def verify(self) -> bool:
        """Verify that one finite witness satisfies every simultaneous clause."""
        try:
            if not self.relay.verify():
                return False
            if self.action_alphabet_size != 4:
                return False
            if self.closed_grammar_state_count != 1 or self.open_grammar_state_count != 1:
                return False
            if self.newly_legal_action_count != 1:
                return False
            if self.grammar_transition_difference_count != 1:
                return False
            if FIRE not in self.relay.open_grammar.legal_actions(0):
                return False
            if FIRE in self.relay.closed_grammar.legal_actions(0):
                return False
            if self.closed_interface_state_count != 2:
                return False
            if self.open_interface_state_count != self.comparison_domain_state_count:
                return False
            if self.open_only_innovation_bits != self.module_count:
                return False
            if self.innovation_slack_bits != 0:
                return False
            if self.exterior_response_lower_bound_state_count != 2 ** self.module_count:
                return False
            if self.maximum_degree > 3:
                return False
            if self.focal_exterior_cut_width != 1:
                return False
            if not self.is_tree_topology:
                return False
            if self.selector_augmented_relay_state_count > 6:
                return False
            if self.selector_augmented_leaf_state_count > 12:
                return False
            if self.worst_canonical_query_length != self.exact_worst_query_formula:
                return False
            return True
        except (AssertionError, KeyError, TypeError, ValueError):
            return False


def certify_fixed_regular_extremal_theorem(
    module_count: int,
) -> FixedRegularExtremalTheoremCertificate:
    """Certify the simultaneous fixed-grammar theorem package at one finite ``m``."""
    certificate = FixedRegularExtremalTheoremCertificate(
        relay=certify_fixed_regular_grammar_relay(module_count)
    )
    if not certificate.verify():
        raise AssertionError("fixed-regular extremal theorem certificate did not verify")
    return certificate


__all__ = [
    "FixedRegularExtremalTheoremCertificate",
    "certify_fixed_regular_extremal_theorem",
]
