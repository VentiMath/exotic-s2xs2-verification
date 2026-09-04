#!/usr/bin/env python3
"""Part B, step 2: certify the literal pieces of trace_x_transport.json as identities of Q by reduction in the
sealed complement system, and assemble the two transport rows from them.  0 = identity in Q (proof)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); HF = os.path.dirname(HERE); LU = os.path.dirname(HF)
SRC = open(f'{HF}/wuebben_dictionary/reduce_in_halted.py').read()
lines = SRC.split('\n'); cut = len(lines); seen = False
for i, ln in enumerate(lines):
    if ln.startswith('class RWS'): seen = True; continue
    if seen and ln and not ln[0].isspace() and not ln.startswith(('def ', 'class ', '#')): cut = i; break
exec('\n'.join(lines[:cut]))
R = RWS(load(f'{LU}/alpha_residual/complement_input.rws.kbprog'))
W = {k: tuple(v) for k, v in json.load(open(f'{HERE}/trace_x_transport.json'))['words_in_Q'].items()}
S = json.load(open(f'{LU}/sealed_transport/r_presentations.json'))['tracked_words']
M = tuple(S['geom_M']); B = W['geom_B']; x = W['geom_x']; y = W['geom_y']
def inv(w): return tuple(-g for g in reversed(w))
def cat(*ws):
    o = ()
    for w in ws: o += tuple(w)
    return freered(o)
def red(w):
    r, steps, ok = R.reduce(to_kb(w)); assert ok; return len(r)
ring = W['ring_M_direct']; yJ2 = W['y_A1_J2']; yJ0 = W['y_A1_J0']; yband = W['y_A1_J0_via_band']
xJ2 = W['x_A1_J2']; xJ0 = W['x_A1_J0']; xband = W['x_A1_J0_via_band']
tests = {
 # angular squares at J2 (A0 -> A1)
 'A1: x at (A1,J2) = geom_x': cat(xJ2, inv(x)),
 'A1: y at (A1,J2) = geom_y': cat(yJ2, inv(y)),

 # R1: radial grids at A1
 'R1[x]: x at (A1,J0) via the radial p-track = x at (A1,J2)  [no puncture]': cat(xJ0, inv(xJ2)),
 'R1[y]: y at (A1,J0) via the radial p-track = ring . y at (A1,J2)': cat(yJ0, inv(cat(ring, yJ2))),
 'R1[y]: y at (A1,J0) via the radial p-track = ring^-1 . y at (A1,J2)': cat(yJ0, inv(cat(inv(ring), yJ2))),
 'R1[y]: y at (A1,J0) = y at (A1,J2) . ring': cat(yJ0, inv(cat(yJ2, ring))),
 'R1[y]: y at (A1,J0) = y at (A1,J2) . ring^-1': cat(yJ0, inv(cat(yJ2, inv(ring)))),
 'ring = geom_M': cat(ring, inv(M)),
 'ring = geom_M^-1': cat(ring, M),
 # S1: band part, read in Q (the loop through the band and back is the B^-1-conjugate of the radial one)
 'band: y via band = B^-1 (y via radial) B': cat(yband, inv(cat(inv(B), yJ0, B))),
 'band: x via band = B^-1 (x via radial) B': cat(xband, inv(cat(inv(B), xJ0, B))),
 'S1: x at (A1,J2) = (y via band)^-1   [x_bottom = y^-1_top]': cat(xJ2, yband),
 'S1: x via band = geom_x geom_y        [x_top = (x y)_bottom]': cat(xband, inv(cat(x, y))),
 # assembled rows
 'row (ours): B x B^-1 = y^-1 ring^-1': cat(B, x, inv(B), ring, y),
 'row (ours): B x B^-1 = y^-1 ring': cat(B, x, inv(B), inv(ring), y),
 'row (ours): B x B^-1 = y^-1 M   [certified before]': cat(B, x, inv(B), inv(M), y),
 'row (inverse loop): B^-1 x B = x y': cat(inv(B), x, B, inv(y), inv(x)),
 'row (inverse loop, y): B^-1 y B = (B^-1 M B) x^-1': cat(inv(B), y, B, x, inv(B), inv(M), B),
 'row (inverse loop, y): B^-1 y B = M x^-1   [unconjugated meridian]': cat(inv(B), y, B, x, inv(M)),
 'row (inverse loop, y): B^-1 y B = M^-1 x^-1': cat(inv(B), y, B, x, M),
 'row (inverse loop, y): B^-1 y B = (B^-1 M^-1 B) x^-1': cat(inv(B), y, B, x, inv(B), M, B),
}
res = {}
for k, w in tests.items():
    r = red(w); res[k] = r
    print(f'{"IDENTITY" if r == 0 else f"residual {r:3d}"}   {k}')
json.dump(res, open(f'{HERE}/certify_pieces.json', 'w'), indent=1)
