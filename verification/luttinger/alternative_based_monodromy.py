#!/usr/bin/env python3
"""Exact based-pi1 certificate for the alternative beta trace.

The construction imports neither the primary bundle/layer code nor the
primary based-monodromy bridge.  It forms the four literal p-whiskered
residual loops in the alternative open beta stack, eliminates the raw
triangulation presentation by elementary Tietze moves, and records every
substitution.  The remaining genus-2 surface words are then reduced by
logged Dehn steps whose relator witnesses are checked independently.
"""

from __future__ import annotations

import argparse
import ast
import gzip
import io
import json
from collections import deque
from pathlib import Path

from alternative_bundle import build_alternative_bundle
from fast_tietze import renumber, simplify, verify_certificate
from independent_peripheral_extractor import rail_loop
from pi1 import free_reduce, inverse


ROOT = Path(__file__).resolve().parent
NAMES = "xyrs"
TARGETS = {
    "x": (("y", -1),),
    "y": (("y", 1), ("x", 1)),
    "r": (("r", 1),),
    "s": (("s", 1),),
}


class DeterministicPresentation:
    """Rank-sorted spanning-tree presentation of a finite 2-complex."""

    def __init__(self, complex_, base):
        self.K = complex_
        self.base = base
        rank = complex_.rank.get

        def simplex_key(simplex):
            return tuple(rank(vertex) for vertex in complex_.sorted_tuple(simplex))

        vertices = sorted(complex_.vertices(), key=rank)
        edges = sorted(complex_.simplices[1], key=simplex_key)
        triangles = sorted(complex_.simplices[2], key=simplex_key)
        adjacency = {vertex: [] for vertex in vertices}
        for edge in edges:
            u, v = complex_.sorted_tuple(edge)
            adjacency[u].append(v)
            adjacency[v].append(u)
        for neighbours in adjacency.values():
            neighbours.sort(key=rank)
        parent = {base: None}
        queue = deque([base])
        while queue:
            vertex = queue.popleft()
            for neighbour in adjacency[vertex]:
                if neighbour not in parent:
                    parent[neighbour] = vertex
                    queue.append(neighbour)
        if len(parent) != len(vertices):
            raise AssertionError("alternative beta trace is disconnected")
        self.tree = {frozenset((vertex, previous))
                     for vertex, previous in parent.items()
                     if previous is not None}
        generator_edges = [edge for edge in edges if edge not in self.tree]
        self.gens = {edge: index + 1
                     for index, edge in enumerate(generator_edges)}
        self.ngens = len(self.gens)
        self.relators = []
        for triangle in triangles:
            a, b, c = complex_.sorted_tuple(triangle)
            word = free_reduce(self.edge_word(a, b) + self.edge_word(b, c) +
                               self.edge_word(c, a))
            if word:
                self.relators.append(word)

    def edge_word(self, u, v):
        if u == v:
            return []
        edge = frozenset((u, v))
        if edge in self.tree:
            return []
        generator = self.gens[edge]
        lower, upper = self.K.sorted_tuple(edge)
        return [generator] if (u, v) == (lower, upper) else [-generator]

    def path_word(self, path):
        word = []
        for u, v in zip(path, path[1:]):
            word.extend(self.edge_word(u, v))
        return free_reduce(word)

    def loop_word(self, path):
        if path[0] != path[-1]:
            raise AssertionError("marked residual is not a loop")
        return self.path_word(path)


def _import_audit():
    source = Path(__file__).read_text(encoding="ascii")
    tree = ast.parse(source)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module)
    forbidden = {"bundle", "layers", "paper_bridge"}
    present = forbidden & set(imports)
    if present:
        raise AssertionError(f"alternative monodromy imported {sorted(present)}")
    return {"imports": sorted(imports),
            "forbidden_primary_modules_absent": sorted(forbidden)}


