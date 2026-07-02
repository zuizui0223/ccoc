"""Pytest collection policy for the manuscript-focused repository surface.

The old theorem branches remain in ``tests/`` until the post-submission physical
move, but are not part of the default paper-core gate. Run ``pytest -m legacy``
to replay the archived material explicitly.
"""

from __future__ import annotations

from pathlib import Path

import pytest


# These names correspond to CORE-0, EXT-1--4, ID-1--3, the experimental-design
# shelf, and deprecated compatibility aggregates. The active paper suite remains
# unmarked and is selected by the default ``-m 'not legacy'`` configuration.
LEGACY_TEST_TOKENS = (
    "adaptive_closure",
    "candidate_safe",
    "causal_closure",
    "common_mode",
    "current_theory",
    "delayed_addressability",
    "delayed_joint",
    "generative_misspecification",
    "joint_open_candidate",
    "multi_competitor",
    "non_nested",
    "observation_envelope",
    "observation_regime",
    "observation_window",
    "robust_canonical",
    "witnessed_boundary",
)


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        filename = Path(str(item.fspath)).stem
        if any(token in filename for token in LEGACY_TEST_TOKENS):
            item.add_marker(pytest.mark.legacy)
