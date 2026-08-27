"""Proof-producing attacks on framing-robustness case 1.

The presentation below is GAP's simplified presentation obtained from
``j_gap/n0_y1_ap1_bp1_jap1_jbp0.fill_then_base.g`` after reversing the raw
relator list immediately before forming the quotient.  A fresh GAP replay on
2026-08-26 returned 2 generators, 7 relators, and total length 542.

This program performs seeded Nielsen basis searches followed by the
proof-producing relator/elimination search in ``presentation_search.py``.
It does not call GAP and does not claim a verdict unless all generators are
eliminated by the replayable elementary moves.
"""

import argparse
from collections import Counter
import json
import math
import random

from fast_tietze import cyclic_reduce, renumber, verify_certificate
from pi1 import inverse
from presentation_search import attack, nielsen_image, nielsen_search, rotations


RELATORS = [
    [2, 1, 2, -1, -2, 1, 2, 1, -2, -1, -2, -1, -2, 1, 2, 2, 1, -2,
     -1, -2, -1, -2, 1, -2, -1, 2, 1, 2, 2, 1, 2, -1, -2, -2, -1, 2,
     1, 2, 1, 2, -1, -2, -2, -1],
    [1, 2, -1, -2, -1, 2, 1, 2, 1, 2, -1, -2, -2, -1, 2, 1, 2, 1, 2,
     -1, 2, 1, -2, -1, -2, -2, -1, -2, 1, 2, 2, 1, -2, -1, -2, -1,
     -2, 1, 2, 2, 1, -2, -1, -2],
    [-2, -1, 2, 1, 2, 1, 2, -1, -2, 1, -2, -1, -2, -1, -2, 1, 2, 2,
     1, -2, -1, -2, -1, -2, 1, -2, -1, 2, 1, 2, 1, 2, -1, 2, 1, 2,
     1, 2, -1, -2, -2, -1, 2, 1, 2, 1, 2, -1, 2, 1, -2, -1, -2, -1,
     -2, 1, 2, 2, 1, -2, -1, -2, -1, -2],
    [-1, -2, 1, 2, 2, 1, -2, -1, -2, -1, -2, 1, 2, 2, 1, 2, 1, 2, -1,
     -2, -2, -1, 2, 1, 2, 1, 2, -1, -2, -2, -1, 2, 1, 1, -2, -1, -2,
     -1, -2, 1, 2, 2, 1, -2, -1, -2, -1, -2, -2, -1, 2, 1, 2, 1, 2,
     -1, -2, -2, -1, 2, 1, 2, 1, 2, -1],
    [-1, 2, 1, 2, 1, 2, -1, -2, -2, -1, 2, 1, 2, 1, 2, -1, -2, -2, -1,
     -2, -1, -2, 1, 2, 2, 1, -2, -1, -2, -1, -2, 1, 2, 1, 2, -1, -2,
     -2, -1, 2, 1, 2, 1, 2, -1, -2, -2, -1, 2, 1, 2, 1, 2, 2, 1, -2,
     -1, -2, -1, -2, 1, 2, 2, 1, -2, -1, -2],
    [1, 2, -1, -1, 2, 1, 2, 1, 2, -1, -2, -2, -1, 2, 1, 2, 1, 2, -1,
     -2, -1, 2, 1, 2, 1, 2, -1, -2, -2, -1, 2, 1, 2, 1, 2, -1, -2, 1,
     -2, -1, 2, -1, -2, 1, 2, 1, -2, -1, -2, -1, -2, 1, 2, 2, 1, -2,
     -1, -2, -1, -2, 1, 2, 1, -2, -1, -2, -1, -2, 1, 2, 2, 1, -2, -1,
     -2, -2],
    [-2, -1, 2, 1, 2, 1, 2, -1, -2, -2, -1, 2, 1, 2, 1, -2, -1, -2,
     -1, -2, 1, 2, 2, 1, -2, -1, -2, -1, -2, 1, 2, 2, 1, -2, -1, -2,
     1, 2, 2, 1, -2, -1, -2, -1, -2, 1, 2, -1, 2, 1, 2, 1, 2, -1, -2,
     -2, -1, 2, 1, 2, 1, 2, -1, 2, 1, -2, -1, -2, -1, -2, -2, -1, 2,
     1, 2, 1, 2, -1, -2, -2, -1, 2, 1, 2, 1, 2, -1, -2, -2, -1, 2, 1,
     -2, -1, -2, -1, -2, 1, 2, 2, 1, -2, -1, -2, -1, -2, 1, 2, 2, 1,
     2, 1, 2, -1, -2, 1, -2, -1, -2, -1, -2, 1, 2, 2, 1, -2, -1, -2,
     -1, -2, 1, -2, -1, 2, 1, 2, 1, 2, -1, -2, -2, -1, -2, -1, -2, 1,
     2, 2, 1, -2, -1, -2, -1, -2, 1, 2, 2, 1, -2, -1, -2, 1, 2, 2, -1,
     -2, -1, 2, 1, 2, 1, 2, -1, -2, -2, -1, 2, 1, 2, 1, 2, -1],
]

