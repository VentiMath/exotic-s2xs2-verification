"""
The target run: complement of T_alpha u T_beta in the triangulated bundle R,
based meridians and product-framing push-off words from the combinatorics,
then the GAP certificate:

  1. pi_1(K) = pi_1(C)/<<mu_a, mu_b>> fingerprint vs Prop 3.5;
  2. relation-sheet diff: pi_1(C) fingerprint vs the author's drilled system
     (base + three corrected transports, no surgery relators) over its small
     sign/placement variants;
  3. the theorem: pi_1(C)/<<mu_a . dir_base(T_a)^eA, mu_b . dir_base(T_b)^eB>>
     trivial for all sign pairs and both c-drift halves.

Run: python3 r_run.py     (writes r_cert.g, runs gap; ~minutes + gap time)
"""
import json
import shutil
import subprocess
import time
from complement import TorusComplement
from bundle import build_bundle, check_bundle
from fast_tietze import (simplify, renumber, save_certificate,
                         verify_certificate)
from fiber import K_BAND
from pi1 import Presentation, free_reduce, inverse
from paper_bridge import build_paper_loops
from sweep import (certify_grid_sweep, grid_intersection_sign,
                   punctured_grid_boundary_cycles)


def beta_basing_sweep(B, T, X, u0b, ambient_signs, torus_signs):
    """Derive the section 8.5 meridian correction from the triangulation.

    The relevant basing arc follows d to its intersection with e.  Along that
    arc it crosses c once.  Sweeping it around beta gives a rectangular grid
    with one interior T_alpha incidence and terminal boundary on T_beta.
    Puncturing at the interior incidence contributes a conjugate of the
    T_alpha meridian, based along the outside edge of this grid.

    Return the oriented meridian diagnostic, the transported reference word,
    and the terminal boundary word traced from the punctured grid.
    """
    K, F, V, m = B['K'], B['F'], B['V'], B['m']
    d = F['curves']['d']
    cset, eset = set(F['curves']['c']), set(F['curves']['e'])
    cd = [i for i, v in enumerate(d) if v in cset]
    de = [i for i, v in enumerate(d) if v in eset]
    assert len(cd) == len(de) == 1
    cd, de = cd[0], de[0]

    # Choose the oriented d-arc on which c occurs before the terminal e
    # crossing.  Include two vertices before c: one makes the T_alpha hit
    # interior and the second leaves a full simplicial collar between its
    # deleted open star and the initial boundary of the sweep.
    def cyclic_indices(start, stop, n, step=1):
        out, i = [], start % n
        while True:
            out.append(i)
            if i == stop % n:
                return out
            i = (i + step) % n
            assert len(out) <= n

    # The side chosen by side_b is e_rail[0].  At the d/e plumbing this is
    # one of the two neighbours of the e-crossing on d, and it must be the
    # penultimate row of the sweep.  This determines which of the two d-arcs
    # to use without consulting any group computation.
    e_normal = B['e_rail'][0]
    normal_idx = d.index(e_normal)
    if normal_idx == (de - 1) % len(d):
        step = 1
    elif normal_idx == (de + 1) % len(d):
        step = -1
    else:
        raise AssertionError("chosen e-normal is not adjacent to d/e crossing")
    arc_idx = cyclic_indices(cd - 2 * step, de, len(d), step)
    arc = [d[i] for i in arc_idx]
    assert arc[-1] in eset and arc[2] in cset
    assert arc[-2] == e_normal

    J = lambda k: ('J', k)

    def beta_loop(v):
        return [(('A', 1, v), J(2))] + \
               [(('S', level, v), ('t', 1)) for level in range(1, m)] + \
               [(('A', 1, v), J(0)),
                (('A', 1, v), J(1)),
                (('A', 1, v), J(2))]

    rows = [beta_loop(v) for v in arc]
    hits = certify_grid_sweep(
        K, rows, {'alpha': B['Ta_verts'], 'beta': B['Tb_verts']})
    alpha_interior = [h for h in hits['alpha']
                      if 0 < h[0] < len(rows) - 1]
    assert len(alpha_interior) == 1, \
        f"beta basing sweep has {len(alpha_interior)} interior alpha hits"
    assert all(i == len(rows) - 1 for i, _, _ in hits['beta']), \
        "beta basing sweep meets T_beta away from its terminal boundary"
    _, _, crossing = alpha_interior[0]
    crossing_sign = grid_intersection_sign(
        K, rows, alpha_interior[0], T, ambient_signs, torus_signs)
    boundary_cycles = punctured_grid_boundary_cycles(K, rows, X.Tverts)
    assert len(boundary_cycles) == 3, \
        f"punctured beta sweep has {len(boundary_cycles)} boundary components"

    # The outside boundary of a regular neighbourhood of the d-arc starts
    # at the chosen e-normal corner and runs from the successor of e around
    # to the c-crossing, at the outer radial level J(2).  This is an explicit
    # edge path in C and hence fixes the conjugate, rather than merely adding
    # an arbitrary meridian conjugate.
    outside_idx = cyclic_indices(normal_idx, cd, len(d), -step)
    outside = [(('A', 1, d[i]), J(2)) for i in outside_idx]
    assert outside[0] == X.r(u0b), \
        "chosen e-normal does not start the sweep's outside basing path"
    assert crossing == (('A', 1, d[cd]), J(1))
    approach = (('A', 1, d[cd]), J(2))
    assert outside[-1] == approach

    # Pick, deterministically, a Ta triangle at the crossing whose dual
    # meridian retracts to the approach vertex, and rotate it to that point.
    candidates = []
    for sigma in sorted((s for s in T.simplices[2] if crossing in s),
                        key=lambda s: tuple(sorted(map(repr, s)))):
        loop = X.oriented_meridian_loop(sigma, ambient_signs, torus_signs)
        if approach in X.to_C(loop[:-1]):
            candidates.append((sigma, loop))
    assert candidates, "no dual meridian is approachable from the sweep"
    _, meridian = candidates[0]
    meridian = X.rotate_loop_to_retraction(meridian, approach)
    correction = X.based_word_via_C(meridian, outside)
    if crossing_sign < 0:
        correction = inverse(correction)
    print("  beta basing sweep: grid %dx%d, alpha hits=%d, beta boundary hits=%d; "
          "oriented intersection sign=%+d" %
          (len(rows), len(rows[0]), len(alpha_interior), len(hits['beta']),
           crossing_sign))
    reference_idx = cyclic_indices(normal_idx, arc_idx[0], len(d), -step)
    reference_path = [(('A', 1, d[i]), J(2)) for i in reference_idx]
    assert reference_path[-1] == rows[0][0]
    reference_loop = rows[0]
    reference_full = (reference_path + reference_loop[1:] +
                      reference_path[::-1][1:])
    reference = X.P.loop_word(reference_full)
    local_base = X.r(u0b)
    terminal_candidates = [cycle for cycle in boundary_cycles
                           if local_base in cycle[:-1]]
    assert len(terminal_candidates) == 1, \
        "cannot identify terminal sweep boundary at beta local base"
    terminal = terminal_candidates[0][:-1]
    k = terminal.index(local_base)
    terminal = terminal[k:] + terminal[:k] + [local_base]
    terminal_word = X.P.loop_word(terminal)
    print("  punctured sweep boundary lengths:",
          sorted(len(cycle) - 1 for cycle in boundary_cycles))
    return correction, reference, terminal_word


