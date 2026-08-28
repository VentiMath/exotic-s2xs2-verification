"""
Calibration 2 (Baldridge-Kirk, the paper's own Appendix B.1 test):
T^4 = T^2_{xy} x T^2_{ab};  T1 = x-circle x a-circle at (y0,b0),
T2 = y-circle x a-circle at (x0,b1), b1 != b0.  Double +-1 Luttinger surgery
on T1 along x and T2 along y.  Expected: (Z^2 x|_A Z) x Z, |tr A| in {1,3}
depending on the relative sign.  The fingerprints below must land on those.
"""
from complex import grid_torus, product
from complement import TorusComplement
from tietze import simplify, renumber
import subprocess
import time

n = 4
S, B = grid_torus(n), grid_torus(n)
K = product(S, B)
print("K f-vector:", K.f_vector())
xrow = [(i, 0) for i in range(n)]          # x-circle at y=0
ycol = [(0, j) for j in range(n)]          # y-circle at x=0
arow0 = [(k, 0) for k in range(n)]         # a-circle at b=0
arow2 = [(k, 2) for k in range(n)]         # a-circle at b=2
T1v = [(f, b) for f in xrow for b in arow0]
T2v = [(f, b) for f in ycol for b in arow2]
T = K.induced(T1v + T2v)
print("T full:", K.is_full(T), " components:", 2)
X = TorusComplement(K, T)
print("C f-vector:", X.C.f_vector())

def torus_data(alpha, beta, a_side, b_side, base_simplex=None):
    a0, b0 = alpha[0], beta[0]
    u0 = frozenset({(a0, b0), (a0, b_side)})
    u1 = frozenset({(a0, b0), (a_side, b0)})
    if base_simplex is None:
        X.presentation(u0)
    sigma = next(s for s in T.simplices[2] if (a0, b0) in s)
    mu_loop = X.meridian_loop(sigma)
    star = [s for s in X.N if (a0, b0) in s]
    to_mu = X.bfs_in_N(u0, mu_loop[0], star)
    lf_loop = X.pushoff_loop([(a, b0) for a in alpha] + [(a0, b0)], lambda v: (v[0], b_side))
    lb_loop = X.pushoff_loop([(a0, b) for b in beta] + [(a0, b0)], lambda v: (a_side, v[1]))
    sq = {(a0, b0), (a_side, b0), (a0, b_side), (a_side, b_side)}
    to_u1 = X.bfs_in_N(u0, u1, [s for s in X.N if s <= sq])
    # words: loops based at u0 (in Ndot); based_word requires the global base
    # simplex at the start of the basing path, so prepend the tree-free route:
    def bw(loop, path):
        full = path + loop[1:] + path[::-1][1:]
        return X.P.loop_word(X.to_C(full))
    return bw(mu_loop, to_mu), bw(lf_loop, [u0]), bw(lb_loop, to_u1)

t = time.time()
mu1, lf1, lb1 = torus_data(xrow, arow0, a_side=(0, 1), b_side=(0, 1))
mu2, lf2, lb2 = torus_data(ycol, arow2, a_side=(1, 0), b_side=(0, 1), base_simplex=X.base_simplex)
P = X.P
print("pi_1(C):", P.ngens, "gens", len(P.relators), "rels", f"({time.time()-t:.1f}s)")
live, rels, ws = simplify(P.ngens, P.relators, [mu1, lf1, lb1, mu2, lf2, lb2])
m, rels, (mu1, lf1, lb1, mu2, lf2, lb2) = renumber(live, rels, ws)
print("reduced:", m, "gens", len(rels), "rels")
print("T1: mu =", mu1, "lf =", lf1, "lb =", lb1)
print("T2: mu =", mu2, "lf =", lf2, "lb =", lb2)
gw = lambda w: "One(F)" if not w else "*".join(f"F.{abs(g)}"+("^-1" if g<0 else "") for g in w)
gap = f"F := FreeGroup({m});;\nrels := [{','.join(gw(r) for r in rels)}];;\nG := F/rels;;\n"
for nm, w in [("mu1",mu1),("lf1",lf1),("lb1",lb1),("mu2",mu2),("lf2",lf2),("lb2",lb2)]:
    gap += f"{nm} := {gw(w)};;\n"
gap += r"""
fp := function(H) local L; L := LowIndexSubgroupsFpGroup(H, 6);
  return [AbelianInvariants(H), List([1..6], i -> Number(L, s -> Index(H, s) = i))]; end;;
Print("pi1(C): ", fp(G), "\n");
Print("pi1(C)/<<mu1,mu2>>: ", fp(F/Concatenation(rels,[mu1,mu2])), " (should be Z^4)\n");
for e1 in [1,-1] do for e2 in [1,-1] do
  Print("double surgery (", e1, ",", e2, "): ", fp(F/Concatenation(rels,[mu1*lf1^e1, mu2*lf2^e2])), "\n");
od; od;
Fm := FreeGroup("u","v","t","z");; u:=Fm.1;; v:=Fm.2;; t:=Fm.3;; z:=Fm.4;;
model := function(A) return Fm/[Comm(u,v), Comm(u,z),Comm(v,z),Comm(t,z),
  t*u*t^-1*(u^A[1][1]*v^A[2][1])^-1, t*v*t^-1*(u^A[1][2]*v^A[2][2])^-1]; end;;
for A in [[[0,1],[-1,1]], [[0,-1],[1,-1]], [[0,1],[-1,3]], [[0,-1],[1,-3]]] do
  Print("(Z^2 x|_A Z) x Z, tr A = ", A[1][1]+A[2][2], ": ", fp(model(A)), "\n");
od;
"""
open("bk.g", "w").write(gap)
out = subprocess.run(["gap", "-q", "bk.g"], input="", capture_output=True, text=True, timeout=1500)
print(out.stdout[-3000:], out.stderr[-500:])
