#!/usr/bin/env python3
"""Independent standard-library verifier for the case-100 transfer proof."""

import argparse
import gzip
import json
from hashlib import sha256
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
RAW = HERE.parent / "raw_j_certificates"


class VerificationError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def inverse(word):
    return [-letter for letter in reversed(word)]


def free_reduce(word):
    output = []
    for letter in word:
        if output and output[-1] == -letter:
            output.pop()
        else:
            output.append(letter)
    return output


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
        candidates.extend(
            tuple(doubled[start:start + len(word)])
            for start in range(len(word))
        )
    return min(candidates)


def monoid(word):
    return [2 * abs(letter) - (1 if letter > 0 else 0) for letter in word]


def signed(word):
    return [
        ((letter + 1) // 2) * (1 if letter % 2 else -1)
        for letter in word
    ]


def relation_key(left, right):
    return cyclic_key(signed(left) + inverse(signed(right)))


def check_word(word, nletters, label):
    require(isinstance(word, list), f"{label} is not a list")
    require(
        all(isinstance(letter, int) and 1 <= letter <= nletters
            for letter in word),
        f"{label} contains an invalid monoid letter",
    )


def apply_trace(word, trace, records, before):
    word = list(word)
    require(isinstance(trace, list), "rewrite trace is not a list")
    for number, step in enumerate(trace):
        require(isinstance(step, list) and len(step) == 2,
                f"bad rewrite step {number}")
        rule_id, position = step
        require(isinstance(rule_id, int) and 0 <= rule_id < before,
                f"rewrite step {number} uses an unproved rule")
        require(isinstance(position, int) and position >= 0,
                f"rewrite step {number} has a bad position")
        rule = records[rule_id]
        left = rule["lhs"]
        require(word[position:position + len(left)] == left,
                f"rewrite step {number} does not match")
        word = (word[:position] + rule["rhs"] +
                word[position + len(left):])
    return word


def verify_records(proof, relators):
    ngens = proof["ngens"]
    nletters = 2 * ngens
    inverses = proof["inverse_letters"]
    expected_inverses = [
        value for i in range(ngens) for value in (2 * i + 2, 2 * i + 1)
    ]
    require(inverses == expected_inverses, "invalid inverse-letter table")
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
            require(inverses[left[0] - 1] == left[1],
                    "false inverse axiom")
        elif kind == "input_relator":
            index = derivation["relator"]
            require(isinstance(index, int) and 0 <= index < len(relators),
                    "invalid input-relator index")
            require(relation_key(left, right) == input_keys[index],
                    "equation does not match claimed input relator")
        elif kind == "overlap":
            parent_a = derivation["parent_a"]
            parent_b = derivation["parent_b"]
            require(0 <= parent_a < record_id and 0 <= parent_b < record_id,
                    "overlap parent has not yet been proved")
            first, second = records[parent_a], records[parent_b]
            lhs_a, lhs_b = first["lhs"], second["lhs"]
            offset = derivation["offset"]
            require(isinstance(offset, int) and
                    -len(lhs_b) < offset < len(lhs_a), "empty overlap")
            low = max(0, offset)
            high = min(len(lhs_a), offset + len(lhs_b))
            require(lhs_a[low:high] == lhs_b[low-offset:high-offset],
                    "parent left sides do not overlap")
            start = min(0, offset)
            end = max(len(lhs_a), offset + len(lhs_b))
            source_word = [
                lhs_a[pos] if 0 <= pos < len(lhs_a) else lhs_b[pos-offset]
                for pos in range(start, end)
            ]
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
                    "overlap does not prove recorded equation")
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
            require(relation_key(left, right) ==
                    relation_key(reduced_left, reduced_right),
                    "tidy change does not preserve the group equation")
        else:
            raise VerificationError(f"unknown derivation kind {kind!r}")
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument(
        "--source", type=Path, default=HERE / "common_core_source.json")
    parser.add_argument("--n0", type=Path, default=RAW /
                        "n0_y1_ap1_bp1_jap1_jbp1_presentation.json")
    parser.add_argument("--n1", type=Path, default=RAW /
                        "n1_y2_ap1_bp1_jap1_jbp1_presentation.json")
    args = parser.parse_args()

    source_bytes = args.source.read_bytes()
    source = json.loads(source_bytes)
    require(source["format"] == "luttinger-case100-common-core-v1",
            "unknown source format")
    n0_bytes, n1_bytes = args.n0.read_bytes(), args.n1.read_bytes()
    require(sha256(n0_bytes).hexdigest() == source["n0_source_sha256"],
            "n0 source digest mismatch")
    require(sha256(n1_bytes).hexdigest() == source["n1_source_sha256"],
            "n1 source digest mismatch")
    n0, n1 = json.loads(n0_bytes), json.loads(n1_bytes)
    core = source["common_relators"]
    require(n0["ngens"] == n1["ngens"] == source["ngens"] == 4,
            "generator-count mismatch")
    require(len(core) == 96, "common core does not contain 96 relators")
    require(n0["relators"][1:] == core and n1["relators"][1:] == core,
            "the frozen presentations do not have the claimed common core")
    require(n0["relators"][0] == source["n0_extra_relator"],
            "n0 extra relator mismatch")
    require(n1["relators"][0] == source["n1_extra_relator"],
            "n1 extra relator mismatch")

    with gzip.open(args.certificate, "rt", encoding="ascii") as stream:
        proof = json.load(stream)
    require(proof["format"] == "luttinger-case100-transfer-proof-v1",
            "unknown certificate format")
    require(proof["source_sha256"] == sha256(source_bytes).hexdigest(),
            "certificate/source digest mismatch")
    require(proof["ngens"] == 4 and proof["common_relators"] == core,
            "certificate presentation mismatch")
    records = verify_records(proof, core)

    expected = {
        "g1": ([1], []), "g1_inverse": ([-1], []),
        "g3": ([3], []), "g3_inverse": ([-3], []),
        "g4": ([4], []), "g4_inverse": ([-4], []),
        "n0_extra": (source["n0_extra_relator"], [-2]),
        "n1_extra": (source["n1_extra_relator"], [-2]),
    }
    targets = proof["targets"]
    require(len(targets) == len(expected), "wrong number of target equalities")
    seen = set()
    for target in targets:
        name = target["name"]
        require(name in expected and name not in seen,
                "unknown or duplicate target equality")
        seen.add(name)
        lhs, rhs = expected[name]
        require(target["lhs"] == lhs and target["rhs"] == rhs,
                f"false target statement for {name}")
        result = apply_trace(monoid(lhs), target["trace"],
                             records, len(records))
        require(result == monoid(rhs), f"target trace failed for {name}")
    require(seen == set(expected), "missing target equality")

    # The checked targets say C forces g1=g3=g4=1 and r0=g2^-1.
    # The frozen n0 presentation is exactly C plus the relation r0=1.
    # Therefore it also forces g2=1, so every one of its four generators is 1.
    print(
        args.certificate,
        "VERIFIED CASE 100 TRIVIAL",
        len(records),
        "proof records; common core 96/97",
    )


if __name__ == "__main__":
    try:
        main()
    except (VerificationError, KeyError, json.JSONDecodeError,
            gzip.BadGzipFile) as error:
        print(f"VERIFICATION FAILED: {error}", file=sys.stderr)
        raise SystemExit(1)
