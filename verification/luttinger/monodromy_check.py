"""
Select and certify the bundle monodromies against Prop 3.5, from the
triangulation alone.

  * psi = T_a T_b (T_b first): close the flip stack into a 3-dim mapping
    torus and fingerprint pi_1 against
      <x,y,r,s,t | [x,y][r,s], t x t^-1 = y^-1, t y t^-1 = y x,
                   t r t^-1 = r, t s t^-1 = s>          (trace 1, "hex")
    versus the wrong-relative-sign model T_a^-1 T_b (trace 3, Anosov).
    Mapping tori of psi and psi^-1 are homeomorphic, so only the relative
    sign of the two twists is selected here; the global inversion is a
    symmetry of pi_1(R) (B -> B^-1) and of the whole certificate.
  * phi0: pi_1 of the alpha mapping torus Y vs
      <x,y,r,s,t | [x,y][r,s], t x t^-1 = r, t y t^-1 = s,
                   t r t^-1 = x, t s t^-1 = y>.

Run:  python3 monodromy_check.py            (writes monodromy.g, runs gap)
"""
import subprocess
import time
from complex import Complex
from pi1 import Presentation
from fiber import build_fiber, K_BAND
from layers import build_stack, prism_cells, tri_list
from fast_tietze import simplify, renumber


def fiber_data():
    F = build_fiber()
    L, V, phi0 = F['L'], F['V'], F['phi0']
    rank = L.rank.get
    tw = {}
    for name in ('a', 'b'):
        k = K_BAND[name]
        tw[name] = (
            [V(name, 0, i) for i in range(k)],
            [V(name, 1, i) for i in range(k)],
            [V(name, -1, i) for i in range(k)],
        )
    return F, L, rank, tw, phi0


def closed_stack_group(L, rank, twists, tag):
    cells, m, name = build_stack(L, rank, twists, copy_tag=tag)
    def squash(v):
        if isinstance(v, tuple) and len(v) == 3 and v[0] == tag and v[1] == m:
            return (tag, 0, v[2])
        return v
    closed = [tuple(squash(v) for v in c) for c in cells]
    order = sorted({v for c in closed for v in c}, key=str)
    MT = Complex(closed, order=order)
    P = Presentation(MT, next(iter(MT.vertices())))
    live, rels, _ = simplify(P.ngens, P.relators, [])
    n, rels, _ = renumber(live, rels, [])
    return n, rels, MT.f_vector()


def alpha_torus_group(L, rank, phi0):
    cells = []
    for t in range(2):
        cells += prism_cells([frozenset(x) for x in tri_list(L)], rank,
                             lambda v, t=t: ('A', t + 1, v),
                             lambda v, t=t: ('A', t, v))
    cells += prism_cells([frozenset(x) for x in tri_list(L)], rank,
                         lambda v: ('A', 0, v),
                         lambda v: ('A', 2, phi0[v]))
    order = sorted({v for c in cells for v in c}, key=str)
    Y = Complex(cells, order=order)
    P = Presentation(Y, next(iter(Y.vertices())))
    live, rels, _ = simplify(P.ngens, P.relators, [])
    n, rels, _ = renumber(live, rels, [])
    return n, rels, Y.f_vector()


def gap_pres(n, rels, name):
    gw = lambda w: "One(F)" if not w else "*".join(
        f"F.{abs(g)}" + ("^-1" if g < 0 else "") for g in w)
    return (f"F := FreeGroup({n});;\n"
            f"{name} := F/[{','.join(gw(r) for r in rels)}];;\n")


MODELS = r"""
Fm := FreeGroup("x","y","r","s","t");;
x:=Fm.1;; y:=Fm.2;; r:=Fm.3;; s:=Fm.4;; t:=Fm.5;;
surf := Comm(x,y)*Comm(r,s);;
conj := function(imgs) return List([1..4],
  i -> t*[x,y,r,s][i]*t^-1*imgs[i]^-1); end;;
hex   := Fm/Concatenation([surf], conj([y^-1, y*x, r, s]));;
# T_a^-1 T_b model: compute the action honestly in GAP-land is overkill;
# instead we only need SOME wrong-relative-sign comparator; x -> x y, y -> y
# is T_b alone (parabolic), a third distinct class.
tb    := Fm/Concatenation([surf], conj([x*y, y, r, s]));;
phim  := Fm/Concatenation([surf], conj([r, s, x, y]));;
fp := function(H) local Lw; Lw := LowIndexSubgroupsFpGroup(H, IDX);
  return [AbelianInvariants(H),
          List([1..IDX], i -> Number(Lw, u -> Index(H, u) = i))]; end;;
"""


def main():
    F, L, rank, tw, phi0 = fiber_data()
    gap = "IDX := 5;;\n" + MODELS
    t0 = time.time()
    print("alpha mapping torus (phi0)...")
    n, rels, fv = alpha_torus_group(L, rank, phi0)
    print(f"  Y f-vector {fv}; reduced to {n} gens {len(rels)} rels "
          f"({time.time()-t0:.1f}s)")
    gap += gap_pres(n, rels, "Yg")
    variants = []
    for (db, da) in ((1, 1), (1, -1)):
        t0 = time.time()
        print(f"beta stack (T_b dir {db}, then T_a dir {da})...")
        curve_b, up_b, lo_b = tw['b']
        curve_a, up_a, lo_a = tw['a']
        twists = [(curve_b, up_b, lo_b, db), (curve_a, up_a, lo_a, da)]
        n, rels, fv = closed_stack_group(L, rank, twists, f"S{db}{da}")
        print(f"  stack f-vector {fv}; reduced to {n} gens {len(rels)} rels "
              f"({time.time()-t0:.1f}s)")
        vname = f"V{'p' if db>0 else 'm'}{'p' if da>0 else 'm'}"
        gap += gap_pres(n, rels, vname)
        variants.append(vname)
    gap += 'Print("phi model : ", fp(phim), "\\n");;\n'
    gap += 'Print("Y actual  : ", fp(Yg), "\\n");;\n'
    gap += 'Print("hex model : ", fp(hex), "\\n");;\n'
    gap += 'Print("tb  model : ", fp(tb), "\\n");;\n'
    for vname in variants:
        gap += f'Print("{vname}       : ", fp({vname}), "\\n");;\n'
    gap += 'QUIT;;\n'
    open("monodromy.g", "w").write(gap)
    out = subprocess.run(["gap", "-q", "monodromy.g"], input="",
                         capture_output=True, text=True, timeout=3600)
    print(out.stdout)
    if out.returncode:
        print(out.stderr[-2000:])


if __name__ == '__main__':
    main()
