"""Budgeted exact quotients for delayed joint reset panels.

The full reset-panel theorem identifies the sharp resources required to recover
all of a delayed binary joint state.  This module resolves the intermediate
case: a finite reset panel can cover only some terminal probes, and therefore
identifies an exact *partial* quotient rather than either everything or nothing.

For a delayed joint state

    (y, b_1, ..., b_m, r) in {0, 1}^{m + 2}

let ``P`` be a panel of legal initial words, each run from a fresh copy.  Write
``R(P)`` for exterior ports whose delayed read word occurs in ``P`` and ``J(P)``
for whether the delayed intervention word occurs.  Then panel-signature
indistinguishability is exactly equality of

    y, (b_i for i in R(P)), and r when J(P)=1.

Consequently the quotient and residual ambiguity are

    |X / ~_P| = 2^(1 + |R(P)| + J(P)),
    |[x]_P|  = 2^(m + 1 - |R(P)| - J(P)).

Duplicate terminal probes and wait-only trials have zero marginal value.  Every
newly covered terminal probe adds exactly one exact bit and halves residual
ambiguity.  This yields sharp trial-, action-, and depth-budget frontiers for the
fixed finite family.

All statements use explicit fresh-reset semantics inherited from
``ResettableTrialPanel``.  They are not claims about stochastic information,
mutual information, noisy experiment design, or non-resettable ecosystems.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import log2
from typing import Iterable, Literal

from .delayed_joint_nonidentifiability import DelayedJointAction, DelayedJointFamily, DelayedJointState
from .delayed_joint_reset_panels import ResettableTrialPanel, TrialWord, required_terminal_words

CoverageKind = Literal["read", "intervene", "wait_or_duplicate"]


def _validate_nonnegative_integer(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")


def _normalize_words(
    family: DelayedJointFamily,
    trial_words: Iterable[Iterable[DelayedJointAction]],
) -> tuple[TrialWord, ...]:
    try:
        words = tuple(tuple(word) for word in trial_words)
    except TypeError as error:
        raise ValueError("trial_words must be an iterable of iterable action words") from error
    # The panel constructor performs the authoritative legal-word validation.
    ResettableTrialPanel(family=family, trial_words=words)
    return words


def _canonical_labels(values: Iterable[object]) -> tuple[int, ...]:
    labels: dict[object, int] = {}
    result: list[int] = []
    for value in values:
        if value not in labels:
            labels[value] = len(labels)
        result.append(labels[value])
    return tuple(result)


def _same_partition(left: tuple[int, ...], right: tuple[int, ...]) -> bool:
    if len(left) != len(right):
        return False
    return all(
        (left[i] == left[j]) == (right[i] == right[j])
        for i in range(len(left))
        for j in range(len(left))
    )


@dataclass(frozen=True)
class TerminalProbeCoverage:
    """The information-bearing terminal probes present in one reset panel."""

    family: DelayedJointFamily
    read_ports: tuple[int, ...]
    covers_intervention: bool

    def __post_init__(self) -> None:
        if tuple(sorted(set(self.read_ports))) != self.read_ports:
            raise ValueError("read_ports must be sorted, unique, and canonical")
        if any(
            not isinstance(port, int) or isinstance(port, bool) or not 0 <= port < self.family.exterior_port_count
            for port in self.read_ports
        ):
            raise ValueError("read_ports contains an invalid structural port")

    @property
    def terminal_probe_count(self) -> int:
        return len(self.read_ports) + int(self.covers_intervention)

    @property
    def retained_interface_bits(self) -> int:
        """Includes the always observed initial focal bit y."""
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

    def coordinate_projection(self, state: DelayedJointState) -> tuple[int, ...]:
        self.family.validate_state(state)
        values = [self.family.output(state)]
        values.extend(self.family.exterior_bit(state, port) for port in self.read_ports)
        if self.covers_intervention:
            values.append(self.family.response_type(state))
        return tuple(values)

    def verify(self) -> bool:
        try:
            expected_ports = tuple(sorted(set(self.read_ports)))
            if self.read_ports != expected_ports:
                return False
            if any(not 0 <= port < self.family.exterior_port_count for port in self.read_ports):
                return False
            if self.quotient_block_count * self.residual_block_cardinality != self.family.state_count:
                return False
            return self.retained_interface_bits == int(log2(self.quotient_block_count))
        except (TypeError, ValueError):
            return False


def terminal_probe_coverage(panel: ResettableTrialPanel) -> TerminalProbeCoverage:
    """Extract canonical coverage; trial multiplicity and order are irrelevant."""
    if not panel.verify():
        raise ValueError("panel must be a valid resettable trial panel")
    family = panel.family
    read_words = {family.grammar.revealing_read_word(port): port for port in range(family.exterior_port_count)}
    read_ports = tuple(sorted({read_words[word] for word in panel.trial_words if word in read_words}))
    coverage = TerminalProbeCoverage(
        family=family,
        read_ports=read_ports,
        covers_intervention=family.grammar.revealing_intervene_word in panel.trial_words,
    )
    if not coverage.verify():
        raise AssertionError("terminal probe coverage did not verify")
    return coverage


def panel_projection_signature(panel: ResettableTrialPanel, state: DelayedJointState) -> tuple[int, ...]:
    """Coordinate summary claimed to be exactly equivalent to panel signature."""
    return terminal_probe_coverage(panel).coordinate_projection(state)


@dataclass(frozen=True)
class PanelQuotientCertificate:
    """Exact equivalence of a panel signature and its covered-coordinate projection."""

    panel: ResettableTrialPanel
    coverage: TerminalProbeCoverage
    signature_block_count: int
    projection_block_count: int
    minimum_signature_block_cardinality: int
    maximum_signature_block_cardinality: int

    @property
    def expected_block_count(self) -> int:
        return self.coverage.quotient_block_count

    @property
    def expected_residual_block_cardinality(self) -> int:
        return self.coverage.residual_block_cardinality

    @property
    def retained_interface_bits(self) -> int:
        return self.coverage.retained_interface_bits

    def verify(self) -> bool:
        try:
            if not self.panel.verify() or not self.coverage.verify() or self.coverage.family != self.panel.family:
                return False
            states = self.panel.family.states
            signature_labels = _canonical_labels(self.panel.signature(state) for state in states)
            projection_labels = _canonical_labels(self.coverage.coordinate_projection(state) for state in states)
            if not _same_partition(signature_labels, projection_labels):
                return False
            blocks: dict[int, int] = {}
            for label in signature_labels:
                blocks[label] = blocks.get(label, 0) + 1
            cardinalities = tuple(blocks.values())
            if self.signature_block_count != len(blocks):
                return False
            if self.projection_block_count != len(set(projection_labels)):
                return False
            if self.minimum_signature_block_cardinality != min(cardinalities):
                return False
            if self.maximum_signature_block_cardinality != max(cardinalities):
                return False
            return (
                self.signature_block_count == self.expected_block_count
                and self.projection_block_count == self.expected_block_count
                and self.minimum_signature_block_cardinality == self.expected_residual_block_cardinality
                and self.maximum_signature_block_cardinality == self.expected_residual_block_cardinality
            )
        except (TypeError, ValueError):
            return False


def certify_panel_quotient(
    family: DelayedJointFamily,
    trial_words: Iterable[Iterable[DelayedJointAction]],
) -> PanelQuotientCertificate:
    panel = ResettableTrialPanel(family=family, trial_words=_normalize_words(family, trial_words))
    coverage = terminal_probe_coverage(panel)
    states = family.states
    signature_labels = _canonical_labels(panel.signature(state) for state in states)
    projection_labels = _canonical_labels(coverage.coordinate_projection(state) for state in states)
    blocks: dict[int, int] = {}
    for label in signature_labels:
        blocks[label] = blocks.get(label, 0) + 1
    certificate = PanelQuotientCertificate(
        panel=panel,
        coverage=coverage,
        signature_block_count=len(blocks),
        projection_block_count=len(set(projection_labels)),
        minimum_signature_block_cardinality=min(blocks.values()),
        maximum_signature_block_cardinality=max(blocks.values()),
    )
    if not certificate.verify():
        raise AssertionError("panel quotient certificate did not verify")
    return certificate


def canonical_covered_panel(family: DelayedJointFamily, probe_count: int) -> ResettableTrialPanel:
    """A deterministic at-most-budget construction using distinct terminal probes."""
    _validate_nonnegative_integer(probe_count, "probe_count")
    words = required_terminal_words(family)[: min(probe_count, family.exterior_port_count + 1)]
    panel = ResettableTrialPanel(family=family, trial_words=words)
    if not panel.verify():
        raise AssertionError("canonical covered panel did not verify")
    return panel


@dataclass(frozen=True)
class TrialBudgetFrontierCertificate:
    """Sharp maximum exact quotient under an at-most-N fresh-trial budget."""

    family: DelayedJointFamily
    trial_budget: int
    construction: PanelQuotientCertificate
    maximum_retained_interface_bits: int

    @property
    def expected_bits(self) -> int:
        return 1 + min(self.trial_budget, self.family.exterior_port_count + 1)

    @property
    def expected_residual_cardinality(self) -> int:
        return 2 ** (self.family.exterior_port_count + 2 - self.expected_bits)

    def verify(self) -> bool:
        try:
            _validate_nonnegative_integer(self.trial_budget, "trial_budget")
            if not self.construction.verify() or self.construction.panel.family != self.family:
                return False
            if self.construction.panel.trial_count > self.trial_budget:
                return False
            # One legal trial can contain at most one terminal probe because the grammar then terminates.
            if self.construction.coverage.terminal_probe_count > self.construction.panel.trial_count:
                return False
            if self.maximum_retained_interface_bits != self.expected_bits:
                return False
            return (
                self.construction.retained_interface_bits == self.expected_bits
                and self.construction.expected_residual_block_cardinality == self.expected_residual_cardinality
            )
        except (TypeError, ValueError):
            return False


def certify_trial_budget_frontier(
    exterior_port_count: int,
    delay: int,
    trial_budget: int,
) -> TrialBudgetFrontierCertificate:
    _validate_nonnegative_integer(trial_budget, "trial_budget")
    family = DelayedJointFamily(exterior_port_count, delay)
    panel = canonical_covered_panel(family, trial_budget)
    certificate = TrialBudgetFrontierCertificate(
        family=family,
        trial_budget=trial_budget,
        construction=certify_panel_quotient(family, panel.trial_words),
        maximum_retained_interface_bits=1 + min(trial_budget, exterior_port_count + 1),
    )
    if not certificate.verify():
        raise AssertionError("trial-budget frontier certificate did not verify")
    return certificate


@dataclass(frozen=True)
class ActionBudgetFrontierCertificate:
    """Sharp maximum exact quotient under an at-most-A total-action budget."""

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

    @property
    def expected_residual_cardinality(self) -> int:
        return 2 ** (self.family.exterior_port_count + 2 - self.expected_bits)

    def verify(self) -> bool:
        try:
            _validate_nonnegative_integer(self.action_budget, "action_budget")
            if not self.construction.verify() or self.construction.panel.family != self.family:
                return False
            if self.construction.panel.total_action_count > self.action_budget:
                return False
            # Every covered terminal probe is a distinct word of length exactly H+1.
            if self.construction.coverage.terminal_probe_count * self.family.first_revealing_horizon > self.action_budget:
                return False
            if self.maximum_retained_interface_bits != self.expected_bits:
                return False
            return (
                self.construction.retained_interface_bits == self.expected_bits
                and self.construction.expected_residual_block_cardinality == self.expected_residual_cardinality
            )
        except (TypeError, ValueError):
            return False


def certify_action_budget_frontier(
    exterior_port_count: int,
    delay: int,
    action_budget: int,
) -> ActionBudgetFrontierCertificate:
    _validate_nonnegative_integer(action_budget, "action_budget")
    family = DelayedJointFamily(exterior_port_count, delay)
    probe_count = min(action_budget // family.first_revealing_horizon, exterior_port_count + 1)
    panel = canonical_covered_panel(family, probe_count)
    certificate = ActionBudgetFrontierCertificate(
        family=family,
        action_budget=action_budget,
        construction=certify_panel_quotient(family, panel.trial_words),
        maximum_retained_interface_bits=1 + probe_count,
    )
    if not certificate.verify():
        raise AssertionError("action-budget frontier certificate did not verify")
    return certificate


@dataclass(frozen=True)
class DepthBudgetFrontierCertificate:
    """Sharp quotient frontier when reset trials are unlimited but depth is bounded."""

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
            _validate_nonnegative_integer(self.maximum_trial_horizon, "maximum_trial_horizon")
            if not self.construction.verify() or self.construction.panel.family != self.family:
                return False
            if self.construction.panel.maximum_trial_horizon > self.maximum_trial_horizon:
                return False
            if self.maximum_retained_interface_bits != self.expected_bits:
                return False
            return self.construction.retained_interface_bits == self.expected_bits
        except (TypeError, ValueError):
            return False


def certify_depth_budget_frontier(
    exterior_port_count: int,
    delay: int,
    maximum_trial_horizon: int,
) -> DepthBudgetFrontierCertificate:
    _validate_nonnegative_integer(maximum_trial_horizon, "maximum_trial_horizon")
    family = DelayedJointFamily(exterior_port_count, delay)
    if maximum_trial_horizon < family.first_revealing_horizon:
        panel = ResettableTrialPanel(family=family, trial_words=())
    else:
        panel = canonical_covered_panel(family, family.exterior_port_count + 1)
    certificate = DepthBudgetFrontierCertificate(
        family=family,
        maximum_trial_horizon=maximum_trial_horizon,
        construction=certify_panel_quotient(family, panel.trial_words),
        maximum_retained_interface_bits=(
            family.exterior_port_count + 2 if maximum_trial_horizon >= family.first_revealing_horizon else 1
        ),
    )
    if not certificate.verify():
        raise AssertionError("depth-budget frontier certificate did not verify")
    return certificate


@dataclass(frozen=True)
class MarginalProbeValueCertificate:
    """Exact one-bit-or-zero marginal value of adding one legal reset trial."""

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
            if self.updated.panel.family != family:
                return False
            if self.updated.panel.trial_words != self.initial.panel.trial_words + (self.added_word,):
                return False
            ResettableTrialPanel(family=family, trial_words=(self.added_word,))
            old = self.initial.coverage
            new = self.updated.coverage
            if self.delta_retained_interface_bits != new.retained_interface_bits - old.retained_interface_bits:
                return False
            if self.residual_ambiguity_ratio != old.residual_block_cardinality // new.residual_block_cardinality:
                return False
            if self.delta_retained_interface_bits not in (0, 1):
                return False
            if self.delta_retained_interface_bits == 1:
                if self.residual_ambiguity_ratio != 2:
                    return False
                if self.coverage_kind == "read":
                    final = self.added_word[-1]
                    if final.kind != "read" or final.read_port is None or final.read_port in old.read_ports:
                        return False
                elif self.coverage_kind == "intervene":
                    if self.added_word != family.grammar.revealing_intervene_word or old.covers_intervention:
                        return False
                else:
                    return False
            else:
                if self.residual_ambiguity_ratio != 1 or self.coverage_kind != "wait_or_duplicate":
                    return False
            return True
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
    initial_words = _normalize_words(family, initial_trial_words)
    normalized_added = tuple(added_word)
    ResettableTrialPanel(family=family, trial_words=(normalized_added,))
    initial = certify_panel_quotient(family, initial_words)
    updated = certify_panel_quotient(family, initial_words + (normalized_added,))
    certificate = MarginalProbeValueCertificate(
        initial=initial,
        added_word=normalized_added,
        updated=updated,
        coverage_kind=classify_added_word(initial.coverage, normalized_added),
        delta_retained_interface_bits=updated.retained_interface_bits - initial.retained_interface_bits,
        residual_ambiguity_ratio=(
            initial.expected_residual_block_cardinality // updated.expected_residual_block_cardinality
        ),
    )
    if not certificate.verify():
        raise AssertionError("marginal probe-value certificate did not verify")
    return certificate


def exhaustive_budgeted_quotient_summary(
    max_exterior_port_count: int,
    max_delay: int,
    max_budget: int,
) -> tuple[PanelQuotientCertificate | TrialBudgetFrontierCertificate | ActionBudgetFrontierCertificate | DepthBudgetFrontierCertificate, ...]:
    _validate_nonnegative_integer(max_delay, "max_delay")
    _validate_nonnegative_integer(max_budget, "max_budget")
    if not isinstance(max_exterior_port_count, int) or isinstance(max_exterior_port_count, bool) or max_exterior_port_count < 1:
        raise ValueError("max_exterior_port_count must be positive")
    certificates: list[PanelQuotientCertificate | TrialBudgetFrontierCertificate | ActionBudgetFrontierCertificate | DepthBudgetFrontierCertificate] = []
    for exterior_port_count in range(1, max_exterior_port_count + 1):
        for delay in range(max_delay + 1):
            family = DelayedJointFamily(exterior_port_count, delay)
            for budget in range(max_budget + 1):
                certificates.append(certify_trial_budget_frontier(exterior_port_count, delay, budget))
                certificates.append(certify_action_budget_frontier(exterior_port_count, delay, budget))
                certificates.append(certify_depth_budget_frontier(exterior_port_count, delay, budget))
            for probe_count in range(exterior_port_count + 2):
                panel = canonical_covered_panel(family, probe_count)
                certificates.append(certify_panel_quotient(family, panel.trial_words))
    return tuple(certificates)
