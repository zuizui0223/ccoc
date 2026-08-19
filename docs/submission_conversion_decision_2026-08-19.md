# CCOC submission-conversion decision — 2026-08-19

## Decision

CCOC is no longer in theorem-expansion mode for the first paper. The current theorem package is sufficient. Remaining work is manuscript construction, claim control, replay pinning, and journal-specific submission QA inside this repository.

Do not add another theorem family unless a current claim fails and the first paper cannot be supported without replacement mathematics.

## First-paper question

> How large can the exact response-interface penalty become when one keeps the controlled system fixed and enlarges only the legal future grammar?

The paper's ecological reading is:

> present/closed functional equivalence need not imply open-future causal equivalence.

## Formal hierarchy

- **CORE-1:** fixed-grammar exact response quotient; foundational substrate, not a novelty claim.
- **CORE-2:** operational/codebook language for the cross-grammar lower bound.
- **CORE-3:** explicit extremal bounded-local sharpness realization.
- **CORE-4/5:** sufficient portability and local obstruction boundaries.

Two retained strengthenings support the paper without becoming additional headline results:

- constrained codebooks weaken the full-product premise;
- approximate addressability tests robustness to bounded decoding error.

## Novelty boundary

Do not claim novelty for:

- context- or input-dependent state minimization;
- fixed-grammar quotient refinement;
- generic noncommutation between reduction and realization/composition;
- pair-separation/cardinality arguments;
- generic bounded-local or universal sequential-machine compilation;
- Fano/information inequalities.

The quantitative center is the same-system closed/open extremal separation. The bounded-local relay is presented as a transparent constrained sharpness witness **without historical-firstness language**.

Issue #122 and related H1–H4 compiler-source work remain useful Related Work provenance, but they no longer block drafting or submission as long as the manuscript does not make a historical firstness claim for the relay.

## Journal lane

Primary target: **Theoretical Ecology**.

The manuscript must lead with the ecological state-representation problem and use finite-state/automata machinery as the proof vehicle rather than the scientific endpoint.

Fallback: **Journal of Mathematical Biology** if the final paper remains substantially more theorem-centered than ecology-centered.

## Manuscript location

All submission prose stays inside CCOC under `manuscript/`.

Canonical route:

```text
manuscript/main.md
  -> docs/manuscript_readiness_audit.md
  -> docs/manuscript_traceability.md
  -> theorem/proof sources
  -> executable replay
```

The theorem code remains in `causal_model/`; it is never copied into a second manuscript repository.

## Submission gates

### Satisfied

- CORE-1–CORE-3 analytic proofs exist;
- deterministic witnesses/tests exist;
- constrained-codebook and approximate-addressability robustness exist;
- the first-paper theorem surface is already reduced;
- CCOC/MLTR/MRM/CED ownership boundaries are explicit;
- separate-repository creation is no longer a blocker;
- firstness language for the relay has been surrendered.

### Remaining

1. Complete the self-contained manuscript prose and analytic proofs under `manuscript/`.
2. Make Related Work source-checked and consistent with the conservative novelty boundary.
3. Build the four-figure contract.
4. Pin one immutable CCOC submission SHA after manuscript-facing cleanup.
5. On that SHA run:
   - `python scripts/verify_theorem_registry.py --check --write-report`
   - `python scripts/verify_paper_core.py --write-report`
   - `pytest -q`
6. Record theorem/source/replay traceability in the manuscript.
7. Perform final human review of every novelty, historical, ecological-interpretation, and authorship/disclosure statement.

## Stop rule

No additional score, special case, field protocol, evidence theorem, mechanism theorem, semantic-repair theorem, or ecological relabeling belongs in the first paper. The next work is manuscript completion and submission QA.
