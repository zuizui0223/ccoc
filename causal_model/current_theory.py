"""Historical compatibility aggregate for pre-v1 RACH imports.

.. deprecated:: 0.1.0

   New theorem work must import either :mod:`portability_core` for the structural
   portability theorem family or :mod:`identifiability_companion` for finite
   evidence and retained-mechanism questions.

This module deliberately preserves a broad pre-v1 aggregate so old certificates,
replays, and notebooks remain importable. It is **not** a statement that its
exports form one theorem spine, and it must not be used as the research entrance.
The aggregate emits a :class:`DeprecationWarning` on import.
"""

from __future__ import annotations

import warnings
from types import ModuleType

from . import addressable_completion_bounds as _addressable_completion_bounds
from . import candidate_safe_laws as _candidate_safe_laws
from . import causal_closure_calculus as _causal_closure_calculus
from . import delayed_addressability as _delayed_addressability
from . import dynamic_boundary_blankets as _dynamic_boundary_blankets
from . import extension_compression as _extension_compression
from . import grammar_aware_blankets as _grammar_aware_blankets
from . import joint_open_candidate_laws as _joint_open_candidate_laws
from . import observation_regime_closure as _observation_regime_closure
from . import observation_window_completion as _observation_window_completion
from . import relay_tree_compilation as _relay_tree_compilation


_HISTORICAL_MODULES: tuple[ModuleType, ...] = (
    _addressable_completion_bounds,
    _candidate_safe_laws,
    _causal_closure_calculus,
    _delayed_addressability,
    _dynamic_boundary_blankets,
    _extension_compression,
    _grammar_aware_blankets,
    _joint_open_candidate_laws,
    _observation_regime_closure,
    _observation_window_completion,
    _relay_tree_compilation,
)


def _module_public_names(module: ModuleType) -> tuple[str, ...]:
    """Return names owned by a historical module without leaking its imports.

    Modules that explicitly declare ``__all__`` retain that declaration. For
    older modules, export classes, functions, and named constants defined in the
    module itself. This preserves the former aggregate's theorem-facing symbols
    while avoiding incidental imports such as ``dataclass`` or ``Iterable``.
    """
    declared = getattr(module, "__all__", None)
    if declared is not None:
        return tuple(declared)
    return tuple(
        name
        for name, value in vars(module).items()
        if not name.startswith("_")
        and (name.isupper() or getattr(value, "__module__", None) == module.__name__)
    )


__all__: tuple[str, ...] = tuple(
    dict.fromkeys(
        name
        for module in _HISTORICAL_MODULES
        for name in _module_public_names(module)
    )
)

for _module in _HISTORICAL_MODULES:
    for _name in _module_public_names(_module):
        globals()[_name] = getattr(_module, _name)

warnings.warn(
    "causal_model.current_theory is a historical compatibility aggregate; "
    "use causal_model.portability_core or causal_model.identifiability_companion for new work.",
    DeprecationWarning,
    stacklevel=2,
)

# Keep only the compatibility symbols visible to consumers.
del _module, _name
