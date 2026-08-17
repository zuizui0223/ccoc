# Current CCOC architecture — 2026-08-17

## Purpose

This file describes the **current tree**, not the full historical theorem archive. Git history preserves retired theorem experiments and proof notes.

## 1. Publication core

The narrow first-paper structural core remains:

1. exact grammar-aware response interfaces;
2. cross-grammar extension/compression obstruction;
3. bounded-local extremal witness;
4. conservative portability boundary;
5. local future-word/fiber-split obstruction.

Canonical modules:

- `causal_model/grammar_aware_blankets.py`
- `causal_model/extension_compression_noncommutation.py`
- `causal_model/relay_tree_compilation.py`
- `causal_model/coherent_portable_macrolaw.py`
- `causal_model/conservative_macro_schema.py`
- `causal_model/fixed_regular_grammar_relay.py`
- `causal_model/extremal_open_composition.py`

The strongest explicit family has

\[
|P_C|=2,
\qquad |P_O|=2^{m+1},
\qquad K_O-K_C=m,
\]

with one fixed four-symbol primitive alphabet, one newly legal primitive action, degree at most three, cut one, and logarithmic selected-coordinate access.

## 2. Active follow-up theorem surfaces

### Exact converse/reuse

- `action_grammar_closure.py`
- `grammar_expansion_closure.py`
- `grammar_interface_reuse.py`
- `terminal_grammar_portability.py`

### Resource layer

- `portability_adaptation_tradeoff.py`
- retained boundary-time / staged-exposure results

### Ecological structural layer

Keep explicit deterministic, stochastic, cross-guild, and spatial modules only where they state a distinct structural result rather than a relabeling of fixed-grammar minimization.

## 3. Deterministic feedback — historical only

CREST §11/§12 was applied on 2026-08-17.

Verdict:

- the general continuation-stable hidden repair is a fixed-initial-partition coarsest stable refinement and routes to **MLTR** if developed further;
- PR #204's feedback-cycle rank remains a historical future-addressability example but is redundant with the current CCOC lower-bound/sharpness core;
- PR #205's five-state copy-anonymous collapse remains a historical fixed-grammar positive example;
- no deterministic-feedback module or focused test remains active in the current tree.

Historical entrance:

- `docs/feedback_portability_theorem_family_2026-08-15.md`
- `docs/feedback_novelty_audit_2026-08-16.md`

Full pre-cleanup recovery pin:

`4c7887c73ba8fa86a5e3883ebb6dce265b80fe7a`.

The feedback family is not an active development target and is not part of the publication-core theorem hierarchy.

## 4. Compatibility shelf

The broad package-root facade in `causal_model/__init__.py` remains temporarily because current repository examples/scripts still import older qualitative/panel names from the package root. No new theorem export should be added there.

The deprecated `causal_model/current_theory.py` aggregate has been retired from the current tree because no active repository code imported it.

Historical candidate-uncertainty, panel-design, benchmark, and observation-design branches remain compatibility/cleanup targets.

## 5. Claim/provenance controls

Keep as durable controls:

- theorem registry and verification scripts;
- paper-core replay;
- CCOC–MLTR claim firewall;
- H1–H4 primary-source audit records;
- hypothesis-recovery pin/ledger;
- manuscript-transfer manifest;
- mechanism-to-data falsification contract.

Historical ledgers may mention source paths retired from the current tree. Such paths refer to the recorded historical commit, not to active modules.

## 6. Cleanup rule

For every remaining file, classify it as one of:

- **CURRENT** — needed by the publication core or a distinct active extension;
- **COMPATIBILITY** — still imported/replayed but not a research surface;
- **HISTORICAL** — scientific conclusion retained in records/Git history; source need not stay in the current tree;
- **REMOVE** — duplicated implementation, duplicated explanation, superseded experiment, or infrastructure without a distinct replay role.

A valid theorem or ecological example is not automatically a reason to keep a dedicated module, test, document, and workflow indefinitely.

## 7. Current cleanup direction

The immediate goal is repository reduction, not theorem expansion and not manuscript growth inside CCOC.

The feedback CREST pass establishes the stricter rule: once a family fails the program-level novelty/routing gate, representative executable examples are not retained merely for symmetry. Scientific conclusions stay in provenance records; active code must justify a current theorem role.