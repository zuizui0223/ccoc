# Anytime symbolic outer-envelope stability

## Aim

The static symbolic outer-envelope theorem asks whether one inner retained set is
contained in one outer retained set. This extension allows both retained sets to
change as information accumulates:

\[
C^{\mathrm{inner}}_{r,t}
\subseteq
C^{\mathrm{outer}}_{r,t}
\qquad
\text{for every required cell }r\text{ and certified look }t.
\]

An analyst may repeatedly inspect the inner/outer classifications and stop when
a desired outer conclusion appears. RACH permits this only under three
simultaneous-over-time certificates.

## Fixed sequential target

Every look must share one `AnytimeSymbolicExtensionTarget`:

```text
same inner tier ID
same outer tier ID
same symbolic candidate space and motif vocabulary
same ordered required cells
```

The candidate sets themselves may change across looks, but the formal inference
target cannot drift after inspection. A changed motif predicate, required cell,
or inner/outer tier identity needs a new certificate target.

## Three all-look obligations

For the true candidate \(\theta^\star\), let \(\mathcal T\) be either all
positive integer looks or one predeclared finite schedule.

### 1. Outer statistical coverage

\[
P\left[
  \forall t\in\mathcal T,\;
  \theta^\star\in\bigcap_{r\in\mathcal R}
  C^{\mathrm{outer}}_{r,t}
\right]
\ge 1-\alpha.
\]

This is supplied by an external confidence-sequence or jointly valid
finite-look method.

### 2. Outer decisive solver semantics

Every SAT/UNSAT certificate used to make an outer decisive RACH conclusion has
its advertised meaning over all required cells, motifs, and certified looks with
probability at least \(1-\beta\).

### 3. Inner-to-outer inclusion validity

\[
P\left[
  \forall t\in\mathcal T,\forall r\in\mathcal R:\
  C^{\mathrm{inner}}_{r,t}\subseteq C^{\mathrm{outer}}_{r,t}
\right]
\ge 1-\gamma.
\]

A deterministic proof-carrying inclusion verifier may set \(\gamma=0\). A
numerical search that merely fails to find a counterexample is not such a proof.
It must provide an explicit nonzero error guarantee or leave stability
unsupported.

## Theorem

Under the three all-look obligations,

\[
P\left[
  \begin{array}{l}
  \text{any false decisive outer INVARIANT or EXCLUDED conclusion, or}\\
  \text{any invalid extension-stability claim, at any }t\in\mathcal T
  \end{array}
\right]
\le \min(1,\alpha+\beta+\gamma).
\]

The same bound holds for any data-dependent stopping time \(\tau\) whose value
lies in \(\mathcal T\):

\[
P\left[
  \text{false decisive outer conclusion or invalid extension-stability claim at }
  \tau
\right]
\le \min(1,\alpha+\beta+\gamma).
\]

No independence is assumed between the three failures.

### Proof

Let \(E\) be the all-look outer retention event, \(S\) the all-look outer
solver-validity event, and \(I\) the all-look inclusion event. On
\(E\cap S\), the existing anytime symbolic theorem rules out every false
outer decisive conclusion. On \(I\), the deterministic outer-envelope
monotonicity theorem validates every `EXTENSION_STABLE` label produced from the
inner/outer relation.

Hence any false decisive outer conclusion or invalid stability label is contained
in

\[
E^c\cup S^c\cup I^c.
\]

A union bound yields \(\alpha+\beta+\gamma\). A stopping-time claim is a
subset of the union over all certified looks.

## Status discipline

At every look, the static extension audit can return:

```text
EXTENSION_STABLE  outer decisive status matches the inner status
SCOPE_FRAGILE     inner decisive status becomes outer UNRESOLVED
NONDECISIVE       both tiers remain unresolved
UNSUPPORTED       missing inclusion proof, unsupported symbolic query, or contradiction
```

An ordinary outer conclusion does not require an inclusion certificate. But it
cannot be promoted to `EXTENSION_STABLE` without an all-look certificate that
covers that specific look.

A finite inclusion schedule combined with all-look coverage and all-look solver
validity yields only a finite-schedule guarantee. The code rejects a later
uncovered look rather than silently extending the claim.

## Relation to prior layers

| Layer | Candidate space | Sequential? | Inclusion risk |
|---|---|---:|---:|
| Nested finite universe audit | finite explicit | no | exact set inclusion |
| Symbolic outer-envelope stability | arbitrary symbolic | no | \(\gamma\) |
| Anytime symbolic lifting | arbitrary symbolic | yes | none |
| **Anytime symbolic outer-envelope stability** | arbitrary symbolic | yes | \(\gamma\) |

With a single look this reduces to symbolic outer-envelope stability. With
\(\gamma=0\) and no inner/outer comparison it reduces to the anytime symbolic
soundness setting. When both outer solver verification and inclusion verification
are proof-carrying, \(\beta=\gamma=0\), leaving only the outer coverage error
\(\alpha\).

## API

| Object | API |
|---|---|
| Fixed all-look inner/outer target | `AnytimeSymbolicExtensionTarget` |
| Inner/outer tiers at one look | `SequentialSymbolicUniverseExtensionSnapshot` |
| Joint all-look inclusion assertion | `AnytimeJointSymbolicInclusionCertificate` |
| Per-look extension audits | `audit_anytime_symbolic_universe_extension` |
| Pointwise theorem witness | `deterministic_anytime_symbolic_extension_stability_witness` |
| Optional-stopping-safe bound | `anytime_symbolic_extension_stability_guarantee` |
