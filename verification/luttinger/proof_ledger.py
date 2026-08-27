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
    "T_surface_bundle": ("external_theorem", (), None),
    "T_rotation_system_thickening": ("external_theorem", (), None),
    "T_elementary_bistellar_trace": ("external_theorem", (), None),
    "T_low_dimensional_PL_smoothing": ("external_theorem", (), None),
    "T_oriented_intersection_naturality": ("external_theorem", (), None),
    "T_derived_regular_neighborhood": ("external_theorem", (), None),
    "T_simplicial_pi1_presentation": ("external_theorem", (), None),
    "T_tietze": ("external_theorem", (), None),
    "T_freedman_HK": ("external_theorem", (), None),
    "T_symplectic_kodaira": ("external_theorem", (), None),
    "T_symplectic_thom": ("external_theorem", (), None),
    "T_rokhlin_arf": ("external_theorem", (), None),
    "T_HF_mixed": ("external_theorem", (), None),

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
    "M_surface_bundle_hypotheses": (
        "machine_certificate", (), "runs/37-surface-bundle-boundary.txt"),
    "M_complement_theorem_hypotheses": (
        "machine_certificate", (), "runs/38-complement-presentation-boundary.txt"),
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

    "G_marked_bundle_identification": (
        "geometric_argument",
        ("M_marked_fiber", "M_independent_marked_fiber",
         "M_based_monodromy", "M_bundle_tori",
         "M_alternative_bundle", "M_alternative_based_monodromy",
         "M_PL_flip_trace", "M_PL_theorem_hypotheses",
         "M_surface_bundle_hypotheses",
         "T_surface_bundle", "T_rotation_system_thickening",
         "T_elementary_bistellar_trace",
         "T_low_dimensional_PL_smoothing"),
        "notes/surface_bundle_referee_packet_2026-08-26.md"),
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
         "M_peripheral_slopes", "M_independent_peripheral_extraction"),
        "notes/peripheral_identification_lemma_2026-08-24.md"),
    "G_section_square_zero": (
        "geometric_argument",
        ("G_marked_bundle_identification", "M_section_PL_push_off",
         "M_PL_theorem_hypotheses",
         "T_oriented_intersection_naturality"),
        "notes/pl_self_intersection_certificate_2026-08-24.md"),

    "C_correct_filled_presentation": (
        "derived_claim",
        ("G_peripheral_identification", "M_complement_tietze", "M_R3",
         "M_complement_theorem_hypotheses",
         "T_derived_regular_neighborhood",
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
