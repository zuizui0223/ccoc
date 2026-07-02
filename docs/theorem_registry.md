# RACH theorem registry: retrieval atlas

This is the reader-facing entry point for the finite mathematical theories in the
repository. The canonical machine-readable source is
[`theorem_registry.json`](theorem_registry.json); CI verifies that every entry
has a finite domain, assumptions, conclusion, code path, regression route,
documentation path, and explicit non-claim.

RACH is a **mathematical ecology** repository, not an empirical data repository.
Read [the non-empirical scope policy](nonempirical_scope.md) before connecting a
finite theorem to an ecological application.

## How to retrieve one theory

1. Find the relevant identifier below.
2. Read its exact domain, assumptions, conclusion, and non-claim in
   `theorem_registry.json`.
3. Open the listed module and documentation page.
4. Run the listed regression command. A passing result validates the supplied
   finite certificate only.

## Canonical map

| ID | Mathematical result | Status | Primary module | Main regression |
|---|---|---|---|---|
| `CORE-0` | finite closure classification | exact finite theorem | `causal_model/causal_closure_calculus.py` | `tests/test_causal_closure_calculus.py` |
| `CORE-1` | exact grammar-aware dynamic interface | exact finite theorem | `causal_model/grammar_aware_blankets.py` | `tests/test_grammar_aware_blankets.py` |
| `CORE-2` | addressable-completion and noncommutation bound | lower-bound obstruction | `causal_model/extension_compression_noncommutation.py` | `tests/test_extension_compression.py` |
| `CORE-3` | binary relay sharpness realization | sharpness witness | `causal_model/relay_tree_compilation.py` | `tests/test_relay_tree_compilation.py` |
| `CORE-4` | nested portability ladder | sufficient criterion | `causal_model/coherent_portable_macrolaw.py` | `tests/test_coherent_portable_macrolaw.py` |
| `CORE-5` | future-word / new-action fiber split | local obstruction | `causal_model/conservative_macro_schema.py` | `tests/test_conservative_macro_schema.py` |
| `EXT-1` | non-nested edge preservation | sufficient criterion | `causal_model/non_nested_portability.py` | `tests/test_non_nested_portability.py` |
| `EXT-2` | transported target exact factorization | sufficient finite-domain theorem | `causal_model/non_nested_portability.py` | `tests/test_non_nested_portability.py` |
| `EXT-3` | conservative non-nested target-action transport | sufficient finite-domain theorem | `causal_model/non_nested_conservative_transport.py` | `tests/test_non_nested_conservative_transport.py` |
| `EXT-4` | non-nested newly-legal-word split | local obstruction | `causal_model/non_nested_portability.py` | `tests/test_non_nested_portability.py` |
| `ID-1` | delayed exposure / finite-evidence no-go | no-go theorem | `causal_model/adaptive_closure_no_go.py` | `tests/test_adaptive_closure_no_go.py` |
| `ID-2` | candidate-universal macro law | exact finite theorem | `causal_model/candidate_safe_laws.py` | `tests/test_candidate_safe_laws.py` |
| `ID-3` | joint exterior--mechanism bound | lower-bound obstruction | `causal_model/joint_open_candidate_laws.py` | `tests/test_joint_open_candidate_laws.py` |
| `LEGACY-1` | conditional experimental-design shelf | frozen conditional design theorems | `docs/legacy/README.md` | listed legacy regressions |

## Portability core v1

### `CORE-0` — finite closure classification

Classifies a declared finite deterministic map as closing, recurrent, or
multistable. It is a prerequisite about a supplied mathematical system, not a
claim that observed ecological dynamics converge.

### `CORE-1` — exact grammar-aware dynamic interface

Defines the exact finite quotient for a supplied system and action grammar. This
is the core abstraction step: output, legal-action rows, and legal successors
must all factor through one summary.

### `CORE-2` — addressability and extension--compression obstruction

When exterior coordinates are jointly realizable and individually decodable under
the declared grammar, an exact open interface must retain their information. The
result is a lower bound conditional on operational separation, not a slogan that
all larger systems need more memory.

### `CORE-3` — relay-tree sharpness witness

Provides the bounded-degree, constant-local-grammar realization attaining the
binary equality case. It calibrates the lower bound; it does not classify arbitrary
local interaction networks.

### `CORE-4` — nested portability ladder

Separates three conclusions that should never be conflated: bounded interface
size, one coherent portable law, and a conservative macro schema under legal-action
growth.

### `CORE-5` — fiber-split obstruction

A later legal word or action can refute one proposed merge if it separates two
states in that fiber. It is local and does not rule out every other macro-law.

## Selected non-nested replacement extension

### `EXT-1` — edge preservation with supplied projections

A declared relation can replace an embedding when both ends already realize the
same exact law and the relation preserves the required structure.

### `EXT-2` — target factorization transported from source

Target labels need not be supplied in advance. They are derived from source labels
when the replacement relation is total, target-fiber label-consistent,
output/equal-legality preserving, and successor-closed.

### `EXT-3` — conservative target-only actions

A target may add an action without breaking portability only when that action has
uniform availability and one macro successor within every derived target fiber.
The resulting certificate constructs one conservative macro schema.

### `EXT-4` — newly-legal-word split after replacement

When the new action or word varies within a proposed carried fiber, it refutes the
merge. This is the negative boundary of `EXT-3`.

## Identifiability companion

### `ID-1` — delayed exposure no-go

A finite observation transcript can remain compatible with a later separating
completion. This is why closure requires an independently declared horizon and
boundary grammar.

### `ID-2` — candidate-universal macro law

A retained candidate family has one deterministic macro law exactly when all
candidate-induced macro maps agree on all declared actions.

### `ID-3` — joint exterior--mechanism bound

Exterior uncertainty and mechanism uncertainty combine only under an explicitly
supplied joint realization and separation premise.

## Legacy shelf

### `LEGACY-1` — conditional experimental-design results

The legacy shelf remains executable but frozen. It concerns design, coverage,
robustness, and failure contracts after a structural interface has already been
fixed. It must not be used to establish closure or portability itself.

## Scope discipline

Every registry entry has an explicit non-claim. That is intentional: in this
repository, the shortest route to a theorem is not a wider narrative but a
well-specified finite domain, a certificate, a regression route, and a clear
statement of what remains `UNRESOLVED`.
