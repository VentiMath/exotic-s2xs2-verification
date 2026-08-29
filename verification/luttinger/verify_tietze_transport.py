#!/usr/bin/env python3
"""Standalone verifier for the sealed raw-complex-to-reduced-presentation
Tietze transport.

Three frozen objects are checked against one another, importing nothing from
the geometry, the simplifier, or any other project module:

  r_tietze_input.json.gz        the raw simplicial complement presentation
                                (99,863 generators, 321,702 relators) with
                                the tracked peripheral and coordinate words
                                and their names
  r_tietze_certificate.json.gz  the recorded elementary Tietze eliminations
  r_presentations.json          the committed reduced presentation, its
                                tracked words, and the renumbering

A step [i, g, rep] is accepted only if generator g occurs exactly once in
the current relator i and rep is the replacement that relator itself
implies; the step is then applied to every relator and tracked word.  The
input is bound to the certificate by SHA-256, the replayed output is bound
by the certificate's output digest, and the renumbered output must equal
the committed presentation exactly.

    python3 verify_tietze_transport.py [--root DIR] [--negative-controls]
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path


class VerificationError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def digest(payload):
    encoded = json.dumps(payload, separators=(",", ":"),
                         sort_keys=True).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def load(path):
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rt", encoding="ascii") as stream:
        return json.load(stream)


def inverse(word):
    return [-x for x in reversed(word)]


def free_reduce(word):
    out = []
    for x in word:
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return out


def cyclic_reduce(word):
    word = free_reduce(word)
    while len(word) >= 2 and word[0] == -word[-1]:
        word = word[1:-1]
    return word


def replay(source, certificate):
    ngens, relators, words = source["ngens"], source["relators"], source["words"]
    require(certificate.get("format") == "luttinger-fast-tietze-v1",
            "unknown certificate format")
    require(certificate.get("ngens") == ngens, "generator count mismatch")
    require(certificate.get("input_sha256") == digest([ngens, relators, words]),
            "certificate does not belong to this input")
    require(certificate.get("steps_count") == len(certificate["steps"]),
            "step count mismatch")
    for index, relator in enumerate(relators):
        for letter in relator:
            require(isinstance(letter, int) and 1 <= abs(letter) <= ngens,
                    f"relator {index} uses an invalid letter")

    rels = {}
    for index, relator in enumerate(relators):
        reduced = cyclic_reduce(relator)
        if reduced:
            rels[index] = reduced
    tracked = [free_reduce(word) for word in words]
    occ = {}

    def index_rel(i):
        for g in {abs(x) for x in rels[i]}:
            occ.setdefault(g, set()).add(i)

    def unindex_rel(i):
        for g in {abs(x) for x in rels[i]}:
            occ[g].discard(i)

    for i in rels:
        index_rel(i)

    for number, step in enumerate(certificate["steps"], 1):
        require(isinstance(step, list) and len(step) == 3,
                f"step {number}: malformed")
        i, g, recorded = step
        require(i in rels, f"step {number}: source relator {i} is absent")
        relator = rels[i]
        positions = [k for k, x in enumerate(relator) if abs(x) == g]
        require(len(positions) == 1,
                f"step {number}: generator {g} does not occur exactly once")
        pos = positions[0]
        expected = inverse(relator[:pos]) + inverse(relator[pos + 1:])
        if relator[pos] < 0:
            expected = inverse(expected)
        require(recorded == expected,
                f"step {number}: replacement is not implied by the relator")

        def substitute(word):
            out = []
            for h in word:
                if h == g:
                    out += recorded
                elif h == -g:
                    out += inverse(recorded)
                else:
                    out.append(h)
            return free_reduce(out)

        targets = list(occ.get(g, ()))
        unindex_rel(i)
        del rels[i]
        for j in targets:
            if j == i or j not in rels:
                continue
            unindex_rel(j)
            replaced = cyclic_reduce(substitute(rels[j]))
            if replaced:
                rels[j] = replaced
                index_rel(j)
            else:
                del rels[j]
        tracked = [substitute(word) for word in tracked]
        occ.pop(g, None)

    seen, out = set(), []
    for relator in rels.values():
        key, inverse_key = tuple(relator), tuple(inverse(relator))
        if key in seen or inverse_key in seen:
            continue
        seen.add(key)
        out.append(relator)
    live = sorted({abs(g) for r in out for g in r} |
                  {abs(g) for w in tracked for g in w})
    require(certificate.get("output_sha256") == digest([live, out, tracked]),
            "replayed output does not match the certificate's output digest")
    return live, out, tracked


def check_against_committed(live, out, tracked, names, presentation):
    renumbering = {g: k + 1 for k, g in enumerate(sorted(live))}
    require({str(old): new for old, new in renumbering.items()}
            == presentation["renumbering"], "renumbering mismatch")

    def renumber(word):
        return [renumbering[abs(g)] * (1 if g > 0 else -1) for g in word]

    require(presentation["ngens"] == len(live),
            "committed generator count mismatch")
    require([renumber(r) for r in out] == presentation["relators"],
            "committed complement relators differ from the replayed output")
    committed_words = presentation["tracked_words"]
    require(len(names) == len(tracked), "tracked word name count mismatch")
    require(len(set(names)) == len(names), "duplicate tracked word name")
    require(sorted(names) == sorted(committed_words),
            "committed tracked word names differ from the sealed input")
    for name, word in zip(names, tracked):
        require(renumber(word) == committed_words[name],
                f"committed tracked word {name} differs from the replayed output")
    return len(out), len(committed_words)


def verify(root):
    source = load(root / "r_tietze_input.json.gz")
    require(source.get("format") == "luttinger-tietze-input-v1",
            "unknown input format")
    require(isinstance(source.get("word_names"), list),
            "sealed input lacks tracked word names")
    certificate = load(root / "r_tietze_certificate.json.gz")
    presentation = load(root / "r_presentations.json")
    require(presentation.get("tietze_certificate")
            == "r_tietze_certificate.json.gz",
            "committed presentation names a different certificate")
    live, out, tracked = replay(source, certificate)
    relators, words = check_against_committed(live, out, tracked,
                                              source["word_names"], presentation)
    return source, certificate, presentation, live, relators, words


def negative_controls(root, source, certificate, presentation):
    def expect_rejection(label, fn):
        try:
            fn()
        except VerificationError as error:
            print(f"REJECTED {label.upper()}: {error}")
        else:
            raise VerificationError(f"{label} was accepted")

    bad_input = json.loads(json.dumps(source))
    bad_input["relators"][0][0] = -bad_input["relators"][0][0]
    expect_rejection("corrupted input relator",
                     lambda: replay(bad_input, certificate))

    omitted = json.loads(json.dumps(certificate))
    del omitted["steps"][0]
    omitted["steps_count"] -= 1
    expect_rejection("omitted elimination step",
                     lambda: replay(source, omitted))

    altered = json.loads(json.dumps(certificate))
    altered["steps"][0][2] = altered["steps"][0][2] + [source["ngens"]]
    expect_rejection("altered substitution",
                     lambda: replay(source, altered))

    live, out, tracked = replay(source, certificate)
    names = source["word_names"]
    bad_output = json.loads(json.dumps(presentation))
    bad_output["relators"][0] = bad_output["relators"][0][::-1]
    expect_rejection("altered committed output",
                     lambda: check_against_committed(live, out, tracked,
                                                     names, bad_output))

    bad_word = json.loads(json.dumps(presentation))
    longest = max(bad_word["tracked_words"],
                  key=lambda name: len(bad_word["tracked_words"][name]))
    bad_word["tracked_words"][longest] = bad_word["tracked_words"][longest][::-1]
    expect_rejection("altered committed tracked word",
                     lambda: check_against_committed(live, out, tracked,
                                                     names, bad_word))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path,
                        default=Path(__file__).resolve().parent / "sealed_transport")
    parser.add_argument("--negative-controls", action="store_true")
    args = parser.parse_args()
    source, certificate, presentation, live, relators, words = verify(args.root)
    print(f"TIETZE TRANSPORT VERIFIED: {source['ngens']} generators, "
          f"{len(source['relators'])} relators -> {len(live)} generators, "
          f"{relators} relators, {words} tracked words after "
          f"{certificate['steps_count']} certified eliminations; committed "
          f"r_presentations.json matches")
    if args.negative_controls:
        negative_controls(args.root, source, certificate, presentation)


if __name__ == "__main__":
    try:
        main()
    except VerificationError as error:
        raise SystemExit(f"VERIFICATION FAILED: {error}")
