#!/usr/bin/env python3
"""Certify the relative representatives used in the marked bundle bridge.

This removes the need to invoke a separate relative isotopy-extension theorem.
For alpha, the certified involution is checked literally on the full three-row
c collar.  For beta, the paper and model use the same ordered twist word
T_a o T_b; its two annular supports are disjoint from the full three-row e
collar, and the complete flip stack restricts there to the literal staircase
product.  Thus the comparison is made in the relative mapping class group
from the outset, rather than repaired by a later isotopy.
"""

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path

from fiber import K_BAND, build_fiber
from layers import build_stack, prism_cells
from pl_self_intersection import certify as certify_section


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collar_vertices(V, name):
    return {
        V(name, row, index)
        for row in (-1, 0, 1)
        for index in range(K_BAND[name])
    }


def collar_record(surface, V, name):
    vertices = collar_vertices(V, name)
    triangles = {simplex for simplex in surface.simplices[2]
                 if simplex <= vertices}
    edges = {edge for triangle in triangles
             for edge in combinations(surface.sorted_tuple(triangle), 2)}
    edges = {frozenset(edge) for edge in edges}
    used_vertices = {vertex for edge in edges for vertex in edge}
    assert used_vertices == vertices

    edge_degree = {edge: 0 for edge in edges}
    for triangle in triangles:
        for edge in combinations(surface.sorted_tuple(triangle), 2):
            edge_degree[frozenset(edge)] += 1
    boundary = {edge for edge, degree in edge_degree.items() if degree == 1}
    assert set(edge_degree.values()) <= {1, 2}
    boundary_degree = {vertex: 0 for vertex in vertices}
    for edge in boundary:
        for vertex in edge:
            boundary_degree[vertex] += 1
    boundary_vertices = {vertex for vertex, degree in boundary_degree.items()
                         if degree}
    assert all(boundary_degree[vertex] == 2 for vertex in boundary_vertices)

    # Count the two boundary cycles directly.
    adjacency = {vertex: set() for vertex in boundary_vertices}
    for edge in boundary:
        u, v = tuple(edge)
        adjacency[u].add(v)
        adjacency[v].add(u)
    components = 0
    unseen = set(boundary_vertices)
    while unseen:
        components += 1
        stack = [unseen.pop()]
        while stack:
            for other in adjacency[stack.pop()]:
                if other in unseen:
                    unseen.remove(other)
                    stack.append(other)
    chi = len(vertices) - len(edges) + len(triangles)
    assert chi == 0 and components == 2
    return {
        "name": name,
        "f_vector": [len(vertices), len(edges), len(triangles)],
        "euler_characteristic": chi,
        "boundary_components": components,
        "is_triangulated_annulus": True,
    }


def beta_stack(F):
    V, surface = F["V"], F["L"]
    twists = []
    twist_specification = []
    for name, direction in (("b", 1), ("a", -1)):
        k = K_BAND[name]
        twists.append((
            [V(name, 0, i) for i in range(k)],
            [V(name, 1, i) for i in range(k)],
            [V(name, -1, i) for i in range(k)],
            direction,
        ))
        twist_specification.append({
            "applied_order": len(twist_specification) + 1,
            "curve": name,
            "combinatorial_direction": direction,
        })
    cells, levels, name = build_stack(
        surface, surface.rank.get, twists, copy_tag="REL")
    return cells, levels, name, twist_specification


