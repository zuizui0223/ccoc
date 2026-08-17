# Current CCOC architecture — 2026-08-17

## 1. Publication core

The current executable spine is:

1. exact grammar-aware response interfaces;
2. cross-grammar addressability / extension-compression lower bound;
3. bounded-local sharpness realization;
4. conservative positive boundary;
5. local future-word/new-action obstruction.

Canonical modules:

- `dynamic_boundary_blankets.py`
- `shared_grammar.py`
- `grammar_aware_blankets.py`
- `extension_compression.py`
- `extension_compression_noncommutation.py`
- `operational_addressability.py`
- `relay_tree_compilation.py`
- `constant_alphabet_relay.py`
- `fixed_regular_grammar_relay.py`
- `extremal_open_composition.py`
- `local_causal_cone.py`
- `coherent_portable_macrolaw.py`
- `conservative_macro_schema.py`
- `portability_core.py`

## 2. Retained quantitative strengthening

### Constrained codebooks

`addressable_codebooks.py` and `codebook_families.py` weaken the full-product premise: jointly realizable states may obey parity, fixed-richness, or other constraints while open addressability still forces a large exact interface. `docs/composition_code_rate.md` records the corresponding correlated-composition interpretation.

### Approximate addressability

`approximate_addressability.py` changes the model premise from exact coordinate recovery to bounded decoding error. It is retained as a stronger-model extension, while explicitly conceding that the Fano/information machinery itself is classical.

## 3. Historicalized internal side branches

The following formerly active branches are valid but no longer justify current executable surfaces:

- exact converse/reuse and terminal-grammar variants;
- generic canonical exterior quotient / boundary blanket constructions;
- duplicate addressable-product wrappers;
- interface-inflation and union-refinement decompositions;
- single-action and absolute-capacity/resource corollaries already subsumed by the fixed-regular extremal package;
- observation-window completion as an ecological corollary/witness of the same open-addressability mechanism;
- budget/depletion, continuous-time, mortality, capacity, saturation, stochastic, cross-guild, spatial, and adaptation-tradeoff special cases.

These results remain recoverable from pre-removal main commit `0d3424a9090b86eae4e369d3749bbe39b6b03432` and historical documentation where retained.

## 4. Compatibility

`delayed_addressability.py` remains temporarily as a tiny compatibility shim forwarding generic grammar types to current CORE-4 code. It contains no theorem logic. Remove it only after the remaining import is migrated directly to `shared_grammar.py`.

No other historical family is retained merely for hypothetical external imports.

## 5. Current provenance

Current reproducibility is theorem-registry integrity + paper-core replay + the surviving structural workflows + immutable Git history. Historical side-branch workflows and dedicated tests are removed with their source bundles.

## 6. Next action

After this structural-surface pass, stop broad deletion. The remaining active tree should be small enough for a final manuscript-core dependency audit and primary-source novelty gate rather than another theorem-development cycle.
