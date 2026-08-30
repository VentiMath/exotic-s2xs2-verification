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
    # Downstream external inputs, each stated with its hypotheses in
    # luttinger/downstream_chain.py (run 64).
    "T_van_kampen": ("external_theorem", (), None),
    "T_covering_sequence": ("external_theorem", (), None),
    "T_duality_uct": ("external_theorem", (), None),
    "T_lattice_index": ("external_theorem", (), None),
    "T_wu_formula": ("external_theorem", (), None),
    "T_freedman": ("external_theorem", (), None),
    "T_hambleton_kreck": ("external_theorem", (), None),
    "T_thurston_symplectic": ("external_theorem", (), None),
    "T_luttinger_symplectic": ("external_theorem", (), None),
    "T_lp_double_bundle": ("external_theorem", (), None),
    "T_lp_quotient_spin": ("external_theorem", (), None),
    "T_kawauchi_B": ("external_theorem", (), None),
    "T_asphericity": ("external_theorem", (), None),
    "T_kodaira_dimension": ("external_theorem", (), None),
    "T_ho_li": ("external_theorem", (), None),
    "T_symplectic_thom": ("external_theorem", (), None),
    "T_symplectic_cover_construction": ("external_theorem", (), None),
    "T_adjunction": ("external_theorem", (), None),
    "T_klug_relative_rochlin": ("external_theorem", (), None),
    "T_levine_arf": ("external_theorem", (), None),
    "T_trace_embedding": ("external_theorem", (), None),
    "T_ball_isotopy": ("external_theorem", (), None),
    "T_novikov": ("external_theorem", (), None),
    "T_lp_regluing": ("external_theorem", (), None),
    "T_lp_floer": ("external_theorem", (), None),
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
    "M_lp_source_figure": (
        "machine_certificate", (),
        "runs/56-lp-source-figure-audit.txt"),
    "M_complement_tietze": ("machine_certificate", (), "runs/11-proof-certificate-and-group-attacks.txt"),
    # Run 66: the seeded raw-complex-to-reduced-presentation transport is
    # sealed with its serialized input and replays under two standalone
    # checkers.  The committed four-generator transport certificate was
    # produced by an unseeded run whose input cannot be regenerated, so the
    # four-generator presentation's link to the raw complex rests on that
    # run's own replay of its fresh certificate — a software-trust node,
    # not a machine certificate.
    "M_sealed_tietze_transport": (
        "machine_certificate", (), "runs/66-sealed-tietze-transport.txt"),
    "S_unseeded_transport_generation": (
        "software_trust", ("M_complement_tietze",),
        "runs/20-direct-peripheral-fillings-trivial.txt"),
    "M_sealed_filled_group_derivations": (
        "machine_certificate", (), "runs/66-sealed-tietze-transport.txt"),
    "M_peripheral_slopes": ("machine_certificate", (), "runs/20-direct-peripheral-fillings-trivial.txt"),
    "M_alpha_coordinate_identity": (
        "machine_certificate", (),
        "luttinger/alpha_residual/certificate.json.gz"),
    "M_beta_coordinate_identity": (
        "machine_certificate", (),
        "luttinger/beta_residual/certificate.json.gz"),
    "M_independent_peripheral_extraction": (
        "machine_certificate", (),
        "runs/30-independent-peripheral-extractor.txt"),
    "M_R3": ("machine_certificate", (), "runs/23-drilled-fiber-relation.txt"),
    # Run 67: the run-23 based monodromy identity lives in the unpunctured
    # beta mapping cylinder.  This node is the missing complement-level
    # check: the whole mapping cylinder embeds at the paper's parallel beta
    # level with zero vertices on either surgery torus, and a basepoint grid
    # identifies its beta loop with the presentation's whiskered B.
    "M_R3_complement": (
        "machine_certificate", (),
        "runs/67-r3-complement-and-lp-disagreement.txt"),
    "M_RWS_replay": ("machine_certificate", (), "runs/21-rewriting-system-export-and-replay.txt"),
    "M_filled_group_derivations": (
        "machine_certificate", (),
        "runs/29-independent-filled-group-certificates.txt"),
    "M_second_filled_group_verifier": (
        "machine_certificate", (),
        "runs/57-second-certificate-verifier.txt"),
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
    "M_downstream_chain": (
        "machine_certificate", (), "runs/64-downstream-proof-chain.txt"),
    "M_section_PL_push_off": ("machine_certificate", (), "runs/28-pl-self-intersection-certificate.txt"),

    "G_equivariant_normal_form": (
        "geometric_argument",
        ("M_lemma71_normal_form", "M_lp_source_figure",
         "T_periodic_disk_involution"),
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
         "M_independent_paper_dictionary", "M_alpha_coordinate_identity",
         "M_beta_coordinate_identity"),
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
        ("G_peripheral_identification", "S_unseeded_transport_generation",
         "M_R3", "M_R3_complement",
         "G_derived_frontier_identification",
         "T_simplicial_pi1_presentation", "T_tietze"),
        "notes/complement_presentation_referee_packet_2026-08-26.md"),
    # The load-bearing chain is the sealed one (run 66): serialized raw
    # complex -> replayed Tietze transport -> 3-generator presentation ->
    # eight derivation certificates, all replayed from frozen files by two
    # checkers each.  The earlier four-generator chain reaches the same
    # eight verdicts through the unseeded transport and is retained as an
    # independent corroborating derivation that nothing depends on.
    "C_correct_sealed_filled_presentation": (
        "derived_claim",
        ("G_peripheral_identification", "M_sealed_tietze_transport", "M_R3",
         "M_R3_complement",
         "G_derived_frontier_identification",
         "T_simplicial_pi1_presentation", "T_tietze"),
        "notes/complement_presentation_referee_packet_2026-08-26.md"),
    "C_pi1_V_trivial": (
        "derived_claim",
        ("C_correct_sealed_filled_presentation",
         "M_sealed_filled_group_derivations",
         "M_second_filled_group_verifier"), None),
    "C_pi1_V_trivial_unseeded_chain": (
        "derived_claim",
        ("C_correct_filled_presentation", "M_filled_group_derivations",
         "M_second_filled_group_verifier"), None),
    # The downstream chain (run 64): every step below is an item of
    # luttinger/downstream_chain_certificate.json, replayed by two checkers.
    "C_homology_of_V": (
        "derived_claim",
        ("C_pi1_V_trivial", "M_downstream_chain", "T_duality_uct",
         "T_wu_formula", "T_lp_double_bundle"), None),
    "C_pi1_double_trivial": (
        "derived_claim",
        ("C_pi1_V_trivial", "T_van_kampen", "T_lp_double_bundle",
         "T_lp_regluing"), None),
    "C_Z_form_hyperbolic": (
        "derived_claim",
        ("C_pi1_double_trivial", "G_section_square_zero",
         "M_downstream_chain", "T_lattice_index", "T_wu_formula",
         "T_duality_uct", "T_lp_double_bundle"), None),
    "C_Z_homeomorphic_S2xS2": (
        "derived_claim", ("C_Z_form_hyperbolic", "T_freedman"), None),
    "C_Z_symplectic": (
        "derived_claim",
        ("T_lp_double_bundle", "T_thurston_symplectic",
         "G_lagrangian_framing", "T_luttinger_symplectic",
         "C_Z_form_hyperbolic"), None),
    "C_Z_not_diffeomorphic_S2xS2": (
        "derived_claim",
        ("C_Z_symplectic", "T_asphericity", "T_kodaira_dimension",
         "T_ho_li", "M_downstream_chain"), None),
    "C_theorem_A_exotic_S2xS2": (
        "derived_claim",
        ("C_Z_homeomorphic_S2xS2", "C_Z_not_diffeomorphic_S2xS2"), None),
    "C_W_invariants": (
        "derived_claim",
        ("C_pi1_double_trivial", "T_lp_quotient_spin",
         "T_covering_sequence", "M_downstream_chain", "C_homology_of_V",
         "T_duality_uct"), None),
    "C_W_homeomorphic_B": (
        "derived_claim",
        ("C_W_invariants", "T_kawauchi_B", "T_hambleton_kreck",
         "M_downstream_chain"), None),
    "C_no_square_zero_torus": (
        "derived_claim",
        ("C_Z_symplectic", "C_Z_form_hyperbolic",
         "T_symplectic_cover_construction", "T_symplectic_thom",
         "M_downstream_chain"), None),
    "C_figure_eight_not_slice_W": (
        "derived_claim",
        ("C_W_invariants", "T_trace_embedding", "T_klug_relative_rochlin",
         "T_levine_arf", "T_covering_sequence", "T_duality_uct",
         "C_no_square_zero_torus", "M_downstream_chain"), None),
    "C_theorem_B_slicing_pair": (
        "derived_claim",
        ("C_W_homeomorphic_B", "C_figure_eight_not_slice_W",
         "T_kawauchi_B", "T_ball_isotopy"), None),
    "C_Zpp_form_odd": (
        "derived_claim",
        ("C_pi1_double_trivial", "T_novikov", "T_lp_regluing",
         "T_lattice_index", "M_downstream_chain", "T_duality_uct"), None),
    "C_Zpp_homeomorphic_CP2": (
        "derived_claim", ("C_Zpp_form_odd", "T_freedman"), None),
    "C_Zpp_not_diffeomorphic_CP2": (
        "derived_claim",
        ("C_Z_symplectic", "T_adjunction", "C_homology_of_V",
         "C_Zpp_form_odd", "T_lp_floer", "M_downstream_chain"), None),
    "C_theorem_C_exotic_CP2": (
        "derived_claim",
        ("C_pi1_double_trivial", "C_Zpp_homeomorphic_CP2",
         "C_Zpp_not_diffeomorphic_CP2"), None),
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
