"""
Assemble the triangulated bundle R: genus-2 fiber L over the once-punctured
torus, monodromy phi0 along alpha, psi0 = T_a T_b along beta.

Base model: alpha-annulus (angular = 3 fiber copies A0,A1,A2 around the
mapping torus Y, radial = J path j0-j1-j2) plus a band (the flip stack St
times the thickness arc tau0-tau1-tau2) whose feet are the fiber over the
angular arcs (copies 0..2) at the outer (j2) and inner (j0) radii.  The
seams identify the stack's bottom/top fiber-times-arc products with the
corresponding product slices of Y x J; the staircase cells agree on the
nose because every cylinder is built source-on-top over the same fiber rank.

Tori:
  T_alpha = c x alpha at mid-radius j1 (c = the phi0-invariant equator);
  T_beta  = e x beta (band core at mid-thickness tau1, radial return at
            angular copy 1).
"""
from complex import Complex, product
from fiber import build_fiber, K_BAND
from layers import build_stack, prism_cells, tri_list


def build_bundle(dir_b=1, dir_a=1, order_ba=('b', 'a')):
    F = build_fiber()
    L, V, phi0 = F['L'], F['V'], F['phi0']
    rank = L.rank.get
    Ltris = [frozenset(t) for t in tri_list(L)]

    # ---- Y: alpha mapping torus (2 product cylinders + phi0 cylinder) ----
    cells_Y = []
    for t in range(2):
        cells_Y += prism_cells(Ltris, rank,
                               lambda v, t=t: ('A', t + 1, v),
                               lambda v, t=t: ('A', t, v))
    cells_Y += prism_cells(Ltris, rank,
                           lambda v: ('A', 0, v),
                           lambda v: ('A', 2, phi0[v]))
    verts_Y = {v for c in cells_Y for v in c}
    order_Y = sorted(verts_Y, key=lambda w: (w[1], rank(w[2])))
    Y = Complex(cells_Y, order=order_Y)

    J = Complex([[('J', 0), ('J', 1)], [('J', 1), ('J', 2)]],
                order=[('J', 0), ('J', 1), ('J', 2)])
    P1 = product(Y, J)

    # ---- St: the beta flip stack --------------------------------------
    def twist_data(name, direction):
        k = K_BAND[name]
        return ([V(name, 0, i) for i in range(k)],
                [V(name, 1, i) for i in range(k)],
                [V(name, -1, i) for i in range(k)],
                direction)

    dirs = {'b': dir_b, 'a': dir_a}
    twists = [twist_data(nm, dirs[nm]) for nm in order_ba]
    cells_St, m, _name = build_stack(L, rank, twists, copy_tag='S')
    verts_St = {v for c in cells_St for v in c}

    def st_key(w):
        if w[0] == 'S' and isinstance(w[1], int):
            return (w[1], 0, rank(w[2]))
        # cone vertex: (('S','cone',level), qi)
        return (w[0][2], 1, w[1])
    order_St = sorted(verts_St, key=st_key)
    St = Complex(cells_St, order=order_St)

    tau = Complex([[('t', 0), ('t', 1)], [('t', 1), ('t', 2)]],
                  order=[('t', 0), ('t', 1), ('t', 2)])
    P2 = product(St, tau)

    # ---- seams: rename the stack's bottom/top slices into P1 names ----
    def rename(pv):
        sv, tv = pv
        if isinstance(sv, tuple) and sv[0] == 'S' and isinstance(sv[1], int):
            if sv[1] == 0:
                return (('A', tv[1], sv[2]), ('J', 2))
            if sv[1] == m:
                return (('A', tv[1], sv[2]), ('J', 0))
        return pv

    cells_K = [K1 for K1 in
               (tuple(sorted(c, key=str)) for c in
                (P1.sorted_tuple(s) for s in P1.simplices[max(P1.simplices)]))]
    cells_K += [tuple(sorted((rename(v) for v in P2.sorted_tuple(s)), key=str))
                for s in P2.simplices[max(P2.simplices)]]
    verts_K = {v for c in cells_K for v in c}
    K = Complex(cells_K, order=sorted(verts_K, key=str))

    # ---- the tori ------------------------------------------------------
    kc, ke = K_BAND['c'], K_BAND['e']
    c_cyc = [V('c', 0, i) for i in range(kc)]
    e_cyc = [V('e', 0, i) for i in range(ke)]
    c_rail = [V('c', 1, i) for i in range(kc)]
    e_rail = [V('e', 1, i) for i in range(ke)]

    Ta_verts = [(('A', t, cv), ('J', 1)) for t in range(3) for cv in c_cyc]
    Tb_verts = [(('S', i, ev), ('t', 1))
                for i in range(1, m) for ev in e_cyc]
    Tb_verts += [(('A', 1, ev), ('J', k)) for k in range(3) for ev in e_cyc]

    return {
        'K': K, 'F': F, 'L': L, 'V': V, 'phi0': phi0, 'm': m,
        'c': c_cyc, 'e': e_cyc, 'c_rail': c_rail, 'e_rail': e_rail,
        'Ta_verts': Ta_verts, 'Tb_verts': Tb_verts,
    }


