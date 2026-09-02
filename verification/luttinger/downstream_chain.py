#!/usr/bin/env python3
"""The existence chain: from certified triviality of pi_1(V_aud) to
Theorem A' -- Z_aud = V_aud u_{sigma_aud} V_aud is a closed symplectic
4-manifold homeomorphic but not diffeomorphic to S^2 x S^2 -- with no
assumption and no reference to any other author's construction.

Every item is one of five kinds:

  external     a theorem from the literature, stated with its hypotheses and
               its source, which this project does not reprove;
  certificate  a machine certificate of this repository, bound by SHA-256;
  proof        a written proof in this repository (a paper fragment and its
               run record), bound by SHA-256, with its premises listed;
  computed     a finite calculation executed here and replayed independently
               by verify_downstream_chain.rb;
  step         a deduction whose premises are earlier items of the chain.

There is no "assumption" kind.  check_chain() fails if any item is an
assumption, if any item's text mentions Lidman--Piccirillo, Wuebben, or the
source-formalization clauses D1--D14, or if the conclusion does not rest on
the three intrinsic pillars K_pi1_Vaud_trivial, K_sigma_aud, P_double_form.
The comparison with other authors' manifolds is the attribution track,
attribution/wuebben_transfer_chain.py, which this chain never cites.

Run without arguments to recompute everything and write
downstream_chain_certificate.json; run with --check to recompute and compare
with the frozen file.
"""

import argparse
import json
from hashlib import sha256
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent          # repository root: paper/ and verification/
OUTPUT = HERE / "downstream_chain_certificate.json"

# --------------------------------------------------------------------------
# Objects (paper/main.tex, Sections 2, 6 and 7).
#
#   F          closed genus-2 surface with the marked five-chain and points p, O
#   phi_0,     the clutching maps of Definition def:Vaudit; both fix p and O
#   psi_0      and preserve one area form Omega (lem:bundle-symplectic-form)
#   R_aud      the genus-2 bundle over Sigma_{1,1} clutched by phi_0, psi_0
#   M_h        dR_aud, the mapping torus of the boundary monodromy h
#   V_aud      R_aud after the two product-framed fillings on T_alpha, T_beta
#   sigma_aud  [z,t] -> [phi_0 z, 1-t] on M_h                    (Run 72)
#   R_hat      R_aud u_{sigma_aud} R_aud;  Z_aud = V_aud u_{sigma_aud} V_aud
#   F          a fiber away from the tori;  Gamma = {p} x Sigma_{1,1};
#   Gamma_hat  Gamma u_{sigma_aud} Gamma, closed of genus 2
# --------------------------------------------------------------------------

EVIDENCE = [
    # pi_1(V_aud) = 1: the sealed chain (run 66) and the earlier export.
    "verification/luttinger/proof_certificates/manifest.json",
    "verification/luttinger/sealed_transport/r_presentations.json",
    "verification/luttinger/r_presentations.json",
    "verification/runs/66-sealed-tietze-transport.txt",
    "verification/runs/67-r3-complement-and-lp-disagreement.txt",
    "verification/luttinger/alpha_residual/source.json",
    "verification/luttinger/alpha_residual/certificate.json.gz",
    "verification/runs/68-alpha-longitude-sealed-certificate.txt",
    "verification/luttinger/beta_residual/source.json",
    "verification/luttinger/beta_residual/certificate.json.gz",
    "verification/runs/69-beta-longitude-sealed-certificate.txt",
    "verification/runs/29-independent-filled-group-certificates.txt",
    "verification/runs/57-second-certificate-verifier.txt",
    "verification/runs/20-direct-peripheral-fillings-trivial.txt",
    "verification/runs/22-model-correspondence-and-framing.txt",
    # Gamma_hat . Gamma_hat = 0 on the simplicial model.
    "verification/runs/28-pl-self-intersection-certificate.txt",
    "verification/notes/pl_self_intersection_certificate_2026-08-24.md",
    # Lagrangian framing = fibered framing.
    "verification/runs/35-framing-lemma-referee-packet.txt",
    "verification/runs/43-weinstein-chart-independence.txt",
    "verification/runs/46-direct-equivariant-moser.txt",
    "verification/runs/47-cumulative-moser-flow.txt",
    "verification/notes/framing_lemma_referee_packet_2026-08-25.md",
    # sigma_aud and the double.
    "verification/luttinger/sigma_aud/sigma_aud_check.py",
    "verification/luttinger/sigma_aud/output.txt",
    "verification/luttinger/sigma_aud/SHA256SUMS",
    "verification/runs/72-sigma-aud-boundary-involution.txt",
    "verification/runs/73-symplectic-form-on-the-double.txt",
    # The written proofs (Sections 6 and 7 of the main paper).
    "paper/main.tex",
]

