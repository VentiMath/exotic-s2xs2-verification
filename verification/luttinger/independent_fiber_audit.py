#!/usr/bin/env python3
"""Compare an independent ribbon-graph fiber with ``fiber.py``'s model.

The comparison is subdivision-independent.  It extracts the oriented ribbon
system of the named filling five-chain, its two p/O face cycles, and the action
of the involution on every directed curve end.  A canonical search over the
five irrelevant curve orientations and global surface orientation supplies a
finite equivariant marked-ribbon equivalence certificate.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
from collections import Counter, defaultdict, deque
from itertools import combinations, product
from pathlib import Path

from complex import Complex
from fiber import build_fiber
from independent_fiber import (build_independent_fiber, check_independent_fiber,
                               disk_signature)


ROOT = Path(__file__).resolve().parent
CURVES = "abcde"


def _cycle_normal_form(cycle):
    cycle = tuple(cycle)
    return min(cycle[index:] + cycle[:index] for index in range(len(cycle)))


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


def _oriented_triangles(surface, reverse=False):
    output = {}
    for triangle, sign in surface.orientation_signs().items():
        ordered = list(surface.sorted_tuple(triangle))
        if sign < 0:
            ordered[1], ordered[2] = ordered[2], ordered[1]
        if reverse:
            ordered[1], ordered[2] = ordered[2], ordered[1]
        output[triangle] = tuple(ordered)
    return output


def _link_order(surface, oriented, vertex, selected):
    following = {}
    for triangle, order in oriented.items():
        if vertex not in triangle:
            continue
        index = order.index(vertex)
        following[order[(index + 1) % 3]] = order[(index + 2) % 3]
    start = min(following, key=repr)
    full = [start]
    current = following[start]
    while current != start:
        if current in full:
            raise AssertionError("surface vertex link repeats before closing")
        full.append(current)
        current = following[current]
    chosen = [neighbour for neighbour in full if neighbour in selected]
    if set(chosen) != set(selected):
        raise AssertionError("marked directions are absent from a vertex link")
    return chosen


def _curve_edges(curves):
    return {
        frozenset((curve[index], curve[(index + 1) % len(curve)]))
        for curve in curves.values() for index in range(len(curve))
    }


def _full_face_labels(surface, curves, oriented):
    chain = set().union(*(set(curve) for curve in curves.values()))
    graph_edges = _curve_edges(curves)
    neighbours = defaultdict(set)
    for edge in graph_edges:
        u, v = tuple(edge)
        neighbours[u].add(v)
        neighbours[v].add(u)

    rotation = {}
    for vertex in chain:
        order = _link_order(surface, oriented, vertex, neighbours[vertex])
        for index, neighbour in enumerate(order):
            # Predecessor gives the boundary cycle on the oriented left side.
            rotation[(vertex, neighbour)] = (
                vertex, order[(index - 1) % len(order)])
    darts = {(u, v) for edge in graph_edges for u, v in
             (tuple(edge), tuple(reversed(tuple(edge))))}
    successor = {(u, v): rotation[(v, u)] for u, v in darts}
    unseen = set(darts)
    face_cycles = []
    while unseen:
        start = min(unseen, key=lambda dart: (repr(dart[0]), repr(dart[1])))
        cycle, current = [], start
        while current in unseen:
            unseen.remove(current)
            cycle.append(current)
            current = successor[current]
        if current != start:
            raise AssertionError("ribbon boundary does not close")
        face_cycles.append(cycle)
    if len(face_cycles) != 2:
        raise AssertionError("filling chain ribbon graph does not have two faces")

    complement = surface.induced(set(surface.vertices()) - chain)
    components = _components(complement)
    if len(components) != 2:
        raise AssertionError("marked chain complement does not have two components")
    component_names = {}
    for index, component in enumerate(components):
        fixed = [point for point in ("p", "O") if point in component]
        if len(fixed) != 1:
            raise AssertionError("complement component lacks a unique p/O label")
        component_names[index] = fixed[0]

    dart_label = {}
    for cycle in face_cycles:
        labels = set()
        for u, v in cycle:
            for triangle, order in oriented.items():
                if u not in triangle or v not in triangle:
                    continue
                index = order.index(u)
                if order[(index + 1) % 3] != v:
                    continue
                third = order[(index + 2) % 3]
                labels.update(component_names[number]
                              for number, component in enumerate(components)
                              if third in component)
        if len(labels) != 1:
            raise AssertionError(f"ribbon face has ambiguous disk label {labels}")
        label = next(iter(labels))
        for dart in cycle:
            dart_label[dart] = label
    return dart_label


def _descriptor(crossing, curve, sign):
    return f"{crossing}:{curve}:{sign}"


def _marked_ribbon_code(fiber, curve_reversals, surface_reverse):
    surface, involution = fiber["L"], fiber["phi0"]
    curves = {}
    for name, reverse in zip(CURVES, curve_reversals):
        cycle = list(fiber["curves"][name])
        curves[name] = list(reversed(cycle)) if reverse else cycle
    oriented = _oriented_triangles(surface, reverse=surface_reverse)
    face_labels = _full_face_labels(surface, curves, oriented)

    membership = defaultdict(list)
    for name, cycle in curves.items():
        for vertex in cycle:
            membership[vertex].append(name)
    crossings = {"".join(sorted(names)): vertex
                 for vertex, names in membership.items() if len(names) == 2}
    if set(crossings) != {"ab", "bc", "cd", "de"}:
        raise AssertionError("named chain has the wrong crossings")

    end_neighbour = {}
    reverse_lookup = {}
    alpha = {}
    segment_lengths = {}
    for name, cycle in curves.items():
        positions = sorted(index for index, vertex in enumerate(cycle)
                           if len(membership[vertex]) == 2)
        if len(positions) not in (1, 2):
            raise AssertionError(f"curve {name} has the wrong crossing count")
        lengths = []
        for number, position in enumerate(positions):
            crossing = "".join(sorted(membership[cycle[position]]))
            plus = _descriptor(crossing, name, "+")
            minus = _descriptor(crossing, name, "-")
            plus_neighbour = cycle[(position + 1) % len(cycle)]
            minus_neighbour = cycle[(position - 1) % len(cycle)]
            end_neighbour[plus] = (cycle[position], plus_neighbour)
            end_neighbour[minus] = (cycle[position], minus_neighbour)
            reverse_lookup[(cycle[position], plus_neighbour)] = plus
            reverse_lookup[(cycle[position], minus_neighbour)] = minus
            next_position = positions[(number + 1) % len(positions)]
            distance = (next_position - position) % len(cycle)
            if not distance:
                distance = len(cycle)
            next_crossing = "".join(sorted(membership[cycle[next_position]]))
            alpha[plus] = _descriptor(next_crossing, name, "-")
            alpha[_descriptor(next_crossing, name, "-")] = plus
            lengths.append(distance)
        segment_lengths[name] = tuple(sorted(lengths))

    rotations = {}
    sigma = {}
    for crossing, vertex in sorted(crossings.items()):
        selected = {neighbour for (base, neighbour), descriptor in
                    reverse_lookup.items() if base == vertex}
        link = _link_order(surface, oriented, vertex, selected)
        order = [reverse_lookup[(vertex, neighbour)] for neighbour in link]
        rotations[crossing] = _cycle_normal_form(order)
        for index, descriptor in enumerate(order):
            sigma[descriptor] = order[(index - 1) % len(order)]

    face_successor = {descriptor: sigma[alpha[descriptor]]
                      for descriptor in alpha}
    unseen = set(face_successor)
    reduced_faces = {}
    while unseen:
        start = min(unseen)
        cycle, current = [], start
        while current in unseen:
            unseen.remove(current)
            cycle.append(current)
            current = face_successor[current]
        if current != start:
            raise AssertionError("reduced ribbon face does not close")
        labels = {face_labels[end_neighbour[descriptor]] for descriptor in cycle}
        if len(labels) != 1:
            raise AssertionError("reduced ribbon face changed p/O label")
        reduced_faces[next(iter(labels))] = _cycle_normal_form(cycle)
    if set(reduced_faces) != {"p", "O"}:
        raise AssertionError("reduced ribbon code does not distinguish p and O")

    involution_ends = {}
    for descriptor, (crossing_vertex, neighbour) in end_neighbour.items():
        image = (involution[crossing_vertex], involution[neighbour])
        if image not in reverse_lookup:
            raise AssertionError("involution does not preserve directed chain ends")
        involution_ends[descriptor] = reverse_lookup[image]
    if involution.get("p") != "p" or involution.get("O") != "O":
        raise AssertionError("involution does not fix the two named faces")

    code = (
        tuple((crossing, rotations[crossing]) for crossing in sorted(rotations)),
        tuple(sorted(alpha.items())),
        tuple(sorted(involution_ends.items())),
        tuple((face, reduced_faces[face]) for face in ("p", "O")),
    )
    return code, segment_lengths


def _canonical_code(fiber):
    candidates = []
    for reversals in product((False, True), repeat=5):
        for surface_reverse in (False, True):
            code, lengths = _marked_ribbon_code(
                fiber, reversals, surface_reverse)
            candidates.append((code, reversals, surface_reverse, lengths))
    return min(candidates, key=lambda candidate: candidate[0])


def _primary_structure(primary):
    surface, curves, involution = primary["L"], primary["curves"], primary["phi0"]
    f_vector = surface.f_vector()
    edge_degrees = Counter()
    for triangle in surface.simplices[2]:
        edge_degrees.update(frozenset(edge) for edge in combinations(triangle, 2))
    if set(edge_degrees.values()) != {2}:
        raise AssertionError("primary fiber is not closed")
    surface.orientation_signs()
    if f_vector[0] - f_vector[1] + f_vector[2] != -2:
        raise AssertionError("primary fiber is not genus two")
    for vertex in surface.vertices():
        link_edges = {triangle - {vertex} for triangle in surface.simplices[2]
                      if vertex in triangle}
        link_degrees = Counter(point for edge in link_edges for point in edge)
        if any(degree != 2 for degree in link_degrees.values()):
            raise AssertionError("primary fiber has a singular vertex link")
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
            raise AssertionError("primary fiber vertex link is disconnected")
    for name, curve in curves.items():
        curve_edges = {
            frozenset((curve[index], curve[(index + 1) % len(curve)]))
            for index in range(len(curve))}
        if not curve_edges <= surface.simplices[1]:
            raise AssertionError(f"primary {name} is not an edge cycle")
        induced = {edge for edge in surface.simplices[1] if edge <= set(curve)}
        if induced != curve_edges:
            raise AssertionError(f"primary {name} has a chord")
    intersections = {}
    for index, first in enumerate(CURVES):
        for second in CURVES[index + 1:]:
            intersections[first + second] = len(set(curves[first]) & set(curves[second]))
    expected = {"ab": 1, "bc": 1, "cd": 1, "de": 1}
    if any(value != expected.get(pair, 0)
           for pair, value in intersections.items()):
        raise AssertionError("primary marked curves are not the ordered chain")
    chain = set().union(*(set(curve) for curve in curves.values()))
    complement = surface.induced(set(surface.vertices()) - chain)
    components = _components(complement)
    if len(components) != 2:
        raise AssertionError("primary chain complement does not have two disks")
    disks = []
    for component in components:
        subcomplex = surface.induced(component)
        vector = subcomplex.f_vector()
        chi = sum((-1) ** index * count for index, count in enumerate(vector))
        if chi != 1:
            raise AssertionError("primary induced face interior does not have chi one")
        fixed = [point for point in ("p", "O") if point in component]
        if len(fixed) != 1:
            raise AssertionError("primary complement disk lacks one fixed point")
        cap_triangles = [triangle for triangle in surface.simplices[2]
                         if fixed[0] in triangle]
        cap_vertices = {vertex for triangle in cap_triangles for vertex in triangle}
        cap = Complex(cap_triangles,
                      order=[vertex for vertex in surface.order
                             if vertex in cap_vertices])
        signature = {"f_vector": vector, "chi": chi,
                     "cap_disk": disk_signature(cap),
                     "fixed_point": fixed[0]}
        disks.append(signature)
    if sorted(vertex for vertex in involution if involution[vertex] == vertex) != ["O", "p"]:
        raise AssertionError("primary involution has the wrong fixed set")
    if set(involution) != set(surface.vertices()) or \
            any(involution[involution[vertex]] != vertex for vertex in involution):
        raise AssertionError("primary involution is not an order-two permutation")
    if any(frozenset(involution[vertex] for vertex in triangle)
           not in surface.simplices[2] for triangle in surface.simplices[2]):
        raise AssertionError("primary involution is not simplicial")
    return {"f_vector": f_vector,
            "chi": f_vector[0] - f_vector[1] + f_vector[2],
            "intersections": intersections,
            "complement_disks": sorted(disks,
                                       key=lambda item: item["fixed_point"])}


def _independence_audit():
    source = (ROOT / "independent_fiber.py").read_text(encoding="ascii")
    tree = ast.parse(source)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module)
    if "fiber" in imports:
        raise AssertionError("independent fiber imported the primary fiber module")
    return {"imports": sorted(imports), "fiber_module_absent": True}


def build_certificate():
    independent = build_independent_fiber()
    primary = build_fiber()
    independent_structure = check_independent_fiber(independent)
    primary_structure = _primary_structure(primary)
    independent_code, independent_orientations, independent_surface_reverse, independent_lengths = \
        _canonical_code(independent)
    primary_code, primary_orientations, primary_surface_reverse, primary_lengths = \
        _canonical_code(primary)
    if independent_code != primary_code:
        raise AssertionError("independent and primary marked ribbon systems differ")

    identity_variant = dict(independent)
    identity_variant["phi0"] = {vertex: vertex
                                for vertex in independent["L"].vertices()}
    identity_code = _canonical_code(identity_variant)[0]
    if identity_code == primary_code:
        raise AssertionError("identity-involution mutation was not detected")
    face_swap_variant = dict(independent)
    face_swap = dict(independent["phi0"])
    face_swap["p"], face_swap["O"] = "O", "p"
    face_swap_variant["phi0"] = face_swap
    try:
        _canonical_code(face_swap_variant)
    except AssertionError:
        pass
    else:
        raise AssertionError("p/O-swapping mutation was not rejected")

    common_subdivision = {}
    for name in CURVES:
        left, right = independent_lengths[name], primary_lengths[name]
        if len(left) != len(right):
            raise AssertionError("curve segments have different crossing combinatorics")
        common_subdivision[name] = [math.lcm(a, b) for a, b in zip(left, right)]
    encoded = json.dumps(independent_code, separators=(",", ":")).encode("ascii")
    return {
        "format": "luttinger-independent-marked-fiber-v1",
        "independence": _independence_audit(),
        "independent_structure": independent_structure,
        "primary_structure": primary_structure,
        "marked_ribbon_code_sha256": hashlib.sha256(encoded).hexdigest(),
        "marked_ribbon_codes_identical": True,
        "mutation_controls": {
            "identity_involution": "DISTINGUISHED",
            "p_O_swapping_involution": "REJECTED",
        },
        "equivariant_data_checked": [
            "named crossing rotations", "two disk faces labeled p and O",
            "involution on every directed curve end", "p and O fixed",
        ],
        "canonicalization_witness": {
            "independent_curve_reversals": list(independent_orientations),
            "independent_surface_reversed": independent_surface_reverse,
            "primary_curve_reversals": list(primary_orientations),
            "primary_surface_reversed": primary_surface_reverse,
        },
        "segment_edges": {
            "independent": {name: list(independent_lengths[name]) for name in CURVES},
            "primary": {name: list(primary_lengths[name]) for name in CURVES},
            "explicit_common_subdivision": common_subdivision,
        },
        "result": "PASS: equivariantly identical marked filling ribbon graphs",
        "theorem_boundary": [
            "an equivariant ribbon-graph isomorphism thickens equivariantly",
            "a commuting boundary-circle map extends by coning over each p/O disk",
            "finite surface homeomorphisms admit compatible PL subdivisions",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=ROOT / "independent_fiber_certificate.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    print("building and comparing independent marked fiber...", flush=True)
    certificate = build_certificate()
    encoded = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.check:
        if args.output.read_text(encoding="ascii") != encoded:
            raise SystemExit("independent fiber certificate mismatch")
        print(f"PASS: {args.output} exactly reproduced")
    else:
        args.output.write_text(encoded, encoding="ascii")
        print(f"wrote {args.output}")
    print(certificate["result"])
    print(certificate["segment_edges"])


if __name__ == "__main__":
    main()
