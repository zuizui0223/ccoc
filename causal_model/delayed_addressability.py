"""Compatibility shim for historical delayed-addressability imports.

The delayed-addressability / finite-evidence theorem family is historical and is
archived at the repository recovery pin recorded in
``docs/historical_theorem_archive.json``.

Current publication-core modules still import the generic finite grammar types
from this former module path. Their canonical implementation now lives in
``causal_model.shared_grammar``. Keep this shim only until those imports are
migrated; do not add theorem logic here.
"""

from .shared_grammar import (
    FinitePrefixGrammar,
    GrammarAwareControlledSystem,
    GrammarHorizonStabilizationCertificate,
    certify_grammar_horizon_stabilization,
)

WAIT = "wait"
FIRE = "fire"

__all__ = [
    "WAIT",
    "FIRE",
    "FinitePrefixGrammar",
    "GrammarAwareControlledSystem",
    "GrammarHorizonStabilizationCertificate",
    "certify_grammar_horizon_stabilization",
]
