# Absolute innovation capacity and local-query latency sharpness

> **Status:** post-reopening sharpness closure for the existing single-action
> innovation family. The finite-domain capacity inequality, Kraft/tree-counting
> bound, and one-edge-per-step propagation argument are mathematical substrate,
> not novelty claims.

## 1. Two questions left after single-action innovation

The single-action relay family already shows that `m` fixed closed compositions
can each have a one-bit exact causal interface, their closed-union quotient and
static join capacity can remain one bit, and legalizing the single primitive
action `fire` can create

\[
\iota_{\rm new}=m
\]

bits of open-only interface innovation.

Two sharpness questions remain.

1. Could any finite system with the same domain and closed-union quotient create
   **more** than `m` new bits?
2. Is the addressed relay's query length merely convenient, or is it forced by
   the declared local routing/propagation architecture?

Both close exactly.

## 2. Absolute finite-domain innovation capacity

Let `D` be one finite comparison domain. Let `P_U` be the exact quotient under the
union of all closed grammars and let `P_O` be the exact quotient under the full
open grammar. Since the open grammar contains the closed union,

\[
P_O\preceq P_U,
\]

so `P_O` refines `P_U`.

Define

\[
\iota_{\rm new}
=
\log_2|P_O|-\log_2|P_U|.
\]

Because a partition of `D` can never have more than `|D|` blocks,

\[
|P_O|\le |D|.
\]

Therefore

\[
\boxed{
\iota_{\rm new}
\le
\log_2|D|-\log_2|P_U|.
}
\]

Call the right-hand side the **absolute innovation capacity** of the finite
comparison domain relative to the closed-union quotient.

### Equality condition

Equality holds iff

\[
|P_O|=|D|,
\]

that is, iff the open quotient is discrete on the declared domain.

Define the unused capacity

\[
\epsilon_{\rm cap}
=
\log_2|D|-\log_2|P_O|\ge0.
\]

Then the exact identity is

\[
\boxed{
\iota_{\max}
=
\iota_{\rm new}
+
\epsilon_{\rm cap}.
}
\]

This is an upper-bound closure, not a new source of inflation.

## 3. The single-action family saturates the absolute upper bound

For the power-of-two relay family,

\[
D_m=\{0,1\}^{m+1},
\qquad
|D_m|=2^{m+1}.
\]

Every fixed closed context and their union retain only the focal bit:

\[
|P_U|=2.
\]

After `fire` becomes legal, the current output gives `y` and the addressed probe
words recover every dormant bit. The open quotient is discrete:

\[
|P_O|=2^{m+1}=|D_m|.
\]

Hence

\[
\boxed{
\iota_{\rm new}
=
\log_2\frac{2^{m+1}}{2}
=m
}
\]

and simultaneously

\[
\boxed{
\iota_{\rm new}=\iota_{\max}.
}
\]

Thus the earlier linear result is actually **absolute-memory sharpness** for the
finite domain: no open grammar on the same states can force more new exact bits
relative to that closed-union quotient.

## 4. Why the latency statement needs an explicit local contract

A latency lower bound does **not** follow from maximum degree alone. A model with
strong global operations, hard-coded nonlocal addressing, or unrestricted
long-range updates can violate graph-distance intuition.

The lower bound therefore uses only the architecture actually implemented by the
CCOC addressed relay:

1. one unique selector token starts at the binary-tree body root;
2. address actions move the selector by at most one adjacent parent--child edge
   per action;
3. memory sites are terminal leaves, so their terminating address words form a
   prefix-free binary code;
4. `fire` injects one pulse only at the currently selected memory leaf;
5. after firing, the dormant bit can influence the focal output only through the
   explicit pulse, which moves at most one adjacent child--parent edge per
   `tick`;
6. the focal output node sits one edge above the binary-tree body root.

No latency claim is made outside this one-edge-per-step local causal contract.

## 5. Address-selection lower bound

Let `m` terminal memories be addressed over a binary alphabet. Because a terminal
memory fires at the end of its address, the terminal address set is prefix-free.

If the maximum address length is `d`, a binary prefix tree contains at most

\[
2^d
\]

