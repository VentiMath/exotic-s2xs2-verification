# Lemma 8.2: independence of the Weinstein chart

## Exact statement needed

Let `T` be a Lagrangian torus and let two Weinstein charts identify germs of
its neighborhood with germs of the zero section in `T^*T`. For an embedded
curve `gamma` in `T`, a sufficiently small constant-momentum copy in either
chart determines the same isotopy class in `nu(T)-T`. Consequently changing
the chart cannot add a meridian to the framing push-off.

This is the only chart-independence consequence used by Lemma 8.2.

## Reduction to charts fixing the zero section

If the charts induce different parameterizations of `T`, precompose one with
the cotangent lift of the resulting base diffeomorphism `h`. On a torus,
decompose `h` into an affine representative of its mapping class followed by
an isotopy. The affine part sends constant covectors to constant covectors;
the cotangent lifts of the isotopy give a homotopy through nowhere-zero
covector sections. Any two nonzero constant covectors are likewise joined in
`R^2-{0}`. These changes therefore give isotopies of the corresponding small
push-offs in the complement. We may reduce to charts that restrict to the
identity on `T` and to the same constant covector.

After shrinking to a common neighborhood, their transition is a
symplectomorphism germ `F:(T^*T,T)->(T^*T,T)` fixing the zero section
pointwise.

## Symplectic Alexander trick

Let `delta_r(q,p)=(q,rp)` be fiber dilation. Although `delta_r` is conformally
symplectic, `delta_r^*omega=r omega`, so the factors cancel in

    F_r = delta_r^-1 F delta_r,       0 < r <= 1.

Every `F_r` is therefore symplectic and fixes the zero section. Taylor
expansion along that section and the symplectic condition give

    dF = [I A; 0 I],   A=A^T.

It follows directly that `F_r` extends smoothly to `r=0` with `F_0=id`. In
the first jet the path is `[I,rA;0,I]`; its exact block algebra is checked
without external symbolic libraries by
`luttinger/weinstein_chart_independence.py`.

This is an isotopy through symplectomorphism germs, relative to the zero
section, from the identity to the chart transition.

## Effect on the framing push-off

Choose the constant-momentum copy of `gamma` sufficiently small that the
compact family `F_r` is defined on it. The curves

    r -> Phi_1(F_r(gamma_epsilon))

form an isotopy in `nu(T)-T` between the push-offs from the two charts. No
member meets `T`: after shrinking the germ, every `F_r` is a local
diffeomorphism preserving `T`, with inverse image of `T` equal to `T`.

Thus the boundary class is independent of the chart. In particular, an
explicit chart in which the fibered copies are constant-momentum copies proves
their meridian coefficient is zero in the canonical Lagrangian framing.

## Relation to ADK03

Auroux--Donaldson--Katzarkov, Section 2.1 and Proposition 2.2, state that the
cotangent-neighborhood identification is canonical up to isotopy and prove
choice-independence for Luttinger surgery. Their proof explicitly says the
neighborhood identification is canonical up to isotopy. The argument above
supplies the precise, weaker boundary-push-off consequence needed here, so
Proposition 2.2 is corroboration rather than a remaining logical input.

Reference: D. Auroux, S. K. Donaldson, and L. Katzarkov, *Luttinger surgery
along Lagrangian tori and non-isotopy for singular symplectic plane curves*,
Math. Ann. 326 (2003), 185–203, Section 2.1 and Proposition 2.2,
<https://doi.org/10.1007/s00208-003-0418-9>.

## Result

The ADK03 chart-independence boundary in Lemma 8.2 is discharged by this
self-contained germ argument. What remains outside the finite checks is
ordinary local existence/uniqueness for the displayed one-dimensional Moser
ODE and the continuous lifting principle for the certified connected double
cover. Neither is specific to symplectic four-manifolds.
