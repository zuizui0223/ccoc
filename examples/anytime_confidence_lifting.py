"""Minimal sequential RACH example without raw data.

The external sequential method is represented only by retained candidate sets.
At look 1 both candidates remain, so the focal motif is unresolved. At look 2
only the inactive candidate remains, so the motif is correctly excluded under
the declared known truth. An external time-uniform coverage certificate, rather
than repeated fixed-time intervals, is what makes optional stopping sound.

Run:
    python examples/anytime_confidence_lifting.py
"""

from causal_model import (
    AnytimeJointCoverageCertificate,
    CandidateAcceptanceSet,
    CandidateMotifUniverse,
    ConfidenceSetCell,
    CoverageMode,
    SequentialConfidenceSetSnapshot,
    anytime_soundness_guarantee_from_coverage,
    deterministic_anytime_lifting_witness,
)


UNIVERSE = CandidateMotifUniverse(
    candidate_motifs={
        "active_focal": frozenset({"focal"}),
        "inactive_focal": frozenset(),
    },
    motifs=("focal",),
)


def snapshot(look: int, retained: frozenset[str]) -> SequentialConfidenceSetSnapshot:
    return SequentialConfidenceSetSnapshot(
        look=look,
        cells=(
            ConfidenceSetCell(
                cell_id="primary",
                acceptance_set=CandidateAcceptanceSet(retained),
                coverage_mode=CoverageMode.EXHAUSTIVE,
            ),
        ),
    )


def main() -> None:
    certificate = AnytimeJointCoverageCertificate(
        true_candidate_id="inactive_focal",
        required_cell_ids=("primary",),
        lower_bound=0.95,
        method="external anytime-valid candidate confidence sequence",
        assumptions=("simultaneous retention across every positive integer look",),
    )
    trajectory = (
        snapshot(1, frozenset({"active_focal", "inactive_focal"})),
        snapshot(2, frozenset({"inactive_focal"})),
    )
    witness = deterministic_anytime_lifting_witness(
        UNIVERSE,
        trajectory,
        true_candidate_id="inactive_focal",
        certificate=certificate,
    )
    guarantee = anytime_soundness_guarantee_from_coverage(UNIVERSE, certificate)

    print("joint retention at every shown look:", witness.joint_retention_at_all_looks)
    print("false-decisive looks:", witness.false_decisive_looks)
    print(
        "time-uniform false-decisive upper bound:",
        guarantee.time_uniform_family_wise_false_decisive_upper_bound,
    )
    print(
        "stopping-time false-decisive upper bound:",
        guarantee.stopping_time_false_decisive_upper_bound,
    )


if __name__ == "__main__":
    main()
