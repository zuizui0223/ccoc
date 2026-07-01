# RACH asset map: active theorem core, future gold, and frozen support

This is a routing map, not a deletion list. The repository accumulated several
substantial implementations before its current theorem spine became clear. The
correct response is neither to pretend they are one theory nor to discard them
blindly. Retain each asset for the job it can actually do.

Read [the theorem spine](theorem_spine.md) first. This map answers the practical
question: **where should the next unit of work go?**

## Classification rule

An asset is **active core** only if it states or verifies one of the promotion
obligations in the theorem spine. An asset is **gold** if it can sharpen,
falsify, or empirically connect a future core theorem without changing that
theorem's subject. An asset is **frozen infrastructure** when it preserves proof
identity or history without strengthening a causal claim.

## 1. Active core: theorem work belongs here

| Asset | Exact present role | Promotion obligation |
|---|---|---|
| `causal_closure_calculus.py` | finite global closure, recurrence, multistability | local rule \(\to\) long-run rule |
| `observation_window_completion.py` | passive-window completion no-go; grammar refinement | passive observation \(\to\) open boundary |
| `extension_compression.py` | fixed closed port versus open port family | closed compression \(\to\) open compression |
| `addressable_completion_bounds.py` | product lower bound, gap inequality, finite blanket obstruction | independently addressable exterior memory |
| `relay_tree_compilation.py` | constant local grammar, pairwise, degree-three realization | robustness of binary selected-port witness |
| `dynamic_boundary_blankets.py` | coarsest dynamic interface, finite blanket and horizon upper bounds | positive open-law criterion |
| `delayed_addressability.py` | prefix grammar, delayed separator, no uniform horizon | outside-delay obstruction |
| `candidate_safe_laws.py` | universal-law criterion, response type, set-valued/candidate-safe outputs | candidate plurality obstruction |
| `joint_open_candidate_laws.py` | common dynamic-interface criterion and joint separator lower bound | universal open laws and justified exterior-plus-mechanism additivity |
| `observation_regime_closure.py` | exact two-regime comparison | special operational grammar change |
| `current_theory.py` | focused public import surface | required entrance for new theorem work |

The core's current combined claim is not one universal theorem. It is a ladder:

\[
\text{a local rule may be promoted only after its time, outside, horizon,
dynamic-interface, and candidate-mechanism obligations have been certified at the claimed level.}
\]

## 2. Gold seam A: grammar-aware positive blanket theorem

The next theorem should strengthen the **positive** side of the delayed grammar
work. `delayed_addressability.py` currently proves finite grammar-aware quotient
stabilization and an unbounded-family delay obstruction. The missing result is a
positive factorization theorem over the product of physical system state and
finite prefix-grammar state.

| Existing asset | Gold that remains | What it must not do |
|---|---|---|
| `delayed_addressability.py` | finite prefix grammar, legal-word product quotient | do not treat grammar state as merely an implementation timer |
| `dynamic_boundary_blankets.py` | update-closed interface and coarsest quotient pattern | do not ignore enabled-action structure when comparing grammar states |
| `joint_open_candidate_laws.py` | common dynamic-interface language | do not require candidate plurality for a grammar-only theorem |
| `relay_tree_compilation.py` | structural selected-port realization | do not claim a full multi-valued joint relay compiler without proving it |

### Extraction target

Build a **grammar-aware dynamic blanket certificate** for a finite controlled
system \(S\) and a finite prefix grammar \(G\). A summary on \(S\times G\) must
preserve:

1. current output;
2. the set of enabled future actions; and
3. successor summary under every enabled action.

The theorem should identify the canonical grammar-aware quotient as the coarsest
exact legal-word interface and give the finite bound in terms of realized summary
states. Grammar state is a declared boundary contract, not automatically a new
physical ecological variable.

## 3. Gold seam B: joint micro-compilation and red-team

