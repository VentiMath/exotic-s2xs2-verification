"""The equivariant-lift step of Lemma 8.2, certified on the simplicial model.

The paper's equivariant Moser normalization cites covering-space theory
twice: the collar quotient A_c -> A_c/phi0 is a connected double cover, and
the normalizing diffeomorphism downstairs lifts, with the lift equivariant
because a deck transformation covering the identity that is not the
identity must equal phi0. Those citations are generic; our collar is not.
This script certifies every topological hypothesis of that argument on the
actual simplicial collar, and proves the deck-group step outright:

  1. the c-band collar A_c (24 vertices, 32 triangles) is a connected
     annulus, phi0-invariant, with the action free and regular (no simplex
     meets its own image and no simplex contains an orbit pair), so the
     quotient is again a simplicial complex;
  2. the quotient A-bar (12 vertices, 16 triangles) is a connected annulus;
  3. the projection is a genuine 2-to-1 simplicial covering: every quotient
     simplex has exactly two preimages and the projection is injective on
     every closed vertex star;
  4. the simplicial deck group is exactly {id, phi0}: fiber-preserving
     adjacency propagation from either seed value at a base vertex forces
     the whole map, and only those two maps arise -- the paper's
     "covers the identity, not the identity, hence equals phi0" step,
     proved by enumeration rather than cited;
  5. both annuli collapse simplicially to their core circles, so the cores
     carry pi1, and the projection restricted to cores is the connected
     double cover of the circle: the core c (length 8) winds exactly twice
     around the quotient core c-bar (length 4). Hence pi_*(pi1(A_c)) is the
     index-two subgroup <[c-bar]^2>, and any map fixing c-bar pointwise
     fixes [c-bar], so the lifting criterion's subgroup condition holds.

What remains cited after this: only the continuous lifting principle itself
(existence and uniqueness of lifts through a covering once the subgroup
condition holds). Its hypotheses, and the deck-group argument, are now
machine facts about the model rather than trusted pictures.

Everything asserts; any failure hard-exits.
"""
import sys
from collections import defaultdict

from fiber import K_BAND, build_fiber


def fail(msg):
    print(f"FAIL {msg}")
    sys.exit(1)


def check(label, ok):
    if not ok:
        fail(label)
    print(f"PASS {label}")


def edges_of(tris):
    count = defaultdict(int)
    for t in tris:
        vs = sorted(t, key=str)
        for e in ((vs[0], vs[1]), (vs[0], vs[2]), (vs[1], vs[2])):
            count[frozenset(e)] += 1
    return count


def is_connected(verts, edge_count):
    adj = defaultdict(set)
    for e in edge_count:
        u, v = tuple(e)
        adj[u].add(v)
        adj[v].add(u)
    start = next(iter(verts))
    seen, frontier = {start}, [start]
    while frontier:
        seen.update(w for v in frontier for w in adj[v] if w not in seen)
        frontier = [w for v in frontier for w in adj[v] if w in seen
                    and w not in getattr(is_connected, "_", ())]
        # simple BFS restart-free variant:
        frontier = [w for w in seen if any(x not in seen for x in adj[w])]
        for w in list(frontier):
            seen.update(adj[w])
    return len(seen) == len(verts)


def boundary_cycles(edge_count):
    boundary = [e for e, n in edge_count.items() if n == 1]
    adj = defaultdict(list)
    for e in boundary:
        u, v = tuple(e)
        adj[u].append(v)
        adj[v].append(u)
    seen, cycles = set(), []
    for start in adj:
        if start in seen:
            continue
        cyc, prev, cur = [start], None, start
        seen.add(start)
        while True:
            nxt = [w for w in adj[cur] if w != prev]
            assert nxt, "boundary trace stuck"
            w = nxt[0]
            if w == start:
                break
            cyc.append(w)
            seen.add(w)
            prev, cur = cur, w
        cycles.append(cyc)
    return cycles


def annulus_report(name, tris):
    verts = set().union(*tris)
    edge_count = edges_of(tris)
    chi = len(verts) - len(edge_count) + len(tris)
    check(f"{name}: every edge lies in at most two triangles",
          all(n <= 2 for n in edge_count.values()))
    check(f"{name}: connected", is_connected(verts, edge_count))
    check(f"{name}: Euler characteristic 0 "
          f"({len(verts)}-{len(edge_count)}+{len(tris)})", chi == 0)
    cycles = boundary_cycles(edge_count)
    check(f"{name}: exactly two boundary circles", len(cycles) == 2)
    print(f"     {name}: {len(verts)} vertices, {len(edge_count)} edges, "
          f"{len(tris)} triangles; boundary lengths "
          f"{sorted(len(c) for c in cycles)}")
    return verts, edge_count


def collapse_to_core(name, tris, core_edges, core_verts):
    tris = set(tris)
    edges = set(edges_of(tris))
    verts = set().union(*tris) if tris else set()
    changed = True
    while changed:
        changed = False
        edge_tris = defaultdict(list)
        for t in tris:
            vs = sorted(t, key=str)
            for e in ((vs[0], vs[1]), (vs[0], vs[2]), (vs[1], vs[2])):
                edge_tris[frozenset(e)].append(t)
        for e in sorted(edges, key=str):
            if e in core_edges:
                continue
            owners = edge_tris.get(e, [])
            if len(owners) == 1 and owners[0] in tris:
                tris.discard(owners[0])
                edges.discard(e)
                changed = True
                break
        if changed:
            continue
        vert_edges = defaultdict(list)
        for e in edges:
            for v in e:
                vert_edges[v].append(e)
        for v in sorted(verts, key=str):
            if v in core_verts:
                continue
            if len(vert_edges.get(v, [])) == 1:
                edges.discard(vert_edges[v][0])
                verts.discard(v)
                changed = True
                break
    check(f"{name}: collapses simplicially to its core circle",
          not tris and edges == core_edges
          and verts == core_verts.union(*core_edges))
    return True


