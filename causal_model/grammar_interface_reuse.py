"""Exact reuse criterion for a canonical closed interface under grammar change.

The controlled plant is fixed and the closed/open prefix grammars share the same
action alphabet, grammar-state set, and initial grammar state, but their transition
tables may differ arbitrarily. The canonical closed quotient can be reused
unchanged as an exact open interface iff its fibers have uniform open enabled
rows and label-deterministic open successors. Canonical minimal quotients may be
equal, open-finer, open-coarser, or incomparable.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
from .dynamic_boundary_blankets import FiniteControlledOutputSystem
from .grammar_aware_blankets import GrammarAwareDynamicInterfaceCertificate, certify_grammar_aware_canonical_interface
from .shared_grammar import FinitePrefixGrammar, GrammarAwareControlledSystem

PartitionRelation = Literal["equal", "closed_refines_open", "open_refines_closed", "incomparable"]
ObstructionKind = Literal["legality", "successor"]


def _validate_same_domain(closed_grammar, open_grammar):
    if closed_grammar.actions != open_grammar.actions:
        raise ValueError("closed and open grammars must use the same ordered action alphabet")
    if closed_grammar.state_count != open_grammar.state_count:
        raise ValueError("closed and open grammars must use the same grammar-state set")
    if closed_grammar.initial_state != open_grammar.initial_state:
        raise ValueError("closed and open grammars must use the same initial grammar state")


def _refines(left, right):
    if len(left) != len(right):
        raise ValueError("partition label tuples must have the same length")
    return all(left[i] != left[j] or right[i] == right[j] for i in range(len(left)) for j in range(i + 1, len(left)))


def canonical_partition_relation(closed_labels, open_labels):
    c = _refines(closed_labels, open_labels)
    o = _refines(open_labels, closed_labels)
    if c and o: return "equal"
    if c: return "closed_refines_open"
    if o: return "open_refines_closed"
    return "incomparable"


def _successor_index(system, index, action):
    x, q = system.product_states[index]
    return system.product_index((system.system.transition(x, action), system.grammar.transition(q, action)))


@dataclass(frozen=True)
class ClosedInterfaceReuseObstructionCertificate:
    plant: FiniteControlledOutputSystem
    closed_grammar: FinitePrefixGrammar
    open_grammar: FinitePrefixGrammar
    closed_labels: tuple[int, ...]
    left_index: int
    right_index: int
    kind: ObstructionKind
    action: str
    def verify(self):
        try:
            _validate_same_domain(self.closed_grammar, self.open_grammar)
            cs = GrammarAwareControlledSystem(self.plant, self.closed_grammar)
            os = GrammarAwareControlledSystem(self.plant, self.open_grammar)
            if self.closed_labels != certify_grammar_aware_canonical_interface(cs).canonical_labels:
                return False
            if self.left_index == self.right_index or self.closed_labels[self.left_index] != self.closed_labels[self.right_index]:
                return False
            _, lq = os.product_states[self.left_index]; _, rq = os.product_states[self.right_index]
            ll = os.grammar.legal_actions(lq); rl = os.grammar.legal_actions(rq)
            if self.kind == "legality":
                return (self.action in ll) != (self.action in rl)
            if self.kind != "successor" or self.action not in ll or self.action not in rl:
                return False
            return self.closed_labels[_successor_index(os, self.left_index, self.action)] != self.closed_labels[_successor_index(os, self.right_index, self.action)]
        except (AssertionError, IndexError, TypeError, ValueError):
            return False


def find_closed_interface_reuse_obstruction(plant, closed_grammar, open_grammar):
    _validate_same_domain(closed_grammar, open_grammar)
    cs = GrammarAwareControlledSystem(plant, closed_grammar)
    os = GrammarAwareControlledSystem(plant, open_grammar)
    labels = certify_grammar_aware_canonical_interface(cs).canonical_labels
    for i in range(os.product_state_count):
        for j in range(i + 1, os.product_state_count):
            if labels[i] != labels[j]: continue
            _, qi = os.product_states[i]; _, qj = os.product_states[j]
            li = os.grammar.legal_actions(qi); lj = os.grammar.legal_actions(qj)
            if li != lj:
                for action in os.system.actions:
                    if (action in li) != (action in lj):
                        cert = ClosedInterfaceReuseObstructionCertificate(plant, closed_grammar, open_grammar, labels, i, j, "legality", action)
                        if not cert.verify(): raise AssertionError("reuse legality obstruction failed")
                        return cert
            for action in li:
                if labels[_successor_index(os, i, action)] != labels[_successor_index(os, j, action)]:
                    cert = ClosedInterfaceReuseObstructionCertificate(plant, closed_grammar, open_grammar, labels, i, j, "successor", action)
                    if not cert.verify(): raise AssertionError("reuse successor obstruction failed")
                    return cert
    return None


@dataclass(frozen=True)
class ClosedInterfaceReuseCertificate:
    plant: FiniteControlledOutputSystem
    closed_grammar: FinitePrefixGrammar
    open_grammar: FinitePrefixGrammar
    closed_labels: tuple[int, ...]
    open_labels: tuple[int, ...]
    @property
    def relation(self): return canonical_partition_relation(self.closed_labels, self.open_labels)
    @property
    def closed_block_count(self): return len(set(self.closed_labels))
    @property
    def open_block_count(self): return len(set(self.open_labels))
    @property
    def minimal_block_delta(self): return self.open_block_count - self.closed_block_count
    @property
    def reusable(self):
        os = GrammarAwareControlledSystem(self.plant, self.open_grammar)
        return GrammarAwareDynamicInterfaceCertificate(os, self.closed_labels).verify()
    def verify(self):
        try:
            _validate_same_domain(self.closed_grammar, self.open_grammar)
            cs = GrammarAwareControlledSystem(self.plant, self.closed_grammar)
            os = GrammarAwareControlledSystem(self.plant, self.open_grammar)
            if self.closed_labels != certify_grammar_aware_canonical_interface(cs).canonical_labels: return False
            if self.open_labels != certify_grammar_aware_canonical_interface(os).canonical_labels: return False
            obstruction = find_closed_interface_reuse_obstruction(self.plant, self.closed_grammar, self.open_grammar)
            if self.reusable != (obstruction is None): return False
            if self.reusable and self.relation not in ("equal", "closed_refines_open"): return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_closed_interface_reuse(plant, closed_grammar, open_grammar):
    _validate_same_domain(closed_grammar, open_grammar)
    cs = GrammarAwareControlledSystem(plant, closed_grammar)
    os = GrammarAwareControlledSystem(plant, open_grammar)
    cert = ClosedInterfaceReuseCertificate(plant, closed_grammar, open_grammar, certify_grammar_aware_canonical_interface(cs).canonical_labels, certify_grammar_aware_canonical_interface(os).canonical_labels)
    if not cert.verify(): raise AssertionError("closed-interface reuse certificate did not verify")
    return cert

__all__ = ["PartitionRelation", "ClosedInterfaceReuseObstructionCertificate", "ClosedInterfaceReuseCertificate", "canonical_partition_relation", "find_closed_interface_reuse_obstruction", "certify_closed_interface_reuse"]
