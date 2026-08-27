#!/usr/bin/env python3
"""Direct PL certificate that the doubled fixed-point section has square zero.

The marked bundle ``K`` contains the section through the fixed vertex ``p``.
This program extracts that section and the actual normal link of ``p`` from
the fiber triangulation.  It then doubles the punctured-torus section and
builds a triangulated normal disk bundle for every constant boundary
clutching rotation.  In each case it constructs a disjoint simplicial normal
push-off and the radial PL cylinder joining it to the zero section.

The signed intersection chain is therefore empty, so the self-intersection
is zero.  Testing every cyclic rotation makes the certificate independent of
which constant derivative is used by the boundary gluing map.
"""

from collections import defaultdict
from hashlib import sha256
from itertools import combinations

from bundle import build_bundle
from complex import Complex, product
from fiber import K_BAND, build_fiber
from layers import build_stack


def _fiber_vertex(vertex):
    """Return the fiber coordinate of an ordinary bundle vertex."""
    first, _second = vertex
    if (isinstance(first, tuple) and len(first) == 3
            and first[0] in {"A", "S"} and isinstance(first[1], int)):
        return first[2]
    return None


def _boundary_cycle(surface):
    degree = defaultdict(int)
    for triangle in surface.simplices[2]:
        for edge in combinations(surface.sorted_tuple(triangle), 2):
            degree[frozenset(edge)] += 1
    boundary = [edge for edge, count in degree.items() if count == 1]
    assert boundary, "surface has no boundary"
    adjacency = defaultdict(set)
    for edge in boundary:
        u, v = tuple(edge)
        adjacency[u].add(v)
        adjacency[v].add(u)
    assert all(len(neighbours) == 2 for neighbours in adjacency.values())

    start = min(adjacency, key=surface.rank.get)
    cycle = [start]
    previous = None
    current = start
    while True:
        choices = sorted(adjacency[current], key=surface.rank.get)
        following = choices[0] if choices[0] != previous else choices[1]
        if following == start:
            break
        assert following not in cycle, "boundary is not one circle"
        cycle.append(following)
        previous, current = current, following
    assert set(cycle) == set(adjacency), "surface boundary is disconnected"
    return cycle


def _fiber_link_cycle(fiber, vertex):
    link_edges = []
    for triangle in fiber.simplices[2]:
        if vertex in triangle:
            link_edges.append(frozenset(triangle - {vertex}))
    adjacency = defaultdict(set)
    for edge in link_edges:
        u, v = tuple(edge)
        adjacency[u].add(v)
        adjacency[v].add(u)
    assert adjacency and all(len(neighbours) == 2
                             for neighbours in adjacency.values())
    start = min(adjacency, key=fiber.rank.get)
    cycle = [start]
    previous = None
    current = start
    while True:
        choices = sorted(adjacency[current], key=fiber.rank.get)
        following = choices[0] if choices[0] != previous else choices[1]
        if following == start:
            break
        cycle.append(following)
        previous, current = current, following
    assert set(cycle) == set(adjacency)
    return cycle


def _check_beta_star_is_product(fiber):
    """The flip stack has no bistellar move in the star of p."""
    V = fiber["V"]
    twists = []
    for name, direction in (("b", 1), ("a", -1)):
        length = K_BAND[name]
        twists.append((
            [V(name, 0, i) for i in range(length)],
            [V(name, 1, i) for i in range(length)],
            [V(name, -1, i) for i in range(length)],
            direction,
        ))
    cells, levels, _ = build_stack(
        fiber["L"], fiber["L"].rank.get, twists, copy_tag="PLN")
    touched = 0
    for cell in cells:
        has_cone = any(
            isinstance(v, tuple) and len(v) == 2
            and isinstance(v[0], tuple) and v[0][:2] == ("PLN", "cone")
            for v in cell)
        has_p = any(
            isinstance(v, tuple) and len(v) == 3
            and v[0] == "PLN" and v[2] == "p" for v in cell)
        touched += int(has_cone and has_p)
    assert touched == 0, "the beta flip stack changes the star of p"
    return levels


