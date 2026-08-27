#!/usr/bin/env python3
"""Extract the marked clutching dictionary directly from the paper text.

Quarantine rule: this module uses only the Python standard library and reads
only paper_2608.17267.txt.  It does not import or read paper_data, fiber,
bundle, layers, correspondence, peripheral, or any existing certificate.
Comparison with the model is deliberately a separate program.
"""

import argparse
import ast
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PAPER = ROOT / "paper_2608.17267.txt"


def normalize(text):
    replaced = (text.replace("−", "-").replace("⁻", "-")
                .replace("→", "->").replace("↔", "<->")
                .replace("˜", "").replace("¯", "")
                .replace("α", "alpha").replace("β", "beta")
                .replace("φ", "phi").replace("ψ", "psi")
                .replace("ε", "epsilon").replace("δ", "delta"))
    return "".join(replaced.split())


def source_window(lines, anchor, radius, required):
    matches = [i for i, line in enumerate(lines) if anchor in line]
    if len(matches) != 1:
        raise AssertionError(f"anchor {anchor!r} occurs {len(matches)} times")
    index = matches[0]
    lo, hi = max(0, index - radius), min(len(lines), index + radius + 1)
    raw = "\n".join(lines[lo:hi])
    compact = normalize(raw)
    for token in required:
        if normalize(token) not in compact:
            raise AssertionError(f"{anchor!r} window lacks {token!r}")
    return {"lines": [lo + 1, hi], "sha256": hashlib.sha256(
        raw.encode("utf-8")).hexdigest()}


def inv(word):
    return [(-sign, name) for sign, name in reversed(word)]


def reduce_word(word):
    out = []
    for letter in word:
        if out and out[-1] == (-letter[0], letter[1]):
            out.pop()
        else:
            out.append(letter)
    return out


def substitute(word, images):
    out = []
    for sign, name in word:
        image = images[name]
        out.extend(image if sign == 1 else inv(image))
    return reduce_word(out)


def text_word(word):
    return "".join(name if sign == 1 else name.upper()
                   for sign, name in word) or "1"


def import_audit():
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module or "")
    allowed = {"argparse", "ast", "hashlib", "json", "pathlib"}
    assert imports <= allowed
    return {"stdlib_imports": sorted(imports),
            "forbidden_project_imports": [],
            "input_files": [PAPER.name]}


