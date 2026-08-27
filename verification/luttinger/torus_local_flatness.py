#!/usr/bin/env python3
"""Exhaustive local-flatness certificate for both surgery tori.

For every simplex sigma of T_alpha and T_beta, certify the standard
codimension-two link pair (lk_K sigma, lk_T sigma):

* triangle: (S^1, empty);
* edge:     (S^2, S^0);
* vertex:   (S^3, unknotted S^1).

The vertex case has proof-producing witnesses.  Deleting one tetrahedron
from the ambient link leaves a complex that elementary-collapses to a point.
The induced complement of the torus-link circle elementary-collapses to a
single cycle.  The explicit full-subcomplex barycentric retraction therefore
gives cyclic knot group; the classical unknot criterion (a knot in S^3 has
cyclic group iff it is the unknot) makes the link pair standard.  Every
collapse is replayed independently.

The output certificate includes one hash-bound record for every simplex.
"""

import argparse
import hashlib
import json
from collections import Counter, defaultdict, deque
from itertools import combinations
from pathlib import Path

from bundle import build_bundle
from complex import Complex


ROOT = Path(__file__).resolve().parent


def skey(simplex):
    return tuple(sorted((repr(vertex) for vertex in simplex)))


def simplex_id(simplex):
    encoded = "|".join(skey(simplex)).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def faces(simplex, size):
    ordered = sorted(simplex, key=repr)
    return {frozenset(face) for face in combinations(ordered, size)}


def connected(vertices, edges):
    vertices = set(vertices)
    if not vertices:
        return False
    adjacency = {vertex: set() for vertex in vertices}
    for edge in edges:
        u, v = tuple(edge)
        adjacency[u].add(v)
        adjacency[v].add(u)
    reached = {min(vertices, key=repr)}
    queue = deque(reached)
    while queue:
        for neighbour in adjacency[queue.popleft()]:
            if neighbour not in reached:
                reached.add(neighbour)
                queue.append(neighbour)
    return reached == vertices


def surface_signature(triangles, expected):
    triangles = set(triangles)
    vertices = set().union(*triangles)
    edges = set().union(*(faces(triangle, 2) for triangle in triangles))
    incidence = Counter(edge for triangle in triangles
                        for edge in faces(triangle, 2))
    assert connected(vertices, edges)
    assert all(degree in (1, 2) for degree in incidence.values())
    boundary = {edge for edge, degree in incidence.items() if degree == 1}
    boundary_vertices = set().union(*boundary) if boundary else set()
    for vertex in vertices:
        link_edges = {triangle - {vertex} for triangle in triangles
                      if vertex in triangle}
        link_vertices = set().union(*link_edges)
        degrees = Counter(point for edge in link_edges for point in edge)
        assert connected(link_vertices, link_edges)
        if vertex in boundary_vertices:
            assert sum(degree == 1 for degree in degrees.values()) == 2
            assert all(degree in (1, 2) for degree in degrees.values())
        else:
            assert all(degree == 2 for degree in degrees.values())
    chi = len(vertices) - len(edges) + len(triangles)
    if expected == "sphere":
        assert not boundary and chi == 2
    elif expected == "disk":
        assert boundary and chi == 1
        boundary_degrees = Counter(vertex for edge in boundary for vertex in edge)
        assert all(degree == 2 for degree in boundary_degrees.values())
        assert connected(boundary_vertices, boundary)
    elif expected == "torus":
        assert not boundary and chi == 0
        Complex(triangles).orientation_signs()
    else:
        raise AssertionError(expected)
    return [len(vertices), len(edges), len(triangles)]


def closed_three_manifold(complex_):
    tetrahedra = complex_.simplices[3]
    triangle_degree = Counter(triangle for tetrahedron in tetrahedra
                              for triangle in faces(tetrahedron, 3))
    assert set(triangle_degree) == complex_.simplices[2]
    assert all(degree == 2 for degree in triangle_degree.values())
    for vertex in complex_.simplices[0]:
        point = next(iter(vertex))
        triangles = {tetrahedron - {point} for tetrahedron in tetrahedra
                     if point in tetrahedron}
        surface_signature(triangles, "sphere")


