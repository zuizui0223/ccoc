# RACH asset map: what to mine, what to freeze

This document is a routing map, not a deletion list. The repository accumulated
several substantial implementations before its present theorem spine became
clear. The correct response is not to pretend that all of them are one theory,
or to discard them blindly. It is to retain each asset for the job it can
actually do.

## Rule of classification

An asset is **active core** only if it states or verifies a promotion claim from
[the promotion calculus](promotion_calculus.md). An asset is **gold** if it can
make a future core theorem sharper, falsifiable, or empirically connectable
without changing that theorem's subject. An asset is **frozen infrastructure**
when it preserves proof identity or history but does not strengthen the causal
claim itself.

## 1. Active core: do new theory work here

| Asset | Current role | Relation to RACH |
|---|---|---|
| `causal_closure_calculus.py` | finite global closure, recurrence, and multistability certificates | failure of promotion across **time** |
| `observation_regime_closure.py` | paired natural / observer-coupled rule systems | failure of promotion across **regimes** |
| `extension_compression.py` | exact closed-versus-open interface separation | failure of promotion across **composition** |
| `relay_tree_compilation.py` | constant-grammar, pairwise, degree-three implementation of the interface witness | removes the hidden high-degree / global-read objection |
| `current_theory.py` | deliberately small public entrance | only import surface for new theorem work |

The main current claim is not “uncertainty is large.” It is:

\[
\text{closed-system causal compression}
\not\Rightarrow
\text{open-system causal compression}.
\]

## 2. Gold seam A: retained-family and evidence gateway

| Existing asset | Gold that remains | What it must **not** do |
|---|---|---|
| `admissibility.py` | candidate-family consensus discipline: a conclusion needs unanimity or becomes `UNRESOLVED` | it must not force the new open-interface theorem into the old motif / switch vocabulary |
| `confidence_lifting.py` | generic logic for lifting simultaneous retained-set coverage to a false-decisive bound | it does not establish a causal law or an interface quotient |
| `anytime_confidence_lifting.py` | optional-stopping / all-look version of the same retained-family logic | it should not become the repository headline |
| `symbolic_candidate_sets.py` | retained families that are not enumerable by hand | solver feasibility is not a proof of composition stability |
| PR #31 finite-alphabet e-process backend | a concrete, proof-carrying way to construct nested retained candidate sets from data | it is a restricted evidence backend, not the open-system theorem |

### Extraction target

Later, extract a **generic retained composition-family adapter**:

\[
\text{data or solver output}
\to
C_t\ \text{of retained world / port-grammar candidates}
\to
\text{candidate-safe interface verdict}.
\]

The adapter should consume arbitrary candidate-specific interface certificates.
It should not assume that a candidate is a Boolean motif, a floral mechanism, or
a disjunctive driver switch.

**Status:** preserve these modules and the e-process PR as an evidence-gateway
staging area. Do not merge or expand them merely because they are sophisticated;
rebase and narrow them only when the composition theorem needs actual retained
families.

## 3. Gold seam B: counterexample miner and exact proof kernel

| Existing asset | Gold that remains | Future use |
|---|---|---|
| `linear_proof_verifier.py` | exact rational witness and Farkas-certificate checking | independently verify finite / polyhedral counterexamples to a proposed preservation theorem |
| `rational_polyhedral_inclusion.py` | exact inclusion checks | test whether a claimed extension class really preserves a declared quotient region |
| `polyhedral_motif_compiler.py` | a compiler from declared semantics to checkable finite query families | only reuse after a new theorem is genuinely expressible in its restricted grammar |
| replayable exact-proof modules | content-addressed proof objects | attach a counterexample or finite exhaustion to a theorem claim, not as a new theory layer |
| finite theorem GitHub workflows | deterministic enumerative regression pattern | make every new finite witness replayable and falsifiable |

### Extraction target

Build a small **counterexample search protocol** for proposed open-composition
claims:

```text
conjectured preservation condition
    -> bounded finite grammar search
    -> exact separating trace / countermodel
    -> independently checked certificate
    -> promote condition, weaken it, or reject it
```

