"""Fundamental group of a simplicial complex from its 2-skeleton."""
from collections import deque


class Presentation:
    """pi_1(K, base) with generators = edges outside a spanning tree."""

    def __init__(self, K, base):
        self.K = K
        self.base = base
        verts = K.vertices()
        adj = {v: [] for v in verts}
        for e in K.simplices[1]:
            u, v = K.sorted_tuple(e)
            adj[u].append(v)
            adj[v].append(u)
        # BFS spanning tree
        parent = {base: None}
        dq = deque([base])
        while dq:
            u = dq.popleft()
            for w in adj[u]:
                if w not in parent:
                    parent[w] = u
                    dq.append(w)
        assert len(parent) == len(verts), "complex not connected"
        self.parent = parent
        tree = set()
        for w, u in parent.items():
            if u is not None:
                tree.add(frozenset((u, w)))
        self.tree = tree
        # generators: non-tree edges, oriented from lower to higher rank
        self.gens = {}
        for e in K.simplices[1]:
            if e not in tree:
                self.gens[e] = len(self.gens) + 1
        self.ngens = len(self.gens)
        # relators from 2-simplices: boundary (a,b),(b,c),(a,c)^-1
        self.relators = []
        for t in K.simplices[2]:
            a, b, c = K.sorted_tuple(t)
            w = self.edge_word(a, b) + self.edge_word(b, c) + self.edge_word(c, a)
            w = free_reduce(w)
            if w:
                self.relators.append(w)

    def edge_word(self, u, v):
        """Word (list of signed generator indices) for traversing edge u->v."""
        if u == v:
            return []
        e = frozenset((u, v))
        if e in self.tree:
            return []
        g = self.gens[e]
        lo, hi = self.K.sorted_tuple(e)
        return [g] if (u, v) == (lo, hi) else [-g]

    def path_word(self, path):
        """Word of an edge path (list of vertices, consecutive equal allowed)."""
        w = []
        for u, v in zip(path, path[1:]):
            w += self.edge_word(u, v)
        return free_reduce(w)

    def loop_word(self, path):
        """Word of a closed edge path, conjugated back to the basepoint via the
        spanning tree (tree paths contribute the empty word, so the word is just
        the path word provided the loop is based at any vertex)."""
        assert path[0] == path[-1]
        return self.path_word(path)

    # -- GAP export -------------------------------------------------------
    def gap_word(self, w):
        if not w:
            return "One(F)"
        return "*".join(f"F.{abs(g)}" + ("^-1" if g < 0 else "") for g in w)

    def gap_setup(self, name="G"):
        lines = [f"F := FreeGroup({self.ngens});;"]
        rels = ",\n".join(self.gap_word(r) for r in self.relators)
        lines.append(f"rels := [\n{rels}\n];;")
        lines.append(f"{name} := F/rels;;")
        return "\n".join(lines)


def free_reduce(w):
    out = []
    for g in w:
        if out and out[-1] == -g:
            out.pop()
        else:
            out.append(g)
    return out


def inverse(w):
    return [-g for g in reversed(w)]
