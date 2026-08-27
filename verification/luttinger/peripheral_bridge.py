"""Certify the slope permutation between local and paper torus coordinates.

The historical run used positive base lifts at arbitrary c[0]/e[0] corners.
The paper uses the inverse base generators A,B and starts at c_y/s_e.  This
module compares the literal closed paths in the two induced surgery tori,
before any complement whiskers are attached.  Since each component is a
torus, a completed KB system gives an exact free-homotopy/homology check.
"""

from bundle import build_bundle, check_bundle
from paper_bridge import build_paper_loops
from pi1 import Presentation, free_reduce, inverse


def _gap_word(word, group="F"):
    if not word:
        return f"One({group})"
    return "*".join(
        f"{group}.{abs(letter)}" + ("^-1" if letter < 0 else "")
        for letter in word)


def _check_path(K, path):
    assert path[0] == path[-1]
    for u, v in zip(path, path[1:]):
        assert u == v or frozenset((u, v)) in K.simplices[1], \
            f"not an edge: {u!r} -> {v!r}"


def _component_program(name, K, paths, identities):
    base = next(iter(K.vertices()))
    P = Presentation(K, base)
    words = {}
    for path_name, path in paths.items():
        _check_path(K, path)
        words[path_name] = P.loop_word(path)

    lines = [f'# {name}', 'LoadPackage("kbmag");;',
             f"F := FreeGroup({P.ngens});;",
             f"rels := [{','.join(_gap_word(r) for r in P.relators)}];;",
             "G := F/rels;;",
             "iso := IsomorphismSimplifiedFpGroup(G);; H := Image(iso);;",
             "rws := KBMAGRewritingSystem(H);;",
             "attempt := CALL_WITH_CATCH(KnuthBendix,[rws]);;",
             "freegens := GeneratorsOfGroup(FreeStructureOfRewritingSystem(rws));;",
             "hom := GroupHomomorphismByImages(F,G,GeneratorsOfGroup(F),GeneratorsOfGroup(G));;",
             "tofree := function(w) local letters;",
             "  letters := LetterRepAssocWord(UnderlyingElement(w));",
             "  if Length(letters)=0 then return One(freegens[1]); fi;",
             "  return Product(letters,i->freegens[AbsInt(i)]^SignInt(i));",
             "end;;",
             f'Print("{name}: KB=",attempt," confluent=",IsConfluent(rws),"\\n");']
    for identity_name, factors in identities.items():
        residual = []
        for path_name, sign in factors:
            word = words[path_name]
            residual += word if sign > 0 else inverse(word)
        residual = free_reduce(residual)
        lines += [f"w := {_gap_word(residual)};;",
                  "wH := Image(iso,Image(hom,w));;",
                  "normal := ReducedForm(rws,tofree(wH));;",
                  f'Print("  {identity_name}: ",normal);;',
                  'if IsOne(normal) then Print("  CERTIFIED IDENTITY\\n");',
                  'else Print("  INCONCLUSIVE\\n"); fi;']
    return "\n".join(lines), words


def main():
    B = build_bundle(dir_b=1, dir_a=-1)
    T = check_bundle(B)
    Ta = T.induced(set(B['Ta_verts']))
    Tb = T.induced(set(B['Tb_verts']))
    c, e, m = B['c'], B['e'], B['m']
    kc, ke = len(c), len(e)
    J = lambda k: ('J', k)
    va = lambda t, i: (('A', t, c[i % kc]), J(1))
    vb = lambda k, i: (('A', 1, e[i % ke]), J(k))
    sb = lambda level, i: (('S', level, e[i % ke]), ('t', 1))

    # Historical positive alpha lift at c[0].
    half = kc // 2
    old_lift = [va(0, 0), va(1, 0), va(2, 0), va(0, half)]
    old_down = old_lift + [va(0, i) for i in range(half - 1, -1, -1)]
    old_up = old_lift + [va(0, i) for i in range(half + 1, kc)] + [va(0, 0)]

    # Paper A-lift at c_y, with the two closing half-arcs retained.
    paper_loops = build_paper_loops(B['F'])
    cset = set(B['F']['curves']['c'])
    cy = next(vertex for vertex in paper_loops['y'] if vertex in cset)
    cy_i = c.index(cy)
    opposite_i = (cy_i + half) % kc
    paper_lift = [va(0, cy_i), va(2, opposite_i), va(1, opposite_i),
                  va(0, opposite_i)]

    def half_arc(step):
        indices, i = [], opposite_i
        while i != cy_i:
            i = (i + step) % kc
            indices.append(i)
        assert len(indices) == half
        return [va(0, i) for i in indices]

    paper_down = paper_lift + half_arc(-1)
    paper_up = paper_lift + half_arc(+1)
    alpha_paths = {
        'old_down': old_down, 'old_up': old_up,
        'paper_down': paper_down, 'paper_up': paper_up,
    }
    alpha_identities = {
        # Reversing the base lift swaps the closing half-arc.
        'old_down_equals_inverse_paper_up':
            [('old_down', 1), ('paper_up', 1)],
        'old_up_equals_inverse_paper_down':
            [('old_up', 1), ('paper_down', 1)],
    }

    # Historical positive beta loop and the paper's inverse B-loop.  psi fixes
    # e pointwise, so there is no half-drift to permute.
    old_beta = ([vb(2, 0)] + [sb(level, 0) for level in range(1, m)] +
                [vb(0, 0), vb(1, 0), vb(2, 0)])
    eset = set(B['F']['curves']['e'])
    se = next(vertex for vertex in paper_loops['s'] if vertex in eset)
    se_i = e.index(se)
    paper_beta = ([vb(2, se_i), vb(1, se_i), vb(0, se_i)] +
                  [sb(level, se_i) for level in range(m - 1, 0, -1)] +
                  [vb(2, se_i)])
    beta_paths = {'old_beta': old_beta, 'paper_beta': paper_beta}
    beta_identities = {
        'old_beta_equals_inverse_paper_beta':
            [('old_beta', 1), ('paper_beta', 1)],
    }

    alpha_gap, alpha_words = _component_program(
        'T_alpha', Ta, alpha_paths, alpha_identities)
    beta_gap, beta_words = _component_program(
        'T_beta', Tb, beta_paths, beta_identities)
    with open('peripheral_bridge.g', 'w', encoding='ascii') as stream:
        stream.write(alpha_gap + "\n" + beta_gap + "\nQUIT;;\n")
    print(f"T_alpha {Ta.f_vector()}: path word lengths " +
          ", ".join(f"{k}={len(v)}" for k, v in alpha_words.items()))
    print(f"T_beta {Tb.f_vector()}: path word lengths " +
          ", ".join(f"{k}={len(v)}" for k, v in beta_words.items()))
    print("wrote peripheral_bridge.g")


if __name__ == '__main__':
    main()