def alpha_s_transport_sweep(B, T, X, ambient_signs, torus_signs):
    """Certify the complete M1 transport membrane as a simplicial grid."""
    J = ('J', 2)
    phi = B['phi0']
    paper_loops = build_paper_loops(B['F'])
    s_path = paper_loops['s']
    rows = [[(('A', 0, vertex), J),
             (('A', 1, vertex), J),
             (('A', 2, vertex), J),
             (('A', 0, phi[vertex]), J)]
            for vertex in s_path]
    hits = certify_grid_sweep(
        B['K'], rows, {'alpha': B['Ta_verts'], 'beta': B['Tb_verts']},
        require_closed=False)
    assert not hits['alpha']
    assert len(hits['beta']) == 1
    hit = hits['beta'][0]
    sign = grid_intersection_sign(
        B['K'], rows, hit, T, ambient_signs, torus_signs)
    cycles = punctured_grid_boundary_cycles(
        B['K'], rows, set(B['Ta_verts']) | set(B['Tb_verts']))
    assert sorted(len(cycle) - 1 for cycle in cycles) == [8, 12]

    q = (('A', 0, 'p'), J)

    def based_cycle(cycle, fiber_start):
        start = (('A', 0, fiber_start), J)
        body = cycle[:-1]
        assert start in body
        i = body.index(start)
        rotated = body[i:] + body[:i] + [start]
        whisker = [q, start]
        full = whisker + rotated[1:] + list(reversed(whisker))[1:]
        return X.P.loop_word(full)

    y_start, s_start = paper_loops['y'][1], paper_loops['s'][1]
    y_cycle = next(cycle for cycle in cycles
                   if (('A', 0, y_start), J) in cycle)
    corrected_cycle = next(cycle for cycle in cycles if cycle is not y_cycle)

    # Isolate the local detour replacing the single s-edge through the
    # deleted T_beta vertex.  Closing it by that original edge gives the
    # puncture meridian, based at the endpoint of the paper's s_2 whisker.
    e_vertices = set(B['F']['curves']['e'])
    crossing_i = next(i for i, vertex in enumerate(s_path)
                      if vertex in e_vertices)
    assert 1 < crossing_i < len(s_path) - 1
    predecessor = (('A', 0, s_path[crossing_i - 1]), J)
    approach = (('A', 0, s_path[crossing_i]), J)
    corrected_body = corrected_cycle[:-1]
    i = corrected_body.index(predecessor)
    j = corrected_body.index(approach)
    assert i < j
    detour = corrected_body[i:j + 1]
    assert frozenset((approach, predecessor)) in X.C.simplices[1]
    # Rotate (detour followed by the closing edge) to the paper approach.
    grid_meridian = [approach, predecessor] + detour[1:] + [approach]
    assert grid_meridian[0] == grid_meridian[-1] == approach

    # Compare inside the complement of the closed star of the crossing.  This
    # local group is Z; equality here is stronger than a global word test and
    # fixes the meridian orientation rather than merely its conjugacy class.
    crossing = hits['beta'][0][2]
    duals = []
    for sigma in sorted((simplex for simplex in T.simplices[2]
                         if crossing in simplex),
                        key=lambda simplex: tuple(sorted(map(repr, simplex)))):
        dual = X.to_C(X.oriented_meridian_loop(
            sigma, ambient_signs, torus_signs))
        if approach in dual[:-1]:
            k = dual[:-1].index(approach)
            dual = dual[k:-1] + dual[:k] + [approach]
            duals.append(dual)
    assert duals
    star_vertices = {vertex for top in B['K'].simplices[4]
                     if crossing in top for vertex in top} - X.Tverts
    star_vertices |= set(grid_meridian)
    for dual in duals:
        star_vertices |= set(dual)
    local = X.C.induced(star_vertices)
    local_presentation = Presentation(local, approach)
    grid_word = local_presentation.loop_word(grid_meridian)
    residuals = []
    for dual in duals:
        dual_word = local_presentation.loop_word(dual)
        residuals += [inverse(grid_word) + dual_word,
                      inverse(grid_word) + inverse(dual_word)]
    live, relators, residuals_out, proof = simplify(
        local_presentation.ngens, local_presentation.relators, residuals,
        verbose=False, certify=True)
    assert verify_certificate(
        local_presentation.ngens, local_presentation.relators, residuals,
        proof) == (live, relators, residuals_out)
    local_rank, local_relators, residuals_out = renumber(
        live, relators, residuals_out)
    assert local_rank == 1 and not local_relators
    assert all(not residuals_out[k] for k in range(0, len(residuals_out), 2))
    assert all(residuals_out[k] in ([1, 1], [-1, -1])
               for k in range(1, len(residuals_out), 2))

    prefix = [(('A', 0, vertex), J)
              for vertex in s_path[:crossing_i + 1]]
    full_grid_meridian = (prefix + grid_meridian[1:] +
                          list(reversed(prefix))[1:])
    words = {
        'alpha_s_y_boundary': based_cycle(y_cycle, y_start),
        'alpha_s_corrected_boundary': based_cycle(corrected_cycle, s_start),
        'alpha_s_grid_N': X.P.loop_word(full_grid_meridian),
    }
    print("  alpha-s sweep: grid %dx%d, beta hits=1, oriented sign=%+d, "
          "boundary lengths=%s" %
          (len(rows), len(rows[0]), sign,
           sorted(len(cycle) - 1 for cycle in cycles)))
    print("  local N identification: closed-star complement rank 1; "
          "grid detour = oriented dual meridian, inverse residual g^+-2; "
          f"Tietze replay steps={len(proof['steps'])}")
    return sign, words


