#!/usr/bin/env python3
"""Freeze the exact 96-relator common core used by the case-100 transfer.

The two inputs are independently stored full presentations.  Their last 96
relators agree byte-for-byte; only their first relator differs.  This script
records that fact in a canonical JSON source and writes the GAP program which
exports the *uncompleted* KBMAG rewriting system used for proof history.
"""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
RAW = HERE.parent / "raw_j_certificates"
N0_NAME = "n0_y1_ap1_bp1_jap1_jbp1_presentation.json"
N1_NAME = "n1_y2_ap1_bp1_jap1_jbp1_presentation.json"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def gap_word(word):
    if not word:
        return "One(F)"
    return "*".join(
        f"F.{abs(letter)}" + ("^-1" if letter < 0 else "")
        for letter in word
    )


def main():
    n0_path = RAW / N0_NAME
    n1_path = RAW / N1_NAME
    n0 = json.loads(n0_path.read_text(encoding="ascii"))
    n1 = json.loads(n1_path.read_text(encoding="ascii"))
    assert n0["ngens"] == n1["ngens"] == 4
    assert len(n0["relators"]) == len(n1["relators"]) == 97
    assert n0["relators"][1:] == n1["relators"][1:]
    assert n0["relators"][0] != n1["relators"][0]

    payload = {
        "format": "luttinger-case100-common-core-v1",
        "ngens": 4,
        "common_relators": n0["relators"][1:],
        "n0_extra_relator": n0["relators"][0],
        "n1_extra_relator": n1["relators"][0],
        "n0_source": N0_NAME,
        "n0_source_sha256": digest(n0_path),
        "n1_source": N1_NAME,
        "n1_source_sha256": digest(n1_path),
        "completion": {
            "ordering": "shortlex",
            "tidyint": 500,
            "maxeqns": 300000,
            "maxstates": 2000000,
        },
        "claim": (
            "The two 97-relator presentations have the displayed 96-relator "
            "common core.  The certificate proves g1=g3=g4=1 and proves both "
            "extra relators equal g2^-1 modulo that core.  Since the n0 extra "
            "relator is imposed in case 100, g2=1 and the case-100 group is "
            "trivial."
        ),
    }
    source_path = HERE / "common_core_source.json"
    source_path.write_text(
        json.dumps(payload, separators=(",", ":"), sort_keys=True) + "\n",
        encoding="ascii",
    )

    relators = ",".join(gap_word(word) for word in payload["common_relators"])
    gap = f'''LoadPackage("kbmag");;
F := FreeGroup(4);;
rels := [{relators}];;
G := F/rels;;
rws := KBMAGRewritingSystem(G);;
opts := OptionsRecordOfKBMAGRewritingSystem(rws);;
opts.tidyint := 500;;
opts.maxeqns := 300000;;
opts.maxstates := 2000000;;
WriteRWS(rws,"luttinger/case100_transfer/common_core_input.rws");;
attempt := CALL_WITH_CATCH(KnuthBendix,[rws]);;
if attempt[1] = true and IsConfluent(rws) then
  WriteRWS(rws,"luttinger/case100_transfer/common_core_confluent.rws");
fi;;
Print("ATTEMPT=",attempt," CONFLUENT=",IsConfluent(rws),"\\n");;
QUIT;;
'''
    (HERE / "build_transfer_input.g").write_text(gap, encoding="ascii")
    print(source_path)
    print(HERE / "build_transfer_input.g")


if __name__ == "__main__":
    main()
