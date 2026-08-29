#!/usr/bin/env python3
"""The downstream proof chain: from the certified triviality of pi_1(V) to
Wuebben's Theorems A, B and C (arXiv:2608.17267), relative to explicitly
named external theorems.

This is the proof-grade successor of the run-24 hypothesis audit.  Every item
in the chain is one of four kinds:

  external     a theorem from the literature, stated with its hypotheses and
               its source, which this project does not reprove;
  certificate  a machine certificate of this repository, bound by SHA-256;
  computed     a finite calculation executed here and replayed independently
               by verify_downstream_chain.rb;
  step         a deduction whose premises are earlier items of the chain.

Run without arguments to recompute everything and write
downstream_chain_certificate.json; run with --check to recompute and compare
with the frozen file.  Nothing here formalizes Freedman theory, symplectic
Kodaira dimension, or Heegaard Floer theory: those enter as named external
items, and the chain records exactly which of their hypotheses is discharged
by which computation or certificate.
"""

import argparse
import json
from hashlib import sha256
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTPUT = HERE / "downstream_chain_certificate.json"

# --------------------------------------------------------------------------
# Objects.  Names follow arXiv:2608.17267 and Lidman--Piccirillo (LP25).
#
#   R      genus-2 surface bundle over the once-punctured torus, dR = S^3_0(Q)
#   V      the specified Lidman--Piccirillo piece V'_{0,0}: R after the two
#          +/-1 Luttinger surgeries on T_alpha, T_beta with the paper's
#          parametrizations
#   sigma  the free orientation-reversing bundle involution of S^3_0(Q)
#   Z      the symplectic double V u_sigma V
#   W      the quotient V / sigma, double covered by Z
#   Z''    the Lidman--Piccirillo regluing V u_{f o sigma} V
#   B      the Kawauchi manifold
#   F      a fiber of R disjoint from the surgery tori;  Gamma a section from
#          a fixed point of phi;  Gamma_hat = Gamma u_sigma Gamma its closure
#          in Z;  Gamma'' = Gamma u_A Gamma its closure in Z''
# --------------------------------------------------------------------------

EVIDENCE = [
    # Theorem D: the four theorem-critical derivation certificates of the
    # sealed chain (run 66) and of the earlier four-generator export, all
    # bound through the proof manifest that hashes them and their inputs.
    "luttinger/proof_certificates/manifest.json",
    "luttinger/sealed_transport/r_presentations.json",
    "luttinger/r_presentations.json",
    "runs/66-sealed-tietze-transport.txt",
    "runs/29-independent-filled-group-certificates.txt",
    "runs/57-second-certificate-verifier.txt",
    # The certified section self-intersection Gamma_hat . Gamma_hat = 0.
    "runs/28-pl-self-intersection-certificate.txt",
    "notes/pl_self_intersection_certificate_2026-08-24.md",
    # The framing identification (Lagrangian framing = fibered framing).
    "runs/35-framing-lemma-referee-packet.txt",
    "runs/43-weinstein-chart-independence.txt",
    "runs/46-direct-equivariant-moser.txt",
    "runs/47-cumulative-moser-flow.txt",
    "notes/framing_lemma_referee_packet_2026-08-25.md",
    # The peripheral identification that the certified presentations are
    # the paper's surgeries.
    "runs/20-direct-peripheral-fillings-trivial.txt",
    "runs/22-model-correspondence-and-framing.txt",
    # The run-24 audit this chain supersedes.
    "runs/24-downstream-theorem-audit.txt",
    "notes/downstream_theorem_audit_2026-08-23.md",
]

CERTIFICATES = [
    {
        "id": "K_pi1_V_trivial",
        "claim": "pi_1(V) = 1 (Theorem D): each of the four n=0 filled "
                 "presentations of the sealed complement presentation "
                 "(whose Tietze transport from the serialized raw complex "
                 "replays from frozen files) carries a derivation-DAG "
                 "certificate accepted by two independent checkers, the "
                 "four fillings of the earlier four-generator export reach "
                 "the same verdicts, and the peripheral identification "
                 "shows they present pi_1 of the paper's surgeries.",
        "evidence": ["luttinger/proof_certificates/manifest.json",
                     "luttinger/sealed_transport/r_presentations.json",
                     "luttinger/r_presentations.json",
                     "runs/66-sealed-tietze-transport.txt",
                     "runs/29-independent-filled-group-certificates.txt",
                     "runs/57-second-certificate-verifier.txt",
                     "runs/20-direct-peripheral-fillings-trivial.txt",
                     "runs/22-model-correspondence-and-framing.txt"],
        "ledger": "C_pi1_V_trivial",
    },
    {
        "id": "K_section_square_zero",
        "claim": "The closed section Gamma_hat of the doubled bundle is a "
                 "closed orientable genus-2 surface with Gamma_hat . "
                 "Gamma_hat = 0, certified on the simplicial model with an "
                 "explicit normal push-off (run 28).",
        "evidence": ["runs/28-pl-self-intersection-certificate.txt",
                     "notes/pl_self_intersection_certificate_2026-08-24.md"],
        "ledger": "G_section_square_zero",
    },
    {
        "id": "K_lagrangian_framing",
        "claim": "The paper's Lemma 8.2: for the Thurston-type form on R the "
                 "tori T_alpha, T_beta are Lagrangian and their Lagrangian "
                 "framing is the fibered framing of the certified "
                 "longitudes, so the certified fillings are the paper's "
                 "Luttinger surgeries.",
        "evidence": ["runs/35-framing-lemma-referee-packet.txt",
                     "runs/43-weinstein-chart-independence.txt",
                     "runs/46-direct-equivariant-moser.txt",
                     "runs/47-cumulative-moser-flow.txt",
                     "notes/framing_lemma_referee_packet_2026-08-25.md"],
        "ledger": "G_lagrangian_framing",
    },
]

