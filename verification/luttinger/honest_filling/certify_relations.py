#!/usr/bin/env python3
"""Check that every relation and identity used by the honest-filling collapse
reduces to the empty word under the complement-only rewriting system
(alpha_residual/complement_input.rws.kbprog).  Each equation of that system is
a consequence of the 78 complement relators, so a reduction to the empty word
proves the identity in pi_1(C_aud) whether or not the system is confluent."""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
LU = HERE.parent

def parse_kbprog(path):
    text = re.sub(r'\s+', '', Path(path).read_text()).replace('\\', '')
    i = text.index('equations:=[') + len('equations:=[')
    depth, j = 1, i
    while depth:
        depth += {'[': 1, ']': -1}.get(text[j], 0); j += 1
    def word(s):
        if s == 'IdWord': return ()
        toks = re.findall(r'_g\d+|\^\d+|\(|\)|\*', s); pos = 0
        def seq():
            nonlocal pos
            out = []
            while pos < len(toks) and toks[pos] != ')':
                t = toks[pos]
                if t == '*': pos += 1; continue
                if t == '(':
                    pos += 1; inner = seq(); pos += 1
                else:
                    inner = [int(t[2:])]; pos += 1
                if pos < len(toks) and toks[pos].startswith('^'):
                    inner = inner * int(toks[pos][1:]); pos += 1
                out += inner
            return out
        return tuple(seq())
    rules = {}
    for m in re.finditer(r'\[([^\[\]]*)\]', text[i:j-1]):
        lhs, rhs = m.group(1).split(',')
        rules.setdefault(word(lhs), word(rhs))
    return rules

def reduce(rules, maxlen, w):
    w = list(w); i = 0
    while i < len(w):
        for L in range(1, min(maxlen, len(w) - i) + 1):
            seg = tuple(w[i:i+L])
            if seg in rules:
                w[i:i+L] = list(rules[seg]); i = max(0, i - maxlen); break
        else:
            i += 1
    return tuple(w)

def freered(w):
    out = []
    for x in w:
        if out and out[-1] == -x: out.pop()
        else: out.append(x)
    return out

def inv(w): return [-x for x in reversed(w)]
def to_kb(w): return tuple(2*x-1 if x > 0 else -2*x for x in w)

def main():
    d = json.loads((HERE / 'honest_filling.json').read_text())
    G = d['sheet_generator_words_in_Q']; names = d['sheet_generators']
    def subst(sw):
        out = []
        for l in sw: out += G[names[abs(l)-1]] if l > 0 else inv(G[names[abs(l)-1]])
        return freered(out)
    rules = parse_kbprog(LU / 'alpha_residual' / 'complement_input.rws.kbprog')
    maxlen = max(len(k) for k in rules)
    print(f'complement system: {len(rules)} equations')
    ok = True
    for k, sw in d['relations_in_sheet_letters'].items():
        red = reduce(rules, maxlen, to_kb(subst(sw)))
        print(f'  relation {k:28s} -> {len(red):3d} {"IDENTITY" if not red else "NOT REDUCED"}'); ok &= not red
    for k, v in d['identities'].items():
        red = reduce(rules, maxlen, to_kb(freered(inv(v['tracked_word']) + subst(v['sheet_word']))))
        print(f'  identity {k:28s} -> {len(red):3d} {"IDENTITY" if not red else "NOT REDUCED"}'); ok &= not red
    for slug, c in d['cases'].items():
        assert subst(c['alpha_relator']) == c['alpha_relator_in_Q'] and subst(c['beta_relator']) == c['beta_relator_in_Q'], slug
    print('case relators re-derived from the sheet words: OK')
    print('ALL RELATIONS AND IDENTITIES CERTIFIED' if ok else 'SOME RELATION DID NOT REDUCE')
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
