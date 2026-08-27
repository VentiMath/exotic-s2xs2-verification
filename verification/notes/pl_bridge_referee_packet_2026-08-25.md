# Referee packet for the PL bridge

## Purpose

This note isolates the general PL facts used to pass from the finite
certificates in Runs 28, 33, and 34 to the paper's marked smooth bundle.  Run
36 integrates and rechecks every finite hypothesis below.  The objective is
to prevent the phrases "ribbon graph thickens," "flip trace," and "smooth the
PL bundle" from hiding distinct assumptions.

There are four general inputs:

1. rotation systems determine oriented ribbon thickenings;
2. the verified labeled cone-ball is the trace of a 2--2 bistellar move;
3. a PL 4-manifold has an essentially unique compatible smoothing;
4. oriented intersection pairings are natural under the resulting marked
   equivalence.

The first two inputs are proved in the special finite form needed here.  The
last two are cited smoothing and Poincare-duality facts.

## Machine-bound hypotheses

`luttinger/pl_theorem_audit.py` reads the Run-33 and Run-34 JSON certificates
and replays the Run-28 self-intersection construction.  It checks:

- all 128 flip links have f-vector `[8,18,12]` and all cone stars have
  f-vector `[9,26,30,12]`;
- all 5,718 vertex links are connected triangulated surfaces with the
  sphere or one-boundary-component disk Euler characteristic recorded by the
  local checker;
- every slab has exactly its two marked fiber boundaries and is a union of
  the labeled flip balls and literal staircase products;
- the two marked-fiber ribbon codes agree, including all crossing rotations,
  both p/O faces, and the involution on every directed curve end;
- every ribbon segment has an explicit common subdivision;
- all four constant normal clutching rotations give a disjoint normal
  push-off, with an exact radial-chain boundary and square zero.
- the ambient marked bundle in the section replay has dimension four, the
  dimension used in the smoothing theorem application.

The integrated result is `luttinger/pl_theorem_hypotheses.json`.

## 1. Equivariant ribbon thickening

A ribbon graph consists of a finite graph and a cyclic order on the
half-edges at every vertex.  Its oriented regular neighborhood is constructed
without a classification theorem: replace each vertex by an oriented disk,
attach one oriented rectangle for each edge in the prescribed cyclic order,
and glue the short sides of the rectangles to their vertex disks.

Suppose two ribbon graphs have an isomorphism preserving the cyclic orders.
Map each vertex disk orientation-preservingly and map each edge rectangle by
a product map.  These maps agree on their attaching intervals and therefore
give an orientation-preserving homeomorphism of the ribbon neighborhoods.
This is the special case of the Heffter--Edmonds rotation principle stated as
Gross--Tucker, *Topological Graph Theory*, Theorems 3.2.2--3.2.3.  A modern
reference is Lando--Zvonkin, *Graphs on Surfaces and Their Applications*,
Chapter 1, <https://doi.org/10.1007/978-3-540-38361-1>.

In Run 34, the isomorphism additionally commutes with the involution on every
directed half-edge.  Choose the vertex-disk and band product maps on one
orbit and define them on its partner by conjugating with the involutions.  At
the two fixed disks, the checked cyclic action makes the same construction
commute there.  Thus the thickening is equivariant; no averaging or
equivariant smoothing theorem is required for this surface-level step.

The boundary components of the ribbon neighborhood are the cycles of the
half-edge rotation followed by edge reversal.  Run 34 checks that there are
exactly two and that the isomorphism preserves their labels p and O.  After
subdividing each paired segment by the explicit product subdivision recorded
in the certificate, the boundary maps are simplicial.  If `h:S^1->S^1` is
such a map, its conical extension is

\[
H([x,t])=[h(x),t].
\]

It is a PL homeomorphism of the disk with inverse the cone on `h^{-1}`.  It
commutes with the involution because `h` does.  Capping the p/O boundary
cycles therefore gives an equivariant marked PL homeomorphism of the two
closed fibers.  This is the entire content previously hidden in
`T_equivariant_ribbon_thickening`.

## 2. The elementary 2--2 trace

Lickorish, Definition 2.3, defines a bistellar move by replacing

\[
A*\partial B \quad\text{with}\quad \partial A*B.
\]

See W. B. R. Lickorish, *Simplicial moves on complexes and manifolds*,
Geom. Topol. Monogr. 2 (1999), 299--320,
<https://arxiv.org/abs/math/9911256>.  For a two-dimensional 2--2 move, `A`
and `B` are the two diagonals on four vertices.  Both displayed complexes are
two-triangle disks, and their union is

\[
\partial(A*B),
\]

the boundary of the tetrahedral 3-ball `A*B`.  Thus the elementary trace is a
PL 3-ball whose lower and upper disks use the complementary diagonals and
whose remaining boundary is the product annulus on the quadrilateral.

