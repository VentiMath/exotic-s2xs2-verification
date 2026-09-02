#!/usr/bin/env python3
"""Machine control for the intrinsic boundary involution sigma_aud (issue #807).

sigma_aud(z, t) = (phi_0(z), -t) on the boundary mapping torus M_h of R_aud, where
h is the commutator of the two clutching maps.  This script checks, on the based
monodromy actions certified elsewhere in this repository, the three algebraic facts
the lemma rests on:

  1. Phi := (phi_0)_* is an involution of pi_1(F, p) -- exactly, as a free-group
     automorphism on the based generators, not merely up to inner automorphism;
  2. Psi := (psi_0)_* has an exact inverse (so every commutator below is defined);
  3. for EVERY ordering and orientation of the commutator h in {Phi, Psi},
        Phi o h o Phi^-1 = h^-1   exactly on the free basis,
     which is what makes (z,t) -> (phi_0(z), -t) respect the seam (z,1) ~ (h(z),0).

Fact 3 is a two-line group identity given fact 1; the point of running it is that the
actions used are the repository's, so the lemma is anchored to certified data rather
than to a symbol.  The same is then reported on H_1(F) = Z^4 as 4x4 matrices.

The monodromy actions are the transport relations of the displayed sheet with the
meridians deleted (they are meridians of tori that do not exist in R):
    A g A^-1 = Phi(g):  x -> r, y -> s, r -> x, s -> y
    B g B^-1 = Psi(g):  x -> y^-1, y -> y x, r -> r, s -> s
Phi(x)=r, Phi(y)=s are certified as literal based paths by paper_bridge.py; the sheet
is Run 70/71's.  Standard library only.
"""
from itertools import product

# ---------------------------------------------------------------- free group, stdlib
GENS = ("x", "y", "r", "s")

def reduce(letters):
    out = []
    for g, e in letters:
        if out and out[-1][0] == g and out[-1][1] == -e: out.pop()
        else: out.append((g, e))
    return tuple(out)

class W:
    __slots__ = ("w",)
    def __init__(self, w=()): self.w = reduce(w)
    def __mul__(self, o): return W(self.w + o.w)
    def inv(self): return W(tuple((g, -e) for g, e in reversed(self.w)))
    def __eq__(self, o): return self.w == o.w
    def __hash__(self): return hash(self.w)
    def __repr__(self): return "1" if not self.w else "".join(g + ("" if e == 1 else "^-1") for g, e in self.w)

x, y, r, s = (W(((g, 1),)) for g in GENS)
ONE = W()

class Aut:
    """Endomorphism of the free group on GENS, given by images of the generators."""
    def __init__(self, images, name):
        self.img = dict(images); self.name = name
    def __call__(self, w):
        out = W()
        for g, e in w.w:
            out = out * (self.img[g] if e == 1 else self.img[g].inv())
        return out
    def __mul__(self, o):                       # (self * o)(w) = self(o(w))  -- apply o first
        return Aut({g: self(o.img[g]) for g in GENS}, f"({self.name}∘{o.name})")
    def __eq__(self, o): return all(self.img[g] == o.img[g] for g in GENS)
    def matrix(self):
        return [[sum(e for gg, e in self.img[g].w if gg == h) for g in GENS] for h in GENS]

ID  = Aut({"x": x, "y": y, "r": r, "s": s}, "id")
Phi = Aut({"x": r, "y": s, "r": x, "s": y}, "Φ")
Psi = Aut({"x": y.inv(), "y": y * x, "r": r, "s": s}, "Ψ")
PsiInv = Aut({"x": x * y, "y": x.inv(), "r": r, "s": s}, "Ψ⁻¹")   # verified below
surface = x * y * x.inv() * y.inv() * r * s * r.inv() * s.inv()

def show(m): return "[" + "; ".join(" ".join(f"{v:2d}" for v in row) for row in m) + "]"

