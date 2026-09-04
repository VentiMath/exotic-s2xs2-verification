#!/usr/bin/env python3
"""Part A: the two candidate x-transport rows and their quotient, reduced in the
sealed complement system (alpha_residual/complement_input.rws.kbprog, a halted
shortlex system for Q: every rule is a consequence of the 78 relators, so a
reduction to the empty word is a proof in pi_1(C_aud); a nonzero residual is
only a normal form in the halted system, not a disproof)."""
import json, os, sys, time
HF = os.path.expanduser('~/exotic-s2xs2-verification/verification/luttinger/honest_filling')
LU = os.path.dirname(HF)
SRC = open(f'{HF}/wuebben_dictionary/reduce_in_halted.py').read()
lines = SRC.split('\n'); cut = len(lines); seen = False
for i, ln in enumerate(lines):
    if ln.startswith('class RWS'): seen = True; continue
    if seen and ln and not ln[0].isspace() and not ln.startswith(('def ', 'class ', '#')): cut = i; break
exec('\n'.join(lines[:cut]))
def inv(w): return tuple(-x for x in reversed(w))
def cat(*ws):
    out = ()
    for w in ws: out += tuple(w)
    return freered(out)
def qstr(w): return ' '.join(f'g{abs(g)}' + ('' if g > 0 else '^-1') for g in w) or '1'
t0 = time.time()
R = RWS(load(f'{LU}/alpha_residual/complement_input.rws.kbprog'))
print(f'complement system: {len(R.rules)} rules, maxlen {R.maxlen}, loaded in {time.time()-t0:.0f}s')
H = json.load(open(f'{HF}/honest_filling.json'))
G = {k: tuple(v) for k, v in H['sheet_generator_words_in_Q'].items()}
x, y, r, s, A, B, M, N = (G[k] for k in 'x y r s A B M N'.split())
def red(w):
    out, steps, ok = R.reduce(to_kb(w))
    assert ok
    return tuple((g + 1) // 2 if g % 2 else -(g // 2) for g in out)   # back to Q letters
tests = {
 'ours: B x B^-1 (y^-1 M)^-1  [certified row]': cat(B, x, inv(B), inv(M), y),
 'his:  B x B^-1 (y^-1)^-1     [printed row B1]': cat(B, x, inv(B), y),
 'quotient of the two rows: (B x B^-1 y) . (B x B^-1 M^-1 y)^-1 = B x B^-1 M B x^-1 B^-1 (free group)': cat(B, x, inv(B), M, B, inv(x), inv(B)),
 'M itself': M,
 'y^-1 M y  (= the quotient, using the certified row)': cat(inv(y), M, y),
 'inverse transport B^-1 x B (x y)^-1  [psi^-1(x) = x y, no meridian]': cat(inv(B), x, B, inv(y), inv(x)),
 'inverse transport B^-1 y B x  [psi^-1(y) = x^-1, no meridian]': cat(inv(B), y, B, x),
 'inverse transport B^-1 r B r^-1': cat(inv(B), r, B, inv(r)),
 'inverse transport B^-1 s B s^-1': cat(inv(B), s, B, inv(s)),
 'his row under the dictionary y -> M^-1 y: B x B^-1 (M^-1 y)': cat(B, x, inv(B), inv(M), y),
 '[B, M] = B M B^-1 M^-1': cat(B, M, inv(B), inv(M)),
 'M_W = B M B^-1': cat(B, M, inv(B)),
 'his alpha filling F1_W = B M B^-1 A x': cat(B, M, inv(B), A, x),
 'derived alpha filling F1 = M A x': cat(M, A, x),
 'F1_W . F1^-1 = B M B^-1 M^-1 (free group)': cat(B, M, inv(B), A, x, inv(x), inv(A), inv(M)),
}
out = {}
for name, w in tests.items():
    rw = red(w)
    out[name] = {'word_in_Q': list(w), 'length': len(w), 'residual_in_Q': list(rw), 'residual_length': len(rw)}
    print(f'{name}\n    input length {len(w):3d} -> residual length {len(rw):3d}   {"IDENTITY IN Q" if not rw else "normal form: " + qstr(rw)}')
# same-normal-form equalities (proofs of equality in Q even without confluence)
eq = {
 'nf(B x B^-1 y) == nf(y^-1 M y)': red(cat(B, x, inv(B), y)) == red(cat(inv(y), M, y)),
 'nf(quotient B x B^-1 M B x^-1 B^-1) == nf(y^-1 M y)': red(cat(B, x, inv(B), M, B, inv(x), inv(B))) == red(cat(inv(y), M, y)),
 'nf(F1_W . F1^-1) == nf([B,M])': red(cat(B, M, inv(B), A, x, inv(x), inv(A), inv(M))) == red(cat(B, M, inv(B), inv(M))),
}
for k, v in eq.items(): print(f'{k}: {v}')
out['_equalities_by_common_normal_form'] = eq
out['_system'] = {'path': 'alpha_residual/complement_input.rws.kbprog', 'rules': len(R.rules)}
out['_letters'] = 'Q letters: g1,g2,g3 of sealed_transport/r_presentations.json (k / -k); sheet words from honest_filling.json sheet_generator_words_in_Q'
json.dump(out, open('residuals.json', 'w'), indent=1)
print('wrote residuals.json')
