# Referee packet for the complement presentation

## Purpose and conclusion

This note isolates the topology between the marked triangulated bundle and
the finite group presentation.  Two facts that had been grouped under
`T_complement_presentation` are elementary and are proved here:

1. the complement of the full torus subcomplex deformation retracts onto the
   induced subcomplex on all remaining vertices;
2. the maximal-tree generators and triangle-boundary relators present the
   fundamental group of that induced subcomplex.

The only specifically PL-geometric residue is the standard derived regular
neighborhood theorem used to interpret the computed frontier loops as loops
on the normal boundary of the tori.

`luttinger/complement_theorem_audit.py` binds the hypotheses below to the
independent Run-30 extraction and the original Run-11 presentation.

## 1. The simplexwise complement retraction

Let `K` be a finite simplicial complex and `T` a full subcomplex.  Let `C` be
the induced subcomplex on `V(K)-V(T)`.  We claim that

\[
 |K|-|T|\simeq |C|.
\]

The deformation retraction is explicit.  In a simplex `sigma`, write a point
in barycentric coordinates as `(lambda_v)`.  Because `T` is full,
`sigma intersect T` is precisely the face spanned by the vertices of `sigma`
lying in `T`.  A point of `sigma-|T|` therefore has

\[
 S=\sum_{v\notin T}\lambda_v>0.
\]

Define `r` by setting the coordinates on `T` equal to zero and replacing each
outside coordinate by `lambda_v/S`.  The straight-line homotopy

\[
 H_t(x)=(1-t)x+t r(x)
\]

stays outside `T`, since its total outside weight is `(1-t)S+t>0`.
The formula is unchanged on common faces, so the simplexwise maps glue.  It
fixes `C` pointwise and is therefore a strong deformation retraction.

This proves the complement reduction used by `complement.py`; no local
flatness, smoothing, or regular-neighborhood theorem is needed for this
homotopy equivalence.  The integrated checker exhausts all 52 nontrivial
partitions of the vertices of simplices of dimensions zero through four.

For the union of the two disjoint tori, use their union as `T`.  Fullness was
checked independently during Run 30.  The independent route reconstructs
exactly 8,860 complement vertices and 108,722 complement edges without
importing `complement.py`.

## 2. The simplicial fundamental-group presentation

Let `C` be connected and choose a maximal tree in its one-skeleton.  Collapse
the tree to a point.  The quotient has one oriented circle for every edge not
in the tree.  Attaching every two-simplex contributes its oriented
three-edge boundary as a relator.  Cells of dimension at least three do not
change the fundamental group.  Cellular van Kampen therefore gives

\[
 \pi_1(C)=\langle e\notin \mathcal T\mid
 \partial\tau,\ \tau\in C^{(2)}\rangle.
\]

This is exactly `pi1.Presentation`: tree edges contribute the empty word,
non-tree edges receive one signed generator, and each ordered triangle adds
`(a,b)(b,c)(a,c)^-1`.

There is a useful independent count.  A tree on 8,860 vertices has 8,859
edges.  Hence the 108,722 complement edges force

\[
 108722-8859=99863
\]

generators, exactly the raw Run-11 count.  The reported 321,702 relators are
the nonempty triangle-boundary relators.  Subsequent Tietze simplification is
a separate ledger input and is not being smuggled into this step.

## 3. The derived frontier and peripheral loops

The first barycentric subdivision has one vertex `b(sigma)` for every
simplex `sigma` of `K`.  The frontier used by both implementations consists
of chains of simplices whose vertices `sigma` meet both `T` and its vertex
complement.  Run 30 independently reconstructs 113,336 such vertices.

On a frontier vertex, the map

\[
 b(\sigma)\longmapsto
 \max\{v\in\sigma:v\notin T\}
\]

extends simplicially to the subdivision of `C`: for a nested chain of
simplices the selected vertices form a weakly ordered simplex.  This is the
combinatorial retraction used to read every frontier path as a path in `C`.
Both the original and independent implementations check every consecutive
edge after applying it.

For a full locally flat PL submanifold, the first derived neighborhood is a
regular neighborhood and this frontier is its normal boundary.  In
codimension two, the boundary of the dual two-cell to a torus triangle is
therefore an oriented meridian.  This is the remaining general PL input.  A
standard reference is Rourke--Sanderson, *Introduction to Piecewise-Linear
Topology*, Chapter 3, especially the derived-neighborhood construction and
Theorem 3.8, <https://doi.org/10.1007/978-3-642-81735-9>.

The construction-specific hypotheses are stronger than a mere numerical
match:

- the two marked vertex sets induce disjoint closed tori with f-vectors
  `[24,72,48]` and `[272,816,544]`;
- the bundle construction supplies literal product normal directions along
  the two tori;
- the independent extractor checks that every dual-meridian link is one
  circle and orients it from the ambient and torus orientations;
- reversed-meridian, opposite-whisker, and opposite-half controls produce
  distinct hashes;
- all exported frontier paths retract to valid edge paths in `C`.

Thus the regular-neighborhood theorem is used only to name the frontier as
the geometric normal boundary—not to infer the complement group or to repair
an invalid simplicial path.

## Exact trust boundary

After this packet, the complement-to-presentation bridge consists of:

1. the explicit barycentric-coordinate deformation retraction proved in
   Section 1;
2. the maximal-tree cellular van Kampen argument proved in Section 2;
3. the derived regular-neighborhood/frontier theorem for the already checked
   full locally flat torus subcomplexes.

The first two may be checked directly from this note.  Only item 3 remains a
cited PL theorem.  The later claim that proof-producing eliminations preserve
the presented group remains separately and visibly dependent on the Tietze
theorem.

## Referee checklist

- Check fullness and the simplexwise normalization formula.
- Check that the union of the two torus vertex sets remains full.
- Check connectedness and the maximal-tree generator count.
- Check the triangle-boundary convention in `pi1.py`.
- Apply the derived regular-neighborhood theorem to the two product torus
  subbundles.
- Check that the dual two-cell orientation agrees with the stated meridian
  convention.
