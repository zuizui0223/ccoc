# Research priorities and theorem freeze

## Decision

New theorem generation is paused until portability core v1 is consolidated and
its stop criteria are met. The repository has enough valid results; the current
risk is not lack of hypotheses but loss of a legible central claim.

## Priority 0 — consolidate, do not extend

**Goal:** turn existing portability results into one coherent theorem family.

Required work:

1. Make [portability core v1](portability_core_v1.md) the public structural
   entry point.
2. Present boundedness, coherent portability, and conservative grammar extension
   as levels of one portability ladder.
3. Demote relay trees to sharpness witnesses.
4. Separate delayed evidence and candidate uncertainty from the core structural
   narrative.
5. State every core conclusion as one of: exact theorem, sufficient criterion,
   lower-bound obstruction, sharp witness, or `UNRESOLVED` region.

**Forbidden during P0:** new special-case grammar theorem, new panel theorem,
new robustness theorem, new measurement protocol, or another witness family.

## Priority 1 — proof hygiene and public interface

**Goal:** make the repository say only what the proofs support.

Required work:

1. Rewrite README and theorem spine around the core/companion/shelf split.
2. Make the public theory entrance point to portability core modules only.
3. Audit claims for these distinctions:

   | Claim type | Required wording |
   |---|---|
   | Exact finite theorem | state domain and grammar explicitly |
   | Sufficient criterion | do not write “iff” without converse proof |
   | Lower bound | name the decoder/joint-realizability premise |
   | Sharpness witness | identify the family and the attained equality |
   | Evidence limitation | distinguish `UNRESOLVED` from impossibility of a law |

4. Freeze experimental-design branches as regression-only.

## Priority 2 — logical package boundaries

Keep one repository until P0/P1 are complete. Use this conceptual partition:

| Package | Question | Contents |
|---|---|---|
| `portability-core` | When does an exact macro-law survive declared composition changes? | blankets, addressability lower bound, conservative portability, sharp relay witness |
| `identifiability-companion` | What can finite evidence establish about closure or retained mechanisms? | delayed adaptive no-go, candidate-safe laws, joint uncertainty laws |
| `experimental-design-legacy` | How should a fixed quotient/contract be measured or protected? | reset panels, witnessed evidence, robustness, common-mode failure |

A physical repository split is deferred until imports and shared finite-model
utilities stabilize. Splitting now would preserve the current conceptual clutter
in multiple locations.

## Priority 3 — choose one next research direction only

After portability core v1 reaches its stop criteria, select **one** direction:

1. non-nested composition, replacement, and rewiring;
2. composition-dependent candidate mechanism families; or
3. noisy / approximate portability.

A new issue must state which canonical core claim it extends, why the existing
criterion does not cover it, and whether it belongs to core or companion work.

## Stop rule

Do not start a new theorem branch merely because a new edge case exists. Start
one only if it changes one of these canonical statements:

\[
\text{exact factorization},
\quad
\text{addressability obstruction},
\quad
\text{conservative portability},
\quad
\text{or finite-evidence identifiability}.
\]

Otherwise record the case as a limitation, example, or legacy regression.

## Completion signal for portability core v1

The core is ready to stop expanding when:

- the one-page core statement is stable;
- the theorem ladder has no duplicated headline result;
- README, theorem spine, and asset map agree;
- companion and legacy branches are visibly separated;
- unresolved cases are listed rather than immediately converted into new theorem
  targets.

The governing issue is [#84](https://github.com/zuizui0223/rach-causal-invariants/issues/84).