fiber = build_fiber()
V, phi0 = fiber["V"], fiber["phi0"]
k = K_BAND["c"]

# -- 1. the collar and the action -------------------------------------------
collar = set()
for r in (-1, 0):
    for i in range(k):
        p00, p10 = V("c", r, i), V("c", r + 1, i)
        p01, p11 = V("c", r, i + 1), V("c", r + 1, i + 1)
        collar.add(frozenset((p00, p10, p01)))
        collar.add(frozenset((p10, p01, p11)))
check("collar has 32 triangles on 24 distinct vertices",
      len(collar) == 32 and len(set().union(*collar)) == 24)
verts, _ = annulus_report("A_c", collar)

check("phi0 maps the collar to itself simplicially",
      all(frozenset(phi0[v] for v in t) in collar for t in collar))
check("the action is free on vertices",
      all(phi0[v] != v for v in verts))
check("no simplex meets its own image",
      all(frozenset(phi0[v] for v in t).isdisjoint(t) for t in collar))
check("no simplex contains an orbit pair (quotient is simplicial)",
      all(phi0[v] != w for t in collar for v in t for w in t))
check("phi0 is an involution on the collar",
      all(phi0[phi0[v]] == v for v in verts))

# -- 2. the quotient ---------------------------------------------------------
rep = {v: min(v, phi0[v], key=str) for v in verts}
quotient = {frozenset(rep[v] for v in t) for t in collar}
check("quotient has 16 triangles on 12 vertices",
      len(quotient) == 16 and len(set().union(*quotient)) == 12
      and all(len(t) == 3 for t in quotient))
annulus_report("A-bar", quotient)

# -- 3. the covering ---------------------------------------------------------
preimages = defaultdict(list)
for t in collar:
    preimages[frozenset(rep[v] for v in t)].append(t)
check("every quotient triangle has exactly two preimage triangles",
      all(len(ts) == 2 for ts in preimages.values())
      and set(preimages) == quotient)

neighbours = defaultdict(set)
for t in collar:
    for v in t:
        neighbours[v].update(t - {v})
star_ok = True
for v in verts:
    imgs = {rep[w] for w in neighbours[v]}
    if len(imgs) != len(neighbours[v]) or rep[v] in imgs:
        star_ok = False
check("projection is injective on every closed vertex star", star_ok)

# -- 4. the deck group, by enumeration ---------------------------------------
base = sorted(verts, key=str)[0]
found = []
for seed in (base, phi0[base]):
    g = {base: seed}
    frontier = [base]
    consistent = True
    while frontier and consistent:
        v = frontier.pop()
        for w in neighbours[v]:
            candidates = [u for u in (w, phi0[w])
                          if u in neighbours[g[v]] or u == g[v]]
            candidates = [u for u in candidates if u in neighbours[g[v]]]
            if len(candidates) != 1:
                consistent = False
                break
            if w in g:
                if g[w] != candidates[0]:
                    consistent = False
                    break
            else:
                g[w] = candidates[0]
                frontier.append(w)
    if consistent and len(g) == len(verts):
        if all(frozenset(g[v] for v in t) in collar for t in collar):
            found.append(g)
check("deck propagation from each seed determines a unique simplicial map",
      len(found) == 2)
check("the two deck transformations are exactly id and phi0",
      all(found[0][v] == v for v in verts)
      and all(found[1][v] == phi0[v] for v in verts))

# -- 5. cores, collapses, and the winding ------------------------------------
core = [V("c", 0, i) for i in range(k)]
core_edges = {frozenset((core[i], core[(i + 1) % k])) for i in range(k)}
collapse_to_core("A_c", collar, core_edges, set(core))

qcore = []
for v in core:
    if rep[v] not in qcore:
        qcore.append(rep[v])
check("quotient core is a 4-cycle", len(qcore) == 4)
qcore_edges = {frozenset((qcore[i], qcore[(i + 1) % 4])) for i in range(4)}
collapse_to_core("A-bar", quotient, qcore_edges, set(qcore))

projected = [rep[v] for v in core]
check("the core covers the quotient core with winding number exactly two",
      projected == qcore + qcore and len(set(projected)) == 4)
check("the total space core is a single connected cycle (connected cover)",
      len(set(core)) == k)

print()
print("subgroup criterion: pi1 is carried by the cores (both collapses");
print("above), pi_* [c] = [c-bar]^2, so pi_*(pi1(A_c)) is the index-two")
print("subgroup; a map fixing c-bar pointwise fixes [c-bar] and therefore")
print("preserves that subgroup. Only the continuous lifting principle")
print("itself remains cited; its hypotheses and the deck-group step are")
print("machine facts above.")
print("ALL SIMPLICIAL LIFT CHECKS PASSED")
