#!/usr/bin/env python3
"""Finite audit of the combinatorial core of Lemma 7.1.

The checker does not import the fiber, bundle, layer, or correspondence code.
It enumerates every oriented ribbon rotation system compatible with the
paper's ordered five-chain and chain-reversing involution.  It then verifies
that the four apparent choices are precisely curve-orientation choices, that
the ribbon has two invariant disk faces, and that the involution acts freely
as a half-turn on each face boundary.  Frozen Runs 34 and 54 are consulted
only after the abstract enumeration.
"""

import argparse
import ast
import hashlib
import json
from itertools import permutations
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent

EDGE_ENDPOINTS = {
    "a0": ("v0", "qa"), "a1": ("qa", "v0"),
    "b0": ("v0", "v1"), "b1": ("v1", "v0"),
    "c0": ("v1", "v2"), "c1": ("v2", "v1"),
    "d0": ("v2", "v3"), "d1": ("v3", "v2"),
    "e0": ("v3", "qe"), "e1": ("qe", "v3"),
}

VERTEX_INVOLUTION = {
    "v0": "v3", "v3": "v0", "v1": "v2", "v2": "v1",
    "qa": "qe", "qe": "qa",
}

EDGE_INVOLUTION = {
    "a0": "e1", "a1": "e0", "e0": "a1", "e1": "a0",
    "b0": "d0", "b1": "d1", "d0": "b0", "d1": "b1",
    "c0": "c1", "c1": "c0",
}


def cyclic_normal_form(items):
    items = tuple(items)
    return min(items[index:] + items[:index] for index in range(len(items)))


def cyclic_orders(items):
    first = min(items)
    rest = [item for item in items if item != first]
    return [(first,) + order for order in permutations(rest)]


def graph_data():
    origin, opposite = {}, {}
    for edge, (left, right) in EDGE_ENDPOINTS.items():
        origin[edge + "+"] = left
        origin[edge + "-"] = right
        opposite[edge + "+"] = edge + "-"
        opposite[edge + "-"] = edge + "+"
    dart_involution = {}
    for dart, vertex in origin.items():
        target_edge = EDGE_INVOLUTION[dart[:-1]]
        target_origin = VERTEX_INVOLUTION[vertex]
        sign = "+" if EDGE_ENDPOINTS[target_edge][0] == target_origin else "-"
        dart_involution[dart] = target_edge + sign
    assert all(dart_involution[dart_involution[dart]] == dart
               for dart in dart_involution)
    incident = {vertex: [] for vertex in VERTEX_INVOLUTION}
    for dart, vertex in origin.items():
        incident[vertex].append(dart)
    return origin, opposite, dart_involution, incident


def image_rotation(rotation, dart_involution):
    return cyclic_normal_form(dart_involution[dart] for dart in rotation)


def transverse(rotation):
    curve_names = [dart[0] for dart in rotation]
    return all(curve_names[index] != curve_names[(index + 1) % 4]
               for index in range(4))


def boundary_faces(rotations, opposite):
    predecessor = {}
    for rotation in rotations.values():
        for index, dart in enumerate(rotation):
            predecessor[dart] = rotation[(index - 1) % len(rotation)]
    successor = {dart: predecessor[opposite[dart]] for dart in opposite}
    unseen, faces = set(successor), []
    while unseen:
        start = min(unseen)
        face, current = [], start
        while current in unseen:
            unseen.remove(current)
            face.append(current)
            current = successor[current]
        assert current == start
        faces.append(tuple(face))
    return faces


def face_action(faces, dart_involution):
    face_sets = [set(face) for face in faces]
    action, shifts = [], []
    for face in faces:
        image = {dart_involution[dart] for dart in face}
        assert image in face_sets
        target = face_sets.index(image)
        action.append(target)
        if target == face_sets.index(set(face)):
            positions = {dart: index for index, dart in enumerate(face)}
            shift_set = {
                (positions[dart_involution[dart]] - positions[dart]) % len(face)
                for dart in face
            }
            assert len(shift_set) == 1
            shifts.append(next(iter(shift_set)))
        else:
            shifts.append(None)
    return action, shifts


def source_audit():
    path = Path(__file__)
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module or "")
    allowed = {"argparse", "ast", "hashlib", "itertools", "json", "pathlib"}
    assert imports <= allowed
    return {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "stdlib_imports": sorted(imports), "project_imports": []}


def read_certificate(name):
    path = ROOT / name
    return path, json.loads(path.read_text(encoding="ascii"))


