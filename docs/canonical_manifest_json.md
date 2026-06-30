# Strict canonical manifest JSON v1

## Purpose

A RACH certificate manifest already hashes candidate-space, motif, coverage,
solver, and query-proof artifacts. To support persistent audit trails and future
signatures, a manifest also needs one unambiguous byte representation.

This module defines **strict canonical manifest JSON v1** for
`CertificateManifest`:

```text
CertificateManifest
  -> exact UTF-8 canonical bytes
  -> SHA-256 canonical_manifest_digest
```

It does not change the existing `manifest.manifest_digest`, which remains for
backward compatibility. The new canonical digest is the stable identity intended
for append-only transcripts and signature layers.

## Canonical byte rules

The serializer emits exactly one UTF-8 JSON byte sequence for a given manifest
contract:

- JSON object keys are lexicographically sorted.
- There is no insignificant whitespace or trailing newline.
- Non-ASCII characters are literal UTF-8, not optional `\\u` escape spellings.
- Manifest lower-bound probabilities use a one-field wrapper:

  ```json
  {"__float_hex__":"0x1.e666666666666p-1"}
  ```

  The hexadecimal spelling is the exact `float.hex()` value, so it preserves the
  binary value and rejects alternative numeric spellings such as `0.95`.
- Motif-definition maps are sorted by motif name.
- Solver query-proof bindings are sorted by
  `(look, cell_id, motif, role)` because the manifest contract already treats
  these bindings as uniquely keyed, not as an ordered proof history.
- Required-cell order and assumption order are preserved. Existing RACH theorem
  APIs treat those tuples as part of the declared target and assertion contract.

## Strict parsing

`parse_canonical_manifest` does more than call `json.loads`:

1. JSON object duplicate keys are rejected before construction.
2. Every object is checked against an exact field schema; unknown and missing
   fields are rejected.
3. JSON types are checked exactly. In particular, booleans cannot stand in for
   look integers, and lower bounds cannot use ordinary JSON numbers.
4. Query roles, SAT/UNSAT statuses, artifact digests, look IDs, and manifest
   invariants are revalidated through the ordinary dataclass constructors.
5. The decoded manifest is serialized again. The input bytes must equal the
   resulting canonical bytes exactly.

Thus pretty printing, key reordering, duplicate-field ambiguity, alternate
Unicode escapes, non-canonical hexadecimal floats, and a UTF-8 byte-order mark
are rejected even when ordinary JSON parsers would accept them.

## Canonical digest versus integrity commitment

A canonical digest proves byte identity of one manifest contract:

\[
\mathrm{digest}=\operatorname{SHA256}(\mathrm{canonical\_bytes}).
\]

It does not make content correct. A changed candidate-space artifact digest can
form a valid **different** canonical manifest. It is detected only when checked
against the expected digest recorded in a transcript, signature, registry, or
other trusted reference.

Likewise, artifact payload semantics remain outside the codec. The manifest
contains SHA-256 commitments to those bytes; `verify_manifest_artifacts` still
checks that supplied artifact payloads match those commitments.

## Scope boundary

The codec deliberately serializes only `CertificateManifest`. It does not define
a universal JSON proof language for Farkas multipliers, confidence sequences, or
arbitrary solver backends. Those are opaque artifact bytes under the current
manifest contract.

The codec provides no signatures, provenance, timestamp authority, append-only
storage, or guarantee that every real-world look was recorded. Those are the
next layers. Its contribution is a stable object that such layers can safely
hash and sign.

## API

| Object | API |
|---|---|
| JSON encoding version identifier | `CANONICAL_MANIFEST_JSON_FORMAT` |
| Canonical JSON-safe object | `canonical_manifest_object` |
| Exact canonical JSON text / bytes | `canonical_manifest_json`, `canonical_manifest_bytes` |
| Stable SHA-256 identity | `canonical_manifest_digest` |
| Serialized or parsed document | `CanonicalManifestDocument` |
| Strict parser | `parse_canonical_manifest` |
| Parser plus expected-digest verification | `verify_canonical_manifest` |
