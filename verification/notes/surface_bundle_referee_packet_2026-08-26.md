# Referee packet for the marked surface-bundle identification

## Purpose and conclusion

This note isolates the theorem called `T_surface_bundle` in the proof ledger.
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
theorem for bundles.  For surface bundles specifically, Baykur--Margalit,
Section 2, state the monodromy classification and use the contractibility of
the identity components of the diffeomorphism group:

- R. Inanc Baykur and D. Margalit, *Indecomposable surface bundles over
  surfaces*, J. Topol. Anal. 5 (2013), 161--181,
  <https://arxiv.org/abs/1209.1162>.
- C. J. Earle and J. Eells, *The diffeomorphism group of a compact Riemann
  surface*, Bull. Amer. Math. Soc. 73 (1967), 557--559,
  <https://doi.org/10.1090/S0002-9904-1967-11746-4>.

The present graph-base argument actually needs less than the full
contractibility theorem: only the identification of components with mapping
classes and homotopy invariance of pullback bundles.

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
be chosen relative to a neighborhood of `e`.  Its mapping torus carries the
product `e`-subbundle and its product collar to the one used in the paper.
This last relative choice is the usual isotopy-extension statement applied
away from the two twist annuli; it does not assert that an arbitrary equality
in the mapping class group automatically preserves an arbitrary curve.

## 4. Exact trust boundary

After the integrated check, the only general facts left in
`T_surface_bundle` are:

1. classification of `F`-bundles by maps to `BDiff+(F)` and homotopy
   invariance under the deformation retraction of the base;
2. identification of genus-2 mapping classes by their outer actions on the
   surface group (Dehn--Nielsen--Baer);
3. the elementary relative isotopy-extension choice for maps already equal
   near the marked curve neighborhoods.

All construction-specific hypotheses are machine-bound: the topology and
marking of the fiber, the topology and two-loop spine of the base, both
based monodromy actions, preservation of `c`, pointwise product behavior on
`e`, and the agreement of the independently extracted crossings and
whiskers.

## Referee checklist

- Confirm that annulus plus the stated band is an oriented once-punctured
  torus and that the displayed two loops form its spine.
- Confirm the standard `BDiff+(F)` classification over that graph.
- Confirm that the two certified automorphisms are compared with the paper
  using the same multiplication and basepoint conventions.
- Apply Dehn--Nielsen--Baer injectivity.
- Check the relative-to-`c` and relative-to-`e` isotopy choices described in
  Section 3.

No fundamental-group simplification, framing theorem, PL smoothing theorem,
or four-manifold classification theorem is part of this packet.
