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

yW = cat(inv(M), y); sW = cat(inv(K), s)
cands_M = {'M': M, 'BMB^-1': cat(B, M, inv(B)), 'B^-1MB': cat(inv(B), M, B), 'y^-1My': cat(inv(y), M, y), 'yMy^-1': cat(y, M, inv(y)),
           'AMA^-1': cat(A, M, inv(A)), 'A^-1MA': cat(inv(A), M, A), 'xMx^-1': cat(x, M, inv(x)), 'x^-1Mx': cat(inv(x), M, x)}
cands_N = {'N': N, 'A^-1NA': cat(inv(A), N, A), 'ANA^-1': cat(A, N, inv(A)), 'BNB^-1': cat(B, N, inv(B)), 'B^-1NB': cat(inv(B), N, B), 's^-1Ns': cat(inv(s), N, s), 'sNs^-1': cat(s, N, inv(s))}
d = inv(r)
for nM, MM in cands_M.items():
    for e4 in (1, -1):
        w = cat(B, yW, inv(B), inv(x), inv(yW), pw(MM, -e4)); print(f"M2 M={nM} e4={e4}: residual {red(w)}")
    for e in (1, -1):
        w = cat(B, sW, inv(B), inv(sW), d, pw(MM, -e), inv(d)); print(f"M3 M={nM} e={e}: residual {red(w)}")
    for eA in (1, -1):
        w = cat(MM, pw(cat(A, x), eA)); print(f"F1 M={nM} eA={eA}: residual {red(w)}")
for nN, NN in cands_N.items():
    for e3 in (1, -1):
        w = cat(A, sW, inv(A), inv(yW), pw(NN, -e3)); print(f"M1 N={nN} e3={e3}: residual {red(w)}")
    for nM, MM in list(cands_M.items())[:3]:
        for e in (1, -1):
            for eB in (1, -1):
                w = cat(NN, pw(cat(d, pw(MM, -e), inv(d), B), eB)); print(f"F2 N={nN} M={nM} e={e} eB={eB}: residual {red(w)}")
