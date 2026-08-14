# RACH/CCOC package boundary — publication core, explicit extensions, compatibility shelf

## Governing decision

CCOC now contains a mature first-paper core plus several established extension packages. The repository should therefore distinguish **publication dependency**, **active extension surfaces**, and **compatibility/legacy code** instead of treating everything outside CORE-1--CORE-5 as one undifferentiated archive.

The first-paper question remains:

> When can exact finite compression that is valid under a declared closed future fail to provide one comparably small exact interface after the legal future grammar is opened?

The first-paper proof dependency graph stays narrow. Later converse/resource/ecological/stochastic/spatial theorems are real results, but they should not enlarge that graph automatically.

## 1. First-paper publication core

Preferred historical entrance:

```python
import causal_model.portability_core as rach
```

The July registry anchors remain `CORE-1`--`CORE-5`. The first-paper proof spine is:

1. exact grammar-aware response interface;
2. extension--compression/addressability obstruction;
3. bounded-local relay sharpness;
4. conservative macro-schema portability;
5. local future-word/new-action fiber split.

The strengthened extremal handoff additionally uses:

```text
causal_model/fixed_regular_grammar_relay.py
causal_model/extremal_open_composition.py
docs/fixed_regular_extremal_theorem_2026-08-13.md
```

These strengthen the relay role without replacing the historical registry IDs.

## 2. Established extension surfaces

The following are **not legacy merely because they are outside the first-paper core**. They are explicit theorem families for follow-up work:

- exact converse/reuse: `action_grammar_closure.py`, `grammar_expansion_closure.py`, `grammar_interface_reuse.py`;
- chain/resource portability: `terminal_grammar_portability.py`, `portability_adaptation_tradeoff.py` and the boundary-time/staged-prefix proofs;
- deterministic ecology: `ecological_saturation_blanket.py`, `ecological_capacity_portability.py`, `budgeted_depletion_blanket.py`;
- stochastic ecology: `stochastic_ecological_portability.py`, `continuous_time_depletion_reach.py`, `per_capita_mortality_reach.py`, `finite_horizon_stochastic_saturation.py`;
- interaction/spatial ecology: `cross_guild_stochastic_coupling.py`, `spatial_dispersal_reachability.py`.

These modules should be imported explicitly. They should not be bulk-added to `portability_core` just to make them easier to discover.

## 3. Compatibility surfaces

`causal_model.current_theory` remains a deprecated pre-v1 aggregate. It exists only so old certificates/notebooks continue to import. It is not a research entrance.

The package root `causal_model/__init__.py` also still exposes the older qualitative/ecological-program and robustness API. Repository examples and verification scripts continue to import those names directly from `causal_model`, so removing that facade now would be an import-breaking cleanup rather than deletion of dead code.

Policy:

- preserve these imports until a tagged manuscript/source release or an explicit major-version migration;
- do not add new theorem work to either broad facade;
- new CCOC theorem code imports explicit modules or `portability_core` where appropriate.

## 4. Legacy shelf

Historical candidate-uncertainty, observation-panel, benchmark, and experimental-design branches remain compatibility/reproducibility material. Their source paths may be moved only after the manuscript source pin is immutable and replayable.

Physical deletion or relocation is deferred because old examples/scripts still depend on those paths. A green full test suite is necessary but not sufficient evidence that external historical imports are safe to break.

## 5. Workflow boundary

The repository should have one generic full-suite Python matrix workflow. `tests.yml` is the canonical generic gate because it installs the package, compiles `causal_model`, and runs full pytest on Python 3.10/3.11/3.12.

The former `ci.yml` duplicated the same three-version full pytest matrix without adding a distinct scientific gate and is therefore removable.

Specialized historical workflows may remain only when they provide a named replay/certificate gate not already represented by generic full pytest or theorem-registry integrity. Their removal should be evaluated separately, not by filename age alone.

## 6. Source-of-truth rules

- `extension_compression_noncommutation.py` is the canonical source for the addressable-product/noncommutation obstruction.
- `operational_addressability.py` supplies finite operational witnesses; it does not infer a grammar or ecological mechanism from data.
- `fixed_regular_grammar_relay.py` + `extremal_open_composition.py` are the current strongest explicit relay realization surface.
- `conservative_macro_schema.py` supplies the manuscript positive boundary.
- `grammar_interface_reuse.py` is the broad same-domain reuse theorem; do not replace it with an unconditional refinement slogan.
- ecological/stochastic/spatial modules remain explicit follow-up theorem surfaces rather than manuscript-core dependencies.

## 7. Cleanup rule

Classify repository material into three buckets before deleting anything:

1. **KEEP** — publication core, established extension theorem, required replay/provenance, or compatibility surface still referenced in-repo;
2. **REMOVE NOW** — exact duplicate infrastructure with no distinct scientific/replay role;
3. **DEFER** — old APIs/workflows/examples whose removal would break compatibility or whose replay role has not yet been replaced by an immutable manuscript pin.

The current cleanup manifest is `docs/core_surface_cleanup_manifest_2026-08-14.md`.
