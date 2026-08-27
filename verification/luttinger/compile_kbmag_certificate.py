#!/usr/bin/env python3
"""Compile a patched-KBMAG history into a small independently checkable proof.

The compiler is untrusted.  It searches the history for explicit rewrite
paths and retains only the dependency cone of the final one-letter rules.
``verify_kbmag_certificate.py`` checks the resulting proof from scratch.
"""

import argparse
import gzip
import io
import json
import re
from hashlib import sha256
from pathlib import Path


EQUATION = re.compile(
    r"#(?P<kind>Initial|New) equation number (?P<num>\d+)"
    r"(?:, from overlap (?P<a>\d+), (?P<b>\d+))?:\n"
    r"(?P<body>.*?)(?=\n\s+#(?:Initial|New) equation number|"
    r"\n#Proof|\n\s+#\d+ eqns|\n\s+#No new|\Z)", re.S)
CONTROL = re.compile(
    r"^#Proof(TidyBegin|NewReduced|Reduced|Change|Drop|TidyEnd) (.*)$", re.M)
GAP_TOKEN = re.compile(r"_g(\d+)(?:\^(\d+))?")


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
    """Canonical key modulo cyclic conjugacy and inversion."""
    word = cyclic_reduce(word)
    if not word:
        return ()
    candidates = []
    for variant in (word, inverse(word)):
        doubled = variant + variant
        candidates.extend(tuple(doubled[i:i + len(word)])
                          for i in range(len(word)))
    return min(candidates)


def parse_gap_word(text):
    if text == "IdWord":
        return []
    out = []
    for generator, exponent in GAP_TOKEN.findall(text):
        out.extend([int(generator)] * int(exponent or 1))
    return out


def parse_equation_body(match):
    body = "".join(match.group("body").replace("#", "").split())
    left, right = body.split("->")
    return parse_gap_word(left), parse_gap_word(right)


def parse_numeric_word(text):
    if text == "[]":
        return []
    return [int(value) for value in text[1:-1].split(",")]


def slug(filling):
    return (f'{filling["half_drift"]}_'
            f'{"p" if filling["sign_a"] > 0 else "m"}1_'
            f'{"p" if filling["sign_b"] > 0 else "m"}1')


