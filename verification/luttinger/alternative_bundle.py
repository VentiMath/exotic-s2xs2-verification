#!/usr/bin/env python3
"""Alternative triangulation of the marked surface bundle R.

This module deliberately does not import bundle.py, layers.py, or the product
constructor from complex.py.  It starts from the separately certified marked
fiber and rebuilds the alpha mapping torus, beta Dehn-twist trace, thickened
base pieces, seams, and surgery tori.

The old beta trace performs four vertex-disjoint flips per interface.  This
builder splits each such batch into pairs, giving twice as many interfaces and
a genuinely different triangulation of the same PL twist cobordism.
"""

from __future__ import annotations

from collections import defaultdict

from complex import Complex
from fiber import K_BAND, build_fiber


def _triangles(surface):
    return {frozenset(triangle) for triangle in surface.simplices[2]}


def _prism_trace(triangles, rank, lower, upper):
    """Triangulate surface x I directly by three tetrahedra per triangle."""
    cells = []
    for triangle in sorted(triangles,
                           key=lambda t: tuple(map(repr, sorted(t, key=rank)))):
        vertices = sorted(triangle, key=rank)
        bottom = [lower(vertex) for vertex in vertices]
        top = [upper(vertex) for vertex in vertices]
        cells.extend([
            (bottom[0], top[0], top[1], top[2]),
            (bottom[0], bottom[1], top[1], top[2]),
            (bottom[0], bottom[1], bottom[2], top[2]),
        ])
    return cells


def _shuffle_product(left, right):
    """Independent staircase product implementation on maximal simplices."""
    maximal = []
    left_dim, right_dim = left.dim, right.dim
    for sigma in sorted(left.simplices[left_dim],
                        key=lambda s: tuple(map(repr, left.sorted_tuple(s)))):
        xs = left.sorted_tuple(sigma)
        for tau in sorted(right.simplices[right_dim],
                          key=lambda s: tuple(map(repr, right.sorted_tuple(s)))):
            ys = right.sorted_tuple(tau)

            def extend(i, j, path):
                if i == len(xs) - 1 and j == len(ys) - 1:
                    maximal.append(path + [(xs[i], ys[j])])
                    return
                if j < len(ys) - 1:
                    extend(i, j + 1, path + [(xs[i], ys[j])])
                if i < len(xs) - 1:
                    extend(i + 1, j, path + [(xs[i], ys[j])])

            # The tie-breaking order is deliberately opposite to the helper
            # in complex.product.  It gives the same staircase subdivision as
            # a set, while being an independent enumeration.
            extend(0, 0, [])
    order = [(x, y) for x in left.order for y in right.order]
    return Complex(maximal, order=order)


def _flip(triangles, edge):
    edge = frozenset(edge)
    incident = [triangle for triangle in triangles if edge < triangle]
    if len(incident) != 2:
        raise AssertionError("flip edge is not interior")
    a, b = tuple(edge)
    c = next(iter(incident[0] - edge))
    d = next(iter(incident[1] - edge))
    if c == d or any({c, d} <= triangle for triangle in triangles):
        raise AssertionError("flip target diagonal already exists")
    updated = set(triangles) - set(incident)
    updated.add(frozenset((a, c, d)))
    updated.add(frozenset((b, c, d)))
    return updated, (a, b, c, d)


def _vertical_square(u, v, rank, lower, upper):
    lo, hi = sorted((u, v), key=rank)
    return [
        (lower(lo), upper(lo), upper(hi)),
        (lower(lo), lower(hi), upper(hi)),
    ]


def _paired_flip_trace(before, quads, rank, lower, upper, cone_tag):
    """Trace one or two disjoint flips by coning each quadrilateral sphere."""
    after = set(before)
    removed = set()
    used_vertices = set()
    for a, b, c, d in quads:
        if used_vertices & {a, b, c, d}:
            raise AssertionError("alternative flip pair is not disjoint")
        used_vertices |= {a, b, c, d}
        floor = {frozenset((a, b, c)), frozenset((a, b, d))}
        if not floor <= after:
            raise AssertionError("alternative flip floor is absent")
        after -= floor
        removed |= floor
        after |= {frozenset((a, c, d)), frozenset((b, c, d))}
    cells = _prism_trace(before - removed, rank, lower, upper)
    for number, (a, b, c, d) in enumerate(quads):
        cone = (cone_tag, number)
        sphere = [
            (lower(a), lower(b), lower(c)),
            (lower(a), lower(b), lower(d)),
            (upper(a), upper(c), upper(d)),
            (upper(b), upper(c), upper(d)),
        ]
        for u, v in ((a, c), (a, d), (b, c), (b, d)):
            sphere.extend(_vertical_square(u, v, rank, lower, upper))
        cells.extend((cone,) + triangle for triangle in sphere)
    return cells, after


