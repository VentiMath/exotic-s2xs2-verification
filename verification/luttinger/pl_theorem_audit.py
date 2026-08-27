#!/usr/bin/env python3
"""Integrate the finite hypotheses used by the residual PL theorems.

The theorem statements themselves remain conventional topology inputs.  This
checker makes their application finite and explicit by reading the independent
fiber and flip-trace certificates and replaying the section push-off audit.
"""

import argparse
import ast
import hashlib
import json
from pathlib import Path

from pl_self_intersection import certify as certify_section


ROOT = Path(__file__).resolve().parent


def _read_json(name):
    path = ROOT / name
    return path, json.loads(path.read_text(encoding="ascii"))


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _count_link_records(distribution):
    return sum(count for records in distribution.values()
               for count in records.values())


def audit():
    flip_path, flip = _read_json("pl_flip_trace_certificate.json")
    fiber_path, fiber = _read_json("independent_fiber_certificate.json")

    assert flip["format"] == "luttinger-pl-flip-trace-v1"
    assert flip["interfaces"] == 64 and flip["flips"] == 128
    assert flip["complete_boundary_components"] == 2
    assert flip["bottom_top_equal_marked_fiber"] is True
    assert flip["mutation_control_deleted_cone_tetrahedron"] == "REJECTED"
    assert flip["cone_link_f_vectors"] == {"[8, 18, 12]": 128}
    assert flip["cone_star_f_vectors"] == {"[9, 26, 30, 12]": 128}
    assert flip["every_flip"]["diagonals"].startswith("old and new")
    assert flip["every_flip"]["simultaneous_quads_vertex_disjoint"] is True
    assert flip["every_flip"]["outside_cone_stars"].startswith(
        "exact staircase prisms")

    links = flip["vertex_link_distributions"]
    assert set(links) == {"sphere", "disk"}
    assert _count_link_records(links) == flip["stack_f_vector"][0]
    for vector_text in links["sphere"]:
        v, e, f = ast.literal_eval(vector_text)
        assert v - e + f == 2
    for vector_text in links["disk"]:
        v, e, f = ast.literal_eval(vector_text)
        assert v - e + f == 1

    assert fiber["format"] == "luttinger-independent-marked-fiber-v1"
    assert fiber["marked_ribbon_codes_identical"] is True
    assert fiber["mutation_controls"] == {
        "identity_involution": "DISTINGUISHED",
        "p_O_swapping_involution": "REJECTED",
    }
    required_equivariant = {
        "named crossing rotations", "two disk faces labeled p and O",
        "involution on every directed curve end", "p and O fixed",
    }
    assert set(fiber["equivariant_data_checked"]) == required_equivariant
    segments = fiber["segment_edges"]
    for curve in ("a", "b", "c", "d", "e"):
        left = segments["independent"][curve]
        right = segments["primary"][curve]
        common = segments["explicit_common_subdivision"][curve]
        assert len(left) == len(right) == len(common)
        assert common == [a * b for a, b in zip(left, right)]

    section = certify_section()
    assert section["ambient_bundle_dimension"] == 4
    assert section["phi0_link_shift"] * 2 == section["normal_link_length"]
    assert section["beta_product_levels"] == 32
    assert len(section["cases"]) == 4
    for shift, case in enumerate(section["cases"]):
        assert case["constant_clutch_shift"] == shift
        assert case["zero_f_vector"] == case["push_f_vector"]
        assert case["signed_intersections"] == []
        assert case["self_intersection"] == 0
        assert case["normal_link_length_range"] == [8, 8]

    return {
        "format": "luttinger-pl-theorem-hypotheses-v1",
        "source_certificates": {
            flip_path.name: _sha256(flip_path),
            fiber_path.name: _sha256(fiber_path),
        },
        "bistellar_application": {
            "verified_flip_balls": flip["flips"],
            "all_vertex_links_classified_by_finite_surface_data": True,
            "boundary_is_two_marked_fibers": True,
            "untouched_region_is_literal_product": True,
        },
        "ribbon_application": {
            "marked_codes_identical": True,
            "equivariance_checked_on_every_directed_curve_end": True,
            "p_O_disk_faces_preserved": True,
            "explicit_common_subdivision_on_every_segment": True,
        },
        "intersection_application": {
            "ambient_bundle_dimension": section["ambient_bundle_dimension"],
            "constant_clutching_cases": len(section["cases"]),
            "normal_push_offs_disjoint": True,
            "radial_chain_boundary_exact": True,
            "self_intersection": 0,
        },
        "external_statements_only": [
            "classification of compact connected triangulated surfaces",
            "the standard trace interpretation of a 2-2 bistellar move",
            "rotation-system thickening and PL coning over disk faces",
            "low-dimensional PL smoothing and intersection naturality",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=ROOT / "pl_theorem_hypotheses.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    certificate = audit()
    encoded = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.check:
        assert args.output.read_text(encoding="ascii") == encoded
        print(f"PASS: {args.output} exactly reproduced")
    else:
        args.output.write_text(encoded, encoding="ascii")
        print(f"wrote {args.output}")
    print("PASS: all finite PL-theorem hypotheses are bound to certificates")


if __name__ == "__main__":
    main()