This is where the existing exact-verification machinery can create mathematical
value. It should mine counterexamples and certify them; it should not dictate
what the theorem is about.

## 4. Gold seam C: adversarial model laboratory

| Existing asset | Gold that remains | Correct role now |
|---|---|---|
| `ecological_program.py` | finite grammar for conjunction, inhibition, alternatives, and feasibility restrictions | adversarial source of semantic counterexamples; not the RACH core ontology |
| `failure_modes.py` | explicit counterexamples to hidden compatibility, inhibition, latent routes, and noisy NULL interpretation | red-team tests for every claimed theorem scope |
| `generative_benchmarks.py` | exact finite sweeps rather than Monte Carlo rhetoric | phase diagrams for where a restricted theorem fails |
| `observation_envelope.py` | exact channel-induced decision envelopes | test the gap between a declared observation channel and a retained candidate family |
| `observation_design.py`, `robust_panel_design.py`, `panel_phase_benchmarks.py` | discrete panel-selection and non-greedy synergy machinery | a later corollary about evidence needed to collapse a retained composition family, never the central theorem |
| `benchmarks.py` | comparison to known finite truth | regression / calibration harness |

### Extraction target

Turn this layer into a **theorem red-team library**. A new RACH theorem should
be tested against deliberately hostile small grammars:

- latent extension ports;
- compatibility restrictions;
- inhibitory or conjunction-dependent local rules;
- simultaneous-message collisions;
- hidden state that breaks a claimed quotient; and
- observation channels that cannot distinguish candidate compositions.

A failure found here is not an embarrassment. It tells us the theorem statement
needs a sharper boundary.

## 5. Freeze shelf: provenance is not the scientific claim

The following family is technically substantial but currently should not drive
new work:

- `certificate_manifest.py`, `tiered_certificate_manifest.py`, and canonical
  JSON variants;
- `admission_transcript.py`, compiled/native transcript variants, and replay
  registries;
- signed transcript checkpoints;
- coverage-contract and transcript adapters; and
- tiered artifact plumbing around those formats.

Their legitimate question is:

\[
\text{Which artifact was used, and has its history changed?}
\]

They do **not** answer:

\[
\text{Is the candidate universe adequate?}
\quad\text{or}\quad
\text{Does a portable causal law exist?}
\]

**Status:** keep tests passing; make no new provenance feature unless RACH begins
publishing externally supplied theorem certificates that actually require an
audit chain. Do not delete the code in a cleanup PR: too many exact proof assets
still depend on it.

## 6. Compatibility shelf: keep, but do not advertise as the core

`causal_model/__init__.py` is a broad backwards-compatible export surface for
older theorem, benchmark, and design modules. It is intentionally not the
research entrance. New theorem work must use `causal_model.current_theory` and
link to this map when it reuses a legacy module.

This keeps existing imports working without allowing the package namespace to
make a false claim that all exported modules form one integrated model.

## Immediate queue

1. **Theorem, not tooling:** characterize a nontrivial class of extension grammars
   for which a bounded open-safe quotient *is* preserved, or give a sharp lower
   bound when it is not.
2. **Separate two notions:** define exactly when an open-safe interface admits a
   single candidate-independent deterministic macro transition.
3. **Counterexample miner:** expose the smallest reusable search/check interface
   over finite extension grammars, reusing the exact proof kernel only as a
   verifier.
4. **Evidence bridge only after 1–3:** rebase the finite-alphabet e-process work
   or extract its minimal protocol behind a generic retained-composition-family
   interface.
5. **Freeze the audit stack:** no new manifest, transcript, checkpoint, or
   provenance variant without a concrete theorem-publication requirement.

## Anti-queue

Do **not** spend the next cycle on:

- another toy whose only novelty is a larger state table;
- an extra audit wrapper around an unchanged theorem;
- a domain-specific floral or ecological model inside this repository;
- a generic statistical backend unconnected to retained composition families; or
- presenting a finite witness as a universal empirical claim.
