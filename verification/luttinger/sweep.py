"""Combinatorial certificates for basing-arc sweeps.

A sweep is supplied as a rectangular grid of vertices of K.  Its rows are
copies of a base loop and its columns follow the basing arc in the fiber.  The
certificate checks every grid edge in K and records incidences with the torus
components.  In the bundle R this formalizes the square in Wuebben section
8.5: one interior incidence with T_alpha and the last row on T_beta.

The grid alone determines the number and location of crossings.  Compatible
orientation signs propagated by ``Complex.orientation_signs`` determine the
oriented intersection sign and the orientation of every punctured boundary.
"""
from collections import defaultdict
from itertools import combinations


def certify_grid_sweep(K, rows, components, require_closed=True):
    """Validate a rectangular sweep and return component incidence records.

    ``rows`` is a nonempty list of equal-length closed vertex paths.  Adjacent
    rows must also be joined column by column by edges of K.  ``components``
    maps names to vertex sets.  Each returned hit is ``(row, column, vertex)``;
    the repeated closing column is omitted.
    """
    assert rows and len(rows) >= 2
    width = len(rows[0])
    assert width >= 2 and all(len(row) == width for row in rows)
    if require_closed:
        assert all(row[0] == row[-1] for row in rows), \
            "each sweep row must be a closed base loop"

    def edge(u, v):
        assert u == v or frozenset((u, v)) in K.simplices[1], \
            f"sweep is not simplicial at {u!r} -> {v!r}"

    for row in rows:
        for u, v in zip(row, row[1:]):
            edge(u, v)
    for i in range(len(rows) - 1):
        for j in range(width):
            edge(rows[i][j], rows[i + 1][j])

    hits = {}
    for name, vertices in components.items():
        vertices = set(vertices)
        hits[name] = [(i, j, v) for i, row in enumerate(rows)
                      for j, v in enumerate(
                          row[:-1] if require_closed else row)
                      if v in vertices]
    return hits


def _permutation_sign(order, canonical):
    pos = {v: i for i, v in enumerate(canonical)}
    perm = [pos[v] for v in order]
    inversions = sum(perm[i] > perm[j] for i in range(len(perm))
                     for j in range(i + 1, len(perm)))
    return -1 if inversions % 2 else 1


def grid_intersection_sign(K, rows, hit, target, ambient_signs, target_signs):
    """Compute the oriented sign of a transverse grid/target incidence."""
    i, j, z = hit
    assert 0 < i < len(rows) - 1 and 0 < j < len(rows[0]) - 1
    grid_triangles = []
    for ii in (i - 1, i):
        for jj in (j - 1, j):
            coords = [(ii, jj), (ii + 1, jj),
                      (ii, jj + 1), (ii + 1, jj + 1)]
            vertices = {rows[u][v]: (u, v) for u, v in coords}
            for tri in K.simplices[2]:
                if z not in tri or not tri <= set(vertices):
                    continue
                canonical = K.sorted_tuple(tri)
                xy = [vertices[v] for v in canonical]
                det = ((xy[1][0] - xy[0][0]) * (xy[2][1] - xy[0][1]) -
                       (xy[1][1] - xy[0][1]) * (xy[2][0] - xy[0][0]))
                if det:
                    grid_triangles.append((tri, 1 if det > 0 else -1))

    signs = set()
    target_vertices = set(target.vertices())
    for grid_tri, grid_sign in grid_triangles:
        if len(grid_tri & target_vertices) != 1:
            continue
        for target_tri in target.simplices[2]:
            if z not in target_tri or grid_tri & target_tri != {z}:
                continue
            top = grid_tri | target_tri
            if top not in K.simplices[4]:
                continue

            def positive_tangent(tri, sign, complex_):
                other = list(tri - {z})
                canonical = complex_.sorted_tuple(tri)
                if _permutation_sign((z, other[0], other[1]), canonical) != sign:
                    other.reverse()
                return other

            ga = positive_tangent(grid_tri, grid_sign, K)
            ta = positive_tangent(target_tri, target_signs[target_tri], target)
            order = (z, ga[0], ga[1], ta[0], ta[1])
            local = _permutation_sign(order, K.sorted_tuple(top))
            signs.add(1 if local == ambient_signs[top] else -1)

    assert len(signs) == 1, \
        f"grid/target incidence is not coherently transverse: signs={signs}"
    return signs.pop()


def punctured_grid_boundary_cycles(K, rows, removed_vertices):
    """Trace the oriented boundary after deleting stars of removed vertices.

    The grid orientation is (increasing row, increasing column).  Each grid
    quadrilateral inherits the diagonal present in K.  Triangles incident to a
    removed vertex are deleted, which is the simplicial complement of an open
    vertex star.  The returned cycles are directed closed edge paths in K.
    """
    # Keep parameter-triangle occurrences, rather than keying only by their
    # image simplex.  For an annulus represented by a rectangle whose first
    # and last rows have the same image, distinct domain triangles may map to
    # the same simplex with opposite orientations and must cancel as chains.
    oriented = []
    for i in range(len(rows) - 1):
        for j in range(len(rows[0]) - 1):
            coords = [(i, j), (i + 1, j),
                      (i, j + 1), (i + 1, j + 1)]
            xy = {rows[u][v]: (u, v) for u, v in coords}
            vertices = list(xy)
            cell_tris = []
            for triple in combinations(vertices, 3):
                tri = frozenset(triple)
                if len(tri) != 3 or tri not in K.simplices[2]:
                    continue
                canonical = K.sorted_tuple(tri)
                pts = [xy[v] for v in canonical]
                det = ((pts[1][0] - pts[0][0]) *
                       (pts[2][1] - pts[0][1]) -
                       (pts[1][1] - pts[0][1]) *
                       (pts[2][0] - pts[0][0]))
                if not det:
                    continue
                order = canonical if det > 0 else \
                    (canonical[0], canonical[2], canonical[1])
                oriented.append((tri, order))
                cell_tris.append(tri)
            assert len(set(cell_tris)) == 2, \
                f"grid cell ({i},{j}) does not contain exactly two triangles"

    removed_vertices = set(removed_vertices)
    coefficients = defaultdict(int)
    representatives = {}
    for tri, (a, b, c) in oriented:
        if tri & removed_vertices:
            continue
        for u, v in ((a, b), (b, c), (c, a)):
            edge = frozenset((u, v))
            canonical = K.sorted_tuple(edge)
            coefficients[edge] += 1 if (u, v) == canonical else -1
            representatives[edge] = canonical

    directed = []
    for edge, coefficient in coefficients.items():
        if coefficient == 0:
            continue
        assert abs(coefficient) == 1, \
            f"nonmanifold grid boundary coefficient {coefficient} on {edge}"
        u, v = representatives[edge]
        directed.append((u, v) if coefficient > 0 else (v, u))

    outgoing = defaultdict(list)
    incoming = defaultdict(list)
    for u, v in directed:
        outgoing[u].append(v)
        incoming[v].append(u)
    boundary_vertices = set(outgoing) | set(incoming)
    assert all(len(outgoing[v]) == len(incoming[v]) == 1
               for v in boundary_vertices), \
        "punctured grid boundary is not a union of oriented circles"

    unused = set(directed)
    cycles = []
    while unused:
        first = min(unused, key=lambda e: (repr(e[0]), repr(e[1])))
        start, current = first
        cycle = [start, current]
        unused.remove(first)
        while current != start:
            nxt = outgoing[current][0]
            assert (current, nxt) in unused
            unused.remove((current, nxt))
            cycle.append(nxt)
            current = nxt
        cycles.append(cycle)
    return cycles
