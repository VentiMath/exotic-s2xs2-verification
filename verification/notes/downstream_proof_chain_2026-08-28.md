# The downstream proof chain (2026-08-28)

> **v2.1 scope clarification.** The finite and Audit-Manifold Theorems prove
> `pi_1(V_aud) = 1`. This downstream chain applies to Wuebben's `V` only after
> Source Formalization D identifies `V_aud` with that fixed member. The
> external theorem audit below is additionally relative to the named results.

This note is the prose form of `luttinger/downstream_chain.py` (run 64). Under
Source Formalization D, it transfers the certified statement
`pi_1(V_aud) = 1` to Wuebben's
specified Lidman–Piccirillo piece and then to the paper's Theorems A, B and C,
with every implication written out, every external theorem stated with its
hypotheses, every hypothesis discharged by a named item, and every finite
calculation executed by two independent checkers. It supersedes the run-24
hypothesis audit (`notes/downstream_theorem_audit_2026-08-23.md`), which it
agrees with on every point it revisits.

Nothing below reproves Freedman theory, the Hambleton–Kreck classification,
symplectic Kodaira dimension, the symplectic Thom theorem, Klug's relative
Rochlin theorem, or the Heegaard Floer argument of Lidman–Piccirillo. Those
are the named inputs, and the chain's content is exactly which of their
hypotheses is met by which fact about V.

## 0. Objects and conventions

Names follow the paper and Lidman–Piccirillo (LP25, arXiv:2505.14387v1).

* `R`: the genus-2 surface bundle over the once-punctured torus with
  monodromies `ab` along beta and `phi` along alpha; `dR = S^3_0(Q)`, `Q`
  the square knot.
* `V = V'_{0,0}`: `R` after the two ±1 Luttinger surgeries on `T_alpha`,
  `T_beta` with the paper's parametrizations — the object whose fundamental
  group is certified trivial.
* `sigma`: the free orientation-reversing bundle involution of `S^3_0(Q)`
  (LP25 Lemma 4).
* `Z = V u_sigma V`: the symplectic double. `W = V / sigma`: the quotient,
  double covered by `Z`. `Z'' = V u_{f o sigma} V`: the Lidman–Piccirillo
  regluing (LP25, proof of Theorem 2).
* `B`: the Kawauchi manifold.
* `F`: a fiber of `R` disjoint from the surgery tori. `Gamma`: a section of
  `R` from a fixed point of `phi`, surviving into `V`. `Gamma_hat = Gamma
  u_sigma Gamma` its closure in `Z`; `Gamma'' = Gamma u_A Gamma` its closure
  in `Z''`.

Item kinds: **A** explicit source-comparison assumptions, **K** machine
certificates of this repository, **E** external theorems, **C** computed
facts, **S** steps. The identifiers are those of
`downstream_chain_certificate.json`.

## 1. Source comparison and certified inputs

**A_source_formalization_D.** Source Formalization D1--D14 is the explicit
assumption identifying the audit bundle, marked tori, peripheral classes,
framing classes, and fillings with Wuebben's fixed target member. It is not
a machine certificate.

**K_pi1_Vaud_trivial.** pi_1(V_aud) = 1. The four n=0 filled
presentations carry derivation-DAG certificates accepted by two independent
checkers (runs 29, 57; bound through `proof_certificates/manifest.json`),
and the audit-model peripheral identification (runs 20, 22) shows they
present pi_1 of the audit fillings.

**K_section_square_zero.** `Gamma_hat` is a closed orientable genus-2
surface in the doubled simplicial bundle with `Gamma_hat . Gamma_hat = 0`,
certified with an explicit normal push-off (run 28).

**K_lagrangian_framing.** The audit-model framing calculation (runs 35,
43, 46, 47): for the Thurston-type form on `R_aud` the tori `T_alpha`, `T_beta`
are Lagrangian and their Lagrangian framing is the fibered framing of the
certified longitudes, so the audit fillings are Luttinger surgeries. Source
Formalization D is the distinct comparison with the paper.

## 2. External theorems, as used

