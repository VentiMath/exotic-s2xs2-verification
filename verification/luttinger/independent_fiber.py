#!/usr/bin/env python3
"""Independent ribbon-graph realization of the marked genus-2 fiber.

This construction does not import ``fiber.py``.  It starts from the abstract
ordered five-chain graph, thickens its specified rotation system by explicit
triangulated vertex disks and edge bands, and caps the two boundary circles.
The marked curves are literal core edge paths and the chain-reversing
involution is an explicit simplicial permutation.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from itertools import combinations

from complex import Complex


EDGE_ENDPOINTS = {
    "a0": ("v0", "qa"), "a1": ("qa", "v0"),
    "b0": ("v0", "v1"), "b1": ("v1", "v0"),
    "c0": ("v1", "v2"), "c1": ("v2", "v1"),
    "d0": ("v2", "v3"), "d1": ("v3", "v2"),
    "e0": ("v3", "qe"), "e1": ("qe", "v3"),
}

ROTATIONS = {
    "v0": ["a0+", "b0+", "a1-", "b1-"],
    "qa": ["a0-", "a1+"],
    "v1": ["b0-", "c0+", "b1+", "c1-"],
    "v2": ["c0-", "d0+", "c1+", "d1-"],
    "v3": ["d0-", "e0+", "d1+", "e1-"],
    "qe": ["e0-", "e1+"],
}

CURVE_EDGES = {
    "a": ["a0", "a1"], "b": ["b0", "b1"],
    "c": ["c0", "c1"], "d": ["d0", "d1"],
    "e": ["e0", "e1"],
}


def _dart_data():
    opposite, origin = {}, {}
    for edge, (lower, upper) in EDGE_ENDPOINTS.items():
        opposite[edge + "+"] = edge + "-"
        opposite[edge + "-"] = edge + "+"
        origin[edge + "+"] = lower
        origin[edge + "-"] = upper
    return opposite, origin


def _boundary_cycles(triangles):
    degrees = Counter()
    for triangle in triangles:
        degrees.update(frozenset(edge) for edge in combinations(triangle, 2))
    boundary = {edge for edge, degree in degrees.items() if degree == 1}
    adjacency = defaultdict(list)
    for edge in boundary:
        u, v = tuple(edge)
        adjacency[u].append(v)
        adjacency[v].append(u)
    if any(len(neighbours) != 2 for neighbours in adjacency.values()):
        raise AssertionError("ribbon neighborhood boundary is not a 1-manifold")
    for neighbours in adjacency.values():
        neighbours.sort(key=repr)
    unused = set(boundary)
    cycles = []
    while unused:
        first = min(unused, key=lambda edge: tuple(sorted(map(repr, edge))))
        start, current = sorted(first, key=repr)
        cycle = [start, current]
        unused.remove(first)
        previous = start
        while current != start:
            following = next(vertex for vertex in adjacency[current]
                             if vertex != previous)
            edge = frozenset((current, following))
            if edge not in unused:
                if following != start:
                    raise AssertionError("boundary cycle repeats before closing")
                current = following
                break
            unused.remove(edge)
            cycle.append(following)
            previous, current = current, following
        cycles.append(cycle[:-1])
    cycles.sort(key=lambda cycle: tuple(map(repr, cycle)))
    return cycles


def build_independent_fiber():
    opposite, origin = _dart_data()
    triangles = []

    # A coned polygonal disk at each graph vertex.  The alternating attachment
    # and connector triangles encode the ribbon rotation without band plumbing.
    for graph_vertex, darts in ROTATIONS.items():
        center = ("V", graph_vertex)
        for index, dart in enumerate(darts):
            following = darts[(index + 1) % len(darts)]
            triangles.append((center, ("D", dart, "L"), ("D", dart, "R")))
            triangles.append((center, ("D", dart, "R"),
                              ("D", following, "L")))

    # Each graph edge is a rectangular band, coned from its own center.  The
    # cross-order at the far end is what makes the total thickening orientable.
    for edge in EDGE_ENDPOINTS:
        dart, reverse = edge + "+", edge + "-"
        center = ("E", edge)
        boundary = [
            ("D", dart, "L"), ("D", dart, "R"),
            ("D", reverse, "L"), ("D", reverse, "R"),
        ]
        for index in range(4):
            triangles.append((center, boundary[index],
                              boundary[(index + 1) % 4]))

    boundary_cycles = _boundary_cycles(triangles)
    if len(boundary_cycles) != 2:
        raise AssertionError("five-chain ribbon graph must have two faces")
    for face, cycle in zip(("p", "O"), boundary_cycles):
        for index in range(len(cycle)):
            triangles.append((face, cycle[index], cycle[(index + 1) % len(cycle)]))

    vertices = {vertex for triangle in triangles for vertex in triangle}
    surface = Complex(triangles, order=sorted(vertices, key=repr))

    graph_vertex_map = {
        "v0": "v3", "v3": "v0", "v1": "v2", "v2": "v1",
        "qa": "qe", "qe": "qa",
    }
    edge_map = {
        "a0": "e1", "a1": "e0", "e0": "a1", "e1": "a0",
        "b0": "d0", "b1": "d1", "d0": "b0", "d1": "b1",
        "c0": "c1", "c1": "c0",
    }
    dart_map = {}
    for dart in opposite:
        target_edge = edge_map[dart[:-1]]
        target_origin = graph_vertex_map[origin[dart]]
        dart_map[dart] = (target_edge + "+"
                          if EDGE_ENDPOINTS[target_edge][0] == target_origin
                          else target_edge + "-")
    involution = {}
    for vertex in surface.vertices():
        if vertex[0] == "V":
            involution[vertex] = ("V", graph_vertex_map[vertex[1]])
        elif vertex[0] == "E":
            involution[vertex] = ("E", edge_map[vertex[1]])
        elif vertex[0] == "D":
            involution[vertex] = ("D", dart_map[vertex[1]], vertex[2])
        else:
            involution[vertex] = vertex

    def core_curve(name):
        first, second = CURVE_EDGES[name]
        d0, r0 = first + "+", first + "-"
        d1, r1 = second + "+", second + "-"
        if name in ("a", "e"):
            return [
                ("V", origin[d0]), ("D", d0, "L"), ("D", r0, "R"),
                ("D", d1, "L"), ("D", r1, "R"),
            ]
        return [
            ("V", origin[d0]), ("D", d0, "L"), ("D", r0, "R"),
            ("V", origin[r0]), ("D", d1, "L"), ("D", r1, "R"),
        ]

    curves = {name: core_curve(name) for name in ("a", "b", "c")}
    curves["d"] = [involution[vertex] for vertex in curves["b"]]
    curves["e"] = [involution[vertex] for vertex in curves["a"]]

    return {
        "L": surface, "curves": curves, "phi0": involution,
        "boundary_cycles": boundary_cycles,
        "construction": "abstract five-chain ribbon graph",
    }


def _components(complex_):
    adjacency = defaultdict(set)
    for edge in complex_.simplices[1]:
        u, v = tuple(edge)
        adjacency[u].add(v)
        adjacency[v].add(u)
    unseen = set(complex_.vertices())
    components = []
    while unseen:
        start = min(unseen, key=repr)
        component = {start}
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for neighbour in adjacency[vertex]:
                if neighbour not in component:
                    component.add(neighbour)
                    queue.append(neighbour)
        unseen -= component
        components.append(component)
    return components


def disk_signature(complex_):
    triangles = set(complex_.simplices[2])
    edge_degrees = Counter()
    for triangle in triangles:
        edge_degrees.update(frozenset(edge) for edge in combinations(triangle, 2))
    if set(edge_degrees) != complex_.simplices[1]:
        raise AssertionError("disk candidate has an edge outside its triangles")
    if any(degree not in (1, 2) for degree in edge_degrees.values()):
        raise AssertionError("disk candidate is not a 2-pseudomanifold")
    boundary = {edge for edge, degree in edge_degrees.items() if degree == 1}
    boundary_degrees = Counter(vertex for edge in boundary for vertex in edge)
    if not boundary or any(degree != 2 for degree in boundary_degrees.values()):
        raise AssertionError("disk candidate boundary is not circular")
    boundary_adjacency = defaultdict(set)
    for edge in boundary:
        u, v = tuple(edge)
        boundary_adjacency[u].add(v)
        boundary_adjacency[v].add(u)
    reached = {min(boundary_adjacency, key=repr)}
    queue = deque(reached)
    while queue:
        vertex = queue.popleft()
        for neighbour in boundary_adjacency[vertex]:
            if neighbour not in reached:
                reached.add(neighbour)
                queue.append(neighbour)
    if reached != set(boundary_adjacency):
        raise AssertionError("disk candidate has multiple boundary components")
    for vertex in complex_.vertices():
        link_edges = {triangle - {vertex} for triangle in triangles
                      if vertex in triangle}
        link_degrees = Counter(point for edge in link_edges for point in edge)
        if vertex in boundary_degrees:
            if sum(degree == 1 for degree in link_degrees.values()) != 2 or \
                    any(degree not in (1, 2) for degree in link_degrees.values()):
                raise AssertionError("disk boundary vertex link is not an interval")
        elif any(degree != 2 for degree in link_degrees.values()):
            raise AssertionError("disk interior vertex link is not a circle")
    vector = complex_.f_vector()
    chi = sum((-1) ** index * count for index, count in enumerate(vector))
    if chi != 1:
        raise AssertionError("disk candidate does not have Euler characteristic one")
    return {"f_vector": vector, "boundary_edges": len(boundary), "chi": chi}


def check_independent_fiber(fiber):
    surface, curves, involution = fiber["L"], fiber["curves"], fiber["phi0"]
    f_vector = surface.f_vector()
    if f_vector != [58, 180, 120]:
        raise AssertionError(f"unexpected independent fiber f-vector {f_vector}")
    if f_vector[0] - f_vector[1] + f_vector[2] != -2:
        raise AssertionError("independent fiber is not genus two")
    edge_degrees = Counter()
    for triangle in surface.simplices[2]:
        edge_degrees.update(frozenset(edge) for edge in combinations(triangle, 2))
    if set(edge_degrees.values()) != {2}:
        raise AssertionError("independent fiber is not closed")
    surface.orientation_signs()
    for vertex in surface.vertices():
        link_edges = {triangle - {vertex} for triangle in surface.simplices[2]
                      if vertex in triangle}
        link_degrees = Counter(point for edge in link_edges for point in edge)
        if any(degree != 2 for degree in link_degrees.values()):
            raise AssertionError("independent fiber has a singular vertex link")
        adjacency = defaultdict(set)
        for edge in link_edges:
            u, v = tuple(edge)
            adjacency[u].add(v)
            adjacency[v].add(u)
        reached = {min(adjacency, key=repr)}
        queue = deque(reached)
        while queue:
            point = queue.popleft()
            for neighbour in adjacency[point]:
                if neighbour not in reached:
                    reached.add(neighbour)
                    queue.append(neighbour)
        if reached != set(adjacency):
            raise AssertionError("independent fiber vertex link is disconnected")

    for name, curve in curves.items():
        if len(curve) != len(set(curve)):
            raise AssertionError(f"independent {name} revisits a vertex")
        curve_edges = {frozenset((curve[index], curve[(index + 1) % len(curve)]))
                       for index in range(len(curve))}
        if not curve_edges <= surface.simplices[1]:
            raise AssertionError(f"independent {name} is not an edge cycle")
        induced_edges = {edge for edge in surface.simplices[1]
                         if edge <= set(curve)}
        if induced_edges != curve_edges:
            raise AssertionError(f"independent {name} has a chord")
    intersections = {}
    for i, first in enumerate("abcde"):
        for second in "abcde"[i + 1:]:
            intersections[first + second] = len(set(curves[first]) &
                                                 set(curves[second]))
    expected = {"ab": 1, "bc": 1, "cd": 1, "de": 1}
    if any(value != expected.get(pair, 0)
           for pair, value in intersections.items()):
        raise AssertionError("independent curves are not the ordered five-chain")

    chain = set().union(*(set(curve) for curve in curves.values()))
    complement = surface.induced(set(surface.vertices()) - chain)
    components = _components(complement)
    if len(components) != 2:
        raise AssertionError("independent five-chain does not fill in two disks")
    disk_data = []
    for component in components:
        subcomplex = surface.induced(component)
        vector = subcomplex.f_vector()
        chi = sum((-1) ** index * count for index, count in enumerate(vector))
        if chi != 1:
            raise AssertionError("induced face interior does not have chi one")
        fixed_point = next(point for point in ("p", "O") if point in component)
        cap = Complex([triangle for triangle in surface.simplices[2]
                       if fixed_point in triangle],
                      order=[vertex for vertex in surface.order
                             if vertex == fixed_point or any(
                                 vertex in triangle and fixed_point in triangle
                                 for triangle in surface.simplices[2])])
        signature = {"f_vector": vector, "chi": chi,
                     "cap_disk": disk_signature(cap),
                     "fixed_point": fixed_point}
        disk_data.append(signature)
    if {item["fixed_point"] for item in disk_data} != {"p", "O"}:
        raise AssertionError("p and O do not lie in distinct complementary disks")

    if set(involution) != set(surface.vertices()):
        raise AssertionError("independent involution has the wrong domain")
    if any(involution[involution[vertex]] != vertex for vertex in involution):
        raise AssertionError("independent involution is not order two")
    if any(frozenset(involution[vertex] for vertex in triangle)
           not in surface.simplices[2] for triangle in surface.simplices[2]):
        raise AssertionError("independent involution is not simplicial")
    fixed = sorted((vertex for vertex in involution
                    if involution[vertex] == vertex), key=repr)
    if fixed != ["O", "p"]:
        raise AssertionError(f"independent involution fixed set is {fixed}")
    pairs = {"a": "e", "e": "a", "b": "d", "d": "b", "c": "c"}
    for name, target in pairs.items():
        if {involution[vertex] for vertex in curves[name]} != set(curves[target]):
            raise AssertionError(f"independent involution does not send {name} to {target}")
    if any(involution[vertex] == vertex for vertex in curves["c"]):
        raise AssertionError("independent involution is not free on c")
    return {
        "f_vector": f_vector,
        "chi": -2,
        "curve_lengths": {name: len(curve) for name, curve in curves.items()},
        "intersections": intersections,
        "complement_disks": sorted(disk_data, key=lambda item: item["fixed_point"]),
        "involution_fixed_set": fixed,
        "involution_chain_action": "a<->e, b<->d, c->c freely",
    }


if __name__ == "__main__":
    independent = build_independent_fiber()
    print(check_independent_fiber(independent))