def _curve_neighbours(triangles, core, rail_vertex):
    neighbours = set()
    for triangle in triangles:
        if rail_vertex in triangle:
            neighbours |= triangle & core
    return neighbours - {rail_vertex}


def _trailing_edges(triangles, curve, rail, direction):
    positions = {vertex: i for i, vertex in enumerate(curve)}
    core = set(curve)
    selected = []
    for rail_vertex in rail:
        neighbours = list(_curve_neighbours(triangles, core, rail_vertex))
        if len(neighbours) != 2:
            raise AssertionError("rail vertex does not see two core vertices")
        first, second = neighbours
        i, j = positions[first], positions[second]
        if (j - i) % len(curve) == 1:
            trailing = first if direction == 1 else second
        elif (i - j) % len(curve) == 1:
            trailing = second if direction == 1 else first
        else:
            raise AssertionError("core neighbours are not cyclically adjacent")
        selected.append(frozenset((rail_vertex, trailing)))
    # The parity classes are disjoint.  Split each into two smaller groups;
    # this is the deliberate triangulation change relative to layers.py.
    groups = []
    for parity_class in (selected[0::2], selected[1::2]):
        midpoint = len(parity_class) // 2
        groups.extend((parity_class[:midpoint], parity_class[midpoint:]))
    return [group for group in groups if group]


def _twist_trace(base_triangles, curve, rail, direction, rank,
                 cells, level, vertex_name):
    current = set(base_triangles)
    for _ in range(len(curve)):
        for edges in _trailing_edges(current, curve, rail, direction):
            quads = []
            changed = current
            for edge in edges:
                changed, quad = _flip(changed, edge)
                quads.append(quad)
            lower = lambda vertex, at=level: vertex_name(at, vertex)
            upper = lambda vertex, at=level: vertex_name(at + 1, vertex)
            trace, checked = _paired_flip_trace(
                current, quads, rank, lower, upper,
                ("ALT_CONE", level))
            if checked != changed:
                raise AssertionError("flip trace roof disagrees with direct flip")
            cells.extend(trace)
            current = changed
            level += 1
    if current != set(base_triangles):
        raise AssertionError("alternative shear did not close")
    return level


def _build_beta_stack(fiber, directions=(1, -1)):
    surface, V = fiber["L"], fiber["V"]
    rank = surface.rank.get
    base = _triangles(surface)
    cells = []
    vertex_name = lambda level, vertex: ("S", level, vertex)
    specifications = [
        ([V("b", 0, i) for i in range(K_BAND["b"])],
         [V("b", 1, i) for i in range(K_BAND["b"])], directions[0]),
        ([V("a", 0, i) for i in range(K_BAND["a"])],
         [V("a", 1, i) for i in range(K_BAND["a"])], directions[1]),
    ]
    level = 0
    for curve, rail, direction in specifications:
        level = _twist_trace(base, curve, rail, direction, rank,
                             cells, level, vertex_name)
    vertices = {vertex for cell in cells for vertex in cell}

    def order_key(vertex):
        if vertex[0] == "S":
            return vertex[1], 0, rank(vertex[2])
        # (("ALT_CONE", level), number)
        return vertex[0][1], 1, vertex[1]

    return Complex(cells, order=sorted(vertices, key=order_key)), level


