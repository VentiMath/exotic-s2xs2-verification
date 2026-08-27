#!/usr/bin/env python3
"""Independent peripheral extraction from the marked bundle triangulation.

This is intentionally separate from complement.py, pi1.py, paper_bridge.py,
peripheral_bridge.py, r_run.py, and sweep.py.  The only project-level input is
the marked triangulation returned by bundle.build_bundle.  Everything after
that point -- derived frontier, orientations, dual meridians, normal
push-offs, whiskers, and canonical serialization -- is implemented here.

The output is basis-free.  It records literal paths in the derived frontier
and its induced-complement retraction rather than words in the large,
set-order-dependent spanning-tree presentation used by r_run.py.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

def vkey(vertex):
    return repr(vertex)


def skey(simplex):
    return tuple(sorted((repr(v) for v in simplex)))


def canonical(value):
    """JSON-safe canonical encoding for nested tuple vertices/simplices."""
    if isinstance(value, frozenset):
        return {"simplex": [canonical(v) for v in sorted(value, key=vkey)]}
    if isinstance(value, tuple):
        return {"tuple": [canonical(v) for v in value]}
    if isinstance(value, list):
        return [canonical(v) for v in value]
    if isinstance(value, dict):
        return {str(k): canonical(value[k]) for k in sorted(value)}
    return value


def digest(value):
    blob = json.dumps(canonical(value), sort_keys=True,
                      separators=(",", ":")).encode("ascii")
    return hashlib.sha256(blob).hexdigest()


def closed_edge_path(edges, path):
    if not path or path[0] != path[-1]:
        return False
    return all(u == v or frozenset((u, v)) in edges
               for u, v in zip(path, path[1:]))


def inverse_path(path):
    return list(reversed(path))


def free_reduce(word):
    result = []
    for letter in word:
        if result and result[-1] == -letter:
            result.pop()
        else:
            result.append(letter)
    return result


def cyclic_reduce(word):
    word = free_reduce(word)
    while len(word) > 1 and word[0] == -word[-1]:
        word = word[1:-1]
    return word


def join_paths(*paths):
    out = list(paths[0])
    for path in paths[1:]:
        if out[-1] != path[0]:
            raise AssertionError(f"path endpoints differ: {out[-1]!r}, {path[0]!r}")
        out.extend(path[1:])
    return out


def rotate_closed(path, index):
    body = path[:-1]
    body = body[index:] + body[:index]
    return body + [body[0]]


def parity(sequence):
    return -1 if sum(sequence[i] > sequence[j]
                     for i in range(len(sequence))
                     for j in range(i + 1, len(sequence))) % 2 else 1


def orientation_signs(K, top_simplices, dimension):
    """Orient pseudomanifold components without Complex.orientation_signs."""
    tops = sorted(top_simplices, key=skey)
    ordered = {s: tuple(sorted(s, key=K.rank.get)) for s in tops}
    incidence = defaultdict(list)
    for simplex in tops:
        vertices = ordered[simplex]
        for i in range(dimension + 1):
            face = frozenset(vertices[:i] + vertices[i + 1:])
            incidence[face].append((simplex, i))
    if any(len(items) > 2 for items in incidence.values()):
        raise AssertionError("non-pseudomanifold incidence")

    signs = {}
    for seed in tops:
        if seed in signs:
            continue
        signs[seed] = 1
        queue = deque([seed])
        while queue:
            simplex = queue.popleft()
            vertices = ordered[simplex]
            for i in range(dimension + 1):
                face = frozenset(vertices[:i] + vertices[i + 1:])
                for neighbour, j in incidence[face]:
                    if neighbour == simplex:
                        continue
                    wanted = -signs[simplex] * (-1 if (i - j) % 2 else 1)
                    if neighbour in signs and signs[neighbour] != wanted:
                        raise AssertionError("nonorientable pseudomanifold")
                    if neighbour not in signs:
                        signs[neighbour] = wanted
                        queue.append(neighbour)
    return signs


def graph_path(start, goals, adjacency, allowed=None):
    goals = set(goals)
    allowed = set(adjacency) if allowed is None else set(allowed)
    if start not in allowed:
        raise AssertionError("path start is outside allowed set")
    previous = {start: None}
    queue = deque([start])
    finish = None
    while queue:
        vertex = queue.popleft()
        if vertex in goals:
            finish = vertex
            break
        for neighbour in sorted(adjacency[vertex], key=vkey):
            if neighbour in allowed and neighbour not in previous:
                previous[neighbour] = vertex
                queue.append(neighbour)
    if finish is None:
        raise AssertionError("no allowed path to target")
    path = [finish]
    while previous[path[-1]] is not None:
        path.append(previous[path[-1]])
    return list(reversed(path))


def punctured_grid_cycles(K, rows, removed_vertices):
    """Oriented boundary of a triangulated grid after deleting hit stars."""
    oriented = []
    for i in range(len(rows) - 1):
        for j in range(len(rows[0]) - 1):
            coordinates = [(i, j), (i + 1, j),
                           (i, j + 1), (i + 1, j + 1)]
            position = {rows[u][v]: (u, v) for u, v in coordinates}
            cell_triangles = []
            for vertices in combinations(position, 3):
                triangle = frozenset(vertices)
                if triangle not in K.simplices[2]:
                    continue
                ordered = tuple(sorted(triangle, key=K.rank.get))
                points = [position[v] for v in ordered]
                determinant = ((points[1][0] - points[0][0]) *
                               (points[2][1] - points[0][1]) -
                               (points[1][1] - points[0][1]) *
                               (points[2][0] - points[0][0]))
                if not determinant:
                    continue
                orientation = ordered if determinant > 0 else \
                    (ordered[0], ordered[2], ordered[1])
                oriented.append((triangle, orientation))
                cell_triangles.append(triangle)
            if len(set(cell_triangles)) != 2:
                raise AssertionError(f"grid cell {(i, j)} is not triangulated")

    removed_vertices = set(removed_vertices)
    coefficients = defaultdict(int)
    representatives = {}
    for triangle, (a, b, c) in oriented:
        if triangle & removed_vertices:
            continue
        for u, v in ((a, b), (b, c), (c, a)):
            edge = frozenset((u, v))
            ordered = tuple(sorted(edge, key=K.rank.get))
            coefficients[edge] += 1 if (u, v) == ordered else -1
            representatives[edge] = ordered
    directed = []
    for edge, coefficient in coefficients.items():
        if not coefficient:
            continue
        if abs(coefficient) != 1:
            raise AssertionError("punctured grid has nonmanifold boundary")
        u, v = representatives[edge]
        directed.append((u, v) if coefficient > 0 else (v, u))
    outgoing = defaultdict(list)
    incoming = defaultdict(list)
    for u, v in directed:
        outgoing[u].append(v)
        incoming[v].append(u)
    vertices = set(outgoing) | set(incoming)
    if any(len(outgoing[v]) != 1 or len(incoming[v]) != 1 for v in vertices):
        raise AssertionError("punctured grid boundary is not circular")
    unused = set(directed)
    cycles = []
    while unused:
        start_edge = min(unused, key=lambda edge: (vkey(edge[0]), vkey(edge[1])))
        start, current = start_edge
        cycle = [start, current]
        unused.remove(start_edge)
        while current != start:
            following = outgoing[current][0]
            if (current, following) not in unused:
                raise AssertionError("punctured grid boundary repeats an edge")
            unused.remove((current, following))
            cycle.append(following)
            current = following
        cycles.append(cycle)
    return cycles


def local_rank_one_certificate(K, vertices, loops):
    """Elementary Tietze proof that based local loops are equal or inverse.

    This small implementation is independent of pi1.py, fast_tietze.py, and
    the original local-N certificate.  It returns the reduced free-rank-one
    images of the supplied loops and the elimination count.
    """
    vertices = set(vertices)
    edges = sorted((edge for edge in K.simplices[1] if edge <= vertices), key=skey)
    triangles = sorted((tri for tri in K.simplices[2] if tri <= vertices), key=skey)
    adjacency = {vertex: [] for vertex in vertices}
    for edge in edges:
        u, v = tuple(edge)
        adjacency[u].append(v)
        adjacency[v].append(u)
    for neighbours in adjacency.values():
        neighbours.sort(key=vkey)
    base = loops[0][0]
    parent = {base: None}
    queue = deque([base])
    while queue:
        vertex = queue.popleft()
        for neighbour in adjacency[vertex]:
            if neighbour not in parent:
                parent[neighbour] = vertex
                queue.append(neighbour)
    if len(parent) != len(vertices):
        raise AssertionError("local complement is disconnected")
    tree = {frozenset((vertex, previous))
            for vertex, previous in parent.items() if previous is not None}
    generator_edges = [edge for edge in edges if edge not in tree]
    generators = {edge: i + 1 for i, edge in enumerate(generator_edges)}

    def edge_word(u, v):
        if u == v:
            return []
        edge = frozenset((u, v))
        if edge in tree:
            return []
        ordered = tuple(sorted(edge, key=K.rank.get))
        letter = generators[edge]
        return [letter if (u, v) == ordered else -letter]

    def path_word(path):
        result = []
        for u, v in zip(path, path[1:]):
            result.extend(edge_word(u, v))
        return free_reduce(result)

    relators = []
    for triangle in triangles:
        a, b, c = tuple(sorted(triangle, key=K.rank.get))
        relator = cyclic_reduce(edge_word(a, b) + edge_word(b, c) +
                                edge_word(c, a))
        if relator:
            relators.append(relator)
    words = [path_word(loop) for loop in loops]
    steps = 0
    while True:
        choices = []
        for index, relator in enumerate(relators):
            counts = defaultdict(int)
            for letter in relator:
                counts[abs(letter)] += 1
            for generator, count in counts.items():
                if count == 1:
                    choices.append((len(relator), index, generator))
        if not choices:
            break
        _, index, generator = min(choices)
        relator = relators[index]
        position = next(i for i, letter in enumerate(relator)
                        if abs(letter) == generator)
        replacement = ([-letter for letter in reversed(relator[:position])] +
                       [-letter for letter in reversed(relator[position + 1:])])
        if relator[position] < 0:
            replacement = [-letter for letter in reversed(replacement)]

        def substitute(word):
            result = []
            for letter in word:
                if letter == generator:
                    result.extend(replacement)
                elif letter == -generator:
                    result.extend(-x for x in reversed(replacement))
                else:
                    result.append(letter)
            return free_reduce(result)

        updated = []
        for other_index, other in enumerate(relators):
            if other_index == index:
                continue
            reduced = cyclic_reduce(substitute(other))
            if reduced:
                updated.append(reduced)
        relators = updated
        words = [substitute(word) for word in words]
        steps += 1
    live = sorted({abs(letter) for relator in relators for letter in relator} |
                  {abs(letter) for word in words for letter in word})
    if len(live) != 1 or relators:
        raise AssertionError(
            f"local complement did not reduce freely to rank one: "
            f"rank={len(live)}, relators={len(relators)}")
    renumber = {live[0]: 1}
    words = [[renumber[abs(letter)] * (1 if letter > 0 else -1)
              for letter in word] for word in words]
    return words, steps, {
        "vertices": len(vertices), "edges": len(edges),
        "triangles": len(triangles), "raw_generators": len(generator_edges),
    }


@dataclass
class ExtractedLoop:
    name: str
    frontier_loop: list
    complement_whisker: list
    complement_loop: list
    source: dict

    def record(self):
        return {
            "name": self.name,
            "source": self.source,
            "frontier_edges": len(self.frontier_loop) - 1,
            "whisker_edges": len(self.complement_whisker) - 1,
            "complement_edges": len(self.complement_loop) - 1,
            "frontier_sha256": digest(self.frontier_loop),
            "whisker_sha256": digest(self.complement_whisker),
            "complement_loop_sha256": digest(self.complement_loop),
        }


class IndependentFrontier:
    def __init__(self, K, torus_vertices):
        self.K = K
        self.torus_vertices = set(torus_vertices)
        self.torus_simplices = {
            d: {s for s in K.simplices[d] if s <= self.torus_vertices}
            for d in range(3)
        }
        # Fullness is checked directly from K, not delegated to Complex.
        for simplex in K.all_simplices():
            if simplex <= self.torus_vertices:
                dim = len(simplex) - 1
                if dim > 2 or simplex not in self.torus_simplices[dim]:
                    raise AssertionError("marked torus is not a full 2-subcomplex")

        self.complement_vertices = set(K.vertices()) - self.torus_vertices
        self.complement_edges = {
            edge for edge in K.simplices[1]
            if edge <= self.complement_vertices
        }
        self.complement_adjacency = {v: set() for v in self.complement_vertices}
        for edge in self.complement_edges:
            u, v = tuple(edge)
            self.complement_adjacency[u].add(v)
            self.complement_adjacency[v].add(u)

        # Vertices of the first-derived regular-neighbourhood frontier.
        self.frontier_vertices = {
            simplex for simplex in K.all_simplices()
            if simplex & self.torus_vertices and simplex - self.torus_vertices
        }
        self.frontier_adjacency = {s: set() for s in self.frontier_vertices}
        # In a barycentric subdivision two vertices are adjacent exactly when
        # their source simplices are comparable.  Enumerating the at most 30
        # proper faces of each 4-simplex is linear in the complex size and
        # avoids a quadratic all-pairs search.
        for larger in self.frontier_vertices:
            vertices = tuple(larger)
            for size in range(1, len(vertices)):
                for face_vertices in combinations(vertices, size):
                    smaller = frozenset(face_vertices)
                    if smaller in self.frontier_vertices:
                        self.frontier_adjacency[larger].add(smaller)
                        self.frontier_adjacency[smaller].add(larger)

    def retract(self, simplex):
        candidates = simplex - self.torus_vertices
        if not candidates:
            raise AssertionError("frontier simplex has no complement vertex")
        return max(candidates, key=self.K.rank.get)

    def retract_path(self, path):
        result = [self.retract(simplex) for simplex in path]
        if any(u != v and frozenset((u, v)) not in self.complement_edges
               for u, v in zip(result, result[1:])):
            raise AssertionError("derived retraction did not give an edge path")
        return result

    def complement_path(self, start, goals, allowed=None):
        return graph_path(start, goals, self.complement_adjacency, allowed)

    def frontier_path(self, start, goals, allowed=None):
        return graph_path(start, goals, self.frontier_adjacency, allowed)

    def dual_meridian(self, triangle, ambient_signs, torus_signs):
        """Oriented boundary of the dual normal disk to a torus triangle."""
        triangle = frozenset(triangle)
        codim_one = sorted((s for s in self.K.simplices[3] if triangle < s),
                           key=skey)
        tops = sorted((s for s in self.K.simplices[4] if triangle < s),
                      key=skey)
        adjacency = defaultdict(list)
        for top in tops:
            faces = [face for face in codim_one if face < top]
            if len(faces) != 2:
                raise AssertionError("bad codimension-two link")
            adjacency[faces[0]].append((top, faces[1]))
            adjacency[faces[1]].append((top, faces[0]))
        if not codim_one or any(len(adjacency[face]) != 2 for face in codim_one):
            raise AssertionError("normal link is not a circle")

        start = codim_one[0]
        cycle = [start]
        current, previous_top = start, None
        while True:
            options = sorted((item for item in adjacency[current]
                              if item[0] != previous_top), key=lambda x: skey(x[0]))
            top, following = options[0]
            cycle.append(top)
            if following == start:
                break
            cycle.append(following)
            current, previous_top = following, top
        if set(cycle[::2]) != set(codim_one) or set(cycle[1::2]) != set(tops):
            raise AssertionError("normal link walk did not use every incidence")

        a = next(iter(cycle[0] - triangle))
        b = next(iter(cycle[2] - triangle))
        top = cycle[1]
        top_order = tuple(sorted(top, key=self.K.rank.get))
        tri_order = tuple(sorted(triangle, key=self.K.rank.get))
        positions = {vertex: i for i, vertex in enumerate(top_order)}
        induced = torus_signs[triangle] * parity(
            [positions[v] for v in tri_order + (a, b)])
        if induced != ambient_signs[top]:
            # Reverse while retaining the same initial codimension-one face.
            cycle = [cycle[0]] + list(reversed(cycle[1:]))
        loop = cycle + [cycle[0]]
        if any(s not in self.frontier_vertices for s in loop):
            raise AssertionError("dual meridian left the derived frontier")
        return loop

    def push_off(self, torus_loop, side):
        """Push a torus edge loop into the frontier using product squares."""
        corners = [frozenset((vertex, side(vertex))) for vertex in torus_loop]
        if any(corner not in self.frontier_vertices for corner in corners):
            raise AssertionError("normal corner is absent from frontier")
        output = [corners[0]]
        for (u, v), (left, right) in zip(zip(torus_loop, torus_loop[1:]),
                                         zip(corners, corners[1:])):
            if left == right:
                continue
            square = {u, v, side(u), side(v)}
            allowed = {simplex for simplex in self.frontier_vertices
                       if simplex <= square}
            segment = self.frontier_path(left, {right}, allowed)
            output.extend(segment[1:])
        if output[0] != output[-1]:
            raise AssertionError("push-off is not closed")
        return output


def rail_loop(F, name):
    """Reconstruct paper x,y,r,s directly from marked rail data."""
    V, phi = F["V"], F["phi0"]
    specifications = {
        "x": ("a", 1, V("a", 1, 1), -1),
        "y": ("b", -1, V("b", -1, 1), 1),
        "r": ("e", 1, phi[V("a", 1, 1)], -1),
        "s": ("d", -1, phi[V("b", -1, 1)], 1),
    }
    curve, row, start, direction = specifications[name]
    rail = [V(curve, row, i) for i in range(F["K_BAND"][curve])]
    index = rail.index(start)
    rail = rail[index:] + rail[:index]
    if direction < 0:
        rail = [rail[0]] + list(reversed(rail[1:]))
    loop = ["p"] + rail + [rail[0], "p"]
    if not closed_edge_path(F["L"].simplices[1], loop):
        raise AssertionError(f"marked {name} rail is not an edge loop")
    return loop


def global_bundle_loops(B):
    """Literal complement loops for x,y,r,s,A,B at q=(A0,p,J2)."""
    J = lambda k: ("J", k)
    result = {}
    for name in "xyrs":
        result[name] = [(('A', 0, vertex), J(2)) for vertex in rail_loop(B["F"], name)]
    alpha_positive = [(('A', t, 'p'), J(2)) for t in (0, 1, 2, 0)]
    result["A"] = inverse_path(alpha_positive)
    cut = (('A', 1, 'p'), J(2))
    local = [cut]
    local.extend((('S', level, 'p'), ('t', 1))
                 for level in range(1, B["m"]))
    local.extend((('A', 1, 'p'), J(k)) for k in (0, 1, 2))
    beta_positive = join_paths(
        [(('A', 0, 'p'), J(2)), cut],
        local,
        [cut, (('A', 0, 'p'), J(2))],
    )
    result["B"] = inverse_path(beta_positive)
    return result


def based_frontier_loop(name, frontier, raw_loop, whisker, source):
    retracted = frontier.retract_path(raw_loop)
    if whisker[-1] != retracted[0]:
        raise AssertionError(f"{name}: whisker misses retracted loop")
    full = whisker + retracted[1:] + inverse_path(whisker)[1:]
    if not closed_edge_path(frontier.complement_edges, full):
        raise AssertionError(f"{name}: retracted based loop is invalid")
    return ExtractedLoop(name, raw_loop, whisker, full, source)


def extract_meridian(name, B, frontier, crossing, fiber_whisker,
                     ambient_signs, torus_signs):
    triangles = sorted((triangle for triangle in frontier.torus_simplices[2]
                        if crossing in triangle), key=skey)
    if not triangles:
        raise AssertionError(f"{name}: no torus triangle at crossing")
    local_vertices = {
        vertex for simplex in B["K"].all_simplices()
        if crossing in simplex for vertex in simplex
        if vertex in frontier.complement_vertices
    }
    choices = []
    for triangle in triangles:
        meridian = frontier.dual_meridian(triangle, ambient_signs, torus_signs)
        targets = set(frontier.retract_path(meridian[:-1]))
        try:
            normal = frontier.complement_path(
                fiber_whisker[-1], targets, local_vertices | {fiber_whisker[-1]})
        except AssertionError:
            continue
        target = normal[-1]
        retractions = frontier.retract_path(meridian[:-1])
        rotation = retractions.index(target)
        meridian = rotate_closed(meridian, rotation)
        whisker = fiber_whisker + normal[1:]
        choices.append((len(normal), skey(triangle), meridian, whisker, triangle))
    if not choices:
        raise AssertionError(f"{name}: crossing star has no normal connector")
    _, _, meridian, whisker, triangle = sorted(choices, key=lambda x: (x[0], x[1]))[0]
    return based_frontier_loop(name, frontier, meridian, whisker, {
        "kind": "oriented_dual_meridian",
        "crossing": canonical(crossing),
        "dual_triangle": canonical(triangle),
        "fiber_whisker_sha256": digest(fiber_whisker),
    })


def extract(B):
    K = B["K"]
    torus_vertices = set(B["Ta_verts"]) | set(B["Tb_verts"])
    frontier = IndependentFrontier(K, torus_vertices)
    ambient_signs = orientation_signs(K, K.simplices[4], 4)
    torus_signs = orientation_signs(K, frontier.torus_simplices[2], 2)
    marked = global_bundle_loops(B)
    q = (('A', 0, 'p'), ('J', 2))
    if any(path[0] != q or path[-1] != q for path in marked.values()):
        raise AssertionError("named bundle loops do not share q")
    if any(not closed_edge_path(frontier.complement_edges, path)
           for path in marked.values()):
        raise AssertionError("named bundle loop leaves the complement")

    F, c, e, m = B["F"], B["c"], B["e"], B["m"]
    J = lambda k: ("J", k)
    y, s = rail_loop(F, "y"), rail_loop(F, "s")
    c_hits = [i for i, vertex in enumerate(y[:-1]) if vertex in set(c)]
    e_hits = [i for i, vertex in enumerate(s[:-1]) if vertex in set(e)]
    if len(c_hits) != 1 or len(e_hits) != 1:
        raise AssertionError("paper whisker does not have a unique torus crossing")
    cy, se = y[c_hits[0]], s[e_hits[0]]
    y1 = [(('A', 0, vertex), J(2)) for vertex in y[:c_hits[0] + 1]]
    s2 = [(('A', 0, vertex), J(2)) for vertex in s[:e_hits[0] + 1]]

    def crossing_star_complement(crossing):
        return {
            vertex for simplex in K.all_simplices() if crossing in simplex
            for vertex in simplex if vertex in frontier.complement_vertices
        }

    meridian_alpha = extract_meridian(
        "geom_M_independent", B, frontier,
        (('A', 0, cy), J(1)), y1, ambient_signs, torus_signs)
    meridian_beta = extract_meridian(
        "N_grid_local_independent", B, frontier,
        (('A', 1, se), J(2)), s2, ambient_signs, torus_signs)

    # Independently reconstruct the punctured alpha-transport grid of s.
    # Its local detour is the source-side N_grid.  Rotating the outer
    # boundary to the paper's AsA^-1 corner transports and reverses it,
    # producing the actual Table-1 meridian N = A*N_grid^-1*A^-1.
    phi = B["phi0"]
    alpha_s_rows = [
        [(('A', 0, vertex), J(2)),
         (('A', 1, vertex), J(2)),
         (('A', 2, vertex), J(2)),
         (('A', 0, phi[vertex]), J(2))]
        for vertex in s
    ]
    for row in alpha_s_rows:
        if any(frozenset((u, v)) not in K.simplices[1]
               for u, v in zip(row, row[1:]) if u != v):
            raise AssertionError("alpha-s transport row is not simplicial")
    for upper, lower in zip(alpha_s_rows, alpha_s_rows[1:]):
        if any(frozenset((u, v)) not in K.simplices[1]
               for u, v in zip(upper, lower) if u != v):
            raise AssertionError("alpha-s transport column is not simplicial")
    alpha_hits = [(i, j, vertex)
                  for i, row in enumerate(alpha_s_rows)
                  for j, vertex in enumerate(row)
                  if vertex in set(B["Ta_verts"])]
    beta_hits = [(i, j, vertex)
                 for i, row in enumerate(alpha_s_rows)
                 for j, vertex in enumerate(row)
                 if vertex in set(B["Tb_verts"])]
    if alpha_hits or len(beta_hits) != 1:
        raise AssertionError("alpha-s grid has wrong torus incidences")
    grid_cycles = punctured_grid_cycles(K, alpha_s_rows, torus_vertices)
    if sorted(len(cycle) - 1 for cycle in grid_cycles) != [8, 12]:
        raise AssertionError("punctured alpha-s boundary has wrong components")
    predecessor = (('A', 0, s[e_hits[0] - 1]), J(2))
    approach = (('A', 0, se), J(2))
    corrected = next(cycle for cycle in grid_cycles
                     if predecessor in cycle and approach in cycle)
    body = corrected[:-1]
    predecessor_index = body.index(predecessor)
    approach_index = body.index(approach)
    if predecessor_index >= approach_index:
        body = list(reversed(body))
        predecessor_index = body.index(predecessor)
        approach_index = body.index(approach)
    detour = body[predecessor_index:approach_index + 1]
    grid_meridian = [approach, predecessor] + detour[1:] + [approach]
    if not closed_edge_path(frontier.complement_edges, grid_meridian):
        raise AssertionError("grid detour is not a complement loop")

    local_normal = meridian_beta.complement_whisker[len(s2) - 1:]
    local_dual_retraction = frontier.retract_path(meridian_beta.frontier_loop)
    local_dual = (local_normal + local_dual_retraction[1:] +
                  inverse_path(local_normal)[1:])
    local_vertices = {
        vertex for top in K.simplices[4] if beta_hits[0][2] in top
        for vertex in top if vertex in frontier.complement_vertices
    } | set(grid_meridian) | set(local_dual)
    local_words, local_steps, local_counts = local_rank_one_certificate(
        K, local_vertices, [grid_meridian, local_dual])
    if local_words[0] != local_words[1] or local_words[0] not in ([1], [-1]):
        raise AssertionError(
            f"grid detour has wrong oriented-meridian image: {local_words}")

    full_grid_meridian = s2 + grid_meridian[1:] + inverse_path(s2)[1:]
    if not closed_edge_path(frontier.complement_edges, full_grid_meridian):
        raise AssertionError("based grid meridian is not a complement loop")
    paper_N_path = join_paths(
        marked["A"], inverse_path(full_grid_meridian),
        inverse_path(marked["A"]))
    if not closed_edge_path(frontier.complement_edges, paper_N_path):
        raise AssertionError("transported paper N is not a complement loop")
    paper_N_record = {
        "name": "geom_N_independent",
        "kind": "transported_oriented_grid_meridian",
        "formula": "A * N_grid^-1 * A^-1",
        "complement_edges": len(paper_N_path) - 1,
        "complement_loop_sha256": digest(paper_N_path),
        "source_grid_meridian_sha256": digest(full_grid_meridian),
        "grid_detour_edges": len(grid_meridian) - 1,
        "grid_boundary_lengths": sorted(len(cycle) - 1 for cycle in grid_cycles),
        "grid_boundary_sha256": sorted(digest(cycle) for cycle in grid_cycles),
        "transport_grid_sha256": digest(alpha_s_rows),
        "unique_beta_hit": canonical(beta_hits[0]),
        "local_rank": 1,
        "local_tietze_steps": local_steps,
        "local_complex": local_counts,
        "local_grid_image": local_words[0],
        "local_dual_image": local_words[1],
        "local_inverse_comparison": free_reduce(
            [-letter for letter in reversed(local_words[0])] +
            [-letter for letter in reversed(local_words[1])]),
        "local_orientation_check": "PASS: grid detour equals oriented dual, not inverse",
    }

    # Alpha product-framing section: lift A from c_y and close through the
    # y_1 half of c.  The direction is selected from the literal y prefix,
    # not from any old peripheral word.
    kc, cy_index = len(c), c.index(cy)
    if kc % 2:
        raise AssertionError("alpha monodromy is not a half rotation")
    opposite = (cy_index + kc // 2) % kc
    va = lambda t, i: (('A', t, c[i % kc]), J(1))
    alpha_section = [va(0, cy_index), va(2, opposite),
                     va(1, opposite), va(0, opposite)]
    i = opposite
    while i != cy_index:
        i = (i - 1) % kc
        alpha_section.append(va(0, i))
    c_rail = B["c_rail"]
    side_alpha = lambda vertex: (
        ('A', vertex[0][1], c_rail[c.index(vertex[0][2])]), J(1))
    alpha_raw = frontier.push_off(alpha_section, side_alpha)
    alpha_target = frontier.retract(alpha_raw[0])
    alpha_normal = frontier.complement_path(
        y1[-1], {alpha_target},
        crossing_star_complement((('A', 0, cy), J(1))) | {y1[-1]})
    alpha_whisker = y1 + alpha_normal[1:]
    longitude_alpha = based_frontier_loop(
        "lb_a_y1_independent", frontier, alpha_raw, alpha_whisker, {
            "kind": "product_framing_push_off",
            "crossing": canonical((('A', 0, cy), J(1))),
            "fiber_whisker": "y_1",
            "base_direction": "A",
            "closing_half": "negative c half",
            "torus_section_sha256": digest(alpha_section),
        })

    # Beta product-framing section: lift B from s_e.  The marked flip stack
    # fixes e pointwise, so there is no fiber drift.
    ke, se_index = len(e), e.index(se)
    vb = lambda k, i: (('A', 1, e[i % ke]), J(k))
    sb = lambda level, i: (('S', level, e[i % ke]), ('t', 1))
    beta_section = [vb(2, se_index), vb(1, se_index), vb(0, se_index)]
    beta_section.extend(sb(level, se_index) for level in range(m - 1, 0, -1))
    beta_section.append(vb(2, se_index))
    e_rail = B["e_rail"]

    def side_beta(vertex):
        if vertex[1] == ('t', 1):
            return (('S', vertex[0][1], e_rail[e.index(vertex[0][2])]), ('t', 1))
        return (('A', 1, e_rail[e.index(vertex[0][2])]), vertex[1])

    beta_raw = frontier.push_off(beta_section, side_beta)
    beta_target = frontier.retract(beta_raw[0])
    beta_normal = frontier.complement_path(
        s2[-1], {beta_target},
        crossing_star_complement((('A', 1, se), J(2))) | {s2[-1]})
    beta_whisker = s2 + beta_normal[1:]
    longitude_beta = based_frontier_loop(
        "lb_b_s2_independent", frontier, beta_raw, beta_whisker, {
            "kind": "product_framing_push_off",
            "crossing": canonical((('A', 1, se), J(2))),
            "fiber_whisker": "s_2",
            "base_direction": "B",
            "fiber_drift": 0,
            "torus_section_sha256": digest(beta_section),
        })

    # Pair-level basing check.  Each meridian and longitude begins with the
    # identical literal paper whisker before a normal connector in the same
    # crossing star/product collar.
    if meridian_alpha.complement_whisker[:len(y1)] != y1 or \
            longitude_alpha.complement_whisker[:len(y1)] != y1:
        raise AssertionError("alpha peripheral elements do not share y_1")
    if meridian_beta.complement_whisker[:len(s2)] != s2 or \
            longitude_beta.complement_whisker[:len(s2)] != s2:
        raise AssertionError("local beta meridian/longitude lost the s_2 prefix")

    # Sensitivity controls: the errors most likely to survive an unbased
    # calculation must change the literal certificate.
    positive_alpha = [va(0, cy_index), va(2, opposite),
                      va(1, opposite), va(0, opposite)]
    i = opposite
    while i != cy_index:
        i = (i + 1) % kc
        positive_alpha.append(va(0, i))
    if digest(positive_alpha) == digest(alpha_section):
        raise AssertionError("the two alpha half-sections were not distinguished")
    y2 = [(('A', 0, vertex), J(2))
          for vertex in reversed(y[c_hits[0]:])]
    if y2[0] != q or y2[-1] != y1[-1] or digest(y2) == digest(y1):
        raise AssertionError("the opposite-side alpha whisker was not distinguished")
    if digest(inverse_path(meridian_alpha.frontier_loop)) == \
            digest(meridian_alpha.frontier_loop):
        raise AssertionError("meridian orientation is not hash-sensitive")

    components = []
    adjacency = {v: set() for v in torus_vertices}
    for edge in frontier.torus_simplices[1]:
        u, v = tuple(edge)
        adjacency[u].add(v)
        adjacency[v].add(u)
    unseen = set(torus_vertices)
    while unseen:
        seed = min(unseen, key=vkey)
        component = {seed}
        queue = [seed]
        while queue:
            vertex = queue.pop()
            for neighbour in adjacency[vertex]:
                if neighbour not in component:
                    component.add(neighbour)
                    queue.append(neighbour)
        unseen -= component
        triangles = [t for t in frontier.torus_simplices[2] if t <= component]
        components.append({
            "vertices": len(component),
            "edges": sum(edge <= component for edge in frontier.torus_simplices[1]),
            "triangles": len(triangles),
            "euler_characteristic": len(component)
                - sum(edge <= component for edge in frontier.torus_simplices[1])
                + len(triangles),
            "vertex_set_sha256": digest(sorted(component, key=vkey)),
        })
    components.sort(key=lambda item: item["vertex_set_sha256"])
    if len(components) != 2 or any(c["euler_characteristic"] != 0 for c in components):
        raise AssertionError("marked set is not two closed tori")

    loops = [meridian_alpha, longitude_alpha, meridian_beta, longitude_beta]
    loop_records = {loop.name: loop.record() for loop in loops}
    loop_records["geom_N_independent"] = paper_N_record
    return {
        "format": "luttinger-independent-peripheral-v2",
        "independence_boundary": {
            "geometric_input": "bundle.build_bundle marked triangulation only",
            "forbidden_modules_imported": [],
            "not_imported": ["complement", "pi1", "paper_bridge",
                             "peripheral_bridge", "r_run", "sweep"],
            "comparison_basis": "literal derived-frontier and complement paths",
        },
        "bundle": {
            "K_f_vector": [len(K.simplices[d]) for d in range(5)],
            "K_vertex_set_sha256": digest(sorted(K.vertices(), key=vkey)),
            "torus_components": components,
            "complement_vertices": len(frontier.complement_vertices),
            "complement_edges": len(frontier.complement_edges),
            "frontier_vertices": len(frontier.frontier_vertices),
        },
        "marked_crossings": {
            "c_y": canonical(cy),
            "s_e": canonical(se),
            "y_1_sha256": digest(y1),
            "s_2_sha256": digest(s2),
        },
        "named_bundle_loops": {
            name: {"edges": len(path) - 1, "sha256": digest(path)}
            for name, path in sorted(marked.items())
        },
        "peripheral_loops": loop_records,
        "pair_checks": {
            "alpha_common_whisker": "PASS: literal y_1 prefix",
            "beta_local_common_whisker": "PASS: local N_grid and longitude use literal s_2 prefix",
            "beta_paper_meridian_transport": "PASS: geom_N = A*N_grid^-1*A^-1 from punctured alpha-s grid",
            "alpha_section": "PASS: A lift plus negative c half",
            "beta_section": "PASS: B lift with zero e drift",
            "meridian_orientation": "PASS: ambient/torus induced orientation",
            "framing": "product/fibered framing; smooth Lagrangian comparison remains Lemma 8.2",
        },
        "sensitivity_controls": {
            "opposite_alpha_half_sha256": digest(positive_alpha),
            "selected_alpha_half_sha256": digest(alpha_section),
            "opposite_y_2_sha256": digest(y2),
            "selected_y_1_sha256": digest(y1),
            "reversed_alpha_meridian_sha256": digest(
                inverse_path(meridian_alpha.frontier_loop)),
            "result": "PASS: opposite half, opposite whisker, and meridian inverse are distinct",
        },
    }


def main():
    # Lazy import keeps extract(B) usable by the alternative bundle builder
    # without importing the original bundle construction at all.
    from bundle import build_bundle

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=Path("independent_peripheral_certificate.json"))
    parser.add_argument("--check", action="store_true",
                        help="compare regenerated result with --output")
    args = parser.parse_args()
    print("building marked bundle triangulation...", flush=True)
    B = build_bundle(dir_b=1, dir_a=-1)
    print("extracting derived-frontier peripheral pairs independently...", flush=True)
    result = extract(B)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not args.output.exists():
            raise SystemExit(f"missing certificate: {args.output}")
        if args.output.read_text(encoding="ascii") != encoded:
            raise SystemExit("independent peripheral certificate mismatch")
        print(f"PASS: {args.output} exactly reproduced")
    else:
        args.output.write_text(encoded, encoding="ascii")
        print(f"wrote {args.output}")
    for name, record in result["peripheral_loops"].items():
        if "frontier_edges" in record:
            print(f"  {name}: frontier={record['frontier_edges']} "
                  f"whisker={record['whisker_edges']} "
                  f"complement={record['complement_edges']} "
                  f"sha256={record['complement_loop_sha256'][:16]}...")
        else:
            print(f"  {name}: transported complement={record['complement_edges']} "
                  f"local-grid={record['grid_detour_edges']} "
                  f"sha256={record['complement_loop_sha256'][:16]}...")
    print("PASS: independently extracted paper peripheral data, including transported N")


if __name__ == "__main__":
    main()
