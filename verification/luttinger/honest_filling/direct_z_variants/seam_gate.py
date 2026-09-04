"""Seam gate for doubled presentations (issue #823).

A doubled presentation of pi_1(Z_aud) = pi_1(V_L u_sigma V_R) is specified, based at the boundary
point q, by (i) the fiber seam map S: fiber loop g in the L copy is identified with S(g) in the R copy,
(ii) the boundary word delta (a word in A, B) and (iii) the fiber transport tau (trivial when q lies on
the boundary, as it does in the audit complex).  Three necessary conditions are checked:

  G1  S is an involution of the free group on x,y,r,s and conjugates the unsurgered boundary
      monodromy h_delta to its inverse (sigma reverses the section circle, so t g t^-1 = h(g) on the
      left must match t^-1 S(g) t = h^-1(S g) on the right).  Free-group computation.
  G2  delta tau(g) delta^-1 = tau(h_delta(g)) in the honest filled group for g = x,y,r,s: the
      identity t g t^-1 = h(g) of the boundary mapping torus pushed into pi_1(V_aud, q).  Certified
      by reduction to the empty word in the halted 500k system (non-reduction = FAIL here, because a
      presentation that cannot pass the gate must not reach kbprog; it may be retried with a larger
      system).
  G3  the boundary relation is delta_L delta_R = 1, not delta_L = delta_R.

kbprog is to be run only on presentations that pass all three.
Usage: python3 seam_gate.py [preset ...]   presets: derived certified identity_seams all_arrangements
"""
import sys, json
_src = open('../wuebben_dictionary/reduce_in_halted.py').read()
exec(_src[:_src.index('sealed = json.load')])
X, Y, R, S, A, B, M, N = range(1, 9)
L = {1:'x',2:'y',3:'r',4:'s',5:'A',6:'B',7:'M',8:'N'}
def inv(w): return [-l for l in reversed(w)]
def show(w): return ' '.join(L[abs(l)] + ('' if l > 0 else '^-1') for l in w) or '1'
def apply(aut, w):
    out = []
    for l in w:
        img = aut[abs(l)]
        out += img if l > 0 else inv(img)
    return list(freered(out))
def compose(f, g): return {k: apply(f, g[k]) for k in (X, Y, R, S)}     # (f o g)(w) = f(g(w))
ID = {X:[X], Y:[Y], R:[R], S:[S]}
PHI = {X:[R], Y:[S], R:[X], S:[Y]}
PSI = {X:[-Y], Y:[Y, X], R:[R], S:[S]}
PSI_INV = {X:[X, Y], Y:[-X], R:[R], S:[S]}
def act(letter):
    if abs(letter) == A: return PHI
    if letter == B: return PSI
    if letter == -B: return PSI_INV
    raise ValueError(letter)
def h_of(delta):
    aut = ID
    for l in delta:                     # w g w^-1 = act(l1)(act(l2)(...)); leftmost letter outermost
        aut = compose(aut, act(l))
    return aut
def invert(aut):
    # brute force inverse on the free group generators for the small automorphisms used here
    from itertools import product
    gens = [X, Y, R, S]
    letters = [g for g in gens] + [-g for g in gens]
    target = {g: [g] for g in gens}
    found = {}
    for length in range(1, 7):
        for word in product(letters, repeat=length):
            w = list(freered(word))
            if len(w) != length: continue
            img = tuple(apply(aut, w))
            for g in gens:
                if g not in found and img == (g,):
                    found[g] = w
        if len(found) == 4: break
    assert len(found) == 4, 'inverse not found by length 6'
    return found

ARR = {'AiBiAB': [-A, -B, A, B], 'BiABAi': [-B, A, B, -A], 'ABAiBi': [A, B, -A, -B], 'BAiBiA': [B, -A, -B, A],
       'BiAiBA': [-B, -A, B, A], 'AiBABi': [-A, B, A, -B], 'BABiAi': [B, A, -B, -A], 'ABiAiB': [A, -B, -A, B]}

def gate(name, seam, delta, tau, relation, Rw):
    h = h_of(delta)
    # G1
    invol = all(apply(seam, apply(seam, [g])) == [g] for g in (X, Y, R, S))
    hinv = invert(h)
    lhs = compose(seam, compose(h, seam))            # S h S^-1 = S h S (S involution)
    g1 = invol and all(lhs[g] == hinv[g] for g in (X, Y, R, S))
    # G2
    res = {}
    for g in (X, Y, R, S):
        w = list(freered(delta + tau[g] + inv(delta) + inv(apply(tau, h[g]))))
        red = Rw.reduce(to_kb(w))[0]
        res[L[g]] = len(red)
    g2 = all(v == 0 for v in res.values())
    g3 = relation == 'product'
    verdict = 'PASS' if (g1 and g2 and g3) else 'FAIL'
    print(f'{name:22s} G1(seam conj. h -> h^-1)={g1!s:5s} G2(pairing residuals)={res} -> {g2!s:5s} G3(delta_L delta_R)={g3!s:5s}  {verdict}', flush=True)
    return verdict

if __name__ == '__main__':
    presets = sys.argv[1:] or ['derived', 'certified', 'identity_seams', 'all_arrangements']
    eqs = load('../kbmag/honest_y1_p1_p1.rws.kbprog'); Rw = RWS(eqs)
    print('filled system: honest_y1_p1_p1 halted shortlex,', len(eqs), 'equations', flush=True)
    out = {}
    if 'derived' in presets:
        out['derived (phi_0 seams, delta = A B^-1 A^-1 B)'] = gate('derived', PHI, ARR['ABiAiB'], ID, 'product', Rw)
    if 'certified' in presets:
        out['certified v2.5.0 (phi_0 seams, delta = A^-1 B^-1 A B)'] = gate('certified_v2.5.0', PHI, ARR['AiBiAB'], ID, 'product', Rw)
    if 'identity_seams' in presets:
        out['identity seams (g_L = g_R, delta = A^-1 B^-1 A B)'] = gate('identity_seams', ID, ARR['AiBiAB'], ID, 'product', Rw)
    if 'all_arrangements' in presets:
        for n, d in ARR.items():
            out[f'phi_0 seams, delta = {n}'] = gate(f'arr_{n}', PHI, d, ID, 'product', Rw)
        out['phi_0 seams, delta = ABiAiB, relation delta_L = delta_R'] = gate('eqn_ABiAiB', PHI, ARR['ABiAiB'], ID, 'equation', Rw)
    json.dump(out, open('seam_gate.json', 'w'), indent=1)
    print('summary:', {k: v for k, v in out.items()})