def geometric_paper_candidates(B, T, X, ambient_signs, torus_signs):
    """Concrete candidate paths for the paper's x,y,r,s,A,B generators.

    The fiber paths are explicit rail parallels with literal one-edge whiskers
    from the fixed point p, certified by ``paper_bridge.py``.  The base paths
    also use p, so all six are genuinely based at the same vertex.  The exact
    normal-position arcs from these paths to every Table 1 puncture remain to
    be certified separately.
    """
    m = B['m']
    J = lambda k: ('J', k)

    def checked_word(path):
        assert path[0] == path[-1]
        assert all(frozenset((v,)) in X.C.simplices[0] for v in path)
        for u, v in zip(path, path[1:]):
            assert u == v or frozenset((u, v)) in X.C.simplices[1]
        return X.P.loop_word(path)

    def shortest_path(start, goals, allowed):
        from collections import deque
        goals, allowed = set(goals), set(allowed)
        assert start in allowed
        previous = {start: None}
        queue = deque([start])
        end = None
        while queue:
            vertex = queue.popleft()
            if vertex in goals:
                end = vertex
                break
            neighbours = set()
            for edge in X.C.simplices[1]:
                if vertex in edge:
                    neighbours |= set(edge) - {vertex}
            for neighbour in sorted(neighbours & allowed, key=repr):
                if neighbour not in previous:
                    previous[neighbour] = vertex
                    queue.append(neighbour)
        assert end is not None
        path = [end]
        while previous[path[-1]] is not None:
            path.append(previous[path[-1]])
        return list(reversed(path))

    paper_loops = build_paper_loops(B['F'])
    # Same based y circle, with c_y approached from the opposite side.  This
    # is the meridian whisker for the adjacent half-drift diagram.
    paper_loops['y2route'] = list(reversed(paper_loops['y']))
    candidates = {}
    for name in 'xyrs':
        path = [(('A', 0, v), J(2)) for v in paper_loops[name]]
        candidates[f'geom_{name}'] = checked_word(path)
    # The paper defines A and B as inverses of the displayed positive base
    # loops.  The common point is (A0,p,J2), off both torus-carrying cuts.
    alpha_positive = [(('A', t, 'p'), J(2)) for t in (0, 1, 2, 0)]
    candidates['geom_A'] = checked_word(list(reversed(alpha_positive)))
    q = (('A', 0, 'p'), J(2))
    cut_base = (('A', 1, 'p'), J(2))
    to_cut = [q, cut_base]
    beta_local = [cut_base]
    beta_local += [(('S', level, 'p'), ('t', 1))
                   for level in range(1, m)]
    beta_local += [(('A', 1, 'p'), J(k)) for k in (0, 1, 2)]
    beta_positive = to_cut + beta_local[1:] + list(reversed(to_cut))[1:]
    candidates['geom_B'] = checked_word(list(reversed(beta_positive)))

    def explicitly_based_meridian(path_name, target_curve, crossing,
                                  prefix_slice):
        """Meridian based by the named initial fiber segment plus a local
        normal segment inside the closed star of ``crossing``."""
        target_set = set(B['F']['curves'][target_curve])
        fiber_path = paper_loops[path_name]
        crossing_indices = [i for i, vertex in enumerate(fiber_path)
                            if vertex in target_set]
        assert len(crossing_indices) == 1
        i = crossing_indices[0]
        prefix = [prefix_slice(vertex) for vertex in fiber_path[:i + 1]]
        approach = prefix[-1]
        meridians = [X.oriented_meridian_loop(
            sigma, ambient_signs, torus_signs)
            for sigma in sorted((simplex for simplex in T.simplices[2]
                                 if crossing in simplex),
                                key=lambda simplex:
                                tuple(sorted(map(repr, simplex))))]
        assert meridians, f"no meridian triangle at {crossing!r}"
        local_vertices = {vertex for simplex in B['K'].all_simplices()
                          if crossing in simplex for vertex in simplex}
        local_vertices &= set(X.C.vertices())
        choices = []
        for meridian in meridians:
            targets = set(X.to_C(meridian[:-1]))
            try:
                normal_segment = shortest_path(
                    approach, targets, local_vertices | {approach})
            except AssertionError:
                continue
            target = normal_segment[-1]
            rotated = X.rotate_loop_to_retraction(meridian, target)
            choices.append((len(normal_segment), repr(target),
                            normal_segment, rotated))
        assert choices, f"no local normal segment reaches {crossing!r}"
        words = []
        for _, _, normal_segment, meridian in sorted(choices):
            whisker = prefix + normal_segment[1:]
            word = X.based_word_via_C(meridian, whisker)
            if word not in words:
                words.append(word)
        return words

    # M: y_1 to c_y in the alpha torus at radial level J1.
    cy = next(vertex for vertex in paper_loops['y']
              if vertex in set(B['F']['curves']['c']))
    m_candidates = explicitly_based_meridian(
        'y', 'c', (('A', 0, cy), J(1)),
        lambda vertex: (('A', 0, vertex), J(2)))
    candidates['geom_M'] = m_candidates[0]
    m_y2_candidates = explicitly_based_meridian(
        'y2route', 'c', (('A', 0, cy), J(1)),
        lambda vertex: (('A', 0, vertex), J(2)))
    candidates['geom_M_y2'] = m_y2_candidates[0]

    # N: s_2 to s_e, approached from the off-cut A0 side of T_beta.
    se = next(vertex for vertex in paper_loops['s']
              if vertex in set(B['F']['curves']['e']))
    n_candidates = explicitly_based_meridian(
        's', 'e', (('A', 1, se), J(2)),
        lambda vertex: (('A', 0, vertex), J(2)))
    candidates['geom_N'] = n_candidates[0]
    for i, word in enumerate(n_candidates):
        candidates[f'geom_N_candidate_{i}'] = word
    return candidates