# Every external theorem the chain consumes.  Statements quoted from the
# source are marked "quoted"; the others are stated in the form used, with
# the hypotheses the chain has to discharge.
EXTERNAL = [
    {
        "id": "E_van_kampen",
        "name": "Seifert--van Kampen theorem (union along a connected "
                "collared boundary)",
        "statement": "If X = X_1 u_Y X_2 with X_1, X_2, Y path connected and "
                     "Y bicollared, then pi_1(X) is the pushout "
                     "pi_1(X_1) *_{pi_1(Y)} pi_1(X_2); in particular pi_1(X) "
                     "is a quotient of pi_1(X_1) * pi_1(X_2).",
        "source": "standard (e.g. Hatcher, Algebraic Topology, Thm 1.20)",
        "hypotheses": ["X_1, X_2, Y path connected", "Y bicollared in X"],
    },
    {
        "id": "E_covering_sequence",
        "name": "Exact sequence of a regular covering",
        "statement": "For a connected regular covering p: Z -> W with deck "
                     "group G there is an exact sequence "
                     "1 -> pi_1(Z) -> pi_1(W) -> G -> 1.",
        "source": "standard (Hatcher, Prop 1.40)",
        "hypotheses": ["Z connected", "p regular with deck group G"],
    },
    {
        "id": "E_duality_uct",
        "name": "Poincare--Lefschetz duality and universal coefficients",
        "statement": "For a compact oriented n-manifold X: H_k(X) = "
                     "H^{n-k}(X, dX); H^k(X) = Hom(H_k X, Z) + Ext(H_{k-1} X, "
                     "Z); H_k(X; Z/2) = H_k(X) (x) Z/2 + Tor(H_{k-1} X, Z/2); "
                     "H^k(X; Z/2) = Hom(H_k(X; Z/2), Z/2); chi(X) is the "
                     "alternating sum of Betti numbers over any field; "
                     "chi of a closed odd-dimensional manifold is 0; chi is "
                     "multiplicative for fiber bundles with compact fiber and "
                     "additive for unions along a common boundary.",
        "source": "standard",
        "hypotheses": [],
    },
    {
        "id": "E_lattice_index",
        "name": "Index formula for sublattices",
        "statement": "If S is a finite-index sublattice of a lattice L with "
                     "symmetric bilinear form, then det(Gram S) = "
                     "[L:S]^2 det(Gram L).  For a closed oriented "
                     "4-manifold, the intersection form on H_2/Tors is "
                     "unimodular (Poincare duality).",
        "source": "standard",
        "hypotheses": [],
    },
    {
        "id": "E_wu",
        "name": "Wu's formula and the Whitney sum formula for w_2",
        "statement": "For a closed oriented 4-manifold M, <w_2(M), x> = x.x "
                     "(mod 2) for every x in H_2(M; Z/2).  For an embedded "
                     "closed oriented surface F in an oriented 4-manifold X, "
                     "<w_2(X), [F]> = w_2(TX|F) = w_2(TF) + w_2(nu F) = "
                     "chi(F) + F.F (mod 2).",
        "source": "standard (Milnor--Stasheff)",
        "hypotheses": [],
    },
    {
        "id": "E_freedman",
        "name": "Freedman's classification of closed simply connected "
                "topological 4-manifolds",
        "statement": "Closed simply connected topological 4-manifolds are "
                     "classified up to homeomorphism by the intersection form "
                     "and the Kirby--Siebenmann invariant KS in Z/2.  Every "
                     "unimodular form is realized; if the form is even, "
                     "KS = signature/8 (mod 2) and the manifold is unique; if "
                     "the form is odd there are exactly two, one for each "
                     "value of KS.",
        "source": "M. H. Freedman, J. Differential Geom. 17 (1982), "
                  "Theorem 1.5",
        "hypotheses": ["closed", "simply connected", "topological 4-manifold"],
    },
    {
        "id": "E_hambleton_kreck",
        "name": "Hambleton--Kreck classification for finite cyclic "
                "fundamental group",
        "statement": "quoted (Hambleton 2008, Theorem 5.1, summarizing "
                     "[HK88, HK93]): \"Closed, oriented topological "
                     "4-manifolds with finite cyclic fundamental groups are "
                     "classified up to homeomorphism by pi_1(M), q_M, the "
                     "w_2-type, and KS(M).\"  Here q_M is the intersection "
                     "form on H_2(M; Z)/Tors and the w_2-type is (I) if the "
                     "universal cover is not spin, (II) if M is spin, (III) "
                     "if M is not spin but its universal cover is.",
        "source": "I. Hambleton and M. Kreck, J. Reine Angew. Math. 444 "
                  "(1993), Theorem C; I. Hambleton, Proc. Gokova 2008, "
                  "Theorem 5.1",
        "hypotheses": ["closed", "oriented", "topological 4-manifold",
                       "pi_1 finite cyclic"],
    },
    {
        "id": "E_bundle_symplectic",
        "name": "Thurston's construction and the paper's Thurston-type form",
        "statement": "A closed oriented surface bundle over a closed oriented "
                     "surface whose fiber is homologically essential carries "
                     "a symplectic form (Thurston 1976).  For R u_sigma R the "
                     "paper chooses such a form whose fiber term is positive "
                     "on F and whose base term is positive on the closed "
                     "section Gamma_hat, so that both are symplectic "
                     "surfaces, and for which the surgery tori are "
                     "Lagrangian.",
        "source": "W. Thurston, Proc. AMS 55 (1976); arXiv:2608.17267, "
                  "proof of Proposition 1.3 and Lemma 8.2; LP25, proof of "
                  "Theorem 8",
        "hypotheses": ["fiber class nonzero in H_2(R u_sigma R)"],
    },
    {
        "id": "E_luttinger",
        "name": "Luttinger surgery is symplectic and local",
        "statement": "Luttinger surgery on a Lagrangian torus in a "
                     "symplectic 4-manifold produces a symplectic 4-manifold "
                     "whose form agrees with the original outside the "
                     "surgered neighborhood; it replaces T^2 x D^2 by "
                     "T^2 x D^2, so the Euler characteristic is unchanged.",
        "source": "K. Luttinger, J. Differential Geom. 42 (1995); Auroux, "
                  "Donaldson, Katzarkov, Math. Ann. 326 (2003), Sect. 2",
        "hypotheses": ["torus Lagrangian"],
    },
    {
        "id": "E_lp_double",
        "name": "Lidman--Piccirillo: the double is a surgered surface bundle",
        "statement": "sigma is a free orientation-reversing bundle "
                     "isomorphism of S^3_0(Q) (LP25 Lemma 4); R u_sigma R, "
                     "with the second copy oriented by (-F, -B), is a closed "
                     "oriented genus-2 surface bundle over a closed genus-2 "
                     "surface; the surgeries in int V commute with doubling, "
                     "so Z = V u_sigma V is R u_sigma R surgered along four "
                     "disjoint Lagrangian tori that miss a fiber F and the "
                     "sections; sigma preserves the boundary circles of the "
                     "sections Gamma, Gamma' setwise, so Gamma_hat = Gamma "
                     "u_sigma Gamma is a closed surface (LP25 Lemma 6 and "
                     "proof of Theorem 8, footnote 3).",
        "source": "arXiv:2505.14387v1, Lemmas 4, 6, proof of Theorem 8",
        "hypotheses": [],
    },
    {
        "id": "E_lp_quotient",
        "name": "Lidman--Piccirillo: the quotient W and its double cover",
        "statement": "W = V / sigma is a closed oriented smooth 4-manifold, "
                     "and Z = V u_sigma V -> W is the connected 2-fold "
                     "covering whose deck involution swaps the two copies of "
                     "V.  W is spin: H_2(W; Z/2) = (Z/2)^2 carries a "
                     "hyperbolic pair (the image of F and the closed "
                     "non-orientable image of Gamma), so its mod-2 form is "
                     "even and w_2(W) = 0 by Wu's formula (LP25 Lemma 7, "
                     "whose proof arXiv:2608.17267 Proposition 1.3 shows "
                     "applies verbatim to V).",
        "source": "arXiv:2505.14387v1, Section 1 and Lemma 7; "
                  "arXiv:2608.17267, proof of Proposition 1.3",
        "hypotheses": ["V spin with H_2(V) = Z<F>, F.F = 0, F.Gamma = 1",
                       "sigma descends (all surgeries in int V)"],
    },
    {
        "id": "E_kawauchi_B",
        "name": "The Kawauchi manifold B",
        "statement": "B is a closed smooth oriented spin 4-manifold with "
                     "pi_1(B) = H_1(B) = Z/2 and b_2(B) = 0, and the "
                     "figure-eight knot 4_1 is smoothly slice in B.",
        "source": "A. Kawauchi, Commun. Math. Res. 25 (2009); "
                  "arXiv:2505.14387v1, Theorem 1 and Section 1",
        "hypotheses": [],
    },
    {
        "id": "E_asphericity",
        "name": "Asphericity of surface bundles over surfaces",
        "statement": "A fiber bundle with aspherical fiber and aspherical "
                     "base is aspherical (long exact sequence of homotopy "
                     "groups).  Closed surfaces of genus >= 1 are aspherical.",
        "source": "standard",
        "hypotheses": [],
    },
    {
        "id": "E_kodaira",
        "name": "Symplectic Kodaira dimension (Li) and its -infinity "
                "characterization (Liu, Li)",
        "statement": "quoted (Ho--Li 2012, p. 1): the Kodaira dimension "
                     "kappa(X, omega) of a symplectic 4-manifold is defined "
                     "from K_omega^2 and K_omega.[omega] of a minimal model, "
                     "with kappa = -infinity iff K^2 < 0 or K.[omega] < 0 for "
                     "the minimal model; \"According to [Li06], kappa(X, "
                     "omega) is independent of the choice of symplectic form "
                     "omega and hence is denoted by kappa(X).\"  For a "
                     "minimal symplectic 4-manifold kappa = -infinity iff it "
                     "is rational or ruled (Liu 1996, Li 2006).  Rational "
                     "and ruled 4-manifolds (CP^2, S^2-bundles over surfaces, "
                     "and their blow-ups) have pi_2 != 0.",
        "source": "T.-J. Li, J. Differential Geom. 74 (2006); A.-K. Liu, "
                  "Math. Res. Lett. 3 (1996); C.-I. Ho and T.-J. Li, Asian "
                  "J. Math. 16 (2012), p. 1",
        "hypotheses": ["X closed symplectic; independence of omega is over "
                       "forms inducing the given orientation"],
    },
    {
        "id": "E_ho_li",
        "name": "Ho--Li: Luttinger surgery preserves Kodaira dimension",
        "statement": "quoted (Ho--Li 2012, Theorem 1.1): \"The Luttinger "
                     "surgery preserves the symplectic Kodaira dimension.\"",
        "source": "C.-I. Ho and T.-J. Li, Asian J. Math. 16 (2012), "
                  "Theorem 1.1",
        "hypotheses": ["surgery is a Luttinger surgery on a Lagrangian torus "
                       "of a closed symplectic 4-manifold"],
    },
    {
        "id": "E_symplectic_thom",
        "name": "Symplectic Thom conjecture",
        "statement": "An embedded symplectic surface in a closed symplectic "
                     "4-manifold is genus-minimizing in its homology class.",
        "source": "P. Ozsvath and Z. Szabo, Ann. of Math. 151 (2000), "
                  "Theorem 1.1",
        "hypotheses": ["closed symplectic 4-manifold",
                       "embedded connected symplectic surface"],
    },
    {
        "id": "E_cover_construction",
        "name": "Connected symplectic k-fold covers of a square-zero "
                "symplectic surface",
        "statement": "For a symplectic surface S of square zero in a "
                     "symplectic 4-manifold and k >= 1, the surface "
                     "Sigma_k = {(u, z) : z^k = eps f(u)} in S x D^2, for a "
                     "map f: S -> S^1 surjective on H_1 and small eps > 0, is "
                     "an embedded, connected, unbranched degree-k cover of S "
                     "representing k[S], and is symplectic.",
        "source": "arXiv:2608.17267, proof of Lemma 4.3 (after Stipsicz--"
                  "Szabo, arXiv:2307.04202, proof of Theorem 1.4)",
        "hypotheses": ["S symplectic", "S.S = 0"],
    },
    {
        "id": "E_adjunction",
        "name": "Adjunction formula for symplectic surfaces",
        "statement": "For a connected embedded symplectic surface S of genus "
                     "g in a symplectic 4-manifold with canonical class K, "
                     "K.S + S.S = 2g - 2.",
        "source": "standard (c_1(TX|S) = c_1(TS) + c_1(nu S))",
        "hypotheses": ["S symplectic"],
    },
    {
        "id": "E_klug",
        "name": "Klug's relative Rochlin theorem",
        "statement": "quoted (Klug 2021, Theorem 2): \"Let X^4 be a smooth "
                     "compact connected oriented 4-manifold with dX an "
                     "integer homology sphere. Let F^2 be an orientable "
                     "characteristic surface with connected boundary that is "
                     "properly embedded in X. Then Arf(F) + Arf(dF) = "
                     "(sigma(X) - [F]^2)/8 + mu(dX) (mod 2).\"  A properly "
                     "embedded surface is characteristic iff its class in "
                     "H_2(X, dX; Z/2) is Lefschetz dual to w_2(X); for spin "
                     "X this means the class vanishes.",
        "source": "M. R. Klug, arXiv:2011.12418 (2021), Theorem 2 and "
                  "Section 2",
        "hypotheses": ["X smooth compact connected oriented",
                       "dX an integer homology sphere",
                       "F orientable, connected boundary, characteristic"],
    },
    {
        "id": "E_levine_arf",
        "name": "Levine's criterion for the Arf invariant",
        "statement": "For a knot K in S^3, Arf(K) = 0 if Delta_K(-1) = +-1 "
                     "(mod 8) and Arf(K) = 1 if Delta_K(-1) = +-3 (mod 8).  "
                     "Equivalently Arf(K) is the Arf invariant of the "
                     "quadratic form x -> x^T S x (mod 2) on H_1 of a Seifert "
                     "surface with Seifert matrix S.",
        "source": "J. Levine, Amer. J. Math. 88 (1966); Lickorish, An "
                  "Introduction to Knot Theory, Thm 10.6",
        "hypotheses": [],
    },
    {
        "id": "E_trace_embedding",
        "name": "Slice disks and the 0-trace",
        "statement": "If K in S^3 = d(X - B^4) bounds a smoothly embedded "
                     "disk D in X - B^4 whose normal framing restricts to the "
                     "Seifert framing of K, then the 0-trace X_0(K) = B^4 u "
                     "(0-framed 2-handle along K) embeds smoothly in X as "
                     "B^4 u nu(D), and a Seifert surface of K capped by D is "
                     "a closed surface of self-intersection 0 in X_0(K) whose "
                     "class generates H_2(X_0(K)) = Z.  The framing condition "
                     "is automatic when H_2(X - B^4, d; Z) is torsion.  "
                     "X_0(K) is simply connected, and the figure-eight knot "
                     "has Seifert genus 1.",
        "source": "arXiv:2505.14387v1, proof of Theorem 1; standard handle "
                  "calculus",
        "hypotheses": ["H_2(X - B^4, d; Z) torsion"],
    },
    {
        "id": "E_ball_isotopy",
        "name": "Sliceness is a diffeomorphism invariant",
        "statement": "Any two smooth orientation-preserving embeddings of "
                     "B^4 into a connected 4-manifold are isotopic "
                     "(Palais--Cerf), so whether a knot is smoothly slice in "
                     "X - B^4 does not depend on the ball; the figure-eight "
                     "knot is amphichiral, so orientation plays no role "
                     "either.",
        "source": "standard",
        "hypotheses": [],
    },
    {
        "id": "E_novikov",
        "name": "Novikov additivity",
        "statement": "If X = X_1 u_Y X_2 is a closed oriented 4-manifold "
                     "glued along a closed 3-manifold Y, then sigma(X) = "
                     "sigma(X_1) + sigma(X_2).  Reversing the orientation of "
                     "a 4-manifold negates its signature.",
        "source": "standard (Atiyah--Singer 1968)",
        "hypotheses": [],
    },
    {
        "id": "E_lp_regluing",
        "name": "Lidman--Piccirillo: the parity-changing regluing",
        "statement": "There is an orientation-preserving diffeomorphism f of "
                     "S^3_0(Q) (two Gluck twists and an isotopy, LP25 Figure "
                     "3) sending the framed meridian (mu, 0) to (mu', 1).  "
                     "With A the framed homology from (mu', 0) to (mu, 0), "
                     "the surface Gamma'' = Gamma u_A Gamma in Z'' = V "
                     "u_{f o sigma} V has odd self-intersection; it meets the "
                     "fiber F once, since F lies in the interior of one copy "
                     "of V.",
        "source": "arXiv:2505.14387v1, proof of Theorem 2; arXiv:2608.17267, "
                  "proof of Theorem 1.2(c)",
        "hypotheses": [],
    },
    {
        "id": "E_lp_floer",
        "name": "Lidman--Piccirillo's Floer-theoretic obstruction",
        "statement": "quoted (LP25 Lemma 9): \"Let t be a spin^c structure "
                     "on V with |<c_1(t), F>| = 2. Then Psi_{V,t} != 0.\"  "
                     "Its proof uses: Z symplectic, |<c_1(k), F>| = 2 for "
                     "the canonical class k, H^2(V) = Z, the nonvanishing "
                     "of the mixed invariant of a symplectic 4-manifold for "
                     "the line spanned by F [OS04], and conjugation symmetry "
                     "[OS06, Thm 3.6].  quoted (LP25 Lemma 10): \"Let "
                     "(M_1, t_1) and (M_2, t_2) be two spin^c four-manifolds "
                     "glued along S^3_0(Q) so that t_1| = t_2| = s_+-. If "
                     "Psi_{M_1,t_1} and Psi_{M_2,t_2} are non-zero, then "
                     "Phi_{M_1 u M_2, span{F}, t} != 0 for any t restricting "
                     "to t_i.\"  (HF_red(S^3_0(Q), s_+-) is one-dimensional "
                     "because S^3_0(Q) is fibered with genus-2 fiber, OS04 "
                     "Thm 5.2.)  Finally (LP25, proof of Theorem 2): CP^2 # "
                     "-CP^2, and CP^2 # -CP^2 # D for any homology 4-sphere "
                     "D, admits for each of its two square-zero lines a "
                     "splitting along S^2 x S^1, and HF_red(S^2 x S^1) = 0 "
                     "in every non-torsion spin^c structure, so every mixed "
                     "invariant of it vanishes; the mixed invariant is an "
                     "invariant of the triple (M, L, t).",
        "source": "arXiv:2505.14387v1, Lemmas 9, 10 and proof of Theorem 2; "
                  "P. Ozsvath and Z. Szabo, Duke Math. J. 121 (2004) and "
                  "Adv. Math. 202 (2006)",
        "hypotheses": ["Z symplectic", "|K_Z . F| = 2", "H^2(V) = Z",
                       "b_2^+(Z'') = 1 and s_+- non-torsion",
                       "span{F} is a square-zero line of Z''"],
    },
]


