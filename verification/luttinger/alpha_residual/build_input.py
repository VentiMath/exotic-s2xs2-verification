#!/usr/bin/env python3
"""Freeze the sealed-complement alpha-longitude residual and KBMAG input.

The target is the literal word

    lb_a_y1^-1 * geom_A * geom_x

in the 3-generator, 78-relator sealed complement presentation.  No filling
relator is included.  This script writes a hash-bound source file and the GAP
program that exports the uncompleted KBMAG rewriting system.
"""

import json
from hashlib import sha256
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRESENTATION = HERE.parent / "sealed_transport" / "r_presentations.json"


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


def gap_word(word):
    if not word:
        return "One(F)"
    return "*".join(
        f"F.{abs(letter)}" + ("^-1" if letter < 0 else "")
        for letter in word
    )


def main():
    input_bytes = PRESENTATION.read_bytes()
    presentation = json.loads(input_bytes)
    tracked = presentation["tracked_words"]
    residual = free_reduce(
        inverse(tracked["lb_a_y1"]) +
        tracked["geom_A"] + tracked["geom_x"]
    )
    assert presentation["ngens"] == 3
    assert len(presentation["relators"]) == 78
    assert len(residual) == 72

    source = {
        "format": "luttinger-alpha-residual-source-v1",
        "presentation_file": str(PRESENTATION.relative_to(HERE.parent)),
        "presentation_sha256": sha256(input_bytes).hexdigest(),
        "ngens": presentation["ngens"],
        "relators": presentation["relators"],
        "word_factors": {
            "lb_a_y1": tracked["lb_a_y1"],
            "geom_A": tracked["geom_A"],
            "geom_x": tracked["geom_x"],
        },
        "target": residual,
        "claim": "lb_a_y1^-1 * geom_A * geom_x = 1 in the sealed complement",
    }
    source_path = HERE / "source.json"
    source_path.write_text(
        json.dumps(source, separators=(",", ":"), sort_keys=True) + "\n",
        encoding="ascii",
    )

    relators = ",".join(gap_word(word) for word in source["relators"])
    gap = f'''LoadPackage("kbmag");;
F := FreeGroup({source["ngens"]});;
rels := [{relators}];;
G := F/rels;;
rws := KBMAGRewritingSystem(G);;
opts := OptionsRecordOfKBMAGRewritingSystem(rws);;
opts.tidyint := 500;;
opts.maxeqns := 300000;;
opts.maxstates := 2000000;;
WriteRWS(rws,"verification/luttinger/alpha_residual/complement_input.rws");;
QUIT;;
'''
    gap_path = HERE / "build_input.g"
    gap_path.write_text(gap, encoding="ascii")
    print(source_path)
    print(gap_path)
    print("target length", len(residual))


if __name__ == "__main__":
    main()
