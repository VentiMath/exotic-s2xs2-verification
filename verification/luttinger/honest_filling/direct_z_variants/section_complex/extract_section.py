"""Extract the p-section subcomplex of the real audit bundle K (all simplices whose vertices carry
fiber label p) and the three based edge paths (alpha_positive, beta_positive, boundary at q), so the
boundary class can be computed in the complex's own section rather than in a hand model."""
import sys, json, time, os
sys.path.insert(0, os.path.expanduser('~/luttinger/direct-z-integration/verification/luttinger'))
from bundle import build_bundle, check_bundle
t0 = time.time()
B = build_bundle(dir_b=1, dir_a=-1)          # same call as r_run.main()
K = B['K']; m = B['m']
print('K f-vector', K.f_vector(), f'{time.time()-t0:.0f}s', flush=True)
def fiber_label(v):
    # vertex names: (('A', t, v), ('J', k)) | (('S', level, v), ('t', k)) | ((('S','cone',level), qi), ('t',k)) ...
    try:
        return v[0][2]
    except Exception:
        return None
def is_p(v): return fiber_label(v) == 'p'
cells = {}
for dim in (0, 1, 2):
    cells[dim] = [sorted(list(s), key=repr) for s in K.simplices[dim] if all(is_p(v) for v in s)]
print({d: len(c) for d, c in cells.items()})
J = lambda k: ('J', k)
q = (('A', 0, 'p'), J(2))
alpha_positive = [(('A', t, 'p'), J(2)) for t in (0, 1, 2, 0)]
beta_positive = [q, (('A', 1, 'p'), J(2))] + [(('S', l, 'p'), ('t', 1)) for l in range(1, m)] + \
                [(('A', 1, 'p'), J(k)) for k in (0, 1, 2)] + [q]
boundary = [q, (('A', 2, 'p'), J(2))] + [(('S', l, 'p'), ('t', 2)) for l in range(1, m)] + \
           [(('A', 2, 'p'), J(0)), (('A', 0, 'p'), J(0))] + [(('S', l, 'p'), ('t', 0)) for l in range(m - 1, 0, -1)] + [q]
verts = {repr(v) for s in cells[0] for v in s}
edges = {frozenset(repr(v) for v in s) for s in cells[1]}
for name, path in (('alpha_positive', alpha_positive), ('beta_positive', beta_positive), ('boundary', boundary)):
    missing_v = [v for v in path if repr(v) not in verts]
    missing_e = [(u, v) for u, v in zip(path, path[1:]) if frozenset((repr(u), repr(v))) not in edges]
    print(name, 'len', len(path), 'missing vertices', missing_v[:3], 'missing edges', missing_e[:3], flush=True)
# boundary check of the section: edges in exactly one section 2-cell
from collections import Counter
cnt = Counter()
for s in cells[2]:
    for i in range(3):
        for j in range(i + 1, 3):
            cnt[frozenset((repr(s[i]), repr(s[j])))] += 1
free = [e for e, c in cnt.items() if c == 1]
print('section: V', len(cells[0]), 'E', len(cells[1]), 'F', len(cells[2]), 'chi', len(cells[0]) - len(cells[1]) + len(cells[2]),
      'free edges', len(free), flush=True)
json.dump({'m': m, 'cells': {str(d): [[repr(v) for v in s] for s in c] for d, c in cells.items()},
           'paths': {n: [repr(v) for v in p] for n, p in (('alpha_positive', alpha_positive), ('beta_positive', beta_positive), ('boundary', boundary))},
           'free_edges': [sorted(e) for e in free]}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'section_complex.json'), 'w'))
print('wrote section_complex.json', f'{time.time()-t0:.0f}s')