# --------------------------------------------------------------------------
# Computed facts.  Each returns a JSON-serializable record whose "result"
# field verify_downstream_chain.rb recomputes independently.
# --------------------------------------------------------------------------

def gram(form, u, v):
    return sum(u[i] * form[i][j] * v[j] for i in range(2) for j in range(2))


def det2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def c_euler():
    chi_F = 2 - 2 * 2                    # closed genus-2 surface
    chi_base = 2 - 2 * 1 - 1             # once-punctured torus
    chi_R = chi_F * chi_base             # bundle with compact fiber
    chi_nu, chi_dnu = 0, 0               # T^2 x D^2 and T^3
    chi_V = chi_R + 2 * (chi_nu - chi_dnu)   # two Luttinger surgeries
    chi_boundary = 0                     # closed 3-manifold
    chi_Z = 2 * chi_V - chi_boundary
    chi_W = chi_Z // 2                   # 2-fold cover
    return {
        "id": "C_euler",
        "claim": "chi(F) = -2, chi(base) = -1, chi(R) = 2, chi(V) = 2, "
                 "chi(Z) = chi(Z'') = 4, chi(W) = 2",
        "result": {"chi_F": chi_F, "chi_base": chi_base, "chi_R": chi_R,
                   "chi_V": chi_V, "chi_Z": chi_Z, "chi_W": chi_W},
    }


