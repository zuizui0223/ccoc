# CCOC hypothesis recovery — deferred candidates and branch-only audit (2026-08-14)

> **Purpose:** recover scientifically meaningful questions that survived only as deferred strengthening notes or branch names. This is not a novelty audit.

## Additional recovered hypotheses

| Recovery ID | Original question | Recovered status | Source | Relation to current theory |
|---|---|---|---|---|
| `REC-40` | Can the delayed-addressability witness compile not only the reader/probe path but also the **delay gate itself** into an autonomous bounded-local clock/mechanism with fixed local resources? | **DEFERRED / NOT PROVED.** The existing theorem represents the delay by an explicit prefix-grammar automaton and explicitly names autonomous local-clock compilation as a separate strengthening. | `docs/delayed_addressability.md` | Later local relay and stochastic ecological results do not supply this exact deterministic local delay-gate compiler. |
| `REC-41` | May robust-admissibility logic report an invariant/excluded motif from a required analysis cell with no accepted candidate because universal quantification is vacuously true? | **REFUTED BY THE INFERENCE CONTRACT.** Empty required accepted sets are `UNSUPPORTED`; optional cells alone cannot carry the cross-cell universal claim. | `docs/robust_admissibility.md`, early admissibility code | A non-vacuity/coverage premise, separate from observation-channel error and sampled-vs-exhaustive search calibration. |
| `REC-43` | Can the degree-three relay compiler support **simultaneous readers / multiple in-flight tokens** while retaining a finite local message grammar and exact macro semantics? | **DEFERRED / NOT PROVED.** The binary joint theorem is explicitly sequential and quiescent between macro actions; concurrent-token semantics remain outside the theorem. | `docs/binary_joint_relay_compilation.md`; PR #58 | Distinct from the multi-valued-register question in `REC-07`: even binary values would require a new concurrency/collision protocol. |

## Branch-only science audit

The repository retains many `agent/*` branches because GitHub write-safety workarounds often created `v2`, `ready`, `final`, or retry branches. Branch names alone are therefore not treated as lost hypotheses.

### Checked suspicious branch: `agent/cut-throughput-portability-v2`

- head: `29a54e59dd6aacb27ccd6ca6b02cfb2dcb4c5859`;
- commit message: `Prove retention-boundary-time tradeoff`;
- comparison with the merged-ready branch shows the same retention/boundary/time theorem lineage;
- its only unique source path relative to the ready branch is `causal_model/cut_throughput_portability.py`, whose complete content is one docstring line: `"""Cut-throughput portability theorem surface."""`.

**Recovery verdict:** no independent theorem or hypothesis is hidden there. The scientifically substantive result is already recovered as the merged retention–boundary–time tradeoff (`HYP-F02/F03`).

### Retry / ready branch classes that do not create new hypotheses

The following name families are treated as implementation/retry branches unless a content comparison shows otherwise:

- `grammar-aware-converse-v2/v2b/v2c/v3` — historical broad attempt plus corrected merged converse sequence already recovered as `HYP-E03`–`HYP-E06`;
- `stochastic-ecological-portability`, `-v2`, `-ready`, `-final`, `-clean` — one theorem-development lineage ending in merged PR #177;
- `terminal-grammar-portability` / `-ready` — same tested theorem head; draft #165 superseded by #166;
- `staged-materialization-prefix-v2` / `-ready` — same resource-theorem lineage;
- `retention-boundary-time-proof` / `-ready` / `cut-throughput-portability-v2` — same retention/boundary/time target, with the cut-throughput branch containing only the empty stub noted above;
- manuscript/source-acquisition `ready` branches — project-control retries, not science hypotheses.

## Branch-audit rule

A residual branch becomes a recovery row only if it contains at least one of:

1. a distinct scientific proposition not present on main;
2. a counterexample that changes a proposition's status;
3. a genuinely different model/domain/grammar contract;
4. a deferred scientific target explicitly named in substantive code/docs.

A branch created only to bypass a write gate, duplicate a tested head, hold an empty module stub, or synchronize docs does not count as a separate hypothesis.

## Current branch-only conclusion

After the suspicious-branch check and the previously completed closed-unmerged-PR audit, no additional branch-only active scientific hypothesis has been found beyond the recovered rows. `REC-40`, `REC-41`, and `REC-43` come from substantive published scope/inference notes, not from dangling branch names.