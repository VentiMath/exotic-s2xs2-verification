"""Explicit based-loop bridge from the paper's octagon to ``fiber.py``.

The five-chain model determines the marked genus-2 surface, but a free
homotopy class is not enough for the relations in Table 1: the whisker from
the fixed point ``p`` matters.  This module chooses edge-circle parallels on
the band rails and gives them literal one-edge whiskers from ``p``.

The choices are equivariant under ``phi0`` and are certified by three finite
checks:

* ``phi0(x) == r`` and ``phi0(y) == s`` as vertex paths;
* ``[x,y][r,s]`` is the sole surface relator, up to cyclic orientation, after
  elementary Tietze elimination;
* ``x,y,r`` are a free basis of the triangulated complement of the curve
  ``e``.  The last assertion is accompanied by explicit short words writing
  every generator of the reduced free group in terms of ``x,y,r``.

This supplies the first half of the geometric bridge.  It does not yet assert
that the resulting whiskers are the particular normal-position whiskers used
for all three punctured transport annuli in Table 1.
"""

from collections import deque

from complex import Complex
from fast_tietze import renumber, simplify, verify_certificate
from fiber import K_BAND, build_fiber
from layers import build_stack
from pi1 import Presentation, free_reduce, inverse


def _rail(F, name, row):
    V = F['V']
    return [V(name, row, i) for i in range(F['K_BAND'][name])]


def _rotate(cycle, start):
    i = cycle.index(start)
    return cycle[i:] + cycle[:i]


def _based_rail(cycle, start, direction):
    """Rail circle with the literal whisker p--start on both ends."""
    body = _rotate(cycle, start)
    if direction < 0:
        body = [body[0]] + list(reversed(body[1:]))
    return ['p'] + body + [body[0], 'p']


def _commutator(a, b):
    return free_reduce(a + b + inverse(a) + inverse(b))


def _cyclic_or_inverse(word):
    out = []
    for w in (word, inverse(word)):
        out.extend(w[i:] + w[:i] for i in range(len(w)))
    return out


def _dehn_reduce(word, relator):
    """Dehn reduction for a length-8 genus-2 surface relator."""
    assert len(relator) == 8
    table = {}
    for cyclic in _cyclic_or_inverse(relator):
        for length in range(5, 9):
            table[tuple(cyclic[:length])] = inverse(cyclic[length:])
    word = free_reduce(word)
    while True:
        changed = False
        for length in (8, 7, 6, 5):
            for i in range(len(word) - length + 1):
                subword = tuple(word[i:i + length])
                if subword in table:
                    word = free_reduce(
                        word[:i] + table[subword] + word[i + length:])
                    changed = True
                    break
            if changed:
                break
        if not changed:
            return word


def _substitute(letter_word, images):
    out = []
    for letter in letter_word:
        image = images[abs(letter) - 1]
        out += image if letter > 0 else inverse(image)
    return free_reduce(out)


def _inverse_basis_certificate(images, rank, max_length=6):
    """Find words in ``images`` equal to each standard free generator."""
    alphabet = tuple(range(1, len(images) + 1)) + \
               tuple(range(-1, -len(images) - 1, -1))
    found = {}
    queue = deque([()])
    while queue and len(found) < rank:
        word = queue.popleft()
        value = _substitute(word, images)
        for g in range(1, rank + 1):
            if value == [g] and g not in found:
                found[g] = list(word)
        if len(word) == max_length:
            continue
        for letter in alphabet:
            if word and word[-1] == -letter:
                continue
            queue.append(word + (letter,))
    assert len(found) == rank, \
        f"named loops do not generate the reduced free group by length {max_length}"
    for g, word in found.items():
        assert _substitute(word, images) == [g]
    return found


def build_paper_loops(F=None):
    """Return explicit vertex paths for the paper names ``x,y,r,s``.

    The a/e pair uses the + rail and the b/d pair the - rail.  Starting
    vertices are paired by ``phi0``; each is adjacent to ``p``.  Reversing the
    a/e rail orientations is forced by the octagon surface-relator convention.
    """
    F = F or build_fiber()
    L, phi0, V = F['L'], F['phi0'], F['V']
    starts = {
        'x': V('a', 1, 1),
        'y': V('b', -1, 1),
    }
    starts['r'] = phi0[starts['x']]
    starts['s'] = phi0[starts['y']]
    rails = {
        'x': _rail(F, 'a', 1),
        'y': _rail(F, 'b', -1),
        'r': _rail(F, 'e', 1),
        's': _rail(F, 'd', -1),
    }
    directions = {'x': -1, 'y': 1, 'r': -1, 's': 1}
    loops = {name: _based_rail(rails[name], starts[name], directions[name])
             for name in 'xyrs'}

    for name, path in loops.items():
        assert path[0] == path[-1] == 'p'
        assert all(u == v or frozenset((u, v)) in L.simplices[1]
                   for u, v in zip(path, path[1:])), \
            f"{name} is not an edge loop"
    assert [phi0[v] for v in loops['x']] == loops['r']
    assert [phi0[v] for v in loops['y']] == loops['s']
    return loops


