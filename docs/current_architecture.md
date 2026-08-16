# Current CCOC architecture — 2026-08-16

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

## 3. Deterministic feedback — reduced active surface

Entrance:

`docs/feedback_portability_theorem_family_2026-08-15.md`

Claim-control audit:

`docs/feedback_novelty_audit_2026-08-16.md`

Only two feedback implementations remain active:

- `causal_model/feedback_gate_rank.py` — mechanism-specific feedback-cycle rank plus causal-arrow ablation;
- `causal_model/feedback_type_portability.py` — replication-independent five-state positive example.

The former PR #207/#208/#210 implementations were retired from the current tree because they are increasingly general fixed-grammar refinement variants of the same classical substrate. Their scientific conclusions are summarized in the consolidated feedback document and their full code/proofs remain at pre-cleanup audit pin

`4c7887c73ba8fa86a5e3883ebb6dce265b80fe7a`.

No deterministic persistent-mode feedback variant is an active development target.

## 4. Compatibility shelf

The broad package-root facade in `causal_model/__init__.py` remains temporarily because current repository examples/scripts still import older qualitative/panel names from the package root. No new theorem export should be added there.

The deprecated `causal_model/current_theory.py` aggregate has been retired from the current tree because no active repository code imported it; only its dedicated compatibility test and historical documentation referenced it. Its final implementation remains recoverable from the pre-cleanup Git pin.

Historical candidate-uncertainty, panel-design, benchmark, and observation-design branches are the next compatibility/reproducibility family to audit.

## 5. Claim/provenance controls

Keep as durable controls:

- theorem registry and verification scripts;
- paper-core replay;
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

A valid theorem is not automatically a reason to keep a dedicated module, test, document, and workflow indefinitely.

## 7. Current cleanup direction

The immediate goal is repository reduction, not theorem expansion and not manuscript growth inside CCOC.

After the feedback and `current_theory` cleanup, the next high-value pass is the old package-root / candidate-panel / benchmark surface: identify in-repository import consumers, retain one compatibility route where required, and retire duplicated implementations only after the surviving regression path is explicit.
