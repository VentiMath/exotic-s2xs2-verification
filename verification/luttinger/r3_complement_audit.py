#!/usr/bin/env python3
"""Complement-level audit of Wuebben's drilled-fiber relation R3.

The older ``paper_bridge.certify_kappa3`` check proves the based monodromy
identity in an unpunctured beta mapping cylinder.  For R3 one also needs the
transport annulus to avoid both surgery tori.  This checker performs that
missing test in the full triangulated bundle.

The loop kappa3 intersects the fiber curve e, so sweeping it on the *core*
beta curve would meet T_beta.  The paper instead uses a parallel beta loop.
We check two simplicial grids:

1. kappa3 swept around the parallel beta loop has no T_alpha or T_beta
   vertices;
2. at the fixed fiber basepoint p, the parallel beta loop is homotopic to the
   core beta loop through a grid that also avoids both tori.

Together with the already certified based action
``psi(kappa3) = r^-1 s^-1 x``, these grids certify R3 in the actual torus
complement, rather than only in the unpunctured mapping cylinder.
"""

from bundle import build_bundle, check_bundle
from fiber import K_BAND
from layers import build_stack
from paper_bridge import certify_kappa3
from sweep import certify_grid_sweep


def beta_loop(B, vertex, transverse_index):
    """A closed beta loop at ``vertex`` and a chosen parallel-band index.

    Index 1 is the core beta curve carrying T_beta.  Indices 0 and 2 are its
    two simplicial parallels.  The stack seams at index j attach to angular
    copy A_j of the alpha annulus.
    """
    assert transverse_index in (0, 1, 2)
    j = transverse_index
    J = lambda k: ('J', k)
    return ([(('A', j, vertex), J(2))] +
            [(('S', level, vertex), ('t', j))
             for level in range(1, B['m'])] +
            [(('A', j, vertex), J(k)) for k in (0, 1, 2)])


def embedded_stack(B, transverse_index):
    """Embed the beta flip stack at one transverse band vertex.

    The paper-bridge certificate is carried by this whole three-dimensional
    mapping cylinder, not by a fixed rectangular edge grid (edges change
    during bistellar flips).  At transverse index 0 the complete cylinder is
    a subcomplex of the torus complement.
    """
    F, L, V = B['F'], B['L'], B['V']
    rank = L.rank.get
    twists = []
    for name, direction in (('b', 1), ('a', -1)):
        k = K_BAND[name]
        twists.append((
            [V(name, 0, i) for i in range(k)],
            [V(name, 1, i) for i in range(k)],
            [V(name, -1, i) for i in range(k)], direction))
    cells, levels, _ = build_stack(L, rank, twists, copy_tag='S')
    assert levels == B['m']
    j = transverse_index

    def embed(vertex):
        # Product endpoint slices are renamed into the alpha-annulus feet by
        # bundle.build_bundle.  Internal and cone vertices keep product names.
        if (isinstance(vertex, tuple) and len(vertex) == 3 and
                vertex[0] == 'S' and isinstance(vertex[1], int)):
            if vertex[1] == 0:
                return (('A', j, vertex[2]), ('J', 2))
            if vertex[1] == levels:
                return (('A', j, vertex[2]), ('J', 0))
        return (vertex, ('t', j))

    mapped_cells = [frozenset(embed(vertex) for vertex in cell)
                    for cell in cells]
    assert all(cell in B['K'].simplices[3] for cell in mapped_cells)
    mapped_vertices = {vertex for cell in mapped_cells for vertex in cell}
    return mapped_cells, mapped_vertices


def run(verbose=True):
    B = build_bundle(dir_b=1, dir_a=-1)
    T = check_bundle(B)
    components = {'alpha': B['Ta_verts'], 'beta': B['Tb_verts']}

    kappa3, certificate = certify_kappa3(B['F'], verbose=False)
    cset = set(B['F']['curves']['c'])
    eset = set(B['F']['curves']['e'])
    c_hits = [vertex for vertex in kappa3 if vertex in cset]
    e_hits = [vertex for vertex in kappa3 if vertex in eset]
    assert not c_hits
    assert len(e_hits) == 1

    # The paper's clean annulus lives in the entire beta mapping cylinder at
    # a parallel band level.  Certify that every mapping-cylinder tetrahedron
    # embeds in K and every one of its vertices lies outside both tori.
    parallel_cells, parallel_vertices = embedded_stack(B, 0)
    parallel_alpha = parallel_vertices & set(B['Ta_verts'])
    parallel_beta = parallel_vertices & set(B['Tb_verts'])
    assert not parallel_alpha
    assert not parallel_beta

    # The core level is deliberately not clean: it contains T_beta.  This
    # sensitivity control detects the exact distinction used in the proof.
    _, core_vertices = embedded_stack(B, 1)
    core_beta = core_vertices & set(B['Tb_verts'])
    assert core_beta

    # Changing the base loop from the chosen parallel to the core is harmless
    # at p: p is fixed by the monodromy and lies on neither fiber curve.
    p = 'p'
    basepoint_rows = [beta_loop(B, p, j) for j in (0, 1)]
    basepoint_hits = certify_grid_sweep(B['K'], basepoint_rows, components)
    assert not basepoint_hits['alpha']
    assert not basepoint_hits['beta']

    result = {
        'kappa_path_length': len(kappa3) - 1,
        'kappa_c_intersections': len(c_hits),
        'kappa_e_intersections': len(e_hits),
        'parallel_stack_tetrahedra': len(parallel_cells),
        'parallel_stack_vertices': len(parallel_vertices),
        'parallel_stack_alpha_vertices': len(parallel_alpha),
        'parallel_stack_beta_vertices': len(parallel_beta),
        'core_stack_beta_vertices': len(core_beta),
        'basepoint_homotopy_shape': [len(basepoint_rows),
                                     len(basepoint_rows[0])],
        'basepoint_homotopy_alpha_hits': len(basepoint_hits['alpha']),
        'basepoint_homotopy_beta_hits': len(basepoint_hits['beta']),
        'based_action_target': 'r^-1 s^-1 x',
        'prior_transport_tietze_steps': certificate['transport_tietze_steps'],
    }
    if verbose:
        print('R3 COMPLEMENT AUDIT')
        print('  kappa3: path length=%d, c-hits=%d, e-hits=%d' %
              (result['kappa_path_length'],
               result['kappa_c_intersections'],
               result['kappa_e_intersections']))
        print('  parallel beta stack: tetrahedra=%d, vertices=%d, '
              'T_alpha vertices=%d, T_beta vertices=%d' %
              (result['parallel_stack_tetrahedra'],
               result['parallel_stack_vertices'],
               result['parallel_stack_alpha_vertices'],
               result['parallel_stack_beta_vertices']))
        print('  core beta stack sensitivity: T_beta vertices=%d' %
              result['core_stack_beta_vertices'])
        print('  parallel-to-core homotopy at p: shape=%s, T_alpha hits=%d, '
              'T_beta hits=%d' %
              (result['basepoint_homotopy_shape'],
               result['basepoint_homotopy_alpha_hits'],
               result['basepoint_homotopy_beta_hits']))
        print('  based monodromy target:', result['based_action_target'])
        print('ALL R3 COMPLEMENT CHECKS PASSED')
    return result


if __name__ == '__main__':
    run()
