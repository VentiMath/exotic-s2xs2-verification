#!/usr/bin/env python3
"""Part B: literal transport membranes for x (and y) in the audit complex C_aud.

Pieces (each a literal grid of edges of K, or a Tietze-certified homotopy in a full subcomplex of C):
  R1  radial grid at angular copy A1: the fiber path g at J2, J1, J0 (columns radial).  Its incidences with
      T_alpha = c x {J1} are exactly the vertices (A1, v, J1) with v in g and v in c.  For g = x: none.
      For g = y: one, at (A1, c_y, J1); puncture it and read the boundary (the meridian ring).
  S1  band (stack) part, in the open stack with the e-vertices deleted (a full subcomplex of C): the based
      loop g at level 0 equals psi(g) at level m through the p-track (x -> y^-1, and x at the top equals
      x y at the bottom), certified by Tietze reduction to the empty word.
  A1  angular squares at J2 between A0 and A1 (product cylinders; meet T_beta only on e, which x, y miss).
Every word is read in the raw 2-skeleton presentation of C (reproduced letter for letter against the sealed
input), transported through the sealed Tietze certificate into Q, and reduced in the sealed complement system.
Requires PYTHONHASHSEED=0."""
import gzip, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
HF = os.path.dirname(HERE); LU = os.path.dirname(HF)
sys.path.insert(0, LU); sys.path.insert(0, f'{LU}/simplicial_filling')
if os.environ.get('PYTHONHASHSEED') != '0':
    raise SystemExit('run with PYTHONHASHSEED=0')
from pi1 import Presentation, free_reduce, inverse
from fast_tietze import simplify, verify_certificate, renumber
from sweep import certify_grid_sweep, grid_intersection_sign, punctured_grid_boundary_cycles
from paper_bridge import build_paper_loops
from complex import Complex
from layers import build_stack
from fiber import K_BAND
from frontier_filling import build_state, transport
t0 = time.time()
def log(m): print(f'[{time.time()-t0:5.0f}s] {m}', flush=True)
B, K, T, amb, tsg, X, P = build_state(t0)
sealed_in = json.load(gzip.open(f'{LU}/sealed_transport/r_tietze_input.json.gz'))
assert P.ngens == sealed_in['ngens'] and P.relators == sealed_in['relators'], 'raw presentation differs from sealed input'
log('raw presentation reproduces the sealed input letter for letter')
F = B['F']; m = B['m']; phi0 = B['phi0']
loops = build_paper_loops(F)
cset, eset = set(F['curves']['c']), set(F['curves']['e'])
J = lambda k: ('J', k)
q = (('A', 0, 'p'), J(2))
out = {'pieces': {}}
words = {}          # raw words to transport

def checked_loop(path):
    assert path[0] == path[-1]
    for u, v in zip(path, path[1:]):
        assert u == v or frozenset((u, v)) in X.C.simplices[1], (u, v)
    return X.P.loop_word(path)

