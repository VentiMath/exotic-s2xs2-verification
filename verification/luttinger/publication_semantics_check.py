#!/usr/bin/env python3
"""Regression-check theorem polarity and scope in the publication sources.

This is deliberately a small, standard-library-only editorial checker. It
does not prove the mathematical statements; it prevents the main paper from
reversing or dropping facts already fixed by the downstream certificate and
the supplement.
"""

import json
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


def main():
    assert FACTS["format"] == "exotic-s2xs2-publication-semantics-v2"
    facts = FACTS["facts"]
    assert facts["slice(4_1,B)"] is True
    assert facts["slice(4_1,W)"] is False
    assert facts["comparison(V_aud,Wuebben_V)_requires"] == [
        f"D{i}" for i in range(1, 15)
    ]
    assert facts["pi_1(V_aud)"] == "trivial"

    require(MAIN, "smoothly slice in $B$ and not smoothly slice in $W$",
            "Theorem B polarity in the main theorem")
    require(MAIN, "The figure-eight knot is smoothly slice in $B$ by "
                  "construction.",
            "Theorem B polarity in the dependency audit")
    require(MAIN, "It is not smoothly slice in $W$",
            "non-sliceness in W")
    forbid(MAIN, "figure-eight knot bounds the constructed disk in $W$",
           "reversed W sliceness claim")
    forbid(MAIN, "If it bounded smoothly in $B$",
           "reversed B nonsliceness claim")

    require(SUPPLEMENT,
            "The figure-eight knot is not smoothly slice in $W$.",
            "supplemental nonsliceness proposition")
    require(SUPPLEMENT, "the sliceness of the figure-eight knot in $B$",
            "supplemental sliceness input")
    require(MAIN, "Under Hypotheses D1--D14", "conditional Wuebben comparison")
    require(MAIN, "The manifold $V_{\\mathrm{aud}}$ is simply connected.",
            "unconditional audit-model conclusion")
    require(MAIN, "D1 &", "first atomic source clause")
    require(MAIN, "D14 &", "last atomic source clause")
    require(MAIN, "No clause of Source Comparison Hypotheses~D1--D14 enters this",
            "source-independent audit-model theorem")

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
