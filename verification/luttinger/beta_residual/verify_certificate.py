#!/usr/bin/env python3
"""Independent standard-library verifier for the beta residual proof."""

import argparse
import gzip
import json
from hashlib import sha256
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent


class VerificationError(Exception):
    pass


def require(condition, message):
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
    expected = [
        value for index in range(ngens)
        for value in (2 * index + 2, 2 * index + 1)
    ]
    require(inverses == expected, "invalid inverse-letter table")
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
            parent_a, parent_b = derivation["parent_a"], derivation["parent_b"]
            require(0 <= parent_a < record_id and 0 <= parent_b < record_id,
                    "overlap parent has not yet been proved")
            first, second = records[parent_a], records[parent_b]
            lhs_a, lhs_b = first["lhs"], second["lhs"]
            offset = derivation["offset"]
            require(isinstance(offset, int) and
                    -len(lhs_b) < offset < len(lhs_a), "empty overlap")
            low, high = max(0, offset), min(len(lhs_a), offset + len(lhs_b))
            require(lhs_a[low:high] == lhs_b[low-offset:high-offset],
                    "parent left sides do not overlap")
            start, end = min(0, offset), max(len(lhs_a), offset + len(lhs_b))
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


def verify(source_bytes, certificate):
    source = json.loads(source_bytes)
    require(source["format"] == "luttinger-beta-residual-source-v1",
            "unknown source format")
    factors = source["word_factors"]
    expected_target = free_reduce(
        inverse(factors["lb_b_s2"]) + inverse(factors["geom_r"]) +
        factors["geom_M"] + factors["geom_r"] + factors["geom_B"]
    )
    require(len(expected_target) == 113 and source["target"] == expected_target,
            "source does not encode the stated 113-letter residual")
    require(source["ngens"] == 3 and len(source["relators"]) == 78,
            "source is not the sealed complement presentation")

    proof = certificate
    require(proof["format"] == "luttinger-beta-residual-proof-v1",
            "unknown certificate format")
    require(proof["source_sha256"] == sha256(source_bytes).hexdigest(),
            "certificate/source digest mismatch")
    require(proof["ngens"] == source["ngens"], "generator-count mismatch")
    require(proof["relators"] == source["relators"],
            "certificate presentation mismatch")
    require(proof["target"] == source["target"], "certificate target mismatch")
    records = verify_records(proof, source["relators"])
    result = apply_trace(
        monoid(source["target"]), proof["target_trace"], records, len(records))
    require(result == [], "target trace does not end at the identity")
    return len(records), len(proof["target_trace"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--source", type=Path, default=HERE / "source.json")
    parser.add_argument("--negative-controls", action="store_true")
    args = parser.parse_args()

    source_bytes = args.source.read_bytes()
    with gzip.open(args.certificate, "rt", encoding="ascii") as stream:
        certificate = json.load(stream)
    record_count, step_count = verify(source_bytes, certificate)
    print(args.certificate, "VERIFIED BETA RESIDUAL IDENTITY",
          record_count, "proof records;", step_count, "target steps")

    if args.negative_controls:
        controls = []

        corrupt = json.loads(json.dumps(certificate))
        corrupt["target"][0] *= -1
        controls.append(("ALTERED TARGET", corrupt))

        corrupt = json.loads(json.dumps(certificate))
        old = corrupt["records"][100]["rhs"][0]
        corrupt["records"][100]["rhs"][0] = 1 if old != 1 else 2
        controls.append(("FORGED DERIVATION RECORD", corrupt))

        corrupt = json.loads(json.dumps(certificate))
        corrupt["relators"][0][0] *= -1
        controls.append(("ALTERED PRESENTATION RELATOR", corrupt))

        corrupt = json.loads(json.dumps(certificate))
        corrupt["target_trace"].pop(len(corrupt["target_trace"]) // 2)
        controls.append(("SPLICED TARGET TRACE", corrupt))

        for label, corrupt in controls:
            try:
                verify(source_bytes, corrupt)
            except VerificationError as error:
                print(f"REJECTED {label}: {error}")
            else:
                raise VerificationError(f"{label.lower()} was accepted")


if __name__ == "__main__":
    try:
        main()
    except (VerificationError, KeyError, json.JSONDecodeError,
            gzip.BadGzipFile) as error:
        print(f"VERIFICATION FAILED: {error}", file=sys.stderr)
        raise SystemExit(1)
