#!/usr/bin/env python3
"""Finite local-PL audit of every flip in the alternative beta trace.

This checker reads the assembled tetrahedra.  It does not call the builder's
flip, trace, or checking helpers.  For each cone vertex it reconstructs the
lower diagonal, upper diagonal, four side squares, link sphere, and cone-ball
boundary.  It also checks every slab and every vertex link in the complete
open trace.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict, deque
from itertools import combinations
from pathlib import Path

from alternative_bundle import build_alternative_bundle


ROOT = Path(__file__).resolve().parent


def _vkey(vertex):
    return repr(vertex)


def _skey(simplex):
    return tuple(sorted((_vkey(vertex) for vertex in simplex)))


def _faces(simplex, size):
    ordered = sorted(simplex, key=_vkey)
    return {frozenset(face) for face in combinations(ordered, size)}


def _f_vector(maximal):
    maximal = list(maximal)
    if not maximal:
        return []
    dimension = max(len(simplex) for simplex in maximal) - 1
    simplices = [set() for _ in range(dimension + 1)]
    for top in maximal:
        ordered = sorted(top, key=_vkey)
        for size in range(1, len(top) + 1):
            simplices[size - 1].update(
                frozenset(face) for face in combinations(ordered, size))
    return [len(level) for level in simplices]


def _connected_graph(vertices, edges):
    vertices = set(vertices)
    if not vertices:
        return False
    adjacency = {vertex: set() for vertex in vertices}
    for edge in edges:
        u, v = tuple(edge)
        adjacency[u].add(v)
        adjacency[v].add(u)
    start = min(vertices, key=_vkey)
    reached = {start}
    queue = deque([start])
    while queue:
        vertex = queue.popleft()
        for neighbour in adjacency[vertex]:
            if neighbour not in reached:
                reached.add(neighbour)
                queue.append(neighbour)
    return reached == vertices


def _surface_signature(triangles, expected):
    triangles = set(triangles)
    vertices = {vertex for triangle in triangles for vertex in triangle}
    edges = set().union(*(_faces(triangle, 2) for triangle in triangles))
    degrees = Counter(edge for triangle in triangles for edge in _faces(triangle, 2))
    if not _connected_graph(vertices, edges):
        raise AssertionError("vertex link is disconnected")
    if any(degree not in (1, 2) for degree in degrees.values()):
        raise AssertionError("vertex link is not a surface")
    boundary_edges = {edge for edge, degree in degrees.items() if degree == 1}
    boundary_vertices = {vertex for edge in boundary_edges for vertex in edge}
    for vertex in vertices:
        vertex_link_edges = {triangle - {vertex} for triangle in triangles
                             if vertex in triangle}
        vertex_link_vertices = {
            neighbour for edge in vertex_link_edges for neighbour in edge}
        link_degrees = Counter(
            neighbour for edge in vertex_link_edges for neighbour in edge)
        if not _connected_graph(vertex_link_vertices, vertex_link_edges):
            raise AssertionError("surface has a singular vertex link")
        degree_one = sum(degree == 1 for degree in link_degrees.values())
        if vertex in boundary_vertices:
            if degree_one != 2 or any(degree not in (1, 2)
                                      for degree in link_degrees.values()):
                raise AssertionError("boundary surface vertex link is not an interval")
        elif any(degree != 2 for degree in link_degrees.values()):
            raise AssertionError("interior surface vertex link is not a circle")
    chi = len(vertices) - len(edges) + len(triangles)
    if expected == "sphere":
        if boundary_edges or chi != 2:
            raise AssertionError("interior vertex link is not a 2-sphere")
    elif expected == "disk":
        if not boundary_edges or chi != 1:
            raise AssertionError("boundary vertex link is not a 2-disk")
        boundary_degrees = Counter(vertex for edge in boundary_edges for vertex in edge)
        if any(boundary_degrees[vertex] != 2 for vertex in boundary_vertices):
            raise AssertionError("disk-link boundary is not circular")
        if not _connected_graph(boundary_vertices, boundary_edges):
            raise AssertionError("disk-link boundary has multiple components")
    else:
        raise AssertionError("unknown surface type")
    return [len(vertices), len(edges), len(triangles)], len(boundary_edges)


def _cone_data(vertex):
    if (isinstance(vertex, tuple) and len(vertex) == 2 and
            isinstance(vertex[0], tuple) and len(vertex[0]) == 2 and
            vertex[0][0] == "ALT_CONE"):
        return vertex[0][1], vertex[1]
    return None


def _surface_vertex(vertex):
    return (isinstance(vertex, tuple) and len(vertex) == 3 and
            vertex[0] == "S" and isinstance(vertex[1], int))


def _triangle_degrees(tetrahedra):
    degrees = Counter()
    for tetrahedron in tetrahedra:
        degrees.update(_faces(tetrahedron, 3))
    return degrees


def _label_triangle(triangle, level):
    if any(not _surface_vertex(vertex) or vertex[1] != level
           for vertex in triangle):
        raise AssertionError("boundary triangle is not in one marked fiber")
    return frozenset(vertex[2] for vertex in triangle)


def _prism_tetrahedra(triangle, level, fiber_rank):
    vertices = sorted(triangle, key=fiber_rank)
    bottom = [("S", level, vertex) for vertex in vertices]
    top = [("S", level + 1, vertex) for vertex in vertices]
    return {
        frozenset((bottom[0], top[0], top[1], top[2])),
        frozenset((bottom[0], bottom[1], top[1], top[2])),
        frozenset((bottom[0], bottom[1], bottom[2], top[2])),
    }


def _audit_cone(cone, tetrahedra, level, fiber_rank):
    star = {tetrahedron for tetrahedron in tetrahedra if cone in tetrahedron}
    if not star:
        raise AssertionError("flip cone has empty star")
    if any(sum(_cone_data(vertex) is not None for vertex in tetrahedron) != 1
           for tetrahedron in star):
        raise AssertionError("flip tetrahedron contains multiple cones")
    link = {tetrahedron - {cone} for tetrahedron in star}
    link_f_vector, boundary_edges = _surface_signature(link, "sphere")
    if link_f_vector != [8, 18, 12] or boundary_edges:
        raise AssertionError("flip cone does not have the standard 8-vertex sphere link")

    star_degrees = _triangle_degrees(star)
    star_boundary = {face for face, degree in star_degrees.items() if degree == 1}
    if star_boundary != link or any(degree not in (1, 2)
                                    for degree in star_degrees.values()):
        raise AssertionError("cone star is not the cone-ball bounded by its link")

    lower = {triangle for triangle in link
             if all(_surface_vertex(vertex) and vertex[1] == level
                    for vertex in triangle)}
    upper = {triangle for triangle in link
             if all(_surface_vertex(vertex) and vertex[1] == level + 1
                    for vertex in triangle)}
    side = link - lower - upper
    if (len(lower), len(upper), len(side)) != (2, 2, 8):
        raise AssertionError("flip sphere has the wrong floor/roof/side partition")
    lower_labels = {_label_triangle(triangle, level) for triangle in lower}
    upper_labels = {_label_triangle(triangle, level + 1) for triangle in upper}
    quad = set().union(*lower_labels)
    if quad != set().union(*upper_labels) or len(quad) != 4:
        raise AssertionError("flip floor and roof have different quadrilaterals")
    old_diagonal = set.intersection(*(set(triangle) for triangle in lower_labels))
    new_diagonal = set.intersection(*(set(triangle) for triangle in upper_labels))
    if len(old_diagonal) != 2 or len(new_diagonal) != 2:
        raise AssertionError("flip diagonal is not shared by two triangles")
    if old_diagonal & new_diagonal or old_diagonal | new_diagonal != quad:
        raise AssertionError("old and new flip diagonals are not complementary")

    boundary_edges_labels = {
        frozenset((old, new)) for old in old_diagonal for new in new_diagonal}
    expected_side = set()
    for edge in boundary_edges_labels:
        low, high = sorted(edge, key=fiber_rank)
        expected_side.add(frozenset((
            ("S", level, low), ("S", level + 1, low),
            ("S", level + 1, high))))
        expected_side.add(frozenset((
            ("S", level, low), ("S", level, high),
            ("S", level + 1, high))))
    if side != expected_side:
        raise AssertionError("flip side is not four correctly triangulated squares")
    return {
        "cone": repr(cone),
        "quad": sorted(map(repr, quad)),
        "old_diagonal": sorted(map(repr, old_diagonal)),
        "new_diagonal": sorted(map(repr, new_diagonal)),
        "link_f_vector": link_f_vector,
        "star_f_vector": _f_vector(star),
    }, lower_labels, upper_labels, quad


def _assign_slabs(stack, levels):
    slabs = {level: set() for level in range(levels)}
    for tetrahedron in stack.simplices[3]:
        cones = [(vertex, _cone_data(vertex)) for vertex in tetrahedron
                 if _cone_data(vertex) is not None]
        if cones:
            if len(cones) != 1:
                raise AssertionError("tetrahedron contains multiple flip cones")
            level = cones[0][1][0]
        else:
            surface_levels = {vertex[1] for vertex in tetrahedron
                              if _surface_vertex(vertex)}
            if len(surface_levels) != 2 or max(surface_levels) - min(surface_levels) != 1:
                raise AssertionError("prism tetrahedron does not span one slab")
            level = min(surface_levels)
        if level not in slabs:
            raise AssertionError("tetrahedron has an out-of-range slab")
        slabs[level].add(tetrahedron)
    if sum(map(len, slabs.values())) != len(stack.simplices[3]):
        raise AssertionError("not every tetrahedron was assigned exactly once")
    return slabs


def build_certificate():
    bundle = build_alternative_bundle()
    stack, levels, fiber = bundle["_beta_stack"], bundle["m"], bundle["F"]
    slabs = _assign_slabs(stack, levels)
    base_triangles = {frozenset(triangle) for triangle in fiber["L"].simplices[2]}
    base_vertices = {vertex for triangle in base_triangles for vertex in triangle}
    base_edges = set().union(*(_faces(triangle, 2) for triangle in base_triangles))
    if not _connected_graph(base_vertices, base_edges):
        raise AssertionError("marked fiber is disconnected")
    current = base_triangles
    slab_records = []
    cone_records = []
    all_cones = set()
    mutation_control_passed = False
    for level in range(levels):
        tetrahedra = slabs[level]
        degrees = _triangle_degrees(tetrahedra)
        if any(degree not in (1, 2) for degree in degrees.values()):
            raise AssertionError("slab is not a 3-pseudomanifold")
        boundary = {triangle for triangle, degree in degrees.items() if degree == 1}
        lower = {triangle for triangle in boundary
                 if all(_surface_vertex(vertex) and vertex[1] == level
                        for vertex in triangle)}
        upper = {triangle for triangle in boundary
                 if all(_surface_vertex(vertex) and vertex[1] == level + 1
                        for vertex in triangle)}
        if boundary != lower | upper:
            raise AssertionError("slab has boundary away from its marked ends")
        lower_labels = {_label_triangle(triangle, level) for triangle in lower}
        upper_labels = {_label_triangle(triangle, level + 1) for triangle in upper}
        if lower_labels != current:
            raise AssertionError("adjacent slab triangulations do not agree")

        cones = sorted({vertex for tetrahedron in tetrahedra for vertex in tetrahedron
                        if _cone_data(vertex) is not None}, key=_vkey)
        if not cones:
            raise AssertionError("flip slab contains no cone")
        if all_cones & set(cones):
            raise AssertionError("flip cone occurs in more than one slab")
        all_cones.update(cones)
        removed, added, used_quad_vertices = set(), set(), set()
        for cone in cones:
            record, floor, roof, quad = _audit_cone(
                cone, tetrahedra, level, fiber["L"].rank.get)
            if used_quad_vertices & quad:
                raise AssertionError("simultaneous flip quadrilaterals intersect")
            used_quad_vertices.update(quad)
            removed.update(floor)
            added.update(roof)
            cone_records.append(record)
            if not mutation_control_passed:
                corrupted = set(tetrahedra)
                victim = min((tetrahedron for tetrahedron in corrupted
                              if cone in tetrahedron), key=_skey)
                corrupted.remove(victim)
                try:
                    _audit_cone(cone, corrupted, level, fiber["L"].rank.get)
                except AssertionError:
                    mutation_control_passed = True
                else:
                    raise AssertionError("deleted cone tetrahedron was accepted")
        if lower_labels - upper_labels != removed:
            raise AssertionError("slab removes triangles not accounted for by cones")
        if upper_labels - lower_labels != added:
            raise AssertionError("slab adds triangles not accounted for by cones")
        noncone_tetrahedra = {
            tetrahedron for tetrahedron in tetrahedra
            if not any(_cone_data(vertex) is not None for vertex in tetrahedron)}
        expected_prisms = set()
        for triangle in lower_labels - removed:
            expected_prisms.update(_prism_tetrahedra(
                triangle, level, fiber["L"].rank.get))
        if noncone_tetrahedra != expected_prisms:
            raise AssertionError("untouched region is not the exact marked prism trace")
        current = upper_labels
        slab_records.append({
            "level": level,
            "tetrahedra": len(tetrahedra),
            "boundary_triangles": len(boundary),
            "cones": len(cones),
            "removed_triangles": len(removed),
            "added_triangles": len(added),
        })
    if current != base_triangles:
        raise AssertionError("complete shear trace does not close its triangulation")
    if not mutation_control_passed:
        raise AssertionError("local mutation control did not run")

    global_degrees = _triangle_degrees(stack.simplices[3])
    if any(degree not in (1, 2) for degree in global_degrees.values()):
        raise AssertionError("complete trace is not a 3-pseudomanifold")
    global_boundary = {triangle for triangle, degree in global_degrees.items()
                       if degree == 1}
    expected_bottom = {
        frozenset(("S", 0, vertex) for vertex in triangle)
        for triangle in base_triangles}
    expected_top = {
        frozenset(("S", levels, vertex) for vertex in triangle)
        for triangle in base_triangles}
    if expected_bottom & expected_top or global_boundary != expected_bottom | expected_top:
        raise AssertionError("complete trace boundary is not exactly two marked fibers")
    if not _connected_graph(stack.vertices(), stack.simplices[1]):
        raise AssertionError("complete beta trace is disconnected")
    boundary_vertices = {vertex for triangle in global_boundary for vertex in triangle}
    incident = defaultdict(set)
    for tetrahedron in stack.simplices[3]:
        for vertex in tetrahedron:
            incident[vertex].add(tetrahedron)
    link_distributions = {"sphere": Counter(), "disk": Counter()}
    link_records = []
    for vertex in sorted(incident, key=_vkey):
        link = {tetrahedron - {vertex} for tetrahedron in incident[vertex]}
        kind = "disk" if vertex in boundary_vertices else "sphere"
        f_vector, boundary_edge_count = _surface_signature(link, kind)
        link_distributions[kind][tuple(f_vector)] += 1
        link_records.append([repr(vertex), kind, f_vector, boundary_edge_count])

    encoded_slabs = json.dumps(slab_records, separators=(",", ":"),
                               sort_keys=True).encode("ascii")
    encoded_cones = json.dumps(cone_records, separators=(",", ":"),
                               sort_keys=True).encode("ascii")
    encoded_links = json.dumps(link_records, separators=(",", ":"),
                              sort_keys=True).encode("ascii")
    link_summary = {
        kind: {str(list(vector)): count for vector, count in sorted(counter.items())}
        for kind, counter in link_distributions.items()
    }
    return {
        "format": "luttinger-pl-flip-trace-v1",
        "construction": "alternative 64-interface beta trace",
        "stack_f_vector": stack.f_vector(),
        "interfaces": levels,
        "flips": len(all_cones),
        "slab_boundary_components": "exactly lower and upper marked fibers",
        "complete_boundary_triangles": len(global_boundary),
        "complete_boundary_components": 2,
        "bottom_top_equal_marked_fiber": True,
        "mutation_control_deleted_cone_tetrahedron": "REJECTED",
        "every_flip": {
            "link": "connected closed chi=2 surface, f=[8,18,12]",
            "star": "cone 3-ball with boundary equal to link",
            "partition": "2 floor + 2 roof + 4 triangulated side squares",
            "diagonals": "old and new are complementary in one quadrilateral",
            "simultaneous_quads_vertex_disjoint": True,
            "outside_cone_stars": "exact staircase prisms over untouched triangles",
        },
        "cone_link_f_vectors": dict(Counter(
            str(record["link_f_vector"]) for record in cone_records)),
        "cone_star_f_vectors": dict(Counter(
            str(record["star_f_vector"]) for record in cone_records)),
        "vertex_link_distributions": link_summary,
        "slab_records_sha256": hashlib.sha256(encoded_slabs).hexdigest(),
        "cone_records_sha256": hashlib.sha256(encoded_cones).hexdigest(),
        "vertex_link_records_sha256": hashlib.sha256(encoded_links).hexdigest(),
        "explicit_theorem_boundary": [
            "connected closed triangulated surface with chi=2 is S^2",
            "cone on a combinatorial S^2 is a PL 3-ball",
            "the labeled 2-2 ball trace realizes the corresponding bistellar move",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=ROOT / "pl_flip_trace_certificate.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    print("auditing every local flip and global vertex link...", flush=True)
    certificate = build_certificate()
    encoded = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.check:
        if args.output.read_text(encoding="ascii") != encoded:
            raise SystemExit("PL flip-trace certificate mismatch")
        print(f"PASS: {args.output} exactly reproduced")
    else:
        args.output.write_text(encoded, encoding="ascii")
        print(f"wrote {args.output}")
    print({key: certificate[key] for key in
           ("interfaces", "flips", "stack_f_vector",
            "complete_boundary_triangles")})
    print("PASS: every local trace is the labeled 2-2 cone-ball")
    print("PASS: every global vertex link is a sphere or boundary disk")


if __name__ == "__main__":
    main()
