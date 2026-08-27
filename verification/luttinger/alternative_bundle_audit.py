#!/usr/bin/env python3
"""Build, audit, and compare the alternative marked-bundle triangulation."""

from __future__ import annotations

import argparse
import ast
import json
from fractions import Fraction
from pathlib import Path

from alternative_bundle import build_alternative_bundle, check_alternative_bundle
from fast_tietze import simplify
from independent_peripheral_extractor import extract, rail_loop
from pi1 import Presentation


ROOT = Path(__file__).resolve().parent


def _matrix_inverse(matrix):
    size = len(matrix)
    augmented = [
        [Fraction(value) for value in matrix[row]] +
        [Fraction(row == column) for column in range(size)]
        for row in range(size)
    ]
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if augmented[row][column]), None)
        if pivot is None:
            raise AssertionError("named bottom loops do not form an H1 basis")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            scale = augmented[row][column]
            augmented[row] = [left - scale * right
                              for left, right in
                              zip(augmented[row], augmented[column])]
    return [row[size:] for row in augmented]


def _matrix_product(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(len(right)))
             for j in range(len(right[0]))]
            for i in range(len(left))]


def _integer_matrix(matrix):
    if any(value.denominator != 1 for row in matrix for value in row):
        raise AssertionError("monodromy matrix is not integral")
    return [[int(value) for value in row] for row in matrix]


def beta_homology_action(bundle):
    """Recover the marked beta action from the two boundary inclusions."""
    stack, levels, fiber = bundle["_beta_stack"], bundle["m"], bundle["F"]
    presentation = Presentation(stack, ("S", 0, "p"))
    names = "xyrs"
    loops = {name: rail_loop(fiber, name) for name in names}
    vertical = [("S", level, "p") for level in range(levels + 1)]

    def at(level, path):
        return [("S", level, vertex) for vertex in path]

    def transported_top(path):
        return vertical + at(levels, path)[1:] + vertical[::-1][1:]

    tracked = [presentation.loop_word(at(0, loops[name])) for name in names]
    tracked.extend(presentation.loop_word(transported_top(loops[name]))
                   for name in names)
    live, relators, reduced = simplify(
        presentation.ngens, presentation.relators, tracked, verbose=False)
    if len(live) != 4:
        raise AssertionError(f"beta trace has H1 rank {len(live)}, want 4")
    exponent_relators = [
        [sum((1 if letter > 0 else -1) for letter in relator
             if abs(letter) == generator) for generator in live]
        for relator in relators
    ]
    if any(any(row) for row in exponent_relators):
        raise AssertionError("beta trace has an unexpected abelian relation")

    def vector(word):
        return [sum((1 if letter > 0 else -1) for letter in word
                    if abs(letter) == generator) for generator in live]

    bottom_vectors = [vector(word) for word in reduced[:4]]
    top_vectors = [vector(word) for word in reduced[4:]]
    # Columns are the named x,y,r,s classes, rows the live H1 basis.
    bottom = [[Fraction(bottom_vectors[column][row]) for column in range(4)]
              for row in range(4)]
    top = [[Fraction(top_vectors[column][row]) for column in range(4)]
           for row in range(4)]
    top_in_bottom = _matrix_product(_matrix_inverse(bottom), top)
    # Same-label top classes equal psi^{-1} of the bottom classes; invert to
    # recover the bottom-to-top monodromy convention used in the paper.
    monodromy = _matrix_inverse(top_in_bottom)
    monodromy = _integer_matrix(monodromy)
    expected = [[0, 1, 0, 0],
                [-1, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]]
    if monodromy != expected:
        raise AssertionError(
            f"alternative beta H1 action {monodromy} != expected {expected}")
    # I-psi is unimodular on <x,y> and zero on <r,s>; adjoining the base
    # circle gives H1(mapping torus)=Z^3 with no torsion.
    determinant_xy = ((1 - monodromy[0][0]) * (1 - monodromy[1][1]) -
                      (-monodromy[0][1]) * (-monodromy[1][0]))
    if abs(determinant_xy) != 1:
        raise AssertionError("beta mapping-torus H1 has unexpected torsion")
    return {
        "basis": list(names),
        "matrix_columns_are_images": monodromy,
        "expected_actions": ["x -> -y", "y -> x+y", "r -> r", "s -> s"],
        "mapping_torus_H1": "Z^3, torsion-free",
        "trace_raw_presentation": {
            "generators": presentation.ngens,
            "relators": len(presentation.relators),
        },
        "trace_H1_rank": len(live),
    }


