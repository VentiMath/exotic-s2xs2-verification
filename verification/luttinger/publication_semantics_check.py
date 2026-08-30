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


def require(text, fragment, label):
    assert fragment in text, f"missing {label}: {fragment!r}"


def forbid(text, fragment, label):
    assert fragment not in text, f"forbidden {label}: {fragment!r}"


def main():
    assert FACTS["format"] == "exotic-s2xs2-publication-semantics-v1"
    facts = FACTS["facts"]
    assert facts["slice(4_1,B)"] is True
    assert facts["slice(4_1,W)"] is False
    assert facts["comparison(V_*,Wuebben_V)_requires"] == [
        "S1", "S2", "S3", "S4"
    ]
    assert facts["pi_1(V_*)"] == "trivial"

    require(MAIN, "smoothly slice in $B$ and not smoothly slice in\n  $W$",
            "Theorem B polarity in the main theorem")
    require(MAIN, "The\nfigure-eight knot is smoothly slice in $B$ by "
                  "construction.",
            "Theorem B polarity in the dependency audit")
    require(MAIN, "It is not\nsmoothly slice in $W$",
            "non-sliceness in W")
    forbid(MAIN, "figure-eight knot bounds the constructed disk in $W$",
           "reversed W sliceness claim")
    forbid(MAIN, "If it bounded\nsmoothly in $B$",
           "reversed B nonsliceness claim")

    require(SUPPLEMENT,
            "The figure-eight knot is not smoothly slice in $W$.",
            "supplemental nonsliceness proposition")
    require(SUPPLEMENT, "the sliceness of\nthe figure-eight knot in $B$",
            "supplemental sliceness input")
    require(MAIN, "Assume S1--S4", "conditional Wuebben comparison")
    require(MAIN, "The audit-defined manifold $V_*$ is simply connected.",
            "unconditional audit-model conclusion")

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
    print("  pi_1(V_*)=1; Wuebben comparison requires S1--S4")


if __name__ == "__main__":
    main()