Quotations are verbatim from the sources; the rest are stated in the form
the chain applies, with the hypotheses the chain has to discharge.

* **E_van_kampen.** If `X = X_1 u_Y X_2` with `X_1, X_2, Y` path connected
  and `Y` bicollared, then pi_1(X) is a quotient of pi_1(X_1) * pi_1(X_2).
* **E_covering_sequence.** For a connected regular covering `Z -> W` with
  deck group `G`: `1 -> pi_1(Z) -> pi_1(W) -> G -> 1` is exact.
* **E_duality_uct.** Poincaré–Lefschetz duality and universal coefficients
  for compact oriented manifolds; chi is the alternating sum of Betti
  numbers over any field, vanishes for closed odd-dimensional manifolds, is
  multiplicative for bundles with compact fiber and additive for unions
  along a common boundary.
* **E_lattice_index.** For a finite-index sublattice `S` of a lattice `L`
  with symmetric bilinear form, `det(Gram S) = [L:S]^2 det(Gram L)`; the
  intersection form on `H_2/Tors` of a closed oriented 4-manifold is
  unimodular.
* **E_wu.** For a closed oriented 4-manifold `M`, `<w_2(M), x> = x.x` (mod
  2) for `x` in `H_2(M; Z/2)`; for an embedded closed oriented surface `F`
  in an oriented 4-manifold `X`, `<w_2(X), [F]> = chi(F) + F.F` (mod 2).
* **E_freedman** (Freedman 1982, Theorem 1.5). Closed simply connected
  topological 4-manifolds are classified up to homeomorphism by the
  intersection form and KS. Every unimodular form is realized; for even
  forms KS = signature/8 (mod 2) and the manifold is unique; for odd forms
  there are exactly two, one per value of KS.
* **E_hambleton_kreck** (Hambleton 2008, Theorem 5.1, summarizing HK88 and
  HK93 Theorem C), quoted: "Closed, oriented topological 4-manifolds with
  finite cyclic fundamental groups are classified up to homeomorphism by
  pi_1(M), q_M, the w_2-type, and KS(M)." Here `q_M` is the form on
  `H_2/Tors`; w_2-type (I): universal cover not spin, (II): `M` spin,
  (III): `M` not spin but the universal cover spin.
* **E_bundle_symplectic** (Thurston 1976; the paper, proofs of Proposition
  1.3 and Lemma 8.2; LP25, proof of Theorem 8). A closed oriented surface
  bundle over a closed oriented surface with homologically essential fiber
  is symplectic; for `R u_sigma R` the paper chooses such a form with fiber
  term positive on `F` and base term positive on `Gamma_hat`, so both are
  symplectic surfaces, and for which the surgery tori are Lagrangian.
* **E_luttinger** (Luttinger 1995; ADK 2003 §2). Luttinger surgery on a
  Lagrangian torus yields a symplectic manifold whose form agrees with the
  original outside the surgered neighborhood; it replaces `T^2 x D^2` by
  `T^2 x D^2`, so chi is unchanged.
* **E_lp_double** (LP25 Lemmas 4, 6, proof of Theorem 8 with footnote 3).
  `sigma` is a free orientation-reversing bundle isomorphism; `R u_sigma R`
  (second copy oriented by `(-F, -B)`) is a closed oriented genus-2 bundle
  over a closed genus-2 surface; surgeries in `int V` commute with
  doubling, so `Z` is `R u_sigma R` surgered on four disjoint Lagrangian
  tori missing `F` and the sections; `sigma` preserves the boundary circles
  of `Gamma`, `Gamma'` setwise, so `Gamma_hat` is a closed surface.
* **E_lp_quotient** (LP25 §1 and Lemma 7; the paper, proof of Proposition
  1.3). `W` is a closed oriented smooth 4-manifold and `Z -> W` is the
  connected 2-fold covering whose deck involution swaps the copies of `V`.
  `W` is spin: `H_2(W; Z/2) = (Z/2)^2` carries a hyperbolic pair (the image
  of `F` and the closed non-orientable image of `Gamma`), so its mod-2 form
  is even and `w_2(W) = 0` by Wu's formula. Hypotheses: `V` spin with
  `H_2(V) = Z<F>`, `F.F = 0`, `F.Gamma = 1`, and `sigma` descends because
  all surgeries are interior.
