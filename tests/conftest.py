"""Pytest collection policy for the manuscript-focused repository surface.

Only the tests that exercise the publication theorem package are unmarked. Every
other historical test is retained as ``legacy`` until the post-submission physical
move. This allowlist avoids silently treating old benchmarks or development-era
checks as paper-core evidence merely because their filename lacks a legacy token.

Run ``pytest -m legacy`` to replay the archived material explicitly.
"""

from __future__ import annotations

from pathlib import Path

import pytest


ACTIVE_PAPER_TEST_FILES = frozenset(
    {
        # CORE-1: exact grammar-aware interface.
        "test_dynamic_boundary_blankets.py",
        "test_shared_grammar.py",
        "test_grammar_aware_blankets.py",
        # CORE-2: operational addressability and noncommutation.
        "test_extension_compression.py",
        "test_operational_addressability.py",
        # CORE-3: bounded-locality sharpness.
        "test_relay_tree_compilation.py",
        # CORE-4 and CORE-5: conservative portability and fiber split.
        "test_coherent_portable_macrolaw.py",
        "test_conservative_macro_schema.py",
        # Publication-surface, identity, and provenance protections.
        "test_public_theory_surfaces.py",
        "test_repository_identity.py",
        "test_theorem_registry.py",
        "test_paper_core_reproducibility.py",
    }
)


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        filename = Path(str(item.fspath)).name
        if filename not in ACTIVE_PAPER_TEST_FILES:
            item.add_marker(pytest.mark.legacy)
