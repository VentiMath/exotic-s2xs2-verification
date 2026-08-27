# Referee packet for the framing lemma

## Purpose and logical role

Lemma 8.2 identifies the product/fiber push-offs used in the combinatorial
peripheral calculation with the Lagrangian-framing push-offs used to define
the paper's Luttinger surgeries.  This is a bridge into the certified group
presentations, not merely a later symplectic decoration.

If a Lagrangian longitude and the certified product longitude differed by

\[
\lambda_L=\lambda_F+j\mu,
\]

then the Luttinger slope represented in product coordinates would be

\[
\mu+k\lambda_L=(1+kj)\mu+k\lambda_F.
\]

The filled-group certificates prove triviality for the stated product-framed
relations; they do not cover arbitrary values of `j`.  A failure of the lemma
would therefore break the identification of those certificates with the
paper's manifolds.  Simple connectivity, the Freedman classification step,
and the symplectic/Kodaira argument would all become unproved.  The group
certificates would remain valid statements about their literal presentations.

## Statement being checked

For the normalized Thurston form used on the bundle `R`, the two named
push-offs on each surgery torus are constant-momentum copies in a Weinstein
chart.  Hence their classes on the boundary of a tubular neighborhood contain
no meridian component and the product/fiber framing agrees with the
Lagrangian framing.

Only germs near the two surgery tori are required.

## The beta torus

The beta monodromy is the identity near the curve `e`; this is certified by
the literal product stack in Run 22.  Thus its neighborhood is a product over
a base annulus.  Relative Moser provides a fiber chart near `e` in which the
fiber area form is

\[
\Omega_0=dt\wedge d\theta_1.
\]

Writing the base annulus as `(theta_2,u)`, the Thurston form is

\[
\omega=dt\wedge d\theta_1+K,du\wedge d\theta_2.
\]

These are canonical cotangent coordinates with momenta `(t,Ku)`.  Both the
in-fiber displacement and the base-normal displacement hold the momenta
constant, so their boundary classes have no meridian term.

## Relative Moser calculation

On an annular collar write

\[
\Omega=f(\theta,t),dt\wedge d\theta,
\qquad f>0,
\qquad \Omega_0=dt\wedge d\theta,
\]

and define

\[
g(\theta,t)=\int_0^t(f(\theta,\tau)-1),d\tau,
\qquad \zeta=g,d\theta.
\]

Then `g(theta,0)=0` and

\[
d\zeta=(f-1),dt\wedge d\theta=\Omega-\Omega_0;
\]

the `theta` derivative wedges with `dtheta` and vanishes.  Put

\[
\omega_s=(1-s)\Omega_0+s\Omega.
\]

Its coefficient is `(1-s)+sf>0`.  The unique vector field satisfying
`i_Xs omega_s=-zeta` is tangent to the `t` direction with coefficient
`-g/((1-s)+sf)`, hence vanishes on the core.  On a sufficiently small fixed
collar of the compact core its time-dependent flow exists for `0<=s<=1`,
fixes the core, and satisfies

\[
\frac d{ds}(\varphi_s^*\omega_s)
=\varphi_s^*(d\zeta+d\iota_{X_s}\omega_s)=0.
\]

Thus `varphi_1^* Omega=Omega_0`.  The coefficient identities, positivity
reduction, vanishing on the core, and sign cancellation are checked by
`luttinger/framing_check.py`.

## Equivariant normalization at the alpha torus

Run 22 certifies that the alpha monodromy restricts to a free,
orientation-preserving half-rotation on a collar of `c`.  Its quotient is an
annulus, the invariant area form descends, and the preceding relative Moser
argument applies downstairs while fixing the quotient core.

The resulting downstairs map induces the identity on the fundamental group,
so it lifts to the connected double cover.  Conjugating the original deck
map by this lift gives a deck transformation covering the identity.  It is
nonidentity because it is conjugate to the original nonidentity map.  The
deck group has two elements, so the conjugate equals the original deck map;
the lift is equivariant.

