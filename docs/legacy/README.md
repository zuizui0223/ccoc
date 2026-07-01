# Legacy shelf: derived design and evidence branches

These modules are retained as executable finite results, but they are **not part
of the active RACH theorem spine** and must not receive new feature work unless a
later core theorem explicitly needs them.

They answer conditional design questions *after* an exact finite boundary
quotient, coverage contract, reset contract, or failure model has already been
fixed. They do not establish exterior closure, extension-stable compression, or
a portable ecological macro-law.

| Frozen branch | Retained files | Why retained | Why not active |
|---|---|---|---|
| Budgeted delayed joint quotients | `delayed_joint_budgeted_quotients.py`, its test, replay, workflow, and document | exact partial-identification ladder for a reset-panel contract | depends on a predeclared reset and budget protocol; it is not a structural open-system theorem |
| Witnessed boundary evidence | `witnessed_boundary_evidence.py`, companions | makes clear that finite evidence gives lower bounds without coverage | evidence bookkeeping, not a new closure or compression result |
| Robust canonical panels | `robust_canonical_panels.py`, companions | exact cell-loss robustness after a canonical panel is fixed | observation design after the quotient, not quotient theory |
| Common-mode canonical panels | `common_mode_canonical_panels.py`, companions | corrects false independence of within-site replication | field failure architecture, not a theorem about open causal composition |

## Rules

1. Keep their tests and deterministic replays passing.
2. Do not re-export them from `causal_model.current_theory`.
3. Do not use their terminology as a headline claim in the README, theorem spine,
   or future theorem targets.
4. A future promotion requires a precise dependency from an active theorem; a
   useful field-design story alone is not enough.

The historical source locations are deliberately preserved for reproducible old
certificates. This shelf is a freeze, not a claim that the results are false.