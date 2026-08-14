# CCOC core-surface cleanup manifest — 2026-08-14

> **Purpose:** separate scientific conclusions that must survive from implementation/infrastructure that can be removed now, and from compatibility material whose physical deletion must wait.

## KEEP — scientific/theorem sources

### First-paper core

Keep the historical CORE/replay source set:

- `causal_model/dynamic_boundary_blankets.py`
- `causal_model/shared_grammar.py`
- `causal_model/grammar_aware_blankets.py`
- `causal_model/extension_compression_noncommutation.py`
- `causal_model/operational_addressability.py`
- `causal_model/extension_compression.py`
- `causal_model/relay_tree_compilation.py`
- `causal_model/coherent_portable_macrolaw.py`
- `causal_model/conservative_macro_schema.py`

Keep the current extremal strengthening:

- `causal_model/fixed_regular_grammar_relay.py`
- `causal_model/extremal_open_composition.py`
- `docs/fixed_regular_extremal_theorem_2026-08-13.md`

### Established follow-up theorem surfaces

Keep explicitly, but do not pull them into the first-paper dependency graph:

- `action_grammar_closure.py`
- `grammar_expansion_closure.py`
- `grammar_interface_reuse.py`
- `terminal_grammar_portability.py`
- `portability_adaptation_tradeoff.py`
- deterministic ecological saturation/capacity/depletion modules
- stochastic ecological portability/mortality/finite-horizon modules
- `cross_guild_stochastic_coupling.py`
- `spatial_dispersal_reachability.py`

### Claim/provenance control

Keep:

- theorem registry and verification scripts;
- paper-core replay script;
- current architecture/research priorities;
- H1--H4 source audit/request packet/issues;
- manuscript transfer manifest;
- `mechanism_to_data_bridge_2026-08-14.md` as the application/falsification contract for established ecological parameters.

These are part of scientific claim control, not disposable project notes.

## KEEP FOR COMPATIBILITY — do not use for new research

### `causal_model/current_theory.py`

Already deprecated and clearly marked as a historical aggregate. Keep until an immutable manuscript source release because historical replay/notebooks may still import it.

### `causal_model/__init__.py`

The package-root facade is scientifically stale relative to the CCOC theorem hierarchy, but repository examples/scripts still import its older qualitative-program/robustness names directly. Removing or radically shrinking it now would be an API break, not dead-code deletion.

Rule: no new theorem exports should be added here. Migrate consumers first; remove only in a deliberate major-version cleanup.

### Historical examples/benchmarks/panel code

Retain for reproducibility until the manuscript pin is frozen. Their scientific role is legacy/companion, but some remain executable import consumers.

## REMOVE NOW

### `.github/workflows/ci.yml`

Removed by PR #194. It duplicated the generic Python 3.10/3.11/3.12 full pytest matrix already supplied by `.github/workflows/tests.yml` while adding no distinct theorem/provenance gate. `tests.yml` additionally compiles the package before pytest.

This was infrastructure duplication, not scientific evidence.

## SPECIALIZED WORKFLOW AUDIT

Do **not** infer that theorem-named workflows are duplicates of `tests.yml`.

The generic pytest configuration uses

```text
-m 'not legacy'
```

so archived/legacy theorem tests are intentionally excluded from the generic full suite.

First audit findings:

- `.github/workflows/adaptive-closure-no-go.yml` — **KEEP**. Runs a focused theorem regression, writes a deterministic JSON replay report, and uploads it as an artifact.
- `.github/workflows/common-mode-canonical-panels.yml` — **KEEP/DEFER**. Replays several theorem layers separately and writes/uploads a deterministic certificate report.
- `.github/workflows/approximate-addressability.yml` — **KEEP**. It explicitly executes `-m legacy` tests that the generic suite excludes, so it is not redundant even though it does not upload a report.

Therefore bulk workflow pruning is not justified. Future workflow deletion requires a file-specific showing that the workflow supplies neither:

1. a legacy test gate excluded from generic pytest;
2. a deterministic verifier/report artifact;
3. a frozen manuscript/release replay contract.

## DEFER

### Remaining specialized theorem workflows

Audit one by one only when cleanup value justifies it. Default disposition is **DEFER**, not delete.

### Physical move to `causal_model.legacy`

Defer until:

1. first-paper manuscript source SHA is immutable;
2. theorem registry + paper-core + full tests replay green on that SHA;
3. compatibility imports are either migrated or deliberately version-broken;
4. legacy path mapping is preserved in a release manifest.

## Scientific conclusions that cleanup must never erase

1. closed exact compression does not imply a comparably small exact interface after grammar opening;
2. the fixed-regular one-action family has `|P_C|=2`, `|P_O|=2^(m+1)`, and exact innovation `m` under bounded local resources;
3. broad same-domain grammar mutation need not monotonically refine the canonical quotient; reuse has its own iff criterion;
4. chain/resource portability has terminal-memory, adaptation-information, boundary-time, and staged-deadline distinctions;
5. ecological finite blankets arise from explicit future-invariance/reachability structure, not small physical boundaries alone;
6. stochastic exact complexity and finite-horizon approximate portability can diverge sharply;
7. hidden cross-guild kernel variation and directed reachability provide mechanistic portability boundaries;
8. historical firstness of the bounded-local realization remains conditional on the H1--H4 primary-source compiler audit.

## Next cleanup action

Do not spend more time pruning specialized workflows unless a concrete redundancy is found. The higher-value remaining cleanup is to migrate old package-root import consumers before any future major-version API reduction, and to perform the physical legacy move only after the manuscript source pin is immutable.
