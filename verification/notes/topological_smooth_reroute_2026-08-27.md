# The PL-to-smooth bridge without smoothing the source

> **v2.0.0 semantic clarification.** The smooth target constructed here is
> the audit-defined bundle `R_*`. References below to “the paper's” target
> mean the extracted marked object used to define `R_*`; equality with
> Wuebben's intended object is the separate conditional boundary S1--S4.

The verification does not need to put a smooth structure on its
four-dimensional triangulation. The smooth manifold of interest already
exists: it is the paper's smooth genus-2 bundle `R`, with its specified smooth
monodromies and Lagrangian product tori. The correct bridge is a marked
fiber-preserving homeomorphism into that target.

## 1. Construct the marked homeomorphism

Forget the smooth structure on the paper's bundle and call the resulting
oriented topological surface bundle `R_top -> B`. The verified complex gives
an oriented PL, hence topological, surface bundle `|K| -> B`.

The punctured-torus base retracts to a rank-two graph. With a fiber marking,
a surface bundle over this graph is obtained by gluing two mapping cylinders,
so it is determined by the ordered pair of monodromy mapping classes. Runs 12
and 32 certify the same two based actions as the paper. Run 52 now constructs
the stronger statement directly: the marked fiber map conjugates the exact
alpha representative and the common supported beta twist word. Gluing the
two resulting mapping-cylinder maps constructs an
orientation-preserving fiberwise homeomorphism

\[
 H:|K|\longrightarrow R_{top}.
\]

This is the explicit graph-clutching argument of Run 52. Its relative data
are stronger than an unmarked bundle equivalence:

- the equivariant fiber identification fixes `p` and `O`;
- it carries `c` with its free half-rotation to the paper's `c`;
- the beta trace is pointwise product near `e`;
- the comparison isotopies are relative to the `c/e` product collars.

Consequently `H` carries the two surgery tori, their normal product framings,
and the fixed-point `p`-section to the corresponding marked objects in the
paper's smooth bundle.

## 2. Why no four-dimensional smoothing is needed

All information extracted from `K` before surgery is topological:

- the complement and its fundamental group;
- based loops on the normal boundary;
- normal meridians and product-framing push-offs;
- homology classes and the radial chain joining the section to its push-off.

Runs 48--49 make the potentially delicate normal-boundary statement
explicit. Hence `H` transports these objects into `R_top` without choosing a
smoothing of `K`.

Now restore the existing smooth structure on the target `R`. The paper's
tori are already its smooth Lagrangian tori. Runs 43--47 establish on this
smooth target that the transported fibered framing is the Lagrangian
framing. Luttinger surgery and the subsequent symplectic argument are
performed there. At no point is a smooth atlas on `K`, concordance uniqueness
of such an atlas, or a diffeomorphism obtained from a source smoothing used.

Thus Hirsch--Mazur smoothing theory remains true background mathematics but
is not a logical dependency of this verification.

## 3. The section square directly in the target

Run 28 constructs locally flat cycles `Gamma` and `Gamma'` in the doubled PL
bundle and an oriented 3-chain `C` satisfying

\[
 \partial C=\Gamma'-\Gamma,
 \qquad \Gamma\cap\Gamma'=\varnothing.
\]

The Run-52 map is fiberwise and preserves the marked boundary product
collars. Apply it to both halves of the double. Its two boundary restrictions
agree with the same clutching identification, so the two copies descend to a
homeomorphism of the doubled bundles. This is the `H` used below; no new
choice or theorem enters at the doubling seam.

The marked homeomorphism carries `Gamma` to the paper's fixed-point section
class. Applying `H` to the displayed chain gives

\[
 \partial H(C)=H(\Gamma')-H(\Gamma),
 \qquad H(\Gamma)\cap H(\Gamma')=\varnothing.
\]

Therefore, entirely inside the target manifold, the section class has a
disjoint homologous representative. Its homological square is zero. The
smooth self-intersection of the paper's smooth section is this same
homological square.

This does not compare two separately defined intersection forms and does not
need a standalone naturality theorem: it transports the actual cycles and
chain, then computes the square in the target.

## 4. Exact remaining boundary

Run 50 machine-binds every relative marking and recomputes the four Run-28
clutching cases. The proof ledger can therefore remove
`T_low_dimensional_PL_smoothing` and
`T_oriented_intersection_naturality`.

Run 52 removes `T_surface_bundle` entirely. Bundle classification and
Dehn--Nielsen--Baer remain useful alternative explanations and diagnostics,
but neither is required. The only gluing fact used is the elementary
mapping-cylinder quotient calculation written out in Run 52.
