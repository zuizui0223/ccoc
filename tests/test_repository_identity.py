"""Regression tests for current-facing CCOC identity and scope."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_distribution_metadata_is_ccoc_facing():
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'name = "ccoc-causal-compression"' in text
    assert 'name = "rach-causal-invariants"' not in text


def test_readme_uses_ccoc_alias_for_current_api_example():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "import causal_model.portability_core as ccoc" in text
    assert "import causal_model.portability_core as rach" not in text


def test_nonempirical_scope_uses_current_ccoc_identity():
    text = (ROOT / "docs" / "nonempirical_scope.md").read_text(encoding="utf-8")
    assert "CCOC is a **theorem-first mathematical ecology** repository" in text
    for stale_current_identity in (
        "RACH is a **mathematical ecology** repository",
        "RACH theorem",
        "RACH certificate",
        "RACH result",
    ):
        assert stale_current_identity not in text


def test_program_positioning_keeps_representation_inference_boundary_explicit():
    text = (ROOT / "docs" / "program_positioning_2026-08-31.md").read_text(
        encoding="utf-8"
    )
    assert "CCOC is a **representation theory" in text
    assert "RACH asks what we still do not know" in text
    assert "N1" in text
    assert "Historical recovery documents may retain" in text
