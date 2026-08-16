# CCOC — causal compression under open composition

CCOC is a theorem-first mathematical-ecology repository for one finite question:

> When can exact compression valid under fixed closed future grammars fail to provide one comparably small exact interface after the legal future grammar is opened?

The current formal scope is finite and mostly deterministic. Passing certificates establish properties of declared finite models; they do not validate an observed ecosystem.

## Core result

The first-paper spine is deliberately narrow:

1. `CORE-1` — exact grammar-aware response interface as foundational substrate;
2. `CORE-2` — **cross-grammar extension/compression lower bound**, the headline theorem candidate;
3. `CORE-3` — bounded-local extremal realization showing sharpness under simple local structure.

Two additional executable results remain as supporting boundaries only:

- `CORE-4` — a conservative sufficient condition under which one declared macro-law survives expansion;
- `CORE-5` — a future-word/new-action split that refutes one proposed merge.

They are not independent CCOC novelty claims and must not be expanded into a source-relative repair theory.

The strongest explicit family has, for every `m>=1`,

\[
|P_C|=2,
\qquad
|P_O|=2^{m+1},
\qquad
K_O-K_C=m,
\]

while using one fixed four-symbol primitive alphabet, one newly legal primitive action, pairwise radius-one dynamics, maximum degree three, cut one, and logarithmic selected-coordinate access.

The safe headline is therefore a **same-system cross-grammar quantitative separation**, not the invention of finite-state minimization.

## CCOC–MLTR claim firewall

CCOC and [MLTR](https://github.com/zuizui0223/mltr) share exact-interface and refinement substrate but answer different quantified questions.

CCOC optimizes separately under each closed grammar and compares those minima with the minimum exact interface under a jointly open grammar:

\[
K_i^*=\min_{q\text{ exact under }\Gamma_i}\log_2|q|,
\qquad
K_O^*=\min_{q\text{ exact under }\Gamma_O}\log_2|q|.
\]

Its target separation is

\[
\max_i K_i^*=O(1),\qquad K_O^*=\Omega(m).
\]

No inherited source partition is fixed, and the closed optima may be different.

MLTR fixes an already accepted source macro-law, transports its labels through a declared structural change, and asks whether that inherited law remains exact and, if not, what unique coarsest exact refinement preserves its inherited semantics. **Minimal repair, transport defect, route coherence, and history completion belong to MLTR, not CCOC.**

See `docs/ccoc_mltr_claim_firewall_2026-08-16.md`.

## Novelty boundary

Do **not** claim novelty for fixed-grammar quotient/minimization, input/context-restricted state reduction, partition refinement, common refinement, ordinary distinguishability, generic causal-cone locality, or generic information inequalities.

The remaining first-paper candidate is the simultaneous quantitative package: very small closed interfaces and closed union, one tiny grammar opening, maximal new exact response memory, and the same bounded-local realization.

Historical firstness of the bounded-local realization remains conditional on the H1–H4 primary-source compiler audit.

## Current code surface

Preferred structural entrance:

```python
import causal_model.portability_core as rach
```

Canonical first-paper modules are listed in `docs/current_architecture.md`.

Distinct follow-up modules remain explicit rather than being re-exported through one giant theory facade.

### Deterministic feedback

The former five-module feedback theorem family has been reduced to two representative executable examples:

- `causal_model/feedback_gate_rank.py` — feedback-cycle memory with causal-arrow ablation;
- `causal_model/feedback_type_portability.py` — replication-independent five-state positive example.

The general continuation-refinement / unique-coarsest-repair result is classical minimization substrate. PR #207/#208/#210 implementations and detailed proof notes are retained in Git history rather than the current tree.

See:

- `docs/feedback_portability_theorem_family_2026-08-15.md`
- `docs/feedback_novelty_audit_2026-08-16.md`

Full pre-cleanup feedback surface:

`4c7887c73ba8fa86a5e3883ebb6dce265b80fe7a`

## Repository cleanup status

CCOC is currently in a **surface-reduction phase**. Files are classified as:

- **CURRENT** — publication core or a distinct active extension;
- **COMPATIBILITY** — still used by current repository consumers;
- **HISTORICAL** — conclusion/provenance retained, implementation may live only in Git history;
- **REMOVE** — duplicated or superseded current-tree surface.

The deprecated `causal_model.current_theory` aggregate has been removed because no active repository code imported it. The broad package-root facade remains temporarily while old examples/scripts are audited.

Cleanup record:

- `docs/core_surface_cleanup_manifest_2026-08-14.md`
- `docs/package_boundary_plan.md`
- `docs/research_priorities.md`

## Reproducibility

The historical paper-core replay remains:

```bash
python scripts/verify_theorem_registry.py --check --write-report
python scripts/verify_paper_core.py --write-report
pytest -q
```

`tests.yml` is the generic Python 3.10/3.11/3.12 test gate. Specialized workflows should remain only when they provide a distinct legacy, artifact, or frozen replay contract.

## Start here

- `docs/ccoc_mltr_claim_firewall_2026-08-16.md` — hard boundary against MLTR repair theory
- `docs/current_architecture.md` — current code/theorem map
- `docs/residual_novelty_decision_2026-08-12.md` — controlling novelty decision
- `docs/manuscript_readiness_audit.md` — first-paper claim boundary
- `docs/manuscript_transfer_manifest_2026-08-14.md` — eventual transfer contract
- `docs/core_surface_cleanup_manifest_2026-08-14.md` — executed cleanup decisions
- `docs/theorem_registry.md` — theorem provenance
- `docs/nonempirical_scope.md` — ecological non-claims
- `FREEZE.md` — historical freeze and reopening policy

## Development rule during cleanup

Do not add a new theorem family while repository reduction is active unless it changes a material model premise and survives prior-art classification.

Do not add source-relative minimal repair, transport defect, route-coherence, or history-completion theorem families here; those belong to MLTR.

The current task is to make the surviving scientific result easier to see, not to increase theorem count.