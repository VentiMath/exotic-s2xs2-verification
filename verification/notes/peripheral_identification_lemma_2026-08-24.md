# Peripheral identification lemma

> **v2.0.0 semantic clarification.** This note proves the peripheral
> identification inside the audit-defined model. Applying the paper's names
> to those paths is the source-semantic assumption S3, not a conclusion of the
> certificate alone.

> **Evidence correction (2026-08-29).** The original version cited Run 15 as
> an elementary-Tietze proof that `lb_a_y1 = A x`. That historical reduction
> was tied to a pre-export coordinate state and does not reproduce over either
> committed export. The equality itself is now proved over the sealed
> 3-generator, 78-relator complement by Run 68: a 61-step reduction of the
> literal 72-letter residual, backed by a 2,506-record KBMAG ancestry DAG and
> replayed independently in Python and Ruby. References below have been
> corrected to distinguish the valid conclusion from the superseded evidence.

Date: 2026-08-24

Evidence snapshot: commits `661e810` and `dad49cf`.

Paper: B. J. Wuebben, *An exotic S2 x S2 and an exotic CP2#CPbar2*,
[arXiv:2608.17267](https://arxiv.org/abs/2608.17267), especially Sections
2.1, 7.1-7.3, 8.2-8.7, and Appendix A.3.

## Purpose

This note supplies the conventional mathematical bridge between the paper's
marked smooth bundle and the independently triangulated model. It does not
repeat the finite-presentation calculation. Its only purpose is to justify
that the two literal meridian/longitude pairs filled in the computation are
the two peripheral pairs specified in the paper.

The statement is deliberately restricted to the paper's reference `n = 0`
section. The adjacent `n = 1` section is a robustness calculation and is not
needed here.

## Notation

On the paper side, let

- `F_LP` be the marked genus-2 fiber of [LP25, Figure 1];
- `phi_0` be its involution and `psi_0 = T_a T_b` its second monodromy;
- `R -> T_0` be the resulting bundle over the once-punctured torus;
- `T_alpha = c rtimes_{phi_0} S1` and `T_beta = e x S1` be the surgery tori;
- `p` be the fiber basepoint and `q` the cut-square basepoint;
- `A = [alpha_bar]^-1` and `B = [beta_bar]^-1` as in Convention 7.2;
- `M` be the meridian of `T_alpha` based along the initial segment `y_1`;
- `N` be the meridian of `T_beta` based along the initial segment `s_2`;
- `lambda_alpha` and `lambda_beta` be the base-direction Lagrangian
  push-offs used for the two surgeries.

On the combinatorial side, let

- `K` be the complex built by `luttinger/bundle.py`;
- `T_alpha^K` and `T_beta^K` be its two induced torus components;
- `C^K` be the induced-complement model used by
  `luttinger/complement.py`;
- `geom_M`, `geom_N`, `lb_a_y1`, and `lb_b_s2` be the four literal based
  boundary loops exported by `luttinger/r_run.py`.

The symbols `x,y,r,s,A,B,M,N` below denote based loops, not merely free
homotopy classes.

## Standard inputs

The proof uses the following conventional topology. These are theorem inputs,
not results of the Python checks.

1. **Marked graph clutching.** Run 52 constructs the bundle map directly on
   the two mapping-cylinder handles. The exact alpha conjugacy and identical
   supported beta twist word make `[x,t] -> [h(x),t]` well-defined in both
   directions. Dehn--Nielsen--Baer is retained only as an independent check.
2. **PL mapping-cylinder realization.** The trace of each elementary
   bistellar flip is a PL product cobordism with the prescribed boundary
   identification. Gluing the traces and staircase products in
   `layers.py` and `bundle.py` therefore triangulates the surface bundle with
   the represented monodromies. Product neighborhoods of the marked curves
   give locally flat regular neighborhoods of the two torus subbundles.
3. **Derived regular neighborhoods.** For a full locally flat subcomplex,
   the derived neighborhood is a regular neighborhood, its frontier is the
   normal boundary, and the complement deformation retracts to the induced
   subcomplex on the remaining vertices. This is the PL result used in
   `complement.py` (Rourke-Sanderson, Chapter 3).

   **Run-49 replacement.** For the actual two tori, the theorem invocation is
   now superseded by an explicit construction. The normal block neighborhood
   is the barycentric half-weight region `sum_T(lambda)>=1/2`, and
   `b(s) -> (b(s intersect T)+b(s minus T))/2` is a globally checked PL
   homeomorphism from the computed mixed-face frontier to its boundary. All
   592 dual triangle loops are checked as literal normal-circle fibers.
4. **Framing normalization.** Relative Moser on an annulus, its equivariant
   lift through a free double cover, and independence of the Lagrangian
   framing from the chosen Weinstein chart apply in the neighborhoods used in
   paper Lemma 8.2.

No classification of closed 4-manifolds and no Floer-theoretic input enters
this lemma.

Run-36 update (2026-08-25): the PL mapping-cylinder, equivariant ribbon
thickening, and compatible-smoothing inputs are now separated and cited in
`notes/pl_bridge_referee_packet_2026-08-25.md`; their construction-specific
hypotheses are replayed by `luttinger/pl_theorem_audit.py`.

Run-50/52 update (2026-08-27): no compatible smoothing of the PL source is
needed. Explicit graph clutching supplies a homeomorphism into the
underlying topological bundle of the paper's already smooth `R`; all smooth
framing operations are performed on `R` after transport.

## Lemma

**Peripheral identification.** There is an orientation-preserving marked
bundle homeomorphism

```text
H: |K| -> R_top
```

over the marked once-punctured-torus base with the following properties.

1. On the reference fiber, `H` carries the combinatorial ordered five-chain
   `(a,b,c,d,e)` to the paper's ordered five-chain, carries the two fixed
   points to `p,O`, and identifies the literal based fiber loops
   `x,y,r,s`.
2. It carries `T_alpha^K` to `T_alpha` and `T_beta^K` to `T_beta`.
3. The induced complement identification carries the commonly based
   combinatorial peripheral pairs

   ```text
   (geom_M, lb_a_y1),   (geom_N, lb_b_s2)
   ```

   to the paper's pairs

   ```text
   (M, lambda_alpha),   (N, lambda_beta),
   ```

   up to the orientation inversions explicitly allowed by Convention 2.1(C7)
   and up to simultaneous conjugacy from changing a common whisker.
4. For the normalized Thurston symplectic form in Lemma 8.2, the two
   combinatorial product/fibered push-offs have zero meridian component and
   are exactly the Lagrangian-framing push-offs.

Consequently, for each surgery-sign pair `(e_alpha,e_beta)` in
`{+1,-1}^2`, the normal closure added to the triangulated complement is the
normal closure prescribed by Luttinger surgery on the paper's two tori:

```text
<< geom_M * lb_a_y1^e_alpha,
   geom_N * lb_b_s2^e_beta >>

=

<< M * lambda_alpha^e_alpha,
   N * lambda_beta^e_beta >>
```

after the corresponding convention signs are matched. Thus the four direct
`n0_y1` filled presentations are presentations of the four convention choices
for the paper's specified surgery, rather than presentations of a nearby
pair of framed tori.

## Proof

### 1. The marked fiber is the paper's fiber

Paper Lemma 7.1 proves that an ordered filling five-chain on the genus-2
surface, together with the chain-reversing involution and its two fixed
points, has the equivariant normal form shown in Figure 1. The proof is not a
homology-only argument: the five-chain is a filling ribbon graph, its
complement is two disks, the ribbon-graph equivalence thickens, and the
extension over the two disks is equivariant and carries the branch points.

The combinatorial fiber passes precisely these hypotheses:

- it is a closed orientable genus-2 surface;
- consecutive members of `(a,b,c,d,e)` meet once and all other pairs are
  disjoint;
- the chain complement consists of two disks containing `p` and `O`;
- the simplicial half-turn exchanges `a <-> e`, `b <-> d`, preserves `c`,
  and has exactly the fixed points `p,O`.

These are checked in `fiber.py` and collected by
`model_correspondence.py`; the recorded output is
`runs/22-model-correspondence-and-framing.txt`. Run 34 independently
reconstructs the surface by vertex disks and edge bands, then verifies the
identical equivariant marked ribbon code—including both p/O faces and the
involution on every directed curve end—against the primary plumbing. Lemma
7.1 therefore supplies
an orientation-preserving equivariant marked diffeomorphism between the
paper fiber and the combinatorial fiber. In particular, `c` and `e` are the
paper's actual embedded curves, not substitutes with the same homology.

The loops used by the computation are literal edge loops from `p`.
`paper_bridge.py` verifies

```text
phi_0(x) = r,   phi_0(y) = s
```

as identities of vertex paths. It also verifies that `[x,y][r,s]` is the
surface relator and that the named loops have the orientations used in the
paper dictionary. This removes the inner-automorphism ambiguity that would
remain if only unbased mapping classes had been compared.

### 2. The two monodromies determine the same marked bundle

The base model in `bundle.py` is an annulus with one band joining its boundary
components. It is a once-punctured torus and retracts to the two loops carrying
the alpha and beta monodromies.

On the alpha loop, the combinatorial monodromy is the literal half-turn, with
based action

```text
x <-> r,   y <-> s.
```

On the beta loop, `paper_bridge.py` transports the complete whiskered edge
loops through the open flip stack. The proof-producing reduction gives

```text
x -> y^-1,   y -> yx,   r -> r,   s -> s,
```

which is the paper's based lift of `psi_0 = T_a T_b`. The 17,839 elementary
Tietze steps are replayed before this result is accepted. Since the marked
actions agree on the two-loop spine, the standard classification of marked
surface bundles over that spine extends the fiber identification to a bundle
equivalence `H`.

There is also a relative statement, not just an equality in the unmarked
mapping-class group. Lemma 7.1 makes the alpha involutions equivariantly
conjugate and carries `c` itself to `c`. For the beta monodromy, both models
use the same ordered Dehn twists about the marked curves `a,b`; their twist
annuli can be identified by the marked fiber diffeomorphism and are disjoint
from `e`. Thus the comparison isotopy can be chosen relative to a
neighborhood of `e`. This is what permits the bundle equivalence below to
preserve the torus subbundles and their product collars.

This is stronger than the earlier comparison of subgroup fingerprints: the
bundle identification uses the actual marked mapping classes. The
mapping-cylinder construction supplies a triangulation of this bundle, not
an unrelated pseudomanifold having the same fundamental-group invariants.

### 3. The bundle equivalence carries the two surgery tori

The paper places

```text
T_alpha = c rtimes_{phi_0} S1,
T_beta  = e x S1.
```

The two induced vertex sets in `bundle.py` have exactly these descriptions.
`model_correspondence.py` checks that they induce two disjoint connected
closed tori. More specifically:

- on `c`, the alpha monodromy is the literal free half-rotation;
- every flip cone in the beta stack misses `e`, and every square of
  `e x I` is a literal product square, so the beta monodromy fixes `e`
  pointwise in the chosen representative.

The equivariant alpha identification and relative beta identification from
Step 2 therefore make the bundle equivalence relative to these subbundles. It
sends the two combinatorial tori to the paper's tori, and their normal product
directions to the fibered normal directions used in Sections 8.4-8.7.

### 4. The combinatorial meridians are the geometric meridians

Both tori are full locally flat subcomplexes. In the first derived
triangulation, `complement.py` uses the frontier of their derived regular
neighborhood. The boundary of the dual two-cell to an oriented torus triangle
is a meridian. `oriented_meridian_loop` orients it from the orientations of
the ambient four-complex and torus.

For `T_alpha`, `geom_M` is this oriented dual meridian joined to the global
basepoint by the literal initial segment `y_1` from `p` to the unique crossing
`c_y`, followed by a normal segment inside the crossing star. This is exactly
the definition of `M` in paper Section 8.3 and Remark 7.3.

For `T_beta`, the alpha transport square of `s` has one transverse
`T_beta` intersection at `s_e`. Removing that point produces a boundary
detour. The local complement has infinite-cyclic meridian group, and the
replayed local Tietze certificate distinguishes the detour from its inverse.
The outer-boundary connector then gives

```text
N = A * N_grid^-1 * A^-1,
```

with the `s_2` basing and the orientation required by
`AsA^-1 = N y`. These are Runs 13 and 14. Thus `geom_N` is the paper's `N`,
not an arbitrary conjugate selected because it simplifies the group.

Reversing an ambient or torus orientation reverses the corresponding
meridian. That is precisely an allowed C7 sign change. It changes neither the
geometric surgery family being checked nor the validity of the identification.

### 5. The push-offs use the same whiskers and the same fibered framing

The alpha loop `lb_a_y1` is constructed at the unique `c_y` crossing, uses
the same `y_1` whisker as `geom_M`, traverses `A`, and closes along the
chosen half of `c`. The sealed complement certificate gives

```text
lb_a_y1 = A x
```

in the complement group (Run 68; Run 15's earlier evidence is superseded).
This is the paper's reference `n = 0`
section `lambda_alpha`, not the adjacent `A r^-1` section.

The beta loop `lb_b_s2` starts at the unique `s_e` crossing, uses the same
literal `s_2` whisker as `geom_N`, traverses `B`, and is pushed in the
fiber-normal direction. The swept basing square has exactly one interior
intersection with `T_alpha`; puncturing the square produces the same
conjugated meridian and path used in the corrected `BsB^-1` relation. This is
the paper's Section 8.5 construction of `lambda_beta`. In the orientation
convention selected by the triangulation, the coordinate expression is

```text
lambda_beta = (r^-1 M r) B.
```

Run 69 proves this exact coordinate identity in the sealed complement: the
113-letter word `lb_b_s2^-1 * geom_r^-1 * geom_M * geom_r * geom_B` reduces
to the identity in 82 steps, whose full 1,540-record ancestry cone is replayed
by independent Python and Ruby verifiers. No filling relation is present.
The direct filling is even more primitive: it uses the literal `lb_b_s2`
boundary loop rather than relying on the substitution.

The short normal jogs from the fiber whiskers to the derived-neighborhood
frontier lie in the product collar. Moving such an endpoint within the same
boundary three-torus changes the two elements by a common rebasing. A change
of the global whisker simultaneously conjugates the meridian and longitude;
their filling normal closure is unchanged. There is therefore no step at
which the meridian and its surgery direction receive unrelated basings.

### 6. The fibered framing is the Lagrangian framing

It remains possible in principle for the correct topological push-off to
differ from the Lagrangian push-off by a meridian. Paper Lemma 8.2 rules this
out for the normalized Thurston form used in the construction.

Near `T_beta`, `psi_0` is the identity near `e`, so the neighborhood is a
genuine product. After relative Moser, the form is

```text
dt ^ dtheta_1 + K du ^ dtheta_2,
```

and the in-fiber and base-normal push-offs have constant momenta.

Near `T_alpha`, the collar of `c` is a free half-rotation. Equivariant Moser
normalizes it to `(theta_1,t) -> (theta_1 + pi,t)`. In the mapping-torus
quotient, the coordinates

```text
Theta_1 = theta_1 - theta_2/2,
Theta_2 = theta_2,
P_1 = t,
P_2 = t/2 + K u
```

are well defined and satisfy

```text
dP_1 ^ dTheta_1 + dP_2 ^ dTheta_2
    = dt ^ dtheta_1 + K du ^ dtheta_2.
```

The fiber push-off has constant momentum `(t_0,t_0/2)` and the half-drifting
base push-off has constant momentum `(0,K u_0)`. Hence neither push-off has a
meridian component. `framing_check.py` independently verifies the relative
primitive and Moser equation, convex-positivity reduction, double-cover and
factor-two calculations, exterior algebra, `2*pi` seam shift, and both
constant-momentum statements; Run 35 records the extended results. Local flow
existence, connected-cover lifting, and Lagrangian-neighborhood germ
uniqueness are the standard theorem inputs isolated in the referee packet.

Thus the product/fibered framing used to construct `lb_a_y1` and `lb_b_s2`
is the Lagrangian framing used by the paper.

### 7. The filling relations agree

Luttinger surgery adds the normal closure of a commonly based meridian times
the appropriate power of its Lagrangian push-off. Steps 1-6 identify the two
literal combinatorial pairs with the paper's two pairs. Simultaneous
conjugacy does not change a normal closure, and the possible inversions are
exactly the convention signs enumerated by the four direct `n0_y1` cases.
This proves the displayed equality of normal closures and the lemma. `square`

## Exact evidence chain

| Mathematical assertion | Evidence | Trust type |
|---|---|---|
| Marked filling five-chain and involution | paper Lemma 7.1; `fiber.py`; `model_correspondence.py`; Run 22 | paper proof plus finite combinatorics |
| Literal based `phi_0` action | `paper_bridge.py`; Runs 12 and 22 | finite path check |
| Literal based `psi_0` action | `paper_bridge.py`; 17,839-step replay; Runs 12 and 22 | replayed Tietze certificate |
| Two torus subbundles | `bundle.py`; `model_correspondence.py`; Runs 22, 51--52 | finite combinatorics plus explicit mapping-cylinder clutching |
| `M` with `y_1` basing | `r_run.py`; Run 12 | derived-neighborhood dual meridian |
| `N` with `s_2` basing and orientation | `r_run.py`; Runs 13-14 | local rank-one and boundary-chain certificates |
| `lambda_alpha = Ax` | sealed presentation; Run 68 | 2,506-record KBMAG ancestry certificate, replayed in Python and Ruby |
| `lambda_beta = (r^-1 M r)B` with `s_2` basing | `r_run.py`; Runs 10, 12, 20, and 69 | punctured sweep and direct boundary path; 1,540-record sealed-complement ancestry certificate replayed in Python and Ruby |
| Fibered equals Lagrangian framing | paper Lemma 8.2; `framing_check.py`; Run 35 | three named smooth theorems plus full inline-calculus audit |
| Four direct `n = 0` filling pairs | `r_presentations.json`; Run 20 | literal path export; no coordinate substitution |

## What is not used

The proof does not use:

- the old arbitrary-`c[0]` or arbitrary-`e[0]` peripheral coordinates;
- the weak low-index fingerprint `[[0,0],[1,3,7,26]]`;
- the unresolved alternate beta formula involving `x M_y2 x^-1`;
- the adjacent `n = 1` section;
- triviality of the filled groups.

In particular, the peripheral identification is logically prior to the KBMAG
calculation. It cannot be justified by the fact that the resulting groups
happen to be trivial.

## Residual trust and falsification targets

This is a conventional proof, not a proof-assistant formalization. The
remaining ways to overturn it are now localized:

1. exhibit an error in the claim that an elementary flip trace used by
   `layers.py` is a relative PL product;
2. exhibit a mismatch between the two based monodromy mapping classes despite
   the certified actions on the genus-2 surface group;
3. exhibit a failure of the marked bundle equivalence to be chosen relative
   to `c` and `e`;
4. exhibit a failure of a derived-neighborhood dual loop to be the oriented
   normal meridian;
5. exhibit a violated hypothesis in the relative/equivariant Moser or
   Weinstein-framing argument of Lemma 8.2;
6. independently trace either common whisker and obtain a nonconjugate
   peripheral pair.

Items 1-5 are precise standard-topology questions suitable for expert review.
Update 2026-08-25: Item 6 has now been carried out by
`independent_peripheral_extractor.py` (Run 30). The separate implementation
recovers both commonly based pairs without importing the original complement,
path, sweep, or peripheral modules. Items 1-5 remain standard-topology review
targets; none is an unspecified “the words may be wrong” objection anymore.