def certify_paper_loops(F=None, verbose=True):
    """Run and return the finite certificates for the based fiber loops."""
    F = F or build_fiber()
    L, curves = F['L'], F['curves']
    loops = build_paper_loops(F)

    # Closed fiber: the named surface word is exactly the unique relator after
    # elementary eliminations, modulo the harmless cyclic/orientation choice.
    P = Presentation(L, 'p')
    named = [P.loop_word(loops[name]) for name in 'xyrs']
    surface = _commutator(named[0], named[1]) + \
              _commutator(named[2], named[3])
    live, rels, words = simplify(
        P.ngens, P.relators, [surface] + named, verbose=False)
    n, rels, words = renumber(live, rels, words)
    assert n == 4 and len(rels) == 1
    surface_word = words[0]
    assert not _dehn_reduce(surface_word, rels[0]), \
        "named surface word is nontrivial in the triangulated surface group"

    # Drilling e: the rails x,y,r avoid the core e and form a free basis.
    e_vertices = set(curves['e'])
    drilled = L.induced(set(L.vertices()) - e_vertices)
    for name in 'xyr':
        assert not (set(loops[name]) & e_vertices), \
            f"paper loop {name} meets the drilled e core"
    Pe = Presentation(drilled, 'p')
    e_named = [Pe.loop_word(loops[name]) for name in 'xyr']
    live_e, rels_e, words_e = simplify(
        Pe.ngens, Pe.relators, e_named, verbose=False)
    rank_e, rels_e, words_e = renumber(live_e, rels_e, words_e)
    assert rank_e == 3 and not rels_e, \
        "the induced complement of e did not reduce to a free rank-3 group"
    inverse_basis = _inverse_basis_certificate(words_e, rank_e)

    certificate = {
        'surface_rank': n,
        'surface_relator': rels[0],
        'named_surface_word': surface_word,
        'e_complement_rank': rank_e,
        'e_basis_images': dict(zip('xyr', words_e)),
        'e_inverse_basis': inverse_basis,
        'starts': {name: loops[name][1] for name in 'xyrs'},
    }
    if verbose:
        print("paper bridge: phi0(x,y)=(r,s) as literal based paths: PASS")
        print("paper bridge: [x,y][r,s] is the surface relator: PASS")
        print("paper bridge: pi1(F-nu(e))=<x,y,r> freely: PASS")
        print("  reduced images:", certificate['e_basis_images'])
        print("  inverse basis certificate:", inverse_basis)
    return loops, certificate


def _concat_paths(*paths):
    out = list(paths[0])
    for path in paths[1:]:
        assert out[-1] == path[0]
        out += path[1:]
    return out


def _tree_generator_loop(P, edge):
    """Return the geometric based loop belonging to a non-tree edge."""
    def root_path(vertex):
        path = [vertex]
        while P.parent[path[-1]] is not None:
            path.append(P.parent[path[-1]])
        return list(reversed(path))

    lo, hi = P.K.sorted_tuple(edge)
    return root_path(lo) + [hi] + list(reversed(root_path(hi)))[1:]


def _deterministic_geometric_generators(K, base):
    """Spanning-tree edge loops independent of Python set iteration order."""
    adjacency = {vertex: [] for vertex in K.vertices()}
    for edge in K.simplices[1]:
        u, v = K.sorted_tuple(edge)
        adjacency[u].append(v)
        adjacency[v].append(u)
    for neighbours in adjacency.values():
        neighbours.sort(key=str)
    parent = {base: None}
    queue = deque([base])
    while queue:
        vertex = queue.popleft()
        for other in adjacency[vertex]:
            if other not in parent:
                parent[other] = vertex
                queue.append(other)
    tree = {frozenset((vertex, par)) for vertex, par in parent.items()
            if par is not None}

    def root_path(vertex):
        path = [vertex]
        while parent[path[-1]] is not None:
            path.append(parent[path[-1]])
        return list(reversed(path))

    edges = sorted((edge for edge in K.simplices[1] if edge not in tree),
                   key=lambda edge: tuple(map(str, K.sorted_tuple(edge))))
    loops = []
    for edge in edges:
        lo, hi = K.sorted_tuple(edge)
        loops.append(root_path(lo) + [hi] +
                     list(reversed(root_path(hi)))[1:])
    return loops