def compact_three_manifold_with_sphere_boundary(complex_):
    tetrahedra = complex_.simplices[3]
    triangle_degree = Counter(triangle for tetrahedron in tetrahedra
                              for triangle in faces(tetrahedron, 3))
    assert set(triangle_degree) == complex_.simplices[2]
    assert all(degree in (1, 2) for degree in triangle_degree.values())
    boundary = {triangle for triangle, degree in triangle_degree.items()
                if degree == 1}
    boundary_f_vector = surface_signature(boundary, "sphere")
    boundary_vertices = set().union(*boundary)
    for vertex in complex_.simplices[0]:
        point = next(iter(vertex))
        triangles = {tetrahedron - {point} for tetrahedron in tetrahedra
                     if point in tetrahedron}
        surface_signature(triangles,
                          "disk" if point in boundary_vertices else "sphere")
    return boundary_f_vector


def maximal_simplices(levels):
    result = set()
    top_dimension = max(levels)
    for dimension, simplices in levels.items():
        for simplex in simplices:
            if not any(simplex < coface
                       for higher in range(dimension + 1, top_dimension + 1)
                       for coface in levels.get(higher, ())):
                result.add(simplex)
    return result


def find_collapse(complex_, target):
    """Return elementary free-face pairs reducing to target point or cycle."""
    levels = {dimension: set(simplices)
              for dimension, simplices in complex_.simplices.items()}
    moves = []
    while True:
        maxima = maximal_simplices(levels)
        candidates = []
        for dimension in range(max(levels) - 1, -1, -1):
            owners = defaultdict(list)
            for coface in levels.get(dimension + 1, ()):
                for vertex in coface:
                    face = coface - {vertex}
                    if face in levels[dimension]:
                        owners[face].append(coface)
            for face, cofaces in owners.items():
                if len(cofaces) == 1 and cofaces[0] in maxima:
                    candidates.append((dimension, face, cofaces[0]))
            if candidates:
                break
        if not candidates:
            break
        dimension, face, coface = min(
            candidates, key=lambda item: (skey(item[1]), skey(item[2])))
        levels[dimension].remove(face)
        levels[dimension + 1].remove(coface)
        moves.append((face, coface))

    counts = [len(levels.get(dimension, ()))
              for dimension in range(max(levels) + 1)]
    if target == "point":
        success = counts[0] == 1 and sum(counts[1:]) == 0
    elif target == "cycle":
        vertices = {next(iter(v)) for v in levels[0]}
        edges = levels[1]
        degrees = Counter(vertex for edge in edges for vertex in edge)
        success = (not any(levels.get(dimension) for dimension in range(2, len(counts)))
                   and connected(vertices, edges)
                   and len(vertices) == len(edges)
                   and all(degrees[vertex] == 2 for vertex in vertices))
    else:
        raise AssertionError(target)
    return success, moves, levels


def replay_collapse(complex_, moves, target):
    levels = {dimension: set(simplices)
              for dimension, simplices in complex_.simplices.items()}
    for face, coface in moves:
        dimension = len(face) - 1
        assert face in levels[dimension]
        assert coface in levels[dimension + 1]
        assert face < coface and len(coface) == len(face) + 1
        owners = [candidate for candidate in levels[dimension + 1]
                  if face < candidate]
        assert owners == [coface] or set(owners) == {coface}
        assert coface in maximal_simplices(levels)
        levels[dimension].remove(face)
        levels[dimension + 1].remove(coface)
    counts = [len(levels.get(dimension, ()))
              for dimension in range(max(levels) + 1)]
    if target == "point":
        assert counts[0] == 1 and sum(counts[1:]) == 0
    else:
        vertices = {next(iter(v)) for v in levels[0]}
        edges = levels[1]
        degrees = Counter(vertex for edge in edges for vertex in edge)
        assert not any(levels.get(dimension) for dimension in range(2, len(counts)))
        assert connected(vertices, edges) and len(vertices) == len(edges)
        assert all(degrees[vertex] == 2 for vertex in vertices)
    encoded = json.dumps([(skey(a), skey(b)) for a, b in moves],
                         separators=(",", ":")).encode("utf-8")
    return counts, hashlib.sha256(encoded).hexdigest()