def certify():
    F = build_fiber()
    surface, V, phi = F["L"], F["V"], F["phi0"]
    c_collar = collar_record(surface, V, "c")
    e_collar = collar_record(surface, V, "e")

    # The alpha representative is already exact, not merely isotopic: phi
    # preserves all three c rows and shifts every row by half a turn.
    c_vertices = collar_vertices(V, "c")
    assert {phi[vertex] for vertex in c_vertices} == c_vertices
    half = K_BAND["c"] // 2
    for row in (-1, 0, 1):
        for index in range(K_BAND["c"]):
            assert phi[V("c", row, index)] == \
                V("c", row, index + half)
    assert phi["p"] == "p" and phi["O"] == "O"

    cells, levels, name, twists = beta_stack(F)
    e_vertices = collar_vertices(V, "e")

    # No bistellar trace ball meets the e collar.
    cone_cells = 0
    for cell in cells:
        has_cone = any(
            isinstance(vertex, tuple) and len(vertex) == 2 and
            isinstance(vertex[0], tuple) and
            vertex[0][:2] == ("REL", "cone")
            for vertex in cell)
        if has_cone:
            cone_cells += 1
            fiber_vertices = {
                vertex[2] for vertex in cell
                if isinstance(vertex, tuple) and len(vertex) == 3 and
                vertex[0] == "REL"
            }
            assert not (fiber_vertices & e_vertices)

    # At every level the restriction to every triangle of the closed e collar
    # is exactly its three-tetrahedron staircase prism, with no extra cell.
    e_triangles = {triangle for triangle in surface.simplices[2]
                   if triangle <= e_vertices}
    actual = set(cells)
    expected = set()
    for level in range(levels):
        expected.update(tuple(cell) for cell in prism_cells(
            e_triangles, surface.rank.get,
            lambda vertex, level=level: name(level + 1, vertex),
            lambda vertex, level=level: name(level, vertex)))
    actual_in_collar = set()
    for cell in cells:
        if all(isinstance(vertex, tuple) and len(vertex) == 3 and
               vertex[0] == "REL" and vertex[2] in e_vertices
               for vertex in cell):
            actual_in_collar.add(tuple(cell))
    assert actual_in_collar == expected
    assert expected <= actual

    # Run 28 independently verifies literal product behavior near the fixed
    # p-section through every beta interface.
    section = certify_section()
    assert section["beta_product_levels"] == levels

    paper_data = ROOT / "paper_data.md"
    paper_text = paper_data.read_text(encoding="utf-8")
    assert "psi0 = T_a" in paper_text.replace("ψ₀", "psi0")
    assert "T_b first" in paper_text
    assert "fixes p, O and the" in paper_text
    assert "right handle pointwise" in paper_text

    fiber_certificate = ROOT / "independent_fiber_certificate.json"
    flip_certificate = ROOT / "pl_flip_trace_certificate.json"
    return {
        "format": "luttinger-relative-marked-monodromy-v1",
        "source_evidence": {
            paper_data.name: digest(paper_data),
            fiber_certificate.name: digest(fiber_certificate),
            flip_certificate.name: digest(flip_certificate),
            "runs/28-pl-self-intersection-certificate.txt": digest(
                REPO / "runs/28-pl-self-intersection-certificate.txt"),
        },
        "collars": {"c": c_collar, "e": e_collar},
        "alpha_relative_representative": {
            "full_c_collar_preserved": True,
            "action_on_each_collar_row": f"shift {half} of {K_BAND['c']}",
            "p_O_fixed": True,
            "comparison_type": "exact equivariant conjugacy, not isotopy",
        },
        "beta_relative_representative": {
            "paper_word": "T_a o T_b (T_b first)",
            "model_twist_trace": twists,
            "interfaces": levels,
            "flip_cone_cells_avoiding_e_collar": cone_cells,
            "e_collar_triangles": len(e_triangles),
            "literal_e_collar_product_tetrahedra": len(expected),
            "p_neighborhood_product_interfaces": section["beta_product_levels"],
            "comparison_type": (
                "same relative twist factorization with support outside e collar"
            ),
        },
        "conclusion": {
            "relative_isotopy_extension_required": False,
            "reason": (
                "alpha is exactly equivariant on the c collar; beta is the "
                "same supported twist word and is literally product on the e "
                "collar and at p"
            ),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path,
        default=ROOT / "relative_marking_certificate.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    certificate = certify()
    encoded = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.check:
        assert args.output.read_text(encoding="ascii") == encoded
        print(f"PASS: {args.output.relative_to(REPO)} exactly reproduced")
    else:
        args.output.write_text(encoded, encoding="ascii")
        print(f"wrote {args.output.relative_to(REPO)}")
    beta = certificate["beta_relative_representative"]
    print("PASS: full c and e collars are certified annuli")
    print("PASS: alpha is exact on the c collar and fixes p,O")
    print("PASS: all", beta["flip_cone_cells_avoiding_e_collar"],
          "beta trace cells avoid the e collar")
    print("PASS:", beta["literal_e_collar_product_tetrahedra"],
          "e-collar product tetrahedra checked")
    print("NO RELATIVE ISOTOPY-EXTENSION STEP REQUIRED")


if __name__ == "__main__":
    main()