def main():
    ok = True
    def check(cond, msg):
        nonlocal ok
        print(("  OK   " if cond else "  FAIL ") + msg)
        ok = ok and cond

    print("1. Phi is an exact involution on the free basis")
    check(Phi * Phi == ID, "Φ∘Φ = id on (x,y,r,s)")
    check(Phi(surface) == r * s * r.inv() * s.inv() * x * y * x.inv() * y.inv(),
          "Φ([x,y][r,s]) = [r,s][x,y]  (= [x,y]^-1 · [x,y][r,s] · [x,y], conjugate: surface relator preserved)")

    print("2. Psi has the stated exact inverse; both preserve the surface relator")
    check(Psi * PsiInv == ID and PsiInv * Psi == ID, "Ψ∘Ψ⁻¹ = Ψ⁻¹∘Ψ = id")
    check(Psi(surface) == surface, "Ψ([x,y][r,s]) = [x,y][r,s] exactly")

    print("3. Phi conjugates every commutator of Phi and Psi to its inverse (exactly on the free basis)")
    PhiInv = Phi
    conventions = {
        "[Φ,Ψ] = Φ Ψ Φ⁻¹ Ψ⁻¹": (Phi * Psi * PhiInv * PsiInv, Psi * Phi * PsiInv * PhiInv),
        "[Ψ,Φ] = Ψ Φ Ψ⁻¹ Φ⁻¹": (Psi * Phi * PsiInv * PhiInv, Phi * Psi * PhiInv * PsiInv),
        "Φ⁻¹ Ψ⁻¹ Φ Ψ":         (PhiInv * PsiInv * Phi * Psi, PsiInv * PhiInv * Psi * Phi),
        "Ψ⁻¹ Φ⁻¹ Ψ Φ":         (PsiInv * PhiInv * Psi * Phi, PhiInv * PsiInv * Phi * Psi),
    }
    for label, (h, hinv) in conventions.items():
        check(h * hinv == ID, f"h = {label}: h∘h⁻¹ = id")
        conj = Phi * h * PhiInv
        check(conj == hinv, f"h = {label}: Φ∘h∘Φ⁻¹ = h⁻¹ on every generator")
        print("         h  :", {g: repr(h.img[g]) for g in GENS})
        print("         h⁻¹:", {g: repr(hinv.img[g]) for g in GENS})

    print("4. the same on H_1(F) = Z^4 (columns = images of x,y,r,s)")
    h = conventions["[Φ,Ψ] = Φ Ψ Φ⁻¹ Ψ⁻¹"][0]
    hinv = conventions["[Φ,Ψ] = Φ Ψ Φ⁻¹ Ψ⁻¹"][1]
    print("   Φ  =", show(Phi.matrix()))
    print("   Ψ  =", show(Psi.matrix()))
    print("   h  =", show(h.matrix()))
    print("   h⁻¹=", show(hinv.matrix()))
    print("   ΦhΦ=", show((Phi * h * Phi).matrix()))
    check((Phi * h * Phi).matrix() == hinv.matrix(), "Φ h Φ⁻¹ = h⁻¹ on H_1(F)")

    print("5. fixed points of sigma_aud[z,t] = [phi_0(z), 1-t] on M_h = F x [0,1] / (z,1)~(h z,0)")
    print("   base points fixed by the reflection: t = 1/2 and the seam t = 0.")
    print("   over t = 1/2: Fix(phi_0) = {p, O} (fiber.py asserts Fix(phi0) == {p, O});")
    print("   over the seam: Fix(h phi_0), an involution since (h phi_0)^2 = h (phi_0 h phi_0) = id;")
    print("   it contains p and O because phi_0 and psi_0 both fix them, hence so does h.")
    print("   So sigma_aud has at least four fixed points and is NOT free.")
    print("   Theorem A (existence) never uses freeness; only the quotient W = V/sigma (Theorem B) does.")
    for name, k in (("h phi_0", conventions["[Φ,Ψ] = Φ Ψ Φ⁻¹ Ψ⁻¹"][0] * Phi),):
        check(k * k == ID, f"({name})^2 = id on the free basis (so it is an involution)")

    print("6. derivative of sigma_aud at the section boundary")
    print("   phi_0 acts on the 24-cycle link of p by shift 12 (pl_self_intersection.py), i.e. by -I;")
    print("   that is constant clutch shift 2 of the four cases certified there, each with")
    print("   Gamma_hat . Gamma_hat = 0.  So the doubled-section certificate already covers sigma_aud.")

    print("\nRESULT:", "PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)

if __name__ == "__main__":
    main()
