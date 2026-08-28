#!/usr/bin/env python3
"""Compile KBMAG ancestry into a compact certificate for case 100.

This program is deliberately outside the trust boundary.  It imports the
existing history parser, searches the completed system for concrete rewrite
traces, and retains their complete dependency cone.  The Python and Ruby
verifiers replay the resulting records without importing this compiler.
"""

import argparse
import gzip
import io
import json
from hashlib import sha256
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from compile_kbmag_certificate import Compiler  # noqa: E402


def monoid(word):
    """Signed free-group letters to KBMAG's positive monoid alphabet."""
    return [2 * abs(letter) - (1 if letter > 0 else 0) for letter in word]


def dependencies(record):
    proof = record["proof"]
    if proof["kind"] == "overlap":
        yield proof["parent_a"]
        yield proof["parent_b"]
        for field in ("trace_a", "trace_b"):
            yield from (step[0] for step in proof[field])
    elif proof["kind"] == "change":
        yield proof["old"]
        for field in ("left_trace", "right_trace"):
            yield from (step[0] for step in proof[field])


def remap_record(record, renumber):
    record = json.loads(json.dumps(record))
    proof = record["proof"]
    for field in ("parent_a", "parent_b", "old"):
        if field in proof:
            proof[field] = renumber[proof[field]]
    for field in ("trace_a", "trace_b", "left_trace", "right_trace"):
        if field in proof:
            proof[field] = [
                [renumber[rule_id], position]
                for rule_id, position in proof[field]
            ]
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("history", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--source", type=Path, default=HERE / "common_core_source.json"
    )
    args = parser.parse_args()

    source_bytes = args.source.read_bytes()
    source = json.loads(source_bytes)
    if source["format"] != "luttinger-case100-common-core-v1":
        raise SystemExit("wrong common-core source format")
    core = source["common_relators"]
    compiler = Compiler(source["ngens"], core)
    compiler.process(args.history.read_text(encoding="ascii"))

    requested = [
        ("g1", [1], []),
        ("g1_inverse", [-1], []),
        ("g3", [3], []),
        ("g3_inverse", [-3], []),
        ("g4", [4], []),
        ("g4_inverse", [-4], []),
        ("n0_extra", source["n0_extra_relator"], [-2]),
        ("n1_extra", source["n1_extra_relator"], [-2]),
    ]
    targets = []
    roots = set()
    for name, lhs_signed, rhs_signed in requested:
        normal, trace = compiler.reduce(monoid(lhs_signed))
        expected = monoid(rhs_signed)
        if normal != expected:
            raise RuntimeError(
                f"{name} has normal form {normal}, expected {expected}"
            )
        roots.update(step[0] for step in trace)
        targets.append({
            "name": name,
            "lhs": lhs_signed,
            "rhs": rhs_signed,
            "trace": trace,
        })

    keep = set()
    stack = list(roots)
    while stack:
        record_id = stack.pop()
        if record_id in keep:
            continue
        keep.add(record_id)
        stack.extend(dependencies(compiler.records[record_id]))

    ordered = sorted(keep)
    renumber = {old: new for new, old in enumerate(ordered)}
    records = [remap_record(compiler.records[old], renumber) for old in ordered]
    for target in targets:
        target["trace"] = [
            [renumber[rule_id], position]
            for rule_id, position in target["trace"]
        ]

    proof = {
        "format": "luttinger-case100-transfer-proof-v1",
        "ngens": source["ngens"],
        "inverse_letters": compiler.inverse_letters,
        "source_sha256": sha256(source_bytes).hexdigest(),
        "common_relators": core,
        "records": records,
        "targets": targets,
        "compiler_fallback_searches": compiler.fallbacks,
        "history_record_count": len(compiler.records),
        "active_final_rule_count": len(compiler.slots),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
            with io.TextIOWrapper(gz, encoding="ascii") as text:
                json.dump(proof, text, separators=(",", ":"), sort_keys=True)
    print(
        args.output,
        len(records),
        "retained records from",
        len(compiler.records),
        "history records;",
        sum(len(target["trace"]) for target in targets),
        "target steps",
    )


if __name__ == "__main__":
    main()
