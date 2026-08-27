"""
Simplicial cobordism layers over a surface complex:

  * mapping cylinder of a simplicial isomorphism (prism cells
    [pi(x0)..pi(xi), xi..xk] over each source simplex) — realizes the map;
  * flip layer: prisms over untouched triangles + a cone over each flipped
    quadrilateral (several disjoint flips may share one layer) — realizes the
    identity while retriangulating;
  * Dehn twist about a band curve = k monotone shear rounds of ONE side band
    (k = curve length), closing with the identity relabel.  The two-band
    symmetric shear with a core rotation is the FINGER ROTATION, isotopic to
    the identity — the mapping-torus H1 unit test below distinguishes them
    (Z^2 Nil for the twist, Z^3 for identity) and pins the twist power to 1
    (H1 torsion Z/n would flag T^n).

All complexes here are lists of maximal simplices over hashable vertex names;
assembly into `Complex` happens at the end (bundle.py).
"""
from complex import Complex


def tri_list(L):
    return [L.sorted_tuple(t) for t in L.simplices[2]]


def flip(tris, edge):
    """Flip `edge` in the surface given by the triangle set `tris`
    (set of frozensets).  Returns (new_tris, quad) where quad = (a,b,c,d):
    old diagonal {a,b}, new diagonal {c,d}."""
    a, b = tuple(edge)
    cont = [t for t in tris if a in t and b in t]
    assert len(cont) == 2, f"edge {edge} not interior"
    t1, t2 = cont
    c = next(iter(t1 - {a, b}))
    d = next(iter(t2 - {a, b}))
    assert c != d
    new_diag = frozenset((c, d))
    assert not any(c in t and d in t for t in tris), \
        f"flip target diagonal {new_diag} already present"
    out = set(tris)
    out.discard(t1)
    out.discard(t2)
    out.add(frozenset((a, c, d)))
    out.add(frozenset((b, c, d)))
    return out, (a, b, c, d)


def prism_cells(triangles, rank, top, bottom):
    """Mapping-cylinder cells over the given triangles.
    top(v), bottom(v): naming maps for the two ends; `rank` orders the
    abstract fiber vertices (defines the staircase).  For a triangle
    [x0<x1<x2] the cells are [b0,t0,t1,t2],[b0,b1,t1,t2],[b0,b1,b2,t2]."""
    cells = []
    for t in triangles:
        xs = sorted(t, key=rank)
        bs = [bottom(v) for v in xs]
        ts = [top(v) for v in xs]
        for i in range(3):
            cells.append(tuple(bs[:i + 1]) + tuple(ts[i:]))
    return cells


def square_diag_tris(u, v, rank, top, bottom):
    """The two triangles of the vertical square over edge {u,v}, split by the
    staircase diagonal {bottom(min), top(max)} — must agree with prism faces."""
    lo, hi = sorted((u, v), key=rank)
    return [
        (bottom(lo), top(lo), top(hi)),
        (bottom(lo), bottom(hi), top(hi)),
    ]


def flip_layer_cells(pre_tris, flips, rank, top, bottom, cone_name):
    """One cobordism layer performing several DISJOINT flips at once.
    pre_tris: triangle set before the flips; flips: list of quads (a,b,c,d)
    (old diagonal {a,b} below, new diagonal {c,d} above).
    Returns (cells, post_tris)."""
    post = set(pre_tris)
    touched = set()
    for (a, b, c, d) in flips:
        t1, t2 = frozenset((a, b, c)), frozenset((a, b, d))
        assert t1 in post and t2 in post, "flip quad not present"
        assert not (touched & {a, b, c, d}), "flips in one layer must be disjoint"
        touched |= {a, b, c, d}
        post.discard(t1)
        post.discard(t2)
        post.add(frozenset((a, c, d)))
        post.add(frozenset((b, c, d)))
    quad_tris_below = {frozenset((a, b, c)) for (a, b, c, d) in flips} | \
                      {frozenset((a, b, d)) for (a, b, c, d) in flips}
    # only the two triangles of each quad are replaced; triangles that merely
    # share vertices with a quad keep their prisms.
    untouched = [t for t in pre_tris if t not in quad_tris_below]
    cells = prism_cells(untouched, rank, top, bottom)
    for qi, (a, b, c, d) in enumerate(flips):
        w = (cone_name, qi)
        # boundary sphere of the quad ball:
        btris = [
            (bottom(a), bottom(b), bottom(c)),   # floor
            (bottom(a), bottom(b), bottom(d)),
            (top(a), top(c), top(d)),            # roof
            (top(b), top(c), top(d)),
        ]
        for (u, v) in ((a, c), (a, d), (b, c), (b, d)):   # quad boundary edges
            btris += square_diag_tris(u, v, rank, top, bottom)
        for tri in btris:
            cells.append((w,) + tri)
    return cells, post