CERTIFICATES = [
    {
        "id": "K_pi1_Vaud_trivial",
        "claim": "pi_1(V_aud) = 1: each of the four n=0 filled "
                 "presentations of the sealed complement presentation "
                 "(whose Tietze transport from the serialized raw complex "
                 "replays from frozen files) carries a derivation-DAG "
                 "certificate accepted by two independent checkers, the "
                 "four fillings of the earlier four-generator export reach "
                 "the same verdicts, and the audit-model peripheral "
                 "identification shows they present pi_1(V_aud); the "
                 "alpha and beta paper-coordinate identities are separately "
                 "certified inside the sealed complement (runs 68--69).",
        "evidence": ["verification/luttinger/proof_certificates/manifest.json",
                     "verification/luttinger/sealed_transport/r_presentations.json",
                     "verification/luttinger/r_presentations.json",
                     "verification/runs/66-sealed-tietze-transport.txt",
                     "verification/runs/67-r3-complement-and-lp-disagreement.txt",
                     "verification/luttinger/alpha_residual/source.json",
                     "verification/luttinger/alpha_residual/certificate.json.gz",
                     "verification/runs/68-alpha-longitude-sealed-certificate.txt",
                     "verification/luttinger/beta_residual/source.json",
                     "verification/luttinger/beta_residual/certificate.json.gz",
                     "verification/runs/69-beta-longitude-sealed-certificate.txt",
                     "verification/runs/29-independent-filled-group-certificates.txt",
                     "verification/runs/57-second-certificate-verifier.txt",
                     "verification/runs/20-direct-peripheral-fillings-trivial.txt",
                     "verification/runs/22-model-correspondence-and-framing.txt"],
        "ledger": "C_pi1_Vaud_trivial",
    },
    {
        "id": "K_section_square_zero",
        "claim": "Gamma_hat = Gamma u_{sigma_aud} Gamma is a closed "
                 "orientable genus-2 surface with Gamma_hat . Gamma_hat = 0: "
                 "certified on the simplicial model with an explicit normal "
                 "push-off for every constant boundary clutching rotation "
                 "(run 28); the derivative of sigma_aud at p is phi_0's "
                 "action on the 24-cycle link of p, shift 12 = -I, the "
                 "'constant clutch shift 2' case (run 72).",
        "evidence": ["verification/runs/28-pl-self-intersection-certificate.txt",
                     "verification/notes/pl_self_intersection_certificate_2026-08-24.md",
                     "verification/runs/72-sigma-aud-boundary-involution.txt"],
        "ledger": "G_section_square_zero",
    },
    {
        "id": "K_lagrangian_framing",
        "claim": "For the split form omega_K on R_aud the tori T_alpha, "
                 "T_beta are Lagrangian and their Lagrangian framing is the "
                 "fibered framing of the certified longitudes, so the two "
                 "product-framed fillings defining V_aud are Luttinger "
                 "surgeries.",
        "evidence": ["verification/runs/35-framing-lemma-referee-packet.txt",
                     "verification/runs/43-weinstein-chart-independence.txt",
                     "verification/runs/46-direct-equivariant-moser.txt",
                     "verification/runs/47-cumulative-moser-flow.txt",
                     "verification/notes/framing_lemma_referee_packet_2026-08-25.md"],
        "ledger": "G_lagrangian_framing",
    },
    {
        "id": "K_sigma_aud",
        "claim": "sigma_aud[z,t] = [phi_0 z, 1-t] is a well-defined "
                 "fiber-preserving involution of M_h = dR_aud = dV_aud "
                 "covering the reflection t -> 1-t of the base circle, "
                 "reversing orientation (phi_0 preserves the fiber's, the "
                 "reflection reverses the base's), and carrying each of the "
                 "circles {p} x S^1, {O} x S^1 onto itself.  The seam "
                 "identity phi_0 h phi_0^-1 = h^-1 is verified exactly on "
                 "the certified based monodromy actions, as automorphisms "
                 "of the free group on x, y, r, s and on H_1(F), for all "
                 "four commutator conventions of h; also (h phi_0)^2 = id.",
        "evidence": ["verification/luttinger/sigma_aud/sigma_aud_check.py",
                     "verification/luttinger/sigma_aud/output.txt",
                     "verification/luttinger/sigma_aud/SHA256SUMS",
                     "verification/runs/72-sigma-aud-boundary-involution.txt",
                     "paper/main.tex"],
        "ledger": "G_sigma_aud",
    },
]

