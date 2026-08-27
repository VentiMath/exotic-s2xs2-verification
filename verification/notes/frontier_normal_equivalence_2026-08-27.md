# Explicit normal block bundle and derived-frontier equivalence

This note replaces the derived-regular-neighborhood theorem in the specific
place where the verification used it. The construction is an explicit
barycentric-coordinate model on the actual marked triangulation.

Let `K` be the certified 4-complex and `T=T_alpha disjoint_union T_beta` the
full torus subcomplex. For a point `x` of `|K|`, write its barycentric
coordinates as `(lambda_v)` and define

\[
 q_T(x)=\sum_{v\in T}\lambda_v.
\]

Set

\[
 N_{1/2}=\{x:q_T(x)\geq 1/2\},\qquad
 F_{1/2}=\{x:q_T(x)=1/2\}.
\]

The first set is an explicit closed normal block neighborhood of `T`; the
second is its boundary. On a simplex with torus face `A` and opposite face
`B`, every point of `N_1/2` has the unique form

\[
 x=qy+(1-q)z,quad y\in\Delta_A, z\in\Delta_B,quad 1/2\le q\le1,
\]

with the `z` coordinate collapsed when `q=1`. Thus the local block is

\[
 \Delta_A\times C(\Delta_B),
\]

and its frontier block is

\[
 \Delta_A\times\Delta_B.
\]

These formulas restrict identically on every common face. The straight-line
homotopy that increases `q` to one, equivalently kills and renormalizes the
outside coordinates, retracts `N_1/2` to `T`. Run 48 supplies the missing
local-pair information: every link pair is the standard codimension-two
pair. Consequently the assembled cone blocks are the normal `D2` blocks,
and their frontier blocks assemble to the normal-circle boundary. This is a
construction, not an appeal to uniqueness of derived regular neighborhoods.

## The computed derived frontier

A vertex of the frontier used by `complement.py` is the barycenter `b(s)` of
a mixed simplex `s`: it meets `T` but is not contained in `T`. Put

\[
 A=s\cap T,\qquad B=s\setminus T.
\]

Both are nonempty. Define

\[
 h(b(s))=\tfrac12b(A)+\tfrac12b(B)
\]

and extend linearly over every chain of mixed simplices. This lands in
`F_1/2`.

Inside a fixed ambient simplex, the mixed-face poset is exactly

\[
 \mathcal F^+(\Delta_A)\times\mathcal F^+(\Delta_B),
\]

the product of the two nonempty-face posets. Its order complex is, by the
definition of barycentric subdivision, the barycentric subdivision of
`Delta_A x Delta_B`. The map `h` sends each poset vertex to the barycenter of
the corresponding product face. It is therefore the canonical PL
homeomorphism from the computed derived-frontier cell to the frontier block.
Because `A` and `B` are obtained by literal intersection and difference, the
maps agree on shared faces. Hence `h` is a global PL homeomorphism

\[
 h:\dot N(T)\longrightarrow F_{1/2}=\partial N_{1/2}.
\]

Run 49 checks this against the complete model:

- 113,336 mixed frontier vertices;
- 769,256 derived comparabilities;
- 22,234 incident 4-simplices;
- all three possible local products, `Delta0 x Delta3`,
  `Delta1 x Delta2`, and `Delta2 x Delta1`;
- exact affine nondegeneracy of every labeled maximal-chain template.

## Meridians

For a torus triangle `tau`, every incident 3- or 4-simplex has torus part
exactly `tau`. Under `h`, the alternating 3-/4-simplex loop used by both
peripheral extractors has constant torus coordinate `b(tau)`, while its
outside parts alternate between vertices and edges of `lk_K(tau)`. It is
therefore precisely the barycentric subdivision of the normal link circle,
with no homotopy or convention change.

Run 49 checks this for all 592 torus triangles. The distribution of fiber
lengths reproduces every local normal cycle in both components. Thus the
machine's `geom_M` and `geom_N` loops are literal normal-circle fibers of
the explicit boundary, not merely loops in a complex later named a boundary
by a theorem.

The product-framing push-offs were already constructed as paths in the same
mixed-face frontier, using literal product squares and the certified rail
normal directions. Composing them with `h` puts them on the explicit normal
boundary without changing their basing or their complement words.

## Resulting trust boundary

The formerly separate theorem node `T_derived_regular_neighborhood` is no
longer needed for the filled-presentation claim. Its two uses are replaced:

1. the frontier is the normal boundary by the explicit level-set block model
   and the global PL homeomorphism `h`;
2. the extracted dual loops are meridians because all of them are checked as
   fibers of that model.

The standard local-pair criteria used to establish local flatness in Run 48
remain named in the ledger. No new smoothing or symplectic claim is made by
this construction.
