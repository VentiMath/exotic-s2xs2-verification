"""Proof-oriented local search on the exported surgery presentations.

This is deliberately narrower than a black-box random Tietze search.  It uses
only two replayable moves:

* replace a relator r by r times a cyclic conjugate of another relator s^±1;
* eliminate a generator that occurs exactly once in a relator.

Both moves preserve the presented group.  The search greedily shortens the
relator set, invokes the certified elementary eliminator after every shortening
round, and records enough data for deterministic replay.  A zero-generator
result would therefore be a genuine triviality certificate.
"""
import argparse
import json
import math
import random

from fast_tietze import cyclic_reduce, renumber, simplify
from pi1 import inverse


def rotations(word):
    return [word[i:] + word[:i] for i in range(len(word))]


def best_multiplier(relators, target):
    """Find the strongest shortening r_target <- r_target * conjugate(r_j)."""
    current = relators[target]
    best = None
    for j, reducer in enumerate(relators):
        if j == target:
            continue
        for orientation, source in ((1, reducer), (-1, inverse(reducer))):
            for shift, rotated in enumerate(rotations(source)):
                candidate = cyclic_reduce(current + rotated)
                if len(candidate) >= len(current):
                    continue
                score = len(current) - len(candidate)
                key = (score, -len(candidate), -j, -orientation, -shift)
                if best is None or key > best[0]:
                    best = (key, candidate, j, orientation, shift)
    return best


def shorten(relators, max_moves=10_000, verbose=False):
    relators = [cyclic_reduce(r) for r in relators if cyclic_reduce(r)]
    moves = []
    while len(moves) < max_moves:
        candidates = []
        for target in range(len(relators)):
            move = best_multiplier(relators, target)
            if move is not None:
                candidates.append((move[0], target, move))
        if not candidates:
            break
        _, target, (_, replacement, reducer, orientation, shift) = max(candidates)
        moves.append({
            "kind": "multiply_relator",
            "target": target,
            "reducer": reducer,
            "orientation": orientation,
            "shift": shift,
            "before": relators[target],
            "after": replacement,
        })
        relators[target] = replacement
        if verbose and len(moves) % 25 == 0:
            print(f"    {len(moves)} relator moves; total length "
                  f"{sum(map(len, relators))}")
    return relators, moves


def attack(ngens, relators, rounds=20, verbose=False):
    all_moves = []
    words = [[i] for i in range(1, ngens + 1)]
    for round_number in range(1, rounds + 1):
        before = (ngens, sum(map(len, relators)))
        relators, moves = shorten(relators, verbose=verbose)
        all_moves.extend(moves)
        live, relators, words, certificate = simplify(
            ngens, relators, words, max_len=10_000, certify=True)
        all_moves.append({"kind": "elimination_block", "certificate": certificate})
        ngens, relators, words = renumber(live, relators, words)
        after = (ngens, sum(map(len, relators)))
        if verbose:
            print(f"    round {round_number}: {before} -> {after}")
        if ngens == 0 or (not moves and after == before):
            break
    return ngens, relators, words, all_moves


def expand_extrep(extrep):
    assert len(extrep) % 2 == 0
    word = []
    for generator, exponent in zip(extrep[::2], extrep[1::2]):
        word += [generator if exponent > 0 else -generator] * abs(exponent)
    return word


def nielsen_image(relators, kind, i, j=None, side=1):
    """Apply one elementary free-group automorphism to every relator."""
    def image(letter):
        sign = 1 if letter > 0 else -1
        generator = abs(letter)
        if kind == "invert" and generator == i:
            return [-letter]
        if kind == "swap":
            if generator == i:
                return [sign * j]
            if generator == j:
                return [sign * i]
        if kind == "multiply" and generator == i:
            base = [i, side * j]
            return base if sign > 0 else inverse(base)
        return [letter]

    return [cyclic_reduce([out for letter in relator
                           for out in image(letter)])
            for relator in relators]


def nielsen_search(ngens, relators, steps, seed, verbose=False):
    """Deterministic-seed simulated annealing over Nielsen automorphisms."""
    rng = random.Random(seed)
    current = [cyclic_reduce(r) for r in relators]
    current_score = sum(map(len, current))
    best, best_score, best_moves = current, current_score, []
    moves = []
    for step in range(steps):
        i = rng.randint(1, ngens)
        j = rng.choice([g for g in range(1, ngens + 1) if g != i])
        choice = rng.randrange(6)
        if choice == 0:
            move = ("invert", i, None, 1)
        elif choice == 1:
            move = ("swap", min(i, j), max(i, j), 1)
        else:
            move = ("multiply", i, j, 1 if choice % 2 else -1)
        candidate = nielsen_image(current, *move)
        score = sum(map(len, candidate))
        # Reheat every 2,000 steps; reject explosive presentations.
        temperature = max(0.5, 8.0 * (1.0 - (step % 2000) / 2000))
        accept = score <= current_score or (
            score < 4 * best_score and
            rng.random() < math.exp((current_score - score) / temperature))
        if accept:
            current, current_score = candidate, score
            moves.append(move)
            if score < best_score:
                best, best_score, best_moves = current, score, list(moves)
                if verbose:
                    print(f"    Nielsen best at step {step}: {best_score}")
        if step and step % 2000 == 0:
            current, current_score, moves = best, best_score, list(best_moves)
    return best, best_moves


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="r_presentations.json")
    parser.add_argument("--gap-input")
    parser.add_argument("--case", type=int)
    parser.add_argument("--output", default="r_presentation_search.json")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--nielsen-steps", type=int, default=0)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    with open(args.input, encoding="ascii") as stream:
        data = json.load(stream)
    gap_cases = None
    if args.gap_input:
        with open(args.gap_input, encoding="ascii") as stream:
            gap_data = json.load(stream)
        assert gap_data["format"] == "gap-simplified-v1"
        gap_cases = {item["case"]: item for item in gap_data["cases"]}
    cases = range(len(data["fillings"])) if args.case is None else [args.case]
    results = []
    for case in cases:
        filling = data["fillings"][case]
        if gap_cases is None:
            ngens = data["ngens"]
            relators = data["relators"] + filling["relators"]
        else:
            ngens = gap_cases[case]["ngens"]
            relators = [expand_extrep(word) for word in
                         gap_cases[case]["extrep_relators"]]
        nielsen_moves = []
        if args.nielsen_steps:
            relators, nielsen_moves = nielsen_search(
                ngens, relators, args.nielsen_steps, args.seed + case,
                args.verbose)
        print(f"case {case}: drift={filling['drift']} "
              f"signs=({filling['sign_a']},{filling['sign_b']})")
        n, reduced, generators, moves = attack(
            ngens, relators, verbose=args.verbose)
        result = {
            "case": case,
            "ngens": n,
            "nrelators": len(reduced),
            "total_length": sum(map(len, reduced)),
            "relators": reduced,
            "generator_images": generators,
            "moves": moves,
            "nielsen_moves": nielsen_moves,
            "certified_trivial": n == 0,
        }
        results.append(result)
        print(f"  result: {n} gens/{len(reduced)} rels, total length "
              f"{result['total_length']}; certified_trivial={n == 0}")
    with open(args.output, "w", encoding="ascii") as stream:
        json.dump({"format": "luttinger-presentation-search-v1",
                   "results": results}, stream, separators=(",", ":"),
                  sort_keys=True)
        stream.write("\n")


if __name__ == "__main__":
    main()
