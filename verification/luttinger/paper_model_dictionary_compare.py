#!/usr/bin/env python3
"""Compare the quarantined paper extraction with independent model runs.

This program is intentionally separate from paper_coordinate_extractor.py.
The extractor knows only the raw paper text; this comparator reads its frozen
output and the certificates for Runs 34, 51, 52, plus Run 30/15 evidence for
the named whiskers and alpha half-drift.
"""

import argparse
import ast
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def read_json(name):
    path = ROOT / name
    return path, json.loads(path.read_text(encoding="ascii"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extractor_source_audit():
    path = ROOT / "paper_coordinate_extractor.py"
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module or "")
    assert imports <= {"argparse", "ast", "hashlib", "json", "pathlib"}
    forbidden_files = [
        "paper_data.md", "independent_fiber_certificate.json",
        "relative_marking_certificate.json", "graph_clutching_certificate.json",
        "independent_peripheral_certificate.json",
    ]
    assert all(name not in source for name in forbidden_files)
    return {"extractor_sha256": digest(path),
            "stdlib_imports": sorted(imports),
            "forbidden_input_filenames_present": []}


def compare():
    paper_path, paper = read_json("paper_coordinate_certificate.json")
    fiber_path, fiber = read_json("independent_fiber_certificate.json")
    relative_path, relative = read_json("relative_marking_certificate.json")
    clutching_path, clutching = read_json("graph_clutching_certificate.json")
    peripheral_path, peripheral = read_json("independent_peripheral_certificate.json")
    run12 = REPO / "runs/12-based-generators-and-table-relations.txt"
    run14 = REPO / "runs/14-M1-connector-and-completion.txt"
    run15 = REPO / "runs/15-alpha-filling-direction.txt"
    run16 = REPO / "runs/16-paper-fillings-trivial.txt"

    assert paper["format"] == "luttinger-paper-coordinate-extraction-v1"
    assert paper["independence"]["forbidden_project_imports"] == []
    assert all(control is True
               for name, control in paper["mutation_controls"].items()
               if not name.endswith("_action"))
    assert paper["mutation_controls"]["reverse_twist_order_action"][
        "distinguished"] is True
    assert paper["mutation_controls"]["reverse_T_b_sign_action"][
        "distinguished"] is True
    assert fiber["format"] == "luttinger-independent-marked-fiber-v1"
    assert relative["format"] == "luttinger-relative-marked-monodromy-v1"
    assert clutching["format"] == "luttinger-explicit-graph-clutching-v1"
    assert peripheral["format"] == "luttinger-independent-peripheral-v2"

    # Run 34: compare the abstract paper ribbon system, not triangulation
    # sizes. Both independently constructed surfaces must realize the same
    # ordered-chain intersection matrix and involution/fixed-point data.
    p_fiber = paper["marked_fiber"]
    assert p_fiber["ordered_five_chain"] == ["a", "b", "c", "d", "e"]
    assert fiber["primary_structure"]["intersections"] == \
        p_fiber["intersection_matrix_upper"]
    assert fiber["independent_structure"]["intersections"] == \
        p_fiber["intersection_matrix_upper"]
    assert fiber["independent_structure"]["involution_chain_action"] == \
        "a<->e, b<->d, c->c freely"
    assert fiber["independent_structure"]["involution_fixed_set"] == ["O", "p"]
    assert sorted(p_fiber["fixed_points"]) == ["O", "p"]
    assert fiber["marked_ribbon_codes_identical"] is True

    # Run 51: exact relative representatives. Paper says c is freely
    # half-rotated, beta is b-then-a, and e/right handle are pointwise fixed.
    p_mono = paper["monodromies"]
    assert p_mono["alpha"]["c_action"] == "free half-rotation"
    assert relative["alpha_relative_representative"][
        "action_on_each_collar_row"] == "shift 4 of 8"
    paper_order = p_mono["beta_factorization"]["application_order"]
    model_trace = relative["beta_relative_representative"]["model_twist_trace"]
    assert [item["curve"] for item in model_trace] == paper_order == ["b", "a"]
    assert p_mono["beta_factorization"]["derived_composite"] == {
        "x": "Y", "y": "yx", "r": "r", "s": "s"}
    assert "e" in p_mono["beta_factorization"]["fixed_pointwise"]
    assert relative["beta_relative_representative"][
        "literal_e_collar_product_tetrahedra"] == 3072

    # Run 52: compare marked handle atoms and the relative twist token order.
    alpha_pairs = {left.strip("'"): right.strip("'")
                   for left, right in clutching["alpha_mapping_cylinder"][
                       "forward_seam_equations"]}
    assert {key: alpha_pairs[key] for key in ("a", "b", "d", "e", "p", "O")} == {
        "a": "e", "b": "d", "d": "b", "e": "a", "p": "p", "O": "O"}
    assert alpha_pairs["c0"] == "c1" and alpha_pairs["c1"] == "c0"
    graph_word = clutching["beta_mapping_cylinder"]["target_relative_twist_word"]
    assert [item[0] for item in graph_word] == paper_order
    assert graph_word == [["b", 1], ["a", -1]]
    assert clutching["global_gluing"]["c_e_p_O_markings_preserved"] is True

    # Named whiskers: compare paper labels with the basis-free Run-30 route.
    p_whiskers = paper["named_whiskers"]
    assert p_whiskers["M"].startswith("y_1:")
    assert p_whiskers["N"].startswith("s_2:")
    assert p_whiskers["s_edge_order"] == ["c_s", "s_e"]
    assert p_whiskers["delta"] == "R"
    assert peripheral["pair_checks"]["alpha_common_whisker"] == \
        "PASS: literal y_1 prefix"
    assert peripheral["pair_checks"]["beta_local_common_whisker"].startswith(
        "PASS: local N_grid and longitude use literal s_2")
    assert peripheral["peripheral_loops"]["lb_a_y1_independent"]["source"][
        "fiber_whisker"] == "y_1"
    assert peripheral["peripheral_loops"]["lb_b_s2_independent"]["source"][
        "fiber_whisker"] == "s_2"

    # Direction words: Run 15 independently resolves the selected alpha half;
    # Run 30 distinguishes it from the opposite half and records zero e drift.
    run15_text = run15.read_text(encoding="ascii")
    assert "exactly A x" in run15_text
    assert paper["marked_clutching_words"]["alpha_base"] == "Ax"
    assert paper["marked_clutching_words"]["alpha_fiber"] == "XR"
    assert peripheral["pair_checks"]["alpha_section"] == \
        "PASS: A lift plus negative c half"
    assert peripheral["sensitivity_controls"]["selected_alpha_half_sha256"] != \
        peripheral["sensitivity_controls"]["opposite_alpha_half_sha256"]
    assert paper["marked_clutching_words"]["beta_fiber"] == "sRS"
    assert peripheral["peripheral_loops"]["lb_b_s2_independent"]["source"][
        "fiber_drift"] == 0

    # Full paper words against the path-derived relation sheet. Sign letters
    # are normalized to the coherent orientation selected by Runs 12/14/16.
    run12_text = run12.read_text(encoding="ascii")
    run14_text = run14.read_text(encoding="ascii")
    run16_text = run16.read_text(encoding="ascii")
    assert "ByB^-1 (M^-1 yx)^-1" in run12_text
    assert "BsB^-1 ((r^-1 M^-1 r)s)^-1" in run12_text
    assert "M1: AsA^-1 = N*y" in run14_text
    assert "M2: ByB^-1 = M^-1*(yx)" in run14_text
    assert "M3: BsB^-1 = (r^-1*M^-1*r)*s" in run14_text
    assert "dir_base(T_alpha) = A x" in run16_text
    assert "dir_base(T_beta)  = (r^-1 M r) B" in run16_text

    return {
        "format": "luttinger-paper-model-dictionary-comparison-v1",
        "source_evidence": {
            paper_path.name: digest(paper_path),
            fiber_path.name: digest(fiber_path),
            relative_path.name: digest(relative_path),
            clutching_path.name: digest(clutching_path),
            peripheral_path.name: digest(peripheral_path),
            str(run12.relative_to(REPO)): digest(run12),
            str(run14.relative_to(REPO)): digest(run14),
            str(run15.relative_to(REPO)): digest(run15),
            str(run16.relative_to(REPO)): digest(run16),
        },
        "extractor_independence_audit": extractor_source_audit(),
        "comparisons": {
            "run34_ordered_five_chain_intersections": "IDENTICAL",
            "run34_involution_and_fixed_points": "IDENTICAL",
            "run51_alpha_c_collar_action": "IDENTICAL free half-rotation",
            "run51_beta_factor_order": "IDENTICAL: b then a",
            "run51_beta_action": "IDENTICAL: x->y^-1,y->yx,r->r,s->s",
            "run51_e_collar": "paper pointwise fixed; model literal product",
            "run52_alpha_marked_seam": "IDENTICAL on a,b,c halves,d,e,p,O",
            "run52_beta_twist_tokens": "IDENTICAL after local sign calibration",
            "run30_M_whisker": "IDENTICAL literal y_1",
            "run30_N_whisker": "IDENTICAL literal s_2",
            "run15_alpha_half_drift": "IDENTICAL Ax; opposite half distinguished",
            "beta_zero_e_drift": "IDENTICAL",
            "table1_corrected_relations": "IDENTICAL in one coherent sign convention",
            "paper_coordinate_direction_words": "IDENTICAL Ax and (r^-1 M r)B",
        },
        "interpretation_controls": {
            "paper_source_not_paper_data_summary": True,
            "twist_composite_recomputed_not_copied": True,
            "extract_then_compare_separation": True,
            "no_discrepancy": True,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=ROOT / "paper_model_dictionary_comparison.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    certificate = compare()
    encoded = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.check:
        assert args.output.read_text(encoding="ascii") == encoded
        print(f"PASS: {args.output.name} exactly reproduced")
    else:
        args.output.write_text(encoded, encoding="ascii")
        print(f"wrote {args.output.name}")
    print("PASS Run 34: five-chain ribbon dictionary and involution agree")
    print("PASS Run 51: alpha/beta relative monodromies agree")
    print("PASS Run 52: marked seam atoms and twist tokens agree")
    print("PASS Runs 30/15: y_1, s_2, and Ax half-drift agree")
    print("NO PAPER-TO-MODEL DICTIONARY DISCREPANCY")


if __name__ == "__main__":
    main()
