#!/usr/bin/env python3
"""Regression-check theorem polarity and scope in the publication sources.

This is deliberately a small, standard-library-only editorial checker.  It
does not prove the mathematical statements.  The main paper now carries the
source-independent audit-manifold theorem, while the supplement preserves the
historical conditional application.  Assertions are therefore located by
stable theorem labels where possible rather than by obsolete prose from an
earlier article structure.
"""

import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
MAIN = (REPO / "paper/main.tex").read_text(encoding="utf-8")
SUPPLEMENT = (REPO / "paper/supplement.tex").read_text(encoding="utf-8")
FACTS = json.loads((HERE / "publication_semantics.json").read_text())
CHAIN = json.loads((HERE / "downstream_chain_certificate.json").read_text())


def normalize_space(text):
    """Ignore editorial line wrapping while preserving token order."""
    return " ".join(text.split())


def require(text, fragment, label):
    assert normalize_space(fragment) in normalize_space(text), (
        f"missing {label}: {fragment!r}"
    )


def forbid(text, fragment, label):
    assert normalize_space(fragment) not in normalize_space(text), (
        f"forbidden {label}: {fragment!r}"
    )


def labeled_environment(text, environment, label):
    """Return a labeled TeX environment, independent of editorial wording."""
    pattern = re.compile(
        rf"\\begin\{{{re.escape(environment)}\}}"
        rf"(?:\[[^\]]*\])?.*?\\label\{{{re.escape(label)}\}}"
        rf".*?\\end\{{{re.escape(environment)}\}}",
        re.DOTALL,
    )
    match = pattern.search(text)
    assert match is not None, f"missing {environment} labeled {label}"
    return match.group(0)


def main():
    assert FACTS["format"] == "exotic-s2xs2-publication-semantics-v2"
    facts = FACTS["facts"]
    assert facts["slice(4_1,B)"] is True
    assert facts["slice(4_1,W)"] is False
    assert facts["comparison(V_aud,Wuebben_V)_requires"] == [
        f"D{i}" for i in range(1, 15)
    ]
    assert facts["pi_1(V_aud)"] == "trivial"

    audit = labeled_environment(MAIN, "theorem", "thm:audit-manifold")
    require(audit, r"\pione(V_{\mathrm{aud}})=1",
            "trivial fundamental group in the Audit-Manifold Theorem")
    require(audit, r"H_k(V_{\mathrm{aud}};\Z)",
            "integral homology in the Audit-Manifold Theorem")

    identification = labeled_environment(MAIN, "theorem", "prop:ident")
    require(identification,
            "No clause of the open source-comparison checklist D1--D14 "
            "enters this theorem.",
            "source-independent audit-model identification")
    require(MAIN, "member remains an open comparison problem",
            "open Wuebben comparison in the main paper")
    require(MAIN, "No exotic-manifold conclusion is asserted here.",
            "main-paper exoticity scope boundary")

    require(SUPPLEMENT, "D1 &", "first atomic source clause")
    require(SUPPLEMENT, "D14 &", "last atomic source clause")
    require(SUPPLEMENT,
            "This appendix is historical and conditional: assume every clause "
            "D1--D14",
            "conditional downstream appendix")
    slice_w = labeled_environment(SUPPLEMENT, "proposition", "prop:slice")
    require(slice_w, "The figure-eight knot is not smoothly slice in $W$.",
            "supplemental nonsliceness proposition")
    require(SUPPLEMENT,
            "in which the figure-eight knot is smoothly slice.",
            "Kawauchi-manifold sliceness input")
    require(SUPPLEMENT, "the sliceness of the figure-eight knot in $B$",
            "Theorem B sliceness polarity")

    # These guards must cover both documents: the conditional statements were
    # moved from the main article to the supplement during the scope revision.
    combined = MAIN + "\n" + SUPPLEMENT
    forbid(combined, "figure-eight knot bounds the constructed disk in $W$",
           "reversed W sliceness claim")
    forbid(combined, "If it bounded smoothly in $B$",
           "reversed B nonsliceness claim")

    nodes = {node["id"]: node for node in CHAIN["items"]}
    assert "smoothly slice in B" in nodes["E_kawauchi_B"]["statement"]
    assert nodes["S11_figure_eight_not_slice_in_W"]["claim"] == (
        "The figure-eight knot is not smoothly slice in W."
    )
    theorem_b = nodes["S12_theorem_B"]
    assert "4_1 is slice in B" in theorem_b["proof"]
    assert "not in W" in theorem_b["proof"]

    print("PASS: publication semantics agree across main paper, supplement, "
          "and downstream certificate")
    print("  slice(4_1,B)=true; slice(4_1,W)=false")
    print("  pi_1(V_aud)=1; Wuebben comparison requires D1--D14")


if __name__ == "__main__":
    main()