def build_alternative_bundle():
    fiber = build_fiber()
    surface, phi = fiber["L"], fiber["phi0"]
    rank = surface.rank.get
    triangles = _triangles(surface)

    # Alpha mapping torus, independently assembled from three prism traces.
    alpha_cells = []
    for time in range(2):
        alpha_cells.extend(_prism_trace(
            triangles, rank,
            lambda vertex, time=time: ("A", time, vertex),
            lambda vertex, time=time: ("A", time + 1, vertex)))
    alpha_cells.extend(_prism_trace(
        triangles, rank,
        lambda vertex: ("A", 2, vertex),
        lambda vertex: ("A", 0, phi[vertex])))
    alpha_vertices = {vertex for cell in alpha_cells for vertex in cell}
    alpha = Complex(alpha_cells, order=sorted(
        alpha_vertices, key=lambda vertex: (vertex[1], rank(vertex[2]))))

    radial = Complex([[("J", 0), ("J", 1)],
                      [("J", 1), ("J", 2)]],
                     order=[("J", 0), ("J", 1), ("J", 2)])
    alpha_thickening = _shuffle_product(alpha, radial)

    stack, levels = _build_beta_stack(fiber)
    transverse = Complex([[("t", 0), ("t", 1)],
                          [("t", 1), ("t", 2)]],
                         order=[("t", 0), ("t", 1), ("t", 2)])
    beta_thickening = _shuffle_product(stack, transverse)

    def seam(vertex):
        stack_vertex, transverse_vertex = vertex
        if (isinstance(stack_vertex, tuple) and len(stack_vertex) == 3 and
                stack_vertex[0] == "S"):
            if stack_vertex[1] == 0:
                return (("A", transverse_vertex[1], stack_vertex[2]), ("J", 2))
            if stack_vertex[1] == levels:
                return (("A", transverse_vertex[1], stack_vertex[2]), ("J", 0))
        return vertex

    cells = [alpha_thickening.sorted_tuple(simplex)
             for simplex in alpha_thickening.simplices[4]]
    cells.extend(tuple(seam(vertex) for vertex in
                       beta_thickening.sorted_tuple(simplex))
                 for simplex in beta_thickening.simplices[4])
    vertices = {vertex for cell in cells for vertex in cell}
    total = Complex(cells, order=sorted(vertices, key=repr))

    c = [fiber["V"]("c", 0, i) for i in range(K_BAND["c"])]
    e = [fiber["V"]("e", 0, i) for i in range(K_BAND["e"])]
    c_rail = [fiber["V"]("c", 1, i) for i in range(K_BAND["c"])]
    e_rail = [fiber["V"]("e", 1, i) for i in range(K_BAND["e"])]
    alpha_torus = [(("A", time, vertex), ("J", 1))
                   for time in range(3) for vertex in c]
    beta_torus = [(('S', level, vertex), ('t', 1))
                  for level in range(1, levels) for vertex in e]
    beta_torus.extend((("A", 1, vertex), ("J", radial_level))
                      for radial_level in range(3) for vertex in e)
    return {
        "K": total, "F": fiber, "L": surface, "V": fiber["V"],
        "phi0": phi, "m": levels, "c": c, "e": e,
        "c_rail": c_rail, "e_rail": e_rail,
        "Ta_verts": alpha_torus, "Tb_verts": beta_torus,
        "_beta_stack": stack,
        "alternative": {
            "beta_interfaces": levels,
            "flip_batch_size": 2,
            "forbidden_imports": ["bundle", "layers", "complex.product"],
        },
    }


def check_alternative_bundle(bundle):
    K = bundle["K"]
    if K.dim != 4:
        raise AssertionError("alternative total space is not 4-dimensional")
    torus_sets = [set(bundle["Ta_verts"]), set(bundle["Tb_verts"])]
    if torus_sets[0] & torus_sets[1]:
        raise AssertionError("alternative surgery tori intersect")
    records = []
    for vertices in torus_sets:
        triangles = {triangle for triangle in K.simplices[2]
                     if triangle <= vertices}
        edges = {edge for edge in K.simplices[1] if edge <= vertices}
        degrees = defaultdict(int)
        for triangle in triangles:
            ordered = tuple(triangle)
            for i in range(3):
                degrees[frozenset((ordered[i], ordered[(i + 1) % 3]))] += 1
        if set(degrees) != edges or any(degree != 2 for degree in degrees.values()):
            raise AssertionError("alternative marked torus is not closed")
        chi = len(vertices) - len(edges) + len(triangles)
        if chi != 0:
            raise AssertionError("alternative marked surface is not a torus")
        records.append([len(vertices), len(edges), len(triangles)])

    # Every tetrahedron incident to a torus is an interior face of exactly
    # two 4-simplices.
    marked = torus_sets[0] | torus_sets[1]
    incidence = defaultdict(int)
    for top in K.simplices[4]:
        if not top & marked:
            continue
        for omitted in top:
            face = top - {omitted}
            if face & marked:
                incidence[face] += 1
    near = [face for face in K.simplices[3] if face & marked]
    if any(incidence[face] != 2 for face in near):
        raise AssertionError("alternative total space is not a manifold near a torus")
    return {"K_f_vector": K.f_vector(), "torus_f_vectors": records,
            "beta_interfaces": bundle["m"],
            "beta_stack": check_beta_stack(bundle["_beta_stack"],
                                             bundle["m"], bundle["L"])}


def check_beta_stack(stack, levels, fiber):
    face_degree = defaultdict(int)
    for tetrahedron in stack.simplices[3]:
        for omitted in tetrahedron:
            face_degree[tetrahedron - {omitted}] += 1
    if any(degree not in (1, 2) for degree in face_degree.values()):
        raise AssertionError("alternative beta trace is not a 3-pseudomanifold")
    boundary = {face for face, degree in face_degree.items() if degree == 1}
    bottom = {frozenset(("S", 0, vertex) for vertex in triangle)
              for triangle in fiber.simplices[2]}
    top = {frozenset(("S", levels, vertex) for vertex in triangle)
           for triangle in fiber.simplices[2]}
    if boundary != bottom | top or bottom & top:
        raise AssertionError("beta trace boundary is not exactly two marked fibers")
    return {"f_vector": stack.f_vector(),
            "boundary_triangles": len(boundary),
            "bottom_top_markings": "PASS: exact labeled copies of L"}


if __name__ == "__main__":
    print("building alternative marked bundle...", flush=True)
    alternative = build_alternative_bundle()
    print(check_alternative_bundle(alternative))
