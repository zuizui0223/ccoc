# Non-empirical scope for mathematical ecology

## What this repository is

RACH is a **mathematical ecology** repository in the following restricted sense:

- it studies finite controlled systems, composition grammars, exact interfaces,
  addressability lower bounds, and evidence limits;
- ecological notions such as boundary, dispersal, replacement, interaction, and
  observation window may motivate the names of model components; and
- every theorem applies only to its declared finite mathematical object.

The repository is **not empirical**. A passing certificate verifies consistency of
an explicitly supplied finite model; it does not validate an observed ecosystem.

## What must not be committed here

Do not add:

1. field observations, occurrence records, monitoring data, images, audio, or
   specimen measurements;
2. fitted parameters, statistical estimates, trained models, or predictions from
   ecological observations;
3. claims that a real population, community, food web, landscape, or habitat has
   been certified by a RACH theorem; or
4. ecological case studies whose central contribution is data analysis rather than
   a finite theorem/certificate.

Synthetic finite transition tables, grammars, counterexamples, and deterministic
replay artifacts are allowed because they are mathematical witnesses, not data.

## How ecology enters legitimately

An ecological application may begin in a separate application repository or
manuscript with an independently justified **model contract**:

\[
(\text{finite state space},\ \text{outputs},\ \text{legal action grammar},\
\text{completion family},\ \text{interpretation map}).
\]

Only after that contract is fixed may a RACH result be cited as a theorem about
that declared model. The application must keep three statements separate:

1. why the contract is scientifically defensible;
2. which RACH certificate is evaluated on the contract; and
3. which ecological interpretation, if any, follows from the result.

RACH itself establishes only item 2.

## Review gate

A pull request belongs in this repository only if it changes or verifies one of:

- a finite theorem, lower bound, sharpness witness, no-go result, or local
  obstruction;
- a certificate, regression, replay, or documentation needed to retrieve such a
  result; or
- repository infrastructure that preserves theorem provenance.

When a proposed contribution contains empirical data or data-derived inference,
place it outside this repository and link only the abstract model contract here.

## Relation to the theorem registry

The canonical retrieval map is [theorem registry](theorem_registry.md). Each
registry record states its finite domain, assumptions, conclusion, code path,
regression route, non-claim, and permitted mathematical-ecology interpretation.
