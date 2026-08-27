#!/usr/bin/env python3
"""Check the explicit dependency boundary of the arXiv:2608.17267 audit.

This is a proof ledger, not a proof assistant. It prevents a machine result,
a cited theorem, and a geometric identification from silently being treated
as the same kind of evidence.
"""

from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

NODES = {
    "T_rotation_system_thickening": ("external_theorem", (), None),
    "T_elementary_bistellar_trace": ("external_theorem", (), None),
    "T_surface_classification": ("external_theorem", (), None),
    "T_contractible_PL3_ball": ("external_theorem", (), None),
    "T_cyclic_knot_unknot": ("external_theorem", (), None),
    "T_simplicial_pi1_presentation": ("external_theorem", (), None),
    "T_tietze": ("external_theorem", (), None),
    "T_freedman_HK": ("external_theorem", (), None),
    "T_symplectic_kodaira": ("external_theorem", (), None),
    "T_symplectic_thom": ("external_theorem", (), None),
    "T_rokhlin_arf": ("external_theorem", (), None),
    "T_HF_mixed": ("external_theorem", (), None),
    "T_periodic_disk_involution": (
        "external_theorem", (),
        "notes/lemma71_equivariant_normal_form_2026-08-27.md"),

    "M_marked_fiber": ("machine_certificate", (), "runs/22-model-correspondence-and-framing.txt"),
    "M_based_monodromy": ("machine_certificate", (), "runs/12-based-generators-and-table-relations.txt"),
    "M_bundle_tori": ("machine_certificate", (), "runs/22-model-correspondence-and-framing.txt"),
    "M_alternative_bundle": (
        "machine_certificate", (), "runs/31-alternative-marked-bundle.txt"),
    "M_alternative_based_monodromy": (
        "machine_certificate", (),
        "runs/32-alternative-based-monodromy.txt"),
    "M_PL_flip_trace": (
        "machine_certificate", (), "runs/33-local-pl-flip-trace.txt"),
    "M_independent_marked_fiber": (
        "machine_certificate", (), "runs/34-independent-marked-fiber.txt"),
    "M_PL_theorem_hypotheses": (
        "machine_certificate", (), "runs/36-pl-theorem-boundary.txt"),
    "M_complement_theorem_hypotheses": (
        "machine_certificate", (), "runs/38-complement-presentation-boundary.txt"),
    "M_torus_local_flatness": (
        "machine_certificate", (), "runs/48-torus-local-flatness.txt"),
    "M_frontier_normal_equivalence": (
        "machine_certificate", (),
        "runs/49-frontier-normal-equivalence.txt"),
    "M_topological_smooth_reroute": (
        "machine_certificate", (),
        "runs/50-topological-smooth-reroute.txt"),
    "M_relative_marked_monodromy": (
        "machine_certificate", (),
        "runs/51-relative-marked-monodromy.txt"),
    "M_explicit_graph_clutching": (
        "machine_certificate", (),
        "runs/52-explicit-graph-clutching.txt"),
    "M_interpretation_dictionary": (
        "machine_certificate", (),
        "runs/53-interpretation-dictionary.txt"),
    "M_independent_paper_dictionary": (
        "machine_certificate", (),
        "runs/54-independent-paper-dictionary.txt"),
    "M_lemma71_normal_form": (
        "machine_certificate", (),
        "runs/55-lemma71-equivariant-normal-form.txt"),
    "M_complement_tietze": ("machine_certificate", (), "runs/11-proof-certificate-and-group-attacks.txt"),
    "M_peripheral_slopes": ("machine_certificate", (), "runs/20-direct-peripheral-fillings-trivial.txt"),
    "M_independent_peripheral_extraction": (
        "machine_certificate", (),
        "runs/30-independent-peripheral-extractor.txt"),
    "M_R3": ("machine_certificate", (), "runs/23-drilled-fiber-relation.txt"),
    "M_RWS_replay": ("machine_certificate", (), "runs/21-rewriting-system-export-and-replay.txt"),
    "M_filled_group_derivations": (
        "machine_certificate", (),
        "runs/29-independent-filled-group-certificates.txt"),
    "M_framing_inline_calculus": (
        "machine_certificate", (),
        "runs/35-framing-lemma-referee-packet.txt"),
    "M_weinstein_chart_first_jet": (
        "machine_certificate", (),
        "runs/43-weinstein-chart-independence.txt"),
    "M_direct_equivariant_moser": (
        "machine_certificate", (),
        "runs/46-direct-equivariant-moser.txt"),
    "M_cumulative_moser_flow": (
        "machine_certificate", (),
        "runs/47-cumulative-moser-flow.txt"),
    "M_downstream_algebra": ("machine_certificate", (), "runs/24-downstream-theorem-audit.txt"),
    "M_section_PL_push_off": ("machine_certificate", (), "runs/28-pl-self-intersection-certificate.txt"),

    "G_equivariant_normal_form": (
        "geometric_argument",
        ("M_lemma71_normal_form", "T_periodic_disk_involution"),
        "notes/lemma71_equivariant_normal_form_2026-08-27.md"),

    "G_marked_bundle_identification": (
        "geometric_argument",
        ("M_marked_fiber", "M_independent_marked_fiber",
         "M_based_monodromy", "M_bundle_tori",
         "M_alternative_bundle", "M_alternative_based_monodromy",
         "M_PL_flip_trace", "M_PL_theorem_hypotheses",
         "M_interpretation_dictionary",
         "G_equivariant_normal_form",
         "G_topological_smooth_reroute",
         "T_elementary_bistellar_trace"),
        "notes/surface_bundle_referee_packet_2026-08-26.md"),
    "G_topological_smooth_reroute": (
        "geometric_argument",
        ("M_topological_smooth_reroute", "M_relative_marked_monodromy",
         "M_explicit_graph_clutching", "M_independent_paper_dictionary",
         "M_independent_marked_fiber",
         "M_PL_flip_trace", "T_rotation_system_thickening",
         "T_elementary_bistellar_trace"),
        "notes/topological_smooth_reroute_2026-08-27.md"),
    "G_weinstein_chart_independence": (
        "geometric_argument", ("M_weinstein_chart_first_jet",),
        "notes/lemma82_chart_independence_2026-08-26.md"),
    "G_constructive_relative_moser": (
        "geometric_argument", ("M_cumulative_moser_flow",),
        "notes/lemma82_cumulative_moser_flow_2026-08-26.md"),
    "G_direct_equivariant_moser": (
        "geometric_argument",
        ("M_direct_equivariant_moser", "G_constructive_relative_moser"),
        "notes/lemma82_direct_equivariant_moser_2026-08-26.md"),
    "G_lagrangian_framing": (
        "geometric_argument",
        ("M_framing_inline_calculus", "G_direct_equivariant_moser",
         "G_weinstein_chart_independence"),
        "notes/framing_lemma_referee_packet_2026-08-25.md"),
    "G_peripheral_identification": (
        "geometric_argument",
        ("G_marked_bundle_identification", "G_lagrangian_framing",
         "M_peripheral_slopes", "M_independent_peripheral_extraction",
         "M_independent_paper_dictionary"),
        "notes/peripheral_identification_lemma_2026-08-24.md"),
    "G_section_square_zero": (
        "geometric_argument",
        ("G_marked_bundle_identification", "M_section_PL_push_off",
         "M_PL_theorem_hypotheses", "G_topological_smooth_reroute"),
        "notes/pl_self_intersection_certificate_2026-08-24.md"),
    "G_torus_local_flatness": (
        "geometric_argument",
        ("M_torus_local_flatness", "T_surface_classification",
         "T_contractible_PL3_ball", "T_cyclic_knot_unknot"),
        "notes/torus_local_flatness_2026-08-27.md"),
    "G_derived_frontier_identification": (
        "geometric_argument",
        ("G_torus_local_flatness", "M_complement_theorem_hypotheses",
         "M_frontier_normal_equivalence"),
        "notes/frontier_normal_equivalence_2026-08-27.md"),

    "C_correct_filled_presentation": (
        "derived_claim",
        ("G_peripheral_identification", "M_complement_tietze", "M_R3",
         "G_derived_frontier_identification",
         "T_simplicial_pi1_presentation", "T_tietze"),
        "notes/complement_presentation_referee_packet_2026-08-26.md"),
    "C_pi1_V_trivial": (
        "derived_claim",
        ("C_correct_filled_presentation", "M_filled_group_derivations"), None),
    "C_no_square_zero_torus": (
        "derived_claim",
        ("C_pi1_V_trivial", "G_section_square_zero",
         "M_downstream_algebra", "T_symplectic_thom"), None),
    "C_exotic_S2xS2": (
        "derived_claim",
        ("C_pi1_V_trivial", "M_downstream_algebra",
         "T_freedman_HK", "T_symplectic_kodaira"), None),
    "C_slicing_pair": (
        "derived_claim",
        ("C_exotic_S2xS2", "C_no_square_zero_torus",
         "T_rokhlin_arf", "T_freedman_HK"), None),
    "C_exotic_CP2bar": (
        "derived_claim",
        ("C_pi1_V_trivial", "M_downstream_algebra",
         "T_freedman_HK", "T_HF_mixed"), None),
}