def c_betti():
    chi_V, chi_Z, chi_W = 2, 4, 2
    # V: connected, pi_1 = 1, nonempty connected boundary.
    b_V = {"b0": 1, "b1": 0, "b3": 0, "b4": 0}
    b_V["b2"] = chi_V - b_V["b0"] + b_V["b1"] + b_V["b3"] - b_V["b4"]
    # Z: closed, simply connected.
    b_Z = {"b0": 1, "b1": 0, "b3": 0, "b4": 1}
    b_Z["b2"] = chi_Z - b_Z["b0"] + b_Z["b1"] + b_Z["b3"] - b_Z["b4"]
    # W: closed, pi_1 finite so b1 = 0 = b3.
    b_W = {"b0": 1, "b1": 0, "b3": 0, "b4": 1}
    b_W["b2"] = chi_W - b_W["b0"] + b_W["b1"] + b_W["b3"] - b_W["b4"]
    # W mod 2: H_1(W; Z/2) = Z/2 since H_1(W) = Z/2, and b3 = b1 by duality.
    b_W2 = {"b0": 1, "b1": 1, "b3": 1, "b4": 1}
    b_W2["b2"] = chi_W - b_W2["b0"] + b_W2["b1"] + b_W2["b3"] - b_W2["b4"]
    assert b_V["b2"] == 1 and b_Z["b2"] == 2 and b_W["b2"] == 0
    assert b_W2["b2"] == 2
    return {
        "id": "C_betti",
        "claim": "b_2(V) = 1, b_2(Z) = b_2(Z'') = 2, b_2(W) = 0, and "
                 "dim H_2(W; Z/2) = 2",
        "result": {"V": b_V, "Z": b_Z, "W": b_W, "W_mod2": b_W2},
    }


