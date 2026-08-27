#!/usr/bin/env python3
"""Small independent checker for ``luttinger-kbmag-proof-v1`` files."""

import argparse
import gzip
import json
from hashlib import sha256
from pathlib import Path


class VerificationError(Exception):
    pass


def require(condition, message="certificate check failed"):
    if not condition:
        raise VerificationError(message)


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


def cyclic_reduce(word):
    word = free_reduce(word)
    while len(word) > 1 and word[0] == -word[-1]:
        word = word[1:-1]
    return word


def cyclic_key(word):
    word = cyclic_reduce(word)
    if not word:
        return ()
    candidates = []
    for variant in (word, inverse(word)):
        doubled = variant + variant
        candidates.extend(tuple(doubled[i:i + len(word)])
                          for i in range(len(word)))
    return min(candidates)


def case_slug(filling):
    return (f'{filling["half_drift"]}_'
            f'{"p" if filling["sign_a"] > 0 else "m"}1_'
            f'{"p" if filling["sign_b"] > 0 else "m"}1')


def check_word(word, nletters, label):
    require(isinstance(word, list), f"{label} is not a list")
    require(all(isinstance(x, int) and 1 <= x <= nletters for x in word),
            f"{label} contains an invalid monoid letter")


def apply_trace(word, trace, records, before):
    word = list(word)
    for step_number, step in enumerate(trace):
        require(isinstance(step, list) and len(step) == 2,
                "bad rewrite step")
        rule_id, position = step
        require(isinstance(rule_id, int) and 0 <= rule_id < before,
                "rewrite uses a rule that has not yet been proved")
        rule = records[rule_id]
        left = rule["lhs"]
        require(isinstance(position, int) and 0 <= position,
                "bad rewrite position")
        require(word[position:position + len(left)] == left,
                f"rewrite step {step_number} does not match")
        word = (word[:position] + rule["rhs"] +
                word[position + len(left):])
    return word


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("certificates", nargs="+", type=Path)
    parser.add_argument("--input", type=Path, default=Path("r_presentations.json"))
    args = parser.parse_args()

    input_bytes = args.input.read_bytes()
    source = json.loads(input_bytes)
    source_digest = sha256(input_bytes).hexdigest()

    for certificate_path in args.certificates:
        with gzip.open(certificate_path, "rt", encoding="ascii") as stream:
            proof = json.load(stream)
        require(proof["format"] == "luttinger-kbmag-proof-v1",
                "unknown certificate format")
        require(proof["input_sha256"] == source_digest,
                "input digest mismatch")
        case = proof["case"]["index"]
        filling = source["paper_fillings"][case]
        require(proof["case"]["slug"] == case_slug(filling),
                "case label mismatch")
        relators = source["relators"] + filling["relators"]
        require(proof["relators"] == relators,
                "presentation relators mismatch")
        require(proof["ngens"] == source["ngens"],
                "presentation generator count mismatch")

        ngens = proof["ngens"]
        nletters = 2 * ngens
        inverse_letters = proof["inverse_letters"]
        require(inverse_letters == [value for pair in
                                    ((2*i + 2, 2*i + 1)
                                     for i in range(ngens))
                                    for value in pair],
                "invalid inverse-letter table")

        def signed(word):
            return [((letter + 1) // 2) * (1 if letter % 2 else -1)
                    for letter in word]

        def relation_key(left, right):
            return cyclic_key(signed(left) + inverse(signed(right)))

        input_keys = [cyclic_key(word) for word in relators]
        records = proof["records"]
        for record_id, record in enumerate(records):
            left, right = record["lhs"], record["rhs"]
            check_word(left, nletters, f"record {record_id} lhs")
            check_word(right, nletters, f"record {record_id} rhs")
            derivation = record["proof"]
            kind = derivation["kind"]

            if kind == "inverse_axiom":
                require(right == [] and len(left) == 2,
                        "malformed inverse axiom")
                require(inverse_letters[left[0] - 1] == left[1],
                        "false inverse axiom")
            elif kind == "input_relator":
                index = derivation["relator"]
                require(isinstance(index, int) and 0 <= index < len(relators),
                        "invalid input-relator index")
                require(relation_key(left, right) == input_keys[index],
                        "equation does not match the claimed input relator")
            elif kind == "overlap":
                parent_a, parent_b = derivation["parent_a"], derivation["parent_b"]
                require(0 <= parent_a < record_id and
                        0 <= parent_b < record_id,
                        "overlap parent has not yet been proved")
                first, second = records[parent_a], records[parent_b]
                lhs_a, lhs_b = first["lhs"], second["lhs"]
                offset = derivation["offset"]
                require(isinstance(offset, int), "nonintegral overlap offset")
                require(-len(lhs_b) < offset < len(lhs_a), "empty overlap")
                lo, hi = max(0, offset), min(len(lhs_a), offset + len(lhs_b))
                require(lhs_a[lo:hi] == lhs_b[lo-offset:hi-offset],
                        "parent left sides do not overlap")
                start, end = min(0, offset), max(len(lhs_a), offset + len(lhs_b))
                source_word = [
                    lhs_a[pos] if 0 <= pos < len(lhs_a)
                    else lhs_b[pos-offset] for pos in range(start, end)]
                pos_a, pos_b = -start, offset - start
                branch_a = (source_word[:pos_a] + first["rhs"] +
                            source_word[pos_a + len(lhs_a):])
                branch_b = (source_word[:pos_b] + second["rhs"] +
                            source_word[pos_b + len(lhs_b):])
                reduced_a = apply_trace(
                    branch_a, derivation["trace_a"], records, record_id)
                reduced_b = apply_trace(
                    branch_b, derivation["trace_b"], records, record_id)
                require(relation_key(left, right) ==
                        relation_key(reduced_a, reduced_b),
                        "overlap does not prove the recorded equation")
            elif kind == "change":
                old_id = derivation["old"]
                require(0 <= old_id < record_id,
                        "changed equation has not yet been proved")
                old = records[old_id]
                reduced_left = apply_trace(
                    old["lhs"], derivation["left_trace"], records, record_id)
                reduced_right = apply_trace(
                    old["rhs"], derivation["right_trace"], records, record_id)
                require(reduced_left == derivation["reduced_left"],
                        "left tidy reduction mismatch")
                require(reduced_right == derivation["reduced_right"],
                        "right tidy reduction mismatch")
                require(relation_key(left, right) == relation_key(
                    reduced_left, reduced_right),
                    "tidy change does not preserve the group equation")
            else:
                raise VerificationError(f"unknown derivation kind {kind!r}")

        roots = proof["roots"]
        require(len(roots) == nletters, "wrong number of identity roots")
        for letter, record_id in enumerate(roots, 1):
            require(isinstance(record_id, int) and
                    0 <= record_id < len(records), "invalid identity root")
            require(records[record_id]["lhs"] == [letter],
                    "identity root has the wrong generator")
            require(records[record_id]["rhs"] == [],
                    "identity root does not end at the identity")
        print(certificate_path, "VERIFIED TRIVIAL",
              len(records), "proof records")


if __name__ == "__main__":
    main()