# ---- R1: radial grids at A1 ------------------------------------------------------------------------
comps = {'alpha': B['Ta_verts'], 'beta': B['Tb_verts']}
for g in ('x', 'y'):
    path = loops[g]
    rows = [[(('A', 1, v), J(k)) for v in path] for k in (2, 1, 0)]     # J2 (outer, band foot) -> J0
    hits = certify_grid_sweep(K, rows, comps)
    rec = {'rows': ['J2', 'J1', 'J0'], 'path_length': len(path) - 1,
           'alpha_hits': [(i, j, repr(v)) for i, j, v in hits['alpha']], 'beta_hits': [(i, j, repr(v)) for i, j, v in hits['beta']]}
    log(f'R1[{g}]: radial grid at A1 is simplicial; T_alpha hits {rec["alpha_hits"]}, T_beta hits {rec["beta_hits"]}')
    out['pieces'][f'R1_{g}'] = rec
    if g == 'y':
        assert len(hits['alpha']) == 1 and not hits['beta']
        hit = hits['alpha'][0]
        sign = grid_intersection_sign(K, rows, hit, T, amb, tsg)
        rec['oriented_sign'] = sign
        cycles = punctured_grid_boundary_cycles(K, rows, X.Tverts)
        rec['boundary_cycle_lengths'] = sorted(len(c) - 1 for c in cycles)
        log(f'R1[y]: oriented intersection sign {sign:+d}; punctured boundary cycles of lengths {rec["boundary_cycle_lengths"]}')
        i_c = hit[1]; cy = path[i_c]
        assert cy in cset
        # With only three radial levels the open star of the puncture vertex reaches both boundary rows, so the
        # punctured grid is a strip with a single boundary circle (length 18).  The meridian is read instead as
        # the link of the puncture vertex in the grid: the 8-cycle of grid vertices around (row 1, column i_c),
        # an edge path of C because every row edge and column edge of the grid is an edge of K.
        r0, r1, r2 = rows
        octo = [r0[i_c - 1], r1[i_c - 1], r2[i_c - 1], r2[i_c], r2[i_c + 1], r1[i_c + 1], r0[i_c + 1], r0[i_c], r0[i_c - 1]]
        assert all(v not in X.Tverts for v in octo)
        to_A1 = [q, (('A', 1, 'p'), J(2))]
        whisker = to_A1 + [(('A', 1, v), J(2)) for v in path[1:i_c]]      # y_1 at A1, up to the predecessor of c_y
        assert whisker[-1] == octo[0]
        words['ring_M_direct'] = checked_loop(whisker + octo[1:] + list(reversed(whisker))[1:])
        rec['ring'] = [repr(v) for v in octo]
        rec['ring_whisker'] = 'q -> (A1,p,J2) -> y_1 at (A1,.,J2) up to the predecessor of c_y'
# the paper loops themselves at q (must equal the sealed geom words)
for g in 'xyrs':
    words[f'geom_{g}'] = checked_loop([(('A', 0, v), J(2)) for v in loops[g]])
alpha_positive = [(('A', t, 'p'), J(2)) for t in (0, 1, 2, 0)]
beta_positive = [q, (('A', 1, 'p'), J(2))] + [(('S', l, 'p'), ('t', 1)) for l in range(1, m)] + [(('A', 1, 'p'), J(k)) for k in (0, 1, 2)] + [q]
words['geom_A'] = checked_loop(list(reversed(alpha_positive)))
words['geom_B'] = checked_loop(list(reversed(beta_positive)))
# x and y^-1 at A1 level J2 and J0, based through the p-track (used to glue the pieces)
for g in ('x', 'y'):
    path = loops[g]
    words[f'{g}_A1_J2'] = checked_loop([q] + [(('A', 1, v), J(2)) for v in path] + [q])
    words[f'{g}_A1_J0'] = checked_loop([q, (('A', 1, 'p'), J(2)), (('A', 1, 'p'), J(1)), (('A', 1, 'p'), J(0))] + [(('A', 1, v), J(0)) for v in path[1:]] + [(('A', 1, 'p'), J(1)), (('A', 1, 'p'), J(2)), q])
    words[f'{g}_A1_J0_via_band'] = checked_loop([q, (('A', 1, 'p'), J(2))] + [(('S', l, 'p'), ('t', 1)) for l in range(1, m)] + [(('A', 1, v), J(0)) for v in path] + [(('S', l, 'p'), ('t', 1)) for l in range(m - 1, 0, -1)] + [(('A', 1, 'p'), J(2)), q])
log(f'{len(words)} raw words read in the 2-skeleton presentation of C')

