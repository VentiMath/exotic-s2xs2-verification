"""Audit the global correspondence between the audit-defined marked bundle and K.

This module deliberately checks structural data *before* any surgery-group
calculation.  It certifies the combinatorial part of the following dictionary:

  audit F                 <-> fiber.py's closed marked genus-2 surface L
  audit phi_0             <-> the simplicial half-turn ``phi0``
  audit psi_0=T_a T_b     <-> the open flip stack with directions (b,+),(a,-)
  audit T_alpha=c x alpha <-> the induced Ta component in bundle.py
  audit T_beta=e x beta   <-> the induced Tb component in bundle.py

The remaining non-combinatorial bridge is stated explicitly in the returned
report: the PL bundle assembled from mapping cylinders must be identified with
the audit-defined smooth bundle, and the product framing must be identified
with its Lagrangian framing.  Comparing those objects with Wuebben's intended
ones is the separate source boundary S1--S4.
"""

from collections import defaultdict
from itertools import combinations

from bundle import build_bundle, check_bundle
from fiber import K_BAND, build_fiber, check_fiber
from layers import build_stack
from paper_bridge import (certify_beta_based_monodromy, certify_kappa3,
                          certify_paper_loops)


def _e_stack_product_check(F):
    """The beta stack restricts to the literal product e x I, pointwise at ends."""
    L, V = F["L"], F["V"]
    twists = []
    for name, direction in (("b", 1), ("a", -1)):
        k = K_BAND[name]
        twists.append((
            [V(name, 0, i) for i in range(k)],
            [V(name, 1, i) for i in range(k)],
            [V(name, -1, i) for i in range(k)],
            direction,
        ))
    cells, levels, _ = build_stack(L, L.rank.get, twists, copy_tag="MC")
    e = [V("e", 0, i) for i in range(K_BAND["e"])]
    e_set = set(e)

    # A flip cone meeting e would mean the purported fixed neighborhood is
    # being retriangulated by the twist construction.
    for cell in cells:
        if any(isinstance(v, tuple) and len(v) == 2 and
               isinstance(v[0], tuple) and v[0][:2] == ("MC", "cone")
               for v in cell):
            assert not any(isinstance(v, tuple) and len(v) == 3 and
                           v[0] == "MC" and v[2] in e_set for v in cell), \
                "a beta-stack flip cone meets the e core"

    triangles = {frozenset(face) for cell in cells
                 for face in combinations(cell, 3)}
    for level in range(levels):
        for i, u in enumerate(e):
            v = e[(i + 1) % len(e)]
            vertical_square = {
                ("MC", level, u), ("MC", level, v),
                ("MC", level + 1, u), ("MC", level + 1, v),
            }
            square_tris = [t for t in triangles if t <= vertical_square]
            assert len(square_tris) == 2, \
                f"e x I square at level {level}, edge {i} is not a product square"
    return {"levels": levels, "e_edges": len(e),
            "checked_product_squares": levels * len(e)}


def _global_codimension_one_check(K):
    """Check K has only interior or boundary tetrahedra and closed boundary."""
    cofaces = defaultdict(int)
    for simplex in K.simplices[4]:
        for face in combinations(K.sorted_tuple(simplex), 4):
            cofaces[frozenset(face)] += 1
    assert set(cofaces) == K.simplices[3]
    bad = [face for face, degree in cofaces.items() if degree not in (1, 2)]
    assert not bad, f"global non-pseudomanifold tetrahedra: {bad[:3]}"
    boundary_tets = {face for face, degree in cofaces.items() if degree == 1}
    assert boundary_tets, "the once-punctured-base bundle must have boundary"

    boundary_tri_degree = defaultdict(int)
    for tet in boundary_tets:
        for tri in combinations(K.sorted_tuple(tet), 3):
            boundary_tri_degree[frozenset(tri)] += 1
    bad_boundary = [tri for tri, degree in boundary_tri_degree.items()
                    if degree != 2]
    assert not bad_boundary, \
        f"boundary is not a closed 3-pseudomanifold: {bad_boundary[:3]}"

    # Boundary connectedness, using tetrahedra adjacent across triangles.
    incident = defaultdict(list)
    for tet in boundary_tets:
        for tri in combinations(K.sorted_tuple(tet), 3):
            incident[frozenset(tri)].append(tet)
    start = next(iter(boundary_tets))
    seen = {start}
    stack = [start]
    while stack:
        tet = stack.pop()
        for tri in combinations(K.sorted_tuple(tet), 3):
            for other in incident[frozenset(tri)]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
    assert seen == boundary_tets, "bundle boundary has more than one component"

    fv = K.f_vector()
    chi = sum((-1) ** i * n for i, n in enumerate(fv))
    assert chi == 2, f"chi(K)={chi}, want chi(F)chi(T0)=(-2)(-1)=2"
    return {"f_vector": fv, "chi": chi,
            "boundary_tetrahedra": len(boundary_tets),
            "boundary_connected": True}


def audit_model_correspondence(verbose=True):
    F = build_fiber()
    check_fiber(F, verbose=verbose)
    loops, fiber_certificate = certify_paper_loops(F, verbose=verbose)
    beta_certificate = certify_beta_based_monodromy(F, verbose=verbose)
    _, kappa_certificate = certify_kappa3(F, verbose=verbose)

    phi0, V = F["phi0"], F["V"]
    c = [V("c", 0, i) for i in range(K_BAND["c"])]
    half = len(c) // 2
    assert [phi0[v] for v in c] == c[half:] + c[:half], \
        "phi0|c is not the literal free half-rotation"
    assert phi0["p"] == "p" and phi0["O"] == "O"

    e_product = _e_stack_product_check(F)
    B = build_bundle(dir_b=1, dir_a=-1)
    T = check_bundle(B)
    global_check = _global_codimension_one_check(B["K"])

    ta, tb = set(B["Ta_verts"]), set(B["Tb_verts"])
    assert not (ta & tb)
    assert T.induced(ta).f_vector()[0] == len(ta)
    assert T.induced(tb).f_vector()[0] == len(tb)

    report = {
        "marked_fiber": "certified",
        "phi0_based_action": "x->r, y->s as literal p-based paths",
        "phi0_on_c": "free half-rotation",
        "psi0_based_action": "x->y^-1, y->yx, r->r, s->s",
        "psi0_on_e": "literal pointwise product",
        "e_stack_product": e_product,
        "global_complex": global_check,
        "surgery_tori": {
            "components": 2,
            "disjoint": True,
            "T_alpha_vertices": len(ta),
            "T_beta_vertices": len(tb),
        },
        "fiber_certificate": fiber_certificate,
        "kappa3_certificate": kappa_certificate,
        "remaining_smooth_inputs": [
            "mapping-cylinder/flip PL bundle is smoothed as the LP marked bundle",
            "fibered framing equals Lagrangian framing (paper Lemma 8.2)",
        ],
    }
    if verbose:
        print("model correspondence: phi0|c is the free half-rotation: PASS")
        print("model correspondence: psi0 fixes e through a literal product: PASS")
        print("model correspondence: K has connected closed boundary and chi=2: PASS")
        print("model correspondence: T_alpha,T_beta are disjoint induced tori: PASS")
        print("remaining smooth inputs:")
        for item in report["remaining_smooth_inputs"]:
            print("  -", item)
    return report


if __name__ == "__main__":
    audit_model_correspondence()
