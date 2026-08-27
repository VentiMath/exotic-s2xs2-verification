"""Proof-producing attack on framing-shift robustness case 2.

Case: n0_y1_ap1_bp1_jap2_jbp0.  These relators are the fresh GAP export
obtained from the fill-then-base raw ordering followed by
IsomorphismSimplifiedFpGroup: 2 generators, 9 relators, total length 876.
This is an auxiliary j_alpha=+2 stress test, not a paper j=0 filling.
"""

import argparse
import json

from case1_compact_attack import (attack, best_common_block,
                                  expand_named_block, replay_attack,
                                  replay_nielsen)
from presentation_search import nielsen_search


RELATORS = [
    [2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,-1,-2,1,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,-2,-1,2,1,2],
    [1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,1,-2,-1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,2,1,2,-1,-2],
    [-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,2,1,2,1,2,-1,-2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1],
    [2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,-2,-1,2,1,2,1,2,-1],
    [-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1],
    [-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1],
    [-2,-1,-2,1,2,2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1],
    [2,1,2,-1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,-2,1,-2,-1,-2,1,2,-1,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,1,-2,-1],
    [-1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,2,2,1,-2,-1,-2,-1,-2,1,1,-2,-1,-2,1,2,2,-1,2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,-1,2,1,2,1,2,-1,-2,-2,1,-2,-2,-1,2,1,2,-1,-2,-2],
]

EXPECTED_LENGTHS = [62, 62, 100, 100, 101, 101, 104, 120, 126]
assert [len(r) for r in RELATORS] == EXPECTED_LENGTHS
assert sum(EXPECTED_LENGTHS) == 876


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=100_000)
    parser.add_argument("--seeds", type=int, default=12)
    parser.add_argument("--expand", action="store_true")
    parser.add_argument("--expanded-steps", type=int, default=100_000)
    parser.add_argument("--input-results")
    parser.add_argument("--output", default="case2_compact_attack_results.json")
    args = parser.parse_args()
    input_relators = RELATORS
    if args.input_results:
        with open(args.input_results, encoding="ascii") as stream:
            previous = json.load(stream)["results"]
        candidates = [row for row in previous if row["ngens"] == 2]
        input_relators = min(candidates,
                              key=lambda row: row["total_length"])["relators"]
    rows = []
    for seed in range(1, args.seeds + 1):
        basis, moves = nielsen_search(2, input_relators, args.steps, seed)
        expansion = None
        expanded_moves = []
        ngens = 2
        if args.expand:
            block = best_common_block(basis)
            basis, expansion = expand_named_block(basis, block)
            ngens = 3
            basis, expanded_moves = nielsen_search(
                3, basis, args.expanded_steps, 10_000 + seed)
        n, reduced, images, proof = attack(ngens, basis, rounds=20)
        # Replay the complete generated route before retaining it.
        check = replay_nielsen(input_relators, moves)
        if expansion is not None:
            check, regenerated = expand_named_block(check, expansion["block"])
            assert regenerated == expansion
            check = replay_nielsen(check, expanded_moves)
        rn, rr, ri = replay_attack(ngens, check, proof)
        assert (rn, rr, ri) == (n, reduced, images)
        row = {"seed": seed, "nielsen_moves": moves,
               "expansion": expansion,
               "expanded_nielsen_moves": expanded_moves,
               "ngens": n, "nrelators": len(reduced),
               "total_length": sum(map(len, reduced)),
               "relators": reduced, "generator_images": images,
               "proof_moves": proof, "certified_trivial": n == 0}
        rows.append(row)
        print(seed, sum(map(len, basis)), n, len(reduced),
              row["total_length"], n == 0, flush=True)
        if n == 0:
            break
    with open(args.output, "w", encoding="ascii") as stream:
        json.dump({"format": "case2-compact-attack-v1",
                   "input_lengths": list(map(len, input_relators)),
                   "results": rows},
                  stream, separators=(",", ":"), sort_keys=True)
        stream.write("\n")


if __name__ == "__main__":
    main()
