# Current RACH/CCOC architecture

## Purpose

RACH/CCOC contains valid results with different questions. They are not presented
as one linear theorem chain. This document maps the current logical packages,
public import surfaces, certificates, and research boundaries after the August
2026 reopening and strengthening pass.

Read [research priorities](research_priorities.md) for the active agenda and
[theorem registry](theorem_registry.md) for provenance.

## 1. Portability core

```python
import causal_model.portability_core as rach
```

This is the structural research entrance for the question

\[
\text{When does exact compression survive a declared expansion of composition/future grammar?}
\]

### Historical publication spine

| Role | Canonical modules |
|---|---|
| exact grammar-aware factorization | `dynamic_boundary_blankets.py`, `grammar_aware_blankets.py` |
| extension--compression obstruction | `extension_compression_noncommutation.py` |
| bounded-local sharpness | `extension_compression.py`, `relay_tree_compilation.py` |
| conservative portability boundary | `compositional_boundedness.py`, `coherent_portable_macrolaw.py`, `conservative_macro_schema.py` |

The historical `CORE-1`--`CORE-5` IDs remain the v1 reproducibility anchors. They
are not a ban on stronger mathematics.

### Post-reopening strengthening layer

The first reopened targets are now **completed**, not future agenda items.

| Strengthening | Main modules / docs | Current role |
|---|---|---|
| arbitrary addressable codebooks | `addressable_codebooks.py`, `docs/addressable_codebook_bound.md` | strict weakening of the full-product premise |
| exact closed-union common refinement and join capacity | union/refinement implementation, `docs/union_grammar_refinement_capacity.md` | exact characterization in the delimited union-grammar subclass |
| static/dynamic inflation decomposition | `interface_inflation.py`, `docs/interface_inflation_decomposition.md` | separates join-realizability loss from open-only future innovation |
| one-new-action maximal innovation | `single_action_innovation.py`, `docs/single_action_innovation.md` | `iota_new=m` with one newly legal primitive action |
| absolute capacity and exact relay latency | `innovation_capacity_latency.py`, `docs/innovation_capacity_latency.md` | proves zero memory slack on the finite domain and zero latency slack in the declared selector/return architecture |
| general local causal-cone order bound | local causal-cone implementation, `docs/local_causal_cone_bound.md` | gives `Omega(log m)` access in the broader radius-one bounded-local class |
| constrained code-rate families | constrained codebook modules, `docs/composition_code_rate.md` | shows near-linear inflation survives parity/fixed-richness constraints |

The current structural conclusion is therefore not merely the historical binary
product witness. The open response interface can be forced by a positive-rate
jointly realizable codebook; the closed-view contribution and genuinely new
open-only future contribution can be separated; and one newly legal primitive
action can realize the absolute finite-domain maximum open-only innovation on the
existing degree-three relay.

### Locality statement

Two locality claims are intentionally separate.

1. **Architecture-specific:** the balanced binary selector plus same-tree return
   path attains `2 log2(m) + 2` actions for powers of two, matching its declared
   prefix-free/one-edge-per-step lower bound.
2. **General bounded-local class:** radius-one propagation plus bounded local state
   and bounded degree imply only an order lower bound `T = Omega(log m)` for
   `2^{Theta(m)}` exact response classes.

Bounded degree alone is not a causal-speed theorem.

### Novelty boundary

The core must not be narrated as a new fixed-grammar quotient, common-refinement
identity, generic state-complexity blow-up, or generic locality theorem. The live
manuscript candidate is the **same-system cross-grammar response-interface
separation**, together with the constrained extremal witness. Historical
realization priority for the relay remains gated by issues #122 and #137.

## 2. Identifiability companion

```python
import causal_model.identifiability_companion as rach_id
```

This package asks a different question:

\[
\text{What can finite evidence or a retained mechanism family justify?}
\]

| Role | Modules |
|---|---|
| delayed exposure and finite-adaptive no-go | `delayed_addressability.py`, `adaptive_closure_no_go.py` |
| candidate mechanism agreement | `candidate_safe_laws.py` |
| joint exterior--mechanism conditions | `joint_open_candidate_laws.py` |
| retained-family support | `admissibility.py`, confidence-lifting modules, `symbolic_candidate_sets.py` |

The adaptive closure no-go is already implemented: every finite-depth adaptive
policy can be matched by a delayed closed/open pair that has the same finite
transcript and diverges later. This result is epistemic and remains outside the
first-paper structural theorem spine.

## 3. Approximate robustness companion

`causal_model/approximate_addressability.py` is a post-reopening companion, not a
new public core facade. It uses a Fano bound to show that approximate coordinate
recovery with fixed error below one half still forces linear retained information
in the binary full-product family:

\[
K_{\mathrm{open}}^{(\varepsilon)}
\ge
1+m\bigl(1-h_2(\varepsilon)\bigr).
\]

This answers a zero-error brittleness objection. It does **not** yet provide an
approximate/stochastic portability theorem.

## 4. Compatibility aggregate

```python
import causal_model.current_theory as historical
```

`current_theory.py` remains a broad backward-compatible aggregate for earlier
imports and regressions. It is not the preferred research entrance for new work.
Use the portability facade, identifiability facade, or an explicitly named
companion module.

## 5. Experimental-design legacy shelf

Reset panels, witnessed evidence, panel robustness, common-mode failure, and
observation-regime special cases remain executable in their original modules.
They begin after a quotient/reset/coverage/failure contract has been selected and
are therefore not part of the structural novelty spine. See
[`legacy/README.md`](../legacy/README.md).

## 6. Replacement / rewiring transport

Non-nested replacement, extinction, recolonization, rewiring, and transport repair
are centered in `zuizui0223/mltr`. They should return to CCOC only if they directly
strengthen the open-composition theorem rather than forming a parallel transport
program.

## 7. Certificate and workflow discipline

Every theorem module retains finite certificate objects and replay routes. A
workflow replays a declared finite domain; it does not prove the analytic theorem
for all finite systems and does not validate an observed ecosystem.

New structural mathematics must:

1. name the exact canonical assumption or conclusion being changed;
2. distinguish theorem, sufficient criterion, lower bound, witness, conjecture,
   and computational evidence;
3. include fail-closed tests/counterexamples where feasible;
4. preserve the July 2026 historical paper-core replay; and
5. enter `main` through a branch and pull request.

The active agenda is now dominated by novelty verification and manuscript
transfer, not by another local special-case theorem. See
[`research_priorities.md`](research_priorities.md).

## Navigation

- [Research priorities](research_priorities.md)
- [Theorem registry](theorem_registry.md)
- [Claim-status audit](claim_status_audit.md)
- [Residual novelty decision](residual_novelty_decision_2026-08-12.md)
- [Cross-grammar quantitative prior-art boundary](cross_grammar_quantitative_prior_art_2026-08-12.md)
- [Universal compiler source audit](universal_compilation_source_audit.md)
- [Legacy shelf](../legacy/README.md)