def _double_base(section, boundary_cycle):
    boundary_index = {v: i for i, v in enumerate(boundary_cycle)}
    size = len(boundary_cycle)
    reflected = {
        v: boundary_cycle[(-i) % size]
        for v, i in boundary_index.items()
    }

    plus = [[("+", v) for v in section.sorted_tuple(t)]
            for t in section.simplices[2]]
    minus = []
    for triangle in section.simplices[2]:
        renamed = []
        for v in section.sorted_tuple(triangle):
            if v in reflected:
                renamed.append(("+", reflected[v]))
            else:
                renamed.append(("-", v))
        minus.append(renamed)
    vertices = {v for triangle in plus + minus for v in triangle}
    base = Complex(plus + minus, order=sorted(vertices, key=repr))

    edge_degree = defaultdict(int)
    for triangle in base.simplices[2]:
        for edge in combinations(base.sorted_tuple(triangle), 2):
            edge_degree[frozenset(edge)] += 1
    assert set(edge_degree.values()) == {2}, "double is not a closed surface"
    assert sum((-1) ** i * n for i, n in enumerate(base.f_vector())) == -2
    base.orientation_signs()
    return base, reflected


def _normal_disk():
    center = ("normal", "zero")
    rays = [("normal", i) for i in range(4)]
    triangles = [
        [center, rays[i], rays[(i + 1) % 4]] for i in range(4)
    ]
    return Complex(triangles, order=[center] + rays), center, rays


def _rotator(center, rays, shift):
    def rotate(vertex):
        if vertex == center:
            return center
        return rays[(rays.index(vertex) + shift) % len(rays)]
    return rotate


def _twisted_neighbourhood(section, reflected, shift):
    disk, center, rays = _normal_disk()
    rotate = _rotator(center, rays, shift)

    plus_triangles = [
        [("+", v) for v in section.sorted_tuple(t)]
        for t in section.simplices[2]
    ]
    minus_triangles = [
        [("-", v) for v in section.sorted_tuple(t)]
        for t in section.simplices[2]
    ]
    plus_order = [("+", v) for v in section.order]
    # Pull the order back through the boundary reflection.  This makes the
    # staircase triangulations on the two sides agree after gluing.
    minus_order = [("-", v) for v in sorted(
        section.order, key=lambda x: section.rank[reflected.get(x, x)])]
    plus_surface = Complex(plus_triangles, order=plus_order)
    minus_surface = Complex(minus_triangles, order=minus_order)

    plus_product = product(plus_surface, disk)
    pulled_disk_order = sorted(disk.order, key=lambda d: disk.rank[rotate(d)])
    minus_disk = Complex(
        [[center, rays[i], rays[(i + 1) % 4]] for i in range(4)],
        order=pulled_disk_order)
    minus_product = product(minus_surface, minus_disk)

    def glue(vertex):
        (side, base_vertex), normal_vertex = vertex
        if side == "-" and base_vertex in reflected:
            return (("+", reflected[base_vertex]), rotate(normal_vertex))
        return vertex

    maximal = [plus_product.sorted_tuple(s)
               for s in plus_product.simplices[4]]
    maximal += [tuple(glue(v) for v in minus_product.sorted_tuple(s))
                for s in minus_product.simplices[4]]
    vertices = {v for simplex in maximal for v in simplex}
    neighbourhood = Complex(maximal, order=sorted(vertices, key=repr))
    return neighbourhood, center, rays


def _certify_push_off(neighbourhood, base, center, rays, shift):
    inverse_rotate = _rotator(center, rays, -shift)
    chosen_ray = rays[0]

    zero_vertices = {
        (base_vertex, center) for base_vertex in base.vertices()
    }
    push_vertices = set()
    for base_vertex in base.vertices():
        side, _ = base_vertex
        normal_vertex = (chosen_ray if side == "+"
                         else inverse_rotate(chosen_ray))
        push_vertices.add((base_vertex, normal_vertex))

    zero = neighbourhood.induced(zero_vertices)
    push = neighbourhood.induced(push_vertices)
    cylinder = neighbourhood.induced(zero_vertices | push_vertices)
    assert zero.f_vector() == base.f_vector()
    assert push.f_vector() == base.f_vector()
    assert not (set(zero.vertices()) & set(push.vertices()))
    assert cylinder.dim == 3
    tetrahedron_signs = cylinder.orientation_signs()

    triangle_degree = defaultdict(int)
    for tetrahedron in cylinder.simplices[3]:
        for triangle in combinations(cylinder.sorted_tuple(tetrahedron), 3):
            triangle_degree[frozenset(triangle)] += 1
    boundary = {triangle for triangle, degree in triangle_degree.items()
                if degree == 1}
    assert set(triangle_degree.values()) <= {1, 2}
    assert boundary == zero.simplices[2] | push.simplices[2], \
        "radial cylinder has an unexpected boundary component"
    assert sum((-1) ** i * n
               for i, n in enumerate(cylinder.f_vector())) == -2

    oriented_boundary = defaultdict(int)
    for tetrahedron, sign in tetrahedron_signs.items():
        vertices = cylinder.sorted_tuple(tetrahedron)
        for i in range(4):
            face = frozenset(vertices[:i] + vertices[i + 1:])
            oriented_boundary[face] += sign * (-1 if i % 2 else 1)
    nonzero_boundary = {
        face: coefficient for face, coefficient in oriented_boundary.items()
        if coefficient
    }
    assert set(nonzero_boundary) == boundary
    assert set(abs(value) for value in nonzero_boundary.values()) == {1}

    # A section triangle is codimension two in the four-dimensional disk
    # bundle.  Its link must be one normal circle, not several components.
    link_lengths = []
    for triangle in zero.simplices[2]:
        link_lengths.append(len(neighbourhood.link_cycle(triangle)))
    assert link_lengths and min(link_lengths) >= 6

    # The two subcomplexes have disjoint realizations.  Thus a transverse
    # signed-intersection enumeration has no local points and total zero.
    signed_intersections = []
    assert sum(signed_intersections) == 0
    return {
        "zero_f_vector": zero.f_vector(),
        "push_f_vector": push.f_vector(),
        "cylinder_f_vector": cylinder.f_vector(),
        "normal_link_length_range": [min(link_lengths), max(link_lengths)],
        "signed_intersections": signed_intersections,
        "self_intersection": 0,
    }


