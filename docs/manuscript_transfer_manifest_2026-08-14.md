# Open-composition manuscript integration manifest — reduced surface

> Updated 2026-08-19: manuscript work is integrated inside CCOC. No separate repository is required.

## Editorial decision

The first CCOC paper uses only the theorem spine needed to answer one question:

> Why can exact compression valid in each declared closed future fail to provide one comparably small exact interface after the legal future grammar is opened?

The publication prose lives under `manuscript/`. The theorem implementation remains under `causal_model/`; manuscript prose references immutable Git provenance rather than copying theorem code.

## Publication-core dependencies

### Foundation

- `dynamic_boundary_blankets.py`
- `shared_grammar.py`
- `grammar_aware_blankets.py`
- `addressable_completion_bounds.py` — CORE-1 foundation dependency only

### Headline lower bound

- `extension_compression.py`
- `extension_compression_noncommutation.py`
- `operational_addressability.py`

### Sharpness / constrained realization

- `relay_tree_compilation.py`
- `constant_alphabet_relay.py`
- `fixed_regular_grammar_relay.py`
- `extremal_open_composition.py`
- `local_causal_cone.py`

### Positive/negative boundary

- `coherent_portable_macrolaw.py`
- `conservative_macro_schema.py`

## Supporting strengthening

Use after the core theorem, not as equal-weight headline results:

- `addressable_codebooks.py`
- `codebook_families.py`
- `docs/addressable_codebook_bound.md`
- `docs/composition_code_rate.md`

These weaken the full-product premise while retaining a large open-interface lower bound.

## Stronger-model extension

`approximate_addressability.py` and `docs/approximate_addressability.md` remain secondary because they replace exact recovery with bounded-error recovery. Fano/information inequalities are classical substrate.

## Historicalized material

Exact converse/reuse, generic canonical quotient branches beyond the retained CORE-1 dependency, resource-accounting, observation-window, evidence/mechanism/repair branches, and ecological special cases are Git-history provenance rather than manuscript dependencies.

Pre-removal recovery pin:

`0d3424a9090b86eae4e369d3749bbe39b6b03432`.

## Claim boundary

Do not claim novelty for:

- fixed-grammar minimization;
- partition refinement;
- contextual/input-restricted reduction in general;
- generic noncommutation;
- generic locality or code counting;
- Fano/information inequalities;
- universal sequential-machine compilation.

The first paper uses the same-system cross-grammar extremal separation as its quantitative center. The bounded-local relay is an explicit constrained extremal/sharpness realization **without historical-firstness language**. The H1–H4 compiler audit is Related Work provenance and is not a manuscript-drafting blocker.

## In-repository integration rule

1. draft publication prose only under `manuscript/`;
2. keep theorem code in `causal_model/`;
3. keep proof source/claim maps in `docs/`;
4. before a submission snapshot, pin the exact CCOC commit SHA and run:

```bash
python scripts/verify_theorem_registry.py --check --write-report
python scripts/verify_paper_core.py --write-report
pytest -q
```

5. record the successful SHA in the manuscript provenance block;
6. never cite `main` or `latest` as proof provenance.

## Stop rule

The next work is manuscript construction, source-checked Related Work, and submission QA. New theorem families or repository splits are out of scope unless the current paper exposes a concrete scientific gap.
