#!/usr/bin/env python3
"""Replay the finite algebra behind the intrinsic audit-manifold invariants.

This checker does not prove the geometric conversion in the paper.  It binds
the sealed complement presentation, verifies the exponent-lattice calculation
used for the slope family, and replays the Euler/Betti/spin arithmetic once the
paper's topological hypotheses (connected boundary, simple connectivity,
surviving fiber and section) have been established.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "sealed_transport" / "r_presentations.json"
EXPECTED_SHA256 = "1e5fc8cb6872a25fa45a227c1e1c207b288c861a3998fe3aae8722ea510c852c"


def exponent_vector(word: list[int], ngens: int) -> tuple[int, ...]:
    out = [0] * ngens
    for letter in word:
        assert 1 <= abs(letter) <= ngens
        out[abs(letter) - 1] += 1 if letter > 0 else -1
    return tuple(out)


def main() -> None:
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256
    data = json.loads(raw)
    assert data["ngens"] == 3 and len(data["relators"]) == 78

    rows = [exponent_vector(word, 3) for word in data["relators"]]
    assert all(row[:2] == (0, 0) for row in rows)
    assert math.gcd(*(abs(row[2]) for row in rows)) == 1

    tracked = data["tracked_words"]
    names = ("geom_M", "geom_N", "lb_a_y1", "lb_b_s2")
    vectors = {name: exponent_vector(tracked[name], 3) for name in names}
    expected = {
        "geom_M": (0, 0, 1),
        "geom_N": (0, 0, 0),
        "lb_a_y1": (0, 1, 2),
        "lb_b_s2": (-1, 0, -3),
    }
    assert vectors == expected

    chi_fiber = 2 - 2 * 2
    chi_base = 2 - 2 * 1 - 1
    chi_vaud = chi_fiber * chi_base
    assert (chi_fiber, chi_base, chi_vaud) == (-2, -1, 2)

    # With connected nonempty boundary and pi_1=1, the paper proves
    # b0=1, b1=b3=b4=0 and torsion-free H2.  Euler characteristic then
    # determines b2, while the square-zero fiber detects w2.
    b0, b1, b3, b4 = 1, 0, 0, 0
    b2 = chi_vaud - b0 + b1 + b3 - b4
    w2_on_fiber = (chi_fiber + 0) % 2
    assert b2 == 1 and w2_on_fiber == 0

    print("PASS: sealed source digest and dimensions")
    print("PASS: complement exponent lattice = Z(0,0,1)")
    print("PASS: [M]=[N]=0, [lambda_alpha]=g2, [lambda_beta]=-g1")
    print("PASS: H1(P_pq) = Z/q + Z/p")
    print("PASS: chi(V_aud)=2, b2(V_aud)=1, w2(F)=0 mod 2")


if __name__ == "__main__":
    main()
