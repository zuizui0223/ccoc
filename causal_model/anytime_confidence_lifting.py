"""Anytime confidence-set lifting for sequential RACH decisions.

This module extends the distribution-agnostic confidence-set lifting theorem to
repeated looks at arbitrary random data.  The external procedure supplies a
*simultaneous-over-time* coverage certificate for retained candidate sets.  RACH
then preserves that guarantee across every allowed look, every motif, and every
possibly data-dependent stopping rule whose stopping time lies in the certified
look scope.

No raw data, likelihood, independence, or sampling model is specified here.
Those assumptions belong entirely to the external procedure that establishes the
confidence-sequence / anytime-confidence-set coverage claim.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .confidence_lifting import (
    CandidateMotifUniverse,
    ConfidenceSetCell,
    classify_confidence_sets,
    false_decisive_motifs,
    joint_coverage_event,
)


def _unit_interval(value: float, name: str) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must lie in [0, 1]")


@dataclass(frozen=True)
class SequentialConfidenceSetSnapshot:
    """Retained candidate sets at one positive integer look index.

    A look index is an analysis opportunity, not necessarily an observation
    count. It can represent an interim sample size, a calendar checkpoint, an
    adaptive batch boundary, or any other ordered information time declared by
    the external sequential procedure.
    """

    look: int
    cells: tuple[ConfidenceSetCell, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.look, int) or self.look < 1:
            raise ValueError("look must be a positive integer")
        if not self.cells:
            raise ValueError("each sequential snapshot needs at least one cell")


@dataclass(frozen=True)
class AnytimeJointCoverageCertificate:
    """External simultaneous coverage for all required cells and all certified looks.

    The certificate asserts

    ``P(for every certified look t, true candidate is retained in every required cell) >= lower_bound``.

    With ``certified_looks=None``, the assertion must cover every positive integer
    look, as supplied for example by an externally valid confidence sequence. A
    finite explicit tuple is also allowed for a predeclared sequence of interim
    analyses. This class records the assertion but does not derive it.
    """

    true_candidate_id: str
    required_cell_ids: tuple[str, ...]
    lower_bound: float
    method: str
    assumptions: tuple[str, ...] = ()
    certified_looks: tuple[int, ...] | None = None

    def __post_init__(self) -> None:
        if not self.true_candidate_id:
            raise ValueError("true_candidate_id must be non-empty")
        if not self.required_cell_ids:
            raise ValueError("required_cell_ids must not be empty")
        if len(set(self.required_cell_ids)) != len(self.required_cell_ids):
            raise ValueError("required_cell_ids must be unique")
        _unit_interval(self.lower_bound, "lower_bound")
        if not self.method:
            raise ValueError("method must be non-empty")
        if self.certified_looks is not None:
            if not self.certified_looks:
                raise ValueError("certified_looks must be non-empty when provided")
            if any(not isinstance(look, int) or look < 1 for look in self.certified_looks):
                raise ValueError("certified_looks must contain positive integers")
            if len(set(self.certified_looks)) != len(self.certified_looks):
                raise ValueError("certified_looks must be unique")

    @property
    def miscoverage_upper_bound(self) -> float:
        return 1.0 - self.lower_bound

    @property
    def is_time_uniform(self) -> bool:
        """Whether the external assertion covers every positive integer look."""

        return self.certified_looks is None

    def covers_look(self, look: int) -> bool:
        """Whether the declared certificate covers a particular look index."""

        return self.certified_looks is None or look in self.certified_looks


@dataclass(frozen=True)
class AnytimeLiftingWitness:
    """Pointwise relation between time-uniform retention and RACH conclusions."""

    true_candidate_id: str
    joint_retention_by_look: Mapping[int, bool]
    false_decisive_motifs_by_look: Mapping[int, tuple[str, ...]]

    @property
    def joint_retention_at_all_looks(self) -> bool:
        return all(self.joint_retention_by_look.values())

    @property
    def false_decisive_looks(self) -> tuple[int, ...]:
        return tuple(
            look
            for look, motifs in self.false_decisive_motifs_by_look.items()
            if motifs
        )

    @property
    def any_false_decisive_claim(self) -> bool:
        return bool(self.false_decisive_looks)

    @property
    def implication_holds(self) -> bool:
        """Whether any false decisive claim implies some joint-retention failure."""

        return not self.any_false_decisive_claim or not self.joint_retention_at_all_looks


@dataclass(frozen=True)
class AnytimeRACHSoundnessGuarantee:
    """Time-uniform, motif-uniform false-decisive control from external coverage."""

    true_candidate_id: str
    joint_time_uniform_coverage_lower_bound: float
    time_uniform_family_wise_false_decisive_upper_bound: float
    stopping_time_false_decisive_upper_bound: float
    false_invariant_upper_bounds: Mapping[str, float]
    false_excluded_upper_bounds: Mapping[str, float]
    required_cell_ids: tuple[str, ...]
    certified_looks: tuple[int, ...] | None
    certificate_method: str
    certificate_assumptions: tuple[str, ...]


def _required_cell_ids(snapshot: SequentialConfidenceSetSnapshot) -> tuple[str, ...]:
    return tuple(cell.cell_id for cell in snapshot.cells if cell.required)


def _validate_snapshots(
    universe: CandidateMotifUniverse,
    snapshots: Iterable[SequentialConfidenceSetSnapshot],
    *,
    expected_required_cell_ids: tuple[str, ...] | None = None,
    certificate: AnytimeJointCoverageCertificate | None = None,
) -> tuple[SequentialConfidenceSetSnapshot, ...]:
    snapshot_tuple = tuple(snapshots)
    if not snapshot_tuple:
        raise ValueError("at least one sequential snapshot is required")
    looks = tuple(snapshot.look for snapshot in snapshot_tuple)
    if len(set(looks)) != len(looks):
        raise ValueError("sequential look indices must be unique")
    if looks != tuple(sorted(looks)):
        raise ValueError("sequential snapshots must be sorted by increasing look")

    first_required = _required_cell_ids(snapshot_tuple[0])
    if not first_required:
        raise ValueError("each snapshot must contain at least one required cell")
    expected = expected_required_cell_ids or first_required
    expected_set = set(expected)
    if not expected_set:
        raise ValueError("expected required cell IDs must not be empty")

    for snapshot in snapshot_tuple:
        # This validates cell IDs, required-cell existence, and candidate IDs in
        # acceptance sets through the non-sequential RACH interface.
        classify_confidence_sets(universe, snapshot.cells)
        observed_required = _required_cell_ids(snapshot)
        if set(observed_required) != expected_set:
            raise ValueError(
                "every sequential snapshot must use exactly the same required cell IDs"
            )
        if certificate is not None and not certificate.covers_look(snapshot.look):
            raise ValueError(
                f"look {snapshot.look} is outside the certificate's declared coverage scope"
            )
    return snapshot_tuple


def deterministic_anytime_lifting_witness(
    universe: CandidateMotifUniverse,
    snapshots: Iterable[SequentialConfidenceSetSnapshot],
    *,
    true_candidate_id: str,
    certificate: AnytimeJointCoverageCertificate | None = None,
) -> AnytimeLiftingWitness:
    """Check the pointwise theorem relation across all realized sequential looks.

    At every look, the ordinary confidence-set lifting implication says that a
    false decisive RACH conclusion requires omission of the true candidate from
    at least one required retained set. Taking the union over looks gives the
    anytime implication:

    ``any false decisive conclusion at any look``
    is a subset of
    ``failure of joint true-candidate retention at some certified look``.

    The statement is deterministic for a realized sequence of retained sets.
    Probability enters only through an external `AnytimeJointCoverageCertificate`.
    """

    if true_candidate_id not in universe.candidate_ids:
        raise ValueError("true_candidate_id must belong to the candidate universe")
    if certificate is not None:
        if certificate.true_candidate_id != true_candidate_id:
            raise ValueError("certificate and requested true_candidate_id must agree")
        expected = certificate.required_cell_ids
    else:
        expected = None
    snapshot_tuple = _validate_snapshots(
        universe,
        snapshots,
        expected_required_cell_ids=expected,
        certificate=certificate,
    )

    retention: dict[int, bool] = {}
    errors: dict[int, tuple[str, ...]] = {}
    for snapshot in snapshot_tuple:
        report = classify_confidence_sets(universe, snapshot.cells)
        retention[snapshot.look] = joint_coverage_event(true_candidate_id, snapshot.cells)
        errors[snapshot.look] = false_decisive_motifs(
            universe,
            report,
            true_candidate_id=true_candidate_id,
        )
    witness = AnytimeLiftingWitness(
        true_candidate_id=true_candidate_id,
        joint_retention_by_look=retention,
        false_decisive_motifs_by_look=errors,
    )
    if not witness.implication_holds:
        raise RuntimeError("anytime confidence-set lifting implication was violated")
    return witness


def anytime_soundness_guarantee_from_coverage(
    universe: CandidateMotifUniverse,
    certificate: AnytimeJointCoverageCertificate,
) -> AnytimeRACHSoundnessGuarantee:
    """Lift a time-uniform coverage certificate into optional-stopping-safe RACH control.

    **Anytime confidence-set lifting theorem.** Let `C_{r,t}(Z,U)` be arbitrary
    possibly randomized candidate sets, indexed by required cell `r` and look
    `t` in a certified scope `T`. Let `theta` be the true candidate. If

    ``P(for every t in T, theta in intersection_r C_{r,t}(Z,U)) >= 1 - alpha``,

    then

    ``P(exists t in T, any false RACH INVARIANT or EXCLUDED conclusion at t) <= alpha``.

    Consequently, for any data-dependent stopping time `tau` taking values in
    `T`,

    ``P(false decisive RACH conclusion at tau) <= alpha``.

    The proof is set inclusion: a false decisive conclusion at one look requires
    joint retention to fail at that same look. No stochastic assumptions are
    added by RACH; the external procedure must justify the time-uniform coverage
    statement over its declared data-generating class.
    """

    if certificate.true_candidate_id not in universe.candidate_ids:
        raise ValueError("certificate true candidate must belong to the candidate universe")
    alpha = certificate.miscoverage_upper_bound
    true_motifs = universe.active_motifs(certificate.true_candidate_id)
    false_invariant = {
        motif: 0.0 if motif in true_motifs else alpha
        for motif in universe.motifs
    }
    false_excluded = {
        motif: alpha if motif in true_motifs else 0.0
        for motif in universe.motifs
    }
    return AnytimeRACHSoundnessGuarantee(
        true_candidate_id=certificate.true_candidate_id,
        joint_time_uniform_coverage_lower_bound=certificate.lower_bound,
        time_uniform_family_wise_false_decisive_upper_bound=alpha,
        stopping_time_false_decisive_upper_bound=alpha,
        false_invariant_upper_bounds=false_invariant,
        false_excluded_upper_bounds=false_excluded,
        required_cell_ids=certificate.required_cell_ids,
        certified_looks=certificate.certified_looks,
        certificate_method=certificate.method,
        certificate_assumptions=certificate.assumptions,
    )
