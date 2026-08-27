"""
Calibration 1:  T^4 = T^2 x T^2,  T = (row cycle) x (column cycle).
Expected:  pi_1(T^4 - T) = Z^2 x F_2,  pi_1(C)/<<mu>> = Z^4,
and 1/1 Luttinger surgery along the fiber direction gives the standard
presentation  < x,y,a,b | [x,y],[a,b],[x,a],[y,a],[x,b], [y,b] = x^{+-1} >.
"""
from complex import grid_torus, product, Complex
from complement import TorusComplement
from pi1 import inverse
import subprocess, sys

n = 3
S = grid_torus(n)       # "fiber"  (vertices (i,j))
B = grid_torus(n)       # "base"
K = product(S, B)
print("K f-vector:", K.f_vector())

alpha = [(i, 0) for i in range(n)]          # row cycle in S
beta = [(0, j) for j in range(n)]           # column cycle in B
Tverts = [(a, b) for a in alpha for b in beta]
T = K.induced(Tverts)
print("T f-vector:", T.f_vector(), " full:", K.is_full(T))

X = TorusComplement(K, T)
print("C f-vector:", X.C.f_vector(), " |Ndot| =", len(X.N))

a0, b0 = alpha[0], beta[0]
a_side = (0, 1)   # neighbour of a0 in S, not on alpha
b_side = (1, 0)   # neighbour of b0 in B, not on beta
u0 = frozenset({(a0, b0), (a0, b_side)})          # basepoint in Ndot
u1 = frozenset({(a0, b0), (a_side, b0)})
P = X.presentation(u0)
print("pi_1(C): generators", P.ngens, "relators", len(P.relators))

# meridian: dual cell boundary of a 2-simplex of T containing (a0,b0)
sigma = next(s for s in T.simplices[2] if (a0, b0) in s)
mu_loop = X.meridian_loop(sigma)
star = [s for s in X.N if (a0, b0) in s]
to_mu = X.bfs_in_N(u0, mu_loop[0], star)
mu = X.based_word(mu_loop, to_mu)

# fiber-direction longitude: alpha x {b0}, pushed to the b_side
lam_f_loop = X.pushoff_loop([(a, b0) for a in alpha] + [(a0, b0)], lambda v: (v[0], b_side))
lam_f = X.based_word(lam_f_loop, [u0])

# base-direction longitude: {a0} x beta, pushed to the a_side
lam_b_loop = X.pushoff_loop([(a0, b) for b in beta] + [(a0, b0)], lambda v: (a_side, v[1]))
to_u1 = X.bfs_in_N(u0, u1, [s for s in X.N if s <= {(a0, b0), (a_side, b0), (a0, b_side), (a_side, b_side)}])
lam_b = X.based_word(lam_b_loop, to_u1)

print("mu    =", mu)
print("lam_f =", lam_f)
print("lam_b =", lam_b)

gap = P.gap_setup("G") + f"""
mu := {P.gap_word(mu)};;  lf := {P.gap_word(lam_f)};;  lb := {P.gap_word(lam_b)};;
fp := function(H) local L; L := LowIndexSubgroupsFpGroup(H, 4);
  return [AbelianInvariants(H), List([1..4], i -> Number(L, s -> Index(H, s) = i))]; end;;
Print("pi1(C) simplified gens: ", Length(GeneratorsOfGroup(SimplifiedFpGroup(G))), "\\n");
Print("pi1(C): ", fp(G), "\\n");
Z2F2 := FreeGroup(4);; Z2F2 := Z2F2/[Comm(Z2F2.1,Z2F2.2), Comm(Z2F2.1,Z2F2.3), Comm(Z2F2.1,Z2F2.4), Comm(Z2F2.2,Z2F2.3), Comm(Z2F2.2,Z2F2.4)];;
Print("Z^2xF_2: ", fp(Z2F2), "\\n");
Print("pi1(C)/<<mu>>: ", fp(F/Concatenation(rels,[mu])), "\\n");
Z4 := FreeGroup(4);; Z4 := Z4/List(Combinations([1..4],2), p -> Comm(Z4.(p[1]), Z4.(p[2])));;
Print("Z^4: ", fp(Z4), "\\n");
Print("mu in [C,C]? ", mu in DerivedSubgroup(G), "  lf,lb commute with mu? ", IsOne(Comm(G.1^0*mu, lf)), " ", IsOne(Comm(mu, lb)), "\\n");
for e in [1,-1] do
  Print("surgery mu*lf^", e, ": ", fp(F/Concatenation(rels,[mu*lf^e])), "\\n");
  Print("surgery mu*lb^", e, ": ", fp(F/Concatenation(rels,[mu*lb^e])), "\\n");
od;
E := FreeGroup("x","y","a","b");; x:=E.1;;y:=E.2;;a:=E.3;;b:=E.4;;
for e in [1,-1] do
  Print("expected (dir x, k=",e,"): ", fp(E/[Comm(x,y),Comm(a,b),Comm(x,a),Comm(y,a),Comm(x,b),Comm(y,b)*x^e]), "\\n");
  Print("expected (dir a, k=",e,"): ", fp(E/[Comm(x,y),Comm(a,b),Comm(x,a),Comm(y,a),Comm(x,b),Comm(y,b)*a^e]), "\\n");
od;
"""
open("t4.g", "w").write(gap)
out = subprocess.run(["gap", "-q", "t4.g"], input="", capture_output=True, text=True, timeout=600)
print(out.stdout[-3000:], out.stderr[-500:])
