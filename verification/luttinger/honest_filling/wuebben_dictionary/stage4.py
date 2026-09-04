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

yW = cat(inv(M), y); sW = cat(inv(K), s); MW = cat(B, M, inv(B)); NW = cat(inv(M), N, M)
Ax = cat(A, x)
tests = {
 '[B,M]': cat(B, M, inv(B), inv(M)),
 '[BMB^-1, Ax]': cat(MW, Ax, inv(MW), inv(Ax)),
 '[M, Ax] (certified control)': cat(M, Ax, inv(M), inv(Ax)),
 '[x, M]': cat(x, M, inv(x), inv(M)),
 '[x^-1A, M]': cat(inv(x), A, M, inv(A), x, inv(M)),
 'M^-1NM = A^-1NA ?': cat(NW, inv(A), inv(N), A),
 '[AM^-1, N]': cat(A, inv(M), N, M, inv(A), inv(N)),
 '[A^-1NA, r^-1MrB] (certified control)': cat(inv(A), N, A, K, B, inv(A), inv(N), A, inv(B), inv(K)),
 '[M^-1NM, r^-1 BMB^-1 r B] (Wuebben beta pair commutes?)': cat(NW, inv(r), MW, r, B, inv(NW), inv(B), inv(r), inv(MW), r),
 '[M^-1NM, r^-1MrB]': cat(NW, K, B, inv(NW), inv(B), inv(K)),
 'B(Ax)B^-1 (Ax)^-1': cat(B, Ax, inv(B), inv(Ax)),
 'B(Ax)B^-1 (Ax)': cat(B, Ax, inv(B), Ax),
}
for n, w in tests.items(): print(f"{n}: residual {red(w)}")