def certify_kappa3(F=None, verbose=True, search_length=10):
    """Construct and certify the clean drilled-c loop of Lemma 10.1.

    Rather than importing the paper's dotted polygonal arc, find a literal
    edge loop in the triangulated complement of c whose closed-surface class
    is s^-1 r^-1 y x.  Then prove x,r,kappa3 freely generate that complement
    and transport the complete based loop through the open beta stack.
    """
    F = F or build_fiber()
    L, curves, V, rank = F['L'], F['curves'], F['V'], F['L'].rank.get
    loops = build_paper_loops(F)
    c_vertices = set(curves['c'])
    drilled = L.induced(set(L.vertices()) - c_vertices)
    assert all(not (set(loops[name]) & c_vertices) for name in ('x', 'r'))
    Pc = Presentation(drilled, 'p')

    edge_loops = _deterministic_geometric_generators(drilled, 'p')
    tracked = [Pc.loop_word(loops['x']), Pc.loop_word(loops['r'])] + \
              [Pc.loop_word(path) for path in edge_loops]
    live, rels, images = simplify(Pc.ngens, Pc.relators, tracked, verbose=False)
    rank_c, rels, images = renumber(live, rels, images)
    assert rank_c == 3 and not rels
    xr_images, edge_images = images[:2], images[2:]

    third = None
    for path, image in zip(edge_loops, edge_images):
        try:
            inverse_basis = _inverse_basis_certificate(
                xr_images + [image], rank_c, max_length=7)
        except AssertionError:
            continue
        third = path, image, inverse_basis
        break
    assert third is not None, "could not find a geometric third basis loop"
    third_path, _, _ = third

    # Express the desired closed-surface class in this geometric free basis.
    P = Presentation(L, 'p')
    named_words = [P.loop_word(loops[name]) for name in 'xyrs']
    basis_paths = [loops['x'], loops['r'], third_path]
    basis_words = [P.loop_word(path) for path in basis_paths]
    live, rels, words = simplify(
        P.ngens, P.relators, named_words + basis_words, verbose=False)
    n, rels, words = renumber(live, rels, words)
    assert n == 4 and len(rels) == 1
    relator = rels[0]
    named_images, basis_images = words[:4], words[4:]
    target = _substitute([-4, -3, 2, 1], named_images)

    alphabet = (1, 2, 3, -1, -2, -3)
    queue = deque([()])
    basis_word = None
    while queue:
        word = queue.popleft()
        value = _substitute(word, basis_images)
        if not _dehn_reduce(value + inverse(target), relator):
            basis_word = list(word)
            break
        if len(word) == search_length:
            continue
        for letter in alphabet:
            if word and word[-1] == -letter:
                continue
            queue.append(word + (letter,))
    assert basis_word is not None, \
        f"no drilled-c representative found through basis length {search_length}"

    factors = []
    for letter in basis_word:
        path = basis_paths[abs(letter) - 1]
        factors.append(path if letter > 0 else list(reversed(path)))
    kappa_path = _concat_paths(*factors)
    assert not (set(kappa_path) & c_vertices)

    # The found loop, together with x and r, is itself a free basis of F-c.
    kappa_word_c = Pc.loop_word(kappa_path)
    live, rels, basis_c = simplify(
        Pc.ngens, Pc.relators,
        [Pc.loop_word(loops['x']), Pc.loop_word(loops['r']), kappa_word_c],
        verbose=False)
    rank_c2, rels, basis_c = renumber(live, rels, basis_c)
    assert rank_c2 == 3 and not rels
    inverse_basis = _inverse_basis_certificate(basis_c, rank_c2, max_length=8)

    # Transport the literal based path and compare with r^-1 s^-1 x.
    twists = []
    for name, direction in (('b', 1), ('a', -1)):
        k = K_BAND[name]
        twists.append((
            [V(name, 0, i) for i in range(k)],
            [V(name, 1, i) for i in range(k)],
            [V(name, -1, i) for i in range(k)], direction))
    cells, levels, _ = build_stack(L, rank, twists, copy_tag='K3')
    stack = Complex(cells, order=sorted(
        {vertex for cell in cells for vertex in cell}, key=str))
    Pstack = Presentation(stack, ('K3', 0, 'p'))

    def at(level, path):
        return [('K3', level, vertex) for vertex in path]

    vertical = [('K3', level, 'p') for level in range(levels + 1)]
    top_target = _concat_paths(
        list(reversed(at(levels, loops['r']))),
        list(reversed(at(levels, loops['s']))),
        at(levels, loops['x']))
    residual_path = _concat_paths(
        at(0, kappa_path), vertical, list(reversed(top_target)),
        list(reversed(vertical)))
    residual = Pstack.loop_word(residual_path)
    live, rels, residuals, proof = simplify(
        Pstack.ngens, Pstack.relators, [residual],
        verbose=False, certify=True)
    assert verify_certificate(Pstack.ngens, Pstack.relators, [residual], proof) == \
           (live, rels, residuals)
    n, rels, residuals = renumber(live, rels, residuals)
    assert n == 4 and rels
    assert not _dehn_reduce(residuals[0], rels[0]), \
        "drilled-fiber beta transport does not equal r^-1 s^-1 x"

    certificate = {
        'kappa_basis_word': basis_word,
        'kappa_path_length': len(kappa_path) - 1,
        'c_complement_rank': rank_c2,
        'c_basis_images': basis_c,
        'c_inverse_basis': inverse_basis,
        'transport_tietze_steps': len(proof['steps']),
        'transport_residual_after_dehn': [],
    }
    if verbose:
        print("paper bridge: kappa3 avoids c and equals s^-1 r^-1 y x: PASS")
        print("paper bridge: pi1(F-nu(c))=<x,r,kappa3> freely: PASS")
        print("paper bridge: B kappa3 B^-1 = r^-1 s^-1 x: PASS")
        print("  geometric basis word:", basis_word,
              "path length:", certificate['kappa_path_length'])
        print("  Tietze replay steps:", certificate['transport_tietze_steps'])
    return kappa_path, certificate


