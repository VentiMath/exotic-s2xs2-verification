#!/usr/bin/env python3
"""Locate the paper's displayed relation sheet inside Wuebben's ancillary GAP families.

Our side: the ten relations, two longitudes, and four sign sheets displayed in the
paper's "Relation sheet and product fillings" subsection, transcribed literally.

Wuebben's side: the relation systems defined in two scripts from the arXiv:2608.17267v1
ancillary package (hashes recorded below), transcribed from GAP into free-group words:

  decide2.g         the (m,n) grid at (e3,e4,e5,eA,eB) in {+-1}^5   (9 x 32 systems)
  fixed_v_certify.g the (m,n)=(0,0) robustness family                (2 x 4096 systems)

Both are searched exhaustively for systems whose relator multiset equals ours as
reduced free-group words.  Nothing is enumerated; this is free-group bookkeeping only,
done in sympy so it shares no code with GAP.  It says nothing about geometry.
"""
from itertools import product
from sympy.combinatorics.free_groups import free_group

WUEBBEN_SOURCES = {
    "arXiv e-print 2608.17267v1 (tar.gz)": "2cdd848816994561be29541322a6c8e197366cdf1ff1825646886d97734b78b2",
    "anc/scripts/decide2.g":               "e750ebb79ed8856388a1b598b7cd003cb096d47531066411ffe45acc2e2900b5",
    "anc/scripts/fixed_v_certify.g":       "da77de354824d023c2f1939bbe72ad3cb2466224e813c1e6e2f466f230612e37",
}

F, x, y, r, s, A, B, M, N = free_group("x y r s A B M N")
inv = lambda w: w ** -1
comm = lambda u, v: u * v * inv(u) * inv(v)          # [u,v] = u v u^-1 v^-1, both papers


# ---------------------------------------------------------------- our displayed sheet
def ours(epsA, epsB):
    surface = comm(x, y) * comm(r, s)
    transport = [
        A * x * inv(A) * inv(r),                  # A x A^-1 = r
        A * y * inv(A) * inv(s),                  # A y A^-1 = s
        A * r * inv(A) * inv(x),                  # A r A^-1 = x
        A * s * inv(A) * inv(N * y),              # A s A^-1 = N y
        B * x * inv(B) * y,                       # B x B^-1 = y^-1
        B * y * inv(B) * inv(inv(M) * y * x),     # B y B^-1 = M^-1 y x
        B * r * inv(B) * inv(r),                  # B r B^-1 = r
        B * s * inv(B) * inv(inv(r) * inv(M) * r * s),   # B s B^-1 = (r^-1 M^-1 r) s
    ]
    drilled = B * (inv(s) * inv(r) * y * x) * inv(B) * inv(inv(r) * inv(s) * x)
    lam_a = A * x
    lam_b = (inv(r) * M * r) * B
    return [surface, *transport, drilled, M * lam_a ** epsA, N * lam_b ** epsB]


# ---------------------------------------------------------------- Wuebben, decide2.g
def wuebben_decide2(m, n, e3, e4, e5, eA, eB):
    R0 = comm(x, y) * comm(r, s)
    kappa3, psik3 = inv(s) * inv(r) * y * x, inv(r) * inv(s) * x
    base = [R0, A * x * inv(A) * inv(r), A * y * inv(A) * inv(s), A * r * inv(A) * inv(x),
            B * x * inv(B) * y, B * r * inv(B) * inv(r), B * kappa3 * inv(B) * inv(psik3)]
    dirTaBase, dirTaFib = A * x, inv(r * x)
    dirTbBase = inv(r) * M ** (-e5) * r * B          # "sign anti-coupled to e5"
    dirTbFib = s * inv(r) * inv(s)
    return base + [
        A * s * inv(A) * inv(N ** e3 * y),
        B * y * inv(B) * inv(M ** e4 * y * x),
        B * s * inv(B) * inv(inv(r) * M ** e5 * r * s),
        M * (dirTaBase * dirTaFib ** n) ** eA,
        N * (dirTbBase * dirTbFib ** m) ** eB,
    ]


# ---------------------------------------------------------------- Wuebben, fixed_v_certify.g
def _mk(lhs, image, correction, side):
    return lhs * inv(correction * image) if side == 1 else lhs * inv(image * correction)

