#!/usr/bin/env python3
"""Reduce words in the 8 sheet letters with a halted kbprog system of an honest filled presentation."""
import json, os, sys, time
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reduce_in_halted.py')).read()
lines = SRC.split('\n'); cut = len(lines); seen = False
for i, ln in enumerate(lines):
    if ln.startswith('class RWS'): seen = True; continue
    if seen and ln and not ln[0].isspace() and not ln.startswith(('def ', 'class ', '#')): cut = i; break
exec('\n'.join(lines[:cut]))
LU = os.path.expanduser('~/exotic-s2xs2-verification/verification/luttinger')
case = sys.argv[1] if len(sys.argv) > 1 else 'honest_y1_p1_p1'
path = sys.argv[2] if len(sys.argv) > 2 else f'{LU}/honest_filling/kbmag/{case}.rws.kbprog'
def inv(w): return tuple(-x for x in reversed(w))
def cat(*ws):
    out = ()
    for w in ws: out += tuple(w)
    return freered(out)
def pw(w, e): return w if e == 1 else inv(w)
idx = {n: i+1 for i, n in enumerate('x y r s A B M N'.split())}
x, y, r, s, A, B, M, N = ((idx[n],) for n in 'x y r s A B M N'.split())
t0 = time.time(); eqs = load(path); R = RWS(eqs); print(f"{case}: loaded {len(R.rules)} rules in {time.time()-t0:.0f}s", flush=True)
def red(w): return len(R.reduce(to_kb(w))[0])
K = cat(inv(r), M, r); d = inv(r)
yW = cat(inv(M), y); sW = cat(inv(K), s); MW = cat(B, M, inv(B)); NW = cat(inv(M), N, M); Ax = cat(A, x)
HF = json.load(open(f'{LU}/honest_filling/honest_filling.json')); c = HF['cases'][case]
tests = {
 'control: this case alpha relator': tuple(c['alpha_relator']),
 'control: this case beta relator': tuple(c['beta_relator']),
 'control: certified Q row BxB^-1 y M^-1': cat(B, x, inv(B), y, inv(M)),
 'control: Wuebben B1 under dictionary': cat(B, x, inv(B), yW),
 'control: Wuebben M1 under dictionary': cat(A, sW, inv(A), inv(yW), inv(NW)),
 'control: Wuebben M2 under dictionary': cat(B, yW, inv(B), inv(x), inv(yW), MW),
 'control: Wuebben M3 under dictionary': cat(B, sW, inv(B), inv(sW), d, MW, inv(d)),
 '[B, M]': cat(B, M, inv(B), inv(M)),
 '[B, Ax]': cat(B, Ax, inv(B), inv(Ax)),
 'M^-1NM (A^-1NA)^-1': cat(NW, inv(A), inv(N), A),
}
for eA in (1, -1): tests[f'F1_W eA={eA}'] = cat(MW, pw(Ax, eA))
for eB in (1, -1): tests[f'F2_W eB={eB}'] = cat(NW, pw(cat(d, MW, inv(d), B), eB))
for eA in (1, -1): tests[f'F1_W with M_W:=M, eA={eA}'] = cat(M, pw(Ax, eA))
for eB in (1, -1): tests[f'F2_W with M_W:=M, N_W:=M^-1NM, eB={eB}'] = cat(NW, pw(cat(d, M, inv(d), B), eB))
for n, w in tests.items(): print(f"  {n}: residual {red(w)}", flush=True)
