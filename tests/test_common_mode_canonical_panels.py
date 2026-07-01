import pytest

from causal_model.common_mode_canonical_panels import (
    analyze_common_mode_panel,
    build_failure_mode_family,
    certify_common_mode_ambiguity,
    certify_common_mode_collapse,
    certify_common_mode_robustness,
    certify_mode_cover,
    certify_mode_disjoint_packing,
    certify_singleton_mode_reduction,
    certify_site_bundle_resilience,
    replicated_two_class_response_table,
    site_bundle_mode_family,
)
from causal_model.robust_canonical_panels import (
    analyze_canonical_panel,
    build_canonical_separation_hypergraph,
    private_bundle_response_table,
)


def test_singleton_modes_reduce_exactly_to_independent_cell_loss():
    system = replicated_two_class_response_table(4)
    hypergraph = build_canonical_separation_hypergraph(system, system.words)
    profile = analyze_canonical_panel(hypergraph, hypergraph.full_cells)
    reduction = certify_singleton_mode_reduction(profile)
    assert reduction.verify()
    assert profile.loss_tolerance == 3
    assert reduction.common_mode_profile.mode_tolerance == 3
    assert reduction.common_mode_profile.cover_for((0, 1)).mode_cover_number == 4


def test_many_replicates_in_one_common_mode_have_zero_one_mode_resilience():
    certificate = certify_common_mode_collapse(5)
    assert certificate.verify()
    assert certificate.independent_profile.loss_tolerance == 4
    assert certificate.common_profile.mode_tolerance == 0
    assert certificate.one_mode_failure.ambiguous_pair == (0, 1)
    assert certificate.one_mode_failure.removed_mode_indices == (0,)
    assert len(certificate.one_mode_failure.removed_cells) == 5


@pytest.mark.parametrize(
    "site_count,replicates_per_site",
    [(1, 5), (2, 1), (2, 4), (4, 3)],
)
def test_site_bundles_make_common_mode_tolerance_depend_on_sites_not_raw_replicates(
    site_count,
    replicates_per_site,
):
    certificate = certify_site_bundle_resilience(site_count, replicates_per_site)
    assert certificate.verify()
    assert certificate.independent_profile.loss_tolerance == site_count * replicates_per_site - 1
    assert certificate.common_profile.mode_tolerance == site_count - 1


def test_site_bundle_survives_one_site_failure_only_when_at_least_two_sites_exist():
    one_site_profile, one_site_family = site_bundle_mode_family(1, 3)
    two_site_profile, two_site_family = site_bundle_mode_family(2, 3)
    assert one_site_profile.loss_tolerance == 2
    assert analyze_common_mode_panel(one_site_family).mode_tolerance == 0
    with pytest.raises(ValueError, match="does not remain exact"):
        certify_common_mode_robustness(one_site_family, 1)
    assert certify_common_mode_robustness(two_site_family, 1).verify()


def test_mode_cover_certificate_finds_minimum_site_cover_for_all_selected_separators():
    _, family = site_bundle_mode_family(3, 2)
    cover = certify_mode_cover(family, (0, 1))
    assert cover.verify()
    assert cover.selected_separators == family.profile.panel
    assert cover.mode_cover_number == 3
    assert cover.cover_mode_indices == (0, 1, 2)


def test_constructive_common_mode_failure_returns_modes_cells_and_ambiguous_pair():
    _, family = site_bundle_mode_family(2, 2)
    profile = analyze_common_mode_panel(family)
    failure = certify_common_mode_ambiguity(profile, 2)
    assert failure.verify()
    assert failure.ambiguous_pair == (0, 1)
    assert failure.removed_mode_indices == (0, 1)
    assert failure.removed_cells == family.profile.panel
    assert failure.retained_panel == ()


def test_mode_disjoint_packing_recovers_mode_diversity_lower_bound_for_private_bundles():
    system = private_bundle_response_table(2)
    hypergraph = build_canonical_separation_hypergraph(system, system.words)
    profile = analyze_canonical_panel(hypergraph, hypergraph.full_cells)
    singleton_modes = tuple((cell,) for cell in profile.panel)
    family = build_failure_mode_family(profile, singleton_modes)
    packing = certify_mode_disjoint_packing(family, 1, ((0, 1), (0, 2), (2, 3)))
    assert packing.verify()
    assert packing.required_mode_diversity_lower_bound == 6
    assert sum(len(support) for _, support in packing.mode_supports) == 6


def test_overlapping_mode_supports_cannot_be_used_as_mode_disjoint_packing():
    system = private_bundle_response_table(1)
    hypergraph = build_canonical_separation_hypergraph(system, system.words)
    profile = analyze_canonical_panel(hypergraph, hypergraph.full_cells)
    family = build_failure_mode_family(profile, tuple((cell,) for cell in profile.panel))
    with pytest.raises(ValueError, match="mode-disjoint"):
        certify_mode_disjoint_packing(family, 0, ((0, 1), (1, 2)))


def test_mode_contract_fails_closed_when_a_panel_cell_has_no_declared_failure_domain():
    _, family = site_bundle_mode_family(2, 2)
    profile = family.profile
    with pytest.raises(ValueError, match="every declared panel cell"):
        build_failure_mode_family(profile, (profile.panel[:2],))


def test_modes_must_be_nonempty_distinct_and_panel_internal():
    _, family = site_bundle_mode_family(2, 1)
    profile = family.profile
    with pytest.raises(ValueError, match="nonempty"):
        build_failure_mode_family(profile, ((), profile.panel))
    with pytest.raises(ValueError, match="distinct"):
        build_failure_mode_family(profile, (profile.panel, profile.panel))
    with pytest.raises(ValueError, match="outside"):
        build_failure_mode_family(profile, (((0, "not-a-word"),), profile.panel))


def test_invalid_mode_budgets_fail_closed():
    _, family = site_bundle_mode_family(2, 1)
    with pytest.raises(ValueError, match="non-negative"):
        certify_common_mode_robustness(family, -1)
