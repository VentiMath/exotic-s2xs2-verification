# Direct PL self-intersection certificate (2026-08-24)

> **v2.0.0 semantic clarification.** The target of the transport discussed
> below is the audit-defined smooth bundle `R_*`. Its comparison with
> Wuebben's intended target is conditional on S1--S4.

## Result

The closed fixed-point section `Gamma_hat` in the doubled marked bundle has

    Gamma_hat . Gamma_hat = 0.

This is now witnessed by an explicit simplicial normal push-off, rather than
being inferred only from spin parity or from an abstract normal-Euler-number
calculation. The replayable computation is
`luttinger/pl_self_intersection.py`; its recorded output is `runs/28`.

## What is extracted from the existing triangulation

The program builds the already certified bundle `K` and takes the full
subcomplex on vertices whose fiber coordinate is the fixed vertex `p`. It
finds an orientable once-punctured torus with f-vector

    [102, 243, 140],

Euler characteristic `-1`, and one 66-edge boundary circle. This is the PL
section `Gamma` in one half.

The link of `p` in the actual marked fiber is a 24-cycle. The simplicial
half-turn `phi0` sends link vertex `i` to `i+12`, exactly the PL form of the
derivative `-I`. The complete 32-level beta flip stack has no flip cone in
the star of `p`, so the other monodromy is a literal product near the section,
the PL form of derivative `I`. Four equally spaced rays coarsen the normal
circle equivariantly: `phi0` acts on them by the two-step half-turn.

Thus the local normal data used here are read from the marked triangulation;
they are not inserted as a separate hand-drawn normal bundle.

## The doubled PL normal neighborhood

Two copies of the extracted punctured torus are glued by an
orientation-reversing simplicial map on their boundary cycles. The result is
a closed orientable genus-2 triangulation with f-vector

    [138, 420, 280].

Over each half the program takes the cone on the four-ray normal circle. On
the common boundary it glues the normal disks by a constant cyclic rotation.
It separately constructs all four possible simplicial rotations. This covers
the only relevant PL data of the paper's constant orientation-preserving
derivative: every constant map into `GL+(2,R)` is homotopic through constant
maps to a rotation, and changing that constant rotation does not create
winding around the boundary circle.

Each of the four resulting disk neighborhoods has f-vector

    [690, 6564, 17632, 18480, 6720].

Every triangle of the zero section has one 8-step normal link circle.

## The push-off and intersection count

Choose one of the four normal rays on the first half. On the second half,
choose its inverse image under the clutching rotation. These choices agree on
the seam and therefore form a closed simplicial section of the normal circle
bundle. The program verifies that this push-off:

1. has the same f-vector as `Gamma_hat`;
2. has no vertex in common with `Gamma_hat`, hence their PL realizations are
   disjoint;
3. is joined to `Gamma_hat` by the induced radial 3-chain;
4. has radial-chain boundary exactly the union of the two sections, with no
   additional seam component, including oriented coefficients `+/-1`; and
5. gives an empty list of transverse local intersection signs.

Consequently the signed intersection sum is the sum of the empty list,
namely zero. Since the second section is explicitly the normal push-off of
the first, this signed intersection is the self-intersection of `Gamma_hat`.

## Logical boundary

The machine certificate establishes the PL calculation for the marked
triangulation and for every constant orientation-preserving clutching
rotation. Applying it to the paper still uses the already isolated geometric
identification of the marked PL bundle with the smooth Lidman--Piccirillo
bundle, and the paper's statement that the fiber derivative of the boundary
gluing is independent of the boundary parameter. It does not assume that the
section has square zero, and it does not use simple connectivity, spin parity,
or the downstream intersection-form argument.

This closes the former R3 computational gap. The remaining trust is the same
PL/smooth marked-bundle identification already recorded elsewhere, not an
uncomputed self-intersection.

Run-36 update (2026-08-25): the marked PL/smooth identification and
intersection-category step are now stated separately in
`notes/pl_bridge_referee_packet_2026-08-25.md`. The integrated checker
recomputes all four clutching cases. Because the radial chain makes the
disjoint push-off homologous to the section, the smooth conclusion uses only
naturality of the homological intersection pairing; the literal PL push-off
does not itself need to be smoothed.

Run-50 update (2026-08-27): the source triangulation no longer needs a
compatible smoothing at all. The marked surface-bundle homeomorphism carries
the two actual disjoint cycles and their bounding radial 3-chain into the
underlying topological manifold of the paper's already smooth bundle. They
remain disjoint and homologous there, so the target section class has square
zero directly. This removes the separate intersection-naturality and
four-dimensional source-smoothing nodes from the proof ledger.