def file_digest(relative):
    path = ROOT / relative
    assert path.is_file(), f"missing evidence: {relative}"
    return sha256(path.read_bytes()).hexdigest()


def check_graph():
    visiting, done = set(), set()

    def visit(name):
        assert name in NODES, f"unknown dependency: {name}"
        if name in done:
            return
        assert name not in visiting, f"dependency cycle through {name}"
        visiting.add(name)
        for dependency in NODES[name][1]:
            visit(dependency)
        visiting.remove(name)
        done.add(name)

    for node in NODES:
        visit(node)
    assert done == set(NODES)


def main():
    check_graph()
    evidence = []
    for name, (kind, _, relative) in NODES.items():
        if relative:
            evidence.append((name, kind, relative, file_digest(relative)))

    kinds = {}
    for kind, _, _ in NODES.values():
        kinds[kind] = kinds.get(kind, 0) + 1

    print("PASS: proof ledger is closed, acyclic, and all evidence files exist")
    print("nodes:", ", ".join(f"{kind}={count}"
                              for kind, count in sorted(kinds.items())))
    print("explicit trust boundary:")
    for name, (kind, _, _) in NODES.items():
        if kind in {"external_theorem", "software_trust", "geometric_argument"}:
            print(f"  {kind}: {name}")
    print(f"bound evidence files: {len(evidence)}")


if __name__ == "__main__":
    main()
