"""
The genus-2 fiber L as the regular neighbourhood of the Lidman-Piccirillo
five-chain a-b-c-d-e (five plumbed annular bands) capped by two discs coned
from p and O.  This is exactly the structure [M] Lemma 7.1 says determines the
marked surface: the machine checks the intersection pattern and the
chain-reversing involution phi0, so the complex IS the marked surface, with no
picture read.

Every curve is a chordless edge cycle with an aligned 3-ring grid collar
(rows -1, 0, +1), so Dehn twists about a and b are realizable by the standard
shear flip sequence, and c and e carry product-framing push-offs.

Vertex names:
  ('γ', r, i)  band vertex: band γ in 'abcde', row r in {-1,0,1}, column i mod k_γ
  crossing patches identify 3x3 blocks of consecutive bands (union-find, the
  canonical representative is the earlier band's name)
  'p', 'O'     the two cone vertices.
phi0: chain-reversing involution  a<->e, b<->d, c->c (half-rotation), p,O fixed.
"""
from collections import defaultdict
from itertools import combinations
from complex import Complex

# columns per band (even, and large enough that all identifications stay
# simplicial and every curve is chordless).  c needs its two crossings at
# antipodal columns for the free half-rotation.
K_BAND = {'a': 8, 'b': 8, 'c': 8, 'd': 8, 'e': 8}
# where each crossing sits: (band1, centre column in band1, band2, centre col in band2)
# the 3x3 patch of band1 spans columns i0-1, i0, i0+1 (centre i0), rows -1,0,1;
# likewise for band2.  Chain order a-b-c-d-e.  c's two crossings are antipodal
# (columns 0 and 4) so phi0's half-rotation of c swaps them.
CROSSINGS = [
    ('a', 0, 'b', 0),
    ('b', 4, 'c', 0),
    ('c', 4, 'd', 0),
    ('d', 4, 'e', 0),
]


def _find(uf, x):
    while uf.get(x, x) != x:
        uf[x] = uf.get(uf[x], uf[x])
        x = uf[x]
    return x


def _union(uf, x, y):
    rx, ry = _find(uf, x), _find(uf, y)
    if rx != ry:
        # keep the lexicographically smaller name canonical (deterministic)
        if str(ry) < str(rx):
            rx, ry = ry, rx
        uf[ry] = rx