def certify_beta_based_monodromy(F=None, verbose=True):
    """Transport the complete p-whiskered paths through the beta stack.

    This tests the precise based-loop issue: the bottom loop and the asserted
    top word are joined using the literal vertical track of ``p`` in the open
    mapping cylinder.  No conclusion is inferred from homology or from the
    corresponding unbased curves.
    """
    F = F or build_fiber()
    L, V, rank = F['L'], F['V'], F['L'].rank.get
    loops = build_paper_loops(F)
    twists = []
    for name, direction in (('b', 1), ('a', -1)):
        k = K_BAND[name]
        twists.append((
            [V(name, 0, i) for i in range(k)],
            [V(name, 1, i) for i in range(k)],
            [V(name, -1, i) for i in range(k)],
            direction,
        ))
    cells, levels, _ = build_stack(L, rank, twists, copy_tag='PB')
    stack = Complex(cells, order=sorted(
        {v for cell in cells for v in cell}, key=str))
    P = Presentation(stack, ('PB', 0, 'p'))

    def at(level, path):
        return [('PB', level, vertex) for vertex in path]

    def product(level, factors):
        paths = []
        for name, sign in factors:
            path = at(level, loops[name])
            paths.append(path if sign > 0 else list(reversed(path)))
        return _concat_paths(*paths)

    vertical = [('PB', level, 'p') for level in range(levels + 1)]
    targets = {
        'x': [('y', -1)],
        'y': [('y', 1), ('x', 1)],
        'r': [('r', 1)],
        's': [('s', 1)],
    }
    residuals = []
    for name in 'xyrs':
        bottom = at(0, loops[name])
        top_target = product(levels, targets[name])
        residual_path = _concat_paths(
            bottom, vertical, list(reversed(top_target)),
            list(reversed(vertical)))
        residuals.append(P.loop_word(residual_path))

    live, rels, words, proof = simplify(
        P.ngens, P.relators, residuals, verbose=False, certify=True)
    assert verify_certificate(P.ngens, P.relators, residuals, proof) == \
           (live, rels, words)
    n, rels, words = renumber(live, rels, words)
    assert n == 4 and rels
    relator = rels[0]
    assert all(rel in _cyclic_or_inverse(relator) for rel in rels), \
        "open beta stack did not reduce to one surface relator"
    reduced = {name: _dehn_reduce(word, relator)
               for name, word in zip('xyrs', words)}
    assert not any(reduced.values()), \
        f"based beta monodromy mismatch: {reduced}"

    certificate = {
        'stack_f_vector': stack.f_vector(),
        'input_generators': P.ngens,
        'input_relators': len(P.relators),
        'tietze_steps': len(proof['steps']),
        'reduced_rank': n,
        'reduced_surface_relator': relator,
        'residuals_after_dehn': reduced,
    }
    if verbose:
        print("paper bridge: full based beta monodromy paths: PASS")
        print("  x->y^-1, y->yx, r->r, s->s")
        print("  Tietze replay steps:", certificate['tietze_steps'])
    return certificate


if __name__ == '__main__':
    certify_paper_loops()
    certify_beta_based_monodromy()
    certify_kappa3()
