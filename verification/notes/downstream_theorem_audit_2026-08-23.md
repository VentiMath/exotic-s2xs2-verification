# Downstream theorem audit (2026-08-23)

Scope: the deductions after the fundamental-group computation in Theorem 1.2
of arXiv:2608.17267: the homeomorphism classifications, exoticness arguments,
the slicing obstruction, and the reglued
`CP^2 # overline(CP)^2` claim.  This is a hypothesis audit, not a
formalization of Freedman theory, symplectic Kodaira dimension, or Heegaard
Floer theory.

## Result

No downstream gap was found.  Conditional on the now-certified statement
`pi_1(V')=1`, the deductions in Theorem 1.2(a)--(c) are supported by the stated
hypotheses.  The places most worth checking were the cyclic-fundamental-group
classification, the square-zero torus lift, minimality/Kodaira dimension, and
the reuse of the Lidman--Piccirillo Floer argument.  Each survives the checks
below.

## 1. The double and the quotient

For the connected two-fold cover `Z' -> W'`, covering theory gives

    1 -> pi_1(Z') -> pi_1(W') -> Z/2 -> 1.

Thus `pi_1(Z')=1` gives `pi_1(W')=Z/2`.  Conversely, if `W'` is homeomorphic
to Kawauchi's `B`, the middle and quotient groups are both `Z/2`, so the
surjection is an isomorphism and its kernel is trivial.

Proposition 1.3 gives that `W'` is a smooth spin rational homology 4-sphere.
For `pi_1(W')=Z/2`, its ordinary form on `H_2/torsion` is zero, its `w_2` type
is spin/type II, and its Kirby--Siebenmann invariant is zero by smoothness.
These are exactly the invariants in the Hambleton--Kreck finite-cyclic
classification.  The same data hold for `B`, so the homeomorphism conclusion
is justified.  The `b_2=0` uniqueness statement in Baykur--Stipsicz--Szabo is
an independent modern cross-check.

## 2. The intersection form of the simply connected double

If `pi_1(Z')=1`, then `chi(Z')=4` gives `b_2=2`.  The fiber `F` and closed
section `Gamma` intersect once, hence their intersection matrix has determinant
`-1` and they are an integral basis.  Spinness makes `Gamma^2=2n` even, and

    F^2=0,  F.Gamma=1,  Gamma^2=2n
    Gamma_0 = Gamma - n F

gives `F^2=Gamma_0^2=0` and `F.Gamma_0=1`.  The form is therefore the
hyperbolic form `H`.  Smoothness gives Kirby--Siebenmann invariant zero, so
Freedman's simply connected classification gives `Z'` homeomorphic to
`S^2 x S^2`.

The corresponding odd calculation used after the boundary regluing is also
correct.  If `Gamma^2=2n+1`, then `E=Gamma-nF` has square `+1` and `F-E` has
square `-1`, with zero mutual intersection.  Thus the rank-two, signature-zero
odd form is `<1> + <-1>`.

These integral basis calculations are executable in
`luttinger/downstream_audit.py`.

## 3. Minimality and Kodaira dimension

The pre-surgery closed genus-2 bundle over a genus-2 surface is aspherical:
both base and fiber are aspherical and the homotopy long exact sequence kills
all higher homotopy groups.  It therefore contains no exceptional sphere and
is minimal.  It is neither rational nor ruled (in particular those manifolds
have nonzero `pi_2`).  By the standard characterization of symplectic Kodaira
dimension `-infinity`, its Kodaira dimension is not `-infinity`.

Ho--Li prove both that Luttinger surgery preserves minimality and that it
preserves symplectic Kodaira dimension.  Independently, the paper's statement
that the resulting `Z'` is minimal because it is spin is valid: a smooth
exceptional sphere would have odd self-intersection `-1`, impossible in a spin
4-manifold.  Since `S^2 x S^2` has Kodaira dimension `-infinity`, diffeomorphism
invariance of symplectic Kodaira dimension distinguishes the smooth structures.

The adjective "non-trivial" in "non-trivial genus-2 surface bundle" is not
needed for this argument; the genera of the base and fiber already supply the
asphericity and non-rational/non-ruled conclusions.

## 4. The no-torus lemma and the lifted torus

In the simply connected double, `F` and `Gamma` form a hyperbolic basis and
are symplectic genus-2 surfaces of square zero.  In a tubular neighborhood,
the paper constructs a connected unbranched degree-`k` cover representing
`kF`; its genus is `k+1`.  The symplectic Thom theorem makes this genus
minimal.  The same holds for `kGamma`.  Since

    (aF+bGamma)^2 = 2ab,

every nonzero square-zero class lies on one of these two axes and has minimum
genus at least two.  It cannot be represented by a torus.

The lift used in the slicing argument is legitimate.  A homologically
essential slice disk makes the simply connected 0-trace `X_0(4_1)` embed in
`W'`, carrying the essential square-zero torus.  The cover restricted to this
simply connected trace is trivial, so either copy embeds in `Z'`.  If the
lifted torus class were zero, its push-forward under the covering map would be
zero, contradicting essentiality of the original class.  Its self-intersection
remains zero because the covering is a local diffeomorphism.

The null-homologous alternative is ruled out by the relative Rokhlin/Arf
obstruction exactly as in Lidman--Piccirillo; `Arf(4_1)=1`.

## 5. The reglued odd manifold and the Floer obstruction

The stronger hypothesis `pi_1(V')=1` is correctly used here.  Van Kampen then
makes both the ordinary double and the boundary-reglued double simply
connected; simple connectivity of the ordinary double alone would not suffice
for an arbitrary regluing.

The Lidman--Piccirillo framing switch changes the parity while preserving
rank two and signature zero.  The preceding odd-form calculation and Freedman
therefore give the homeomorphism type `CP^2 # overline(CP)^2`.

The relative-invariant argument also carries over:

* `Z'` is symplectic with `b^+=1`.
* The surviving fiber is symplectic of genus two and square zero.  Adjunction
  directly gives `K.F=2`; no extra canonical-class-under-surgery assumption is
  needed for this pairing.
* `H^2(V')=Z` and the fiber generates `H_2(V')`, so the two restrictions with
  `|c_1.F|=2` are the conjugate pair used in the original Lemma 9.
* For the non-torsion boundary Spin-c structures, the relevant reduced Floer
  group of the genus-2 fibered zero-surgery is one-dimensional, so the two
  nonzero relative invariants pair nontrivially after regluing.
* In standard `CP^2 # overline(CP)^2`, each of the two primitive square-zero
  lines has a square-zero sphere.  Cutting on the boundary of its tubular
  neighborhood gives `S^2 x S^1`, whose reduced Floer group vanishes in the
  relevant non-torsion Spin-c structure.  Hence the corresponding mixed
  invariant vanishes, contradicting the nonzero invariant of the reglued
  manifold.

## 6. Remaining epistemic boundary

This audit does not independently reprove the external classification,
symplectic, Rokhlin, or Floer theorems.  It checks that their hypotheses match
the manifolds and classes constructed here and that the intervening algebra is
correct.  With the geometric fundamental-group certificate in runs 10--23,
there is no presently identified mathematical blocker in the paper's proof.

Primary sources checked: Freedman (1982); Hambleton--Kreck (1988, 1993), as
summarized precisely in Hambleton (2008), Theorem 5.1; Ozsvath--Szabo (2000,
2004); Li (2006); Ho--Li (2012); Lidman--Piccirillo (2025); and the current
paper arXiv:2608.17267.
