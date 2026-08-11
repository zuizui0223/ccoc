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

Post-reopening work now separates the sources of that inflation. `CORE-2` has an
arbitrary addressable-codebook lower bound and, for exact closed-grammar unions,
a common-refinement characterization with a fibered join capacity. The full open
grammar may then add genuinely new future words that refine the closed union
further. The resulting exact decomposition is

\[
\Delta_{\rm total}
=
\Delta_{\rm capacity}
-
\delta_{\rm join}
+
\iota_{\rm new}.
\]

The static first two terms have natural-join ancestry. The dynamic last term has a
sharpness family on the degree-three binary relay: every fixed closed composition
already permits its `0/1` address routing and `tick`, but excludes only the single
primitive action `fire`. Every fixed closed quotient, their union, and the static
join capacity remain one bit. Legalizing that one action makes all dormant leaf
reads available and forces

\[
\boxed{\iota_{\rm new}=m}
\]

additional bits while the full action alphabet remains size four.

This `m`-bit innovation is now also closed from above. On the declared finite
macro domain `D_m={0,1}^{m+1}`, no open quotient can add more than

\[
\log_2|D_m|-\log_2|P_U|=m
\]

bits relative to the two-state closed-union quotient. The open relay quotient is
discrete, so it attains that **absolute finite-domain innovation capacity**.

The same family is latency-sharp under the explicit local architecture it actually
implements: a unique selector moves at most one parent--child edge per address
symbol, `fire` injects a pulse at one terminal memory leaf, and the pulse moves at
most one child--parent edge per `tick` to the focal output. Prefix-free binary
addressing plus the return path gives

\[
L_{\rm query}^{\rm worst}
\ge
2\lceil\log_2m\rceil+2.
\]

For the balanced power-of-two family, every canonical probe has exactly
`2 log2(m) + 2` actions, so the construction attains this declared-locality lower
bound with equality. No latency claim is made for arbitrary bounded-degree systems
with unrestricted global operations.

The historical `CORE-5` newly-legal-word fiber split is the local witness for a
positive `iota_new` term. Constrained parity and fixed-richness families separately
quantify the join-realizability term.

## Start here

- [Freeze/reopening record](FREEZE.md) — historical freeze point and current
  development policy.
- [Addressable-codebook bound](docs/addressable_codebook_bound.md) — post-reopening
  strict weakening of the full-product premise, with comparison-domain scope.
- [Union-grammar refinement capacity](docs/union_grammar_refinement_capacity.md) —
  exact common-refinement characterization, fibered capacity, and join-realizability
  defect for the union-grammar subclass.
- [Database-join ancestry](docs/database_join_ancestry.md) — classical lossless
  natural-join ancestry and the corresponding novelty boundary.
- [Interface inflation decomposition](docs/interface_inflation_decomposition.md) —
  separates closed-view capacity, join-realizability loss, and open-only future
  innovation, absorbing the fiber-split obstruction into one exact accounting.
- [Single-action innovation](docs/single_action_innovation.md) — one newly legal
  primitive action creates `m` bits of pure open-only innovation on the existing
  bounded-degree constant-alphabet relay.
- [Innovation capacity and latency](docs/innovation_capacity_latency.md) — proves
  the `m`-bit family is absolutely memory-sharp and exactly latency-sharp under
  its declared one-edge-per-step local selector/pulse architecture.
- [Composition code rate](docs/composition_code_rate.md) — constrained families,
  fixed-richness asymptotics, and bounded-degree relay inheritance.
- [Constant-alphabet relay](docs/constant_alphabet_relay.md) — binary-address
  strengthening of the bounded-locality sharpness construction.
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

Post-reopening strengthening tests are part of the ordinary test suite but are
not silently added to the historical v1 paper-core replay until a new versioned
core is deliberately promoted.

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