EXPECTED_LENGTHS = [44, 44, 64, 65, 67, 76, 182]
assert [len(r) for r in RELATORS] == EXPECTED_LENGTHS
assert sum(EXPECTED_LENGTHS) == 542

# Highest-scoring common cyclic subword in the 379-letter Nielsen basis: it
# occurs (up to inversion) in six of the seven relators.  Naming it reduces
# the expanded presentation from 379 to 331 letters, including its definition.
EXPANSION_BLOCK = [-1, -2, -2, -1, 2, -1, -2, -2, -1, -1, -1]


def best_common_block(relators, minimum=4, maximum=30):
    """Return the cyclic subword with the largest naming-length saving."""
    counts = Counter()
    for length in range(minimum, maximum + 1):
        for relator in relators:
            doubled = relator + relator[:length - 1]
            seen = set()
            for start in range(len(relator)):
                word = tuple(doubled[start:start + length])
                key = min(word, tuple(inverse(word)))
                seen.add(key)
            counts.update(seen)
    return list(max(counts, key=lambda word:
                    ((len(word) - 1) * counts[word] - (len(word) + 1),
                     len(word), counts[word])))


def expand_named_block(relators, block=EXPANSION_BLOCK):
    """Add generator 3=block and replace one cyclic occurrence per relator."""
    out = []
    replacements = []
    inverse_block = inverse(block)
    for index, relator in enumerate(relators):
        found = None
        doubled = relator + relator
        for sign, needle in ((1, block), (-1, inverse_block)):
            for start in range(len(relator)):
                if doubled[start:start + len(needle)] == needle:
                    found = (sign, start, needle)
                    break
            if found is not None:
                break
        if found is None:
            out.append(list(relator))
            continue
        sign, start, needle = found
        rotated = doubled[start:start + len(relator)]
        replaced = [3 * sign] + rotated[len(needle):]
        out.append(cyclic_reduce(replaced))
        replacements.append({"relator": index, "sign": sign,
                             "rotation": start})
    # z * block^-1 = 1, hence z=block.
    out.append([3] + inverse(block))
    return out, {"kind": "named_block_expansion", "generator": 3,
                 "block": block, "replacements": replacements,
                 "input_length": sum(map(len, relators)),
                 "output_length": sum(map(len, out))}


def relator_anneal(relators, steps, seed):
    """Anneal through elementary relator multiplications.

    Each accepted move replaces r_i by r_i times a cyclic conjugate of
    r_j^+/-1.  This preserves the normal closure of the relator set, and the
    complete accepted path is returned for replay.
    """
    rng = random.Random(seed)
    current = [cyclic_reduce(r) for r in relators]
    score = sum(map(len, current))
    best = [list(r) for r in current]
    best_score = score
    accepted = []
    best_moves = []
    for step in range(steps):
        target = rng.randrange(len(current))
        reducer = rng.randrange(len(current) - 1)
        if reducer >= target:
            reducer += 1
        orientation = rng.choice((1, -1))
        source = (current[reducer] if orientation == 1
                  else inverse(current[reducer]))
        shift = rng.randrange(len(source))
        rotated = source[shift:] + source[:shift]
        replacement = cyclic_reduce(current[target] + rotated)
        candidate_score = score - len(current[target]) + len(replacement)
        # Frequent reheating lets the search cross short local barriers while
        # a hard cap prevents explosive presentations.
        phase = (step % 10_000) / 10_000
        temperature = max(0.25, 16.0 * (1.0 - phase))
        accept = candidate_score <= score or (
            candidate_score < 3 * best_score and
            rng.random() < math.exp((score - candidate_score) / temperature))
        if accept:
            move = {
                "target": target,
                "reducer": reducer,
                "orientation": orientation,
                "shift": shift,
                "before": current[target],
                "after": replacement,
            }
            current[target] = replacement
            score = candidate_score
            accepted.append(move)
            if score < best_score:
                best = [list(r) for r in current]
                best_score = score
                best_moves = list(accepted)
        if step and step % 10_000 == 0:
            current = [list(r) for r in best]
            score = best_score
            accepted = list(best_moves)
    return best, best_moves


def verify_relator_moves(relators, moves):
    current = [cyclic_reduce(r) for r in relators]
    for number, move in enumerate(moves, 1):
        target = move["target"]
        reducer = move["reducer"]
        assert current[target] == move["before"], number
        source = (current[reducer] if move["orientation"] == 1
                  else inverse(current[reducer]))
        shift = move["shift"]
        rotated = source[shift:] + source[:shift]
        expected = cyclic_reduce(current[target] + rotated)
        assert expected == move["after"], number
        current[target] = expected
    return current


