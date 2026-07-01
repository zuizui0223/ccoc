import pytest

from causal_model.canonical_boundary_blankets import redundant_exterior_response_table
from causal_model.robust_canonical_panels import (
    analyze_canonical_panel,
    build_canonical_separation_hypergraph,
    certify_disjoint_separation_packing,
    certify_dropout_ambiguity,
    certify_optimal_robust_panel,
    certify_private_bundle_optimality,
    certify_robust_canonical_panel,
    private_bundle_response_table,
)


def test_canonical_hypergraph_has_exact_pairwise_separation_sets():
    system = redundant_exterior_response_table()
    hypergraph = build_canonical_separation_hypergraph(system, ("observe", "read"))
    assert hypergraph.verify()
    assert hypergraph.class_count == 2
    assert hypergraph.pairs == ((0, 1),)
    assert hypergraph.separation_set((0, 1)) == ((0, "read"), (1, "read"))


def test_exact_panel_is_precisely_a_transversal_of_every_pairwise_separation_set():
    system = redundant_exterior_response_table()
    hypergraph = build_canonical_separation_hypergraph(system, ("observe", "read"))
    profile = analyze_canonical_panel(hypergraph, ((0, "read"),))
    assert profile.verify()
    assert profile.is_exact
    assert profile.loss_tolerance == 0
    assert profile.count_for((0, 1)) == 1
    certificate = certify_robust_canonical_panel(hypergraph, ((0, "read"),), loss_budget=0)
    assert certificate.verify()


def test_missing_all_separators_makes_even_zero_loss_exactness_fail():
    system = redundant_exterior_response_table()
    hypergraph = build_canonical_separation_hypergraph(system, ("observe", "read"))
    profile = analyze_canonical_panel(hypergraph, ((0, "observe"), (1, "observe")))
    assert profile.verify()
    assert not profile.is_exact
    assert profile.loss_tolerance == -1
    with pytest.raises(ValueError, match="does not distinguish"):
        certify_robust_canonical_panel(hypergraph, profile.panel, loss_budget=0)
    dropout = certify_dropout_ambiguity(profile, loss_budget=0)
    assert dropout.verify()
    assert dropout.ambiguous_pair == (0, 1)
    assert dropout.removed_cells == ()


def test_two_independent_separators_survive_one_cell_loss():
    system = redundant_exterior_response_table()
    hypergraph = build_canonical_separation_hypergraph(system, ("observe", "read"))
    panel = ((0, "read"), (1, "read"))
    robust = certify_robust_canonical_panel(hypergraph, panel, loss_budget=1)
    assert robust.verify()
    assert robust.profile.loss_tolerance == 1
    with pytest.raises(ValueError, match="does not distinguish"):
        certify_robust_canonical_panel(hypergraph, ((0, "read"),), loss_budget=1)


def test_constructive_dropout_certificate_names_the_ambiguous_pair_and_removed_cells():
    system = redundant_exterior_response_table()
    hypergraph = build_canonical_separation_hypergraph(system, ("observe", "read"))
    profile = analyze_canonical_panel(hypergraph, ((0, "read"),))
    dropout = certify_dropout_ambiguity(profile, loss_budget=1)
    assert dropout.verify()
    assert dropout.ambiguous_pair == (0, 1)
    assert dropout.removed_cells == ((0, "read"),)
    assert dropout.retained_panel == ()


@pytest.mark.parametrize("replication", [1, 2, 3, 5])
def test_private_bundle_has_closed_form_optimal_robust_panel(replication):
    certificate = certify_private_bundle_optimality(replication)
    assert certificate.verify()
    assert certificate.robust_panel.loss_budget == replication - 1
    assert certificate.optimality.panel_size == 3 * replication
    assert certificate.optimality.optimum_size == 3 * replication
    assert certificate.packing.lower_bound == 3 * replication


def test_private_bundle_disjoint_packing_is_a_real_lower_bound_not_enumeration():
    system = private_bundle_response_table(2)
    hypergraph = build_canonical_separation_hypergraph(system, system.words)
    packing = certify_disjoint_separation_packing(hypergraph, 1, ((0, 1), (0, 2), (2, 3)))
    robust = certify_robust_canonical_panel(hypergraph, hypergraph.full_cells, 1)
    optimality = certify_optimal_robust_panel(robust, packing)
    assert packing.verify()
    assert packing.lower_bound == 6
    assert optimality.verify()
    assert optimality.panel_size == 6


def test_private_bundle_panel_loses_robustness_exactly_when_loss_budget_reaches_replication():
    system = private_bundle_response_table(2)
    hypergraph = build_canonical_separation_hypergraph(system, system.words)
    profile = analyze_canonical_panel(hypergraph, hypergraph.full_cells)
    assert profile.loss_tolerance == 1
    dropout = certify_dropout_ambiguity(profile, loss_budget=2)
    assert dropout.verify()
    assert len(dropout.removed_cells) == 2
    assert dropout.ambiguous_pair in ((0, 1), (0, 2), (2, 3))


def test_non_disjoint_pair_collection_cannot_be_used_as_a_packing_lower_bound():
    system = private_bundle_response_table(1)
    hypergraph = build_canonical_separation_hypergraph(system, system.words)
    # (0,1) is separated only by the left bundle; (1,2) also uses that bundle.
    with pytest.raises(ValueError, match="not a nonempty disjoint"):
        certify_disjoint_separation_packing(hypergraph, 0, ((0, 1), (1, 2)))


def test_invalid_cells_loss_budgets_and_trivial_blankets_fail_closed():
    system = redundant_exterior_response_table()
    hypergraph = build_canonical_separation_hypergraph(system, ("observe", "read"))
    with pytest.raises(ValueError, match="declared grammar"):
        analyze_canonical_panel(hypergraph, ((0, "unknown"),))
    with pytest.raises(ValueError, match="non-negative"):
        certify_robust_canonical_panel(hypergraph, ((0, "read"),), loss_budget=-1)

    # A one-class exterior has no pairwise separation problem; the theorem does
    # not pretend that it has a meaningful finite loss-tolerance bottleneck.
    from causal_model.canonical_boundary_blankets import FiniteBoundaryResponseTable

    one_class = FiniteBoundaryResponseTable(
        inside_count=1,
        exterior_count=1,
        words=("x",),
        responses=(((0,),),),
    )
    with pytest.raises(ValueError, match="at least two"):
        build_canonical_separation_hypergraph(one_class, ("x",))
