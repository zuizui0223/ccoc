# Nested candidate-universe stability

## The unresolved assumption

Every RACH theorem is conditional on a declared candidate universe. Statistical
coverage can say that the true candidate is retained with high probability only
if a faithful candidate was present in the universe in the first place.

No finite workflow can prove that an arbitrary scientific mechanism was not
omitted. This module therefore does not label a sampled candidate grammar
"complete." It asks a narrower, auditable question:

> Which conclusions survive a predeclared expansion from a narrow candidate
> universe to a wider outer envelope?

## Nested retained universes

For each required robustness cell \(r\), let

\[
C_r^{(0)} \subseteq C_r^{(1)} \subseteq \cdots \subseteq C_r^{(K)}
\]

be non-empty retained candidate sets. A candidate shared by two tiers denotes
the same mechanism and must retain the same motif assignment. The final tier is
a declared **outer envelope**, not a claim to contain all mechanisms in nature.

The finite implementation checks these subset relations exactly. An arbitrary
symbolic extension may use an external inclusion certificate, but must not be
called exact unless that certificate is independently justified.

## Monotonicity theorem

For a Boolean motif \(m\), classify each tier across all required cells using
the ordinary RACH rules. Then, under the nested-set condition:

\[
\mathrm{INVARIANT}_{K}(m) \implies \mathrm{INVARIANT}_{0}(m),
\]

\[
\mathrm{EXCLUDED}_{K}(m) \implies \mathrm{EXCLUDED}_{0}(m),
\]

and

\[
\mathrm{UNRESOLVED}_{0}(m) \implies \mathrm{UNRESOLVED}_{K}(m).
\]

### Proof

If \(m\) is invariant in the outer tier, every candidate in every
\(C_r^{(K)}\) has \(m\). Since each inner retained set is a subset of the
outer set, every candidate in every \(C_r^{(0)}\) also has \(m\). The excluded
case is symmetric.

If the inner tier is unresolved, there are accepted inner candidates witnessing
both \(m=1\) and \(m=0\) across the required-cell classification. Both remain
in every outer superset, so no outer tier can make a universal positive or
negative claim.

The theorem is deterministic. It needs neither a data distribution nor a
sampling model.

## Extension-stable and scope-fragile conclusions

A motif is **extension-stable** when the outermost declared envelope reports
`INVARIANT` or `EXCLUDED`. The monotonicity theorem guarantees that the same
decisive result held at every narrower tier.

A motif is **scope-fragile** when a narrower tier reports a decisive result but
the outer envelope does not preserve that same status. A common example is:

```text
narrow universe:  every retained candidate has m        -> INVARIANT
outer envelope:   a new retained competitor lacks m     -> UNRESOLVED
```

The narrow conclusion is not thereby proven false. It is simply not robust to
the stated expansion, so RACH should report the outer-envelope status rather
than retaining the narrower decisive label.

## Relation to random-data soundness

The existing confidence-set lifting theorem applies to whichever candidate set
is treated as the inferential target. Thus, if the outer envelope has a valid
all-cell or all-look coverage certificate with failure probability \(\alpha\),
then decisive conclusions at that outer tier inherit the usual false-decisive
bound. With a symbolic solver validity error \(\beta\), the anytime symbolic
bound remains

\[
P(\text{any false decisive outer-envelope conclusion})
\le \min(1,\alpha+\beta).
\]

Nested-universe stability does not remove the candidate-coverage assumption. It
makes it testable over a declared sequence of broader approximations and gives a
principled reason to prefer outer-envelope conclusions.

## Scope boundary

The exact finite implementation requires each required retained set to be
non-empty. Empty sets are `UNSUPPORTED` in ordinary RACH, and vacuous universal
statements over an empty set must not be used to claim extension stability.

The module does not generate alternative mechanisms, estimate how likely an
omission is, or declare an outer envelope exhaustive. Those tasks require a
separate grammar-design or scientific-modeling argument.

## Code mapping

| Object | API |
|---|---|
| One finite nested universe tier | `FiniteUniverseTier` |
| Exact adjacent-tier inclusion audit | `UniverseExtensionTransition` |
| Full chain classification and stability report | `audit_nested_universe_stability` |
| Outermost stable conclusions | `extension_stable_motifs` |
| Narrow conclusions lost under expansion | `scope_fragile_motifs` |
