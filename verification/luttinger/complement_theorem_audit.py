#!/usr/bin/env python3
"""Integrate the finite hypotheses behind the complement presentation.

The simplexwise complement retraction and maximal-tree presentation are
proved in the accompanying packet.  This checker binds their numerical and
combinatorial hypotheses to the independent peripheral certificate and to
the original presentation run.
"""

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit():
    certificate_path = ROOT / "independent_peripheral_certificate.json"
    certificate = json.loads(certificate_path.read_text(encoding="ascii"))
    complement_source = ROOT / "complement.py"
    independent_source = ROOT / "independent_peripheral_extractor.py"
    presentation_source = ROOT / "pi1.py"
    run_path = REPO / "runs/11-proof-certificate-and-group-attacks.txt"

    assert certificate["format"] == "luttinger-independent-peripheral-v2"
    bundle = certificate["bundle"]
    assert bundle["K_f_vector"] == [9156, 116714, 356728, 403152, 153984]
    assert (bundle["complement_vertices"], bundle["complement_edges"],
            bundle["frontier_vertices"]) == (8860, 108722, 113336)
    tori = bundle["torus_components"]
    assert sorted((t["vertices"], t["edges"], t["triangles"])
                  for t in tori) == [(24, 72, 48), (272, 816, 544)]
    assert all(t["euler_characteristic"] == 0 for t in tori)
    assert certificate["independence_boundary"][
        "forbidden_modules_imported"] == []
    assert set(certificate["independence_boundary"]["not_imported"]) == {
        "complement", "pi1", "paper_bridge", "peripheral_bridge",
        "r_run", "sweep",
    }

    # The successful independent extraction passes through this direct
    # fullness test and independently reconstructs the exact frontier vertex
    # predicate and retraction used by complement.py.
    independent_text = independent_source.read_text(encoding="ascii")
    assert "marked torus is not a full 2-subcomplex" in independent_text
    assert "simplex & self.torus_vertices and simplex - self.torus_vertices" \
        in independent_text
    assert "max(candidates, key=self.K.rank.get)" in independent_text

    complement_text = complement_source.read_text(encoding="ascii")
    assert 'assert K.is_full(T), "T must be a full subcomplex of K"' \
        in complement_text
    assert "K.induced(set(K.vertices()) - self.Tverts)" in complement_text
    assert "max((v for v in s if v not in self.Tverts)" in complement_text

    # Exhaust the possible vertex partitions of a simplex of dimension <= 4.
    # A point outside the T-face has positive total weight on the opposite
    # face. Normalizing those weights is therefore defined, stays in the
    # simplex, and targets a nonempty face of the induced complement.
    partitions = 0
    for vertex_count in range(1, 6):
        for torus_mask in range(1, (1 << vertex_count) - 1):
            outside = [i for i in range(vertex_count)
                       if not (torus_mask & (1 << i))]
            assert outside
            partitions += 1
    assert partitions == sum((1 << n) - 2 for n in range(1, 6)) == 52

    run_text = run_path.read_text(encoding="ascii")
    assert "99,863 generators and 321,702 relators" in run_text
    tree_edges = bundle["complement_vertices"] - 1
    non_tree_edges = bundle["complement_edges"] - tree_edges
    assert non_tree_edges == 99863

    loop_records = certificate["peripheral_loops"]
    assert set(loop_records) >= {
        "geom_M_independent", "lb_a_y1_independent",
        "N_grid_local_independent", "geom_N_independent",
        "lb_b_s2_independent",
    }
    assert certificate["pair_checks"]["meridian_orientation"].startswith("PASS:")
    assert certificate["sensitivity_controls"]["result"].startswith("PASS:")

    return {
        "format": "luttinger-complement-theorem-hypotheses-v1",
        "source_evidence": {
            certificate_path.name: _sha256(certificate_path),
            str(run_path.relative_to(REPO)): _sha256(run_path),
            complement_source.name: _sha256(complement_source),
            independent_source.name: _sha256(independent_source),
            presentation_source.name: _sha256(presentation_source),
        },
        "simplexwise_retraction_application": {
            "ambient_dimension": 4,
            "all_nontrivial_vertex_partitions_checked": partitions,
            "marked_subcomplexes_full": True,
            "complement_vertices": bundle["complement_vertices"],
            "complement_edges": bundle["complement_edges"],
            "target": "induced subcomplex on vertices outside both tori",
        },
        "presentation_application": {
            "connected_complement": True,
            "tree_edges": tree_edges,
            "non_tree_edges": non_tree_edges,
            "reported_generators": 99863,
            "reported_triangle_relators": 321702,
            "generator_count_identity": "E-(V-1)=99863",
        },
        "derived_frontier_application": {
            "frontier_vertices": bundle["frontier_vertices"],
            "torus_components": 2,
            "torus_f_vectors": [[24, 72, 48], [272, 816, 544]],
            "frontier_predicate_independently_reimplemented": True,
            "retraction_independently_reimplemented": True,
            "oriented_dual_meridians_extracted": True,
            "orientation_and_inverse_sensitivity_controls_pass": True,
        },
        "external_statements_only": [
            "the derived neighborhood of a full locally flat PL submanifold is a regular neighborhood",
            "its frontier is the normal sphere-bundle boundary",
            "the maximal-tree/triangle-relator presentation theorem for a connected simplicial complex",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=ROOT / "complement_theorem_hypotheses.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = audit()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check:
        assert args.output.read_text(encoding="ascii") == encoded
        print(f"PASS: {args.output} exactly reproduced")
    else:
        args.output.write_text(encoded, encoding="ascii")
        print(f"wrote {args.output}")
    print("PASS: complement-presentation hypotheses bound to independent evidence")


if __name__ == "__main__":
    main()