Run 33 verifies precisely a subdivision of this labeled object for every
move: two floor triangles, two roof triangles, complementary diagonals, four
staircase side squares, a connected closed surface link with Euler
characteristic two, and its cone star.  By the classification of compact
surfaces, the link is `S^2`; its cone is a PL 3-ball.  The labeled boundary
partition gives the preceding lower disk, upper disk, and product annulus.
The relevant full surface-classification statement is J. Gallier,
*The Classification Theorem for Compact Surfaces*, Theorem 5.3.2,
<https://arxiv.org/abs/0805.0562>: compact surfaces are determined by
orientability, boundary count, and Euler characteristic.  In the present
chi-two closed and chi-one one-boundary-component cases the results are the
sphere and disk, respectively.

The simultaneous quadrilaterals are vertex-disjoint, so their trace balls
are disjoint.  Outside them, Run 33 verifies literal staircase
triangulations of `triangle x I`.  Gluing the trace balls and product prisms
along their checked common faces therefore produces a relative PL product
cobordism from the lower marked fiber to the upper marked fiber.  Iterating
the 64 slabs gives the represented mapping cylinder.  Pachner's general
theorem is stronger than needed, but supplies the standard context: U.
Pachner, *P.L. homeomorphic manifolds are equivalent by elementary
shellings*, European J. Combin. 12 (1991), 129--145,
<https://doi.org/10.1016/S0195-6698(13)80080-7>.

The global vertex-link audit independently confirms that the assembled open
stack is a combinatorial 3-manifold with exactly the two marked fiber
boundaries.  Hence the construction is not relying only on the local move
labels.

## 3. From the marked PL bundle to the smooth bundle

The mapping-cylinder construction gives a compact PL 4-manifold, with the
marked fiber and torus subbundles carried in explicit product charts.  The
based monodromy certificates identify its two mapping classes with those of
the paper.  The already separate marked-surface-bundle theorem therefore
identifies the PL bundle with the underlying PL bundle of the paper's smooth
bundle.

The remaining category change is standard low-dimensional smoothing theory.
Hirsch--Mazur classify compatible smoothings by maps to `PL/O`; `PL/O` is
6-connected.  Consequently a PL manifold of dimension four is smoothable
and its compatible smoothing is unique up to concordance.  Their product
theorem turns the relevant concordance into a diffeomorphism.  References:

- M. Hirsch and B. Mazur, *Smoothings of Piecewise Linear Manifolds*, Annals
  of Mathematics Studies 80, Princeton University Press (1974), Parts I--II,
  <https://www.jstor.org/stable/j.ctt1bd6m0d>;
- C. Lange, *Equivariant smoothing of piecewise linear manifolds*,
  Math. Proc. Cambridge Philos. Soc. 160 (2016), 347--359, introduction and
  main theorem, <https://arxiv.org/abs/1507.02395>.

Only ordinary smoothing is needed for the bundle.  The marked curves and
tori already lie in literal surface/product charts, so those charts may be
smoothed first and the relative product form of the smoothing theorem used
away from them.  Alternatively, smooth representatives of the certified
surface mapping classes give the same marked smooth mapping torus directly.
There is no appeal here to smoothing an arbitrary wild subcomplex.

## 4. The square-zero section survives the category change

Run 28 constructs a PL section `Gamma_hat`, a disjoint normal push-off
`Gamma_hat'`, and an oriented radial 3-chain with

\[
\partial C=\Gamma_{hat}'-\Gamma_{hat}.
\]

Thus the two disjoint surfaces represent the same homology class.  Their
algebraic intersection is zero, so

\[
[\Gamma_{hat}]^2=0
\]

in the oriented PL 4-manifold's homological intersection pairing.  This
conclusion does not require smoothing the particular triangulated push-off:
the intersection form is the Poincare-duality pairing

\[
(a,b)\mapsto \langle PD(a)\smile PD(b),[M]\rangle,
\]

and is natural under orientation-preserving homeomorphisms.  The marked
bundle equivalence carries the section class to the paper's smooth section
class, whose smooth self-intersection is the same homological square.

For the PL regular-neighborhood and intersection framework, see
Rourke--Sanderson, *Introduction to Piecewise-Linear Topology*, Chapter 3,
especially the derived-neighborhood construction and Theorem 3.8,
<https://doi.org/10.1007/978-3-642-81735-9>.  Naturality of the final formula
is ordinary Poincare duality, not an additional dimension-four smoothing
claim.

## Exact remaining trust boundary

After Run 36, the PL boundary consists of these named conventional facts:

1. compact-surface classification in the sphere/disk cases;
2. the standard PL interpretation of the explicitly labeled 2--2 trace;
3. existence and concordance uniqueness of compatible smoothings in
   dimension four;
4. naturality of the oriented homological intersection pairing.

Every construction-specific hypothesis of those facts is represented in the
integrated certificate.  No picture-based mapping-class inference, shared
fiber implementation, unexamined vertex link, or uncomputed normal clutching
remains in this bridge.

## Referee checklist

- Check the cell-by-cell equivariant ribbon thickening and conical p/O disk
  extensions.
- Check that the Run-33 labeled boundary partition is exactly the
  `A*boundary(B)` to `boundary(A)*B` trace.
- Check that the relative/product smoothing statement applies to the marked
  bundle charts, or use smooth mapping-torus representatives directly.
- Check that the marked equivalence sends the Run-28 section class to the
  paper's fixed-point section class.
