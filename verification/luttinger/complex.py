"""
Minimal finite simplicial-complex toolkit.

Vertices are arbitrary hashable objects.  A Complex carries a total order on its
vertices (needed for the staircase product) and the full set of simplices,
stored as frozensets, indexed by dimension.
"""
from itertools import combinations
from collections import defaultdict, deque


class Complex:
    def __init__(self, maximal, order=None):
        """maximal: iterable of iterables of vertices (maximal simplices).
        order: list giving the total order on vertices (default: sorted)."""
        maximal = [frozenset(s) for s in maximal]
        verts = set()
        for s in maximal:
            verts |= s
        if order is None:
            order = sorted(verts)
        self.order = list(order)
        self.rank = {v: i for i, v in enumerate(self.order)}
        assert verts <= set(self.order), "order must contain all vertices"
        self.simplices = defaultdict(set)   # dim -> set of frozensets
        for s in maximal:
            for k in range(1, len(s) + 1):
                for f in combinations(sorted(s, key=self.rank.get), k):
                    self.simplices[k - 1].add(frozenset(f))
        self.dim = max(self.simplices) if self.simplices else -1

    # -- basic accessors -------------------------------------------------
    def vertices(self):
        return [next(iter(s)) for s in self.simplices[0]]

    def skeleton(self, k):
        return self.simplices[k]

    def __contains__(self, s):
        s = frozenset(s)
        return s in self.simplices[len(s) - 1]

    def all_simplices(self):
        for k in sorted(self.simplices):
            yield from self.simplices[k]

    def sorted_tuple(self, s):
        return tuple(sorted(s, key=self.rank.get))

    def f_vector(self):
        return [len(self.simplices[k]) for k in sorted(self.simplices)]

    def orientation_signs(self, dimension=None):
        """Orient every top-dimensional pseudomanifold component.

        Signs are relative to this complex's vertex order. Shared facets get
        opposite induced orientations; boundary facets are allowed.
        """
        d = self.dim if dimension is None else dimension
        top = self.simplices[d]
        incidence = defaultdict(list)
        ordered = {}
        for simplex in top:
            vs = self.sorted_tuple(simplex)
            ordered[simplex] = vs
            for i in range(d + 1):
                incidence[frozenset(vs[:i] + vs[i + 1:])].append((simplex, i))
        assert all(len(items) <= 2 for items in incidence.values()), \
            "top-dimensional complex is not a pseudomanifold"

        signs = {}
        for seed in sorted(top, key=lambda s: tuple(map(repr, self.sorted_tuple(s)))):
            if seed in signs:
                continue
            signs[seed] = 1
            queue = deque([seed])
            while queue:
                simplex = queue.popleft()
                vs = ordered[simplex]
                for i in range(d + 1):
                    face = frozenset(vs[:i] + vs[i + 1:])
                    for neighbour, j in incidence[face]:
                        if neighbour == simplex:
                            continue
                        want = -signs[simplex] * (-1 if (i - j) % 2 else 1)
                        if neighbour in signs:
                            assert signs[neighbour] == want, \
                                "top-dimensional complex is not orientable"
                        else:
                            signs[neighbour] = want
                            queue.append(neighbour)
        return signs

    # -- derived complexes -----------------------------------------------
    def induced(self, vertex_subset):
        """Full subcomplex spanned by a set of vertices."""
        vs = set(vertex_subset)
        top = [s for s in self.all_simplices() if s <= vs]
        return Complex(top, order=[v for v in self.order if v in vs])

    def is_full(self, sub):
        """Is the subcomplex `sub` full in self?"""
        vs = set(sub.vertices())
        for s in self.all_simplices():
            if s <= vs and s not in sub:
                return False
        return True

    def cofaces(self, s, k):
        """k-simplices of self containing s."""
        s = frozenset(s)
        return [t for t in self.simplices[k] if s <= t]

    def link_cycle(self, s):
        """For a codimension-2 simplex s in a PL manifold: the link is a
        circle; return it as a cyclic list alternating (cod-1, top) simplices
        containing s:  t0, T0, t1, T1, ... with t_i < T_i > t_{i+1}."""
        s = frozenset(s)
        d = self.dim
        cod1 = self.cofaces(s, d - 1)
        top = self.cofaces(s, d)
        # each top simplex contains exactly two cod1 cofaces of s
        adj = defaultdict(list)
        for T in top:
            ts = [t for t in cod1 if t <= T]
            assert len(ts) == 2, (s, T, ts)
            adj[ts[0]].append((T, ts[1]))
            adj[ts[1]].append((T, ts[0]))
        # walk the cycle
        start = cod1[0]
        cyc = [start]
        prevT = None
        cur = start
        while True:
            nxt = [(T, t) for (T, t) in adj[cur] if T is not prevT and T != prevT]
            if prevT is None:
                T, t = adj[cur][0]
            else:
                cand = [(T, t) for (T, t) in adj[cur] if T != prevT]
                assert len(cand) == 1, "link not a circle"
                T, t = cand[0]
            cyc.append(T)
            if t == start:
                break
            cyc.append(t)
            cur, prevT = t, T
        assert len(cyc) == 2 * len(top) == 2 * len(cod1), "link is not a single circle"
        return cyc


def product(K, L):
    """Staircase (ordered) triangulation of |K| x |L|.
    Vertices are pairs (u, v); order is lexicographic in (rank_K, rank_L)."""
    order = [(u, v) for u in K.order for v in L.order]
    maximal = []
    topK = max(K.simplices)
    topL = max(L.simplices)
    # use ALL simplices of K and L as sources (faces are regenerated anyway);
    # maximal products suffice:
    for s in K.simplices[topK]:
        st = K.sorted_tuple(s)
        for t in L.simplices[topL]:
            tt = L.sorted_tuple(t)
            p, q = len(st), len(tt)
            # monotone lattice paths from (0,0) to (p-1,q-1)
            def paths(i, j, acc):
                if i == p - 1 and j == q - 1:
                    maximal.append(acc + [(st[i], tt[j])])
                    return
                if i < p - 1:
                    paths(i + 1, j, acc + [(st[i], tt[j])])
                if j < q - 1:
                    paths(i, j + 1, acc + [(st[i], tt[j])])
            paths(0, 0, [])
    return Complex(maximal, order=order)


def grid_torus(n=3):
    """Standard n x n grid triangulation of the torus (n>=3 gives a genuine
    simplicial complex).  Vertices (i,j) mod n."""
    tri = []
    for i in range(n):
        for j in range(n):
            a, b, c, d = (i, j), ((i + 1) % n, j), ((i + 1) % n, (j + 1) % n), (i, (j + 1) % n)
            tri.append([a, b, c])
            tri.append([a, d, c])
    order = [(i, j) for i in range(n) for j in range(n)]
    return Complex(tri, order=order)


def cycle_complex(vertices):
    """The simplicial circle on the given cyclic list of vertices."""
    n = len(vertices)
    return Complex([[vertices[i], vertices[(i + 1) % n]] for i in range(n)], order=list(vertices))