def build_fiber():
    uf = {}
    # -- plumb the crossings: identify the 3x3 blocks -----------------------
    # band1 local frame at the patch: (row r, col i0+t), t in -1,0,1
    # band2 local frame:              (row s, col j0+u), u in -1,0,1
    # identification: band2's along-direction is band1's across-direction:
    #   (b1, r, i0+t) == (b2, t, j0+r)
    # (both bands' rows run -1..1; this is the transpose gluing.  Orientation
    # consistency across the whole chain is certified by the checks below.)
    for b1, i0, b2, j0 in CROSSINGS:
        k1, k2 = K_BAND[b1], K_BAND[b2]
        for r in (-1, 0, 1):
            for t in (-1, 0, 1):
                _union(uf, (b1, r, (i0 + t) % k1), (b2, t, (j0 + r) % k2))

    def V(b, r, i):
        return _find(uf, (b, r, i % K_BAND[b]))

    # -- band triangles: uniform "/" diagonal ------------------------------
    tris = set()
    for b, k in K_BAND.items():
        for r in (-1, 0):
            for i in range(k):
                p00 = V(b, r, i)
                p10 = V(b, r + 1, i)
                p01 = V(b, r, i + 1)
                p11 = V(b, r + 1, i + 1)
                # "/" diagonal: {p10, p01}
                tris.add(frozenset((p00, p10, p01)))
                tris.add(frozenset((p10, p01, p11)))
    tris = {t for t in tris if len(t) == 3}

    # -- find the boundary circles and cone them ---------------------------
    # boundary edges: edges lying in exactly one triangle
    edge_count = defaultdict(list)
    for t in tris:
        vs = sorted(t, key=str)
        for e in ((vs[0], vs[1]), (vs[0], vs[2]), (vs[1], vs[2])):
            edge_count[frozenset(e)].append(t)
    boundary = [e for e, ts in edge_count.items() if len(ts) == 1]
    # trace boundary cycles
    adj = defaultdict(list)
    for e in boundary:
        u, v = tuple(e)
        adj[u].append(v)
        adj[v].append(u)
    seen = set()
    cycles = []
    for start in adj:
        if start in seen:
            continue
        cyc = [start]
        seen.add(start)
        prev = None
        cur = start
        while True:
            nxt = [w for w in adj[cur] if w != prev]
            # at a vertex visited by the boundary twice this would branch;
            # the checks below fail loudly if the neighbourhood is not clean
            assert len(nxt) >= 1, "boundary trace stuck"
            w = nxt[0]
            if w == start:
                break
            cyc.append(w)
            seen.add(w)
            prev, cur = cur, w
        cycles.append(cyc)
    assert len(cycles) == 2, f"five-chain nbhd must have 2 boundary circles, got {len(cycles)}"
    # cone: p on the circle that contains a-band outer vertices, O on the other
    cone_names = ['p', 'O']
    # deterministic assignment: the circle containing the a-band's row +1
    # far column goes to p
    marker = V('a', 1, K_BAND['a'] // 2)
    if marker in cycles[1]:
        cycles = [cycles[1], cycles[0]]
    for cn, cyc in zip(cone_names, cycles):
        n = len(cyc)
        for idx in range(n):
            tris.add(frozenset((cn, cyc[idx], cyc[(idx + 1) % n])))

    order = sorted({v for t in tris for v in t}, key=str)
    L = Complex(tris, order=order)

    # -- the five curves ----------------------------------------------------
    curves = {b: [V(b, 0, i) for i in range(K_BAND[b])] for b in K_BAND}

    # -- phi0: chain-reversing involution -----------------------------------
    # a<->e, b<->d, c->c shifted by half; rows preserved; column maps chosen so
    # the crossing pattern is equivariant:
    #   crossing (a,0,b,0)  <->  crossing (d,6,e,0) reversed
    #   crossing (b,6,c,0)  <->  crossing (c,6,d,0) reversed
    # Solve for the column maps: phi0(γ, r, i) = (γ', σ_r r, m_γ ± i + off).
    # We try the natural guess and certify by assertion.
    phi0 = {}

    def setmap(x, y):
        if x in phi0:
            assert phi0[x] == y, f"phi0 inconsistent at {x}: {phi0[x]} vs {y}"
        phi0[x] = y

    pair = {'a': 'e', 'e': 'a', 'b': 'd', 'd': 'b', 'c': 'c'}
    # column shifts chosen so crossings map to crossings: ab<->de, bc<->cd,
    # and c's two crossings swap (free half-rotation).
    shift = {'a': 0, 'e': 0, 'b': 4, 'd': 4, 'c': K_BAND['c'] // 2}
    for b, k in K_BAND.items():
        for r in (-1, 0, 1):
            for i in range(k):
                src = V(b, r, i)
                dst = V(pair[b], r, i + shift[b])
                setmap(src, dst)
    setmap('p', 'p')
    setmap('O', 'O')

    return {
        'L': L, 'curves': curves, 'phi0': phi0, 'V': V,
        'K_BAND': K_BAND, 'boundary_cycles': cycles,
    }


# ---------------------------------------------------------------------------
def check_fiber(F, verbose=True):
    L, curves, phi0 = F['L'], F['curves'], F['phi0']
    out = []

    def log(*a):
        if verbose:
            print(*a)
        out.append(a)

    fv = L.f_vector()
    chi = fv[0] - fv[1] + fv[2]
    log("f-vector:", fv, " chi =", chi)
    assert chi == -2, "Euler characteristic must be -2"

    # closed surface: every edge in exactly 2 triangles
    ec = defaultdict(int)
    for t in L.simplices[2]:
        vs = L.sorted_tuple(t)
        for e in ((vs[0], vs[1]), (vs[0], vs[2]), (vs[1], vs[2])):
            ec[frozenset(e)] += 1
    bad = [e for e, c in ec.items() if c != 2]
    assert not bad, f"non-manifold edges: {bad[:5]}"

    # vertex links are single circles
    for v in L.vertices():
        star = [t for t in L.simplices[2] if v in t]
        link_edges = [tuple(sorted(t - {v}, key=str)) for t in star]
        deg = defaultdict(int)
        for a, b in link_edges:
            deg[a] += 1
            deg[b] += 1
        assert all(d == 2 for d in deg.values()), f"link of {v} not a circle"
        # connectivity of the link
        nodes = set(deg)
        nbr = defaultdict(list)
        for a, b in link_edges:
            nbr[a].append(b)
            nbr[b].append(a)
        comp = {next(iter(nodes))}
        stack = list(comp)
        while stack:
            x = stack.pop()
            for y in nbr[x]:
                if y not in comp:
                    comp.add(y)
                    stack.append(y)
        assert comp == nodes, f"link of {v} disconnected"
    log("closed surface: OK (all edges in 2 triangles, links circles)")

    # orientable: propagate orientations
    tri_list = list(L.simplices[2])
    tri_neighbours = defaultdict(list)
    for triangle in tri_list:
        for edge in combinations(L.sorted_tuple(triangle), 2):
            tri_neighbours[frozenset(edge)].append(triangle)
    orient = {}
    from collections import deque
    for seed in tri_list:
        if seed in orient:
            continue
        orient[seed] = tuple(L.sorted_tuple(seed))
        dq = deque([seed])
        while dq:
            t = dq.popleft()
            vs = orient[t]
            for k in range(3):
                u, v = vs[k], vs[(k + 1) % 3]
                e = frozenset((u, v))
                for s in tri_neighbours[e]:
                    if s == t:
                        continue
                    w = next(x for x in s if x not in e)
                    # s must get orientation with edge (v,u)
                    want = (v, u, w)
                    if s in orient:
                        got = orient[s]
                        assert _same_cyclic(got, want), "not orientable"
                    else:
                        orient[s] = want
                        dq.append(s)
    log("orientable: OK")

    # phi0 is a simplicial automorphism of order 2
    assert all(phi0[phi0[v]] == v for v in phi0), "phi0 not an involution"
    assert set(phi0) == set(L.vertices()), "phi0 domain mismatch"
    for t in L.simplices[2]:
        img = frozenset(phi0[v] for v in t)
        assert img in L.simplices[2], f"phi0 not simplicial on {t}"
    fixed = [v for v in phi0 if phi0[v] == v]
    assert sorted(fixed) == ['O', 'p'], f"Fix(phi0) = {fixed}, want p, O"
    log("phi0: simplicial involution, Fix = {p, O}: OK")

    # curves: chordless cycles, phi0-equivariance
    for name, cyc in curves.items():
        k = len(cyc)
        assert len(set(cyc)) == k, f"curve {name} revisits a vertex"
        for i in range(k):
            assert frozenset((cyc[i], cyc[(i + 1) % k])) in L.simplices[1], \
                f"curve {name} not an edge cycle at {i}"
        chords = [(i, j) for i in range(k) for j in range(i + 2, k)
                  if (i, j) != (0, k - 1)
                  and frozenset((cyc[i], cyc[j])) in L.simplices[1]]
        assert not chords, f"curve {name} has chords: {chords[:4]}"
    log("curves a,b,c,d,e: chordless edge cycles: OK")

    pair = {'a': 'e', 'e': 'a', 'b': 'd', 'd': 'b', 'c': 'c'}
    for name, cyc in curves.items():
        img = {phi0[v] for v in cyc}
        assert img == set(curves[pair[name]]), f"phi0({name}) != {pair[name]}"
    assert all(phi0[v] != v for v in curves['c']), "phi0 not free on c"
    log("phi0-equivariance of the chain (a<->e, b<->d, c->c free): OK")

    # intersection pattern of the five-chain
    names = ['a', 'b', 'c', 'd', 'e']
    inter = {}
    for i, n1 in enumerate(names):
        for n2 in names[i + 1:]:
            common = set(curves[n1]) & set(curves[n2])
            inter[(n1, n2)] = len(common)
    want = {('a', 'b'): 1, ('b', 'c'): 1, ('c', 'd'): 1, ('d', 'e'): 1}
    for k, v in inter.items():
        assert v == want.get(k, 0), f"intersection {k}: got {v}, want {want.get(k, 0)}"
    log("five-chain intersection pattern:", inter, ": OK")

    # transversality at each crossing: the two curve directions interleave in
    # the vertex link
    for (n1, n2), cnt in want.items():
        v = next(iter(set(curves[n1]) & set(curves[n2])))
        _check_transverse(L, curves[n1], curves[n2], v)
    log("crossings transverse: OK")

    # complement of the chain = 2 discs containing p and O
    chain = set().union(*curves.values())
    rest = L.induced(set(L.vertices()) - chain)
    comps = _components(rest)
    assert len(comps) == 2, f"complement has {len(comps)} components"
    for comp in comps:
        sub = L.induced(comp)
        f = sub.f_vector()
        chi_c = f[0] - f[1] + (f[2] if len(f) > 2 else 0)
        assert chi_c == 1, f"complement component chi = {chi_c}, want 1 (disc)"
    assert ('p' in comps[0]) != ('p' in comps[1])
    log("complement of five-chain: two discs, p and O separated: OK")
    return True


def _same_cyclic(a, b):
    return b in (a, (a[1], a[2], a[0]), (a[2], a[0], a[1]))


def _components(C):
    verts = C.vertices()
    nbr = defaultdict(set)
    for e in C.simplices[1]:
        u, v = tuple(e)
        nbr[u].add(v)
        nbr[v].add(u)
    seen = set()
    comps = []
    for v in verts:
        if v in seen:
            continue
        comp = {v}
        stack = [v]
        while stack:
            x = stack.pop()
            for y in nbr[x]:
                if y not in comp:
                    comp.add(y)
                    stack.append(y)
        seen |= comp
        comps.append(comp)
    return comps


def _check_transverse(L, cyc1, cyc2, v):
    """At shared vertex v the four arc-ends of the two curves must interleave
    in the link circle of v."""
    star = [t for t in L.simplices[2] if v in t]
    link_edges = [tuple(sorted(t - {v}, key=str)) for t in star]
    nbr = defaultdict(list)
    for a, b in link_edges:
        nbr[a].append(b)
        nbr[b].append(a)
    start = link_edges[0][0]
    cycle = [start]
    prev = None
    while True:
        cand = [w for w in nbr[cycle[-1]] if w != prev]
        w = cand[0]
        if w == start:
            break
        prev = cycle[-1]
        cycle.append(w)
    def ends(cyc):
        k = len(cyc)
        i = cyc.index(v)
        return {cyc[(i - 1) % k], cyc[(i + 1) % k]}
    e1, e2 = ends(cyc1), ends(cyc2)
    pos = {w: i for i, w in enumerate(cycle)}
    p1 = sorted(pos[w] for w in e1)
    p2 = sorted(pos[w] for w in e2)
    # interleaving: exactly one of p2 lies strictly between p1
    between = sum(1 for q in p2 if p1[0] < q < p1[1])
    assert between == 1, f"curves not transverse at {v}"


# global helper used inside check (populated per-call)
ec_triangles = None
tri_neighbours = None


def _prep_neighbours(L):
    global tri_neighbours
    tri_neighbours = defaultdict(list)
    for t in L.simplices[2]:
        vs = L.sorted_tuple(t)
        for e in ((vs[0], vs[1]), (vs[0], vs[2]), (vs[1], vs[2])):
            tri_neighbours[frozenset(e)].append(t)


if __name__ == '__main__':
    F = build_fiber()
    _prep_neighbours(F['L'])
    check_fiber(F)
    print("fiber: ALL CHECKS PASS")