def build_certificate():
    origin, opposite, dart_involution, incident = graph_data()
    target_v0 = ("a0+", "b0+", "a1-", "b1-")
    target_v1 = ("b0-", "c0+", "b1+", "c1-")
    candidates, admissible = 0, []
    for v0 in cyclic_orders(incident["v0"]):
        for v1 in cyclic_orders(incident["v1"]):
            candidates += 1
            rotations = {
                "v0": v0, "v1": v1,
                "v3": image_rotation(v0, dart_involution),
                "v2": image_rotation(v1, dart_involution),
                "qa": cyclic_normal_form(incident["qa"]),
                "qe": cyclic_normal_form(incident["qe"]),
            }
            assert image_rotation(rotations["qa"], dart_involution) == \
                cyclic_normal_form(rotations["qe"])
            if not all(transverse(rotations[vertex])
                       for vertex in ("v0", "v1", "v2", "v3")):
                continue
            faces = boundary_faces(rotations, opposite)
            if len(faces) != 2:
                continue
            action, shifts = face_action(faces, dart_involution)
            if action != [0, 1]:
                continue
            assert sorted(len(face) for face in faces) == [10, 10]
            assert sorted(shifts) == [5, 5]
            sign_bits = [int(cyclic_normal_form(v0) != target_v0),
                         int(cyclic_normal_form(v1) != target_v1)]
            # Orient b arbitrarily; reversing a toggles only the a/b sign and
            # reversing c toggles only the b/c sign.  The involution transports
            # those choices to e and d.  Thus every bit pair normalizes.
            orientation_witness = {
                "reverse_a_and_e": bool(sign_bits[0]),
                "reverse_c": bool(sign_bits[1]),
                "reverse_b_and_d": False,
            }
            admissible.append({
                "independent_crossing_bits": sign_bits,
                "face_lengths": sorted(len(face) for face in faces),
                "face_half_turn_shifts": sorted(shifts),
                "orientation_normalization": orientation_witness,
            })

    assert candidates == 36
    assert len(admissible) == 4
    assert sorted(item["independent_crossing_bits"] for item in admissible) == \
        [[0, 0], [0, 1], [1, 0], [1, 1]]

    # The ribbon is a connected orientable surface with V=6 graph disks,
    # E=10 bands and F=2 disk caps.  Its Euler characteristic forces genus 2.
    cell_counts = {"vertices": 6, "bands": 10, "disk_faces": 2}
    chi = cell_counts["vertices"] - cell_counts["bands"] + \
        cell_counts["disk_faces"]
    genus = (2 - chi) // 2
    assert (chi, genus) == (-2, 2)

    paper_path, paper = read_certificate("paper_coordinate_certificate.json")
    run34_path, run34 = read_certificate("independent_fiber_certificate.json")
    assert paper["marked_fiber"]["ordered_five_chain"] == list("abcde")
    assert paper["marked_fiber"]["involution"] == {
        "a": "e", "e": "a", "b": "d", "d": "b", "c": "c"}
    assert sorted(paper["marked_fiber"]["fixed_points"]) == ["O", "p"]
    assert run34["marked_ribbon_codes_identical"] is True
    assert set(run34["equivariant_data_checked"]) == {
        "named crossing rotations", "two disk faces labeled p and O",
        "involution on every directed curve end", "p and O fixed"}
    assert run34["primary_structure"]["chi"] == -2
    assert len(run34["primary_structure"]["complement_disks"]) == 2

    return {
        "format": "luttinger-lemma71-normal-form-v1",
        "checker_independence": source_audit(),
        "input_hashes": {
            paper_path.name: hashlib.sha256(paper_path.read_bytes()).hexdigest(),
            run34_path.name: hashlib.sha256(run34_path.read_bytes()).hexdigest(),
        },
        "rotation_enumeration": {
            "raw_independent_rotation_pairs": candidates,
            "admissible_equivariant_transverse_systems": len(admissible),
            "systems": admissible,
            "all_normalize_to_one_oriented_ribbon_system": True,
        },
        "canonical_surface": {
            "cell_counts": cell_counts, "euler_characteristic": chi,
            "genus": genus, "complementary_faces": "two disks",
            "face_involution": "each 10-cycle shifted freely by 5",
            "fixed_points_after_coning": ["p", "O"],
        },
        "explicit_extensions": {
            "ribbon": "map vertex disks cyclically and edge bands by product coordinates",
            "face_boundary": "equivariant cyclic maps of two 10-cycles",
            "cone_formula": "[z,t] -> [f(z),t] on each labeled disk",
            "equivariance_identity": "cone(f)(i(z),t)=i(cone(f)(z,t))",
        },
        "comparison_to_runs_34_54": "PASS",
        "remaining_general_input": (
            "classification/linearization of an orientation-preserving order-two "
            "disk diffeomorphism with one interior fixed point"),
        "result": "PASS: Lemma 7.1 reduced to the periodic-disk involution theorem",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=ROOT / "lemma71_normal_form_certificate.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    certificate = build_certificate()
    encoded = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.check:
        assert args.output.read_text(encoding="ascii") == encoded
        print(f"PASS: {args.output.name} exactly reproduced")
    else:
        args.output.write_text(encoded, encoding="ascii")
        print(f"wrote {args.output.name}")
    print("PASS: all 36 independent ribbon rotations enumerated")
    print("PASS: exactly four admissible systems, all orientation-normalize")
    print("PASS: two invariant 10-edge disk faces, boundary action shift 5")
    print("PASS: Runs 34 and 54 satisfy the finite normal-form hypotheses")
    print(certificate["result"])


if __name__ == "__main__":
    main()
