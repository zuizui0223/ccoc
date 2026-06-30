# All-look compiler-admitted polyhedral outer envelopes

## What this connects

There are two prior exact layers:

1. The monotone polyhedral admission schema proves, for every admitted look,

   \[
   C^{\mathrm{inner}}_t
   \subseteq
   C^{\mathrm{base}}
   \subseteq
   C^{\mathrm{outer}}.
   \]

2. The proof-carrying polyhedral motif compiler turns a retained polyhedron
   \(C\) into exact branch queries over one fixed tagged candidate union

   \[
   \Theta=\bigcup_j U_j.
   \]

This module combines them. It is the first all-look RACH path in which the
active / inactive motif complement is compiler-generated rather than supplied as
three hand-written solver systems.

## Retained sets seen by RACH

The semantic retained set at a look is not the ambient polyhedron by itself. It
is

\[
R_t=C_t\cap\Theta.
\]

The fixed tagged union \(\Theta\) is held constant by the admission schema.
Therefore ordinary set monotonicity gives

\[
C^{\mathrm{inner}}_t\subseteq C^{\mathrm{outer}}
\quad\Longrightarrow\quad
C^{\mathrm{inner}}_t\cap\Theta
\subseteq
C^{\mathrm{outer}}\cap\Theta.
\]

No new solver search is needed for this implication. The existing exact
base-row-preserving inclusion admission proves the ambient inclusion, and
intersection with a fixed set preserves it.

## What a caller supplies at one look

For each required robustness cell and each tier, a caller supplies only:

```text
retained rational linear system C
one LinearFeasibilityProof per compiler-generated branch query ID
```

The caller does not supply an active or inactive linear system. The gate derives
the unique plan prefix from:

```text
fixed query namespace
inner or outer tier
look number
required cell ID
```

and compiles every branch

\[
C\cap U_j.
\]

The branch proof map must contain exactly those generated IDs. Its query systems,
roles, tag values, and variable order are reconstructed from the plan before
exact proof verification.

## All-look certificates

`verify_exact_compiled_polyhedral_extension_admission_schema` re-verifies the
tagged partition, verifies the base inner-to-outer inclusion, and emits:

```text
AnytimeSolverSemanticValidityCertificate(lower_bound=1.0)
AnytimeJointSymbolicInclusionCertificate(lower_bound=1.0)
```

for every positive integer look admitted through the gate.

The solver certificate means that every decisive branch result used by a claimed
look has an exact rational witness or Farkas proof, and active/inactive branch
families come only from the fixed tag partition.

The inclusion certificate means that the compiler-retained sets
\(C_t\cap\Theta\) are nested because the ambient retained polyhedra are nested
and \(\Theta\) is fixed.

With an external all-look coverage certificate of level \(1-\alpha\),

\[
P\left(
\exists t, m:
\text{ false decisive outer conclusion or invalid extension-stability claim}
\right)
\le \alpha
\]

across all compiler-admitted looks and any data-dependent stopping rule.

## Non-emptiness

The all-look gate requires an exact SAT branch for every inner and outer
retained union. A SAT witness for

\[
C\cap U_j
\]

is also a witness for ambient \(C\), so it supplies the exact witness needed by
the monotone inclusion admission layer. This excludes empty candidate-union
states from the exact-admitted path rather than deriving a decisive claim from
vacuous inclusion.

## Boundaries

The guarantee applies only when all of the following remain fixed and are used
as declared:

- the finite tagged rational polyhedral union \(\Theta\);
- the candidate-space and motif vocabulary;
- all conflict-separation proofs for differently tagged cells;
- the fixed outer ambient retained system;
- base-row-preserving inner retained updates; and
- the compiler admission gate for every claimed look.

The module does not prove that the declared union contains nature, infer the tag
semantics, establish statistical coverage, accept nonlinear/integer/disjunctive
constraints, or make a bypassed manual-query snapshot safe. It also does not yet
adapt the append-only transcript API; the next audit-layer extension can record
these compiler-admitted snapshots and bind their partition / plan artifacts into
the signed history.

## API

| Task | API |
|---|---|
| Declare fixed all-look compiler target | `ExactCompiledPolyhedralExtensionAdmissionSchema` |
| Verify target and obtain beta/gamma-zero certificates | `verify_exact_compiled_polyhedral_extension_admission_schema` |
| Derive the only accepted branch plan | `compiled_query_plan_for_admission` |
| Supply branch proofs at one look | `ExactCompiledPolyhedralProofCell`, `ExactCompiledPolyhedralExtensionLook` |
| Build one admitted paired snapshot | `admit_exact_compiled_polyhedral_extension_look` |
| Audit admitted snapshots | `audit_exact_compiled_polyhedral_extension_looks` |
| Obtain the optional-stopping guarantee | `exact_compiled_polyhedral_extension_guarantee` |