* **E_kawauchi_B** (Kawauchi 2009; LP25 Theorem 1 and §1). `B` is a closed
  smooth oriented spin 4-manifold with `pi_1(B) = H_1(B) = Z/2`, `b_2(B) =
  0`, in which `4_1` is smoothly slice.
* **E_asphericity.** A bundle with aspherical fiber and base is aspherical;
  closed surfaces of genus ≥ 1 are aspherical.
* **E_kodaira** (Li 2006; Liu 1996; Ho–Li 2012 p. 1, quoted). kappa is
  defined from `K^2` and `K.[omega]` of a minimal model, with kappa =
  −infinity iff `K^2 < 0` or `K.[omega] < 0` for the minimal model;
  "According to [Li06], kappa(X, omega) is independent of the choice of
  symplectic form omega and hence is denoted by kappa(X)." A minimal
  symplectic 4-manifold has kappa = −infinity iff it is rational or ruled;
  rational and ruled 4-manifolds have `pi_2 != 0`. The independence is over
  forms inducing a fixed orientation.
* **E_ho_li** (Ho–Li 2012, Theorem 1.1), quoted: "The Luttinger surgery
  preserves the symplectic Kodaira dimension."
* **E_symplectic_thom** (Ozsváth–Szabó 2000, Theorem 1.1). An embedded
  symplectic surface in a closed symplectic 4-manifold is genus-minimizing
  in its homology class.
* **E_cover_construction** (the paper, proof of Lemma 4.3, after
  Stipsicz–Szabó). For a square-zero symplectic surface `S` and `k ≥ 1`,
  `Sigma_k = {(u, z) : z^k = eps f(u)}` in `S x D^2`, with `f: S -> S^1`
  surjective on `H_1` and small `eps`, is an embedded connected unbranched
  degree-k cover of `S` representing `k[S]`, and is symplectic.
* **E_adjunction.** For a connected embedded symplectic surface of genus
  `g`, `K.S + S.S = 2g − 2`.
* **E_klug** (Klug 2021, Theorem 2), quoted: "Let X^4 be a smooth compact
  connected oriented 4-manifold with dX an integer homology sphere. Let F^2
  be an orientable characteristic surface with connected boundary that is
  properly embedded in X. Then Arf(F) + Arf(dF) = (sigma(X) − [F]^2)/8 +
  mu(dX) (mod 2)." A properly embedded surface is characteristic iff its
  class in `H_2(X, dX; Z/2)` is Lefschetz dual to `w_2(X)`; for spin `X`,
  iff the class vanishes.
* **E_levine_arf** (Levine 1966). `Arf(K) = 0` if `Delta_K(−1) = ±1` (mod
  8) and `1` if `±3` (mod 8); equivalently the Arf invariant of `x -> x^T S
  x` (mod 2) for a Seifert matrix `S`.
* **E_trace_embedding** (LP25, proof of Theorem 1; handle calculus). A
  smooth slice disk `D` for `K` in `X − B^4` with Seifert-framed normal
  bundle gives an embedding `X_0(K) = B^4 u nu(D)` in `X`, in which a
  Seifert surface capped by `D` is a closed surface of square 0 generating
  `H_2(X_0(K)) = Z`; the framing condition is automatic when `H_2(X − B^4,
  d; Z)` is torsion; `X_0(K)` is simply connected; `4_1` has genus 1.
* **E_ball_isotopy** (Palais–Cerf). Any two orientation-preserving smooth
  embeddings of `B^4` in a connected 4-manifold are isotopic, so sliceness
  in `X − B^4` is independent of the ball; `4_1` is amphichiral.
* **E_novikov.** Signature is additive for unions along a closed
  3-manifold; reversing orientation negates it.