prefix-free terminal words of length at most `d`. Equivalently, Kraft's
inequality gives the same count.

Thus

\[
\boxed{
L_{\rm addr}^{\rm worst}
\ge
\lceil\log_2m\rceil.
}
\]

For `m=2^d`, the current relay uses all `2^d` binary words of length exactly `d`,
so the address phase attains this bound.

## 6. Return-path causal lower bound

Take a memory leaf whose selector depth below the body root is `d_j`. In the
current tree the focal output is one edge above the body root, hence that leaf is
at graph distance

\[
d_j+1
\]

from the focal node.

At the moment `fire` is applied, the leaf bit is injected into the leaf's
transient pulse state. The focal output does not yet see that bit. Under the
one-edge-per-`tick` propagation rule, at least

\[
d_j+1
\]

additional propagation ticks are required before that leaf bit can affect the
focal output.

Therefore every addressed read of that leaf needs at least

\[
\boxed{
L_j
\ge
 d_j + 1 + (d_j+1)
 =2d_j+2.
}
\]

The terms are, respectively, address routing, one `fire`, and the leaf-to-focal
causal path.

## 7. Worst-case architecture lower bound

Combining the prefix-free address lower bound with the same-tree return-path
contract gives

\[
\boxed{
L_{\rm query}^{\rm worst}
\ge
2\lceil\log_2m\rceil+2.
}
\]

For the implemented power-of-two family `m=2^d`, every memory leaf has selector
depth `d` and focal distance `d+1`. The canonical word is

\[
w_j
=
\operatorname{addr}(j)
\;\mathsf{fire}\;
\mathsf{tick}^{d+1},
\]

whose length is

\[
|w_j|=d+1+(d+1)=2d+2.
\]

Hence

\[
\boxed{
L_{\rm query}^{\rm worst}
=2\log_2m+2
}
\]

and the construction attains the declared local-architecture lower bound exactly.

This is stronger than order-optimality: within this selector-plus-pulse contract,
there is zero latency slack at every power-of-two family size.

## 8. What this closes

The current single-action family now simultaneously satisfies:

- every fixed closed composition: one-bit exact interface;
- closed-union interface: one bit;
- static shared-view/join capacity: one bit;
- newly legal primitive action types: one (`fire`);
- full global action alphabet: four symbols;
- open-only exact innovation: `m` bits;
- absolute finite-domain innovation capacity: `m` bits;
- maximum degree: three;
- pairwise local selector and pulse updates;
- constant local state/message grammar;
- worst-case addressed query latency: `2 log2(m)+2`;
- architecture-level latency lower bound: `2 log2(m)+2`.

So both the **amount of new exact causal memory** and the **query latency under the
declared local architecture** are saturated by the same construction.

## 9. Novelty boundary

None of the following is a novelty claim:

- a partition has at most as many blocks as its underlying set;
- Kraft/prefix-code counting;
- graph-distance lower bounds under one-edge-per-step signal propagation;
- the fact that an extra observation/intervention can refine an equivalence.

The CCOC novelty candidate remains the simultaneous separation package: small
exact causal interfaces in every fixed closed composition and their union, one
new primitive action producing the maximum possible open-only interface
innovation, and an exact bounded-degree/pairwise/constant-alphabet realization
that also meets its explicit local query-latency lower bound.

A priority claim still requires comparison with automata alphabet/action
extensions, causal abstraction under changing intervention families, local and
distributed computation, and network-query lower bounds.

## 10. Executable certificates

`causal_model.innovation_capacity_latency` provides:

- `InnovationCapacityCertificate`: actual innovation, absolute finite-domain
  maximum, unused capacity, and saturation iff the open quotient is discrete;
- `PrefixFreeAddressLatencyCertificate`: exact prefix-free/Kraft accounting and
  the logarithmic worst-case address lower bound;
- `RelayLocalLatencyCertificate`: explicit selector depth, response path, per-port
  local latency lower bounds, and equality for the balanced addressed relay;
- `SingleActionSharpnessClosureCertificate`: checks that the same finite family
  saturates both the absolute-memory and declared-locality latency bounds.

The finite certificates replay supplied instances. The all-size statements are
the elementary symbolic arguments above.
