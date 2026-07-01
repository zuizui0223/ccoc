"""Budgeted exact quotients for delayed joint reset panels.

The full reset-panel theorem gives the resources required to recover every
coordinate of a fixed delayed binary joint state.  This module gives the exact
middle layer: a limited fresh-copy panel identifies a specific partial quotient.

The observation contract includes one zero-action baseline read of the focal bit
``y`` before allocating reset trials.  A panel record is therefore

    (baseline y, ordered trial traces).

This makes the N=0 case explicit: without a terminal trial, the focal baseline
is still known but every exterior/response coordinate remains unresolved.

For a panel ``P`` covering read ports ``R(P)`` and the intervention indicator
``J(P)``, the exact quotient is equality of

    y, (b_i for i in R(P)), and r when J(P)=1.

Thus

    |X / ~_P| = 2^(1 + |R(P)| + J(P)),
    |[x]_P|  = 2^(m + 1 - |R(P)| - J(P)).

Each newly covered terminal probe contributes one exact bit and halves residual
ambiguity.  Wait-only and duplicate probes contribute zero.  All statements are
finite deterministic results under explicit fresh-reset semantics; they are not
claims about probabilistic information or non-resettable ecosystems.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import log2
from typing import Iterable, Literal

from .delayed_joint_nonidentifiability import DelayedJointAction, DelayedJointFamily, DelayedJointState
from .delayed_joint_reset_panels import ResettableTrialPanel, TrialWord, required_terminal_words

CoverageKind = Literal["read", "intervene", "wait_or_duplicate"]
BaselinePanelSignature = tuple[int, tuple[tuple[int, ...], ...]]


def _nonnegative(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")


def _labels(values: Iterable[object]) -> tuple[int, ...]:
    table: dict[object, int] = {}
    result: list[int] = []
    for value in values:
        if value not in table:
            table[value] = len(table)
        result.append(table[value])
    return tuple(result)


def _same_partition(left: tuple[int, ...], right: tuple[int, ...]) -> bool:
    return len(left) == len(right) and all(
        (left[i] == left[j]) == (right[i] == right[j])
        for i in range(len(left))
        for j in range(len(left))
    )


def _words(family: DelayedJointFamily, trial_words: Iterable[Iterable[DelayedJointAction]]) -> tuple[TrialWord, ...]:
    try:
        normalized = tuple(tuple(word) for word in trial_words)
    except TypeError as error:
        raise ValueError("trial_words must be an iterable of action words") from error
    ResettableTrialPanel(family=family, trial_words=normalized)
    return normalized


def observed_panel_signature(panel: ResettableTrialPanel, state: DelayedJointState) -> BaselinePanelSignature:
    """Zero-action focal baseline plus the fresh-copy panel traces."""
    panel.family.validate_state(state)
    return panel.family.output(state), panel.signature(state)


@dataclass(frozen=True)
class TerminalProbeCoverage:
    family: DelayedJointFamily
    read_ports: tuple[int, ...]
    covers_intervention: bool

    def __post_init__(self) -> None:
        if tuple(sorted(set(self.read_ports))) != self.read_ports:
            raise ValueError("read_ports must be sorted and unique")
        if any(not isinstance(port, int) or isinstance(port, bool) or not 0 <= port < self.family.exterior_port_count for port in self.read_ports):
            raise ValueError("read_ports contains an invalid structural port")

    @property
    def terminal_probe_count(self) -> int:
        return len(self.read_ports) + int(self.covers_intervention)

    @property
    def retained_interface_bits(self) -> int:
        return 1 + self.terminal_probe_count

    @property
    def quotient_block_count(self) -> int:
        return 2 ** self.retained_interface_bits

    @property
    def residual_block_cardinality(self) -> int:
        return 2 ** (self.family.exterior_port_count + 1 - self.terminal_probe_count)

    @property
    def is_full(self) -> bool:
        return self.terminal_probe_count == self.family.exterior_port_count + 1

    def projection(self, state: DelayedJointState) -> tuple[int, ...]:
        self.family.validate_state(state)
        values = [self.family.output(state)]
        values.extend(self.family.exterior_bit(state, port) for port in self.read_ports)
        if self.covers_intervention:
            values.append(self.family.response_type(state))
        return tuple(values)

    def verify(self) -> bool:
        try:
            return (
                tuple(sorted(set(self.read_ports))) == self.read_ports
                and self.quotient_block_count * self.residual_block_cardinality == self.family.state_count
                and int(log2(self.quotient_block_count)) == self.retained_interface_bits
            )
        except (TypeError, ValueError):
            return False


def terminal_probe_coverage(panel: ResettableTrialPanel) -> TerminalProbeCoverage:
    if not panel.verify():
        raise ValueError("panel must be valid")
    family = panel.family
    read_word_to_port = {
        family.grammar.revealing_read_word(port): port
        for port in range(family.exterior_port_count)
    }
    coverage = TerminalProbeCoverage(
        family=family,
        read_ports=tuple(sorted({read_word_to_port[word] for word in panel.trial_words if word in read_word_to_port})),
        covers_intervention=family.grammar.revealing_intervene_word in panel.trial_words,
    )
    if not coverage.verify():
        raise AssertionError("coverage did not verify")
    return coverage


def panel_projection_signature(panel: ResettableTrialPanel, state: DelayedJointState) -> tuple[int, ...]:
    return terminal_probe_coverage(panel).projection(state)


@dataclass(frozen=True)
class PanelQuotientCertificate:
    panel: ResettableTrialPanel
    coverage: TerminalProbeCoverage
    signature_block_count: int
    projection_block_count: int
    minimum_signature_block_cardinality: int
    maximum_signature_block_cardinality: int

    @property
    def retained_interface_bits(self) -> int:
        return self.coverage.retained_interface_bits

    @property
    def expected_block_count(self) -> int:
        return self.coverage.quotient_block_count

    @property
    def expected_residual_block_cardinality(self) -> int:
        return self.coverage.residual_block_cardinality

    def verify(self) -> bool:
        try:
            if not self.panel.verify() or not self.coverage.verify() or self.coverage.family != self.panel.family:
                return False
            states = self.panel.family.states
            record_labels = _labels(observed_panel_signature(self.panel, state) for state in states)
            projection_labels = _labels(self.coverage.projection(state) for state in states)
            if not _same_partition(record_labels, projection_labels):
                return False
            counts: dict[int, int] = {}
            for label in record_labels:
                counts[label] = counts.get(label, 0) + 1
            return (
                self.signature_block_count == len(counts) == self.expected_block_count
                and self.projection_block_count == len(set(projection_labels)) == self.expected_block_count
                and self.minimum_signature_block_cardinality == min(counts.values()) == self.expected_residual_block_cardinality
                and self.maximum_signature_block_cardinality == max(counts.values()) == self.expected_residual_block_cardinality
            )
        except (TypeError, ValueError):
            return False


def certify_panel_quotient(
    family: DelayedJointFamily,
    trial_words: Iterable[Iterable[DelayedJointAction]],
) -> PanelQuotientCertificate:
    panel = ResettableTrialPanel(family=family, trial_words=_words(family, trial_words))
    coverage = terminal_probe_coverage(panel)
    states = family.states
    labels = _labels(observed_panel_signature(panel, state) for state in states)
    projection_labels = _labels(coverage.projection(state) for state in states)
    counts: dict[int, int] = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    certificate = PanelQuotientCertificate(
        panel=panel,
        coverage=coverage,
        signature_block_count=len(counts),
        projection_block_count=len(set(projection_labels)),
        minimum_signature_block_cardinality=min(counts.values()),
        maximum_signature_block_cardinality=max(counts.values()),
    )
    if not certificate.verify():
        raise AssertionError("panel quotient certificate did not verify")
    return certificate


def canonical_covered_panel(family: DelayedJointFamily, probe_count: int) -> ResettableTrialPanel:
    _nonnegative(probe_count, "probe_count")
    words = required_terminal_words(family)[: min(probe_count, family.exterior_port_count + 1)]
    return ResettableTrialPanel(family=family, trial_words=words)


@dataclass(frozen=True)
class TrialBudgetFrontierCertificate:
    family: DelayedJointFamily
    trial_budget: int
    construction: PanelQuotientCertificate
    maximum_retained_interface_bits: int

    @property
    def expected_bits(self) -> int:
        return 1 + min(self.trial_budget, self.family.exterior_port_count + 1)

    def verify(self) -> bool:
        try:
            _nonnegative(self.trial_budget, "trial_budget")
            return (
                self.construction.verify()
                and self.construction.panel.family == self.family
                and self.construction.panel.trial_count <= self.trial_budget
                and self.construction.coverage.terminal_probe_count <= self.construction.panel.trial_count
                and self.maximum_retained_interface_bits == self.expected_bits
                and self.construction.retained_interface_bits == self.expected_bits
            )
        except (TypeError, ValueError):
            return False


def certify_trial_budget_frontier(exterior_port_count: int, delay: int, trial_budget: int) -> TrialBudgetFrontierCertificate:
    _nonnegative(trial_budget, "trial_budget")
    family = DelayedJointFamily(exterior_port_count, delay)
    panel = canonical_covered_panel(family, trial_budget)
    certificate = TrialBudgetFrontierCertificate(
        family=family,
        trial_budget=trial_budget,
        construction=certify_panel_quotient(family, panel.trial_words),
        maximum_retained_interface_bits=1 + min(trial_budget, exterior_port_count + 1),
    )
    if not certificate.verify():
        raise AssertionError("trial budget frontier did not verify")
    return certificate


@dataclass(frozen=True)
class ActionBudgetFrontierCertificate:
    family: DelayedJointFamily
    action_budget: int
    construction: PanelQuotientCertificate
    maximum_retained_interface_bits: int

    @property
    def affordable_terminal_probe_count(self) -> int:
        return min(self.action_budget // self.family.first_revealing_horizon, self.family.exterior_port_count + 1)

    @property
    def expected_bits(self) -> int:
        return 1 + self.affordable_terminal_probe_count

    def verify(self) -> bool:
        try:
            _nonnegative(self.action_budget, "action_budget")
            return (
                self.construction.verify()
                and self.construction.panel.family == self.family
                and self.construction.panel.total_action_count <= self.action_budget
                and self.construction.coverage.terminal_probe_count * self.family.first_revealing_horizon <= self.action_budget
                and self.maximum_retained_interface_bits == self.expected_bits
                and self.construction.retained_interface_bits == self.expected_bits
            )
        except (TypeError, ValueError):
            return False


def certify_action_budget_frontier(exterior_port_count: int, delay: int, action_budget: int) -> ActionBudgetFrontierCertificate:
    _nonnegative(action_budget, "action_budget")
    family = DelayedJointFamily(exterior_port_count, delay)
    count = min(action_budget // family.first_revealing_horizon, exterior_port_count + 1)
    panel = canonical_covered_panel(family, count)
    certificate = ActionBudgetFrontierCertificate(
        family=family,
        action_budget=action_budget,
        construction=certify_panel_quotient(family, panel.trial_words),
        maximum_retained_interface_bits=1 + count,
    )
    if not certificate.verify():
        raise AssertionError("action budget frontier did not verify")
    return certificate


@dataclass(frozen=True)
class DepthBudgetFrontierCertificate:
    family: DelayedJointFamily
    maximum_trial_horizon: int
    construction: PanelQuotientCertificate
    maximum_retained_interface_bits: int

    @property
    def can_reach_terminal_boundary(self) -> bool:
        return self.maximum_trial_horizon >= self.family.first_revealing_horizon

    @property
    def expected_bits(self) -> int:
        return self.family.exterior_port_count + 2 if self.can_reach_terminal_boundary else 1

    def verify(self) -> bool:
        try:
            _nonnegative(self.maximum_trial_horizon, "maximum_trial_horizon")
            return (
                self.construction.verify()
                and self.construction.panel.family == self.family
                and self.construction.panel.maximum_trial_horizon <= self.maximum_trial_horizon
                and self.maximum_retained_interface_bits == self.expected_bits
                and self.construction.retained_interface_bits == self.expected_bits
            )
        except (TypeError, ValueError):
            return False


def certify_depth_budget_frontier(exterior_port_count: int, delay: int, maximum_trial_horizon: int) -> DepthBudgetFrontierCertificate:
    _nonnegative(maximum_trial_horizon, "maximum_trial_horizon")
    family = DelayedJointFamily(exterior_port_count, delay)
    panel = (
        canonical_covered_panel(family, family.exterior_port_count + 1)
        if maximum_trial_horizon >= family.first_revealing_horizon
        else ResettableTrialPanel(family=family, trial_words=())
    )
    certificate = DepthBudgetFrontierCertificate(
        family=family,
        maximum_trial_horizon=maximum_trial_horizon,
        construction=certify_panel_quotient(family, panel.trial_words),
        maximum_retained_interface_bits=(family.exterior_port_count + 2 if maximum_trial_horizon >= family.first_revealing_horizon else 1),
    )
    if not certificate.verify():
        raise AssertionError("depth budget frontier did not verify")
    return certificate


@dataclass(frozen=True)
class MarginalProbeValueCertificate:
    initial: PanelQuotientCertificate
    added_word: TrialWord
    updated: PanelQuotientCertificate
    coverage_kind: CoverageKind
    delta_retained_interface_bits: int
    residual_ambiguity_ratio: int

    def verify(self) -> bool:
        try:
            if not self.initial.verify() or not self.updated.verify():
                return False
            family = self.initial.panel.family
            old, new = self.initial.coverage, self.updated.coverage
            if self.updated.panel.family != family or self.updated.panel.trial_words != self.initial.panel.trial_words + (self.added_word,):
                return False
            ResettableTrialPanel(family=family, trial_words=(self.added_word,))
            if self.delta_retained_interface_bits != new.retained_interface_bits - old.retained_interface_bits:
                return False
            if self.residual_ambiguity_ratio != old.residual_block_cardinality // new.residual_block_cardinality:
                return False
            if self.delta_retained_interface_bits == 1:
                if self.residual_ambiguity_ratio != 2:
                    return False
                if self.coverage_kind == "read":
                    terminal = self.added_word[-1]
                    return terminal.kind == "read" and terminal.read_port not in old.read_ports
                if self.coverage_kind == "intervene":
                    return self.added_word == family.grammar.revealing_intervene_word and not old.covers_intervention
                return False
            return self.delta_retained_interface_bits == 0 and self.residual_ambiguity_ratio == 1 and self.coverage_kind == "wait_or_duplicate"
        except (TypeError, ValueError):
            return False


def classify_added_word(coverage: TerminalProbeCoverage, word: TrialWord) -> CoverageKind:
    family = coverage.family
    for port in range(family.exterior_port_count):
        if word == family.grammar.revealing_read_word(port):
            return "read" if port not in coverage.read_ports else "wait_or_duplicate"
    if word == family.grammar.revealing_intervene_word:
        return "intervene" if not coverage.covers_intervention else "wait_or_duplicate"
    return "wait_or_duplicate"


def certify_marginal_probe_value(
    family: DelayedJointFamily,
    initial_trial_words: Iterable[Iterable[DelayedJointAction]],
    added_word: Iterable[DelayedJointAction],
) -> MarginalProbeValueCertificate:
    initial_words = _words(family, initial_trial_words)
    added = tuple(added_word)
    ResettableTrialPanel(family=family, trial_words=(added,))
    initial = certify_panel_quotient(family, initial_words)
    updated = certify_panel_quotient(family, initial_words + (added,))
    certificate = MarginalProbeValueCertificate(
        initial=initial,
        added_word=added,
        updated=updated,
        coverage_kind=classify_added_word(initial.coverage, added),
        delta_retained_interface_bits=updated.retained_interface_bits - initial.retained_interface_bits,
        residual_ambiguity_ratio=initial.expected_residual_block_cardinality // updated.expected_residual_block_cardinality,
    )
    if not certificate.verify():
        raise AssertionError("marginal probe value did not verify")
    return certificate


def exhaustive_budgeted_quotient_summary(
    max_exterior_port_count: int,
    max_delay: int,
    max_budget: int,
) -> tuple[PanelQuotientCertificate | TrialBudgetFrontierCertificate | ActionBudgetFrontierCertificate | DepthBudgetFrontierCertificate, ...]:
    if not isinstance(max_exterior_port_count, int) or isinstance(max_exterior_port_count, bool) or max_exterior_port_count < 1:
        raise ValueError("max_exterior_port_count must be positive")
    _nonnegative(max_delay, "max_delay")
    _nonnegative(max_budget, "max_budget")
    certificates: list[PanelQuotientCertificate | TrialBudgetFrontierCertificate | ActionBudgetFrontierCertificate | DepthBudgetFrontierCertificate] = []
    for m in range(1, max_exterior_port_count + 1):
        for delay in range(max_delay + 1):
            family = DelayedJointFamily(m, delay)
            for budget in range(max_budget + 1):
                certificates.extend((
                    certify_trial_budget_frontier(m, delay, budget),
                    certify_action_budget_frontier(m, delay, budget),
                    certify_depth_budget_frontier(m, delay, budget),
                ))
            for count in range(m + 2):
                panel = canonical_covered_panel(family, count)
                certificates.append(certify_panel_quotient(family, panel.trial_words))
    return tuple(certificates)
