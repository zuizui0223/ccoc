# Tier-aware certificate manifest v2

## Why v2 exists

Manifest v1 keys a solver proof by

```text
(look, cell, motif, role)
```

That is sufficient for a single retained set. It is not sufficient for the
compiler-admitted outer-envelope path, which has both

\[
C^{\mathrm{inner}}_t\cap\Theta
\quad\text{and}\quad
C^{\mathrm{outer}}\cap\Theta.
\]

At one look, the inner and outer proof families can legitimately have the same
cell, motif, and role while referring to different retained systems and different
compiled branch plans. Binding both to one tierless key would overwrite one
family or conflate their semantics.

Manifest v2 therefore uses the explicit key

```text
(tier, look, cell, motif, role)
```

where `tier` is exactly `inner` or `outer`.

## V2 structure

`TieredCertificateManifest` retains the v1 components:

- `ManifestTarget`;
- time-uniform coverage assertion;
- time-uniform solver-semantic-validity assertion.

It adds:

- one fixed `semantic_partition_artifact`, committing the tagged polyhedral
  candidate union used by the compiler;
- `TieredQueryPlanBinding` entries, keyed by
  \((\mathrm{tier},\mathrm{look},\mathrm{cell})\); and
- `TieredSolverQueryProofBinding` entries, keyed by
  \((\mathrm{tier},\mathrm{look},\mathrm{cell},\mathrm{motif},\mathrm{role})\).

Every decisive proof binding contains its query-plan artifact and must match the
unique plan binding at the same tier, look, and cell exactly. Thus a proof
artifact cannot be moved from an inner compiled plan to an outer plan, or from
one look/cell to another, without invalidating the manifest.

The v2 artifact registry contains the target and assertion artifacts, fixed
semantic partition, every tiered plan, and every decisive role-proof artifact.
It rejects reuse of one human-readable artifact ID with different SHA-256 or
media-type commitments.

## Canonical bytes and strict parsing

V2 has independent byte identifiers:

```text
rach-certificate-manifest/v2
rach-canonical-tiered-manifest-json/v2
```

The canonical serializer sorts plan bindings by

```text
(tier, look, cell)
```

and proof bindings by

```text
(tier, look, cell, motif, role).
```

The strict parser rejects duplicate JSON keys, unknown or missing fields,
noncanonical whitespace/key order, malformed tier values, malformed statuses,
and syntactically valid bytes that do not reproduce the unique canonical v2
serialization.

V1 canonical JSON remains completely unchanged. No v1 digest, existing transcript
entry, or signed checkpoint is reinterpreted under v2.

## Explicit migration boundary

A v1 manifest has no tier coordinate. It therefore cannot be mechanically
upgraded into a truthful two-tier manifest.

`migrate_v1_manifest_to_explicit_single_tier_v2` requires all of the following:

1. an explicit `QueryTier.INNER` **or** `QueryTier.OUTER` chosen by the caller;
2. an explicit semantic-partition artifact; and
3. one explicit v2 query-plan binding for every v1 proof's look/cell.

The function migrates v1 proof artifacts into the chosen single tier only. It
never duplicates a v1 proof into both inner and outer tiers, never infers a
partition, and never fabricates plan artifacts. To bind both tiers, construct a
native v2 manifest from the two actual compiler-admitted proof families.

## Relation to #25 transcript evidence

The compiler transcript adapter remains useful: it records all branch-proof
families in the append-only history and works with already-signed v1 manifests.
Manifest v2 supplies the missing first-class tier coordinate for new manifests.
A later integration can make the #25 adapter emit a native v2 manifest alongside
each transcript checkpoint, but v2 deliberately does not rewrite old evidence.

## Guarantees and limits

V2 strengthens identity binding. It does not by itself:

- replay opaque proof artifacts;
- prove the tagged partition represents nature;
- establish external statistical all-look coverage;
- prove every inspected look was recorded; or
- replace signed checkpoints, timestamps, or transparency logs.

The exact all-look theorem remains conditional on the same coverage, admission,
compiler, and trusted-verifier obligations. V2 makes the inner/outer proof
artifacts that discharge those obligations harder to conflate or transplant.

## API

| Task | API |
|---|---|
| Tier identifier | `QueryTier` |
| Bind one tier/look/cell plan | `TieredQueryPlanBinding` |
| Bind one tiered role proof | `TieredSolverQueryProofBinding` |
| Construct v2 manifest | `build_anytime_tiered_symbolic_manifest` |
| Verify context / artifact bytes | `verify_anytime_tiered_symbolic_manifest` |
| Explicit v1 single-tier migration | `migrate_v1_manifest_to_explicit_single_tier_v2` |
| Strict canonical v2 serialization | `canonical_tiered_manifest_json`, `canonical_tiered_manifest_digest` |
| Strict canonical v2 parsing | `parse_canonical_tiered_manifest` |
