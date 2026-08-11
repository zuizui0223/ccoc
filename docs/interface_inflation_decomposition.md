# Causal interface inflation decomposition

> **Status:** post-reopening theorem-family consolidation. The logarithmic
> partition identity is elementary bookkeeping; the purpose is to separate the
> static join/refinement contribution already latent in the closed grammars from
> genuinely new causal distinctions created only after additional future words
> become legal.

## 1. Three grammars, not one

Fix one finite comparison domain `D`.

For each closed context `j`, let

\[
\mathcal L_j
\]

be its exact response grammar and `P_j` its exact response quotient on `D`.

Define the **closed-union grammar**

\[
\mathcal L_U=\bigcup_j\mathcal L_j.
\]

Its exact quotient `P_U` is the common refinement of the `P_j`.

The actual open system may allow still more future words:

\[
\mathcal L_U\subseteq\mathcal L_O.
\]

Let `P_O` be the exact quotient under the full open grammar.

The distinction between `L_U` and `L_O` is crucial. Static projection/natural-join
reasoning can explain how much information is required merely to make all closed
views simultaneously available. It cannot by itself explain response distinctions
that no closed context ever made legal.

## 2. Shared-base capacity term

Assume the closed quotients refine one shared base partition `P_0`. For each base
block `B`, let `r_j(B)` be the number of context-`j` closed blocks inside `B`.

The nominal fibered capacity of the closed views is

\[
C
=
\sum_{B\in P_0}\prod_j r_j(B).
\]

Equivalently, if the exact closed response labels are treated as relational
projections sharing the base key, `C` is the cardinality of their natural join.

Define the **join-realizability defect**

\[
\boxed{
\delta_{\rm join}
=
\log_2C-\log_2|P_U|
\ge0.
}
\]

This term vanishes exactly when the realized closed response relation is lossless
under the natural join of its projections.

This static part has classical database ancestry and is not a novelty claim.

## 3. Open-only innovation term

Because

\[
\mathcal L_U\subseteq\mathcal L_O,
\]

the open quotient can only refine `P_U`.

Define

\[
\boxed{
\iota_{\rm new}
=
\log_2|P_O|-\log_2|P_U|
\ge0.
}
\]

This is the extra exact memory forced by future response words that are available
only in the open grammar.

### Exact zero criterion

\[
\boxed{
\iota_{\rm new}=0
\iff
P_O=P_U.
}
\]

Equivalently, every open response word is constant inside each closed-union
quotient block, so all open responses factor through the union interface.

### Exact positive criterion

If

\[
\mathcal L_O
=
\mathcal L_U\cup\mathcal L_{\rm new},
\]

then

\[
\boxed{
\iota_{\rm new}>0
}
\]

iff there exist states `s,t` such that

\[
s\sim_U t
\]

but for at least one new word `w in L_new`,

\[
R(s,w)\ne R(t,w).
\]

Thus the existing CCOC newly-legal-word / fiber-split witness is not a separate
kind of obstruction: it is the local certificate for a positive open-only
innovation term.

## 4. Exact three-term decomposition

The total closed-to-open interface gap is

\[
\Delta_{\rm total}
=
\log_2|P_O|
-
\max_j\log_2|P_j|.
\]

Add and subtract `log2 C` and `log2 |P_U|`:

\[
\boxed{
\Delta_{\rm total}
=
\underbrace{\left(\log_2C-\max_j\log_2|P_j|\right)}_{\text{closed-view capacity}}
-
\underbrace{\delta_{\rm join}}_{\text{missing joint closed types}}
+
\underbrace{\iota_{\rm new}}_{\text{open-only future distinctions}}.
}
\]

This is an exact identity under the declared partition/refinement contract.

It separates two mechanisms that were previously easy to conflate:

1. **composition of old closed laws** can make the simultaneous interface large
   even if no genuinely new action is introduced;
2. **newly legal open futures** can split the resulting joint interface still
   further.

## 5. Mixed witness: one extra bit beyond the closed join

Take four jointly realizable binary coordinates

\[
(y,b_1,b_2,h).
\]

- shared base reads `y`;
- closed context 1 reads `(y,b1)`;
- closed context 2 reads `(y,b2)`;
- the closed-union grammar reads `(y,b1,b2)`;
- one open-only future word reads `h`.

Then

\[
|P_1|=|P_2|=4,
\qquad
C=8,
\qquad
|P_U|=8,
\qquad
|P_O|=16.
\]

Hence

\[
\delta_{\rm join}=0,
\qquad
\iota_{\rm new}=1,
\]

and

\[
\boxed{
\Delta_{\rm total}=2.
}
\]

Only one bit of that gap is available from simultaneous composition of the closed
views. The second bit exists because the open grammar legalizes a response that
was absent from every closed context.

This is the simplest example in which static database join theory explains only
part of the final causal-interface inflation.

## 6. Mixed witness with both loss and innovation

Constrain `(y,b1,b2)` to even parity but leave `h` free.

The closed shared-base capacity remains

\[
C=8,
\]

but only four `(y,b1,b2)` union response types are realized:

\[
|P_U|=4,
\qquad
\delta_{\rm join}=1.
\]

The open-only read of `h` doubles the union quotient:

\[
|P_O|=8,
\qquad
\iota_{\rm new}=1.
\]

With `|P_j|=4`,

\[
\Delta_{\rm total}
=1-1+1
=1.
\]

The join loss and open-only innovation are therefore independent terms: they can
both be positive in the same family.

## 7. Relation to the existing theorem spine

### CORE-2

The addressability / extension--compression lower bound remains the general tool
when the open grammar is not known to be an exact union or when only separating
future words are available.

The union-refinement theorem gives an exact characterization of the `L_U` part.

### CORE-5

A newly legal word that separates two states merged by `P_U` is exactly a witness
that

\[
\iota_{\rm new}>0.
\]

Conversely, any positive innovation term contains such a split pair and at least
one separating open-only word.

Thus the negative `CORE-5` witness is naturally absorbed into the general
inflation decomposition.

### Positive portability

If all open-only words factor through `P_U`, then

\[
\iota_{\rm new}=0.
\]

This is the response-level version of the conservative portability requirement:
new legal behavior must be label-deterministic on the old joint macro fibers.

## 8. Novelty boundary

The following are not novelty claims:

- adding and subtracting logarithmic partition cardinalities;
- common refinement of equivalence relations;
- natural-join / lossless-join reconstruction of static projections; or
- the statement that adding observations can refine an equivalence relation.

The intended CCOC contribution is the **causal composition interpretation and
construction package**:

- each closed label is an exact controlled future-response class, not a static
  table attribute chosen a priori;
- the theory distinguishes inflation from simultaneous composition of old
  response grammars from inflation created by newly legal futures;
- constrained composition families can remain close to the static join capacity;
- the large gaps have bounded-degree, pairwise, constant-local-grammar and
  constant-global-action-alphabet realizations.

A manuscript claim must still be checked against causal abstraction, interface
refinement, automata/test theory, and database joins. The decomposition is most
valuable as a theorem-spine unification unless that comparison establishes a
stronger novelty statement.

## 9. Executable certificates

`causal_model.interface_inflation` contains:

- `InterfaceInflationDecompositionCertificate` for pure finite partition data;
- `OperationalInterfaceInflationCertificate` for one controlled output system,
  a shared base word family, closed word families, and additional open-only words;
- `OpenOnlyWordSplitWitness` returning a concrete state pair, separating word,
  and conflicting traces whenever the innovation term is positive.

The finite replay verifies supplied contracts; the exact identities and iff
criteria are proved symbolically above.
