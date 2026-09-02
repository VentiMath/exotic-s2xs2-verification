#!/usr/bin/env python3
"""Check the explicit dependency boundary of the arXiv:2608.17267 audit.

This is a proof ledger, not a proof assistant. It prevents a machine result,
a cited theorem, a geometric argument, and a source-identification assumption
from silently being treated as the same kind of evidence.
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

    # These are not mathematical theorems about the audit model.  They are
    # the fourteen clauses D1--D14 of Source Formalization D, needed to
    # compare that explicit model with Wuebben's pinned text and figures.
    # Keeping them as their own evidence kind prevents the ledger from
    # silently treating a source reading as a machine certificate.
    "A_Source_Formalization_D": (
        "source_assumption", (),
        "notes/source_identification_assumptions_2026-08-29.md"),

    "M_marked_fiber": ("machine_certificate", (), "runs/22-model-correspondence-and-framing.txt"),
    "M_based_monodromy": ("machine_certificate", (), "runs/12-based-generators-and-table-relations.txt"),
    "M_bundle_tori": ("machine_certificate", (), "runs/22-model-correspondence-and-framing.txt"),
    "M_alternative_bundle": (
        "machine_certificate", (), "luttinger/alternative_bundle_certificate.json"),
    "M_alternative_based_monodromy": (
        "machine_certificate", (),
        "runs/32-alternative-based-monodromy.txt"),
    "M_PL_flip_trace": (
        "machine_certificate", (), "luttinger/pl_flip_trace_certificate.json"),
    "M_independent_marked_fiber": (
        "machine_certificate", (), "luttinger/independent_fiber_certificate.json"),
    "M_PL_theorem_hypotheses": (
        "machine_certificate", (), "luttinger/pl_theorem_hypotheses.json"),
    "M_complement_theorem_hypotheses": (
        "machine_certificate", (), "luttinger/complement_theorem_hypotheses.json"),
    "M_torus_local_flatness": (
        "machine_certificate", (), "luttinger/torus_local_flatness_certificate.json"),
    "M_frontier_normal_equivalence": (
        "machine_certificate", (),
        "luttinger/frontier_normal_equivalence_certificate.json"),
    "M_topological_smooth_reroute": (
        "machine_certificate", (),
        "luttinger/topological_smooth_bridge_certificate.json"),
    "M_relative_marked_monodromy": (
        "machine_certificate", (),
        "luttinger/relative_marking_certificate.json"),
    "M_explicit_graph_clutching": (
        "machine_certificate", (),
        "luttinger/graph_clutching_certificate.json"),
    "M_interpretation_dictionary": (
        "machine_certificate", (),
        "luttinger/interpretation_dictionary_certificate.json"),
    "M_independent_paper_dictionary": (
        "machine_certificate", (),
        "runs/54-independent-paper-dictionary.txt"),
    "M_lemma71_normal_form": (
        "machine_certificate", (),
        "luttinger/lemma71_normal_form_certificate.json"),
    "M_lp_source_figure": (
        "machine_certificate", (),
        "luttinger/lp_source_figure_certificate.json"),
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
        "luttinger/independent_peripheral_certificate.json"),
    # Run 70: the ten displayed relations plus the two filling words, typed
    # from the paper, enumerate to the trivial group on all four sign sheets.
    "M_displayed_sheet_collapse": (
        "machine_certificate", (), "luttinger/displayed_sheet/output.txt"),
    # Run 77: the eight named loops generate the sealed complement group Q
    # (index 1), and the drilled-fiber relation is a free-group consequence
    # of the four B-transport relations and the surface relation.
    "M_generation_check": (
        "machine_certificate", (), "luttinger/generation_check/output.txt"),
    # The relation sheet as a written geometric argument (paper, Lemma "the
    # relation sheet"): membranes, crossings, whiskers; signs and letter
    # placement certified by the sealed transport.
    "G_relation_sheet": (
        "geometric_argument",
        ("M_based_monodromy", "M_sealed_tietze_transport", "M_R3"), None),
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
    # Run 74 split the run-64 chain in two.  The transfer of Wuebben's
    # Theorems A, B, C under D1--D14 is the ATTRIBUTION chain, moved to
    # luttinger/attribution/ unchanged; the EXISTENCE chain for Theorem A'
    # about Z_aud carries no assumption and no item about any other
    # author's construction (check_existence_boundary below enforces it).
    "M_wuebben_transfer_chain": (
        "machine_certificate", (),
        "luttinger/attribution/wuebben_transfer_chain_certificate.json"),
    "M_existence_chain": (
        "machine_certificate", (), "luttinger/downstream_chain_certificate.json"),
    "M_sigma_aud_seam_identity": (
        "machine_certificate", (), "runs/72-sigma-aud-boundary-involution.txt"),
    "M_section_PL_push_off": ("machine_certificate", (), "runs/28-pl-self-intersection-certificate.txt"),

    "G_equivariant_normal_form": (
        "geometric_argument",
        ("M_lemma71_normal_form", "M_lp_source_figure",
         "T_periodic_disk_involution"),
        "notes/lemma71_equivariant_normal_form_2026-08-27.md"),

    "G_audit_model_identification": (
        "geometric_argument",
        ("M_marked_fiber", "M_independent_marked_fiber",
         "M_based_monodromy", "M_bundle_tori",
         "M_alternative_bundle", "M_alternative_based_monodromy",
         "M_PL_flip_trace", "M_PL_theorem_hypotheses",
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
        ("G_audit_model_identification", "G_lagrangian_framing",
         "M_peripheral_slopes", "M_independent_peripheral_extraction",
         "M_alpha_coordinate_identity",
         "M_beta_coordinate_identity"),
        "notes/peripheral_identification_lemma_2026-08-24.md"),
    "G_Wuebben_comparison": (
        "geometric_argument",
        ("G_audit_model_identification", "G_peripheral_identification",
         "G_equivariant_normal_form", "M_interpretation_dictionary",
         "M_independent_paper_dictionary", "M_lp_source_figure",
         "A_Source_Formalization_D"), None),
    "G_section_square_zero": (
        "geometric_argument",
        ("G_audit_model_identification", "M_section_PL_push_off",
         "M_PL_theorem_hypotheses", "G_topological_smooth_reroute"),
        "notes/pl_self_intersection_certificate_2026-08-24.md"),
    # The intrinsic boundary involution and the double (runs 72, 73;
    # paper/sigma_aud.tex, paper/symplectic_double.tex).
    "G_sigma_aud": (
        "geometric_argument",
        ("M_sigma_aud_seam_identity", "M_based_monodromy",
         "G_audit_model_identification"),
        "runs/72-sigma-aud-boundary-involution.txt"),
    "G_audit_double": (
        "geometric_argument",
        ("G_sigma_aud", "G_section_square_zero"),
        "runs/72-sigma-aud-boundary-involution.txt"),
    "G_double_form": (
        "geometric_argument",
        ("G_sigma_aud", "G_audit_double", "G_lagrangian_framing"),
        "runs/73-symplectic-form-on-the-double.txt"),
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
    "C_pi1_Vaud_trivial_from_sheet": (
        "derived_claim",
        ("G_relation_sheet", "M_generation_check",
         "M_displayed_sheet_collapse",
         "M_alpha_coordinate_identity", "M_beta_coordinate_identity"), None),
    "C_pi1_Vaud_trivial": (
        "derived_claim",
        ("C_pi1_Vaud_trivial_from_sheet",
         "C_correct_sealed_filled_presentation",
         "M_sealed_filled_group_derivations",
         "M_second_filled_group_verifier"), None),
    "C_pi1_Vaud_trivial_unseeded_chain": (
        "derived_claim",
        ("C_correct_filled_presentation", "M_filled_group_derivations",
         "M_second_filled_group_verifier"), None),
    # The existence chain (run 74): every step below is an item of
    # luttinger/downstream_chain_certificate.json, replayed by two checkers,
    # and none of them depends on a source assumption or on any other
    # author's construction.
    "C_pi1_Zaud_trivial": (
        "derived_claim",
        ("C_pi1_Vaud_trivial", "T_van_kampen", "G_audit_double"), None),
    "C_Zaud_form_hyperbolic": (
        "derived_claim",
        ("C_pi1_Zaud_trivial", "G_section_square_zero", "G_audit_double",
         "M_existence_chain", "T_lattice_index", "T_wu_formula",
         "T_duality_uct"), None),
    "C_Zaud_homeomorphic_S2xS2": (
        "derived_claim", ("C_Zaud_form_hyperbolic", "T_freedman"), None),
    "C_Zaud_symplectic": (
        "derived_claim",
        ("G_double_form", "G_lagrangian_framing", "T_luttinger_symplectic",
         "G_audit_double"), None),
    "C_Zaud_not_diffeomorphic_S2xS2": (
        "derived_claim",
        ("C_Zaud_symplectic", "G_audit_double", "T_asphericity",
         "T_kodaira_dimension", "T_ho_li", "M_existence_chain"), None),
    "C_theorem_A_prime_exotic_S2xS2": (
        "derived_claim",
        ("C_Zaud_homeomorphic_S2xS2", "C_Zaud_symplectic",
         "C_Zaud_not_diffeomorphic_S2xS2"), None),

    # ---- attribution track: the transfer of Wuebben's theorems under
    # D1--D14 (luttinger/attribution/wuebben_transfer_chain.py, run 64).
    "C_pi1_V_trivial": (
        "derived_claim",
        ("C_pi1_Vaud_trivial", "G_Wuebben_comparison"), None),
    # Every step below is an item of
    # luttinger/attribution/wuebben_transfer_chain_certificate.json,
    # replayed by two checkers.
    "C_homology_of_V": (
        "derived_claim",
        ("C_pi1_V_trivial", "M_wuebben_transfer_chain", "T_duality_uct",
         "T_wu_formula", "T_lp_double_bundle"), None),
    "C_pi1_double_trivial": (
        "derived_claim",
        ("C_pi1_V_trivial", "T_van_kampen", "T_lp_double_bundle",
         "T_lp_regluing"), None),
    "C_Z_form_hyperbolic": (
        "derived_claim",
        ("C_pi1_double_trivial", "G_section_square_zero",
         "M_wuebben_transfer_chain", "T_lattice_index", "T_wu_formula",
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
         "T_ho_li", "M_wuebben_transfer_chain"), None),
    "C_theorem_A_exotic_S2xS2": (
        "derived_claim",
        ("C_Z_homeomorphic_S2xS2", "C_Z_not_diffeomorphic_S2xS2"), None),
    "C_W_invariants": (
        "derived_claim",
        ("C_pi1_double_trivial", "T_lp_quotient_spin",
         "T_covering_sequence", "M_wuebben_transfer_chain", "C_homology_of_V",
         "T_duality_uct"), None),
    "C_W_homeomorphic_B": (
        "derived_claim",
        ("C_W_invariants", "T_kawauchi_B", "T_hambleton_kreck",
         "M_wuebben_transfer_chain"), None),
    "C_no_square_zero_torus": (
        "derived_claim",
        ("C_Z_symplectic", "C_Z_form_hyperbolic",
         "T_symplectic_cover_construction", "T_symplectic_thom",
         "M_wuebben_transfer_chain"), None),
    "C_figure_eight_not_slice_W": (
        "derived_claim",
        ("C_W_invariants", "T_trace_embedding", "T_klug_relative_rochlin",
         "T_levine_arf", "T_covering_sequence", "T_duality_uct",
         "C_no_square_zero_torus", "M_wuebben_transfer_chain"), None),
    "C_theorem_B_slicing_pair": (
        "derived_claim",
        ("C_W_homeomorphic_B", "C_figure_eight_not_slice_W",
         "T_kawauchi_B", "T_ball_isotopy"), None),
    "C_Zpp_form_odd": (
        "derived_claim",
        ("C_pi1_double_trivial", "T_novikov", "T_lp_regluing",
         "T_lattice_index", "M_wuebben_transfer_chain", "T_duality_uct"), None),
    "C_Zpp_homeomorphic_CP2": (
        "derived_claim", ("C_Zpp_form_odd", "T_freedman"), None),
    "C_Zpp_not_diffeomorphic_CP2": (
        "derived_claim",
        ("C_Z_symplectic", "T_adjunction", "C_homology_of_V",
         "C_Zpp_form_odd", "T_lp_floer", "M_wuebben_transfer_chain"), None),
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


EXISTENCE_CONCLUSION = "C_theorem_A_prime_exotic_S2xS2"


def closure(name, acc=None):
    acc = set() if acc is None else acc
    for dependency in NODES[name][1]:
        if dependency not in acc:
            acc.add(dependency)
            closure(dependency, acc)
    return acc


def check_existence_boundary():
    """Theorem A' rests on no source assumption and on nothing named after
    another author's construction."""
    deps = closure(EXISTENCE_CONCLUSION)
    for name in sorted(deps):
        kind = NODES[name][0]
        assert kind != "source_assumption", f"{EXISTENCE_CONCLUSION} rests on {name}"
        lowered = name.lower()
        assert "_lp_" not in lowered and "wuebben" not in lowered, (
            f"{EXISTENCE_CONCLUSION} rests on {name}")
    for pillar in ("C_pi1_Vaud_trivial", "G_sigma_aud", "G_double_form",
                   "M_existence_chain"):
        assert pillar in deps, f"{EXISTENCE_CONCLUSION} misses {pillar}"
    return deps


def main():
    check_graph()
    existence = check_existence_boundary()
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
        if kind in {"external_theorem", "software_trust", "source_assumption",
                    "geometric_argument"}:
            print(f"  {kind}: {name}")
    print(f"bound evidence files: {len(evidence)}")
    kinds_e = {}
    for name in existence:
        kinds_e[NODES[name][0]] = kinds_e.get(NODES[name][0], 0) + 1
    print(f"existence boundary of {EXISTENCE_CONCLUSION}: "
          + ", ".join(f"{k}={v}" for k, v in sorted(kinds_e.items()))
          + "; source_assumption=0; no _lp_/wuebben node")


if __name__ == "__main__":
    main()
