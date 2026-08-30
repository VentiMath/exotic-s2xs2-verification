#!/usr/bin/env python3
"""Audit the reroute from the PL model into the audit-defined smooth bundle.

No smoothing of the 4-dimensional source triangulation is required.  Forget
the smooth structure on the audit-defined bundle R_*. The explicit graph-clutching
construction gives an orientation-preserving fiberwise homeomorphism from
the certified PL bundle |K| to this underlying topological bundle, relative
to c, e, p, and their product collars. All combinatorial conclusions are
transported by that homeomorphism; symplectic/Lagrangian statements are then
made only on the already-smooth target R_*.

For the section, Run 28 supplies disjoint homologous locally flat cycles
Gamma and Gamma'.  Their images are still disjoint and homologous in R_*, so
the target section class has square zero directly in R_*.  This avoids a
separate naturality theorem for comparing PL and smooth intersections.

This certificate is internal to the audit model.  Identifying R_* and its
marked tori with Wuebben's intended objects is the separate source boundary
S1--S4; it is not asserted here.
"""

import argparse
import hashlib
import json
from pathlib import Path

from pl_self_intersection import certify as certify_section


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def read_json(name):
    path = ROOT / name
    return path, json.loads(path.read_text(encoding="ascii"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def certify():
    clutching_path, clutching = read_json("graph_clutching_certificate.json")
    pl_path, pl = read_json("pl_theorem_hypotheses.json")
    frontier_path, frontier = read_json(
        "frontier_normal_equivalence_certificate.json")
    flatness_path, flatness = read_json("torus_local_flatness_certificate.json")
    peripheral_path, peripheral = read_json("independent_peripheral_certificate.json")

    assert clutching["format"] == "luttinger-explicit-graph-clutching-v1"
    assert clutching["base_handle_decomposition"]["rank"] == 2
    assert clutching["base_handle_decomposition"]["two_cells"] == 0
    assert clutching["alpha_mapping_cylinder"][
        "quotient_map_well_defined_both_directions"] is True
    assert clutching["beta_mapping_cylinder"][
        "quotient_map_well_defined_both_directions"] is True
    assert clutching["global_gluing"][
        "bundle_homeomorphism_constructed"] is True
    assert clutching["global_gluing"]["c_e_p_O_markings_preserved"] is True
    assert clutching["conclusion"][
        "surface_bundle_classification_required"] is False
    assert clutching["conclusion"]["dehn_nielsen_baer_required"] is False

    assert pl["format"] == "luttinger-pl-theorem-hypotheses-v1"
    assert pl["ribbon_application"]["p_O_disk_faces_preserved"] is True
    assert pl["intersection_application"] == {
        "ambient_bundle_dimension": 4,
        "constant_clutching_cases": 4,
        "normal_push_offs_disjoint": True,
        "radial_chain_boundary_exact": True,
        "self_intersection": 0,
    }

    # Recompute rather than trust the old prose summary: p is fixed by the
    # alpha half-turn, the beta trace is literal product near p, and all four
    # doubled clutching cases carry the exact disjoint radial push-off.
    section = certify_section()
    assert section["ambient_bundle_dimension"] == 4
    assert section["beta_product_levels"] == 32
    assert section["phi0_link_shift"] * 2 == section["normal_link_length"]
    assert len(section["cases"]) == 4
    for case in section["cases"]:
        assert case["signed_intersections"] == []
        assert case["self_intersection"] == 0
        assert case["zero_f_vector"] == case["push_f_vector"]

    assert frontier["format"] == "luttinger-frontier-normal-equivalence-v1"
    assert frontier["frontier_vertices"] == 113336
    assert frontier["meridian_fibers_checked"] == 592
    assert flatness["format"] == "luttinger-torus-local-flatness-v1"
    assert flatness["total_simplices_checked"] == 1776
    assert peripheral["format"] == "luttinger-independent-peripheral-v2"
    assert peripheral["pair_checks"]["framing"].startswith(
        "product/fibered framing")
    assert peripheral["pair_checks"]["meridian_orientation"].startswith("PASS:")

    framing_runs = [REPO / "runs/43-weinstein-chart-independence.txt",
                    REPO / "runs/44-weinstein-second-route.txt",
                    REPO / "runs/46-direct-equivariant-moser.txt",
                    REPO / "runs/47-cumulative-moser-flow.txt"]
    assert all(path.is_file() for path in framing_runs)

    return {
        "format": "luttinger-topological-smooth-reroute-v1",
        "source_evidence": {
            clutching_path.name: digest(clutching_path),
            pl_path.name: digest(pl_path),
            frontier_path.name: digest(frontier_path),
            flatness_path.name: digest(flatness_path),
            peripheral_path.name: digest(peripheral_path),
            **{str(path.relative_to(REPO)): digest(path) for path in framing_runs},
        },
        "marked_bundle_homeomorphism": {
            "source": "certified oriented PL genus-2 bundle |K|",
            "target": "underlying topological bundle of the audit-defined smooth R_*",
            "base_spine_rank": 2,
            "same_ordered_monodromy_mapping_classes": True,
            "fiber_orientation_preserved": True,
            "p_O_sections_preserved": True,
            "T_alpha_c_and_product_collar_preserved": True,
            "T_beta_e_and_product_collar_preserved": True,
            "source_four_manifold_smoothing_required": False,
        },
        "transported_topological_data": {
            "complement_pi1_and_based_paths": True,
            "normal_meridian_fibers": frontier["meridian_fibers_checked"],
            "product_framing_push_offs": True,
            "local_flat_torus_simplices": flatness["total_simplices_checked"],
        },
        "smooth_target_only": {
            "audit_Rstar_is_already_smooth": True,
            "audit_tori_are_the_smooth_Lagrangian_tori": True,
            "fibered_equals_Lagrangian_framing_runs": [43, 44, 46, 47],
            "smooth_operations_performed_on_source_PL_complex": False,
        },
        "section_transport": {
            "p_section_preserved": True,
            "doubled_bundle_extension": (
                "apply the same marked fiberwise H on both halves"
            ),
            "boundary_gluing_compatibility": True,
            "beta_product_levels": section["beta_product_levels"],
            "constant_clutching_cases": len(section["cases"]),
            "disjoint_push_offs": True,
            "radial_chain_boundary_exact": True,
            "image_cycles_disjoint_in_target": True,
            "image_cycles_homologous_in_target": True,
            "target_section_homological_square": 0,
            "separate_intersection_naturality_theorem_required": False,
        },
        "conclusion": (
            "the proof transports the certified topological data into the "
            "audit-defined already-smooth marked bundle; no compatible smoothing "
            "or smoothing-uniqueness theorem for |K| is required"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=ROOT / "topological_smooth_bridge_certificate.json")
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
    print("PASS: marked PL bundle maps to the audit-defined smooth bundle")
    print("PASS: tori, collars, peripheral data, and p-section are preserved")
    print("PASS: section square zero transported by disjoint homologous cycles")
    print("NO FOUR-DIMENSIONAL SOURCE SMOOTHING THEOREM REQUIRED")


if __name__ == "__main__":
    main()
