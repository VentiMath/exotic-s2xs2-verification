#!/usr/bin/env python3
r"""Construct the derived-frontier/normal-block-boundary equivalence.

For the full torus subcomplex T in K, a vertex of the computed first-derived
frontier is a mixed simplex s of K.  Write A=s∩T and B=s\T.  The explicit
map

    b(s) |-> (b(A)+b(B))/2

extends linearly over chains.  Its image is the barycentric level set
sum_{v in T} lambda_v=1/2.  In an ambient simplex with a torus vertices and
b outside vertices, the mixed-face poset is the product of the nonempty-face
posets of Delta^(a-1) and Delta^(b-1).  Its order complex is exactly the
barycentric subdivision of Delta^(a-1) x Delta^(b-1), so the map is a PL
homeomorphism on every cell and the formulas agree on shared faces.

This checker binds that universal argument to every mixed simplex and every
ambient top simplex in the actual bundle.  It also checks every torus
triangle: the already-used alternating 3-/4-simplex meridian maps to the
barycentric subdivision of the normal link circle, hence is literally a
normal-circle fiber of this boundary model.
"""

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path

from bundle import build_bundle


ROOT = Path(__file__).resolve().parent


def skey(simplex):
    return tuple(sorted((repr(vertex) for vertex in simplex)))


def faces(simplex, size):
    return {frozenset(face) for face in combinations(simplex, size)}


