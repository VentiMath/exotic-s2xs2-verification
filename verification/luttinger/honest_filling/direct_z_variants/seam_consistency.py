"""Seam-consistency test for the direct double (issue #819).

In pi_1 of the boundary mapping torus M_h, based on the p-section circle t,
    t g t^-1 = h_*(g)   for every fiber loop g,
where h is the boundary monodromy, the commutator of phi_0 and psi_0 in the
order fixed by the oriented boundary word.  Pushing into pi_1(V_aud, q) along a
base arc gamma turns t into an arrangement delta of [A,B] and g into its
transported image tau(g).  A pair (delta, tau) used in the doubled presentation
is consistent only if
    delta tau(g) delta^-1 = tau(h_delta(g))   in the honest filled group.
The certified presentation uses tau = id.  h_delta is computed from the
UNSURGERED monodromy actions (sheet rows with M = N = 1):
    phi_0: x<->r, y<->s;   psi_0: x->y^-1, y->yx, r->r, s->s.
Equality is certified by reduction to the empty word in the halted shortlex
system for honest_y1_p1_p1 (non-reduction is inconclusive).
"""
import sys
_src = open('../wuebben_dictionary/reduce_in_halted.py').read()
exec(_src[:_src.index('sealed = json.load')])  # load, to_kb, freered, RWS only; skip the module's demo run

X, Y, R, S, A, B, M, N = range(1, 9)

def inv(w): return [-l for l in reversed(w)]

phi = {X: [R], Y: [S], R: [X], S: [Y]}
psi = {X: [-Y], Y: [Y, X], R: [R], S: [S]}
psi_inv = {X: [X, Y], Y: [-X], R: [R], S: [S]}

def apply(aut, w):
    out = []
    for l in w:
        img = aut[abs(l)]
        out += img if l > 0 else inv(img)
    return list(freered(out))

def act(letter):
    if letter == A or letter == -A: return phi
    if letter == B: return psi
    if letter == -B: return psi_inv
    raise ValueError(letter)

def h_of(delta, g):
    w = [g]
    for l in reversed(delta):
        w = apply(act(l), w)
    return w

arr = {'AiBiAB': [-A, -B, A, B], 'BiABAi': [-B, A, B, -A], 'ABAiBi': [A, B, -A, -B], 'BAiBiA': [B, -A, -B, A],
       'BiAiBA': [-B, -A, B, A], 'AiBABi': [-A, B, A, -B], 'BABiAi': [B, A, -B, -A], 'ABiAiB': [A, -B, -A, B]}

# sanity: psi_inv really inverts psi on the free group
for g in (X, Y, R, S):
    assert apply(psi, apply(psi_inv, [g])) == [g] and apply(psi_inv, apply(psi, [g])) == [g]

sysfile = sys.argv[1] if len(sys.argv) > 1 else '../kbmag/honest_y1_p1_p1.rws.kbprog'
eqs = load(sysfile)
Rw = RWS(eqs)
print('system', sysfile, 'equations', len(eqs), flush=True)

names = {X: 'x', Y: 'y', R: 'r', S: 's'}
for name, d in arr.items():
    res = []
    for g in (X, Y, R, S):
        lhs = d + [g] + inv(d)
        rhs = h_of(d, g)
        w = freered(lhs + inv(rhs))
        red = Rw.reduce(to_kb(w))[0]
        res.append((names[g], len(red)))
    ok = all(n == 0 for _, n in res)
    print(f'{name:8s} consistent_with_trivial_transport={ok!s:5s} residual_lengths={res}', flush=True)
