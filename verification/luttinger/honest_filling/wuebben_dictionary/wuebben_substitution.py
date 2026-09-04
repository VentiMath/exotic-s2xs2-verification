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
    r = R.reduce(to_kb(w))
    return len(r)
x, y, r, s, A, B, M, N = (G[k] for k in 'x y r s A B M N'.split())
K = cat(inv(r), M, r)          # delta M delta^-1 with delta = r^-1
cands_y = {'y': y, 'My': cat(M, y), 'M^-1y': cat(inv(M), y), 'yM': cat(y, M), 'yM^-1': cat(y, inv(M))}
cands_s = {'s': s, 'Ks': cat(K, s), 'K^-1s': cat(inv(K), s), 'sK': cat(s, K), 'sK^-1': cat(s, inv(K))}
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
t0 = time.time()
# stage 1: sign-free rows
unsigned = ['R0', 'A1', 'A2', 'A3', 'B1', 'B2', 'R3']
survivors = []
for (ny, yy), (ns, ss), (nM, MM), (nN, NN) in itertools.product(cands_y.items(), cands_s.items(), cands_M.items(), cands_N.items()):
    rw = rows(x, yy, r, ss, A, B, MM, NN, 1, 1, 1, 1, 1)
    res = {k: red(rw[k]) for k in unsigned}
    ok = [k for k, v in res.items() if v == 0]
    if len(ok) >= 6:
        print(f"y={ny} s={ns} M={nM} N={nN}: reduced {ok}; residual lengths {res}", flush=True)
    if len(ok) == 7: survivors.append((ny, ns, nM, nN))
print(f"stage 1 done in {time.time()-t0:.0f}s; full survivors: {survivors}", flush=True)
for ny, ns, nM, nN in survivors:
    for e3, e4, e, eA, eB in itertools.product((1, -1), repeat=5):
        rw = rows(x, cands_y[ny], r, cands_s[ns], A, B, cands_M[nM], cands_N[nN], e3, e4, e, eA, eB)
        res = {k: red(rw[k]) for k in ('M1', 'M2', 'M3', 'F1', 'F2')}
        if all(v == 0 for v in res.values()):
            print(f"ALL ELEVEN REDUCE: y={ny} s={ns} M={nM} N={nN} signs e3={e3} e4={e4} e={e} eA={eA} eB={eB}", flush=True)
        elif sum(v == 0 for v in res.values()) >= 4:
            print(f"  partial: y={ny} s={ns} M={nM} N={nN} signs {e3,e4,e,eA,eB}: {res}", flush=True)
print("DONE", flush=True)