def rotate_relabel(curve, amount):
    """Permutation dict rotating the curve cycle by `amount` (identity
    elsewhere; callers extend with .get(v, v))."""
    k = len(curve)
    return {curve[i]: curve[(i + amount) % k] for i in range(k)}


def _curve_neighbours(tris, curve_set, rail_vertex):
    """The curve vertices sharing an edge with rail_vertex in `tris`."""
    out = set()
    for t in tris:
        if rail_vertex in t:
            out |= (t & curve_set) - {rail_vertex}
    return out


def _shear_round(tris, curve, rail, direction):
    """One full shear round of the band between `curve` and `rail`: for each
    rail vertex, flip its 'trailing' edge to the curve, advancing the band's
    winding one notch.  direction +1/-1 picks which of the two curve
    neighbours is trailing.  Returns two vertex-disjoint batches of edges."""
    k = len(curve)
    pos = {v: i for i, v in enumerate(curve)}
    curve_set = set(curve)
    edges = []
    for i in range(k):
        nb = _curve_neighbours(tris, curve_set, rail[i])
        assert len(nb) == 2, f"rail vertex {rail[i]} has {len(nb)} curve neighbours"
        n1, n2 = sorted(nb, key=lambda v: pos[v])
        # the two neighbours are cyclically adjacent on the curve; the
        # 'trailing' one (to flip) is behind in the +direction sense.
        j1, j2 = pos[n1], pos[n2]
        if (j2 - j1) % k == 1:
            lead, trail = (n2, n1) if direction == 1 else (n1, n2)
        elif (j1 - j2) % k == 1:
            lead, trail = (n1, n2) if direction == 1 else (n2, n1)
        else:
            raise AssertionError("band wound past adjacency — not a grid band")
        edges.append(frozenset((rail[i], trail)))
    return [edges[0::2], edges[1::2]]


def realize_twist(tris, curve, upper, lower, direction=1, rail='upper'):
    """Realize a Dehn twist about `curve` as k monotone shear rounds of ONE
    side band (the annulus between the curve and the chosen rail), closing
    with the identity relabel.  direction +1/-1 gives the two twist signs.
    Returns layers_of_quads (2k batches)."""
    the_rail = upper if rail == 'upper' else lower
    k = len(curve)
    cur = set(tris)
    layers = []
    for _round in range(k):
        for batch in _shear_round(cur, curve, the_rail, direction):
            quads = []
            for e in batch:
                cur, quad = flip(cur, e)
                quads.append(quad)
            layers.append(quads)
    assert cur == set(tris), "monotone shear did not close after k rounds"
    return layers


# ---------------------------------------------------------------------------
# unit test: mapping torus of one Dehn twist on the 4x4 grid torus.
# pi_1 = <x,y,t | [x,y]=1, t x t^-1 = x, t y t^-1 = y x^{+-1}> (Nil), whose
# abelianization is Z^2 (+ nothing), against Z^3 for the identity monodromy.
def _abelianization(P):
    """Smith normal form of the abelianized relation matrix -> invariant
    factors (list of d_i > 1 and number of zeros = free rank)."""
    rows = []
    for r in P.relators:
        v = {}
        for g in r:
            v[abs(g)] = v.get(abs(g), 0) + (1 if g > 0 else -1)
        rows.append([v.get(i + 1, 0) for i in range(P.ngens)])
    if not rows:
        return [], P.ngens
    M = [row[:] for row in rows]
    m, n = len(M), len(M[0])
    # simple SNF
    divisors = []
    top = 0
    left = 0
    while top < m and left < n:
        # find pivot: smallest nonzero |entry|
        piv = None
        for i in range(top, m):
            for j in range(left, n):
                if M[i][j] != 0 and (piv is None or abs(M[i][j]) < abs(M[piv[0]][piv[1]])):
                    piv = (i, j)
        if piv is None:
            break
        pi, pj = piv
        M[top], M[pi] = M[pi], M[top]
        for row in M:
            row[left], row[pj] = row[pj], row[left]
        again = True
        while again:
            again = False
            p = M[top][left]
            for i in range(top + 1, m):
                q = M[i][left] // p
                if q:
                    for j in range(left, n):
                        M[i][j] -= q * M[top][j]
                if M[i][left] != 0:
                    M[top], M[i] = M[i], M[top]
                    again = True
                    break
            if again:
                continue
            for j in range(left + 1, n):
                q = M[top][j] // p
                if q:
                    for i in range(top, m):
                        M[i][j] -= q * M[i][left]
                if M[top][j] != 0:
                    for i in range(top, m):
                        M[i][left], M[i][j] = M[i][j], M[i][left]
                    again = True
                    break
        divisors.append(abs(M[top][left]))
        top += 1
        left += 1
    free_rank = n - len([d for d in divisors if d != 0])
    torsion = [d for d in divisors if d not in (0, 1)]
    return torsion, free_rank