* **E_lp_regluing** (LP25, proof of Theorem 2; the paper, proof of Theorem
  1.2(c)). There is an orientation-preserving diffeomorphism `f` of
  `S^3_0(Q)` (two Gluck twists and an isotopy) sending the framed meridian
  `(mu, 0)` to `(mu', 1)`; with `A` the framed homology from `(mu', 0)` to
  `(mu, 0)`, `Gamma'' = Gamma u_A Gamma` in `Z''` has odd self-intersection
  and meets `F` once.
* **E_lp_floer** (LP25 Lemmas 9, 10 and proof of Theorem 2; OS04, OS06).
  Lemma 9, quoted: "Let t be a spin^c structure on V with |<c_1(t), F>| =
  2. Then Psi_{V,t} ≠ 0." Its proof uses `Z` symplectic, `|<c_1(k), F>| =
  2` for the canonical class, `H^2(V) = Z`, the nonvanishing of the mixed
  invariant of a symplectic 4-manifold for the line of `F` [OS04], and
  conjugation symmetry [OS06, Thm 3.6]. Lemma 10, quoted: "Let (M_1, t_1)
  and (M_2, t_2) be two spin^c four-manifolds glued along S^3_0(Q) so that
  t_1| = t_2| = s_±. If Psi_{M_1,t_1} and Psi_{M_2,t_2} are non-zero, then
  Phi_{M_1 u M_2, span{F}, t} ≠ 0 for any t restricting to t_i." Finally,
  `CP^2 # −CP^2` (and its sum with any homology 4-sphere) admits for each
  of its two square-zero lines a splitting along `S^2 x S^1`, and
  `HF_red(S^2 x S^1) = 0` in every non-torsion spin^c structure, so all its
  mixed invariants vanish; the mixed invariant is an invariant of
  `(M, L, t)`.

## 3. The chain

**S00 (source transfer).** Under Source Formalization D, the relative smooth
comparison extends over both fillings and identifies `V_aud` with Wuebben's
fixed target member `V`. Hence certified `pi_1(V_aud)=1` implies
`pi_1(V)=1`.

**S1 (homology of V).** `H_1(V) = 0`, `H_3(V) = 0`, `H_2(V) = Z<F>` with
`F.F = 0`, and `V` is spin.

*Proof.* pi_1(V) = 1 gives `H_1(V) = 0`. The boundary is connected, so
`H^0(V) -> H^0(dV)` is onto and `H^1(V) = Hom(H_1 V, Z) = 0`; the pair
sequence gives `H^1(V, dV) = 0`, hence `H_3(V) = H^1(V, dV) = 0`. Likewise
`H_1(V, dV) = 0` (it sits between `H_1(V) = 0` and the injective `H_0(dV)
-> H_0(V)`), so `Tors H_2(V) = Tors H^3(V) = Tors H_1(V, dV) = 0`. chi(V) =
chi(R) = chi(F) chi(base) = (−2)(−1) = 2, unchanged by the two surgeries
(E_luttinger), and `b_0 = 1`, `b_1 = b_3 = b_4 = 0` give `b_2(V) = 1`
(C_euler, C_betti). A section `Gamma` is properly embedded and meets `F`
once, so `[F]` pairs to 1 with the relative class `[Gamma]` and is
primitive: `H_2(V) = Z<F>`. `F.F = 0` since a fiber has trivial normal
bundle. `H_2(V; Z/2) = Z/2<F>` by universal coefficients, `w_2` is detected
on it, and `<w_2, F> = chi(F) + F.F = −2 + 0 = 0` (mod 2) (C_w2_fiber,
E_wu). ∎

**S2 (the doubles are simply connected).** pi_1(Z) = pi_1(Z'') = 1.

*Proof.* Both are unions of two copies of `V` along the connected
bicollared boundary `S^3_0(Q)`; by E_van_kampen each fundamental group is a
quotient of pi_1(V) * pi_1(V) = 1. This is the one place where pi_1(V) =
1, rather than pi_1(Z) = 1, is needed: the regluing twists the amalgam. ∎

**S3 (the form of Z).** `H_2(Z) = Z<F, Gamma_hat>` with intersection form
`H`; `Z` is closed, simply connected, spin, `b_2 = 2`, signature 0.