def wuebben_fixed_v(pAs, pBy, pBs, deltaBs, deltaF, eta, pF, e3, e4, e5, eA, eB, section):
    base = [comm(x, y) * comm(r, s),
            A * x * inv(A) * inv(r), A * y * inv(A) * inv(s), A * r * inv(A) * inv(x),
            B * x * inv(B) * y, B * r * inv(B) * inv(r),
            B * (inv(s) * inv(r) * y * x) * inv(B) * inv(inv(r) * inv(s) * x)]
    corrF = deltaF * M ** eta * inv(deltaF)
    dirTb = corrF * B if pF == 1 else B * corrF
    return base + [
        _mk(A * s * inv(A), y, N ** e3, pAs),
        _mk(B * y * inv(B), y * x, M ** e4, pBy),
        _mk(B * s * inv(B), s, deltaBs * M ** e5 * inv(deltaBs), pBs),
        M * section ** eA,
        N * dirTb ** eB,
    ]


# ---------------------------------------------------------------- comparison
def same_multiset(a, b):
    a, b = list(a), list(b)
    if len(a) != len(b):
        return False
    for w in a:
        try:
            b.remove(w)
        except ValueError:
            return False
    return not b

def same_up_to_inverse(a, b):
    a, b = list(a), list(b)
    if len(a) != len(b):
        return False
    for w in a:
        if w in b: b.remove(w)
        elif inv(w) in b: b.remove(inv(w))
        else: return False
    return not b


def main():
    print("Wuebben sources (sha256):")
    for k, v in WUEBBEN_SOURCES.items():
        print(f"  {v}  {k}")
    print()

    signs = [1, -1]
    ok = True
    for epsA, epsB in product(signs, signs):
        mine = ours(epsA, epsB)
        tag = f"({'+' if epsA==1 else '-'},{'+' if epsB==1 else '-'})"
        print(f"=== our sheet {tag}: {len(mine)} relators ===")

        hits = []
        for m, n in product([-1, 0, 1], repeat=2):
            for e3, e4, e5, eA, eB in product(signs, repeat=5):
                theirs = wuebben_decide2(m, n, e3, e4, e5, eA, eB)
                if same_multiset(mine, theirs):
                    hits.append(("literal", m, n, e3, e4, e5, eA, eB))
                elif same_up_to_inverse(mine, theirs):
                    hits.append(("up-to-inverse", m, n, e3, e4, e5, eA, eB))
        print(f"  decide2.g grid (288 systems): {len(hits)} match(es)")
        for h in hits:
            print(f"    {h[0]:14} m={h[1]:+d} n={h[2]:+d}  e3={h[3]:+d} e4={h[4]:+d} e5={h[5]:+d}  eA={h[6]:+d} eB={h[7]:+d}")

        hits2 = []
        for section_name, section in (("y1/Ax", A * x), ("y2/Ar^-1", A * inv(r))):
            for pAs, pBy, pBs in product([1, 2], repeat=3):
                for deltaBs, deltaF in product([inv(r), x], repeat=2):
                    for eta, pF in product(signs, [1, 2]):
                        for e3, e4, e5, eA, eB in product(signs, repeat=5):
                            theirs = wuebben_fixed_v(pAs, pBy, pBs, deltaBs, deltaF, eta, pF,
                                                     e3, e4, e5, eA, eB, section)
                            if same_multiset(mine, theirs):
                                hits2.append(("literal", section_name, pAs, pBy, pBs,
                                              str(deltaBs), str(deltaF), eta, pF, e3, e4, e5, eA, eB))
                            elif same_up_to_inverse(mine, theirs):
                                hits2.append(("up-to-inverse", section_name, pAs, pBy, pBs,
                                              str(deltaBs), str(deltaF), eta, pF, e3, e4, e5, eA, eB))
        print(f"  fixed_v_certify.g family (8192 systems): {len(hits2)} match(es)")
        for h in hits2:
            print(f"    {h[0]:14} section={h[1]:9} placements(As,By,Bs,F)=({h[2]},{h[3]},{h[4]},{h[8]})"
                  f"  deltaBs={h[5]} deltaF={h[6]} eta={h[7]:+d}"
                  f"  e3={h[9]:+d} e4={h[10]:+d} e5={h[11]:+d} eA={h[12]:+d} eB={h[13]:+d}")
        if epsA == 1 and epsB == 1 and not any(h[0] == "literal" for h in hits):
            ok = False
        print()

    print("generator dictionary: identity on (x, y, r, s, A, B, M, N); same commutator convention")
    print("RESULT:", "our (+,+) sheet is literally a decide2.g system at (m,n)=(0,0)" if ok
          else "NO literal decide2.g match for our (+,+) sheet")
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