def build_stack(L_complex, rank, twists, copy_tag='S'):
    """Stack of layers over the fiber realizing the composite of the given
    twists (first entry applied first).  twists: list of
    (curve, upper, lower, want_rel) with want_rel in {+1,-1,None}.
    Returns (cells, n_copies, copyname): copyname(i, v) names fiber copy i;
    copies 0..n are the interfaces (copy 0 = bottom, copy n = top; both
    carry the base triangulation)."""
    base_tris = {frozenset(t) for t in tri_list(L_complex)}
    cells = []
    level = 0
    cur_tris = base_tris

    def name(i, v):
        return (copy_tag, i, v)

    for (curve, upper, lower, direction) in twists:
        assert cur_tris == base_tris, "each twist starts from the base triangulation"
        layers = realize_twist(cur_tris, curve, upper, lower, direction)
        for quads in layers:
            top = lambda v, i=level: name(i + 1, v)
            bottom = lambda v, i=level: name(i, v)
            layer_cells, cur_tris = flip_layer_cells(
                cur_tris, quads, rank, top, bottom, (copy_tag, 'cone', level))
            cells += layer_cells
            level += 1
        assert cur_tris == base_tris
    return cells, level, name


# ---------------------------------------------------------------------------
if __name__ == '__main__':
    from complex import grid_torus
    from pi1 import Presentation

    n = 4
    T = grid_torus(n)
    rank = T.rank.get
    curve = [(i, 0) for i in range(n)]          # row cycle
    upper = [(i, 1) for i in range(n)]
    lower = [(i, n - 1) for i in range(n)]
    cells, m, name = build_stack(T, rank, [(curve, upper, lower, 1)])
    # close into the mapping torus: identify copy m with copy 0
    def squash(v):
        if isinstance(v, tuple) and len(v) == 3 and v[0] == 'S' and v[1] == m:
            return ('S', 0, v[2])
        return v
    closed = [tuple(squash(v) for v in c) for c in cells]
    MT = Complex(closed, order=sorted({v for c in closed for v in c}, key=str))
    print("mapping torus f-vector:", MT.f_vector())
    P = Presentation(MT, next(iter(MT.vertices())))
    tors, rank_free = _abelianization(P)
    print("H1 =", "Z^%d" % rank_free, "+", tors)
    assert (tors, rank_free) == ([], 2), \
        "twist mapping torus must have H1 = Z^2 (Nil), got Z^%d + %s" % (rank_free, tors)
    # control: identity monodromy (3 product layers, closed up) -> T^3, H1 = Z^3
    cells3 = []
    for i in range(3):
        cells3 += prism_cells([frozenset(t) for t in
                               [T.sorted_tuple(s) for s in T.simplices[2]]],
                              rank,
                              lambda v, i=i: ('S', (i + 1) % 3, v),
                              lambda v, i=i: ('S', i, v))
    MT3 = Complex(cells3, order=sorted({v for c in cells3 for v in c}, key=str))
    P3 = Presentation(MT3, next(iter(MT3.vertices())))
    tors3, free3 = _abelianization(P3)
    print("control (identity monodromy): H1 = Z^%d + %s" % (free3, tors3))
    assert (tors3, free3) == ([], 3)
    print("layers: twist mapping torus unit test PASS")