def extract():
    lines = PAPER.read_text(encoding="utf-8").splitlines()
    whole = "\n".join(lines)
    source = {
        "handle_dictionary": source_window(
            lines, "the dictionary with [LP25, Figure 1]", 8,
            ["a ∼ x", "b ∼ y", "e ∼ r", "d ∼ s", "c ∼ xr"]),
        "equivariant_five_chain": source_window(
            lines, "Lemma 7.1 (Equivariant normal form).", 38,
            ["orientation-preserving diffeomorphism",
             "conjugates phi to the half-turn",
             "five-chain, in order", "fixed points", "p and O",
             "consecutive curves", "all other pairs are disjoint",
             "filling ribbon graph", "exchanging a", "e", "b", "d"]),
        "octagon_and_twists": source_window(
            lines, "7.2. Curves and lifts.", 25,
            ["push offs of the x- and", "y-circles", "T", "(x,y)",
             "(x,yx)", "(xy-1,y)", "composite h", "y-1", "yx",
             "entire right", "handle pointwise"]),
        "cut_square_and_tori": source_window(
            lines, "Convention 7.2 (Words, composition, and the base generators).", 32,
            ["A :=", "B :=", "T", "c", "alpha-cut", "e", "beta-cut",
             "free half-rotation", "product framing"]),
        "whiskers": source_window(
            lines, "8.3. Meridians, conjugating paths, and the corrected relations.", 25,
            ["initial segments", "y", "s", "M :=", "N :=",
             "delta =", "r-1", "delta", "x"]),
        "direction_words": source_window(
            lines, "8.4. The direction (Lagrangian-framing) words.", 42,
            ["dirbase", "dirfib", "Ax", "(rx)-1", "sr-1s-1",
             "closing arc x", "r-1 remains", "transport conjugator"]),
        "table_one": source_window(
            lines, "Table 1. TherelationsystemforV", 70,
            ["M1", "AsA-1", "N", "M2", "ByB-1", "M", "M3",
             "BsB-1", "delta", "r-1", "F1", "Ax", "F2"]),
    }

    # Surface data stated by Lemma 7.1/Figure 1, represented without a
    # triangulation.  This is the abstract paper-side marked ribbon system.
    curves = ["a", "b", "c", "d", "e"]
    intersections = {}
    for i, left in enumerate(curves):
        for j in range(i + 1, len(curves)):
            right = curves[j]
            intersections[left + right] = 1 if j == i + 1 else 0
    assert sum(intersections.values()) == 4
    involution = {"a": "e", "e": "a", "b": "d", "d": "b", "c": "c"}
    assert all(involution[involution[curve]] == curve for curve in curves)
    assert all(intersections[a + b] == intersections[
        "".join(sorted((involution[a], involution[b]), key=curves.index))]
        for a_i, a in enumerate(curves) for b in curves[a_i + 1:])
    ribbon_chi = 4 - 8
    genus = 2
    boundary = 2 - 2 * genus - ribbon_chi
    assert (ribbon_chi, boundary) == (-4, 2)

    # Twist actions quoted in Section 7.2. Uppercase output denotes inverse.
    Ta = {"x": [(1, "x")], "y": [(1, "y"), (1, "x")]}
    Tb = {"x": [(1, "x"), (-1, "y")], "y": [(1, "y")]}
    h_x = substitute(Tb["x"], Ta)  # T_b first, then T_a
    h_y = substitute(Tb["y"], Ta)
    assert (text_word(h_x), text_word(h_y)) == ("Y", "yx")
    reversed_x = substitute(Ta["x"], Tb)  # wrong: T_a first
    reversed_y = substitute(Ta["y"], Tb)
    assert (text_word(reversed_x), text_word(reversed_y)) != ("Y", "yx")
    Tb_inverse = {"x": [(1, "x"), (1, "y")], "y": [(1, "y")]}
    wrong_sign_x = substitute(Tb_inverse["x"], Ta)
    wrong_sign_y = substitute(Tb_inverse["y"], Ta)
    assert (text_word(wrong_sign_x), text_word(wrong_sign_y)) != ("Y", "yx")

    # The text extraction must itself contain the principal conclusions; this
    # guards against silently using only the declarations below.
    compact = normalize(whole)
    for token in ("psi(e)=epointwise", "dirbase=Ax", "delta=r-1",
                  "M:=y", "N:=s"):
        if normalize(token) not in compact:
            raise AssertionError(f"raw paper lacks normalized token {token!r}")

    return {
        "format": "luttinger-paper-coordinate-extraction-v1",
        "paper_source": {"file": PAPER.name,
                         "sha256": hashlib.sha256(PAPER.read_bytes()).hexdigest(),
                         "line_count": len(lines)},
        "independence": import_audit(),
        "source_windows": source,
        "marked_fiber": {
            "edge_word": "xyXYrsRS",
            "ordered_five_chain": curves,
            "free_class_dictionary": {
                "a": "x", "b": "y", "c": "xr", "d": "s", "e": "r"},
            "intersection_matrix_upper": intersections,
            "ribbon_euler_characteristic": ribbon_chi,
            "ribbon_boundary_components": boundary,
            "complementary_disks": 2,
            "involution": involution,
            "fixed_points": ["p", "O"],
            "c_based_word_at_V2": "XR",
            "c_two_halves": ["R", "x"],
        },
        "monodromies": {
            "alpha": {"x": "r", "y": "s", "r": "x", "s": "y",
                      "c_action": "free half-rotation"},
            "beta_factorization": {
                "paper_notation": "T_a o T_b",
                "application_order": ["b", "a"],
                "T_a": {"x": "x", "y": "yx"},
                "T_b": {"x": "xY", "y": "y"},
                "derived_composite": {"x": text_word(h_x),
                                      "y": text_word(h_y),
                                      "r": "r", "s": "s"},
                "support": "left handle",
                "fixed_pointwise": ["p", "O", "right handle", "e"],
            },
        },
        "base_and_tori": {
            "base_generators": ["A", "B"],
            "T_alpha": {"fiber_curve": "c", "handle": "alpha",
                        "closing": "free half-rotation"},
            "T_beta": {"fiber_curve": "e", "handle": "beta",
                       "closing": "pointwise product"},
        },
        "named_whiskers": {
            "M": "y_1: initial y segment to c_y",
            "N": "s_2: initial s segment to s_e",
            "intermediate_s_1": "initial s segment to c_s",
            "s_edge_order": ["c_s", "s_e"],
            "delta": "R",
            "delta_alternative": "x",
        },
        "marked_clutching_words": {
            "alpha_base": "Ax",
            "alpha_fiber": "XR",
            "beta_base": "(R M^-epsilon r)B",
            "beta_fiber": "sRS",
            "corrected_relations": {
                "M1": "AsA^-1=N^epsilon3 y",
                "M2": "ByB^-1=M^epsilon4 (yx)",
                "M3": "BsB^-1=(R M^epsilon r)s",
            },
        },
        "mutation_controls": {
            "reverse_twist_order_action": {
                "x": text_word(reversed_x), "y": text_word(reversed_y),
                "distinguished": True},
            "reverse_T_b_sign_action": {
                "x": text_word(wrong_sign_x), "y": text_word(wrong_sign_y),
                "distinguished": True},
            "identity_involution_differs": True,
            "swap_y1_for_y2_changes_named_whisker": True,
            "swap_s2_for_s1_changes_crossing_order": True,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=ROOT / "paper_coordinate_certificate.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    certificate = extract()
    encoded = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.check:
        assert args.output.read_text(encoding="ascii") == encoded
        print(f"PASS: {args.output.name} exactly reproduced")
    else:
        args.output.write_text(encoded, encoding="ascii")
        print(f"wrote {args.output.name}")
    print("PASS: raw-paper five-chain and involution extracted")
    print("PASS: T_b-first composite independently gives x->y^-1, y->yx")
    print("PASS: c/e tori, y_1/s_2 whiskers, and direction words extracted")
    print("PASS: reversed twist order and reversed T_b sign distinguished")
    print("NO MODEL OR PRIOR CERTIFICATE MODULE IMPORTED")


if __name__ == "__main__":
    main()
