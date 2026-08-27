r"""
pi_1 of the complement of a full 2-dimensional subcomplex T (a torus) in a
triangulated closed 4-manifold K, together with based meridian/longitude words.

Rigorous basis (Rourke-Sanderson, ch. 3):
  * T full in K  =>  |K| - |T| deformation retracts onto C := induced
    subcomplex of K on V(K) \ V(T).
  * In the first derived K', the derived neighbourhood N(T) is a regular
    neighbourhood; its frontier  Ndot = { chains s0<...<sk of simplices of K,
    none in T, all meeting T }  is a triangulation of  d(nu T) = T^3.
  * r : C' -> C,  r(b(s)) = max-order vertex of s \ T, is a simplicial map
    homotopic to the retraction, hence an iso on pi_1.  We read all boundary
    loops in Ndot, push them to C through r, and compute in pi_1(C).
"""
from collections import deque
from complex import Complex
from pi1 import Presentation, free_reduce, inverse


class TorusComplement:
    def __init__(self, K, T):
        self.K, self.T = K, T
        assert K.is_full(T), "T must be a full subcomplex of K"
        self.Tverts = set(T.vertices())
        self.C = K.induced(set(K.vertices()) - self.Tverts)
        # vertices of Ndot: simplices of K not in T but meeting T
        self.N = [s for s in K.all_simplices() if (s & self.Tverts) and s not in T]
        self.Nset = set(self.N)

    # -- the retraction to C ----------------------------------------------
    def r(self, s):
        return max((v for v in s if v not in self.Tverts), key=self.K.rank.get)

    # -- paths inside Ndot --------------------------------------------------
    def n_adjacent(self, s, t):
        return s < t or t < s

    def bfs_in_N(self, start, goal, allowed=None):
        """Shortest path in the 1-skeleton of Ndot from start to goal, using
        only vertices (simplices) in `allowed` (default: all of Ndot)."""
        pool = list(allowed) if allowed is not None else self.N
        pool = [s for s in pool if s in self.Nset]
        prev = {start: None}
        dq = deque([start])
        while dq:
            s = dq.popleft()
            if s == goal:
                break
            for t in pool:
                if t not in prev and self.n_adjacent(s, t):
                    prev[t] = s
                    dq.append(t)
        assert goal in prev, "no path in Ndot"
        path = [goal]
        while prev[path[-1]] is not None:
            path.append(prev[path[-1]])
        return path[::-1]

    # -- the meridian -----------------------------------------------------
    def meridian_loop(self, sigma):
        """Boundary of the dual 2-cell of the 2-simplex sigma of T, as a loop
        in Ndot (alternating 3- and 4-simplices containing sigma)."""
        cyc = self.K.link_cycle(sigma)
        for s in cyc:
            assert s in self.Nset
        return cyc + [cyc[0]]

    def oriented_meridian_loop(self, sigma, ambient_signs, torus_signs):
        """Dual meridian oriented by compatible orientations of K and T."""
        sigma = frozenset(sigma)
        cyc = self.K.link_cycle(sigma)
        a = next(iter(cyc[0] - sigma))
        top = cyc[1]
        b = next(iter(cyc[2] - sigma))
        canonical_top = self.K.sorted_tuple(top)
        canonical_sigma = self.T.sorted_tuple(sigma)
        trial = canonical_sigma + (a, b)
        pos = {v: i for i, v in enumerate(canonical_top)}
        perm = [pos[v] for v in trial]
        inversions = sum(perm[i] > perm[j] for i in range(len(perm))
                         for j in range(i + 1, len(perm)))
        trial_sign = torus_signs[sigma] * (-1 if inversions % 2 else 1)
        if trial_sign != ambient_signs[top]:
            cyc = [cyc[0]] + list(reversed(cyc[1:]))
        for s in cyc:
            assert s in self.Nset
        return cyc + [cyc[0]]

    # -- push off a closed edge path of T into Ndot ------------------------
    def pushoff_loop(self, gamma, side):
        """gamma: closed edge path in T (list of vertices, first==last).
        side: function vertex_of_T -> vertex of K not in T, adjacent to it,
        giving the normal direction (constant 'side' of a product framing).
        Returns a loop in Ndot whose i-th corner is the edge {g_i, side(g_i)}."""
        corners = [frozenset((g, side(g))) for g in gamma]
        for c in corners:
            assert c in self.Nset, f"{c} not an edge of K meeting T"
        loop = [corners[0]]
        for (g0, g1), (c0, c1) in zip(zip(gamma, gamma[1:]), zip(corners, corners[1:])):
            if c0 == c1:
                continue
            square = {g0, g1, side(g0), side(g1)}
            allowed = [s for s in self.N if s <= square]
            seg = self.bfs_in_N(c0, c1, allowed)
            loop += seg[1:]
        assert loop[0] == loop[-1]
        return loop

    # -- words ---------------------------------------------------------------
    def to_C(self, nloop):
        return [self.r(s) for s in nloop]

    def presentation(self, base_simplex):
        self.base_simplex = base_simplex
        self.P = Presentation(self.C, self.r(base_simplex))
        return self.P

    def based_word(self, nloop, basing_path):
        """Word of  basing_path . nloop . basing_path^-1  (all in Ndot)."""
        assert basing_path[-1] == nloop[0] and nloop[0] == nloop[-1]
        full = basing_path + nloop[1:] + basing_path[::-1][1:]
        assert full[0] == full[-1] == self.base_simplex
        return self.P.loop_word(self.to_C(full))

    def rotate_loop_to_retraction(self, nloop, vertex):
        """Rotate a closed Ndot loop so that its image in C starts at vertex.

        This is useful when a punctured sweep approaches a meridian through a
        specified vertex of C.  Rotation changes the local basepoint but not
        the oriented loop.
        """
        assert nloop[0] == nloop[-1]
        body = nloop[:-1]
        positions = [i for i, s in enumerate(body) if self.r(s) == vertex]
        assert positions, f"loop never retracts to requested vertex {vertex}"
        i = positions[0]
        body = body[i:] + body[:i]
        return body + [body[0]]

    def based_word_via_C(self, nloop, basing_path):
        """Base an Ndot loop along an explicit edge path in C.

        Unlike :meth:`based_word`, the whisker is allowed to leave the
        boundary component.  This is the operation needed for a meridian
        created by puncturing a sweep whose other boundary lies on a different
        surgery torus.
        """
        assert nloop[0] == nloop[-1]
        assert basing_path[-1] == self.r(nloop[0])
        assert all(v in self.C.simplices[0] for v in
                   (frozenset((x,)) for x in basing_path))
        for u, v in zip(basing_path, basing_path[1:]):
            assert u == v or frozenset((u, v)) in self.C.simplices[1], \
                f"basing path is not an edge path in C at {u!r} -> {v!r}"
        loop = self.to_C(nloop)
        full = basing_path + loop[1:] + basing_path[::-1][1:]
        assert full[0] == full[-1]
        return self.P.loop_word(full)
