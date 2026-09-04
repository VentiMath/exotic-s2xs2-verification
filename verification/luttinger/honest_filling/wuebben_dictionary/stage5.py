#!/usr/bin/env python3
"""Do Wuebben's Table 1 relations hold in the audit complement group Q after a
meridian re-basing of the sheet loops?  A reduction to the empty word in the halted
complement system is a proof; a nonzero residual is inconclusive."""
import json, re, itertools, sys, os, time
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reduce_in_halted.py')).read()
# keep only the helper definitions (everything before the first top-level statement after class RWS)
lines = SRC.split('\n'); cut = len(lines); seen_class = False
for i, ln in enumerate(lines):
    if ln.startswith('class RWS'): seen_class = True; continue
    if seen_class and ln and not ln[0].isspace() and not ln.startswith(('def ', 'class ', '#')):
        cut = i; break
exec('\n'.join(lines[:cut]))
LU = os.path.expanduser('~/exotic-s2xs2-verification/verification/luttinger')
eqs = load(f'{LU}/alpha_residual/complement_input.rws.kbprog')
R = RWS(eqs)
H = json.load(open(f'{LU}/honest_filling/honest_filling.json'))
G = {k: tuple(v) for k, v in H['sheet_generator_words_in_Q'].items()}
def inv(w): return tuple(-x for x in reversed(w))
def cat(*ws):
    out = ()
    for w in ws: out = out + tuple(w)
    return freered(out)
def pw(w, e): return w if e == 1 else inv(w)
def red(w):
    r = R.reduce(to_kb(w))[0]
    return len(r)
x, y, r, s, A, B, M, N = (G[k] for k in 'x y r s A B M N'.split())
K = cat(inv(r), M, r)          # delta M delta^-1 with delta = r^-1
cands_y = {f'M^{a}yM^{b}': cat(pw(M,a) if a else (), y, pw(M,b) if b else ()) for a in (-1,0,1) for b in (-1,0,1)}
cands_s = {f'K^{a}sK^{b}': cat(pw(K,a) if a else (), s, pw(K,b) if b else ()) for a in (-1,0,1) for b in (-1,0,1)}
cands_M = {'M': M, 'y^-1My': cat(inv(y), M, y), 'yMy^-1': cat(y, M, inv(y))}
cands_N = {'N': N, 'A^-1NA': cat(inv(A), N, A), 'ANA^-1': cat(A, N, inv(A))}
def rows(xx, yy, rr, ss, AA, BB, MM, NN, e3, e4, e, eA, eB):
    d = inv(rr)
    return {
     'R0': cat(xx, yy, inv(xx), inv(yy), rr, ss, inv(rr), inv(ss)),
     'A1': cat(AA, xx, inv(AA), inv(rr)), 'A2': cat(AA, yy, inv(AA), inv(ss)), 'A3': cat(AA, rr, inv(AA), inv(xx)),
     'B1': cat(BB, xx, inv(BB), yy), 'B2': cat(BB, rr, inv(BB), inv(rr)),
     'R3': cat(BB, inv(ss), inv(rr), yy, xx, inv(BB), inv(xx), ss, rr),
     'M1': cat(AA, ss, inv(AA), inv(yy), pw(NN, -e3)),
     'M2': cat(BB, yy, inv(BB), inv(xx), inv(yy), pw(MM, -e4)),
     'M3': cat(BB, ss, inv(BB), inv(ss), d, pw(MM, -e), inv(d)),
     'F1': cat(MM, pw(cat(AA, xx), eA)),
     'F2': cat(NN, pw(cat(d, pw(MM, -e), inv(d), BB), eB)),
    }

yW = cat(inv(M), y); sW = cat(inv(K), s); MW = cat(B, M, inv(B))
target = cat(A, sW, inv(A), inv(yW))   # = N_W^{e3}
NA = cat(inv(A), N, A)
cands = {'M^-1NM': cat(inv(M), N, M), 'A^-1NA': NA, 'K^-1NK': cat(inv(K), N, K), 'KNK^-1': cat(K, N, inv(K)),
 'K^-1(A^-1NA)K': cat(inv(K), NA, K), 'K(A^-1NA)K^-1': cat(K, NA, inv(K)), 'M^-1(A^-1NA)M': cat(inv(M), NA, M), 'M(A^-1NA)M^-1': cat(M, NA, inv(M)),
 'A^-1K^-1NKA': cat(inv(A), inv(K), N, K, A), 'A^-1KNK^-1A': cat(inv(A), K, N, inv(K), A), 'A^-1M^-1NMA': cat(inv(A), inv(M), N, M, A), 'A^-1MNM^-1A': cat(inv(A), M, N, inv(M), A)}
for n, NW in cands.items():
    for e3 in (1, -1):
        print(f"M1 with N_W={n}, e3={e3}: residual {red(cat(target, pw(NW, -e3)))}")
print("equalities in Q:")
print(" M^-1NM vs K^-1(A^-1NA)K:", red(cat(cat(inv(M), N, M), inv(cat(inv(K), NA, K)))))
print(" M^-1NM vs A^-1K^-1NKA:", red(cat(cat(inv(M), N, M), inv(cat(inv(A), inv(K), N, K, A)))))
