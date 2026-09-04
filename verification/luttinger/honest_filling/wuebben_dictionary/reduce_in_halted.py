"""Reduce the sealed paper beta relators (and the extractor beta relators)
with the halted, non-confluent KBMAG systems of the boundary-tori
presentations.  Every equation in a halted system is a consequence of the
input relators, so a reduction to the empty word is a proof that the word
lies in the normal closure -- confluence is not needed."""
import json, re, sys, time, glob, os
SF = os.path.expanduser('~/exotic-s2xs2-verification/verification/luttinger/simplicial_filling')
LU = os.path.expanduser('~/exotic-s2xs2-verification/verification/luttinger')

def parse_words_block(text, key):
    i = text.index(key + ':=['); i += len(key) + 3
    depth = 1; j = i
    while depth:
        c = text[j]
        if c == '[': depth += 1
        elif c == ']': depth -= 1
        j += 1
    body = text[i:j-1]
    eqs = []
    for m in re.finditer(r'\[([^\[\]]*)\]', body):
        lhs, rhs = m.group(1).split(',')
        eqs.append((word(lhs), word(rhs)))
    return eqs

def word(s):
    if s == 'IdWord': return ()
    toks = re.findall(r'_g\d+|\^\d+|\(|\)|\*', s)
    pos = 0
    def seq():
        nonlocal pos
        out = []
        while pos < len(toks) and toks[pos] != ')':
            t = toks[pos]
            if t == '*': pos += 1; continue
            if t == '(':
                pos += 1; inner = seq(); assert toks[pos] == ')'; pos += 1
            else:
                assert t.startswith('_g'), t
                inner = [int(t[2:])]; pos += 1
            if pos < len(toks) and toks[pos].startswith('^'):
                inner = inner * int(toks[pos][1:]); pos += 1
            out += inner
        return out
    w = seq(); assert pos == len(toks), (s, pos)
    return tuple(w)

def load(path):
    t = open(path).read()
    t = re.sub(r'\s+', '', t).replace('\\', '')
    eqs = parse_words_block(t, 'equations')
    return eqs

def to_kb(w):  # Q letters: k / -k  ->  _g(2k-1) / _g(2k)
    return tuple(2*x-1 if x > 0 else -2*x for x in w)

def freered(w):
    out=[]
    for x in w:
        if out and out[-1]==-x: out.pop()
        else: out.append(x)
    return tuple(out)

class RWS:
    def __init__(self, eqs):
        self.rules = {}
        for l, r in eqs:
            if l not in self.rules: self.rules[l] = r
        self.maxlen = max(len(l) for l in self.rules)
    def reduce(self, w, limit=2_000_000):
        w = list(w); rules = self.rules; maxlen = self.maxlen; steps = 0
        i = 0
        while i < len(w):
            hit = None
            for L in range(1, min(maxlen, len(w)-i)+1):
                seg = tuple(w[i:i+L])
                if seg in rules:
                    hit = (L, rules[seg]); break
            if hit:
                L, rhs = hit
                w[i:i+L] = list(rhs)
                i = max(0, i - maxlen); steps += 1
                if steps > limit: return tuple(w), steps, False
            else:
                i += 1
        return tuple(w), steps, True

sealed = json.load(open(f'{LU}/sealed_transport/r_presentations.json'))
targets = {}
for f in sealed['paper_fillings']:
    tag = f"paper:{f['half_drift']}:a{f['sign_a']:+d}:b{f['sign_b']:+d}"
    targets[tag+':A'] = f['relators'][0]; targets[tag+':B'] = f['relators'][1]
for f in sealed['fillings']:
    tag = f"ext:drift{f['drift']}:a{f['sign_a']:+d}:b{f['sign_b']:+d}"
    targets[tag+':A'] = f['relators'][0]; targets[tag+':B'] = f['relators'][1]
# de-duplicate by word
uniq = {}
for k, w in targets.items():
    uniq.setdefault(tuple(freered(w)), []).append(k)

systems = sorted(glob.glob(f'{SF}/raw_proof_inputs*/*.rws.kbprog') + glob.glob(f'{SF}/common_core/*.rws.kbprog'))
for path in systems:
    t0 = time.time()
    eqs = load(path)
    R = RWS(eqs)
    print(f'\n== {os.path.relpath(path, SF)}: {len(eqs)} equations, maxlen {R.maxlen}, parsed in {time.time()-t0:.1f}s')
    # sanity: the input relators of this case
    rws_in = path[:-len('.kbprog')]
    ineqs = load(rws_in)
    print(f'   input file {os.path.basename(rws_in)}: {len(ineqs)} equations; lengths of first two non-inverse equations:',
          [len(l)+len(r) for l, r in ineqs if len(l)+len(r) > 2][:2])
    for w, names in uniq.items():
        red, steps, ok = R.reduce(to_kb(w))
        print(f'   {"/".join(names)[:70]:70s} len {len(w):3d} -> {len(red):3d}  {"IDENTITY" if not red else ""}')
    sys.stdout.flush()
