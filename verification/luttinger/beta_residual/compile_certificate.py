#!/usr/bin/env python3
"""Compile a KBMAG history into a proof of the beta residual identity.

This compiler is outside the trust boundary.  It parses the proof-producing
KBMAG history, finds a concrete reduction of the frozen 72-letter word to the
identity, and retains only the rules on which that reduction depends.
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
    parser.add_argument("--source", type=Path, default=HERE / "source.json")
    args = parser.parse_args()

    source_bytes = args.source.read_bytes()
    source = json.loads(source_bytes)
    if source["format"] != "luttinger-beta-residual-source-v1":
        raise SystemExit("wrong beta-residual source format")

    compiler = Compiler(source["ngens"], source["relators"])
    compiler.process(args.history.read_text(encoding="ascii"))
    target_monoid = monoid(source["target"])
    normal, trace = compiler.reduce(target_monoid)
    if normal:
        raise RuntimeError(
            f"beta residual has nonempty normal form {normal}"
        )

    roots = {step[0] for step in trace}
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
    trace = [[renumber[rule_id], position] for rule_id, position in trace]

    certificate = {
        "format": "luttinger-beta-residual-proof-v1",
        "source_sha256": sha256(source_bytes).hexdigest(),
        "ngens": source["ngens"],
        "inverse_letters": compiler.inverse_letters,
        "relators": source["relators"],
        "target": source["target"],
        "target_trace": trace,
        "records": records,
        "compiler_fallback_searches": compiler.fallbacks,
        "history_record_count": len(compiler.records),
        "active_final_rule_count": len(compiler.slots),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
            with io.TextIOWrapper(gz, encoding="ascii") as stream:
                json.dump(certificate, stream, separators=(",", ":"),
                          sort_keys=True)
    print(
        args.output,
        len(records),
        "retained records from",
        len(compiler.records),
        "history records;",
        len(trace),
        "target steps",
    )


if __name__ == "__main__":
    main()