class Compiler:
    def __init__(self, ngens, relators):
        self.ngens = ngens
        self.nletters = 2 * ngens
        self.inverse_letters = [value for pair in
                                ((2*i + 2, 2*i + 1) for i in range(ngens))
                                for value in pair]
        self.relators = relators
        self.input_keys = {}
        for index, word in enumerate(relators):
            self.input_keys.setdefault(cyclic_key(word), index)
        self.records = []
        self.slots = []
        self.pending = None
        self.batch = None
        self.reduced = {}
        self.new_reduced = {}
        self.index = {}
        self.max_lhs = 0
        self.fallbacks = 0

    def signed(self, word):
        return [((letter + 1) // 2) * (1 if letter % 2 else -1)
                for letter in word]

    def relation_key(self, left, right):
        return cyclic_key(self.signed(left) + inverse(self.signed(right)))

    def add_slot(self, record_id):
        self.slots.append(record_id)
        left = self.records[record_id]["lhs"]
        self.index.setdefault(tuple(left), []).append((len(self.slots), record_id))
        self.max_lhs = max(self.max_lhs, len(left))

    def rebuild_index(self):
        self.index = {}
        self.max_lhs = 0
        for slot, record_id in enumerate(self.slots, 1):
            left = self.records[record_id]["lhs"]
            self.index.setdefault(tuple(left), []).append((slot, record_id))
            self.max_lhs = max(self.max_lhs, len(left))

    def rewrites(self, word, forbidden=None):
        """All one-step rewrites, in KBMAG's preferred order."""
        hits = []
        for end in range(1, len(word) + 1):
            # The reduction automaton selects the shortest matching suffix.
            for start in range(end - 1, max(-1, end - self.max_lhs - 1), -1):
                for slot, record_id in self.index.get(tuple(word[start:end]), ()):
                    if record_id == forbidden:
                        continue
                    record = self.records[record_id]
                    result = word[:start] + record["rhs"] + word[end:]
                    # KBMAG's automaton keeps the latest slot when identical
                    # left sides coexist between tidy passes.
                    hits.append((end, -start, -slot, result,
                                 [record_id, start]))
        hits.sort(key=lambda item: item[:3])
        return [(item[3], item[4]) for item in hits]

    def reduce(self, word, forbidden=None):
        word = list(word)
        trace = []
        for _ in range(100000):
            choices = self.rewrites(word, forbidden)
            if not choices:
                return word, trace
            word, step = choices[0]
            trace.append(step)
        raise RuntimeError("rewrite step limit exceeded")

    def normal_forms(self, word, forbidden=None, limit=200000):
        """Enumerate reachable normal forms for rare reducer tie cases."""
        start = tuple(word)
        stack = [start]
        paths = {start: []}
        normals = []
        while stack:
            current = stack.pop()
            choices = self.rewrites(list(current), forbidden)
            if not choices:
                normals.append((list(current), paths[current]))
                continue
            for result, step in choices:
                result = tuple(result)
                if result in paths:
                    continue
                paths[result] = paths[current] + [step]
                stack.append(result)
                if len(paths) > limit:
                    raise RuntimeError("normal-form search limit exceeded")
        return normals

    def greedy_path(self, source, target, forbidden=None):
        source, target = tuple(source), tuple(target)
        if source == target:
            return []
        current = source
        greedy_trace = []
        for _ in range(100000):
            choices = self.rewrites(list(current), forbidden)
            if not choices:
                break
            result, step = choices[0]
            greedy_trace.append(step)
            current = tuple(result)
            if current == target:
                return greedy_trace
        return None

    def find_path(self, source, target, forbidden=None, limit=200000):
        """Find an explicit directed rewrite path to a known target."""
        greedy = self.greedy_path(source, target, forbidden)
        if greedy is not None:
            return greedy
        source, target = tuple(source), tuple(target)
        stack = [source]
        paths = {source: []}
        while stack:
            current = stack.pop()
            for result, step in self.rewrites(list(current), forbidden):
                result = tuple(result)
                if result in paths:
                    continue
                path = paths[current] + [step]
                if result == target:
                    return path
                paths[result] = path
                stack.append(result)
                if len(paths) > limit:
                    raise RuntimeError("rewrite path search limit exceeded")
        raise RuntimeError("target is not reachable by active rewrite rules")

    def find_pair(self, left, right, target_key, forbidden_left=None):
        left_nf, left_trace = self.reduce(left, forbidden_left)
        right_nf, right_trace = self.reduce(right)
        if self.relation_key(left_nf, right_nf) == target_key:
            return left_trace, right_trace

        self.fallbacks += 1
        left_forms = self.normal_forms(left, forbidden_left)
        right_forms = self.normal_forms(right)
        right_by_key = {}
        for word, trace in right_forms:
            right_by_key.setdefault(tuple(word), trace)
        for left_word, left_path in left_forms:
            for right_word, right_path in right_forms:
                if self.relation_key(left_word, right_word) == target_key:
                    return left_path, right_path
        raise RuntimeError("could not reconstruct KBMAG reduction")

    def overlap_proof(self, parent_a, parent_b, left, right, reduced_pair=None):
        first = self.records[parent_a]
        second = self.records[parent_b]
        lhs_a, lhs_b = first["lhs"], second["lhs"]
        target_key = self.relation_key(left, right)
        for offset in range(-len(lhs_b) + 1, len(lhs_a)):
            lo, hi = max(0, offset), min(len(lhs_a), offset + len(lhs_b))
            if lhs_a[lo:hi] != lhs_b[lo-offset:hi-offset]:
                continue
            start, end = min(0, offset), max(len(lhs_a), offset + len(lhs_b))
            source = [lhs_a[pos] if 0 <= pos < len(lhs_a)
                      else lhs_b[pos-offset] for pos in range(start, end)]
            pos_a, pos_b = -start, offset - start
            branch_a = (source[:pos_a] + first["rhs"] +
                        source[pos_a + len(lhs_a):])
            branch_b = (source[:pos_b] + second["rhs"] +
                        source[pos_b + len(lhs_b):])
            try:
                if reduced_pair is None:
                    trace_a, trace_b = self.find_pair(
                        branch_a, branch_b, target_key)
                else:
                    logged_a, logged_b = reduced_pair
                    if self.relation_key(logged_a, logged_b) != target_key:
                        raise RuntimeError("orientation changed the group relation")
                    pairings = ((logged_b, logged_a), (logged_a, logged_b))
                    traces = None
                    for target_a, target_b in pairings:
                        candidate_a = self.greedy_path(branch_a, target_a)
                        candidate_b = self.greedy_path(branch_b, target_b)
                        if candidate_a is not None and candidate_b is not None:
                            traces = candidate_a, candidate_b
                            break
                    if traces is None:
                        # Rare non-deterministic reducer case: search only
                        # after both cheap pairings have been ruled out.
                        for target_a, target_b in pairings:
                            try:
                                traces = (self.find_path(branch_a, target_a),
                                          self.find_path(branch_b, target_b))
                                break
                            except RuntimeError:
                                pass
                    if traces is None:
                        raise RuntimeError("logged reductions are unreachable")
                    trace_a, trace_b = traces
            except RuntimeError:
                continue
            return {
                "kind": "overlap", "parent_a": parent_a,
                "parent_b": parent_b, "offset": offset,
                "trace_a": trace_a, "trace_b": trace_b,
            }
        raise RuntimeError("no valid parent overlap found")

    def commit_pending(self, expected):
        if self.pending is None:
            return
        number, record_id = self.pending
        if expected == len(self.slots) + 1 and number == expected:
            self.add_slot(record_id)
        elif expected != len(self.slots):
            raise RuntimeError("cannot resolve pending equation")
        self.pending = None

    def process(self, history):
        events = sorted(
            [(m.start(), "equation", m) for m in EQUATION.finditer(history)] +
            [(m.start(), "control", m) for m in CONTROL.finditer(history)])
        for _, kind, match in events:
            if kind == "equation":
                number = int(match.group("num"))
                left, right = parse_equation_body(match)
                record_id = len(self.records)
                record = {"lhs": left, "rhs": right}
                self.records.append(record)
                if match.group("kind") == "Initial":
                    if number != len(self.slots) + 1:
                        raise RuntimeError("bad initial equation numbering")
                    if right == [] and len(left) == 2 and \
                            self.inverse_letters[left[0] - 1] == left[1]:
                        record["proof"] = {"kind": "inverse_axiom"}
                    else:
                        key = self.relation_key(left, right)
                        if key not in self.input_keys:
                            raise RuntimeError("initial equation is not an input relator")
                        record["proof"] = {
                            "kind": "input_relator",
                            "relator": self.input_keys[key],
                        }
                    self.add_slot(record_id)
                    continue

                if self.pending is not None:
                    pending_number, pending_id = self.pending
                    if number == pending_number + 1:
                        self.add_slot(pending_id)
                    elif number != pending_number:
                        raise RuntimeError("bad new-equation numbering")
                parent_a = self.slots[int(match.group("a")) - 1]
                parent_b = self.slots[int(match.group("b")) - 1]
                try:
                    record["proof"] = self.overlap_proof(
                        parent_a, parent_b, left, right,
                        self.new_reduced.pop(number, None))
                except RuntimeError as error:
                    raise RuntimeError(
                        f"could not reconstruct new equation {number} from "
                        f"slots {match.group('a')}, {match.group('b')}") from error
                self.pending = (number, record_id)
                continue

            control, payload = match.group(1), match.group(2)
            if control == "NewReduced":
                fields = payload.split()
                self.new_reduced[int(fields[0])] = (
                    parse_numeric_word(fields[1]),
                    parse_numeric_word(fields[2]))
            elif control == "TidyBegin":
                expected = int(payload)
                self.commit_pending(expected)
                if expected != len(self.slots):
                    raise RuntimeError("bad tidy input size")
                self.batch = {"old": list(self.slots), "changes": {}, "drops": set()}
            elif control == "Reduced":
                fields = payload.split()
                self.reduced[int(fields[0])] = (
                    parse_numeric_word(fields[1]),
                    parse_numeric_word(fields[2]))
            elif control == "Change":
                fields = payload.split()
                slot = int(fields[0])
                old_left, old_right, new_left, new_right = map(
                    parse_numeric_word, fields[1:])
                old_id = self.slots[slot - 1]
                old = self.records[old_id]
                if old["lhs"] != old_left or old["rhs"] != old_right:
                    raise RuntimeError("tidy change does not match active equation")
                record_id = len(self.records)
                try:
                    reduced_left, reduced_right = self.reduced[slot]
                    if self.relation_key(reduced_left, reduced_right) != \
                            self.relation_key(new_left, new_right):
                        raise RuntimeError("orientation changed the group relation")
                    left_trace = self.find_path(
                        old_left, reduced_left, forbidden=old_id)
                    right_trace = self.find_path(old_right, reduced_right)
                except RuntimeError as error:
                    raise RuntimeError(
                        f"could not reconstruct tidy change in slot {slot}: "
                        f"{old_left}={old_right} -> {new_left}={new_right}") from error
                self.records.append({
                    "lhs": new_left, "rhs": new_right,
                    "proof": {"kind": "change", "old": old_id,
                              "reduced_left": reduced_left,
                              "reduced_right": reduced_right,
                              "left_trace": left_trace,
                              "right_trace": right_trace},
                })
                self.batch["changes"][slot] = record_id
            elif control == "Drop":
                self.batch["drops"].add(int(payload))
            else:
                expected = int(payload)
                self.slots = [
                    self.batch["changes"].get(slot, record_id)
                    for slot, record_id in enumerate(self.batch["old"], 1)
                    if slot not in self.batch["drops"]]
                if len(self.slots) != expected:
                    raise RuntimeError("bad tidy output size")
                self.batch = None
                self.reduced = {}
                self.rebuild_index()

        if self.pending is not None:
            self.commit_pending(len(self.slots) + 1)

    def certificate(self, case, input_digest):
        roots = []
        for letter in range(1, self.nletters + 1):
            matches = [record_id for record_id in self.slots
                       if self.records[record_id]["lhs"] == [letter]
                       and self.records[record_id]["rhs"] == []]
            if not matches:
                raise RuntimeError(f"no final identity rule for letter {letter}")
            roots.append(matches[0])

        keep, stack = set(), list(roots)
        while stack:
            record_id = stack.pop()
            if record_id in keep:
                continue
            keep.add(record_id)
            proof = self.records[record_id]["proof"]
            if proof["kind"] == "overlap":
                stack.extend([proof["parent_a"], proof["parent_b"]])
                stack.extend(step[0] for step in proof["trace_a"])
                stack.extend(step[0] for step in proof["trace_b"])
            elif proof["kind"] == "change":
                stack.append(proof["old"])
                stack.extend(step[0] for step in proof["left_trace"])
                stack.extend(step[0] for step in proof["right_trace"])

        ordered = sorted(keep)
        renumber = {old: new for new, old in enumerate(ordered)}
        records = []
        for old_id in ordered:
            record = json.loads(json.dumps(self.records[old_id]))
            proof = record["proof"]
            for field in ("parent_a", "parent_b", "old"):
                if field in proof:
                    proof[field] = renumber[proof[field]]
            for field in ("trace_a", "trace_b", "left_trace", "right_trace"):
                if field in proof:
                    proof[field] = [[renumber[step[0]], step[1]]
                                    for step in proof[field]]
            records.append(record)
        return {
            "format": "luttinger-kbmag-proof-v1",
            "case": case,
            "ngens": self.ngens,
            "inverse_letters": self.inverse_letters,
            "input_sha256": input_digest,
            "relators": self.relators,
            "records": records,
            "roots": [renumber[root] for root in roots],
            "compiler_fallback_searches": self.fallbacks,
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("history", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--input", type=Path, default=Path("r_presentations.json"))
    parser.add_argument("--case", type=int, required=True)
    args = parser.parse_args()

    input_bytes = args.input.read_bytes()
    data = json.loads(input_bytes)
    filling = data["paper_fillings"][args.case]
    relators = data["relators"] + filling["relators"]
    compiler = Compiler(data["ngens"], relators)
    compiler.process(args.history.read_text(errors="strict"))
    certificate = compiler.certificate(
        {"index": args.case, "slug": slug(filling),
         "half_drift": filling["half_drift"],
         "sign_a": filling["sign_a"], "sign_b": filling["sign_b"]},
        sha256(input_bytes).hexdigest())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("wb") as raw_stream:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw_stream,
                           mtime=0) as compressed:
            with io.TextIOWrapper(compressed, encoding="ascii") as stream:
                json.dump(certificate, stream, separators=(",", ":"),
                          sort_keys=True)
    print(args.output, len(certificate["records"]), "proof records",
          compiler.fallbacks, "fallback searches")


if __name__ == "__main__":
    main()