| Existing asset | Gold that remains | Future use |
|---|---|---|
| `relay_tree_compilation.py` | degree-three binary selected-port compiler | extend only with an explicit multi-valued/joint protocol theorem |
| `joint_open_candidate_laws.py` | canonical joint product and separator certificates | red-team whether joint realizability/separation premises are necessary |
| `failure_modes.py` | counterexamples to hidden compatibility, inhibition, latent routes | search for false additive-lower-bound conjectures |
| `generative_benchmarks.py` | exact finite sweeps | map restricted failure domains |
| `observation_envelope.py` | channel-induced decision envelopes | test which joint distinctions a channel cannot expose |

### Extraction target

Build a **joint-counterexample protocol**:

```text
proposed grammar-aware blanket or additive joint-law claim
    -> bounded completion/candidate grammar search
    -> equal observed prefix with a future separator or transition obstruction
    -> independently checked certificate
    -> prove, weaken, or reject the condition
```

This layer should mine and certify counterexamples. It should not dictate what
the theorem is about.

## 4. Gold seam C: retained-family and evidence gateway

| Existing asset | Gold that remains | What it must not do |
|---|---|---|
| `admissibility.py` | unanimity / `UNRESOLVED` discipline over retained families | do not force new completion grammars into old motif vocabulary |
| `confidence_lifting.py` | false-decisive control from simultaneous retained-set coverage | does not establish open-interface validity |
| `anytime_confidence_lifting.py` | optional-stopping/all-look retained-set control | should not become the repository headline |
| `symbolic_candidate_sets.py` | large retained families that cannot be listed | solver feasibility is not outside invariance |
| PR #31 finite-alphabet e-process backend | restricted proof-carrying retained-family construction from data | restricted evidence backend, not an open-law theorem |

### Extraction target

Later, and only behind the exact structural interfaces now defined, extract:

\[
\text{data or solver output}
\to
C_t\text{ of retained completion/mechanism candidates}
\to
\text{universal, candidate-safe, set-valued, or UNRESOLVED verdict}.
\]

The adapter must accept arbitrary candidate-specific boundary and response
certificates. It must not assume floral mechanisms, Boolean motifs, or a fixed
small action vocabulary.

**Status:** preserve these modules and PR #31 as evidence-gateway staging. Do
not promote or expand them until the structural theorem specifies exactly what
the evidence must retain.

## 5. Freeze shelf: provenance is not the scientific claim

The following family is technically substantial but should not drive current
research work:

- `certificate_manifest.py`, `tiered_certificate_manifest.py`, and canonical
  JSON variants;
- `admission_transcript.py`, compiled/native transcript variants, and replay
  registries;
- signed transcript checkpoints;
- coverage-contract and transcript adapters; and
- tiered artifact plumbing around those formats.

They answer:

\[
\text{Which artifact was used, and has its history changed?}
\]

They do **not** answer whether an exterior completion remains possible, whether
a dynamic blanket is sufficient, or whether one macro transition is universal.

**Status:** keep tests passing. Add no new provenance feature unless a published
theorem certificate genuinely requires an audit chain. Do not casually delete
this code: exact-proof assets may still depend on it.

## 6. Compatibility shelf

`causal_model/__init__.py` is a broad backwards-compatible export surface for
older theorem, benchmark, and design modules. It is intentionally not the
research entrance. New theorem work must use `causal_model.current_theory`.

## Immediate queue

1. **Grammar-aware dynamic blanket theorem.** Give a positive finite factorization
   theorem on system-state × prefix-grammar-state, including enabled-action
   structure and update closure.
2. **Joint micro-compilation.** Compile the multi-valued joint witness to a
   degree-three pairwise protocol, or prove the sharp restricted compiler result.
3. **Joint counterexample miner.** Search small hostile grammar/candidate families
   for a future separator or macro-transition obstruction.
4. **Evidence bridge only after 1–3.** Narrow/rebase retained-family and e-process
   work behind generic candidate-boundary interfaces.
5. **Freeze audit work.** No new manifest, transcript, checkpoint, or provenance
   variant without a concrete theorem-publication requirement.

## Anti-queue

Do **not** spend the next cycle on:

- another coordinate toy whose only novelty is a larger state table;
- a provenance wrapper around an unchanged theorem;
- a domain-specific floral or ecological model inside this repository;
- a generic statistical backend unconnected to retained completion/mechanism
  families; or
- presenting a finite witness as a universal empirical claim.