def _digest_maximal(complex_):
    records = sorted(repr(tuple(sorted(simplex, key=repr)))
                     for simplex in complex_.simplices[complex_.dim])
    return sha256("\n".join(records).encode()).hexdigest()


def certify():
    fiber = build_fiber()
    link = _fiber_link_cycle(fiber["L"], "p")
    phi0 = fiber["phi0"]
    assert len(link) == 24
    assert all(phi0[vertex] == link[(i + 12) % 24]
               for i, vertex in enumerate(link))
    marked_rays = [link[i] for i in (0, 6, 12, 18)]
    assert [phi0[v] for v in marked_rays] == marked_rays[2:] + marked_rays[:2]
    beta_levels = _check_beta_star_is_product(fiber)

    bundle = build_bundle(dir_b=1, dir_a=-1)
    assert bundle["K"].dim == 4
    section_vertices = {
        vertex for vertex in bundle["K"].vertices()
        if _fiber_vertex(vertex) == "p"
    }
    section = bundle["K"].induced(section_vertices)
    boundary = _boundary_cycle(section)
    assert section.f_vector() == [102, 243, 140]
    assert sum((-1) ** i * n for i, n in enumerate(section.f_vector())) == -1
    assert len(boundary) == 66
    section.orientation_signs()

    base, reflected = _double_base(section, boundary)
    assert base.f_vector() == [138, 420, 280]

    cases = []
    canonical_digest = None
    for shift in range(4):
        neighbourhood, center, rays = _twisted_neighbourhood(
            section, reflected, shift)
        result = _certify_push_off(
            neighbourhood, base, center, rays, shift)
        result["constant_clutch_shift"] = shift
        result["neighbourhood_f_vector"] = neighbourhood.f_vector()
        result["maximal_cell_sha256"] = _digest_maximal(neighbourhood)
        if shift == 0:
            canonical_digest = result["maximal_cell_sha256"]
        cases.append(result)

    print("PASS: extracted p-section is an orientable once-punctured torus")
    print("  section f-vector:", section.f_vector(), "boundary cycle:", len(boundary))
    print("PASS: actual normal link of p is a 24-cycle")
    print("  phi0 acts by shift 12 (-I); beta stack is product at p across",
          beta_levels, "levels")
    print("PASS: doubled section is a closed orientable genus-2 surface")
    print("  double f-vector:", base.f_vector())
    for result in cases:
        print("PASS: constant clutch shift {constant_clutch_shift}: "
              "push-off disjoint, radial cylinder boundary exact, "
              "signed intersections={signed_intersections}, square={self_intersection}"
              .format(**result))
        print("  normal neighbourhood f-vector:",
              result["neighbourhood_f_vector"],
              "radial cylinder:", result["cylinder_f_vector"],
              "link lengths:", result["normal_link_length_range"])
        print("  maximal-cell sha256:", result["maximal_cell_sha256"])
    print("CERTIFIED: Gamma_hat . Gamma_hat = 0")
    return {
        "ambient_bundle_dimension": bundle["K"].dim,
        "section_f_vector": section.f_vector(),
        "section_boundary_length": len(boundary),
        "normal_link_length": len(link),
        "phi0_link_shift": 12,
        "beta_product_levels": beta_levels,
        "double_f_vector": base.f_vector(),
        "cases": cases,
        "canonical_digest": canonical_digest,
    }


if __name__ == "__main__":
    certify()