def main():
    t0 = time.time()
    print("building bundle...")
    B = build_bundle(dir_b=1, dir_a=-1)
    K = B['K']
    print(f"  K f-vector {K.f_vector()} ({time.time()-t0:.0f}s)")
    T = check_bundle(B)
    t0 = time.time()
    ambient_signs = K.orientation_signs()
    torus_signs = T.orientation_signs()
    print(f"  oriented K and both torus components ({time.time()-t0:.0f}s)")

    t0 = time.time()
    X = TorusComplement(K, T)
    print(f"  complement C f-vector {X.C.f_vector()}, |Ndot| = {len(X.N)} "
          f"({time.time()-t0:.0f}s)")

    c, e = B['c'], B['e']
    crail, erail = B['c_rail'], B['e_rail']
    kc, ke = len(c), len(e)
    m = B['m']
    J = lambda k: ('J', k)

    # ---- T_alpha loops -------------------------------------------------
    va = lambda t, i: (('A', t, c[i % kc]), J(1))
    ra = lambda t, i: (('A', t, crail[i % kc]), J(1))
    u0a = frozenset({va(0, 0), ra(0, 0)})
    t0 = time.time()
    P = X.presentation(u0a)
    print(f"  pi1(C): {P.ngens} generators, {len(P.relators)} relators "
          f"({time.time()-t0:.0f}s)")

    sigma_a = next(s for s in T.simplices[2] if va(0, 0) in s)
    mu_loop_a = X.oriented_meridian_loop(
        sigma_a, ambient_signs, torus_signs)
    star_a = [s for s in X.N if va(0, 0) in s]
    to_mu_a = X.bfs_in_N(u0a, mu_loop_a[0], star_a)
    mu_a = X.based_word(mu_loop_a, to_mu_a)

    # fiber-direction push-off: c in copy A0, pushed in the base normal (J)
    gam_fib_a = [va(0, i) for i in range(kc)] + [va(0, 0)]
    lf_a_loop = X.pushoff_loop(gam_fib_a, lambda v: (v[0], J(2)))
    lf_a = X.based_word(lf_a_loop, X.bfs_in_N(u0a, lf_a_loop[0], star_a))

    # base-direction push-off: the alpha-lift with the half-rotation drift,
    # pushed in the fiber normal (the c-rail).  Both drift halves.
    half = kc // 2
    lift = [va(0, 0), va(1, 0), va(2, 0), va(0, half)]
    drift_down = [va(0, i) for i in range(half - 1, -1, -1)]
    drift_up = [va(0, i) for i in range(half + 1, kc)] + [va(0, 0)]
    side_a = lambda v: (('A', v[0][1], crail[c.index(v[0][2])]), J(1))
    lb_a1_loop = X.pushoff_loop(lift + drift_down, side_a)
    lb_a2_loop = X.pushoff_loop(lift + drift_up, side_a)
    lb_a1 = X.based_word(lb_a1_loop, [u0a])
    lb_a2 = X.based_word(lb_a2_loop, [u0a])

    # Paper-coordinate versions of the same two half-drift sections.  Section
    # 8.4 does not start at the arbitrary c[0] corner above: it starts at the
    # y-edge crossing c_y and bases the push-off along y_1.  Keep this lasso
    # explicit, since replacing it by the presentation tree is precisely the
    # based/unbased ambiguity under audit.
    paper_loops = build_paper_loops(B['F'])
    cset = set(B['F']['curves']['c'])
    y_hits = [i for i, vertex in enumerate(paper_loops['y'])
              if vertex in cset]
    assert len(y_hits) == 1
    y_hit = y_hits[0]
    cy = paper_loops['y'][y_hit]
    cy_i = c.index(cy)
    opposite_i = (cy_i + half) % kc
    # A is the inverse of the displayed positive alpha loop.  Since phi_0 is
    # an involution, lifting A from c_y first enters the last alpha layer at
    # phi_0(c_y), then runs backward to layer zero.
    paper_lift = [va(0, cy_i), va(2, opposite_i), va(1, opposite_i),
                  va(0, opposite_i)]

    def half_arc(step):
        indices = []
        i = opposite_i
        while i != cy_i:
            i = (i + step) % kc
            indices.append(i)
        assert len(indices) == half
        return [va(0, i) for i in indices]

    lb_a_y1_loop = X.pushoff_loop(paper_lift + half_arc(-1), side_a)
    lb_a_y2_loop = X.pushoff_loop(paper_lift + half_arc(+1), side_a)

    # The literal y_1 path ends at c_y in the unobstructed J2 slice.  Join it
    # to the retracted push-off corner by a shortest edge path in C; this last
    # small normal jog is part of the lasso, not an implicit tree choice.
    q_to_cy_y1 = [(('A', 0, vertex), J(2))
                  for vertex in paper_loops['y'][:y_hit + 1]]
    # The adjacent diagram approaches the same crossing from the other side
    # of y.  Its literal p-to-c_y route is the reversed suffix of the based y
    # loop, not the y_1 prefix reused with the other half-arc.
    y2_route = list(reversed(paper_loops['y'][y_hit:]))
    assert y2_route[0] == 'p' and y2_route[-1] == cy
    q_to_cy_y2 = [(('A', 0, vertex), J(2)) for vertex in y2_route]

    def shortest_C_path(start, goal):
        from collections import deque
        previous = {start: None}
        queue = deque([start])
        adjacency = {vertex: [] for vertex in X.C.vertices()}
        for edge in X.C.simplices[1]:
            u, v = tuple(edge)
            adjacency[u].append(v)
            adjacency[v].append(u)
        while queue and goal not in previous:
            vertex = queue.popleft()
            for neighbour in sorted(adjacency[vertex], key=repr):
                if neighbour not in previous:
                    previous[neighbour] = vertex
                    queue.append(neighbour)
        assert goal in previous
        path = [goal]
        while previous[path[-1]] is not None:
            path.append(previous[path[-1]])
        return list(reversed(path))

    def paper_based_alpha_word(loop, q_to_cy):
        target = X.r(loop[0])
        normal_jog = shortest_C_path(q_to_cy[-1], target)
        basing_path = q_to_cy + normal_jog[1:]
        return X.based_word_via_C(loop, basing_path), normal_jog

    lb_a_y1, lb_a_y1_jog = paper_based_alpha_word(
        lb_a_y1_loop, q_to_cy_y1)
    lb_a_y2, lb_a_y2_jog = paper_based_alpha_word(
        lb_a_y2_loop, q_to_cy_y2)
    print(f"  T_alpha words: |mu| {len(mu_a)}, |lf| {len(lf_a)}, "
          f"|lb1| {len(lb_a1)}, |lb2| {len(lb_a2)}, "
          f"|paper-y1| {len(lb_a_y1)}, |paper-y2| {len(lb_a_y2)}; "
          f"normal jogs {len(lb_a_y1_jog)-1}/{len(lb_a_y2_jog)-1} edges")

    # ---- T_beta loops --------------------------------------------------
    vb = lambda k, i: (('A', 1, e[i % ke]), J(k))
    sb = lambda lvl, i: (('S', lvl, e[i % ke]), ('t', 1))
    u0b = frozenset({vb(2, 0), (('A', 1, erail[0]), J(2))})

    sigma_b = next(s for s in T.simplices[2] if vb(2, 0) in s)
    mu_loop_b = X.oriented_meridian_loop(
        sigma_b, ambient_signs, torus_signs)
    star_b = [s for s in X.N if vb(2, 0) in s]
    to_mu_b = X.bfs_in_N(u0b, mu_loop_b[0], star_b)

    def bw(loop, path):
        full = path + loop[1:] + path[::-1][1:]
        return X.P.loop_word(X.to_C(full))

    mu_b = bw(mu_loop_b, to_mu_b)

    gam_fib_b = [vb(2, i) for i in range(ke)] + [vb(2, 0)]
    # at the corner the radial J-direction lies IN T_beta (the return
    # leg), so the base normal is the angular direction: the next fiber
    # copy at the same radius.
    lf_b_loop = X.pushoff_loop(gam_fib_b, lambda v: (('A', 2, v[0][2]), J(2)))
    lf_b = bw(lf_b_loop, X.bfs_in_N(u0b, lf_b_loop[0], star_b))

    # base-direction: through the stack at e0 (mid-thickness), radial return
    gam_base_b = [vb(2, 0)] + [sb(l, 0) for l in range(1, m)] + \
                 [vb(0, 0), vb(1, 0), vb(2, 0)]

    def side_b(v):
        if v[1] == ('t', 1):
            return (('S', v[0][1], erail[e.index(v[0][2])]), ('t', 1))
        return (('A', 1, erail[e.index(v[0][2])]), v[1])

    lb_b_loop = X.pushoff_loop(gam_base_b, side_b)
    lb_b = bw(lb_b_loop, [u0b])

    # Paper-coordinate beta section: start at the unique s_e crossing, use
    # the literal initial segment s_2 as whisker, and traverse B (the inverse
    # of the displayed positive beta loop).  psi fixes e pointwise, so the
    # reversed lifted section has no fiber drift.
    eset = set(B['F']['curves']['e'])
    s_hits = [i for i, vertex in enumerate(paper_loops['s'])
              if vertex in eset]
    assert len(s_hits) == 1
    s_hit = s_hits[0]
    se = paper_loops['s'][s_hit]
    se_i = e.index(se)
    gam_base_b_s2 = ([vb(2, se_i), vb(1, se_i), vb(0, se_i)] +
                     [sb(level, se_i)
                      for level in range(m - 1, 0, -1)] +
                     [vb(2, se_i)])
    lb_b_s2_loop = X.pushoff_loop(gam_base_b_s2, side_b)
    q_to_se = [(('A', 0, vertex), J(2))
               for vertex in paper_loops['s'][:s_hit + 1]]
    s2_jog = shortest_C_path(q_to_se[-1], X.r(lb_b_s2_loop[0]))
    lb_b_s2 = X.based_word_via_C(
        lb_b_s2_loop, q_to_se + s2_jog[1:])
    corr_b, bref_b, lb_b_sweep = beta_basing_sweep(
        B, T, X, u0b, ambient_signs, torus_signs)
    alpha_s_sign, alpha_s_words = alpha_s_transport_sweep(
        B, T, X, ambient_signs, torus_signs)
    print(f"  T_beta words: |mu| {len(mu_b)}, |lf| {len(lf_b)}, "
          f"|lb| {len(lb_b)}, |paper-s2| {len(lb_b_s2)}; "
          f"normal jog {len(s2_jog)-1} edges")

    # ---- Tietze --------------------------------------------------------
    t0 = time.time()
    sweep_residual = inverse(corr_b + bref_b) + lb_b_sweep
    longitude_residual = inverse(lb_b) + lb_b_sweep
    tracked = {
        "mu_a": mu_a, "lf_a": lf_a, "lb_a1": lb_a1, "lb_a2": lb_a2,
        "lb_a_y1": lb_a_y1, "lb_a_y2": lb_a_y2,
        "mu_b": mu_b, "lf_b": lf_b, "lb_b": lb_b, "corr_b": corr_b,
        "lb_b_s2": lb_b_s2,
        "beta_reference": bref_b, "lb_b_sweep": lb_b_sweep,
        "sweep_residual": sweep_residual,
        "longitude_residual": longitude_residual,
    }
    tracked.update(alpha_s_words)
    geometric = geometric_paper_candidates(
        B, T, X, ambient_signs, torus_signs)
    # The detour meridian is based at the source-side corner.  Table 1 starts
    # AsA^-1 at the opposite corner, so its plain correction is the transported
    # inverse A*Ngrid^-1*A^-1.  The outer-boundary connector forces this word.
    geometric['geom_N_source'] = alpha_s_words['alpha_s_grid_N']
    geometric['geom_N'] = (geometric['geom_A'] +
                           inverse(alpha_s_words['alpha_s_grid_N']) +
                           inverse(geometric['geom_A']))
    tracked.update(geometric)

    def signed(word, sign):
        return word if sign == 1 else inverse(word)

    # Convention scan for three coordinate identities quoted in Table 1.
    # Empty residuals are proofs in pi_1(C); nonempty residuals are merely
    # inconclusive because elementary elimination is not a word solver.
    coordinate_names = []
    for section_name, section in (("y1", lb_a_y1), ("y2", lb_a_y2)):
        for sign_a in (1, -1):
            for sign_x in (1, -1):
                name = (f"coord_alpha_base_{section_name}_"
                        f"A{sign_a:+d}_x{sign_x:+d}")
                candidate = signed(geometric['geom_A'], sign_a) + \
                            signed(geometric['geom_x'], sign_x)
                tracked[name] = free_reduce(inverse(section) + candidate)
                coordinate_names.append(name)
    for sign_a in (1, -1):
        for sign_r in (1, -1):
            name = f"coord_alpha_base_y2_A{sign_a:+d}_r{sign_r:+d}"
            candidate = signed(geometric['geom_A'], sign_a) + \
                        signed(geometric['geom_r'], sign_r)
            tracked[name] = free_reduce(inverse(lb_a_y2) + candidate)
            coordinate_names.append(name)
    for sign_r in (1, -1):
        for sign_x in (1, -1):
            core = signed(geometric['geom_r'], sign_r) + \
                   signed(geometric['geom_x'], sign_x)
            for output_sign in (1, -1):
                name = (f"coord_alpha_fiber_r{sign_r:+d}_x{sign_x:+d}_"
                        f"out{output_sign:+d}")
                candidate = inverse(core)
                tracked[name] = free_reduce(
                    inverse(signed(lf_a, output_sign)) + candidate)
                coordinate_names.append(name)
    for sign_s in (1, -1):
        for sign_r in (1, -1):
            candidate = (signed(geometric['geom_s'], sign_s) +
                         inverse(signed(geometric['geom_r'], sign_r)) +
                         inverse(signed(geometric['geom_s'], sign_s)))
            for output_sign in (1, -1):
                name = (f"coord_beta_fiber_s{sign_s:+d}_r{sign_r:+d}_"
                        f"out{output_sign:+d}")
                tracked[name] = free_reduce(
                    inverse(signed(lf_b, output_sign)) + candidate)
                coordinate_names.append(name)
    for sign_b in (1, -1):
        name = f"coord_beta_reference_B{sign_b:+d}"
        tracked[name] = free_reduce(
            inverse(bref_b) + signed(geometric['geom_B'], sign_b))
        coordinate_names.append(name)

    # Full beta base-direction word from Section 8.4.  M3 has already fixed
    # epsilon=-1 in our oriented convention, so the paper predicts
    # (r^-1 M r) B.  Scan the nearby sign/order conventions as diagnostics;
    # only an empty residual or a positive rewriting certificate is asserted.
    beta_corrections = {}
    for sign_m in (1, -1):
        correction = (inverse(geometric['geom_r']) +
                      signed(geometric['geom_M'], sign_m) +
                      geometric['geom_r'])
        beta_corrections[sign_m] = correction
        for sign_b in (1, -1):
            bb = signed(geometric['geom_B'], sign_b)
            for order, candidate in (("left", correction + bb),
                                     ("right", bb + correction)):
                for output_sign in (1, -1):
                    name = (f"coord_beta_base_M{sign_m:+d}_B{sign_b:+d}_"
                            f"{order}_out{output_sign:+d}")
                    tracked[name] = free_reduce(
                        inverse(signed(lb_b_s2, output_sign)) + candidate)
                    coordinate_names.append(name)

    # The first complete Table 1 comparison, with every loop and the meridian
    # carrying its explicit paper whisker.  The sign is left to the oriented
    # annulus calculation; exactly one convention should reduce to identity.
    for sign_m in (1, -1):
        name = f"table_M2_sign{sign_m:+d}"
        lhs = (geometric['geom_B'] + geometric['geom_y'] +
               inverse(geometric['geom_B']))
        rhs = (signed(geometric['geom_M'], sign_m) +
               geometric['geom_y'] + geometric['geom_x'])
        tracked[name] = free_reduce(lhs + inverse(rhs))
        coordinate_names.append(name)
        name = f"table_M3_sign{sign_m:+d}"
        lhs = (geometric['geom_B'] + geometric['geom_s'] +
               inverse(geometric['geom_B']))
        delta = inverse(geometric['geom_r'])
        rhs = (delta + signed(geometric['geom_M'], sign_m) +
               inverse(delta) + geometric['geom_s'])
        tracked[name] = free_reduce(lhs + inverse(rhs))
        coordinate_names.append(name)
    for sign_n in (1, -1):
        name = f"table_M1_sign{sign_n:+d}"
        lhs = (geometric['geom_A'] + geometric['geom_s'] +
               inverse(geometric['geom_A']))
        rhs = signed(geometric['geom_N'], sign_n) + geometric['geom_y']
        tracked[name] = free_reduce(lhs + inverse(rhs))
        coordinate_names.append(name)

    # Identify the two actual boundary components of the punctured M1 grid in
    # paper coordinates.  These scans do not assume their orientations.
    for boundary_name, target in (
            ('alpha_s_y_boundary', geometric['geom_y']),
            ('alpha_s_corrected_boundary',
             geometric['geom_A'] + geometric['geom_s'] +
             inverse(geometric['geom_A']))):
        for boundary_sign in (1, -1):
            name = f"coord_{boundary_name}_sign{boundary_sign:+d}"
            tracked[name] = free_reduce(
                inverse(signed(tracked[boundary_name], boundary_sign)) +
                target)
            coordinate_names.append(name)

    tracked_names = list(tracked)
    original_words = list(tracked.values())
    live, rels, words, tietze_certificate = simplify(
        P.ngens, P.relators, original_words, verbose=True, certify=True)
    replayed = verify_certificate(
        P.ngens, P.relators, original_words, tietze_certificate, verbose=True)
    assert replayed == (live, rels, words)
    save_certificate("r_tietze_certificate.json.gz", tietze_certificate)
    renumbering = {g: i + 1 for i, g in enumerate(sorted(live))}
    n, rels, words = renumber(live, rels, words)
    tracked = dict(zip(tracked_names, words))
    mu_a, lf_a = tracked['mu_a'], tracked['lf_a']
    lb_a1, lb_a2 = tracked['lb_a1'], tracked['lb_a2']
    mu_b, lf_b, lb_b = tracked['mu_b'], tracked['lf_b'], tracked['lb_b']
    corr_b, bref_b = tracked['corr_b'], tracked['beta_reference']
    lb_b_sweep = tracked['lb_b_sweep']
    sweep_residual = tracked['sweep_residual']
    longitude_residual = tracked['longitude_residual']
    print(f"  reduced: {n} gens, {len(rels)} relators ({time.time()-t0:.0f}s)")
    print(f"  words: mu_a {mu_a}\n         lb_a1 {lb_a1}\n         lb_a2 {lb_a2}\n"
          f"         mu_b {mu_b}\n         lb_b {lb_b}\n         lf_a {lf_a}\n"
          f"         lf_b {lf_b}\n         corr_b {corr_b}\n"
          f"         beta_reference {bref_b}\n"
          f"         lb_b_sweep {lb_b_sweep}\n"
          f"         sweep_residual {sweep_residual}\n"
          f"         longitude_residual {longitude_residual}")
    print("  sweep boundary identity corr_b * beta_reference = lb_b_sweep: ",
          "EXACT after Tietze" if not sweep_residual else
          f"not reduced to identity (residual length {len(sweep_residual)})")
    print("  direct and sweep boundary longitudes agree: ",
          "EXACT after Tietze" if not longitude_residual else
          f"not reduced to identity (residual length {len(longitude_residual)})")
    assert not longitude_residual, \
        "direct push-off disagrees with triangulation-derived sweep boundary"
    exact_coordinates = [name for name in coordinate_names if not tracked[name]]
    print("  exact paper-coordinate candidate identities:",
          exact_coordinates if exact_coordinates else "none")

    fillings = []
    for drift, longitude_a in ((1, lb_a1), (2, lb_a2)):
        for sign_a in (1, -1):
            for sign_b in (1, -1):
                power_a = longitude_a if sign_a == 1 else inverse(longitude_a)
                power_b = lb_b if sign_b == 1 else inverse(lb_b)
                fillings.append({
                    "drift": drift,
                    "sign_a": sign_a,
                    "sign_b": sign_b,
                    "paper_half_drift": "n1_y2" if drift == 1 else "n0_y1",
                    "paper_sign_a": -sign_a,
                    "paper_sign_b": -sign_b,
                    "relators": [mu_a + power_a, mu_b + power_b],
                })
    paper_fillings = []
    for half_name, meridian_a, longitude_a in (
            ("n0_y1", tracked['geom_M'], tracked['lb_a_y1']),
            ("n1_y2", tracked['geom_M_y2'], tracked['lb_a_y2'])):
        for sign_a in (1, -1):
            for sign_b in (1, -1):
                power_a = (longitude_a if sign_a == 1 else
                           inverse(longitude_a))
                power_b = (tracked['lb_b_s2'] if sign_b == 1 else
                           inverse(tracked['lb_b_s2']))
                paper_fillings.append({
                    "half_drift": half_name,
                    "sign_a": sign_a,
                    "sign_b": sign_b,
                    "relators": [meridian_a + power_a,
                                  tracked['geom_N'] + power_b],
                })
    export = {
        "format": "luttinger-filled-presentations-v1",
        "ngens": n,
        "relators": rels,
        "tracked_words": tracked,
        "fillings": fillings,
        "paper_fillings": paper_fillings,
        "tietze_certificate": "r_tietze_certificate.json.gz",
        "renumbering": {str(old): new for old, new in renumbering.items()},
    }
    with open("r_presentations.json", "w", encoding="ascii") as stream:
        json.dump(export, stream, separators=(",", ":"), sort_keys=True)
        stream.write("\n")
    print("  Tietze certificate replay: PASS; wrote r_presentations.json and "
          "r_tietze_certificate.json.gz")

    # ---- GAP certificate ----------------------------------------------
    gw = lambda w: "One(F)" if not w else "*".join(
        f"F.{abs(g)}" + ("^-1" if g < 0 else "") for g in w)
    gap = f"F := FreeGroup({n});;\n"
    gap += f"rels := [{','.join(gw(r) for r in rels)}];;\n"
    for nm, w in [("mua", mu_a), ("lfa", lf_a), ("lba1", lb_a1),
                  ("lba2", lb_a2), ("mub", mu_b), ("lfb", lf_b),
                  ("lbb", lb_b), ("lbbsweep", lb_b_sweep),
                  ("corrb", corr_b), ("brefb", bref_b)]:
        gap += f"{nm} := {gw(w)};;\n"
    gap += r"""
IDX := 4;;
fp := function(H) local Lw; Lw := LowIndexSubgroupsFpGroup(H, IDX);
  return [AbelianInvariants(H),
          List([1..IDX], i -> Number(Lw, u -> Index(H, u) = i))]; end;;

# 1. filling both tori back must give pi_1(R) = Prop 3.5
Fp := FreeGroup("x","y","r","s","A","B");;
x:=Fp.1;; y:=Fp.2;; r:=Fp.3;; s:=Fp.4;; A:=Fp.5;; Bg:=Fp.6;;
cm := function(u,v) return u*v*u^-1*v^-1; end;;
R35 := Fp/[cm(x,y)*cm(r,s),
  A*x*A^-1*r^-1, A*y*A^-1*s^-1, A*r*A^-1*x^-1, A*s*A^-1*y^-1,
  Bg*x*Bg^-1*y, Bg*y*Bg^-1*(y*x)^-1, Bg*r*Bg^-1*r^-1, Bg*s*Bg^-1*s^-1];;
Print("Prop 3.5 model : ", fp(R35), "\n");
Print("pi1(K) machine : ", fp(F/Concatenation(rels,[mua,mub])), "\n");

# 2. relation-sheet diff: the author's drilled system (fixed_v_certify.g
# base + three corrected transports, no surgery relators), over its local
# sign variants; the machine's pi1(C) must land on one of these fingerprints.
Fd := FreeGroup("x","y","r","s","A","B","M","N");;
x:=Fd.1;; y:=Fd.2;; r:=Fd.3;; s:=Fd.4;; A:=Fd.5;; Bd:=Fd.6;; M:=Fd.7;; N:=Fd.8;;
drilled := function(e3,e4,e5)
  return Fd/[cm(x,y)*cm(r,s),
    A*x*A^-1*r^-1, A*y*A^-1*s^-1, A*r*A^-1*x^-1,
    Bd*x*Bd^-1*y, Bd*r*Bd^-1*r^-1,
    Bd*(s^-1*r^-1*y*x)*Bd^-1*(r^-1*s^-1*x)^-1,
    A*s*A^-1*(N^e3*y)^-1,
    Bd*y*Bd^-1*(M^e4*y*x)^-1,
    Bd*s*Bd^-1*(r^-1*M^e5*r*s)^-1];
end;;
Print("pi1(C) machine : ", fp(F/rels), "\n");
for e3 in [1,-1] do for e4 in [1,-1] do for e5 in [1,-1] do
  Print("drilled(",e3,",",e4,",",e5,") : ", fp(drilled(e3,e4,e5)), "\n");
od; od; od;

# 3. the theorem: both +-1 base-direction surgeries kill the group,
# for every sign pair and both c-drift halves.
triv := function(G) local S, tab;
  if Length(AbelianInvariants(G)) > 0 then return "H1 NONZERO"; fi;
  S := SimplifiedFpGroup(G);
  if Length(FreeGeneratorsOfFpGroup(S)) = 0 then return "TRIVIAL (Tietze)"; fi;
  tab := CosetTableFromGensAndRels(FreeGeneratorsOfFpGroup(S),
           RelatorsOfFpGroup(S), [] : max := 2000000, silent := true);
  if tab = fail then return "OVERFLOW"; fi;
  if Length(tab[1]) = 1 then return "TRIVIAL"; fi;
  return Concatenation("|G| = ", String(Length(tab[1])));
end;;
# The direct boundary longitude lbb is already the slope used for surgery.
# lbbsweep is independently traced on the punctured sweep and has already
# reduced exactly to lbb in Python.  corrb*brefb is diagnostic until its
# coordinate identity is certified and must never be multiplied into lbb.
for pair in [["direct",lbb]] do
  for lba in [lba1, lba2] do
    for eA in [1,-1] do for eB in [1,-1] do
      Print("surgery ",pair[1]," drift=", Position([lba1,lba2],lba),
        " (", eA, ",", eB, "): ",
        triv(F/Concatenation(rels,[mua*lba^eA, mub*pair[2]^eB])), "\n");
    od; od;
  od;
od;
QUIT;;
"""
    open("r_cert.g", "w").write(gap)
    if shutil.which("gap") is None:
        print("gap is not on PATH; wrote r_cert.g and skipped GAP certificate")
        return
    print("running gap certificate...")
    out = subprocess.run(["gap", "-q", "r_cert.g"], input="",
                         capture_output=True, text=True, timeout=14000)
    print(out.stdout)
    if out.returncode:
        print(out.stderr[-3000:])


if __name__ == '__main__':
    main()