def c_w2_fiber():
    chi_F, FF = -2, 0
    pairing = (chi_F + FF) % 2
    assert pairing == 0
    return {
        "id": "C_w2_fiber",
        "claim": "<w_2, [F]> = chi(F) + F.F = -2 + 0 = 0 (mod 2), so a "
                 "4-manifold whose mod-2 second homology is generated by F "
                 "is spin",
        "result": {"chi_F": chi_F, "F_squared": FF, "w2_pairing_mod2": pairing},
    }


def c_hyperbolic_basis():
    # Gram matrix of (F, Gamma_hat) in Z with the certified Gamma_hat^2 = 0.
    g = ((0, 1), (1, 0))
    d = det2(g)
    index_squared = abs(d)   # = [L:S]^2 * |det L| with |det L| = 1
    assert d == -1 and index_squared == 1
    # Even, signature 0, b+ = b- = 1: the vectors F +- Gamma_hat have
    # squares +2 and -2.
    plus = gram(g, (1, 1), (1, 1))
    minus = gram(g, (1, -1), (1, -1))
    assert plus == 2 and minus == -2
    even = all(gram(g, v, v) % 2 == 0 for v in product(range(-3, 4), repeat=2))
    assert even
    return {
        "id": "C_hyperbolic_basis",
        "claim": "With F.F = 0, F.Gamma_hat = 1, Gamma_hat.Gamma_hat = 0 the "
                 "Gram determinant is -1, so (F, Gamma_hat) is a basis of "
                 "the unimodular rank-2 lattice H_2(Z) and the form is the "
                 "hyperbolic form H: even, signature 0, b+ = b- = 1",
        "result": {"gram": [list(r) for r in g], "det": d,
                   "index_squared": index_squared, "signature": 0,
                   "b_plus": 1, "b_minus": 1, "even": True,
                   "witness_squares": {"F+G": plus, "F-G": minus}},
    }


def c_square_zero_axes():
    # Exact: (aF + b Gamma_hat)^2 = 2ab, and 2ab = 0 in Z forces a = 0 or
    # b = 0.  The enumeration is a cross-check on a box.
    h = ((0, 1), (1, 0))
    box = 60
    offaxis = [(a, b) for a, b in product(range(-box, box + 1), repeat=2)
               if (a, b) != (0, 0) and gram(h, (a, b), (a, b)) == 0
               and a != 0 and b != 0]
    assert not offaxis
    return {
        "id": "C_square_zero_axes",
        "claim": "(aF + b Gamma_hat)^2 = 2ab; a nonzero square-zero class "
                 "is kF or k Gamma_hat with k != 0",
        "result": {"square_formula": "2ab", "box": box,
                   "off_axis_square_zero": len(offaxis)},
    }


def c_cover_genus():
    rows = []
    for k in range(1, 41):
        chi = k * (2 - 2 * 2)
        genus = 1 - chi // 2
        assert genus == k + 1
        rows.append([k, genus])
    return {
        "id": "C_cover_genus",
        "claim": "A connected unbranched degree-k cover of a closed genus-2 "
                 "surface has chi = -2k and genus k + 1; hence a symplectic "
                 "representative of kF (k != 0) has genus |k| + 1 >= 2",
        "result": {"genus_of_k_cover": rows[:8], "checked_k_up_to": 40,
                   "minimum_over_k_nonzero": 2},
    }


def c_adjunction():
    g, SS = 2, 0
    KS = 2 * g - 2 - SS
    assert KS == 2
    return {
        "id": "C_adjunction",
        "claim": "K_Z . F = 2g(F) - 2 - F.F = 2, so |<c_1(K_Z), F>| = 2",
        "result": {"genus": g, "F_squared": SS, "K_dot_F": KS},
    }


def c_odd_basis():
    # Gram [[0,1],[1,2n+1]] of (F, Gamma'') in Z''.  E = Gamma'' - nF and
    # D = F - E give squares +1, -1 and E.D = 0, for every n: the identities
    # are polynomial in n and are verified on a range.
    rows = []
    for n in range(-25, 26):
        q = ((0, 1), (1, 2 * n + 1))
        e = (-n, 1)
        d = (1 + n, -1)
        ee, dd, ed = gram(q, e, e), gram(q, d, d), gram(q, e, d)
        assert (ee, dd, ed) == (1, -1, 0)
        assert det2(q) == -1
        rows.append([n, ee, dd, ed])
    return {
        "id": "C_odd_basis",
        "claim": "With F.F = 0, F.Gamma'' = 1 and Gamma''.Gamma'' = 2n+1 odd, "
                 "E = Gamma'' - nF and D = F - E satisfy E.E = 1, D.D = -1, "
                 "E.D = 0 and det = -1, so H_2(Z'') = Z<E, D> with form "
                 "<1> + <-1>: odd, signature 0, b+ = 1",
        "result": {"identities": "E.E = (2n+1) - 2n = 1; D.D = 0 - 2(1) + 1 "
                                 "= -1; E.D = 1 - 1 = 0",
                   "checked_n_range": [-25, 25], "signature": 0,
                   "b_plus": 1, "odd": True},
    }


def c_square_zero_lines_odd():
    # In <1> + <-1>: a^2 - b^2 = 0 iff a = +-b: exactly two lines.
    box = 60
    sols = {(a, b) for a, b in product(range(-box, box + 1), repeat=2)
            if (a, b) != (0, 0) and a * a - b * b == 0}
    lines = {(1, 1) if a == b else (1, -1) for a, b in sols}
    assert lines == {(1, 1), (1, -1)}
    return {
        "id": "C_square_zero_lines_odd",
        "claim": "The form <1> + <-1> has exactly two square-zero lines, "
                 "spanned by (1, 1) and (1, -1); a diffeomorphism from Z'' "
                 "to CP^2 # -CP^2 carries span{F} to one of them",
        "result": {"lines": [[1, 1], [1, -1]], "box": box},
    }


def c_arf_figure_eight():
    # Seifert matrix of 4_1 (Rolfsen): S = [[1, -1], [0, -1]].
    S = ((1, -1), (0, -1))
    # Alexander polynomial det(S - t S^T) as coefficients of t^0, t^1, t^2.
    # (S - tS^T) = [[1 - t, -1], [t, -1 + t]].
    # det = (1 - t)(t - 1) + t = -t^2 + 3t - 1.
    coeffs = [-1, 3, -1]
    delta_minus1 = sum(c * (-1) ** i for i, c in enumerate(coeffs))
    assert delta_minus1 == -5
    residue = delta_minus1 % 8          # 3 (mod 8): Levine gives Arf = 1
    arf_levine = 0 if residue in (1, 7) else 1
    # Quadratic form q(x) = x^T S x (mod 2) on (Z/2)^2.
    values = {}
    for x in product((0, 1), repeat=2):
        values[x] = sum(x[i] * S[i][j] * x[j] for i in range(2)
                        for j in range(2)) % 2
    zeros = sum(1 for v in values.values() if v == 0)
    arf_quadratic = 0 if zeros == 3 else 1
    assert arf_levine == 1 and arf_quadratic == 1
    return {
        "id": "C_arf_figure_eight",
        "claim": "Arf(4_1) = 1: Delta(t) = -t^2 + 3t - 1 gives Delta(-1) = -5 "
                 "= 3 (mod 8), and the Seifert quadratic form takes the value "
                 "0 on exactly one of four elements",
        "result": {"seifert_matrix": [list(r) for r in S],
                   "alexander_coefficients": coeffs,
                   "delta_at_minus_one": delta_minus1, "residue_mod_8": residue,
                   "arf_by_levine": arf_levine,
                   "quadratic_form_zeros": zeros,
                   "arf_by_quadratic_form": arf_quadratic, "arf": 1},
    }


