#!/usr/bin/env python3
"""Freeze the sealed-complement beta-longitude residual.

The target is the literal word

    lb_b_s2^-1 * geom_r^-1 * geom_M * geom_r * geom_B

in the 3-generator, 78-relator sealed complement presentation.  The KBMAG
rewriting input is the identical complement-only input already frozen under
``../alpha_residual/complement_input.rws``.
"""

import json
from hashlib import sha256
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRESENTATION = HERE.parent / "sealed_transport" / "r_presentations.json"
RWS = HERE.parent / "alpha_residual" / "complement_input.rws"


def inverse(word):
    return [-letter for letter in reversed(word)]


def free_reduce(word):
    out = []
    for letter in word:
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def main():
    input_bytes = PRESENTATION.read_bytes()
    presentation = json.loads(input_bytes)
    tracked = presentation["tracked_words"]
    residual = free_reduce(
        inverse(tracked["lb_b_s2"]) +
        inverse(tracked["geom_r"]) + tracked["geom_M"] +
        tracked["geom_r"] + tracked["geom_B"]
    )
    assert presentation["ngens"] == 3
    assert len(presentation["relators"]) == 78
    assert len(residual) == 113

    source = {
        "format": "luttinger-beta-residual-source-v1",
        "presentation_file": str(PRESENTATION.relative_to(HERE.parent)),
        "presentation_sha256": sha256(input_bytes).hexdigest(),
        "rewriting_input": str(RWS.relative_to(HERE.parent)),
        "rewriting_input_sha256": sha256(RWS.read_bytes()).hexdigest(),
        "ngens": presentation["ngens"],
        "relators": presentation["relators"],
        "word_factors": {
            "lb_b_s2": tracked["lb_b_s2"],
            "geom_r": tracked["geom_r"],
            "geom_M": tracked["geom_M"],
            "geom_B": tracked["geom_B"],
        },
        "target": residual,
        "claim": (
            "lb_b_s2^-1 * geom_r^-1 * geom_M * geom_r * geom_B = 1 "
            "in the sealed complement"
        ),
    }
    source_path = HERE / "source.json"
    source_path.write_text(
        json.dumps(source, separators=(",", ":"), sort_keys=True) + "\n",
        encoding="ascii",
    )
    print(source_path)
    print("target length", len(residual))


if __name__ == "__main__":
    main()
