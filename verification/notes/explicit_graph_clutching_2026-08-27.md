# Explicit graph clutching for the marked bundle

## Conclusion

The marked bundle homeomorphism can be constructed directly from the two
mapping-cylinder presentations. Neither classification by maps into
`BDiff+(F)` nor Dehn--Nielsen--Baer is required.

## The pieces

The once-punctured-torus base used in both constructions is an annulus with
one band, a thickening of a graph with one vertex and two loop handles
`alpha,beta`. Both total spaces are presented by a common fiber block and
the two corresponding mapping cylinders. There is no base 2-cell.

Run 34 constructs an orientation-preserving marked fiber homeomorphism

\[
 h:F_K\longrightarrow F_R
\]

from the common equivariant ribbon code and the two coned `p/O` disks.

## The quotient calculation

For a monodromy `f`, write

\[
 M_f=(F\times[0,1])/((x,1)\sim(f(x),0)).
\]

If `h f_K=f_R h`, the formula

\[
 H_f([x,t])=[h(x),t]
\]

is well-defined. Its inverse is `[y,t] -> [h^{-1}(y),t]`; the reverse seam
equation follows from the same conjugacy. Thus `H_f` is a homeomorphism of
mapping cylinders, not merely a map of their interiors.

For alpha, Run 51 gives the conjugacy exactly on the equivariant marked
ribbon system, including the full `c` collar and the fixed points `p,O`.

For beta, source and target use the identical supported word

\[
 T_a\circ T_b,
\]

with `T_b` first. Choose the target annulus coordinates by transporting the
source coordinates through `h`. The standard formula

\[
 D(\theta,r)=(\theta+\epsilon 2\pi\rho(r),r)
\]

then satisfies `h D_K h^{-1}=D_R` factor by factor. The local sign convention
`b:+1,a:-1` is independently calibrated against the paper's displayed based
action in Run 12; injectivity of the action map is not used. Run 51 checks
that these supports miss the full `e` collar and that the restriction there
is the literal product.

If the paper's displayed Dehn twists use different annulus charts, this does
not reintroduce bundle classification. Interpolate their twist profiles by
`rho_s=(1-s)rho_K+s rho_R`; every
`D_s(theta,r)=(theta+epsilon 2 pi rho_s(r),r)` is a relative annulus
diffeomorphism. More generally, for an isotopy `J_s` from
`h psi_K h^{-1}` to the chosen paper representative `g`, put

\[
 k_s=g^{-1}J_{1-s}h.
\]

Then `k_0=h` and `g k_1=k_0 psi_K`, precisely the well-definedness condition
for the displayed convention `(x,1)~(psi_K(x),0)`. Thus
`[x,s] -> [k_s(x),s]` is the explicit mapping-cylinder homeomorphism. This is
the seam calculation itself, not an appeal to classification of bundles.

Both handle maps restrict to the same `h` on the common vertex fiber, so they
glue. Their inverses glue for the same reason. With no base 2-cell, there is
no further coherence equation. This constructs the required
orientation-preserving marked bundle homeomorphism.

## What remains external

The construction uses the already-listed elementary ribbon-thickening and
labeled bistellar-trace interpretations to obtain the marked fiber map and
the relative Dehn-twist traces. It adds no bundle-classification theorem.
The based fundamental-group actions remain strong independent diagnostics,
but Dehn--Nielsen--Baer is no longer required.
