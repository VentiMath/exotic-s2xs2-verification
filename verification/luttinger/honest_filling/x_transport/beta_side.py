#!/usr/bin/env python3
"""Beta side under the geometric map, reduced in the sealed complement system (0 = identity in Q).

Our complex: the alpha sweep (A0 -> A1 -> A2 -> phi_0 -> A0) meets T_beta at A1, BEFORE the phi_0 wrap, so by the
mechanism of README Part C the correction in A s A^-1 = [corr] y is the direct meridian conjugated by A.  r_run.py
indeed defines N := geom_N = A . N_grid^-1 . A^-1 with N_grid = alpha_s_grid_N the direct meridian (whisker s_2 plus
the local detour), so the certified row A s A^-1 = N y already carries the conjugation inside the letter N, and the
direct meridian is N_grid^-1 = A^-1 N A (the honest beta filling uses it).
Wuebben: T_beta = e x {beta-cut}, met before the phi_0 wrap along alpha-bar as well; his N is the direct meridian
(whisker s_2).  The alpha-torus isotopy of Part C inserts the c_s meridian into every path through c_s; s_2 passes
c_s, so the geometric image of his N is K^{-1} N_direct K with K = r^-1 M r (the c_s meridian whiskered via s_1 and
the arc of c), N_direct = N_grid^{+-1}.  Candidates below; the dictionary's M^-1 N M for comparison."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); HF = os.path.dirname(HERE); LU = os.path.dirname(HF)
SRC = open(f'{HF}/wuebben_dictionary/reduce_in_halted.py').read()
lines = SRC.split('\n'); cut = len(lines); seen = False
for i, ln in enumerate(lines):
    if ln.startswith('class RWS'): seen = True; continue
    if seen and ln and not ln[0].isspace() and not ln.startswith(('def ', 'class ', '#')): cut = i; break
exec('\n'.join(lines[:cut]))
R = RWS(load(f'{LU}/alpha_residual/complement_input.rws.kbprog'))
G = {k: tuple(v) for k, v in json.load(open(f'{HF}/honest_filling.json'))['sheet_generator_words_in_Q'].items()}
S = json.load(open(f'{LU}/sealed_transport/r_presentations.json'))['tracked_words']
x, y, r, s, A, B, M, N = (G[k] for k in 'x y r s A B M N'.split())
def inv(w): return tuple(-g for g in reversed(w))
def cat(*ws):
    o = ()
    for w in ws: o += tuple(w)
    return freered(o)
def pw(w, e): return w if e == 1 else inv(w)
def comm(a, b): return cat(a, b, inv(a), inv(b))
def red(w):
    o, st, ok = R.reduce(to_kb(w)); assert ok; return len(o)
Ngrid = tuple(S['alpha_s_grid_N'])
K = cat(inv(r), M, r); yW = cat(inv(M), y); sW = cat(inv(K), s)
Ndir = cat(inv(A), N, A)                     # = N_grid^-1 (free-word identity in honest_filling.json)
out = {}
def rep(name, w):
    n = red(w); out[name] = n; print(f'{"IDENTITY" if n == 0 else f"residual {n:3d}"}   {name}')
print('== provenance of N')
rep('geom_N = A N_grid^-1 A^-1 (free-word identity, as words in Q)', cat(N, inv(cat(A, inv(Ngrid), inv(A)))))
rep('certified row A s A^-1 = N y', cat(A, s, inv(A), inv(y), inv(N)))
rep('A M A^-1 = K = r^-1 M r  (c_y meridian transported around alpha is the c_s meridian)', cat(A, M, inv(A), inv(K)))
rep('A M A^-1 = K^-1', cat(A, M, inv(A), K))
rep('[K, N_dir]  (c_s meridian vs e meridian, both s-whiskered)', comm(K, Ndir))
rep('[M, N_dir]', comm(M, Ndir))
cands = {'N_dir = A^-1 N A (direct, honest orientation)': Ndir, 'N_dir^-1': inv(Ndir),
         'K^-1 N_dir K (geometric image of his N)': cat(inv(K), Ndir, K), 'K^-1 N_dir^-1 K': cat(inv(K), inv(Ndir), K),
         'K N_dir K^-1': cat(K, Ndir, inv(K)), 'K N_dir^-1 K^-1': cat(K, inv(Ndir), inv(K)),
         'M^-1 N M (algebraic dictionary)': cat(inv(M), N, M), 'N (as printed)': N}
print('== his row M1: A s_W A^-1 = N_W^e3 y_W, with s_W = K^-1 s, y_W = M^-1 y')
for cn, NW in cands.items():
    for e3 in (1, -1):
        his = cat(A, sW, inv(A), inv(yW), pw(NW, -e3))
        mech = cat(A, sW, inv(A), inv(yW), inv(pw(cat(A, NW, inv(A)), e3)))
        rep(f'M1 printed   N_W={cn}, e3={e3:+d}', his)
        rep(f'M1 mechanism (A N_W A^-1)^e3   N_W={cn}, e3={e3:+d}', mech)
        rep(f'M1 printed . [A, N_W^e3]^-1   N_W={cn}, e3={e3:+d}', cat(his, inv(comm(A, pw(NW, e3)))))
print('== his filling F2 = N_W ((r^-1 M_W^{-e} r) B)^eB with e = -1 (his M3 sign matching our B s B^-1 row)')
Fh = {eb: cat(Ndir, pw(cat(inv(r), M, r, B), eb)) for eb in (1, -1)}          # honest beta filling A^-1 N A (r^-1 M r B)^eb
for cn, NW in list(cands.items())[:6]:
    for eb in (1, -1):
        F2 = cat(NW, pw(cat(inv(r), M, r, B), eb))
        rep(f'F2_W(geo) . F2_honest^-1   N_W={cn}, eB={eb:+d}', cat(F2, inv(Fh[eb])))
MWd = cat(B, M, inv(B)); NWd = cat(inv(M), N, M)
for eb in (1, -1):
    F2d = cat(NWd, pw(cat(inv(r), MWd, r, B), eb))
    rep(f'F2_W(dict) . F2_honest^-1   eB={eb:+d}', cat(F2d, inv(Fh[eb])))
    rep(f'F2_W(dict) . (sealed N (r^-1 M r B)^eB)^-1   eB={eb:+d}', cat(F2d, inv(cat(N, pw(cat(inv(r), M, r, B), eb)))))
json.dump(out, open(f'{HERE}/beta_side.json', 'w'), indent=1)

print('== named quotients (free-group identities noted; reductions in Q)')
lam = cat(inv(r), M, r, B)
NWg = cat(inv(K), Ndir, K)
# F2_W(geo) . F2_honest^-1 is the free word K^-1 N_dir K N_dir^-1 = [K^-1, N_dir]
assert cat(NWg, lam, inv(cat(Ndir, lam))) == comm(inv(K), Ndir)
rep('[K^-1, N_dir]  (= F2_W(geo) . F2_honest^-1 as free words)', comm(inv(K), Ndir))
# his printed lambda_W (r^-1 M r B, letters fixed) versus the s_2-whiskered push-off carried by the isotopy, K^-1 lam K:
# (K^-1 lam K) lam^-1 = K^-1 (r^-1 M r) B K B^-1 (r^-1 M r)^-1 = B K B^-1 K^-1 = [B, K] as free words
assert cat(inv(K), lam, K, inv(lam)) == comm(B, K)
rep('[B, K] = [B, A M A^-1]  (= (K^-1 lam K) lam^-1 as free words)', comm(B, K))
rep('[A, K]', comm(A, K))
rep('[K, lam]', comm(K, lam))
rep('[B, M]', comm(B, M))
json.dump(out, open(f'{HERE}/beta_side.json', 'w'), indent=1)
