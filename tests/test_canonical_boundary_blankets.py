import pytest

from causal_model.canonical_boundary_blankets import (
    FiniteBoundaryResponseTable,
    binary_addressable_ladder,
    certify_addressable_ladder,
    certify_boundary_summary_factor,
    certify_canonical_boundary_blanket,
    certify_finite_grammar_chain,
    certify_joint_observability,
    redundant_exterior_response_table,
)


def test_redundant_raw_exterior_collapses_to_two_canonical_response_types():
    system = redundant_exterior_response_table()
    certificate = certify_canonical_boundary_blanket(system, ("observe", "read"))
    assert certificate.verify()
    assert certificate.canonical_labels == (0, 0, 1, 1)
    assert certificate.blanket_block_count == 2
    assert certificate.joint_interface_block_count == 4
    assert certificate.equality_holds
    assert certificate.boundary_bits == 1.0
    assert certificate.interface_upper_bound_bits == 2.0
    assert certificate.realized_interface_bits == 2.0


def test_canonical_summary_is_strictly_smaller_than_raw_exterior_identity_summary():
    system = redundant_exterior_response_table()
    raw = certify_boundary_summary_factor(system, ("observe", "read"), (0, 1, 2, 3))
    canonical = certify_boundary_summary_factor(system, ("observe", "read"), (0, 0, 1, 1))
    assert raw.verify() and canonical.verify()
    assert raw.summary_image_count == 4
    assert raw.canonical_block_count == 2
    assert not raw.is_minimal
    assert canonical.summary_image_count == 2
    assert canonical.canonical_block_count == 2
    assert canonical.is_minimal
    assert canonical.quotient_factor == (0, 1)


def test_unsound_summary_that_merges_distinct_response_types_fails_closed():
    system = redundant_exterior_response_table()
    with pytest.raises(ValueError, match="not response-sound"):
        certify_boundary_summary_factor(system, ("observe", "read"), (0, 0, 0, 0))


def test_empty_grammar_has_one_exterior_blanket_class_and_no_joint_observability():
    system = redundant_exterior_response_table()
    certificate = certify_canonical_boundary_blanket(system, ())
    assert certificate.verify()
    assert certificate.blanket_block_count == 1
    assert certificate.joint_interface_block_count == 1
    assert not certificate.equality_holds
    observability = certify_joint_observability(system, ())
    assert observability.verify()
    assert not observability.is_joint_observable


def test_joint_observability_certificate_requires_all_inside_blanket_cells_to_separate():
    system = redundant_exterior_response_table()
    certificate = certify_joint_observability(system, ("observe", "read"))
    assert certificate.verify()
    assert certificate.is_joint_observable
    assert certificate.separating_cell_pairs == certificate.expected_pair_count


def test_finite_grammar_chain_refines_monotonically_and_stabilizes_after_last_new_word():
    system = redundant_exterior_response_table()
    chain = certify_finite_grammar_chain(
        system,
        ((), ("observe",), ("observe", "read"), ("observe", "read")),
    )
    assert chain.verify()
    assert chain.block_counts == (1, 1, 2, 2)
    assert chain.first_terminal_stable_level == 2


def test_non_nested_grammar_chain_is_rejected():
    system = redundant_exterior_response_table()
    with pytest.raises(AssertionError, match="certificate did not verify"):
        certify_finite_grammar_chain(system, (("observe",), ("read",)))


def test_binary_addressable_ladder_has_exact_exponential_blanket_growth():
    certificate = certify_addressable_ladder(4)
    assert certificate.verify()
    assert certificate.chain.block_counts == (1, 2, 4, 8, 16)
    assert certificate.chain.first_terminal_stable_level == 4


@pytest.mark.parametrize("bit_count", [1, 2, 3, 5])
def test_addressable_ladder_prefixes_match_the_number_of_readable_binary_coordinates(bit_count):
    system, levels = binary_addressable_ladder(bit_count)
    chain = certify_finite_grammar_chain(system, levels)
    assert chain.verify()
    assert chain.block_counts == tuple(2**k for k in range(bit_count + 1))


def test_response_table_rejects_bad_shapes_and_duplicate_words():
    with pytest.raises(ValueError, match="words must be unique"):
        FiniteBoundaryResponseTable(
            inside_count=1,
            exterior_count=1,
            words=("x", "x"),
            responses=(((0, 0),),),
        )
    with pytest.raises(ValueError, match="one row per exterior"):
        FiniteBoundaryResponseTable(
            inside_count=1,
            exterior_count=2,
            words=("x",),
            responses=(((0,),),),
        )


def test_grammar_validation_rejects_unknown_and_duplicate_words():
    system = redundant_exterior_response_table()
    with pytest.raises(ValueError, match="outside"):
        system.normalize_grammar(("unknown",))
    with pytest.raises(ValueError, match="unique"):
        system.normalize_grammar(("read", "read"))


def test_summary_label_length_and_type_fail_closed():
    system = redundant_exterior_response_table()
    with pytest.raises(ValueError, match="one label"):
        certify_boundary_summary_factor(system, ("read",), (0, 1))
    with pytest.raises(ValueError, match="non-negative"):
        certify_boundary_summary_factor(system, ("read",), (0, -1, 1, 1))