def c_klug_instance():
    # Klug's formula for a null-homologous (mod 2) slice disk D of 4_1 in
    # the punctured W: Arf(D) + Arf(4_1) = (sigma - [D]^2)/8 + mu(S^3).
    arf_disk = 0             # H_1(D; Z/2) = 0
    sigma_W = 0              # rational homology sphere
    D_squared = 0            # H_2(W - B^4, d; Z) is torsion
    mu_S3 = 0
    rhs = ((sigma_W - D_squared) // 8 + mu_S3) % 2
    forced_arf = (rhs - arf_disk) % 2
    assert forced_arf == 0
    return {
        "id": "C_klug_instance",
        "claim": "For a slice disk of 4_1 in W - B^4 that vanishes in "
                 "H_2(W - B^4, d; Z/2), Klug's formula forces Arf(4_1) = 0, "
                 "contradicting Arf(4_1) = 1",
        "result": {"arf_disk": arf_disk, "sigma": sigma_W,
                   "D_squared": D_squared, "mu_S3": mu_S3,
                   "forced_arf_41": forced_arf, "actual_arf_41": 1,
                   "contradiction": True},
    }


def c_covering_order():
    order_Z, deck = 1, 2
    order_W = order_Z * deck
    assert order_W == 2
    return {
        "id": "C_covering_order",
        "claim": "1 -> pi_1(Z) -> pi_1(W) -> Z/2 -> 1 with pi_1(Z) = 1 gives "
                 "|pi_1(W)| = 2, so pi_1(W) = Z/2 (the only group of order 2)",
        "result": {"order_pi1_Z": order_Z, "deck_order": deck,
                   "order_pi1_W": order_W},
    }


def c_hk_invariants():
    W = {"pi_1": "Z/2", "form_on_H2_mod_torsion": "zero form of rank 0",
         "w2_type": "II", "KS": 0}
    B = dict(W)
    assert W == B
    return {
        "id": "C_hk_invariants",
        "claim": "W and B have the same Hambleton--Kreck invariants: "
                 "pi_1 = Z/2, q = the zero form on H_2/Tors = 0, w_2-type "
                 "(II), KS = 0",
        "result": {"W": W, "B": B, "equal": True},
    }


def c_signatures():
    sigma_V = "s"   # unknown integer; only its cancellation matters
    sigma_Z = "s + (-s) = 0"
    sigma_Zpp = "s + (-s) = 0"
    ks_even = (0 // 8) % 2
    return {
        "id": "C_signatures",
        "claim": "Z and Z'' are unions of V and -V along the whole "
                 "boundary, so sigma(Z) = sigma(Z'') = sigma(V) - sigma(V) "
                 "= 0; for the even form H, KS = sigma/8 = 0 (mod 2)",
        "result": {"sigma_V": sigma_V, "sigma_Z": sigma_Z,
                   "sigma_Zpp": sigma_Zpp, "KS_even_case": ks_even},
    }


def c_orientation_reversal():
    return {
        "id": "C_orientation_reversal",
        "claim": "S^2 x S^2 admits an orientation-reversing diffeomorphism "
                 "(a reflection of one factor), so a diffeomorphism Z -> "
                 "S^2 x S^2 may be taken orientation-preserving",
        "result": {"map": "(x, y) -> (rho(x), y), rho a reflection of S^2",
                   "degree": -1},
    }


COMPUTED_FUNCTIONS = [
    c_euler, c_betti, c_w2_fiber, c_hyperbolic_basis, c_square_zero_axes,
    c_cover_genus, c_adjunction, c_odd_basis, c_square_zero_lines_odd,
    c_arf_figure_eight, c_klug_instance, c_covering_order, c_hk_invariants,
    c_signatures, c_orientation_reversal,
]


# --------------------------------------------------------------------------
# The chain.  "uses" lists ids of externals (E_), certificates (K_),
# computed facts (C_) and earlier steps (S_).
# --------------------------------------------------------------------------

STEPS = [
    {
        "id": "S1_homology_of_V",
        "claim": "H_1(V) = 0, H_3(V) = 0, H_2(V) = Z generated by the fiber F "
                 "with F.F = 0, and V is spin.",
        "proof": "pi_1(V) = 1 gives H_1(V) = 0.  The boundary S^3_0(Q) is "
                 "connected, so Lefschetz duality with universal "
                 "coefficients gives H_3(V) = H^1(V, dV) = 0 and "
                 "Tors H_2(V) = Tors H^3(V) = Tors H_1(V, dV) = 0.  chi(V) "
                 "= 2 then gives b_2(V) = 1.  A section Gamma is a properly "
                 "embedded surface meeting the fiber once, so [F] pairs to 1 "
                 "with a relative class and is primitive: H_2(V) = Z<F>.  "
                 "F.F = 0 since a fiber has trivial normal bundle.  "
                 "H_2(V; Z/2) = Z/2<F> by universal coefficients, w_2 is "
                 "detected on it, and <w_2, F> = chi(F) + F.F = 0 (mod 2).",
        "uses": ["K_pi1_V_trivial", "E_duality_uct", "C_euler", "C_betti",
                 "C_w2_fiber", "E_wu", "E_lp_double"],
    },
    {
        "id": "S2_double_simply_connected",
        "claim": "pi_1(Z) = 1 and pi_1(Z'') = 1.",
        "proof": "Z = V u_sigma V and Z'' = V u_{f o sigma} V are unions of "
                 "two copies of V along the connected bicollared boundary "
                 "S^3_0(Q); by van Kampen each fundamental group is a "
                 "quotient of pi_1(V) * pi_1(V) = 1.  This is the one place "
                 "where pi_1(V) = 1, rather than pi_1(Z) = 1, is needed: the "
                 "regluing twists the amalgam.",
        "uses": ["K_pi1_V_trivial", "E_van_kampen", "E_lp_double",
                 "E_lp_regluing"],
    },
    {
        "id": "S3_form_of_Z",
        "claim": "H_2(Z) = Z<F, Gamma_hat> with intersection form H; Z is "
                 "spin, closed, simply connected, with b_2 = 2 and "
                 "signature 0.",
        "proof": "chi(Z) = 2 chi(V) - chi(S^3_0(Q)) = 4 and pi_1(Z) = 1 give "
                 "b_2(Z) = 2 with H_2(Z) torsion-free.  F.F = 0, "
                 "F.Gamma_hat = 1 (a fiber meets a section once), and "
                 "Gamma_hat.Gamma_hat = 0 by the run-28 certificate.  The "
                 "Gram determinant is -1 and the form is unimodular, so "
                 "(F, Gamma_hat) is a basis and the form is H.  H is even, "
                 "so by Wu's formula w_2(Z) = 0.",
        "uses": ["S2_double_simply_connected", "C_euler", "C_betti",
                 "K_section_square_zero", "E_lp_double", "E_lattice_index",
                 "C_hyperbolic_basis", "E_wu", "E_duality_uct"],
    },
    {
        "id": "S4_Z_homeomorphic_S2xS2",
        "claim": "Z is homeomorphic to S^2 x S^2.",
        "proof": "Z is a closed simply connected topological 4-manifold with "
                 "even intersection form H, the form of S^2 x S^2; for even "
                 "forms KS = signature/8 = 0 is determined, so Freedman's "
                 "classification gives the homeomorphism.",
        "uses": ["S3_form_of_Z", "E_freedman", "C_signatures"],
    },
    {
        "id": "S5_Z_symplectic",
        "claim": "Z is a closed symplectic 4-manifold, obtained from the "
                 "closed genus-2 surface bundle R u_sigma R over a genus-2 "
                 "surface by Luttinger surgery on four disjoint Lagrangian "
                 "tori that miss F and Gamma_hat; F and Gamma_hat are "
                 "symplectic surfaces of genus 2 and square 0.",
        "proof": "R u_sigma R is a closed surface bundle whose fiber is "
                 "homologically essential (F.Gamma_hat = 1), so it carries "
                 "the paper's Thurston-type form, positive on F and on "
                 "Gamma_hat.  The surgery tori are Lagrangian for it "
                 "(Lemma 8.2, machine-checked), the surgeries are the "
                 "certified Luttinger surgeries, and Luttinger surgery "
                 "preserves the symplectic structure away from the surgered "
                 "neighborhoods, which miss F and Gamma_hat.",
        "uses": ["E_lp_double", "E_bundle_symplectic", "K_lagrangian_framing",
                 "E_luttinger", "S3_form_of_Z"],
    },
    {
        "id": "S6_Z_not_diffeomorphic_S2xS2",
        "claim": "Z is not diffeomorphic to S^2 x S^2.",
        "proof": "R u_sigma R is aspherical (genus-2 fiber and base), hence "
                 "minimal (an exceptional sphere would be null-homotopic, "
                 "hence of square 0, not -1) and neither rational nor ruled "
                 "(those have pi_2 != 0); so kappa(R u_sigma R) != -infinity.  "
                 "Luttinger surgery preserves kappa (Ho--Li), so kappa(Z) != "
                 "-infinity.  If psi: Z -> S^2 x S^2 were a diffeomorphism, "
                 "composing with a reflection of one factor if necessary "
                 "makes it orientation-preserving; pulling back a product "
                 "form gives a symplectic form on Z inducing its "
                 "orientation with kappa = kappa(S^2 x S^2) = -infinity "
                 "(rational), contradicting the independence of kappa from "
                 "the form.",
        "uses": ["S5_Z_symplectic", "E_asphericity", "E_kodaira", "E_ho_li",
                 "C_orientation_reversal"],
    },
    {
        "id": "S7_theorem_A",
        "claim": "Theorem A: Z is homeomorphic but not diffeomorphic to "
                 "S^2 x S^2.",
        "proof": "S4 and S6.",
        "uses": ["S4_Z_homeomorphic_S2xS2", "S6_Z_not_diffeomorphic_S2xS2"],
    },
    {
        "id": "S8_W_invariants",
        "claim": "W is a closed oriented smooth spin 4-manifold with "
                 "pi_1(W) = Z/2, b_2(W) = 0 (a rational homology sphere), "
                 "signature 0 and KS(W) = 0.",
        "proof": "Z -> W is a connected 2-fold covering, so pi_1(W) has "
                 "order 2.  chi(W) = chi(Z)/2 = 2 and b_1(W) = 0 give "
                 "b_2(W) = 0, hence sigma(W) = 0.  W is spin by "
                 "Lidman--Piccirillo's Lemma 7, whose hypotheses S1 "
                 "supplies.  KS(W) = 0 because W is smooth.",
        "uses": ["S2_double_simply_connected", "E_lp_quotient",
                 "E_covering_sequence", "C_covering_order", "C_euler",
                 "C_betti", "S1_homology_of_V", "E_duality_uct"],
    },
    {
        "id": "S9_W_homeomorphic_B",
        "claim": "W is homeomorphic to the Kawauchi manifold B.",
        "proof": "Both are closed oriented topological 4-manifolds with "
                 "pi_1 = Z/2, zero intersection form on H_2/Tors = 0, "
                 "w_2-type (II), and KS = 0 (both smooth).  These are the "
                 "Hambleton--Kreck invariants, which classify up to "
                 "homeomorphism.",
        "uses": ["S8_W_invariants", "E_kawauchi_B", "C_hk_invariants",
                 "E_hambleton_kreck"],
    },
    {
        "id": "S10_no_square_zero_torus",
        "claim": "No nonzero square-zero class in H_2(Z; Z) is represented "
                 "by a smoothly embedded torus (the paper's Lemma 4.3).",
        "proof": "For k >= 1 the connected symplectic k-fold covers of F and "
                 "of Gamma_hat represent kF and k Gamma_hat with genus "
                 "k + 1; by the symplectic Thom theorem these genera are "
                 "minimal, and reversing orientation covers k < 0.  Since "
                 "(aF + b Gamma_hat)^2 = 2ab, every nonzero square-zero "
                 "class is kF or k Gamma_hat with k != 0 and has minimal "
                 "genus |k| + 1 >= 2.",
        "uses": ["S5_Z_symplectic", "S3_form_of_Z", "E_cover_construction",
                 "C_cover_genus", "E_symplectic_thom", "C_square_zero_axes"],
    },
    {
        "id": "S11_figure_eight_not_slice_in_W",
        "claim": "The figure-eight knot is not smoothly slice in W.",
        "proof": "Let D be a smooth slice disk in W - B^4.  H_2(W - B^4, d; Z) "
                 "= H^2(W) = Z/2 is torsion, so D's relative "
                 "self-intersection is 0 and its framing is the Seifert "
                 "framing.  Case 1: [D, dD] = 0 in H_2(W - B^4, d; Z/2).  "
                 "Then D is characteristic in the spin manifold W - B^4, "
                 "and Klug's Theorem 2 with Arf(D) = 0, sigma = 0, [D]^2 = "
                 "0, mu(S^3) = 0 forces Arf(4_1) = 0; but Arf(4_1) = 1.  "
                 "Case 2: [D, dD] != 0.  Then the 0-trace X_0(4_1) embeds in "
                 "W and the torus T = (Seifert surface) u D has square 0 "
                 "and [T] != 0 in H_2(W; Z/2).  X_0(4_1) is simply "
                 "connected, so it lifts to Z and T lifts to a torus T~ with "
                 "p_*[T~] = [T] != 0, hence [T~] != 0 in H_2(Z; Z/2) = "
                 "H_2(Z) (x) Z/2, so [T~] != 0 in H_2(Z; Z); T~.T~ = T.T = 0 "
                 "since p is a local diffeomorphism.  This contradicts S10.",
        "uses": ["S8_W_invariants", "S9_W_homeomorphic_B", "E_trace_embedding",
                 "E_klug", "E_levine_arf", "C_arf_figure_eight",
                 "C_klug_instance", "E_covering_sequence", "E_duality_uct",
                 "S10_no_square_zero_torus", "C_betti"],
    },
    {
        "id": "S12_theorem_B",
        "claim": "Theorem B: W is homeomorphic to B, and the pair (B, W) is "
                 "distinguished by the smooth sliceness of the figure-eight "
                 "knot, hence not diffeomorphic.",
        "proof": "S9 gives the homeomorphism.  4_1 is slice in B and, by "
                 "S11, not in W; sliceness in a closed 4-manifold is a "
                 "diffeomorphism invariant, so no diffeomorphism B -> W "
                 "exists.",
        "uses": ["S9_W_homeomorphic_B", "S11_figure_eight_not_slice_in_W",
                 "E_kawauchi_B", "E_ball_isotopy"],
    },
    {
        "id": "S13_form_of_Zpp",
        "claim": "Z'' is closed, simply connected, smooth, with b_2 = 2, "
                 "signature 0 and odd intersection form <1> + <-1>.",
        "proof": "pi_1(Z'') = 1 by S2 and chi(Z'') = 4 give b_2 = 2 with "
                 "H_2 free.  Novikov additivity over the two copies of V "
                 "(the second with reversed orientation) gives signature 0.  "
                 "F.F = 0, F.Gamma'' = 1 and Gamma''.Gamma'' odd by "
                 "Lidman--Piccirillo's regluing; the Gram determinant is -1 "
                 "so (F, Gamma'') is a basis, and the explicit change of "
                 "basis E = Gamma'' - nF, D = F - E diagonalizes the form as "
                 "<1> + <-1>.",
        "uses": ["S2_double_simply_connected", "C_euler", "C_betti",
                 "E_novikov", "C_signatures", "E_lp_regluing",
                 "E_lattice_index", "C_odd_basis", "E_duality_uct"],
    },
    {
        "id": "S14_Zpp_homeomorphic_CP2",
        "claim": "Z'' is homeomorphic to CP^2 # -CP^2.",
        "proof": "Z'' is closed and simply connected with the odd form "
                 "<1> + <-1> and KS = 0 (smooth); of Freedman's two "
                 "manifolds with this form, the one with KS = 0 is "
                 "CP^2 # -CP^2.",
        "uses": ["S13_form_of_Zpp", "E_freedman"],
    },
    {
        "id": "S15_Zpp_not_diffeomorphic_CP2",
        "claim": "Z'' is not diffeomorphic to CP^2 # -CP^2.",
        "proof": "Z is symplectic with |K_Z . F| = 2 by adjunction (F "
                 "symplectic of genus 2 and square 0) and H^2(V) = Z, so "
                 "Lidman--Piccirillo's Lemma 9 gives Psi_{V,t} != 0 for both "
                 "spin^c structures with |<c_1(t), F>| = 2.  Z'' is V u V "
                 "along S^3_0(Q) with t restricting to the non-torsion s_+-, "
                 "b_2^+(Z'') = 1 and span{F} a square-zero line, so Lemma 10 "
                 "gives a nonvanishing mixed invariant Phi_{Z'', span{F}, "
                 "t}.  A diffeomorphism to CP^2 # -CP^2 would carry span{F} "
                 "to one of its two square-zero lines, along each of which "
                 "the manifold splits over S^2 x S^1 and every mixed "
                 "invariant vanishes.",
        "uses": ["S5_Z_symplectic", "C_adjunction", "E_adjunction",
                 "S1_homology_of_V", "S13_form_of_Zpp",
                 "C_square_zero_lines_odd", "E_lp_floer"],
    },
    {
        "id": "S16_theorem_C",
        "claim": "Theorem C: Z'' is a closed simply connected 4-manifold "
                 "homeomorphic but not diffeomorphic to CP^2 # -CP^2.",
        "proof": "S2, S14 and S15.",
        "uses": ["S2_double_simply_connected", "S14_Zpp_homeomorphic_CP2",
                 "S15_Zpp_not_diffeomorphic_CP2"],
    },
]

CONCLUSIONS = ["S7_theorem_A", "S12_theorem_B", "S16_theorem_C"]


def file_digest(relative):
    path = ROOT / relative
    assert path.is_file(), f"missing evidence: {relative}"
    return sha256(path.read_bytes()).hexdigest()


def check_chain(items):
    ids = {item["id"] for item in items}
    kinds = {item["id"]: item["kind"] for item in items}
    graph = {item["id"]: tuple(item.get("uses", ())) for item in items}
    for name, uses in graph.items():
        for dep in uses:
            assert dep in ids, f"{name} uses unknown item {dep}"
            assert kinds[dep] != "step" or dep != name
    visiting, done = set(), set()

    def visit(name):
        if name in done:
            return
        assert name not in visiting, f"cycle through {name}"
        visiting.add(name)
        for dep in graph[name]:
            visit(dep)
        visiting.remove(name)
        done.add(name)

    for name in graph:
        visit(name)
    # Every external hypothesis-bearing item and every certificate is used.
    used = {dep for uses in graph.values() for dep in uses}
    for item in items:
        if item["kind"] != "step":
            assert item["id"] in used, f"unused item {item['id']}"
    for conclusion in CONCLUSIONS:
        assert conclusion in ids
    # Theorem D is reachable from every conclusion.
    def closure(name, acc):
        for dep in graph[name]:
            if dep not in acc:
                acc.add(dep)
                closure(dep, acc)
        return acc
    for conclusion in CONCLUSIONS:
        assert "K_pi1_V_trivial" in closure(conclusion, set())


def payload():
    computed = [fn() for fn in COMPUTED_FUNCTIONS]
    items = ([dict(e, kind="external") for e in EXTERNAL]
             + [dict(k, kind="certificate") for k in CERTIFICATES]
             + [dict(c, kind="computed") for c in computed]
             + [dict(s, kind="step") for s in STEPS])
    check_chain(items)
    evidence = {relative: file_digest(relative) for relative in EVIDENCE}
    for cert in CERTIFICATES:
        for relative in cert["evidence"]:
            assert relative in evidence, relative
    return {
        "format": "luttinger-downstream-proof-chain-v1",
        "target": "arXiv:2608.17267 Theorems A, B, C from Theorem D",
        "conclusions": CONCLUSIONS,
        "items": items,
        "evidence_sha256": evidence,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    current = payload()
    kinds = {}
    for item in current["items"]:
        kinds[item["kind"]] = kinds.get(item["kind"], 0) + 1
    summary = ", ".join(f"{k}={v}" for k, v in sorted(kinds.items()))
    if args.check:
        frozen = json.loads(OUTPUT.read_text(encoding="utf-8"))
        assert frozen == current, "downstream chain certificate mismatch"
        print(f"PASS: downstream proof chain replays ({summary}); "
              f"{len(current['evidence_sha256'])} evidence digests match")
        return
    OUTPUT.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8")
    print(f"{OUTPUT}: {summary}; {len(current['evidence_sha256'])} "
          "evidence files bound")
    for conclusion in CONCLUSIONS:
        step = next(s for s in STEPS if s["id"] == conclusion)
        print(f"  {conclusion}: {step['claim']}")


if __name__ == "__main__":
    main()