def construction_import_audit():
    source = (ROOT / "alternative_bundle.py").read_text(encoding="ascii")
    tree = ast.parse(source)
    imports = []
    complex_names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module)
            if node.module == "complex":
                complex_names.extend(alias.name for alias in node.names)
    forbidden = {"bundle", "layers"}
    if forbidden & set(imports):
        raise AssertionError(f"alternative builder imported {forbidden & set(imports)}")
    if "product" in complex_names:
        raise AssertionError("alternative builder imported complex.product")
    return {"imports": sorted(imports),
            "forbidden_modules_absent": sorted(forbidden),
            "complex_product_imported": False}


def build_certificate(primary_path):
    primary = json.loads(primary_path.read_text(encoding="ascii"))
    alternative_bundle = build_alternative_bundle()
    structure = check_alternative_bundle(alternative_bundle)
    monodromy = beta_homology_action(alternative_bundle)
    alternative = extract(alternative_bundle)

    if structure["K_f_vector"] == primary["bundle"]["K_f_vector"]:
        raise AssertionError("alternative total space accidentally matches primary f-vector")
    if alternative["marked_crossings"] != primary["marked_crossings"]:
        raise AssertionError("alternative bundle changed the paper crossings/whiskers")
    same_literal = ["geom_M_independent", "lb_a_y1_independent",
                    "N_grid_local_independent", "geom_N_independent"]
    literal_comparisons = {}
    for name in same_literal:
        old = primary["peripheral_loops"][name]["complement_loop_sha256"]
        new = alternative["peripheral_loops"][name]["complement_loop_sha256"]
        if old != new:
            raise AssertionError(f"unchanged alpha-side path changed: {name}")
        literal_comparisons[name] = "IDENTICAL canonical complement path"
    old_beta = primary["peripheral_loops"]["lb_b_s2_independent"]
    new_beta = alternative["peripheral_loops"]["lb_b_s2_independent"]
    for key in ("kind", "crossing", "fiber_whisker", "base_direction",
                "fiber_drift"):
        if old_beta["source"][key] != new_beta["source"][key]:
            raise AssertionError(f"alternative beta semantic field changed: {key}")
    if old_beta["complement_loop_sha256"] == new_beta["complement_loop_sha256"]:
        raise AssertionError("alternative beta push-off path did not change")

    return {
        "format": "luttinger-alternative-bundle-v1",
        "construction_boundary": construction_import_audit(),
        "structure": structure,
        "alternative_K_vertex_sha256": alternative["bundle"]["K_vertex_set_sha256"],
        "primary_K_vertex_sha256": primary["bundle"]["K_vertex_set_sha256"],
        "beta_monodromy": monodromy,
        "peripheral_comparison": {
            "marked_crossings_and_whiskers": "IDENTICAL",
            "literal_unchanged_paths": literal_comparisons,
            "beta_push_off": {
                "semantic_source_fields": "IDENTICAL",
                "primary_edges": old_beta["complement_edges"],
                "alternative_edges": new_beta["complement_edges"],
                "primary_sha256": old_beta["complement_loop_sha256"],
                "alternative_sha256": new_beta["complement_loop_sha256"],
                "path_difference": "EXPECTED: 32 versus 64 beta interfaces",
            },
            "transported_N_formula":
                alternative["peripheral_loops"]["geom_N_independent"]["formula"],
            "result": "PASS: same marked peripheral semantics on a different triangulation",
        },
        "scope": {
            "shared_input": "fiber.build_fiber marked genus-2 surface",
            "independent": "products, mapping cylinders, flip traces, twist stack, seams, total 4-complex, marked tori",
            "theorem_input": "paired annular shear realizes the stated Dehn twists",
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--primary", type=Path,
                        default=ROOT / "independent_peripheral_certificate.json")
    parser.add_argument("--output", type=Path,
                        default=ROOT / "alternative_bundle_certificate.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    print("building and auditing alternative marked bundle...", flush=True)
    certificate = build_certificate(args.primary)
    encoded = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.check:
        if args.output.read_text(encoding="ascii") != encoded:
            raise SystemExit("alternative bundle certificate mismatch")
        print(f"PASS: {args.output} exactly reproduced")
    else:
        args.output.write_text(encoded, encoding="ascii")
        print(f"wrote {args.output}")
    print(certificate["structure"])
    print(certificate["beta_monodromy"]["matrix_columns_are_images"])
    print(certificate["peripheral_comparison"]["result"])


if __name__ == "__main__":
    main()