*Proof.* chi(Z) = 2 chi(V) − chi(S^3_0(Q)) = 4 and pi_1(Z) = 1 give
`b_2(Z) = 2` with `H_2(Z)` torsion-free (`Tors H_2 = Tors H^3 = Tors H_1 =
0`). `F.F = 0`; `F.Gamma_hat = 1` (a fiber meets a section once);
`Gamma_hat.Gamma_hat = 0` by K_section_square_zero. The Gram determinant of
`(F, Gamma_hat)` is −1 and the ambient form is unimodular, so by
E_lattice_index the index of the sublattice is 1: `(F, Gamma_hat)` is a
basis and the form is `H` (C_hyperbolic_basis). `H` is even, so `w_2(Z) =
0` by Wu's formula (`H_2(Z; Z/2) = H_2(Z) ⊗ Z/2`). ∎

**S4.** `Z` is homeomorphic to `S^2 x S^2`.

*Proof.* `Z` is a closed simply connected topological 4-manifold with even
form `H`, the form of `S^2 x S^2`; for even forms KS = signature/8 = 0 is
determined (C_signatures), so E_freedman gives the homeomorphism. ∎

**S5 (Z is symplectic).** `Z` is a closed symplectic 4-manifold, obtained
from the closed genus-2 bundle `R u_sigma R` over a genus-2 surface by
Luttinger surgery on four disjoint Lagrangian tori missing `F` and
`Gamma_hat`; `F` and `Gamma_hat` are symplectic surfaces of genus 2 and
square 0.

*Proof.* `R u_sigma R` is a closed surface bundle (E_lp_double) whose fiber
is homologically essential (`F.Gamma_hat = 1`), so it carries the paper's
Thurston-type form, positive on `F` and `Gamma_hat` (E_bundle_symplectic).
The surgery tori are Lagrangian for it and the surgeries are the certified
Luttinger surgeries (K_lagrangian_framing), and Luttinger surgery preserves
the form away from the surgered neighborhoods, which miss `F` and
`Gamma_hat` (E_luttinger). ∎

**S6.** `Z` is not diffeomorphic to `S^2 x S^2`.

*Proof.* `R u_sigma R` is aspherical (genus-2 fiber and base,
E_asphericity), hence minimal — an exceptional sphere would be
null-homotopic, hence of square 0, not −1 — and neither rational nor ruled,
since those have `pi_2 ≠ 0`; so kappa(R u_sigma R) ≠ −infinity
(E_kodaira). Luttinger surgery preserves kappa (E_ho_li), so kappa(Z) ≠
−infinity. Suppose `psi: Z -> S^2 x S^2` were a diffeomorphism. Composing
with a reflection of one factor if necessary (C_orientation_reversal), take
`psi` orientation-preserving; then `psi^*` of a product form is a
symplectic form on `Z` inducing its orientation, with kappa = kappa(S^2 x
S^2) = −infinity (rational), contradicting the independence of kappa from
the form. ∎

**S7 = Theorem A.** `Z` is homeomorphic but not diffeomorphic to `S^2 x
S^2`. (S4, S6.)

**S8 (invariants of W).** `W` is a closed oriented smooth spin 4-manifold
with pi_1(W) = Z/2, `b_2(W) = 0`, signature 0, KS(W) = 0.

*Proof.* `Z -> W` is a connected 2-fold covering (E_lp_quotient), so
E_covering_sequence gives `|pi_1(W)| = 2` (C_covering_order). chi(W) =
chi(Z)/2 = 2 and `b_1(W) = 0` give `b_2(W) = 0`, hence signature 0
(C_euler, C_betti). `W` is spin by E_lp_quotient, whose hypotheses S1
supplies. KS = 0 because `W` is smooth. ∎

**S9.** `W` is homeomorphic to `B`.

*Proof.* Both are closed oriented topological 4-manifolds with pi_1 = Z/2,
zero form on `H_2/Tors = 0`, w_2-type (II), KS = 0 (both smooth)
(C_hk_invariants, E_kawauchi_B). These are the invariants of
E_hambleton_kreck. ∎

