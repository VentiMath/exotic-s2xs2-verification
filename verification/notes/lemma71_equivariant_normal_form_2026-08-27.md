# Lemma 7.1: equivariant normal form

## Statement being audited

Let the Lidman--Piccirillo genus-two surface carry the ordered five-chain
`a,b,c,d,e` and its orientation-preserving involution, which reverses the
chain, preserves `c`, and has two fixed points. Lemma 7.1 asserts that there
is an orientation-preserving diffeomorphism to the paper's marked octagon
which carries the five named curves in order, conjugates the involution to
the half-turn, and carries the two fixed points to `p` and `O`.

The proof naturally separates into a finite ribbon problem and a disk-action
problem. Run 55 certifies the first and reduces the second to an exact
classical theorem.

## 1. The five-chain fills the surface

A regular neighborhood of the five-chain deformation retracts to a graph
with six vertices and ten edges: four transverse crossing vertices and one
auxiliary vertex on each of the two end loops. Hence its Euler characteristic
is `6-10=-4`. The pairs `(a,b)` and `(d,e)` give two disjoint symplectic
pairs, so the neighborhood has genus at least two. Since it lies in a
genus-two surface, its genus is exactly two, and

```
-4 = 2 - 2(2) - boundary_components
```

forces two boundary components. The complement has Euler characteristic
`-2-(-4)=2`. Each complementary component has nonempty boundary and therefore
Euler characteristic at most one, so the two components are disks.

This also makes explicit a small step compressed in the paper: Euler
characteristic two alone is not the conclusion; the fact that there are
exactly two boundary circles forces two disk components.

## 2. Exhaustive equivariant ribbon classification

`lemma71_normal_form_check.py` starts from the abstract five-chain graph, not
from either triangulated fiber. At each independent four-valent crossing
there are six cyclic rotations, hence 36 pairs before constraints. The
chain-reversing involution determines the rotations at the other two
crossings.

The checker imposes only:

* alternating curve ends at each transverse crossing;
* preservation of cyclic order by the orientation-preserving involution;
* two ribbon boundary faces; and
* preservation, rather than exchange, of those two faces.

Exactly four systems survive. They are the four possible sign choices at the
two independent crossings. Orient `b` arbitrarily, reverse `a` (and therefore
`e`) if needed at the first crossing, and reverse `c` if needed at the
second. This normalizes all four systems to the same oriented ribbon system;
the involution transports the choices to `d,e`. Thus there is one
orientation-preserving equivariant marked ribbon type, not four geometric
possibilities.

Every surviving system has two boundary cycles of length ten. On each, the
involution is the free shift by five. The thickening map is constructive:
map each vertex disk by the cyclic map of its marked sectors and each edge
band in product coordinates. These maps agree on their attaching intervals,
so no general ribbon-thickening classification is needed for this instance.

Runs 34 and 54 then verify that the octagon model realizes precisely these
finite hypotheses and carries the required `a,b,c,d,e,p,O` labels.

## 3. The two complementary disks

The neighborhood is disjoint from the two fixed points. If the involution
exchanged the two complementary disks, neither disk could contain a fixed
point, contradicting the assumed two-point fixed set. Hence each disk is
invariant. Brouwer gives a fixed point in each, and because there are exactly
two globally, each contains exactly one.

The remaining fact is the classical periodic-disk theorem: a periodic
homeomorphism of the disk is topologically conjugate to an element of
`O(2)`. This is Theorem 3.1 of Adrian Constantin and Boris Kolev,
[*The theorem of Kerékjártó on periodic homeomorphisms of the disc and the
sphere*](https://arxiv.org/abs/math/0303256). In the orientation-preserving,
nontrivial, order-two case it is conjugate to the half-turn. Consequently its
quotient is a disk with one order-two branch point, exactly as used in the
paper.

The smooth upgrade needed by Lemma 7.1 is local and standard. Average a
Riemannian metric over the involution. At its isolated fixed point the
derivative is the orientation-preserving nontrivial involution `-I`, and the
exponential chart linearizes the action near that point. Downstairs, extend
the already matched boundary diffeomorphism over the quotient disk while
making it linear in these branch charts; lift the extension selected by its
boundary value. The lift is smooth at the branch point, agrees with the
ribbon map on the boundary, and conjugates the disk actions. Applying this
to the two labeled disks completes the required diffeomorphism.

## Conclusion and trust boundary

There is no remaining project-specific choice inside Lemma 7.1. Its ribbon
classification, face count, face action, labels, and comparison with the
octagon are finite and replayable. The only general input is the published
periodic-disk involution theorem (plus routine smooth disk extension and
invariant-metric linearization). Relative to that standard two-dimensional
theorem, Lemma 7.1 is proved.

## Run 56 source update

Run 56 independently checks that the hypotheses above are not merely
Wuebben's transcription: the immutable Lidman--Piccirillo v1 TeX explicitly
states the involution action, oriented preservation of `c`, and two fixed
points, while the original vector Figure 1 realizes exactly the ordered
five-chain intersections. Thus the remaining input to this lemma is the
periodic-disk theorem, not an unchecked source-figure identification.