In standard quotient coordinates the covering is
`bar_theta=2 theta`.  Therefore

\[
q^*(dt\wedge d\bar\theta)=2,dt\wedge d\theta.
\]

Replacing `t` by `t_1=2t` absorbs the factor, and the deck map is
`(theta_1,t_1) -> (theta_1+pi,t_1)`.  The order-two deck calculation and the
factor-two rescaling are checked by `luttinger/framing_check.py`.

## The alpha Weinstein chart

The mapping-torus seam is

\[
(\theta_1,t,2\pi,u)\sim(\theta_1+\pi,t,0,u).
\]

Define

\[
\Theta_1=\theta_1-\tfrac12\theta_2,
\quad \Theta_2=\theta_2,
\quad P_1=t,
\quad P_2=\tfrac12t+Ku.
\]

Across the seam `Theta_1` changes by `2pi`, so it descends as a circle
coordinate.  Direct exterior algebra gives

\[
dP_1\wedge d\Theta_1+dP_2\wedge d\Theta_2
=dt\wedge d\theta_1+K,du\wedge d\theta_2.
\]

The fiber displacement has constant momentum `(t_0,t_0/2)`.  The closed
base-direction drift has constant `Theta_1` and momentum `(0,Ku_0)`.  The
seam, symplectic-form, and constant-momentum identities are checked exactly
by `luttinger/framing_check.py`.

## Chart independence and the precise citation

Auroux--Donaldson--Katzarkov, *Luttinger surgery along Lagrangian tori and
non-isotopy for singular symplectic plane curves*, Math. Ann. 326 (2003),
185--203, Section 2.1 and Proposition 2.2,
<https://doi.org/10.1007/s00208-003-0418-9>, states that the identification of
a neighborhood of a Lagrangian torus with a neighborhood of the zero section
in its cotangent bundle is canonical up to isotopy, and proves independence
of the choices entering the surgery construction.  The freely available
author PDF is <https://people.math.harvard.edu/~auroux/papers/lagrsurg.pdf>.

For the use here, an isotopy of the neighborhood identification preserves the
homotopy class on the boundary of a sufficiently small constant-momentum
push-off.  Thus exhibiting the named curves as constant-momentum copies in
the explicit charts determines the canonical Lagrangian-framing classes.

The ADK proposition supports this last independence statement; it does not
replace the explicit local calculations above.

## Exact remaining trust boundary

Runs 43--44 discharge chart/framing independence. Run 46 avoids the lifting
criterion by defining the Moser vector field directly upstairs and deriving
equivariance from uniqueness. Run 47 then supplies that existence and
uniqueness constructively for general positive `f`: the flow is the unique
radial inverse of the strictly increasing cumulative coordinate
`H_s(theta,t)=t+s integral_0^t(f-1)`. Thus the normalization has no remaining
separately cited smooth-topology or ODE theorem; its residual analysis is
ordinary one-variable differentiation, integration, and monotone inversion.

The quotient is an annulus, positivity, preservation of sides, fixed-core
condition, deck-group calculation, factor-two normalization, mapping-torus
seam, and both constant-momentum assertions are all supplied explicitly.
No framing discrepancy has been found.

References for these inputs are:

- J. Moser, *On the volume elements on a manifold*, Trans. Amer. Math. Soc.
  120 (1965), 286--294,
  <https://doi.org/10.1090/S0002-9947-1965-0182927-5>.  Here the paper's
  displayed relative primitive makes the usual Moser vector field vanish on
  the core, giving the relative form needed above.

## Referee checklist

- Confirm the Run 47 cumulative-coordinate inverse on a common collar and
  its differentiated Moser identity.
- Confirm the direct upstairs field in Run 46 projects correctly and that ODE
  uniqueness gives its equivariant flow.
- Confirm either of the independent chart arguments in Runs 43--44.
- Confirm that the paper's two developed based words are the two curves whose
  constant-momentum representatives are displayed here; that separate bridge
  is documented in `notes/peripheral_identification_lemma_2026-08-24.md`.