def _concat_paths(*paths):
    output = []
    for path in paths:
        if not path:
            continue
        if output and output[-1] != path[0]:
            raise AssertionError("path factors do not meet")
        output.extend(path if not output else path[1:])
    return output


def _cyclic_or_inverse(word):
    output = []
    for oriented in (word, inverse(word)):
        output.extend(oriented[index:] + oriented[:index]
                      for index in range(len(oriented)))
    return output


def _dehn_prove(word, relator):
    """Return logged, locally checkable Dehn reductions to the empty word."""
    if len(relator) != 8:
        raise AssertionError("expected the length-eight genus-2 relator")
    witnesses = {}
    for cyclic in _cyclic_or_inverse(relator):
        for length in range(5, 9):
            witnesses[tuple(cyclic[:length])] = cyclic[length:]
    current = free_reduce(word)
    steps = []
    while current:
        chosen = None
        for length in (8, 7, 6, 5):
            for index in range(len(current) - length + 1):
                subword = tuple(current[index:index + length])
                if subword in witnesses:
                    complement = witnesses[subword]
                    replacement = inverse(complement)
                    chosen = (index, list(subword), complement, replacement)
                    break
            if chosen is not None:
                break
        if chosen is None:
            raise AssertionError(f"nontrivial reduced residual: {current}")
        index, subword, complement, replacement = chosen
        steps.append([index, subword, complement])
        current = free_reduce(
            current[:index] + replacement + current[index + len(subword):])
    return steps


def _verify_dehn(word, relator, steps):
    current = free_reduce(word)
    rotations = {tuple(cyclic) for cyclic in _cyclic_or_inverse(relator)}
    for number, (index, subword, complement) in enumerate(steps, 1):
        if len(subword) <= len(complement):
            raise AssertionError(f"Dehn step {number}: replacement is not shorter")
        if tuple(subword + complement) not in rotations:
            raise AssertionError(f"Dehn step {number}: no relator witness")
        if current[index:index + len(subword)] != subword:
            raise AssertionError(f"Dehn step {number}: subword is absent")
        current = free_reduce(
            current[:index] + inverse(complement) +
            current[index + len(subword):])
    if current:
        raise AssertionError(f"Dehn proof ended at nonempty word {current}")


def build_problem():
    bundle = build_alternative_bundle()
    stack, levels, fiber = bundle["_beta_stack"], bundle["m"], bundle["F"]
    presentation = DeterministicPresentation(stack, ("S", 0, "p"))
    loops = {name: rail_loop(fiber, name) for name in NAMES}

    def at(level, path):
        return [("S", level, vertex) for vertex in path]

    def product(level, factors):
        paths = []
        for name, sign in factors:
            path = at(level, loops[name])
            paths.append(path if sign > 0 else list(reversed(path)))
        return _concat_paths(*paths)

    vertical = [("S", level, "p") for level in range(levels + 1)]
    residuals = []
    lengths = {}
    for name in NAMES:
        bottom = at(0, loops[name])
        top_target = product(levels, TARGETS[name])
        residual_path = _concat_paths(
            bottom, vertical, list(reversed(top_target)),
            list(reversed(vertical)))
        residuals.append(presentation.loop_word(residual_path))
        lengths[name] = len(residual_path) - 1
    return bundle, presentation, residuals, lengths


def _finish_replay(live, relators, words, certificate):
    rank, reduced_relators, reduced_words = renumber(live, relators, words)
    if rank != 4 or not reduced_relators:
        raise AssertionError("alternative trace did not reduce to a surface group")
    surface_relator = reduced_relators[0]
    rotations = {tuple(word) for word in _cyclic_or_inverse(surface_relator)}
    if any(tuple(relator) not in rotations for relator in reduced_relators):
        raise AssertionError("reduced presentation has a non-surface relator")
    dehn = certificate["based_monodromy"]["dehn_steps"]
    for name, word in zip(NAMES, reduced_words):
        _verify_dehn(word, surface_relator, dehn[name])
    expected_relator = certificate["based_monodromy"]["reduced_surface_relator"]
    if surface_relator != expected_relator:
        raise AssertionError("reduced surface relator changed")
    return rank, surface_relator, reduced_words


