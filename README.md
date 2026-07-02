# RACH Causal Invariants

RACH is a theorem-first **mathematical ecology** repository about a finite causal question:

> When does a finite macro-law remain exact as the permitted outside of a focal window expands?

This repository contains finite mathematical models, certificates, lower bounds,
sharpness witnesses, and no-go results. It is **not empirical**: it contains no
field datasets, fitted ecological parameters, or claim that a passing certificate
validates an observed ecosystem.

## Start here

- [Theorem registry](docs/theorem_registry.md) — one retrieval ID for every public mathematical claim.
- [Non-empirical scope](docs/nonempirical_scope.md) — the data boundary and the correct role of ecology in a model contract.
- [Portability core v1](docs/portability_core_v1.md) — the frozen structural core.
- [Non-nested replacement portability](docs/non_nested_replacement_portability.md) — the selected extension, now frozen at finite deterministic N1–N3.
- [Claim-status audit](docs/claim_status_audit.md) — exact scope and non-claims.
- [Theorem spine](docs/theorem_spine.md) — core, extension, companion, and legacy relationships.
- [Research priorities](docs/research_priorities.md) — freeze rules and paused directions.
- [Legacy shelf](docs/legacy/README.md) — conditional design mathematics after a structural contract is fixed.

## Public imports

```python
import causal_model.portability_core as rach
import causal_model.identifiability_companion as rach_id
```

`causal_model.current_theory` is historical compatibility surface, not a public entrance for new work.

## The package in one page

### Core

A declared finite system and legal-action grammar admit an exact macro-interface
when output, legal actions, and successors factor through one update-consistent
summary. Conversely, independently addressable exterior factors impose an open
interface-memory lower bound. The relay tree is a sharpness witness.

### Replacement extension

For finite replacement without embeddings, a total transport can preserve a
supplied macro-law, construct a target exact projection from a source projection,
or transport a conservative schema when target-only actions are uniform within
all derived target fibers. A new action that splits a fiber refutes that proposed
merge locally.

### Companions

Finite evidence alone need not certify closure without a horizon and grammar
contract. A retained candidate family has one deterministic law only when its
induced macro maps agree. Experimental-design modules remain conditional legacy
results.

## Retrieval contract

Every public theory is recovered through its registry record:

1. finite domain and assumptions;
2. conclusion and explicit non-claim;
3. source module and certificate symbol;
4. regression or deterministic replay route; and
5. documentation path and ecological interpretation boundary.

Run the registry integrity check with:

```bash
python scripts/verify_theorem_registry.py --check --write-report
```

A passing check confirms that the repository links its theorem assets correctly.
It does not validate an ecological dataset or observed system.

## Scope boundary

Ecological mechanisms may motivate a separate finite model contract:

```text
finite state space + outputs + legal grammar + completion family + interpretation map
```

RACH proves only statements about that declared abstract object. Empirical data,
model fitting, and field inference belong outside this repository.