# ---- S1: band part in the open stack minus e ------------------------------------------------------------
L, V, rank = F['L'], F['V'], F['L'].rank.get
twists = [([V(n, 0, i) for i in range(K_BAND[n])], [V(n, 1, i) for i in range(K_BAND[n])], [V(n, -1, i) for i in range(K_BAND[n])], d) for n, d in (('b', 1), ('a', -1))]
cells, levels, _ = build_stack(L, rank, twists, copy_tag='SX')
assert levels == m
drilled = [c for c in cells if not any((isinstance(v, tuple) and len(v) == 3 and v[0] == 'SX' and isinstance(v[1], int) and v[2] in eset) for v in c)]
stack = Complex(drilled, order=sorted({v for c in drilled for v in c}, key=str))
PS = Presentation(stack, ('SX', 0, 'p'))
def at(level, path): return [('SX', level, v) for v in path]
def cat(*ps):
    o = list(ps[0])
    for p in ps[1:]:
        assert o[-1] == p[0]; o += p[1:]
    return o
vert = [('SX', l, 'p') for l in range(m + 1)]
tests_S = {
 'x_bottom = (y^-1)_top': cat(at(0, loops['x']), vert, at(m, loops['y']), list(reversed(vert))),          # x . vert . y (top) . vert^-1: y^-1 top means reversed y; so compare x = vert y^-1 vert^-1  <=> x vert y vert^-1 = 1
 'x_top = (x y)_bottom': cat(vert, at(m, loops['x']), list(reversed(vert)), list(reversed(at(0, loops['y']))), list(reversed(at(0, loops['x'])))),
 'y_bottom = (y x)_top': cat(at(0, loops['y']), vert, list(reversed(at(m, loops['x']))), list(reversed(at(m, loops['y']))), list(reversed(vert))),
}
res_words = [PS.loop_word(p) for p in tests_S.values()]
live, rels, red, proof = simplify(PS.ngens, PS.relators, res_words, verbose=False, certify=True)
assert verify_certificate(PS.ngens, PS.relators, res_words, proof) == (live, rels, red)
n, rels, red = renumber(live, rels, red)
out['pieces']['S1_stack_minus_e'] = {'rank_after_tietze': n, 'relators_after_tietze': [len(r) for r in rels], 'residual_lengths': dict(zip(tests_S, [len(w) for w in red])), 'tietze_steps': len(proof['steps'])}
log(f'S1: stack minus e: rank {n}, relators {[len(r) for r in rels]}, residuals {dict(zip(tests_S, [len(w) for w in red]))}')
for k, w in zip(tests_S, red):
    assert not w, f'stack homotopy {k} did not reduce to the empty word'

# ---- transport into Q -------------------------------------------------------------------------------------
cert = json.load(gzip.open(f'{LU}/sealed_transport/r_tietze_certificate.json.gz'))
pres = json.load(open(f'{LU}/sealed_transport/r_presentations.json'))
names = list(sealed_in['word_names']) + list(words)
allw = list(sealed_in['words']) + [words[k] for k in words]
live, rels_out, tracked = transport(P.ngens, P.relators, allw, cert, verbose=False)
ren = {int(k): v for k, v in pres['renumbering'].items()}
f = lambda w: [ren[abs(g)] * (1 if g > 0 else -1) for g in w]
assert [f(r) for r in rels_out] == pres['relators']
tracked = [f(w) for w in tracked]
for nm, w in zip(sealed_in['word_names'], tracked):
    assert w == pres['tracked_words'][nm], nm
qw = dict(zip(names[len(sealed_in['words']):], tracked[len(sealed_in['words']):]))
for g in 'xyrs': assert qw[f'geom_{g}'] == pres['tracked_words'][f'geom_{g}']
assert qw['geom_A'] == pres['tracked_words']['geom_A'] and qw['geom_B'] == pres['tracked_words']['geom_B']
log('sealed transport replayed: Q and the 89 sealed words reproduced; new words in Q letters')
out['words_in_Q'] = qw
json.dump(out, open(f'{HERE}/trace_x_transport.json', 'w'), indent=1)
log('wrote trace_x_transport.json')