def generate_certificate():
    bundle, presentation, residuals, path_lengths = build_problem()
    live, relators, words, certificate = simplify(
        presentation.ngens, presentation.relators, residuals,
        verbose=True, certify=True)
    replayed = verify_certificate(
        presentation.ngens, presentation.relators, residuals, certificate,
        verbose=True)
    if replayed != (live, relators, words):
        raise AssertionError("immediate Tietze replay disagrees")
    rank, reduced_relators, reduced_words = renumber(live, relators, words)
    if rank != 4 or not reduced_relators:
        raise AssertionError("alternative trace did not reduce to a surface group")
    surface_relator = reduced_relators[0]
    rotations = {tuple(word) for word in _cyclic_or_inverse(surface_relator)}
    if any(tuple(relator) not in rotations for relator in reduced_relators):
        raise AssertionError("reduced presentation has a non-surface relator")
    dehn = {name: _dehn_prove(word, surface_relator)
            for name, word in zip(NAMES, reduced_words)}
    certificate["based_monodromy"] = {
        "claim": "x->y^-1, y->yx, r->r, s->s",
        "convention": "bottom loop equals vertical * top target * vertical^-1",
        "construction": "alternative 64-interface open beta trace",
        "import_audit": _import_audit(),
        "stack_f_vector": bundle["_beta_stack"].f_vector(),
        "interfaces": bundle["m"],
        "input_generators": presentation.ngens,
        "input_relators": len(presentation.relators),
        "residual_path_edges": path_lengths,
        "reduced_rank": rank,
        "reduced_surface_relator": surface_relator,
        "dehn_steps": dehn,
        "dehn_step_counts": {name: len(dehn[name]) for name in NAMES},
        "residuals_after_dehn": {name: [] for name in NAMES},
    }
    _finish_replay(live, relators, words, certificate)
    return certificate


def verify_saved_certificate(certificate):
    _, presentation, residuals, _ = build_problem()
    live, relators, words = verify_certificate(
        presentation.ngens, presentation.relators, residuals, certificate,
        verbose=True)
    rank, surface_relator, _ = _finish_replay(
        live, relators, words, certificate)
    metadata = certificate["based_monodromy"]
    if metadata["claim"] != "x->y^-1, y->yx, r->r, s->s":
        raise AssertionError("certificate claim changed")
    if metadata["input_generators"] != presentation.ngens:
        raise AssertionError("input generator count changed")
    if metadata["input_relators"] != len(presentation.relators):
        raise AssertionError("input relator count changed")
    if metadata["import_audit"] != _import_audit():
        raise AssertionError("construction import boundary changed")
    return {
        "claim": metadata["claim"],
        "interfaces": metadata["interfaces"],
        "tietze_steps": certificate["steps_count"],
        "dehn_step_counts": metadata["dehn_step_counts"],
        "reduced_rank": rank,
        "reduced_surface_relator": surface_relator,
    }


def save_deterministic(path, certificate):
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            with io.TextIOWrapper(zipped, encoding="ascii") as text:
                json.dump(certificate, text, separators=(",", ":"), sort_keys=True)
                text.write("\n")


def load(path):
    with gzip.open(path, "rt", encoding="ascii") as stream:
        return json.load(stream)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=ROOT / "alternative_based_monodromy.json.gz")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        print("rebuilding alternative trace and replaying saved proof...", flush=True)
        result = verify_saved_certificate(load(args.output))
        print("PASS: exact based pi1 monodromy", result)
    else:
        print("building alternative trace and generating proof...", flush=True)
        certificate = generate_certificate()
        save_deterministic(args.output, certificate)
        print(f"wrote {args.output}")
        print(verify_saved_certificate(load(args.output)))


if __name__ == "__main__":
    main()