def rank(vectors):
    matrix = [list(vector) for vector in vectors if any(vector)]
    if not matrix:
        return 0
    rows, columns = len(matrix), len(matrix[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [left - scale * right
                           for left, right in zip(matrix[row], matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def level_vertex(A, B, ordered):
    """Exact barycentric coordinates of (b(A)+b(B))/2."""
    return tuple(Fraction(1, 2 * len(A)) if vertex in A
                 else Fraction(1, 2 * len(B)) if vertex in B
                 else Fraction(0) for vertex in ordered)


def maximal_product_chains(a, b):
    """Maximal chains in nonempty-face(Delta_a) x nonempty-face(Delta_b)."""
    left, right = tuple(range(a)), tuple(range(a, a + b))
    chains = []
    for first_left in left:
        for first_right in right:
            remaining = [("A", vertex) for vertex in left if vertex != first_left]
            remaining += [("B", vertex) for vertex in right if vertex != first_right]
            for order in permutations(remaining):
                A, B = {first_left}, {first_right}
                chain = [(frozenset(A), frozenset(B))]
                for side, vertex in order:
                    (A if side == "A" else B).add(vertex)
                    chain.append((frozenset(A), frozenset(B)))
                chains.append(tuple(chain))
    return chains


def local_models():
    records = []
    for a, b in ((1, 4), (2, 3), (3, 2)):
        ordered = tuple(range(a + b))
        vertices = [(frozenset(A), frozenset(B))
                    for size_a in range(1, a + 1)
                    for A in combinations(range(a), size_a)
                    for size_b in range(1, b + 1)
                    for B in combinations(range(a, a + b), size_b)]
        chains = maximal_product_chains(a, b)
        assert len(vertices) == (2 ** a - 1) * (2 ** b - 1)
        assert len(chains) == 6 * a * b
        for chain in chains:
            points = [level_vertex(A, B, ordered) for A, B in chain]
            differences = [tuple(x - y for x, y in zip(point, points[0]))
                           for point in points[1:]]
            assert rank(differences) == 3
            assert all(sum(point[:a]) == Fraction(1, 2)
                       and sum(point[a:]) == Fraction(1, 2)
                       for point in points)
        encoded = json.dumps([[(sorted(A), sorted(B)) for A, B in chain]
                              for chain in chains], separators=(",", ":"))
        records.append({
            "torus_vertices": a,
            "outside_vertices": b,
            "product_cell": f"Delta^{a-1} x Delta^{b-1}",
            "frontier_vertices": len(vertices),
            "maximal_chain_tetrahedra": len(chains),
            "all_tetrahedra_affinely_nondegenerate": True,
            "chain_list_sha256": hashlib.sha256(encoded.encode("ascii")).hexdigest(),
        })
    return records


def meridian_cycle(triangle, tetrahedra, tops):
    adjacency = defaultdict(list)
    for top in tops:
        faces_ = [tetrahedron for tetrahedron in tetrahedra if tetrahedron < top]
        assert len(faces_) == 2
        adjacency[faces_[0]].append((top, faces_[1]))
        adjacency[faces_[1]].append((top, faces_[0]))
    assert tetrahedra and all(len(adjacency[face]) == 2 for face in tetrahedra)
    start = min(tetrahedra, key=skey)
    cycle, current, previous = [start], start, None
    while True:
        options = sorted((item for item in adjacency[current]
                          if item[0] != previous), key=lambda item: skey(item[0]))
        top, following = options[0]
        cycle.append(top)
        if following == start:
            break
        cycle.append(following)
        current, previous = following, top
    assert set(cycle[::2]) == set(tetrahedra)
    assert set(cycle[1::2]) == set(tops)
    return cycle


def certify():
    bundle = build_bundle(dir_b=1, dir_a=-1)
    K = bundle["K"]
    component_sets = {
        "T_alpha": set(bundle["Ta_verts"]),
        "T_beta": set(bundle["Tb_verts"]),
    }
    torus_vertices = set().union(*component_sets.values())
    T = K.induced(torus_vertices)
    assert K.is_full(T)

    mixed = {simplex for simplex in K.all_simplices()
             if simplex & torus_vertices and simplex - torus_vertices}
    assert len(mixed) == 113336

    # The vertex map is a literal bijection s <-> (s∩T,s\T), lies on the
    # half-weight level, and respects/refects every derived edge relation.
    pairs = {}
    relation_count = 0
    for simplex in mixed:
        A, B = simplex & torus_vertices, simplex - torus_vertices
        assert A and B and A | B == simplex and not A & B
        pair = (A, B)
        assert pair not in pairs
        pairs[pair] = simplex
        coordinates = level_vertex(A, B, tuple(simplex))
        ordered = tuple(simplex)
        assert sum(coordinates[i] for i, vertex in enumerate(ordered)
                   if vertex in torus_vertices) == Fraction(1, 2)
        assert sum(coordinates[i] for i, vertex in enumerate(ordered)
                   if vertex not in torus_vertices) == Fraction(1, 2)
        for size in range(2, len(simplex)):
            for face in faces(simplex, size):
                if face in mixed:
                    relation_count += 1
                    A0, B0 = face & torus_vertices, face - torus_vertices
                    assert A0 <= A and B0 <= B
                    assert pairs.get((A0, B0), face) == face
    assert len(pairs) == len(mixed)

    # Bind the universal local models to every actual ambient 4-simplex near
    # T. Fullness implies a top simplex contains at most one torus triangle.
    top_distribution = Counter()
    near_tops = []
    for top in K.simplices[4]:
        a = len(top & torus_vertices)
        if not a:
            continue
        assert 1 <= a <= 3
        b = 5 - a
        top_distribution[(a, b)] += 1
        near_tops.append(top)
        expected_vertices = (2 ** a - 1) * (2 ** b - 1)
        actual = {face for size in range(2, 6) for face in faces(top, size)
                  if face in mixed}
        assert len(actual) == expected_vertices

    # Incidence indices for all normal fiber circles.
    tetra_by_triangle = defaultdict(list)
    top_by_triangle = defaultdict(list)
    torus_triangles = T.simplices[2]
    for tetrahedron in K.simplices[3]:
        marked = tetrahedron & torus_vertices
        if len(marked) == 3 and marked in torus_triangles:
            tetra_by_triangle[marked].append(tetrahedron)
    for top in near_tops:
        marked = top & torus_vertices
        if len(marked) == 3 and marked in torus_triangles:
            top_by_triangle[marked].append(top)

    meridian_records = []
    for triangle in sorted(torus_triangles, key=skey):
        cycle = meridian_cycle(triangle, tetra_by_triangle[triangle],
                               top_by_triangle[triangle])
        outside_chain = []
        for simplex in cycle:
            A, B = simplex & torus_vertices, simplex - torus_vertices
            assert A == triangle and B
            outside_chain.append(B)
            assert simplex in mixed
        assert all(len(B) == (1 if index % 2 == 0 else 2)
                   for index, B in enumerate(outside_chain))
        assert all(outside_chain[index] < outside_chain[(index + 1) % len(outside_chain)]
                   if index % 2 == 0
                   else outside_chain[(index + 1) % len(outside_chain)] < outside_chain[index]
                   for index in range(len(outside_chain)))
        encoded = json.dumps([skey(simplex) for simplex in cycle],
                             separators=(",", ":")).encode("utf-8")
        component = next(name for name, vertices in component_sets.items()
                         if triangle <= vertices)
        meridian_records.append({
            "component": component,
            "triangle_sha256": hashlib.sha256(
                "|".join(skey(triangle)).encode("utf-8")).hexdigest(),
            "fiber_subdivision_edges": len(cycle),
            "constant_torus_face": True,
            "alternating_outside_vertex_edge": True,
            "cycle_sha256": hashlib.sha256(encoded).hexdigest(),
        })
    assert len(meridian_records) == 592

    meridian_distribution = Counter(
        (record["component"], record["fiber_subdivision_edges"])
        for record in meridian_records)
    encoded_meridians = json.dumps(meridian_records, sort_keys=True,
                                   separators=(",", ":")).encode("utf-8")
    return {
        "format": "luttinger-frontier-normal-equivalence-v1",
        "ambient_f_vector": K.f_vector(),
        "frontier_vertices": len(mixed),
        "mixed_face_pair_bijection": True,
        "derived_comparabilities_checked": relation_count,
        "level_set": "sum_T(lambda)=1/2",
        "vertex_formula": "b(s) -> (b(s intersect T)+b(s minus T))/2",
        "near_top_simplices": len(near_tops),
        "top_intersection_distribution": {
            f"a={a},b={b}": count
            for (a, b), count in sorted(top_distribution.items())
        },
        "local_product_models": local_models(),
        "meridian_fibers_checked": len(meridian_records),
        "meridian_distribution": {
            f"{component},length={length}": count
            for (component, length), count in sorted(meridian_distribution.items())
        },
        "meridian_records_sha256": hashlib.sha256(encoded_meridians).hexdigest(),
        "local_flatness_certificate_sha256": hashlib.sha256(
            (ROOT / "torus_local_flatness_certificate.json").read_bytes()).hexdigest(),
        "conclusion": (
            "the computed derived frontier is explicitly PL-homeomorphic "
            "to the half-weight normal block boundary, and every extracted "
            "dual meridian is a normal-circle fiber"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=ROOT / "frontier_normal_equivalence_certificate.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    certificate = certify()
    encoded = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.check:
        assert args.output.read_text(encoding="ascii") == encoded
        print(f"PASS: {args.output.relative_to(ROOT.parent)} exactly reproduced")
    else:
        args.output.write_text(encoded, encoding="ascii")
        print(f"wrote {args.output}")
    print(f"PASS: {certificate['frontier_vertices']:,} frontier vertices bound")
    print(f"PASS: {certificate['near_top_simplices']:,} local product cells checked")
    print(f"PASS: all {certificate['meridian_fibers_checked']} meridians are normal fibers")
    print("PASS: explicit derived-frontier/normal-boundary equivalence")


if __name__ == "__main__":
    main()
