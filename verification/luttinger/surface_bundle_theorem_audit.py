#!/usr/bin/env python3
"""Bind the finite hypotheses of the marked-surface-bundle theorem.

This does not prove bundle classification or Dehn--Nielsen--Baer.  It checks
that the particular application in this audit has exactly the advertised
base, fiber, monodromy, and relative markings, and binds those claims to the
independent certificates already in the repository.
"""

import argparse
import gzip
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_json(name):
    path = ROOT / name
    return path, json.loads(path.read_text(encoding="ascii"))


def _free_reduce(word):
    out = []
    for letter in word:
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def _inverse(word):
    return [-letter for letter in reversed(word)]


def _substitute(word, images):
    out = []
    for letter in word:
        image = images[abs(letter)]
        out.extend(image if letter > 0 else _inverse(image))
    return _free_reduce(out)


def _cyclically_equal(left, right):
    left, right = _free_reduce(left), _free_reduce(right)
    if len(left) != len(right):
        return False
    doubled = left + left
    return any(doubled[i:i + len(left)] == right for i in range(len(left)))


def audit():
    fiber_path, fiber = _read_json("independent_fiber_certificate.json")
    alternative_path, alternative = _read_json("alternative_bundle_certificate.json")
    relative_path, relative = _read_json("relative_marking_certificate.json")
    based_path = ROOT / "alternative_based_monodromy.json.gz"
    with gzip.open(based_path, "rt", encoding="ascii") as stream:
        based = json.load(stream)
    primary_run = REPO / "runs/12-based-generators-and-table-relations.txt"

    # Annulus plus one orientation-preserving band joining its two boundary
    # components: chi drops by one, the two boundary components join, and the
    # resulting connected orientable surface has genus one and one boundary.
    annulus_chi = 0
    base_chi = annulus_chi - 1
    base_boundary = 1
    base_genus = (2 - base_boundary - base_chi) // 2
    assert (base_chi, base_boundary, base_genus) == (-1, 1, 1)
    spine_vertices, spine_edges = 1, 2
    assert spine_edges - spine_vertices + 1 == 2

    assert fiber["format"] == "luttinger-independent-marked-fiber-v1"
    assert fiber["independent_structure"]["chi"] == -2
    assert fiber["primary_structure"]["chi"] == -2
    assert fiber["marked_ribbon_codes_identical"] is True
    assert fiber["independent_structure"]["involution_chain_action"] == \
        "a<->e, b<->d, c->c freely"
    assert set(fiber["equivariant_data_checked"]) == {
        "named crossing rotations", "two disk faces labeled p and O",
        "involution on every directed curve end", "p and O fixed",
    }

    primary_text = primary_run.read_text(encoding="ascii")
    assert "phi0(x,y)=(r,s) as vertex paths" in primary_text
    assert "x -> y^-1,  y -> yx,  r -> r,  s -> s" in primary_text
    assert "17,839 elementary Tietze eliminations" in primary_text

    assert based["based_monodromy"]["claim"] == \
        "x->y^-1, y->yx, r->r, s->s"
    assert based["based_monodromy"]["interfaces"] == 64
    assert based["based_monodromy"]["residuals_after_dehn"] == {
        "r": [], "s": [], "x": [], "y": []}
    assert based["based_monodromy"]["import_audit"][
        "forbidden_primary_modules_absent"] == [
            "bundle", "layers", "paper_bridge"]

    assert alternative["format"] == "luttinger-alternative-bundle-v1"
    assert alternative["structure"]["beta_interfaces"] == 64
    assert alternative["peripheral_comparison"][
        "marked_crossings_and_whiskers"] == "IDENTICAL"
    assert alternative["peripheral_comparison"]["result"].startswith("PASS:")

    assert relative["format"] == "luttinger-relative-marked-monodromy-v1"
    assert relative["collars"]["c"]["is_triangulated_annulus"] is True
    assert relative["collars"]["e"]["is_triangulated_annulus"] is True
    assert relative["alpha_relative_representative"][
        "full_c_collar_preserved"] is True
    assert relative["beta_relative_representative"][
        "paper_word"] == "T_a o T_b (T_b first)"
    assert relative["beta_relative_representative"][
        "literal_e_collar_product_tetrahedra"] == 3072
    assert relative["conclusion"]["relative_isotopy_extension_required"] is False

    # x,y,r,s are 1,2,3,4.  The closed oriented surface relator is checked
    # only as a conjugacy class because closed-surface DNB lands in Out(pi1).
    relator = [1, 2, -1, -2, 3, 4, -3, -4]
    alpha = {1: [3], 2: [4], 3: [1], 4: [2]}
    beta = {1: [-2], 2: [2, 1], 3: [3], 4: [4]}
    assert _cyclically_equal(relator, _substitute(relator, alpha))
    assert _cyclically_equal(relator, _substitute(relator, beta))

    return {
        "format": "luttinger-surface-bundle-theorem-hypotheses-v1",
        "source_certificates": {
            fiber_path.name: _sha256(fiber_path),
            alternative_path.name: _sha256(alternative_path),
            relative_path.name: _sha256(relative_path),
            based_path.name: _sha256(based_path),
            str(primary_run.relative_to(REPO)): _sha256(primary_run),
        },
        "base_application": {
            "construction": "oriented annulus plus one band joining its boundary components",
            "genus": base_genus,
            "boundary_components": base_boundary,
            "euler_characteristic": base_chi,
            "spine": "one vertex and two loop edges",
            "spine_rank": spine_edges - spine_vertices + 1,
            "no_two_cell_coherence_condition": True,
        },
        "fiber_application": {
            "closed_oriented_genus": 2,
            "independent_marked_ribbon_equivalence": True,
            "p_O_fixed": True,
            "alpha_involution_on_c": "free half-rotation",
            "beta_on_e": "relative pointwise product",
        },
        "monodromy_application": {
            "alpha_based_action": "x<->r, y<->s",
            "beta_based_action": "x->y^-1, y->yx, r->r, s->s",
            "primary_beta_tietze_steps": 17839,
            "independent_beta_interfaces": 64,
            "independent_beta_residuals": "all empty after certified replay",
            "surface_relator_conjugacy_preserved": True,
            "based_actions_stronger_than_required_outer_actions": True,
        },
        "relative_marking_application": {
            "T_alpha_core_c_preserved": True,
            "T_beta_core_e_preserved_relative_to_a_neighborhood": True,
            "marked_crossings_and_whiskers_independently_identical": True,
            "relative_representatives_constructed_directly": True,
            "relative_isotopy_extension_required": False,
        },
        "external_statements_only": [
            "classification of bundles by homotopy classes into BDiff+(F)",
            "Dehn-Nielsen-Baer injectivity into Out(pi1(F))",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=ROOT / "surface_bundle_theorem_hypotheses.json")
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
    print("PASS: marked-surface-bundle theorem hypotheses bound to certificates")


if __name__ == "__main__":
    main()