def check_bundle(B):
    """Structural checks: K is a 4-pseudomanifold near the tori; the induced
    subcomplexes on the torus vertex sets are two disjoint closed tori."""
    from collections import defaultdict
    K = B['K']
    top = max(K.simplices)
    assert top == 4, f"K has dimension {top}"
    Tset = set(B['Ta_verts']) | set(B['Tb_verts'])
    assert len(Tset) == len(B['Ta_verts']) + len(B['Tb_verts']), \
        "torus vertex lists overlap"

    T = K.induced(Tset)
    fv = T.f_vector()
    chi = fv[0] - fv[1] + fv[2]
    assert len(fv) == 3, f"induced T has dimension {len(fv)-1}, want 2"
    assert chi == 0, f"induced T has chi = {chi}, want 0 (two tori)"
    # each component is a closed surface
    edge_deg = defaultdict(int)
    for t in T.simplices[2]:
        vs = T.sorted_tuple(t)
        for e in ((vs[0], vs[1]), (vs[0], vs[2]), (vs[1], vs[2])):
            edge_deg[frozenset(e)] += 1
    bad = [e for e, d in edge_deg.items() if d != 2]
    assert not bad, f"T not closed: {bad[:4]}"
    # two components, matching the two vertex sets
    comp_of = {}
    nbr = defaultdict(set)
    for e in T.simplices[1]:
        u, v = tuple(e)
        nbr[u].add(v)
        nbr[v].add(u)
    comps = []
    seen = set()
    for v in T.vertices():
        if v in seen:
            continue
        comp = {v}
        stack = [v]
        while stack:
            x = stack.pop()
            for y in nbr[x]:
                if y not in comp:
                    comp.add(y)
                    stack.append(y)
        seen |= comp
        comps.append(comp)
    assert len(comps) == 2, f"induced T has {len(comps)} components"
    assert {frozenset(B['Ta_verts']), frozenset(B['Tb_verts'])} == \
           {frozenset(c) for c in comps}, "components mix the two tori"

    # K is locally a 4-manifold along T: every 3-simplex meeting T lies in
    # exactly two 4-simplices
    from itertools import combinations
    near = [s for s in K.simplices[3] if s & Tset]
    cof = defaultdict(int)
    for s in K.simplices[4]:
        if not (s & Tset):
            continue
        for f in combinations(sorted(s, key=str), 4):
            fs = frozenset(f)
            if fs & Tset:
                cof[fs] += 1
    bad3 = [s for s in near if cof.get(s, 0) != 2]
    assert not bad3, f"{len(bad3)} 3-simplices near T are not interior " \
                     f"(e.g. {list(bad3[:2])})"
    print("bundle checks: T = two disjoint closed tori, K 4-manifold near T: OK")
    return T


if __name__ == '__main__':
    import time
    t0 = time.time()
    print("building bundle (dir_b=1, dir_a=-1, certified by monodromy_check)...")
    B = build_bundle(dir_b=1, dir_a=-1)
    print(f"K f-vector: {B['K'].f_vector()}  ({time.time()-t0:.0f}s)")
    t0 = time.time()
    check_bundle(B)
    print(f"checks: {time.time()-t0:.0f}s")
