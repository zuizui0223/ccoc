"""CCOC package.

The publication-core API is intentionally explicit:

    import causal_model.portability_core as rach

The package root does not re-export historical evidence, candidate, panel, or
companion-theory APIs.  Those surfaces are preserved in Git history and routed by
CREST to their owning companion repositories.
"""

__all__: tuple[str, ...] = ()
