# Referee packet for the marked surface-bundle identification

> **v2.0.0 semantic clarification.** The construction below proves the
> bundle statement for the audit-defined `R_*`. Comparing `R_*` with the
> object intended by Wuebben is not part of this packet; it is S1--S4.

## Purpose and conclusion

This note records the former theorem route called `T_surface_bundle`. Run 52
supersedes that route with an explicit graph-clutching construction, and
`T_surface_bundle` is no longer in the proof ledger.
The conclusion needed by the audit is narrow: the combinatorially assembled
genus-2 bundle, with its marked fiber and the two torus subbundles, is bundle
equivalent to the bundle specified in the paper.

There is no additional relation or coherence condition hidden in this step.
The base is a once-punctured torus and retracts to a bouquet of two circles.
Consequently the marked bundle is determined by the two monodromy mapping
classes.  Both have already been certified as *based* actions, in two
different beta-stack triangulations.  The finite hypotheses of this argument
are integrated by `luttinger/surface_bundle_theorem_audit.py` and frozen in
`luttinger/surface_bundle_theorem_hypotheses.json`.

## 1. Why two monodromies suffice

Let `F` be the closed oriented genus-2 fiber and let `B` be the
once-punctured torus.  Smooth oriented `F`-bundles are classified by homotopy
classes of maps

\[
 B\longrightarrow B\operatorname{Diff}^+(F).
\]

The construction of `B` used here is an oriented annulus with one band
joining its two boundary components.  Attaching that band decreases Euler
characteristic from zero to minus one and joins the boundary components, so
the result is an oriented genus-one surface with one boundary component.  It
deformation retracts to a graph with one vertex and two loop edges.

For a graph, a map into any connected target component is determined up to
homotopy by the components of the two edge loops.  Equivalently, after a
fiber marking at the vertex, the bundle is determined by the ordered pair

\[
 ([\phi_0],[\psi_0])\in
 \pi_0\operatorname{Diff}^+(F)^2=\operatorname{Mod}(F)^2.
\]

Changing the fiber marking simultaneously conjugates the pair.  Here the
fiber marking is fixed, so even that ambiguity is absent.  In particular,
there is no base two-cell whose attaching word would impose a commutator
condition.  This is the decisive simplification supplied by the boundary of
the base.

The standard classifying-space formulation is in Steenrod's classification
theorem for bundles. For surface bundles specifically, Baykur--Margalit,
Section 2, state the monodromy classification. Their broader surface-base
discussion uses contractibility of identity components, but that stronger
fact is not needed for the present graph base:

- R. Inanc Baykur and D. Margalit, *Indecomposable surface bundles over
  surfaces*, J. Topol. Anal. 5 (2013), 161--181,
  <https://arxiv.org/abs/1209.1162>.
- C. J. Earle and J. Eells, *The diffeomorphism group of a compact Riemann
  surface*, Bull. Amer. Math. Soc. 73 (1967), 557--559,
  <https://doi.org/10.1090/S0002-9904-1967-11746-4>.

Indeed, the present argument uses only
`pi1(BDiff+(F)) = pi0(Diff+(F))`, identification of those components with
mapping classes, and homotopy invariance of pullback bundles. No claim about
higher homotopy groups or contractibility of `Diff_0(F)` is required.

## 2. Why the certified actions determine the mapping classes

Use the paper's based generators `x,y,r,s` of the closed genus-2 surface
group.  The two actions certified by the construction are

\[
 \phi_0:x\leftrightarrow r,\quad y\leftrightarrow s,
\]

and

\[
 \psi_0:x\mapsto y^{-1},\quad y\mapsto yx,\quad
 r\mapsto r,\quad s\mapsto s.
\]

Run 12 obtains the beta action from literal basepoint whiskers and replays
17,839 elementary Tietze eliminations.  Run 32 repeats it on a different
64-interface beta trace and reduces all four based residual paths to the
empty word with a separately replayed 34,735-step certificate.  Thus the
comparison is not an inference from homology or free homotopy.

Dehn--Nielsen--Baer identifies the orientation-preserving mapping class group
of a closed oriented surface with the orientation-preserving subgroup of
`Out(pi1(F))`.  In particular its map to `Out(pi1(F))` is injective.  Equality
of the displayed based automorphisms is stronger than equality of the outer
automorphisms, so it forces equality of the two mapping classes.  A precise
modern reference is Farb--Margalit, Theorem 8.1:

- B. Farb and D. Margalit, *A Primer on Mapping Class Groups*, Princeton
  Mathematical Series 49 (2012), Chapter 8,
  <https://doi.org/10.23943/princeton/9780691147949.003.0009>.

The integrated checker also verifies algebraically that each displayed
automorphism preserves the conjugacy class of
`[x,y][r,s]`.  This is a diagnostic, not a replacement for the two geometric
realizations and their proof-producing path calculations.

## 3. Preservation of the marked torus subbundles

The needed equivalence is relative to more than a single fiber.

For `T_alpha`, the independent marked-fiber certificate identifies the full
equivariant ribbon code.  It preserves the named curve `c`, the two labeled
complementary disks containing `p` and `O`, and the involution on every
directed curve end.  On `c`, `phi_0` is the certified free half-rotation.
The mapping torus of this marked circle is therefore carried to the paper's
`c`-subbundle.

For `T_beta`, both representatives use the same ordered twists supported near
`a` and `b`, which are disjoint from `e`.  The primary beta trace is a literal
product on `e` through all 32 interfaces; the alternative 64-interface trace
has the same marked peripheral semantics.  The comparison isotopy can hence
be avoided entirely. Run 51 constructs the full three-row `e` collar, checks
that all 1,536 beta trace cells avoid it, and checks all 3,072 tetrahedra in
the restricted stack against the literal staircase product. Since the paper
and model use the same ordered relative twist word `T_a o T_b`, their
comparison is relative to the `e` collar by construction. Run 51 likewise
checks exact equivariance of the alpha map on every row of the `c` collar.

## 4. Status after Run 52

The classification and Dehn--Nielsen--Baer discussion above is retained as
an independent conventional route. It is no longer an active trust boundary.
Run 52 defines `[x,t] -> [h(x),t]` on both mapping-cylinder handles, checks
the forward and inverse seam equations, and glues the maps along their common
fiber block. Run 51 supplies the exact relative conjugacies. Since the base
has no two-cell, no further coherence equation exists.

All construction-specific hypotheses are machine-bound: the topology and
marking of the fiber, the topology and two-loop spine of the base, both
based monodromy actions, preservation of `c`, pointwise product behavior on
`e`, and the agreement of the independently extracted crossings and
whiskers.

## Referee checklist

- Confirm that annulus plus the stated band is an oriented once-punctured
  torus and that the displayed two loops form its spine.
- Check the direct two-handle quotient calculation in Run 52.
- Confirm that the two certified automorphisms are compared with the paper
  using the same multiplication and basepoint conventions.
- Treat the based actions and Dehn--Nielsen--Baer as an independent control,
  not as the construction of the map.
- Check the direct `c`-collar equivariance and the supported beta twist word
  certified in Run 51.

No fundamental-group simplification, framing theorem, PL smoothing theorem,
or four-manifold classification theorem is part of this packet.

Run 50 uses the resulting map only as an orientation-preserving homeomorphism
from the marked source bundle to the underlying topological manifold of the
paper's already smooth target. It transports the named tori, collars, and
section cycles; it does not assert or require a compatible smoothing of the
source triangulation.