PROOFS = [
    {
        "id": "P_split_form",
        "claim": "The clutching maps may be chosen to preserve one positive "
                 "area form Omega on F, phi_0 as the stated half-rotation on "
                 "a collar of c and psi_0 the identity on a collar of e, "
                 "both fixing p and O; in the resulting flat product atlas "
                 "omega_K = Omega_vert + K pi^* eta is a symplectic form on "
                 "R_aud for every K > 0 and every positive area form eta on "
                 "Sigma_{1,1}, T_alpha and T_beta are Lagrangian, and each "
                 "has a protected neighborhood with split coordinates "
                 "omega_K = f dt ^ dtheta_1 + K du ^ dtheta_2.",
        "where": "paper/main.tex, lem:bundle-symplectic-form",
        "evidence": ["paper/main.tex"],
        "uses": [],
    },
    {
        "id": "P_audit_double",
        "claim": "R_hat = R_aud u_{sigma_aud} R_aud is a closed oriented "
                 "genus-2 surface bundle over the closed genus-2 surface "
                 "Sigma_hat = Sigma_{1,1} u_rho Sigma_{1,1}, oriented "
                 "compatibly with both copies; Z_aud = V_aud u_{sigma_aud} "
                 "V_aud is R_hat surgered on four pairwise disjoint interior "
                 "tori -- T_alpha, T_beta and their images under the swap of "
                 "the copies -- all missing a fiber F and the doubled section "
                 "Gamma_hat; Gamma_hat is closed of genus 2; F.F = 0, "
                 "F.Gamma_hat = 1, Gamma_hat.Gamma_hat = 0.",
        "where": "paper/main.tex, lem:sigma-aud and cor:audit-double",
        "evidence": ["paper/main.tex",
                     "verification/runs/72-sigma-aud-boundary-involution.txt"],
        "uses": ["K_sigma_aud", "K_section_square_zero"],
    },
    {
        "id": "P_double_form",
        "claim": "With eta = ds ^ dt on a boundary collar disjoint from the "
                 "annular collars of alpha, beta: eta glues to a positive "
                 "area form eta_hat on Sigma_hat (the second copy's collar "
                 "coordinates are t' = 1-t, s' = -s, and ds' ^ dt' = ds ^ dt); "
                 "Omega_vert glues to a closed vertical form on R_hat "
                 "(sigma_aud is fiberwise the constant Omega-preserving "
                 "phi_0); omega_hat_K = Omega_hat_vert + K pi_hat^* eta_hat "
                 "is symplectic on R_hat, restricts to omega_K on each copy, "
                 "is positive on F and on Gamma_hat, and the four surgery "
                 "tori are Lagrangian with protected split coordinates "
                 "disjoint from the seam collar.",
        "where": "paper/main.tex, lem:double-form",
        "evidence": ["paper/main.tex",
                     "verification/runs/73-symplectic-form-on-the-double.txt"],
        "uses": ["P_split_form", "K_sigma_aud", "P_audit_double"],
    },
]

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
                     "value of KS.  A smooth manifold has KS = 0.",
        "source": "M. H. Freedman, J. Differential Geom. 17 (1982), "
                  "Theorem 1.5",
        "hypotheses": ["closed", "simply connected", "topological 4-manifold"],
    },
    {
        "id": "E_luttinger",
        "name": "Luttinger surgery is symplectic and local",
        "statement": "Luttinger surgery on a Lagrangian torus in a "
                     "symplectic 4-manifold, along the Lagrangian framing, "
                     "produces a symplectic 4-manifold whose form agrees "
                     "with the original outside the surgered neighborhood; "
                     "it replaces T^2 x D^2 by T^2 x D^2, so the Euler "
                     "characteristic is unchanged.",
        "source": "K. Luttinger, J. Differential Geom. 42 (1995); Auroux, "
                  "Donaldson, Katzarkov, Math. Ann. 326 (2003), Definition "
                  "2.1 and Proposition 2.2",
        "hypotheses": ["torus Lagrangian", "slope Lagrangian-framed"],
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
        "name": "Symplectic Kodaira dimension (Li), its -infinity "
                "characterization (Liu), and its oriented-diffeomorphism "
                "invariance (Li)",
        "statement": "Definition (Li, Clay Math. Proc. 5 (2006), Definition "
                     "2.2): for a minimal closed symplectic 4-manifold "
                     "(M, omega) with canonical class K, kappa(M, omega) = "
                     "-infinity if K.[omega] < 0 or K.K < 0, 0 if both vanish, "
                     "1 if K.[omega] > 0 and K.K = 0, 2 if both are positive; "
                     "for a non-minimal manifold it is that of any symplectic "
                     "minimal model.  Theorem 2.4(2) there (attributed to "
                     "Liu 1996): quoted, \"(M, omega) has Kodaira dimension "
                     "-infinity if and only if it is rational or ruled\", "
                     "rational meaning the underlying smooth manifold is "
                     "S^2 x S^2 or CP^2 # k(-CP^2), ruled meaning an S^2-bundle "
                     "over a surface blown up k >= 0 times; all have pi_2 != 0 "
                     "since each contains a homologically nonzero embedded "
                     "sphere.  Invariance (p. 251): quoted, \"the Kodaira "
                     "dimension of (M, omega) only depends on the oriented "
                     "diffeomorphism type of M, i.e. if omega' is another "
                     "symplectic form on M compatible with the orientation of "
                     "M, then kappa(M, omega) = kappa(M, omega')\".",
        "source": "T.-J. Li, The Kodaira dimension of symplectic "
                  "4-manifolds, Clay Math. Proc. 5 (2006), 249--261, "
                  "Definition 2.2, Theorem 2.4(2), p. 251; T.-J. Li, J. "
                  "Differential Geom. 74 (2006), 321--352; A.-K. Liu, Math. "
                  "Res. Lett. 3 (1996), 569--585",
        "hypotheses": ["M closed oriented; every symplectic form compatible "
                       "with that orientation; minimality for the -infinity "
                       "characterization"],
    },
    {
        "id": "E_ho_li",
        "name": "Ho--Li: Luttinger surgery preserves Kodaira dimension",
        "statement": "quoted (Ho--Li 2012, Theorem 1.1): \"The Luttinger "
                     "surgery preserves the symplectic Kodaira dimension.\"",
        "source": "C.-I. Ho and T.-J. Li, Asian J. Math. 16 (2012), "
                  "299--318, Theorem 1.1 (numbering as in arXiv:1108.0479v2)",
        "hypotheses": ["surgery is the Luttinger surgery of Ho--Li Section "
                       "2.1 (Auroux--Donaldson--Katzarkov), on a Lagrangian "
                       "torus of a closed oriented symplectic 4-manifold"],
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
    chi_boundary = 0                     # closed 3-manifold M_h
    chi_Z = 2 * chi_V - chi_boundary
    assert (chi_V, chi_Z) == (2, 4)
    return {
        "id": "C_euler",
        "claim": "chi(F) = -2, chi(Sigma_{1,1}) = -1, chi(R_aud) = 2, "
                 "chi(V_aud) = 2, chi(Z_aud) = 4",
        "result": {"chi_F": chi_F, "chi_base": chi_base, "chi_R": chi_R,
                   "chi_V": chi_V, "chi_Z": chi_Z},
    }


def c_betti():
    chi_V, chi_Z = 2, 4
    # V_aud: connected, pi_1 = 1, nonempty connected boundary.
    b_V = {"b0": 1, "b1": 0, "b3": 0, "b4": 0}
    b_V["b2"] = chi_V - b_V["b0"] + b_V["b1"] + b_V["b3"] - b_V["b4"]
    # Z_aud: closed, simply connected.
    b_Z = {"b0": 1, "b1": 0, "b3": 0, "b4": 1}
    b_Z["b2"] = chi_Z - b_Z["b0"] + b_Z["b1"] + b_Z["b3"] - b_Z["b4"]
    assert b_V["b2"] == 1 and b_Z["b2"] == 2
    return {
        "id": "C_betti",
        "claim": "b_2(V_aud) = 1 and b_2(Z_aud) = 2",
        "result": {"V": b_V, "Z": b_Z},
    }


def c_hyperbolic_basis():
    # Gram matrix of (F, Gamma_hat) in Z_aud with the certified Gamma_hat^2 = 0.
    g = ((0, 1), (1, 0))
    d = det2(g)
    index_squared = abs(d)   # = [L:S]^2 * |det L| with |det L| = 1
    assert d == -1 and index_squared == 1
    plus = gram(g, (1, 1), (1, 1))
    minus = gram(g, (1, -1), (1, -1))
    assert plus == 2 and minus == -2
    even = all(gram(g, v, v) % 2 == 0 for v in product(range(-3, 4), repeat=2))
    assert even
    return {
        "id": "C_hyperbolic_basis",
        "claim": "With F.F = 0, F.Gamma_hat = 1, Gamma_hat.Gamma_hat = 0 the "
                 "Gram determinant is -1, so (F, Gamma_hat) is a basis of "
                 "the unimodular rank-2 lattice H_2(Z_aud) and the form is "
                 "the hyperbolic form H: even, signature 0, b+ = b- = 1",
        "result": {"gram": [list(r) for r in g], "det": d,
                   "index_squared": index_squared, "signature": 0,
                   "b_plus": 1, "b_minus": 1, "even": True,
                   "witness_squares": {"F+G": plus, "F-G": minus}},
    }


def c_signatures():
    sigma_V = "s"   # unknown integer; only its cancellation matters
    sigma_Z = "s + (-s) = 0"
    ks_smooth = 0
    return {
        "id": "C_signatures",
        "claim": "Z_aud is the union of V_aud and -V_aud along the whole "
                 "boundary, so sigma(Z_aud) = sigma(V_aud) - sigma(V_aud) = 0 "
                 "(also read off the form H); Z_aud is smooth, so KS = 0",
        "result": {"sigma_V": sigma_V, "sigma_Z": sigma_Z,
                   "KS_smooth": ks_smooth},
    }


def c_orientation_reversal():
    return {
        "id": "C_orientation_reversal",
        "claim": "S^2 x S^2 admits an orientation-reversing diffeomorphism "
                 "(a reflection of one factor), so a diffeomorphism Z_aud -> "
                 "S^2 x S^2 may be taken orientation-preserving",
        "result": {"map": "(x, y) -> (rho(x), y), rho a reflection of S^2",
                   "degree": -1},
    }


COMPUTED_FUNCTIONS = [
    c_euler, c_betti, c_hyperbolic_basis, c_signatures,
    c_orientation_reversal,
]


# --------------------------------------------------------------------------
# The chain.  "uses" lists ids of externals (E_), certificates (K_), proofs
# (P_), computed facts (C_) and earlier steps (S_).
# --------------------------------------------------------------------------

STEPS = [
    {
        "id": "S0_pi1_Vaud_trivial",
        "claim": "pi_1(V_aud) = 1.",
        "proof": "The certificate K_pi1_Vaud_trivial, read literally: the "
                 "certified presentations present pi_1(V_aud), and each is "
                 "certified trivial.",
        "uses": ["K_pi1_Vaud_trivial"],
    },
    {
        "id": "S2_double_simply_connected",
        "claim": "pi_1(Z_aud) = 1.",
        "proof": "Z_aud = V_aud u_{sigma_aud} V_aud is a union of two copies "
                 "of V_aud along the connected bicollared boundary M_h; by "
                 "van Kampen pi_1(Z_aud) is a quotient of pi_1(V_aud) * "
                 "pi_1(V_aud) = 1.",
        "uses": ["S0_pi1_Vaud_trivial", "E_van_kampen", "P_audit_double"],
    },
    {
        "id": "S3_form_of_Z",
        "claim": "H_2(Z_aud) = Z<F, Gamma_hat> with intersection form H; "
                 "Z_aud is closed, smooth, simply connected and spin, with "
                 "b_2 = 2 and signature 0.",
        "proof": "chi(Z_aud) = 2 chi(V_aud) - chi(M_h) = 4 and pi_1(Z_aud) = 1 "
                 "give b_2 = 2 with H_2 torsion-free.  F.F = 0, "
                 "F.Gamma_hat = 1 and Gamma_hat.Gamma_hat = 0 by "
                 "cor:audit-double and the run-28 certificate.  The Gram "
                 "determinant is -1 and the form is unimodular, so "
                 "(F, Gamma_hat) is a basis and the form is H.  H is even, "
                 "so by Wu's formula w_2(Z_aud) = 0.",
        "uses": ["S2_double_simply_connected", "C_euler", "C_betti",
                 "K_section_square_zero", "P_audit_double", "E_lattice_index",
                 "C_hyperbolic_basis", "E_wu", "E_duality_uct"],
    },
    {
        "id": "S4_Z_homeomorphic_S2xS2",
        "claim": "Z_aud is homeomorphic to S^2 x S^2.",
        "proof": "Z_aud is a closed simply connected 4-manifold with even "
                 "intersection form H, the form of S^2 x S^2, and KS = 0 "
                 "because it is smooth; Freedman's classification gives the "
                 "homeomorphism.",
        "uses": ["S3_form_of_Z", "E_freedman", "C_signatures"],
    },
    {
        "id": "S5_Z_symplectic",
        "claim": "Z_aud is a closed symplectic 4-manifold, obtained from the "
                 "closed genus-2 surface bundle (R_hat, omega_hat_K) by "
                 "Luttinger surgery on four disjoint Lagrangian tori that "
                 "miss F and Gamma_hat; F and Gamma_hat are symplectic "
                 "surfaces of genus 2 and square 0.",
        "proof": "omega_hat_K is symplectic on R_hat, positive on F and "
                 "Gamma_hat, and the four tori are Lagrangian with split "
                 "protected coordinates (lem:double-form).  On each copy the "
                 "form is omega_K, so the product-framed filling slopes are "
                 "the Lagrangian-framing classes (thm:framing, certified); "
                 "the mirror tori are carried to T_alpha, T_beta by the swap "
                 "of the copies, which is a symplectomorphism (phi_0 "
                 "preserves Omega, (t,s) -> (1-t,-s) preserves ds ^ dt).  "
                 "So the four surgeries are Luttinger surgeries, and the "
                 "surgered form agrees with omega_hat_K away from the four "
                 "neighborhoods, which miss F and Gamma_hat.",
        "uses": ["P_double_form", "K_lagrangian_framing", "E_luttinger",
                 "P_audit_double"],
    },
    {
        "id": "S6_Z_not_diffeomorphic_S2xS2",
        "claim": "Z_aud is not diffeomorphic to S^2 x S^2.",
        "proof": "R_hat is a surface bundle with genus-2 fiber and genus-2 "
                 "base, hence aspherical, hence minimal (an exceptional "
                 "sphere would be null-homotopic, of square 0, not -1) and "
                 "neither rational nor ruled (those have pi_2 != 0); by "
                 "Liu's theorem (E_kodaira, Theorem 2.4(2)) "
                 "kappa(R_hat, omega_hat_K) != -infinity.  Each of the four "
                 "Luttinger surgeries preserves kappa (Ho--Li), so "
                 "kappa(Z_aud, omega_hat) != -infinity.  If "
                 "psi: Z_aud -> S^2 x S^2 were a diffeomorphism, composing "
                 "with a reflection of one factor if necessary makes it "
                 "orientation-preserving from the omega_hat-orientation; "
                 "the pullback of a product form omega_{a,b} is then a "
                 "symplectic form on Z_aud compatible with that orientation, "
                 "and kappa(Z_aud, psi^* omega_{a,b}) = kappa(S^2 x S^2, "
                 "omega_{a,b}) = -infinity by the definition (S^2 x S^2 is "
                 "minimal, its intersection form being even, and K.[omega_"
                 "{a,b}] = -2a - 2b < 0 since K evaluates to -2 on each "
                 "factor sphere).  Two symplectic forms on Z_aud compatible "
                 "with one orientation have equal kappa (E_kodaira, p. 251), "
                 "contradiction.",
        "uses": ["S5_Z_symplectic", "P_audit_double", "E_asphericity",
                 "E_kodaira", "E_ho_li", "C_orientation_reversal"],
    },
    {
        "id": "S7_theorem_A_prime",
        "claim": "Theorem A': Z_aud is a closed symplectic 4-manifold "
                 "homeomorphic but not diffeomorphic to S^2 x S^2.",
        "proof": "S4, S5 and S6.",
        "uses": ["S4_Z_homeomorphic_S2xS2", "S5_Z_symplectic",
                 "S6_Z_not_diffeomorphic_S2xS2"],
    },
]

CONCLUSIONS = ["S7_theorem_A_prime"]
PILLARS = ["K_pi1_Vaud_trivial", "K_sigma_aud", "P_double_form"]

# Names that must not appear in any text field of any item on this chain.
# The comparison with those constructions is attribution, not existence.
FORBIDDEN = ["Lidman", "Piccirillo", "LP25", "2505.14387", "Wuebben",
             "2608.17267", "Source Formalization", "D1--D14", "D1-D14"]
TEXT_FIELDS = ["claim", "statement", "proof", "name", "source", "where",
               "hypotheses"]


def file_digest(relative):
    path = ROOT / relative
    assert path.is_file(), f"missing evidence: {relative}"
    return sha256(path.read_bytes()).hexdigest()


def check_chain(items):
    ids = {item["id"] for item in items}
    kinds = {item["id"]: item["kind"] for item in items}
    assert "assumption" not in kinds.values(), "no assumptions on this chain"
    graph = {item["id"]: tuple(item.get("uses", ())) for item in items}
    for name, uses in graph.items():
        for dep in uses:
            assert dep in ids, f"{name} uses unknown item {dep}"
            assert dep != name
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
    for conclusion in CONCLUSIONS:
        assert conclusion in ids

    def closure(name, acc):
        for dep in graph[name]:
            if dep not in acc:
                acc.add(dep)
                closure(dep, acc)
        return acc
    on_path = set()
    for conclusion in CONCLUSIONS:
        on_path |= closure(conclusion, set())
    # Every item other than a conclusion lies on the path of a conclusion:
    # nothing dangling, nothing decorative.
    for item in items:
        if item["id"] not in CONCLUSIONS:
            assert item["id"] in on_path, f"{item['id']} is not on the path"
    # The conclusion rests on the three intrinsic pillars.
    for pillar in PILLARS:
        assert pillar in on_path, f"conclusion misses {pillar}"
    # No item on the chain refers to another author's construction.
    for item in items:
        for field in TEXT_FIELDS:
            text = item.get(field, "")
            if isinstance(text, list):
                text = " ".join(text)
            for word in FORBIDDEN:
                assert word not in text, f"{item['id']}.{field} mentions {word!r}"
    # Every proof item is bound to a file.
    for item in items:
        if item["kind"] == "proof":
            assert item["evidence"], f"proof {item['id']} unbound"


def payload():
    computed = [fn() for fn in COMPUTED_FUNCTIONS]
    items = ([dict(e, kind="external") for e in EXTERNAL]
             + [dict(k, kind="certificate") for k in CERTIFICATES]
             + [dict(p, kind="proof") for p in PROOFS]
             + [dict(c, kind="computed") for c in computed]
             + [dict(s, kind="step") for s in STEPS])
    check_chain(items)
    evidence = {relative: file_digest(relative) for relative in EVIDENCE}
    for item in CERTIFICATES + PROOFS:
        for relative in item["evidence"]:
            assert relative in evidence, relative
    return {
        "format": "luttinger-existence-chain-v3",
        "target": "Theorem A': Z_aud = V_aud u_{sigma_aud} V_aud is a closed "
                  "symplectic 4-manifold homeomorphic but not diffeomorphic "
                  "to S^2 x S^2, from the audit theorem, the paper's own "
                  "lemmas, and named external theorems; no assumption",
        "conclusions": CONCLUSIONS,
        "pillars": PILLARS,
        "forbidden": FORBIDDEN,
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
        print(f"PASS: existence chain replays ({summary}); "
              f"{len(current['evidence_sha256'])} evidence digests match; "
              f"assumptions=0")
        return
    OUTPUT.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8")
    print(f"{OUTPUT}: {summary}; {len(current['evidence_sha256'])} "
          "evidence files bound; assumptions=0")
    for conclusion in CONCLUSIONS:
        step = next(s for s in STEPS if s["id"] == conclusion)
        print(f"  {conclusion}: {step['claim']}")


if __name__ == "__main__":
    main()
