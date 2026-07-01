# Current RACH architecture

## Purpose

RACH contains valid results with different questions. They are no longer
presented as one linear theorem chain. This document maps the current logical
packages, public import surfaces, certificates, and workflows.

Read [portability core v1](portability_core_v1.md) first, then
[research priorities](research_priorities.md).

## Public surfaces

### 1. Portability core

```python
import causal_model.portability_core as rach
```

This is the research entrance for the structural question:

\[
\text{When does an exact finite macro-law survive declared composition changes?}
\]

| Role | Modules |
|---|---|
| finite-model prerequisite | `causal_closure_calculus.py` |
| exact grammar-aware factorization | `dynamic_boundary_blankets.py`, `grammar_aware_blankets.py` |
| central lower bound | `extension_compression_noncommutation.py` |
| sharpness witness | `extension_compression.py`, `relay_tree_compilation.py` |
| portability ladder | `compositional_boundedness.py`, `coherent_portable_macrolaw.py`, `conservative_macro_schema.py` |

The dependency order is conceptual:

```text
finite closure prerequisite
        -> exact dynamic factorization
        -> addressability obstruction / lower bound
        -> boundedness -> coherent law -> conservative grammar extension
```

The final three arrows are a theorem ladder, not three independent research
programs. The relay tree is a witness that the lower bound survives constant
local grammar, pairwise interactions, and degree three; it is not a separate
headline theory.

### 2. Identifiability companion

```python
import causal_model.identifiability_companion as rach_id
```

This package asks a distinct question:

\[
\text{What can finite evidence or retained mechanism families justify?}
\]

| Role | Modules |
|---|---|
| delayed horizon and finite-adaptive evidence limits | `delayed_addressability.py`, `adaptive_closure_no_go.py` |
| candidate mechanism agreement | `candidate_safe_laws.py` |
| joint exterior–mechanism conditions | `joint_open_candidate_laws.py` |
| retained-family support | `admissibility.py`, confidence-lifting modules, `symbolic_candidate_sets.py` |

These results can conclude candidate-safe, set-valued, or `UNRESOLVED`. They do
not become premises of the structural portability theorem merely because they
also concern open systems.

### 3. Compatibility aggregate

```python
import causal_model.current_theory as historical
```

`current_theory.py` remains a broad backward-compatible aggregate for earlier
imports and regressions. It is **not** the research entrance for new theorem
work. New code should import one of the two facades above or an explicit
lower-level module.

### 4. Experimental-design legacy shelf

Reset panels, witnessed evidence, panel robustness, common-mode failure, and
observation-regime special cases remain executable in their original modules.
They are not public theorem surfaces because they begin after a quotient, reset,
coverage, or failure contract has been selected. See [legacy/README.md](legacy/README.md).

## Certificate and workflow discipline

Every existing theorem module retains its own finite certificate objects and
replay workflow. A workflow replays a declared finite domain; it does not prove
claims about arbitrary ecosystems outside that domain.

A new structural theorem may be added only after the v1 freeze is lifted and it
changes one canonical claim in the portability core or a deliberately selected
identifiability direction. It must include:

1. exact finite domain and grammar;
2. statement status: theorem, sufficient criterion, lower bound, witness, or
   unresolved boundary;
3. independently checkable certificate;
4. fail-closed and counterexample tests; and
5. deterministic replay artifact.

## Shared infrastructure

`causal_model.__init__` stays broad for compatibility. Manifests, transcripts,
signatures, checkpoints, and artifact registries preserve provenance only. They
must remain stable but do not determine closure, portability, or universal
mechanism laws.

## Navigation

- [Portability core v1](portability_core_v1.md)
- [Research priorities](research_priorities.md)
- [Theorem map](theorem_spine.md)
- [Asset map](repository_asset_map.md)
- [Legacy shelf](legacy/README.md)