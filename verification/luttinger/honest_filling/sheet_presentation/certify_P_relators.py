#!/usr/bin/env python3
"""Certify the relators of P (mtc3.log: presentation of Q on the sheet loops h1..h8) as identities of
pi_1(C_aud) by substituting the geom words and reducing in the halted complement system.  Reconstructed
from the session transcript on 2026-09-03; writes certified_P_relators.json next to this file."""
import json, re, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
LU = os.path.abspath(os.path.join(HERE, '..', '..'))
_src = open(os.path.join(HERE, '..', 'wuebben_dictionary', 'reduce_in_halted.py')).read()
exec(_src[:_src.index('sealed = json.load')])          # load, to_kb, freered, RWS
def inv(w): return [-x for x in reversed(w)]
T = json.load(open(f'{LU}/sealed_transport/r_presentations.json'))['tracked_words']
names = ['x', 'y', 'r', 's', 'A', 'B', 'M', 'N']; G = {n: T['geom_' + n] for n in names}
log = open(os.path.join(HERE, 'mtc3.log')).read().replace('\\\n', '')
rel_lines = [l.strip() for l in log.split('P relators:')[1].splitlines() if l.strip().startswith('h')]
def parse(s):
    toks = re.findall(r'h\d+|\^-?\d+|\(|\)|\*', s); pos = 0
    def seq():
        nonlocal pos
        out = []
        while pos < len(toks) and toks[pos] != ')':
            t = toks[pos]
            if t == '*': pos += 1; continue
            if t == '(':
                pos += 1; inner = seq(); pos += 1
            else: inner = [int(t[1:])]; pos += 1
            if pos < len(toks) and toks[pos].startswith('^'):
                e = int(toks[pos][1:]); pos += 1
                inner = inner * e if e > 0 else [-x for x in reversed(inner)] * (-e)
            out += inner
        return out
    return seq()
def subst(sw):
    out = []
    for l in sw: out += G[names[abs(l) - 1]] if l > 0 else inv(G[names[abs(l) - 1]])
    return list(freered(out))
R = RWS(load(f'{LU}/alpha_residual/complement_input.rws.kbprog'))
cert = []
for s in rel_lines:
    sw = parse(s); q = subst(sw); red = R.reduce(to_kb(q))[0]
    print(f'   {s:70s} Q-len {len(q):4d} -> {len(red):3d} {"IDENTITY" if not red else ""}')
    if not red: cert.append(sw)
json.dump(cert, open(os.path.join(HERE, 'certified_P_relators.json'), 'w'))
print(len(cert), 'of', len(rel_lines), 'P relators certified by reduction')
