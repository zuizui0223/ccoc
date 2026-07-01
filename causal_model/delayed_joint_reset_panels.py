"""Exact reset-panel complexity for delayed joint identification.

``delayed_joint_nonidentifiability`` proves that one fixed horizon cannot certify
candidate-safe open closure uniformly when joint exterior and response-type
distinctions are delayed.  This module gives the positive fixed-family
counterpart under one explicit resource model:

* every trial is applied to a fresh resettable copy of the same unknown initial
  delayed-joint state; and
* a panel record is the ordered tuple of output traces from those independent
  trials.

For the binary delayed joint state

    (y, b_1, ..., b_m, r) in {0,1}^{m+2}

with delay ``H``, exact identification has the sharp resource vector

    minimum resettable trials = m + 1,
    minimum maximum trial horizon = H + 1,
    minimum total sequential action count = (m + 1)(H + 1).

The canonical panel uses every delayed structural read word plus the delayed
intervention word.  The lower bound is exact because a pair differing only in
``b_i`` is separated by no legal initial word except the word ending in
``read_i``; a pair differing only in ``r`` is separated only by the word ending
in ``intervene``.

This is a finite deterministic experiment-complexity theorem.  It does not
assume that empirical ecosystems are resettable, binary, or noiseless.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable

from .delayed_joint_nonidentifiability import (
    DelayedJointAction,
    DelayedJointFamily,
    DelayedJointState,
)

TrialWord = tuple[DelayedJointAction, ...]
PanelSignature = tuple[tuple[int, ...], ...]


def _validate_positive_integer(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _normalize_trial_word(family: DelayedJointFamily, word: Iterable[DelayedJointAction]) -> TrialWord:
    try:
        normalized = tuple(word)
    except TypeError as error:
        raise ValueError("trial word must be iterable") from error
    if family.grammar.normalize_legal_word(normalized) != normalized:
        raise AssertionError("legal-word normalization unexpectedly changed a word")
    return normalized


def required_terminal_words(family: DelayedJointFamily) -> tuple[TrialWord, ...]:
    """The distinct terminal words that are individually necessary for exactness."""
    return tuple(
        family.grammar.revealing_read_word(port)
        for port in range(family.exterior_port_count)
    ) + (family.grammar.revealing_intervene_word,)


@dataclass(frozen=True)
class ResettableTrialPanel:
    """A finite list of legal initial words, each run on a fresh system copy.

    The class deliberately does not provide a stateful ``run_next`` method.
    Each signature component calls ``family.trace`` from the original grammar
    state and original macro state, which makes reset semantics explicit.
    """

    family: DelayedJointFamily
    trial_words: tuple[TrialWord, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.trial_words, tuple):
            raise ValueError("trial_words must be a tuple")
        for word in self.trial_words:
            if not isinstance(word, tuple):
                raise ValueError("each trial word must be a tuple")
            _normalize_trial_word(self.family, word)

    @property
    def trial_count(self) -> int:
        return len(self.trial_words)

    @property
    def maximum_trial_horizon(self) -> int:
        return max((len(word) for word in self.trial_words), default=0)

    @property
    def total_action_count(self) -> int:
        return sum(len(word) for word in self.trial_words)

    @property
    def distinct_trial_words(self) -> tuple[TrialWord, ...]:
        seen: set[TrialWord] = set()
        ordered: list[TrialWord] = []
        for word in self.trial_words:
            if word not in seen:
                seen.add(word)
                ordered.append(word)
        return tuple(ordered)

    def signature(self, state: DelayedJointState) -> PanelSignature:
        self.family.validate_state(state)
        return tuple(self.family.trace(state, word) for word in self.trial_words)

    def first_collision(self) -> tuple[DelayedJointState, DelayedJointState] | None:
        signatures: dict[PanelSignature, DelayedJointState] = {}
        for state in self.family.states:
            signature = self.signature(state)
            previous = signatures.get(signature)
            if previous is not None and previous != state:
                return previous, state
            signatures[signature] = state
        return None

    @property
    def is_exact(self) -> bool:
        return self.first_collision() is None

    def verify(self) -> bool:
        try:
            if not self.family.grammar.verify():
                return False
            for word in self.trial_words:
                if _normalize_trial_word(self.family, word) != word:
                    return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


@dataclass(frozen=True)
class ResetPanelExactnessCertificate:
    """Certificate that a reset panel identifies every delayed joint state."""

    panel: ResettableTrialPanel
    state_count: int
    signature_count: int

    def verify(self) -> bool:
        try:
            if not self.panel.verify():
                return False
            if self.state_count != self.panel.family.state_count:
                return False
            signatures = {self.panel.signature(state) for state in self.panel.family.states}
            if self.signature_count != len(signatures):
                return False
            return self.signature_count == self.state_count and self.panel.is_exact
        except (TypeError, ValueError):
            return False


def certify_reset_panel_exactness(
    family: DelayedJointFamily,
    trial_words: Iterable[Iterable[DelayedJointAction]],
) -> ResetPanelExactnessCertificate:
    panel = ResettableTrialPanel(
        family=family,
        trial_words=tuple(_normalize_trial_word(family, word) for word in trial_words),
    )
    certificate = ResetPanelExactnessCertificate(
        panel=panel,
        state_count=family.state_count,
        signature_count=len({panel.signature(state) for state in family.states}),
    )
    if not certificate.verify():
        raise ValueError("reset panel is not exact for the declared delayed joint family")
    return certificate


@dataclass(frozen=True)
class TerminalProbeNecessityCertificate:
    """A coordinate pair uniquely separated by one required terminal word."""

    family: DelayedJointFamily
    coordinate_kind: str
    exterior_port: int | None
    left: DelayedJointState
    right: DelayedJointState
    required_word: TrialWord

    def verify(self) -> bool:
        try:
            self.family.validate_state(self.left)
            self.family.validate_state(self.right)
            if self.left == self.right:
                return False
            legal_words = self.family.grammar.legal_words_through(self.family.first_revealing_horizon)
            if self.required_word not in legal_words:
                return False
            if self.coordinate_kind == "exterior":
                if not isinstance(self.exterior_port, int) or isinstance(self.exterior_port, bool):
                    return False
                if not 0 <= self.exterior_port < self.family.exterior_port_count:
                    return False
                expected_left = (0,) + (0,) * self.family.exterior_port_count + (0,)
                expected_right = (
                    (0,)
                    + tuple(1 if index == self.exterior_port else 0 for index in range(self.family.exterior_port_count))
                    + (0,)
                )
                if self.left != expected_left or self.right != expected_right:
                    return False
                if self.required_word != self.family.grammar.revealing_read_word(self.exterior_port):
                    return False
            elif self.coordinate_kind == "response":
                if self.exterior_port is not None:
                    return False
                expected_left = (0,) + (0,) * self.family.exterior_port_count + (0,)
                expected_right = (0,) + (0,) * self.family.exterior_port_count + (1,)
                if self.left != expected_left or self.right != expected_right:
                    return False
                if self.required_word != self.family.grammar.revealing_intervene_word:
                    return False
            else:
                return False
            if self.family.trace(self.left, self.required_word) == self.family.trace(self.right, self.required_word):
                return False
            for word in legal_words:
                if word == self.required_word:
                    continue
                if self.family.trace(self.left, word) != self.family.trace(self.right, word):
                    return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def terminal_probe_necessity_certificates(
    family: DelayedJointFamily,
) -> tuple[TerminalProbeNecessityCertificate, ...]:
    zero = (0,) + (0,) * family.exterior_port_count + (0,)
    certificates = tuple(
        TerminalProbeNecessityCertificate(
            family=family,
            coordinate_kind="exterior",
            exterior_port=port,
            left=zero,
            right=(0,)
            + tuple(1 if index == port else 0 for index in range(family.exterior_port_count))
            + (0,),
            required_word=family.grammar.revealing_read_word(port),
        )
        for port in range(family.exterior_port_count)
    ) + (
        TerminalProbeNecessityCertificate(
            family=family,
            coordinate_kind="response",
            exterior_port=None,
            left=zero,
            right=(0,) + (0,) * family.exterior_port_count + (1,),
            required_word=family.grammar.revealing_intervene_word,
        ),
    )
    if not all(certificate.verify() for certificate in certificates):
        raise AssertionError("terminal-probe necessity certificates did not verify")
    return certificates


@dataclass(frozen=True)
class MissingTerminalProbeCertificate:
    """A proposed panel fails because it omits one uniquely necessary probe."""

    panel: ResettableTrialPanel
    necessity: TerminalProbeNecessityCertificate

    def verify(self) -> bool:
        try:
            if not self.panel.verify() or not self.necessity.verify():
                return False
            if self.panel.family != self.necessity.family:
                return False
            if self.necessity.required_word in self.panel.trial_words:
                return False
            return self.panel.signature(self.necessity.left) == self.panel.signature(self.necessity.right)
        except (TypeError, ValueError):
            return False


def find_missing_terminal_probe(
    family: DelayedJointFamily,
    trial_words: Iterable[Iterable[DelayedJointAction]],
) -> MissingTerminalProbeCertificate | None:
    panel = ResettableTrialPanel(
        family=family,
        trial_words=tuple(_normalize_trial_word(family, word) for word in trial_words),
    )
    for necessity in terminal_probe_necessity_certificates(family):
        if necessity.required_word not in panel.trial_words:
            certificate = MissingTerminalProbeCertificate(panel=panel, necessity=necessity)
            if not certificate.verify():
                raise AssertionError("missing terminal-probe certificate did not verify")
            return certificate
    return None


def canonical_reset_panel(family: DelayedJointFamily) -> ResettableTrialPanel:
    panel = ResettableTrialPanel(family=family, trial_words=required_terminal_words(family))
    if not panel.verify():
        raise AssertionError("canonical reset panel did not verify")
    return panel


@dataclass(frozen=True)
class DelayedJointResetPanelComplexityCertificate:
    """Sharp trial, depth, and total-action complexity for one family member."""

    family: DelayedJointFamily
    canonical_panel: ResettableTrialPanel
    exactness: ResetPanelExactnessCertificate
    necessity_certificates: tuple[TerminalProbeNecessityCertificate, ...]
    minimum_trial_count: int
    minimum_maximum_trial_horizon: int
    minimum_total_action_count: int

    @property
    def expected_trial_count(self) -> int:
        return self.family.exterior_port_count + 1

    @property
    def expected_maximum_trial_horizon(self) -> int:
        return self.family.first_revealing_horizon

    @property
    def expected_total_action_count(self) -> int:
        return self.expected_trial_count * self.expected_maximum_trial_horizon

    @property
    def parallel_wall_clock_lower_bound(self) -> int:
        """With unrestricted parallel resettable replicas, depth remains H + 1."""
        return self.expected_maximum_trial_horizon

    def verify(self) -> bool:
        try:
            if self.canonical_panel.family != self.family or not self.canonical_panel.verify():
                return False
            if not self.exactness.verify() or self.exactness.panel != self.canonical_panel:
                return False
            if self.canonical_panel.trial_words != required_terminal_words(self.family):
                return False
            if len(self.necessity_certificates) != self.expected_trial_count:
                return False
            if tuple(certificate.required_word for certificate in self.necessity_certificates) != required_terminal_words(
                self.family
            ):
                return False
            if not all(certificate.verify() for certificate in self.necessity_certificates):
                return False
            if len(set(self.canonical_panel.trial_words)) != self.expected_trial_count:
                return False
            if self.minimum_trial_count != self.expected_trial_count:
                return False
            if self.minimum_maximum_trial_horizon != self.expected_maximum_trial_horizon:
                return False
            if self.minimum_total_action_count != self.expected_total_action_count:
                return False
            if self.canonical_panel.trial_count != self.minimum_trial_count:
                return False
            if self.canonical_panel.maximum_trial_horizon != self.minimum_maximum_trial_horizon:
                return False
            if self.canonical_panel.total_action_count != self.minimum_total_action_count:
                return False
            if self.parallel_wall_clock_lower_bound != self.minimum_maximum_trial_horizon:
                return False
            for subset_size in range(self.expected_trial_count):
                for subset in combinations(self.canonical_panel.trial_words, subset_size):
                    obstruction = find_missing_terminal_probe(self.family, subset)
                    if obstruction is None or not obstruction.verify():
                        return False
            return True
        except (AssertionError, TypeError, ValueError):
            return False


def certify_delayed_joint_reset_panel_complexity(
    exterior_port_count: int,
    delay: int,
) -> DelayedJointResetPanelComplexityCertificate:
    family = DelayedJointFamily(exterior_port_count=exterior_port_count, delay=delay)
    panel = canonical_reset_panel(family)
    exactness = certify_reset_panel_exactness(family, panel.trial_words)
    certificate = DelayedJointResetPanelComplexityCertificate(
        family=family,
        canonical_panel=panel,
        exactness=exactness,
        necessity_certificates=terminal_probe_necessity_certificates(family),
        minimum_trial_count=exterior_port_count + 1,
        minimum_maximum_trial_horizon=family.first_revealing_horizon,
        minimum_total_action_count=(exterior_port_count + 1) * family.first_revealing_horizon,
    )
    if not certificate.verify():
        raise AssertionError("delayed joint reset-panel complexity certificate did not verify")
    return certificate


def exhaustive_reset_panel_complexity_summary(
    max_exterior_port_count: int,
    max_delay: int,
) -> tuple[DelayedJointResetPanelComplexityCertificate, ...]:
    _validate_positive_integer(max_exterior_port_count, "max_exterior_port_count")
    if not isinstance(max_delay, int) or isinstance(max_delay, bool) or max_delay < 0:
        raise ValueError("max_delay must be a non-negative integer")
    return tuple(
        certify_delayed_joint_reset_panel_complexity(exterior_port_count, delay)
        for exterior_port_count in range(1, max_exterior_port_count + 1)
        for delay in range(max_delay + 1)
    )