**S10 (no square-zero torus; the paper's Lemma 4.3).** No nonzero
square-zero class in `H_2(Z; Z)` is represented by a smoothly embedded
torus.

*Proof.* For `k ≥ 1` the connected symplectic k-fold covers of `F` and of
`Gamma_hat` (E_cover_construction) represent `kF` and `k Gamma_hat` and
have genus `k + 1` (C_cover_genus: chi = −2k). By E_symplectic_thom these
genera are minimal; reversing orientation covers `k < 0`. Since `(aF + b
Gamma_hat)^2 = 2ab` (C_square_zero_axes), every nonzero square-zero class
is `kF` or `k Gamma_hat` with `k ≠ 0`, of minimal genus `|k| + 1 ≥ 2`. ∎

**S11.** The figure-eight knot is not smoothly slice in `W`.

*Proof.* Let `D` be a smooth slice disk in `W − B^4`. `H_2(W − B^4, d; Z)
= H^2(W) = Z/2` is torsion (S8 with E_duality_uct), so the relative
self-intersection of `D` is 0 and its framing is the Seifert framing.

Case 1: `[D, dD] = 0` in `H_2(W − B^4, d; Z/2)`. Then `D` is characteristic
in the spin manifold `W − B^4`, and E_klug applies with `X = W − B^4`
(smooth, compact, connected, oriented, `dX = S^3`), `F = D` (orientable,
connected boundary, characteristic): `Arf(D) + Arf(4_1) = (sigma − [D]^2)/8
+ mu(S^3)`. Here `Arf(D) = 0`, `sigma = 0`, `[D]^2 = 0`, `mu(S^3) = 0`, so
`Arf(4_1) = 0` (C_klug_instance); but `Arf(4_1) = 1` (C_arf_figure_eight,
E_levine_arf: `Delta(t) = −t^2 + 3t − 1`, `Delta(−1) = −5 ≡ 3` (mod 8)).

Case 2: `[D, dD] ≠ 0`. By E_trace_embedding, `X_0(4_1)` embeds in `W` and
the torus `T` (Seifert surface capped by `D`) has square 0 with `[T] ≠ 0`
in `H_2(W; Z/2)`. `X_0(4_1)` is simply connected, so it lifts to `Z` and
`T` lifts to a torus `T~` with `p_*[T~] = [T] ≠ 0`, hence `[T~] ≠ 0` in
`H_2(Z; Z/2) = H_2(Z) ⊗ Z/2` and therefore in `H_2(Z; Z)`; `T~.T~ = T.T =
0` since `p` is a local diffeomorphism. This contradicts S10. ∎

**S12 = Theorem B.** `W` is homeomorphic to `B`, and `(B, W)` is
distinguished by the smooth sliceness of `4_1`, hence not diffeomorphic.
(S9; `4_1` slice in `B` by E_kawauchi_B, not in `W` by S11; sliceness is a
diffeomorphism invariant by E_ball_isotopy.)

**S13 (the form of Z'').** `Z''` is closed, simply connected, smooth, with
`b_2 = 2`, signature 0 and odd form `<1> ⊕ <−1>`.

*Proof.* pi_1(Z'') = 1 (S2) and chi(Z'') = 4 give `b_2 = 2` with `H_2`
free. Novikov additivity over the two copies of `V`, the second with
reversed orientation, gives signature 0 (E_novikov, C_signatures). `F.F =
0`, `F.Gamma'' = 1` and `Gamma''.Gamma'' = 2n + 1` odd (E_lp_regluing); the
Gram determinant is −1 so `(F, Gamma'')` is a basis (E_lattice_index), and
`E = Gamma'' − nF`, `D = F − E` satisfy `E.E = 1`, `D.D = −1`, `E.D = 0`
for every `n` (C_odd_basis): the form is `<1> ⊕ <−1>`. ∎

**S14.** `Z''` is homeomorphic to `CP^2 # −CP^2`. (S13 and E_freedman: of
the two manifolds with this odd form, the one with KS = 0 — `Z''` is smooth
— is `CP^2 # −CP^2`.)

**S15.** `Z''` is not diffeomorphic to `CP^2 # −CP^2`.

*Proof.* `Z` is symplectic (S5) with `|K_Z.F| = 2` by adjunction
(C_adjunction, E_adjunction: `F` symplectic, genus 2, square 0) and `H^2(V)
= Z` (S1), so Lemma 9 of E_lp_floer gives `Psi_{V,t} ≠ 0` for both spin^c
structures with `|<c_1(t), F>| = 2`. `Z''` is `V u V` along `S^3_0(Q)` with
`t` restricting to the non-torsion `s_±`, `b_2^+(Z'') = 1` and `span{F}` a
square-zero line (S13), so Lemma 10 gives a nonvanishing mixed invariant
`Phi_{Z'', span{F}, t}`. A diffeomorphism to `CP^2 # −CP^2` would carry
`span{F}` to one of its two square-zero lines (C_square_zero_lines_odd),
along each of which the manifold splits over `S^2 x S^1` and every mixed
invariant vanishes. ∎

**S16 = Theorem C.** `Z''` is a closed simply connected 4-manifold
homeomorphic but not diffeomorphic to `CP^2 # −CP^2`. (S2, S14, S15.)

## 4. Statement

**Theorem.** Under Source Formalization D, for the specified
Lidman–Piccirillo piece `V`, relative to the 25 external theorems of §2 and
the three certificates of §1:

* (A) the symplectic double `Z = V u_sigma V` is homeomorphic but not
  diffeomorphic to `S^2 x S^2`;
* (B) `W = V / sigma` is homeomorphic to the Kawauchi manifold `B`, and the
  pair `(B, W)` is homeomorphic but not diffeomorphic, distinguished by the
  smooth sliceness of the figure-eight knot;
* (C) the Lidman–Piccirillo regluing `Z''` is a closed simply connected
  4-manifold homeomorphic but not diffeomorphic to `CP^2 # −CP^2`.

Every hypothesis of every external theorem is discharged by a named
certificate, computation, or earlier step, as recorded in the `uses`
fields of the certificate, and both checkers verify that each of (A), (B),
(C) depends on the certified pi_1(V) = 1.

## 5. Where each external theorem enters

| External | Used in | Hypotheses discharged by |
|---|---|---|
| E_van_kampen | S2 | E_lp_double, E_lp_regluing (connected collared boundary) |
| E_covering_sequence | S8, S11 | E_lp_quotient (connected 2-fold cover) |
| E_duality_uct, E_lattice_index, E_wu | S1, S3, S8, S11, S13 | C_euler, C_betti, K_section_square_zero |
| E_freedman | S4, S14 | S3, S13 (closed, simply connected, form, KS from smoothness or parity) |
| E_hambleton_kreck | S9 | S8, E_kawauchi_B, C_hk_invariants |
| E_bundle_symplectic, E_luttinger, E_lp_double | S5 | C_hyperbolic_basis (essential fiber), K_lagrangian_framing |
| E_asphericity, E_kodaira, E_ho_li | S6 | S5, C_orientation_reversal |
| E_lp_quotient | S8 | S1 (V spin, H_2(V) = Z<F>) |
| E_kawauchi_B | S9, S12 | — (facts about B) |
| E_cover_construction, E_symplectic_thom | S10 | S5 (F, Gamma_hat symplectic, square 0), C_cover_genus |
| E_trace_embedding, E_klug, E_levine_arf, E_ball_isotopy | S11, S12 | S8 (spin, sigma = 0, torsion relative H_2), C_arf_figure_eight, C_klug_instance, S10 |
| E_novikov, E_lp_regluing | S13 | S2, C_odd_basis |
| E_adjunction, E_lp_floer | S15 | S5, S1, S13, C_adjunction, C_square_zero_lines_odd |

## 6. Replay

From `verification/luttinger`:

    python3 downstream_chain.py --check
    ruby verify_downstream_chain.rb
    python3 proof_ledger.py

The first recomputes every item and compares with the frozen certificate;
the second re-derives every computed fact with independent code, checks the
dependency graph, and verifies the evidence digests; the third checks that
the repository's whole dependency ledger, now including this chain, is
closed and acyclic.