def replay_nielsen(relators, moves):
    current = [cyclic_reduce(r) for r in relators]
    for move in moves:
        current = nielsen_image(current, *move)
    return current


def replay_attack(ngens, relators, moves):
    """Independently replay the two move types emitted by attack()."""
    current = [cyclic_reduce(r) for r in relators if cyclic_reduce(r)]
    images = [[i] for i in range(1, ngens + 1)]
    for number, move in enumerate(moves, 1):
        if move["kind"] == "multiply_relator":
            target = move["target"]
            reducer = move["reducer"]
            assert current[target] == move["before"], number
            source = (current[reducer] if move["orientation"] == 1
                      else inverse(current[reducer]))
            shift = move["shift"]
            rotated = source[shift:] + source[:shift]
            expected = cyclic_reduce(current[target] + rotated)
            assert expected == move["after"], number
            current[target] = expected
        elif move["kind"] == "elimination_block":
            live, current, images = verify_certificate(
                ngens, current, images, move["certificate"])
            ngens, current, images = renumber(live, current, images)
        else:
            raise AssertionError(f"unknown attack move at {number}")
    return ngens, current, images


def verify_row(input_relators, row):
    basis = replay_nielsen(input_relators, row["nielsen_moves"])
    ngens = 2
    if row["expansion"] is not None:
        basis, expansion = expand_named_block(
            basis, row["expansion"]["block"])
        for key, value in row["expansion"].items():
            assert expansion[key] == value
        ngens = 3
        basis = replay_nielsen(basis, row["expanded_nielsen_moves"])
    basis = verify_relator_moves(basis, row["relator_moves"])
    n, relators, images = replay_attack(ngens, basis, row["proof_moves"])
    assert n == row["ngens"]
    assert relators == row["relators"]
    assert images == row["generator_images"]
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=50_000)
    parser.add_argument("--seeds", type=int, default=12)
    parser.add_argument("--relator-steps", type=int, default=0)
    parser.add_argument("--expanded-nielsen-steps", type=int, default=0)
    parser.add_argument("--output")
    parser.add_argument("--input-results")
    args = parser.parse_args()

    input_relators = RELATORS
    if args.input_results:
        with open(args.input_results, encoding="ascii") as stream:
            previous = json.load(stream)["results"]
        decided = [row for row in previous if row["ngens"] == 2]
        input_relators = min(decided, key=lambda row: row["total_length"])[
            "relators"]

    results = []
    for seed in range(1, args.seeds + 1):
        # The named block is defined in the canonical seed-1 379-letter
        # basis.  Vary only the subsequent three-generator search so every
        # expanded run starts from the same checked presentation.
        first_seed = 1 if args.expanded_nielsen_steps else seed
        basis, nielsen_moves = nielsen_search(
            2, input_relators, args.steps, first_seed)
        ngens = 2
        expansion = None
        expanded_nielsen_moves = []
        if args.expanded_nielsen_steps:
            block = (EXPANSION_BLOCK if input_relators is RELATORS
                     else best_common_block(basis))
            basis, expansion = expand_named_block(basis, block)
            if input_relators is RELATORS:
                assert len(expansion["replacements"]) == 6
                assert expansion["output_length"] == 331
            ngens = 3
            basis, expanded_nielsen_moves = nielsen_search(
                ngens, basis, args.expanded_nielsen_steps, 10_000 + seed)
        relator_moves = []
        if args.relator_steps:
            annealed, relator_moves = relator_anneal(
                basis, args.relator_steps, seed)
            assert verify_relator_moves(basis, relator_moves) == annealed
            basis = annealed
        n, reduced, images, proof_moves = attack(ngens, basis, rounds=20)
        row = {
            "seed": seed,
            "nielsen_length": sum(map(len, basis)),
            "nielsen_moves": nielsen_moves,
            "expansion": expansion,
            "expanded_nielsen_moves": expanded_nielsen_moves,
            "relator_moves": relator_moves,
            "ngens": n,
            "nrelators": len(reduced),
            "total_length": sum(map(len, reduced)),
            "relators": reduced,
            "generator_images": images,
            "proof_moves": proof_moves,
            "certified_trivial": n == 0,
        }
        results.append(row)
        print(seed, row["nielsen_length"], n, len(reduced),
              row["total_length"], n == 0, flush=True)
        if n == 0:
            break

    if args.output:
        with open(args.output, "w", encoding="ascii") as stream:
            json.dump({"format": "case1-compact-attack-v1",
                       "input_lengths": EXPECTED_LENGTHS,
                       "actual_input_lengths": list(map(len, input_relators)),
                       "results": results}, stream,
                      separators=(",", ":"), sort_keys=True)
            stream.write("\n")


if __name__ == "__main__":
    main()
