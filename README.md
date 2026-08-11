# RACH: causal compression under open composition

RACH is a theorem-first **mathematical ecology** source archive and active theory
repository for one finite question:

> When does exact compression in each fixed closed composition fail to extend to one small exact interface for a declared open composition grammar?

The current formal scope is finite and deterministic. It contains no field
datasets, fitted ecological parameters, or claim that a passing certificate
validates an observed ecosystem.

> **Development status — active again as of 2026-08-11.** The July 2026 freeze
> remains a reproducibility checkpoint for the first open-composition manuscript,
> but the repository is no longer theorem-frozen. New mathematics may strengthen
> or replace canonical claims when developed on a branch, reviewed by PR, and
> accompanied by explicit assumptions, proofs/certificates, counterexamples, and
> deterministic replay where applicable. See the [freeze/reopening record](FREEZE.md).

## Paper core

The first manuscript package uses one theorem family.

1. **Exact grammar-aware interface.** A finite summary is exact only if output,
   legal-action rows, and successors factor through it.
2. **Extension--compression noncommutation.** Jointly realizable exterior
   coordinates with uniform legal decoder words force an additive lower bound on
   open-interface memory.
3. **Bounded-locality sharpness.** A binary relay family attains the gap with
   pairwise messages, maximum degree three, and a constant-size local
   node/message grammar.
4. **Constructive boundary.** A finite conservative macro schema remains exact
   when newly legal actions are uniform inside every macro fiber; a fiber split
   refutes the proposed merge locally.

The central claim is conditional on a declared finite system and grammar:

\[
\text{closed-context exact compression}
\not\Rightarrow
\text{one small exact interface for the open union grammar}.
\]

The active post-freeze research priority is to determine how far the product and
joint-realisability assumptions behind the lower bound can be weakened while
retaining a quantitative extension--compression separation and bounded-locality
sharpness.

## Start here

- [Freeze/reopening record](FREEZE.md) — historical freeze point and current
  development policy.
- [Paper-core mathematical audit](docs/paper_core_audit.md) — formal proof versus
  finite replay, corrected assumptions, and the GitHub Actions contract.
- [Publication-core scope](docs/manuscript_readiness_audit.md) — theorem-to-paper
  map, robustness limits, and explicit non-claims.
- [Portability core v1](docs/portability_core_v1.md) — formal source statement of
  the first manuscript theorem family.
- [Research priorities](docs/research_priorities.md) — active theorem-strengthening
  agenda after reopening.
- [Theorem registry](docs/theorem_registry.md) — complete provenance record for
  active and archived finite results.
- [Non-empirical scope](docs/nonempirical_scope.md) — what RACH does and does not
  establish about ecology.
- [Legacy shelf](legacy/README.md) — retained non-publication theorem branches,
  compatibility status, and later promotion rules.

## Active public import

```python
import causal_model.portability_core as rach
```

`causal_model.current_theory` and `causal_model.identifiability_companion` remain
compatibility surfaces. New theorem work should use the canonical portability
modules or an explicitly designated successor module rather than silently
broadening compatibility aggregates.

## Reproducibility boundary

The first-paper verifier set remains restricted to the finite theorem assets
behind `CORE-1` through `CORE-5`. In particular, it covers the exact-interface
criterion, addressable-product injection, relay compilation, conservative schema,
and local fiber-split obstruction.

Run the paper-core finite replay locally with:

```bash
python scripts/verify_paper_core.py --write-report
```

It writes `artifacts/paper_core_reproducibility_report.json`. The matching
**Paper-core reproducibility** GitHub Actions workflow runs this replay together
with the explicit paper-core test suite and theorem-registry provenance check.

A passing check confirms that declared finite certificate paths and selected
witnesses remain reproducible. It does not validate an ecological dataset,
infer reachability or a grammar from observations, or establish that an observed
ecosystem satisfies the declared model contract.

## Development policy

The July 2026 frozen paper core is retained as a stable provenance baseline, not
as a ban on further mathematics. New theorem development must:

- occur on a branch and enter `main` through a reviewed pull request;
- state exactly which canonical assumption or conclusion it changes;
- distinguish theorem, lower bound, sufficient condition, witness, conjecture,
  and computational evidence;
- preserve the historical replay of the v1 paper core; and
- avoid broad ecological claims not supported by an explicit model contract.

Replacement transport and rewiring remain developed in `zuizui0223/mltr` unless
a result directly strengthens the open-composition theorem itself.
