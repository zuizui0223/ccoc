# Symbolic outer-envelope stability

## Purpose

The finite nested-universe audit checks explicit candidate-set inclusion. This
module extends that audit to symbolic retained sets over continuous, mixed,
countably infinite, or uncountable candidate spaces.

It does **not** claim that an outer candidate envelope contains nature. It asks
auditably whether a conclusion survives a declared, solver-certified expansion:

\[
C^{\mathrm{inner}}_r \subseteq C^{\mathrm{outer}}_r
\qquad\text{for every required cell }r.
\]

An outer envelope is therefore an explicitly stated robustness target, not a
claim of exhaustive scientific mechanism coverage.

## Symbolic tiers

A `SymbolicUniverseTier` contains:

```text
one SymbolicCandidateSpace
one symbolic retained set per required cell
one fixed motif vocabulary
```

The inner and outer tiers must use the same candidate space, motif vocabulary,
and ordered required-cell IDs. Inclusion is **not** inferred from descriptions or
tier names. It is supplied by a `JointSymbolicInclusionCertificate` that covers
all required cells jointly.

For each cell, the inclusion query is conceptually

\[
C^{\mathrm{inner}}_r \cap \bigl(\Theta\setminus C^{\mathrm{outer}}_r\bigr)
=\varnothing.
\]

A SAT/SMT, interval, polyhedral, or other backend may prove that emptiness. The
present module records its joint validity guarantee; it does not implement the
search or proof verifier.

## Deterministic monotonicity

Assume every required inner retained set is contained in the corresponding outer
set. Then the ordinary symbolic RACH status is monotone:

\[
\mathrm{INVARIANT}_{\mathrm{outer}}(m)
\Rightarrow
\mathrm{INVARIANT}_{\mathrm{inner}}(m),
\]

\[
\mathrm{EXCLUDED}_{\mathrm{outer}}(m)
\Rightarrow
\mathrm{EXCLUDED}_{\mathrm{inner}}(m),
\]

and

\[
\mathrm{UNRESOLVED}_{\mathrm{inner}}(m)
\Rightarrow
\mathrm{UNRESOLVED}_{\mathrm{outer}}(m).
\]

The proof is pure set inclusion. An outer universal claim applies to every
inner candidate because every inner candidate is also outer. Conversely, inner
witnesses for both motif values remain witnesses in the outer superset.

## Audit statuses

For each motif, `audit_symbolic_universe_extension` reports one of:

```text
EXTENSION_STABLE
    outer status is INVARIANT or EXCLUDED and matches the inner status

SCOPE_FRAGILE
    inner is decisive but the outer envelope becomes UNRESOLVED

NONDECISIVE
    both tiers are unresolved

UNSUPPORTED
    no joint inclusion certificate, unsupported symbolic status, or a
    status pattern contradictory to the claimed inclusion
```

The `SCOPE_FRAGILE` label does not prove a narrow result false. It says the
result is not robust to the declared outer envelope, so the outer result should
be used for the broader claim.

## Statistical and solver-aware guarantee

Let:

- \(\alpha\) be the failure probability of a valid outer retained-set coverage
  certificate;
- \(\beta\) be the failure probability of the decisive outer solver semantics;
  and
- \(\gamma\) be the failure probability of the joint inclusion certificate.

Then, without assuming independence,

\[
P(\text{any false decisive outer conclusion}
  \ \lor\ 
  \text{any false extension-stability claim})
\le \min(1,\alpha+\beta+\gamma).
\]

The reason is a union bound over three global failure events: outer true-point
retention, outer solver semantics, and inner-to-outer inclusion validity. If
all three events hold, a false outer decisive conclusion is impossible by the
existing symbolic lifting theorem, and a false stability relation is impossible
by the deterministic inclusion theorem.

A deterministic proof-carrying outer solver and inclusion verifier may set
\(\beta=0\) and \(\gamma=0\), reducing the guarantee to the outer statistical
coverage error \(\alpha\).

## Critical boundary

An ordinary outer symbolic conclusion can exist without an inclusion certificate.
It must **not** be promoted to `EXTENSION_STABLE` in that case. The audit returns
`UNSUPPORTED` for stability because the required inner-to-outer relation has not
been established.

Likewise, a numerical optimizer failing to find a counterexample is not an
inclusion proof. It must be represented as a nonzero-\(\gamma\) external
validity statement or as no certificate at all.

## API mapping

| Mathematical object | API |
|---|---|
| Symbolic inner or outer retained-set tier | `SymbolicUniverseTier` |
| Joint inclusion assertion | `JointSymbolicInclusionCertificate` |
| Motif-wise stability result | `SymbolicExtensionMotifAudit` |
| Full expansion report | `audit_symbolic_universe_extension` |
| \(\alpha+\beta+\gamma\) soundness bound | `symbolic_extension_stability_guarantee` |