def link_complex(incident_tops, simplex):
    return Complex([top - simplex for top in incident_tops])


def induced_outside(complex_, excluded_vertices):
    candidates = {top - excluded_vertices for top in complex_.simplices[3]
                  if top - excluded_vertices}
    maximal = {simplex for simplex in candidates
               if not any(simplex < other for other in candidates)}
    return Complex(maximal)


def certify_component(name, K, torus_vertices):
    torus_vertices = set(torus_vertices)
    T = K.induced(torus_vertices)
    assert T.dim == 2 and K.is_full(T)
    assert surface_signature(T.simplices[2], "torus") == T.f_vector()

    top_incidence = defaultdict(list)
    for top in K.simplices[4]:
        marked = top & torus_vertices
        for size in range(1, min(3, len(marked)) + 1):
            for simplex in combinations(marked, size):
                top_incidence[frozenset(simplex)].append(top)

    triangle_incidence = defaultdict(list)
    for triangle in T.simplices[2]:
        for size in range(1, 4):
            for simplex in combinations(triangle, size):
                triangle_incidence[frozenset(simplex)].append(triangle)

    records = []
    for dimension in range(3):
        for simplex in sorted(T.simplices[dimension], key=skey):
            ambient = link_complex(top_incidence[simplex], simplex)
            torus_link_maximal = {triangle - simplex
                                  for triangle in triangle_incidence[simplex]
                                  if triangle - simplex}
            record = {
                "component": name,
                "simplex_dimension": dimension,
                "simplex_sha256": simplex_id(simplex),
                "ambient_link_f_vector": ambient.f_vector(),
            }
            if dimension == 2:
                assert ambient.dim == 1
                edges = ambient.simplices[1]
                vertices = {next(iter(v)) for v in ambient.simplices[0]}
                degrees = Counter(vertex for edge in edges for vertex in edge)
                assert connected(vertices, edges)
                assert all(degrees[vertex] == 2 for vertex in vertices)
                assert not torus_link_maximal
                record.update({"link_pair": "(S1,empty)",
                               "normal_circle_length": len(edges)})
            elif dimension == 1:
                assert ambient.dim == 2
                surface_signature(ambient.simplices[2], "sphere")
                torus_link_vertices = set().union(*torus_link_maximal)
                assert len(torus_link_vertices) == 2
                assert all(len(simplex_) == 1 for simplex_ in torus_link_maximal)
                record.update({"link_pair": "(S2,S0)",
                               "torus_link_vertices": 2})
            else:
                assert ambient.dim == 3
                closed_three_manifold(ambient)
                puncture_witness = None
                chosen_punctured = None
                for tetrahedron in sorted(ambient.simplices[3], key=skey):
                    punctured = Complex(ambient.simplices[3] - {tetrahedron})
                    success, moves, _ = find_collapse(punctured, "point")
                    if success:
                        counts, digest = replay_collapse(punctured, moves, "point")
                        puncture_witness = (len(moves), counts, digest,
                                            simplex_id(tetrahedron))
                        chosen_punctured = punctured
                        break
                assert puncture_witness is not None
                puncture_boundary = compact_three_manifold_with_sphere_boundary(
                    chosen_punctured)

                torus_link = Complex(torus_link_maximal)
                assert torus_link.dim == 1
                link_edges = torus_link.simplices[1]
                link_vertices = {next(iter(v)) for v in torus_link.simplices[0]}
                degrees = Counter(vertex for edge in link_edges for vertex in edge)
                assert connected(link_vertices, link_edges)
                assert all(degrees[vertex] == 2 for vertex in link_vertices)
                # Fullness of T in K implies this link circle is full in the
                # ambient link; check it directly rather than infer it.
                assert all(not (simplex <= link_vertices) or simplex in torus_link
                           for simplex in ambient.all_simplices())

                exterior = induced_outside(ambient, link_vertices)
                assert exterior.dim == 3
                success, moves, _ = find_collapse(exterior, "cycle")
                assert success
                counts, digest = replay_collapse(exterior, moves, "cycle")
                record.update({
                    "link_pair": "(S3,unknotted_S1)",
                    "torus_link_length": len(link_edges),
                    "punctured_S3_collapse_moves": puncture_witness[0],
                    "punctured_S3_remainder": puncture_witness[1],
                    "punctured_S3_moves_sha256": puncture_witness[2],
                    "puncture_tetrahedron_sha256": puncture_witness[3],
                    "punctured_S3_boundary_f_vector": puncture_boundary,
                    "exterior_f_vector": exterior.f_vector(),
                    "exterior_collapse_moves": len(moves),
                    "exterior_spine_f_vector": counts,
                    "exterior_moves_sha256": digest,
                    "unknot_criterion": "full knot complement collapses to S1",
                })
            records.append(record)
    return T.f_vector(), records


