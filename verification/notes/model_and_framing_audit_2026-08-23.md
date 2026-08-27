# Marked-bundle and framing audit (2026-08-23)

## Conclusion

The triangulated object used by the independent computation is not merely a
bundle with matching fingerprints. Its marked fiber, based monodromies, and
two surgery subbundles agree with the data defining Wuebben's/Lidman--
Piccirillo's (R,T_\alpha,T_\beta). Subject to the standard classification of
surface bundles over a surface with boundary, this closes the former
"possibly a nearby manifold" gap.

The displayed algebra in framing Lemma 8.2 also checks. The apparent Moser
sign problem in plain-text extraction disappears when the PDF's subscripts
are restored: the interpolation is

\[
\omega_s=(1-s)\Omega_0+s\Omega,
\qquad d\zeta=\Omega-\Omega_0,
\qquad \iota_{X_s}\omega_s=-\zeta.
\]

Consequently \(\partial_s\omega_s+d\iota_{X_s}\omega_s=0\).

## Executable correspondence

`luttinger/model_correspondence.py` checks:

1. The fiber is a closed orientable genus-2 surface. The five curves are a
   filling ordered five-chain; their complement consists of the two disks
   containing (p,O).
2. The involution is a simplicial half-turn with exactly those two fixed
   points and sends (a\leftrightarrow e), (b\leftrightarrow d), while
   restricting to a free half-rotation of (c).
3. The literal (p)-based loops satisfy
   \(\phi_0(x,y)=(r,s)\), not merely the corresponding free homotopy classes.
4. The open beta stack has the exact based action
   \(x\mapsto y^{-1}, y\mapsto yx, r\mapsto r, s\mapsto s\), with 17,839
   proof-producing Tietze steps replayed.
5. Every flip cone in that stack misses (e), and all 256 edge-level squares
   of (e\times I) are literal product squares. Hence \(\psi_0\) fixes the
   torus fiber (e) pointwise in the constructed representative.
6. The assembled four-complex has Euler characteristic 2, every tetrahedron
   has one or two 4-simplex cofaces, and its boundary is a connected closed
   3-pseudomanifold.
7. The two specified vertex sets induce exactly two disjoint closed tori,
   giving the mapping torus (c\rtimes_{\phi_0}S^1=T_\alpha) and the product
   (e\times S^1=T_\beta).

The base construction is an annulus with one band joining its two boundary
components, hence a once-punctured torus. It retracts to the two generator
loops. An oriented surface bundle over this base is fixed, up to bundle
equivalence, by the two based mapping classes. The based Dehn--Nielsen--Baer
injection makes the exact automorphisms above stronger than the needed
mapping-class comparison. Thus the marked fiber identification of Lemma 7.1
extends to the required bundle equivalence and carries the two subbundles to
the two triangulated tori.

## Framing calculation

`luttinger/framing_check.py` checks the exact exterior-algebra and seam
identities in Lemma 8.2. For

\[
\Theta_1=\theta_1-\tfrac12\theta_2,\quad
\Theta_2=\theta_2,\quad P_1=t,\quad P_2=\tfrac12t+Ku,
\]

it verifies

\[
dP_1\wedge d\Theta_1+dP_2\wedge d\Theta_2
=dt\wedge d\theta_1+Kdu\wedge d\theta_2.
\]

Across the mapping-torus seam, \(\Theta_1\) changes by exactly (2\pi), so
it is a well-defined circle coordinate. The fiber push-off has constant
momentum \((t_0,t_0/2)\), and the drifting base push-off has constant momentum
\((0,Ku_0)\). Neither acquires a meridian component in this chart.

The remaining ingredients are standard smooth/symplectic results rather than
unchecked coordinate assertions: relative Moser on an annulus, lifting the
normalization through the free involution quotient, and independence of the
Lagrangian framing from the Weinstein chart. The hypotheses required for
each are present in the lemma. No substantive framing error was found.

Update (2026-08-25): Run 35 now checks the relative primitive, positivity
reduction, Moser vector-field equation, double-cover deck calculation, and
factor-two rescaling as well. It verifies the precise ADK03 citation and
isolates the remaining standard inputs in
`notes/framing_lemma_referee_packet_2026-08-25.md`. That packet also corrects
the dependency footprint: this framing bridge is upstream of the certified
filled presentations, not merely of the later symplectic conclusion.

## Implementation issue found

The new top-level audit exposed a stale coding error in `check_fiber`: its
orientability traversal referred to an uninitialized triangle-neighbor table.
The table is now constructed explicitly. The repaired test passes. This bug
affected an assertion routine, not the surface construction or any exported
group relator.

## Current proof boundary

The group computation is conditional on standard PL and symplectic topology,
but no longer on an unidentified global correspondence. A fully formal proof
assistant development would still need formal versions of surface-bundle
classification, relative/equivariant Moser, and Weinstein neighborhood
invariance. For a conventional journal proof, these are legitimate cited
theorems.

Run 31 adds an independent assembly check. A second implementation constructs
a different, 64-interface triangulation without importing the original bundle
or layer modules. It recovers the same marked beta homology action and the same
peripheral semantics. This does not replace the exact based-monodromy proof
above: the two routes still share the marked fiber, and interpreting the
paired annular shear as the stated Dehn twists uses the standard PL flip-trace
fact now exposed in the proof ledger.

Run 32 removes the first limitation in that sentence: a separate 34,735-step
Tietze certificate now proves the full based action of the alternative trace,
not merely its homology action. The shared marked fiber and the local PL
interpretation of the flip trace remain explicit boundaries.

Run 33 computationally resolves the local part of the latter boundary. It
checks all 128 cone links and stars, the labeled floor/roof diagonals and side
squares, every untouched prism, both ends of every slab, and all vertex links
of the complete trace. The remaining external statement is only the elementary
PL interpretation of the verified labeled 2-2 cone-ball.

Run 34 independently reconstructs the marked fiber itself. Its 58-vertex
vertex-disk/edge-band triangulation imports no primary fiber code and has the
same canonical equivariant ribbon data as the 86-vertex plumbing: all crossing
rotations, both p/O faces, and the involution on every directed curve end.
The certificate also records explicit common subdivisions of every compressed
curve segment. This removes the former shared-fiber software boundary.

Run 36 integrates these PL facts with the Run-28 section push-off and gives
the residual rotation-system, bistellar-trace, dimension-four smoothing, and
intersection-naturality statements explicit proofs or precise citations. See
`notes/pl_bridge_referee_packet_2026-08-25.md`.
