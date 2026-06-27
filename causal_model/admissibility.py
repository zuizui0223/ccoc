"""Generic robust-admissibility classification across analysis cells.

A robustness cell is a fully declared analysis context: for example a prior,
tolerance, sampling plan, or endpoint rule. Each cell supplies sampled program
runs and an acceptance indicator determined outside this module.

For a motif m and nonempty cell c, write A_c for the accepted runs in c.

    invariant in c  <=>  m is active in every r in A_c
    excluded in c   <=>  m is inactive in every r in A_c

A motif is globally invariant or excluded only when the respective relation holds
in *every required nonempty cell*. If a required cell has no accepted runs, the
universal conclusion is unsupported rather than silently based on the remaining
cells.

These are bookkeeping and finite-sample classifications. They are conditional on
the declared program grammar, parameter domain, observation encoding, acceptance
rule, and selected robustness cells. They do not identify a causal mechanism in
nature by themselves.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Mapping


class MotifStatus(str, Enum):
    """Robust classification for one candidate motif."""

    INVARIANT = "invariant"
    EXCLUDED = "excluded"
    UNRESOLVED = "unresolved"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True)
class ProgramRun:
    """One sampled qualitative program evaluation.

    ``active_motifs`` must name only motifs in the declared grammar. Acceptance is
    stored explicitly so the classifier does not conflate a simulation result with
    an acceptance decision.
    """

    run_id: str
    cell_id: str
    active_motifs: frozenset[str]
    accepted: bool


@dataclass(frozen=True)
class RobustnessCell:
    """One required analysis context and its evaluated program runs."""

    cell_id: str
    description: str
    runs: tuple[ProgramRun, ...]
    required: bool = True

    def __post_init__(self) -> None:
        if not self.cell_id:
            raise ValueError("cell_id must be non-empty")
        for run in self.runs:
            if run.cell_id != self.cell_id:
                raise ValueError("every run in a cell must carry that cell_id")

    @property
    def accepted_runs(self) -> tuple[ProgramRun, ...]:
        return tuple(run for run in self.runs if run.accepted)


@dataclass(frozen=True)
class MotifClassification:
    """Classification plus evidence counts across required robustness cells."""

    motif: str
    status: MotifStatus
    accepted_run_count: int
    active_accepted_count: int
    inactive_accepted_count: int
    empty_required_cells: tuple[str, ...]
    cell_statuses: Mapping[str, MotifStatus]

    @property
    def active_fraction(self) -> float | None:
        if self.accepted_run_count == 0:
            return None
        return self.active_accepted_count / self.accepted_run_count


@dataclass(frozen=True)
class AdmissibilityReport:
    """Cross-cell robust-admissibility output for a declared motif vocabulary."""

    motifs: tuple[str, ...]
    classifications: Mapping[str, MotifClassification]
    required_cells: tuple[str, ...]
    empty_required_cells: tuple[str, ...]

    def by_status(self, status: MotifStatus) -> tuple[str, ...]:
        return tuple(
            motif
            for motif in self.motifs
            if self.classifications[motif].status is status
        )


def _check_inputs(motifs: Iterable[str], cells: Iterable[RobustnessCell]) -> tuple[tuple[str, ...], tuple[RobustnessCell, ...]]:
    motif_tuple = tuple(motifs)
    if not motif_tuple:
        raise ValueError("at least one declared motif is required")
    if len(set(motif_tuple)) != len(motif_tuple):
        raise ValueError("declared motifs must be unique")
    if any(not motif for motif in motif_tuple):
        raise ValueError("motif names must be non-empty")

    cell_tuple = tuple(cells)
    if not cell_tuple:
        raise ValueError("at least one robustness cell is required")
    ids = [cell.cell_id for cell in cell_tuple]
    if len(set(ids)) != len(ids):
        raise ValueError("robustness cell IDs must be unique")

    vocabulary = set(motif_tuple)
    for cell in cell_tuple:
        for run in cell.runs:
            unknown = set(run.active_motifs) - vocabulary
            if unknown:
                raise ValueError(
                    f"run {run.run_id!r} in cell {cell.cell_id!r} contains unknown motifs: {sorted(unknown)}"
                )
    return motif_tuple, cell_tuple


def _status_in_cell(motif: str, cell: RobustnessCell) -> MotifStatus:
    accepted = cell.accepted_runs
    if not accepted:
        return MotifStatus.UNSUPPORTED
    n_active = sum(motif in run.active_motifs for run in accepted)
    if n_active == len(accepted):
        return MotifStatus.INVARIANT
    if n_active == 0:
        return MotifStatus.EXCLUDED
    return MotifStatus.UNRESOLVED


def classify_motifs(
    motifs: Iterable[str],
    cells: Iterable[RobustnessCell],
) -> AdmissibilityReport:
    """Classify motifs across required robustness cells.

    Optional cells are reported per-cell but never block a universal conclusion.
    A required empty cell yields ``UNSUPPORTED`` for every motif because the
    requested robustness domain has not been covered by accepted programs.
    """
    motif_tuple, cell_tuple = _check_inputs(motifs, cells)
    required = tuple(cell for cell in cell_tuple if cell.required)
    empty_required = tuple(cell.cell_id for cell in required if not cell.accepted_runs)

    classifications: dict[str, MotifClassification] = {}
    for motif in motif_tuple:
        per_cell = {cell.cell_id: _status_in_cell(motif, cell) for cell in cell_tuple}
        accepted_runs = tuple(run for cell in required for run in cell.accepted_runs)
        active = sum(motif in run.active_motifs for run in accepted_runs)
        inactive = len(accepted_runs) - active

        if empty_required:
            overall = MotifStatus.UNSUPPORTED
        else:
            required_statuses = [per_cell[cell.cell_id] for cell in required]
            if all(status is MotifStatus.INVARIANT for status in required_statuses):
                overall = MotifStatus.INVARIANT
            elif all(status is MotifStatus.EXCLUDED for status in required_statuses):
                overall = MotifStatus.EXCLUDED
            else:
                overall = MotifStatus.UNRESOLVED

        classifications[motif] = MotifClassification(
            motif=motif,
            status=overall,
            accepted_run_count=len(accepted_runs),
            active_accepted_count=active,
            inactive_accepted_count=inactive,
            empty_required_cells=empty_required,
            cell_statuses=per_cell,
        )

    return AdmissibilityReport(
        motifs=motif_tuple,
        classifications=classifications,
        required_cells=tuple(cell.cell_id for cell in required),
        empty_required_cells=empty_required,
    )


def accepted_programs(cells: Iterable[RobustnessCell]) -> tuple[ProgramRun, ...]:
    """Flatten accepted runs while retaining their declared robustness-cell IDs."""
    return tuple(run for cell in cells for run in cell.accepted_runs)
