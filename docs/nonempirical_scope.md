# Non-empirical scope for CCOC

## What this repository is

CCOC is a **theorem-first mathematical ecology** repository for finite structural questions about exact causal compression under declared future grammars.

Its current publication-facing scope is:

- finite controlled systems and declared legal future grammars;
- exact response interfaces and their quotient size;
- cross-grammar lower bounds for interface inflation when future actions become legal;
- bounded-local sharpness witnesses and portability/forced-split boundaries; and
- executable certificates and provenance that support, but do not replace, the analytic proofs.

CCOC is **not an inference or identification method**. It does not rank uncertain mechanism hypotheses, quantify posterior or admissible-set uncertainty, select the next observation, or infer latent channel decompositions from data. Those are separate inferential problems.

The repository is also **not empirical**. A passing certificate verifies consistency of an explicitly supplied finite model; it does not validate an observed ecosystem.

## What must not be committed here

Do not add:

1. field observations, occurrence records, monitoring data, images, audio, or specimen measurements as evidence for a CCOC theorem;
2. fitted parameters, statistical estimates, trained models, or predictions from ecological observations as though they established the finite theorem premises;
3. mechanism-ranking, residual-entropy, next-observation, proxy-identification, or calibration-transport methods whose scientific target is epistemic uncertainty rather than exact representation; or
4. claims that a real population, community, food web, landscape, or habitat has been certified by a CCOC theorem without an independently justified model contract.

Synthetic finite transition tables, grammars, counterexamples, and deterministic replay artifacts are allowed because they are mathematical witnesses, not empirical data.

## How ecology enters legitimately

An ecological application may begin in a separate application repository or manuscript with an independently justified **model contract**:

\[
(\text{finite state space},\ \text{controlled transition rule},\ \text{focal output},\
\text{legal future grammar},\ \text{interpretation map}).
\]

Only after that contract is fixed may a CCOC theorem be applied to the declared model. The application must keep three statements separate:

1. why the model contract is scientifically defensible;
2. which CCOC theorem or certificate is evaluated on that contract; and
3. which ecological interpretation, if any, follows from the result.

CCOC establishes item 2 conditional on item 1. It does not infer item 1 from data.

## Program boundary

CCOC answers a **representation question**:

> Given a fully declared finite controlled system, how much state information must an exact response interface retain under a specified grammar of legal futures, and how can that requirement change when the grammar is opened?

This is distinct from two nearby inferential questions:

- **mechanism uncertainty / observation design**: which causal hypotheses remain compatible with evidence, and which observation would reduce that uncertainty;
- **channel identification**: whether latent multiplicative channels are point-, partially-, or non-identified from a declared observation class and calibration assumptions.

The current CCOC manuscript does not depend on either inferential programme. Historical files may retain older RACH terminology when documenting repository ancestry; current-facing files must use CCOC for the present repository and theorem programme.

## Review gate

A pull request belongs in this repository only if it changes or verifies one of:

- a finite theorem, lower bound, sharpness witness, no-go result, or local obstruction within the CCOC representation contract;
- a certificate, regression, replay, or documentation needed to retrieve such a result; or
- repository infrastructure that preserves theorem provenance and the current CCOC identity.

When a proposed contribution instead concerns empirical inference, observation selection, proxy calibration, or data-derived mechanism claims, place it in the repository that owns that inferential task and link only the abstract model contract here when needed.

## Relation to the theorem registry

The canonical retrieval map is [theorem registry](theorem_registry.md). Each registry record states its finite domain, assumptions, conclusion, code path, regression route, non-claim, and permitted mathematical-ecology interpretation.
