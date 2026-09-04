#!/usr/bin/env python3
import json, os, sys, time, itertools
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reduce_in_halted.py')).read()
lines = SRC.split('\n'); cut = len(lines); seen = False
for i, ln in enumerate(lines):
    if ln.startswith('class RWS'): seen = True; continue
    if seen and ln and not ln[0].isspace() and not ln.startswith(('def ', 'class ', '#')): cut = i; break
exec('\n'.join(lines[:cut]))
LU = os.path.expanduser('~/exotic-s2xs2-verification/verification/luttinger')
case = sys.argv[1] if len(sys.argv) > 1 else 'honest_y1_p1_p1'
RP = json.load(open(f'{LU}/honest_filling/reduced_presentations.json'))[case]
old2new = [tuple(w) for w in RP['old_generators_in_new']]   # sheet gen i -> word in new gens
def inv(w): return tuple(-x for x in reversed(w))
def cat(*ws):
    out = ()
    for w in ws: out += tuple(w)
    return freered(out)
def pw(w, e): return w if e == 1 else inv(w)
def sheet(*syms):
    """sheet-letter word from symbols like 'x','y^-1' -> tuple of ±i over x,y,r,s,A,B,M,N"""
    idx = {n: i+1 for i, n in enumerate('x y r s A B M N'.split())}
    out = []
    for t in syms:
        if t.endswith('^-1'): out.append(-idx[t[:-3]])
        else: out.append(idx[t])
    return tuple(out)
def translate(w):  # sheet word -> new-generator word
    out = ()
    for g in w:
        out = out + (old2new[g-1] if g > 0 else inv(old2new[-g-1]))
    return freered(out)
t0 = time.time()
eqs = load(f'{LU}/honest_filling/kbmag/{case.replace("honest_","reduced_honest_")}.rws.kbprog')
R = RWS(eqs); print(f"loaded {len(R.rules)} rules in {time.time()-t0:.0f}s", flush=True)
def red(w):
    return len(R.reduce(to_kb(translate(w)))[0])
x, y, r, s, A, B, M, N = (sheet(n) for n in 'x y r s A B M N'.split())
K = cat(inv(r), M, r)
yW = cat(inv(M), y); sW = cat(inv(K), s); MW = cat(B, M, inv(B)); NW = cat(inv(M), N, M)
d = inv(r)
# controls: audit honest fillings for this case (from honest_filling.json cases)
HF = json.load(open(f'{LU}/honest_filling/honest_filling.json'))
c = HF['cases'][case] if isinstance(HF['cases'], dict) else [cc for cc in HF['cases'] if cc.get('name') == case][0]
print("case record keys:", list(c) if isinstance(c, dict) else c, flush=True)
for k, v in (c.items() if isinstance(c, dict) else []):
    if 'sheet' in k and isinstance(v, (list, dict)):
        print(k, json.dumps(v)[:300], flush=True)
tests = {
  'control: audit sheet row B x B^-1 y M^-1': cat(B, x, inv(B), y, inv(M)),
  'control: Wuebben B1 under dictionary (B x B^-1 y_W)': cat(B, x, inv(B), yW),
  'control: Wuebben M2 under dictionary': cat(B, yW, inv(B), inv(x), inv(yW), pw(MW, 1)),
  'control: Wuebben M1 under dictionary': cat(A, sW, inv(A), inv(yW), pw(NW, -1)),
  'sealed beta-relator style [A, N]': cat(A, N, inv(A), inv(N)),
}
for eA in (1, -1):
    tests[f'F1_W eA={eA}: BMB^-1 (Ax)^{eA}'] = cat(MW, pw(cat(A, x), eA))
for eB in (1, -1):
    tests[f'F2_W eB={eB}: M^-1NM (r^-1 BMB^-1 r B)^{eB}'] = cat(NW, pw(cat(d, MW, inv(d), B), eB))
# also the audit-form fillings with every sign, as sanity: M (Ax)^e and A^-1 N A (r^-1 M r B)^e
for e in (1, -1):
    tests[f'audit F1 form M(Ax)^{e}'] = cat(M, pw(cat(A, x), e))
    tests[f'audit F2 form A^-1NA (r^-1MrB)^{e}'] = cat(inv(A), N, A, pw(cat(d, M, inv(d), B), e))
for name, w in tests.items():
    t1 = time.time(); L = red(w)
    print(f"{name}: residual length {L}  ({time.time()-t1:.1f}s)", flush=True)
