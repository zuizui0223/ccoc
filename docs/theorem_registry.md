# RACH theorem registry: publication core and legacy archive

The canonical machine-readable record is
[`theorem_registry.json`](theorem_registry.json). CI verifies that every record
has a finite domain, assumptions, conclusion, source path, regression route,
documentation path, and an explicit non-claim.

RACH is a **mathematical ecology** repository, not an empirical data repository.
Read [the non-empirical scope policy](nonempirical_scope.md) before connecting a
finite theorem to an ecological application.

## Reading rule

The registry is complete provenance, not a claim that all entries belong to the
current paper. The open-composition manuscript uses only the **publication core**
below. All other entries are retained in the [legacy shelf](../legacy/README.md).

A passing regression validates the supplied finite certificate only. It does not
validate an observed ecosystem or infer the correct boundary grammar from data.

## Publication core

| ID | Manuscript role | Status | Primary source |
|---|---|---|---|
| `CORE-1` | exact grammar-aware dynamic interface | exact finite theorem | `causal_model/grammar_aware_blankets.py` |
| `CORE-2` | addressability and extension--compression lower bound | lower-bound obstruction | `causal_model/extension_compression_noncommutation.py` |
| `CORE-3` | binary relay sharpness realization | sharpness witness | `causal_model/relay_tree_compilation.py` |
| `CORE-4` | conservative macro-schema portability boundary | sufficient criterion | `causal_model/conservative_macro_schema.py` |
| `CORE-5` | future-word / new-action fiber split | local obstruction | `causal_model/conservative_macro_schema.py` |

### `CORE-1` — exact grammar-aware dynamic interface

For a supplied finite controlled system and action grammar, an exact interface
preserves output, legal-action rows, and successor labels. The grammar-aware
legal-word quotient is the coarsest such interface.

### `CORE-2` — addressability and extension--compression obstruction

When exterior coordinates are jointly realizable and uniformly decodable under
the declared open grammar, every exact open interface must retain their product
information. Closed-context factorizations supply the comparison upper bounds.
The result is conditional on operational separation; it does not say that every
larger system needs more memory.

### `CORE-3` — relay-tree sharpness witness

A binary relay family attains the equality case with a constant-size local
node/message grammar, pairwise messages, and maximum degree three. It is a
sharpness construction, not a classification of arbitrary local networks.

### `CORE-4` — conservative macro schema

A finite macro schema is portable through declared legal-action growth when old
meanings are preserved and every newly available action has uniform availability
and one macro successor within each macro fiber. This is sufficient, not
necessary.

### `CORE-5` — fiber-split obstruction

A later legal word or newly legal action refutes one proposed merge if it
separates two states inside that fiber. This local obstruction does not rule out
every alternative macro-law.

## Legacy archive

| ID | Archived branch | Why retained |
|---|---|---|
| `CORE-0` | finite closure classification | prerequisite for selected finite maps, outside the manuscript theorem |
| `EXT-1` | non-nested edge preservation | later replacement / rewiring extension |
| `EXT-2` | transported target exact factorization | later replacement / rewiring extension |
| `EXT-3` | conservative non-nested target-action transport | later replacement / rewiring extension |
| `EXT-4` | non-nested newly-legal-word split | later replacement / rewiring extension |
| `ID-1` | delayed exposure / finite-evidence no-go | companion on what monitoring can establish |
| `ID-2` | candidate-universal macro law | companion on mechanism uncertainty |
| `ID-3` | joint exterior--mechanism bound | companion on combined uncertainty |
| `LEGACY-1` | conditional experimental-design shelf | post-quotient design and failure contracts |

The archive may be replayed explicitly, but it is not part of the manuscript's
proof package. See [legacy manifest](../legacy/manifest.md) for source paths,
compatibility rules, and the planned later physical move.

## Registry IDs required by provenance checks

The following identifiers remain intentionally discoverable:
`CORE-0`, `CORE-1`, `CORE-2`, `CORE-3`, `CORE-4`, `CORE-5`, `EXT-1`, `EXT-2`,
`EXT-3`, `EXT-4`, `ID-1`, `ID-2`, `ID-3`, and `LEGACY-1`.
