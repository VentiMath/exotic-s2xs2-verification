#!/usr/bin/env python3
"""Part C: Wuebben's alpha-side rows (B1, M2, M3) and his alpha filling F1 under the two candidate
identifications of his letters with ours, reduced in the sealed complement system.
  algebraic dictionary (wuebben_dictionary/):  y -> M^-1 y, s -> r^-1 M^-1 r s, M -> B M B^-1, x, r, A, B fixed
  geometric map (isotopy of T_alpha across the fiber over q; Part C of README):  same on y, s, x, r, A, B, but M -> M
0 = identity in Q; 'same nf as' = equal in Q by common normal form (a proof even without confluence)."""
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
x, y, r, s, A, B, M, N = (G[k] for k in 'x y r s A B M N'.split())
def inv(w): return tuple(-g for g in reversed(w))
def cat(*ws):
    o = ()
    for w in ws: o += tuple(w)
    return freered(o)
def pw(w, e): return w if e == 1 else inv(w)
def nf(w):
    o, st, ok = R.reduce(to_kb(w)); assert ok; return o
yW = cat(inv(M), y); sW = cat(inv(r), inv(M), r, s); d = inv(r)
maps = {'algebraic dictionary (M -> B M B^-1)': cat(B, M, inv(B)), 'geometric map (M -> M)': M}
out = {}
for mname, MW in maps.items():
    print(f'== {mname}')
    rows = {
     'B1: B x B^-1 = y_W^-1': cat(B, x, inv(B), yW),
     'M2 (e4=-1): B y_W B^-1 = M_W^-1 y_W x': cat(B, yW, inv(B), inv(x), inv(yW), MW),
     'M2 (e4=+1): B y_W B^-1 = M_W y_W x': cat(B, yW, inv(B), inv(x), inv(yW), inv(MW)),
     'M3 (e=-1): B s_W B^-1 = d M_W^-1 d^-1 s_W, d = r^-1': cat(B, sW, inv(B), inv(sW), d, MW, inv(d)),
     'M3 (e=+1): B s_W B^-1 = d M_W d^-1 s_W, d = r^-1': cat(B, sW, inv(B), inv(sW), d, inv(MW), inv(d)),
     'F1_W (eA=+1) = M_W A x': cat(MW, A, x),
     'F1_W (eA=+1) . (M A x)^-1': cat(MW, A, x, inv(x), inv(A), inv(M)),
    }
    refs = {'[B,M] = B M B^-1 M^-1': cat(B, M, inv(B), inv(M)), '[B,M^-1] = B M^-1 B^-1 M': cat(B, inv(M), inv(B), M),
            'B M^-1 B^-1 M^-1 (M2/M3 with the other sign)': cat(B, inv(M), inv(B), inv(M)), 'M A x (derived filling)': cat(M, A, x),
            'r^-1 [B,M^-1] r': cat(inv(r), B, inv(M), inv(B), M, r), 'r^-1 B M^-1 B^-1 M^-1 r': cat(inv(r), B, inv(M), inv(B), inv(M), r)}
    refnf = {k: nf(v) for k, v in refs.items()}
    out[mname] = {}
    for k, w in rows.items():
        n = nf(w); same = [rk for rk, rv in refnf.items() if rv == n]
        out[mname][k] = {'residual_length': len(n), 'same_normal_form_as': same}
        print(f'   {"IDENTITY" if not n else f"residual {len(n):3d}"}   {k}' + (f'   == {same}' if same else ''))
json.dump(out, open(f'{HERE}/wuebben_rows_two_maps.json', 'w'), indent=1)

# explicit quotients (equality in Q by reduction of the quotient to the empty word, independent of normal forms)
print('== explicit quotients under the geometric map (M_W = M)')
MW = M
quot = {
 'M2 (e4=-1) relator . [B,M^-1]^-1': cat(B, yW, inv(B), inv(x), inv(yW), MW, inv(cat(B, inv(M), inv(B), M))),
 'M3 (e=-1) relator . (r^-1 [B,M^-1] r)^-1': cat(B, sW, inv(B), inv(sW), d, MW, inv(d), inv(cat(inv(r), B, inv(M), inv(B), M, r))),
 'M3 (e=+1) relator . (r^-1 B M^-1 B^-1 M^-1 r)^-1': cat(B, sW, inv(B), inv(sW), d, inv(MW), inv(d), inv(cat(inv(r), B, inv(M), inv(B), inv(M), r))),
 'M2 (e4=+1) relator . (B M^-1 B^-1 M^-1)^-1': cat(B, yW, inv(B), inv(x), inv(yW), inv(MW), inv(cat(B, inv(M), inv(B), inv(M)))),
}
out['explicit quotients, geometric map'] = {}
for k, w in quot.items():
    n = nf(w); out['explicit quotients, geometric map'][k] = len(n)
    print(f'   {"IDENTITY" if not n else f"residual {len(n):3d}"}   {k}')
json.dump(out, open(f'{HERE}/wuebben_rows_two_maps.json', 'w'), indent=1)
