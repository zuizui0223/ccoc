# RACH: causal compression under open composition

RACH is a theorem-first **mathematical ecology** source archive for one finite
question:

> When does exact compression in each fixed closed composition fail to extend to one small exact interface for a declared open composition grammar?

The active publication package is finite and deterministic. It contains no field
datasets, fitted ecological parameters, or claim that a passing certificate
validates an observed ecosystem.

## Paper core

The manuscript uses one theorem package.

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

## Start here

- [Paper-core mathematical audit](docs/paper_core_audit.md) — formal proof versus
  finite replay, corrected assumptions, and the GitHub Actions contract.
- [Publication-core scope](docs/manuscript_readiness_audit.md) — theorem-to-paper
  map, robustness limits, and explicit non-claims.
- [Portability core v1](docs/portability_core_v1.md) — formal source statement of
  the active theorem family.
- [Theorem registry](docs/theorem_registry.md) — complete provenance record for
  active and archived finite results.
- [Non-empirical scope](docs/nonempirical_scope.md) — what RACH does and does not
  establish about ecology.
- [Legacy shelf](legacy/README.md) — retained non-publication theorem branches,
  compatibility status, and later physical-move plan.

## Active public import

```python
import causal_model.portability_core as rach
```

`causal_model.current_theory` and `causal_model.identifiability_companion` remain
only as archived compatibility surfaces. They are not entry points for new work
or the present manuscript.

## Reproducibility boundary

The active verifier set is restricted to the finite theorem assets behind
`CORE-1` through `CORE-5`. In particular, it covers the exact-interface
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

## Archive policy

Replacement transport, finite-evidence limitations, candidate-mechanism
uncertainty, panel designs, and historical examples are retained in the
[legacy manifest](legacy/manifest.md). They may be replayed, but they are outside
the manuscript's theorem package and must not be used to broaden its claim.