def certify():
    bundle = build_bundle(dir_b=1, dir_a=-1)
    K = bundle["K"]
    components = []
    all_records = []
    for name, vertices in (("T_alpha", bundle["Ta_verts"]),
                           ("T_beta", bundle["Tb_verts"])):
        f_vector, records = certify_component(name, K, vertices)
        components.append({
            "name": name,
            "f_vector": f_vector,
            "simplex_records": len(records),
            "vertices_checked": sum(r["simplex_dimension"] == 0 for r in records),
            "edges_checked": sum(r["simplex_dimension"] == 1 for r in records),
            "triangles_checked": sum(r["simplex_dimension"] == 2 for r in records),
        })
        all_records.extend(records)

    expected = sum(sum(component["f_vector"]) for component in components)
    assert len(all_records) == expected == 1776
    distribution = Counter(record["link_pair"] for record in all_records)
    assert distribution == {
        "(S3,unknotted_S1)": 296,
        "(S2,S0)": 888,
        "(S1,empty)": 592,
    }
    encoded_records = json.dumps(all_records, sort_keys=True,
                                 separators=(",", ":")).encode("utf-8")
    return {
        "format": "luttinger-torus-local-flatness-v1",
        "ambient_f_vector": K.f_vector(),
        "components": components,
        "total_simplices_checked": len(all_records),
        "link_pair_distribution": dict(sorted(distribution.items())),
        "all_simplex_records_sha256": hashlib.sha256(encoded_records).hexdigest(),
        "vertex_witnesses": [record for record in all_records
                             if record["simplex_dimension"] == 0],
        "standard_theorems_used": [
            "classification of compact connected triangulated surfaces",
            "a compact contractible PL 3-manifold with S2 boundary is a 3-ball",
            "a PL knot in S3 with cyclic group is the unknot",
        ],
        "conclusion": "both full embedded tori are locally flat at every simplex",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=ROOT / "torus_local_flatness_certificate.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    certificate = certify()
    encoded = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.check:
        assert args.output.read_text(encoding="ascii") == encoded
        try:
            label = args.output.relative_to(ROOT.parent)
        except ValueError:
            label = args.output
        print(f"PASS: {label} exactly reproduced")
    else:
        args.output.write_text(encoded, encoding="ascii")
        print(f"wrote {args.output}")
    for component in certificate["components"]:
        print(f"PASS {component['name']}: {component['vertices_checked']} vertices, "
              f"{component['edges_checked']} edges, "
              f"{component['triangles_checked']} triangles")
    print("PASS: all 1,776 simplex link pairs are standard")
    print("PASS: both surgery tori are locally flat")


if __name__ == "__main__":
    main()
