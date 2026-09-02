#!/usr/bin/env python3
"""Locate the paper's displayed relation sheet inside Wuebben's ancillary GAP families.

Standard library only.  Free-group words are reduced by the twenty-line reducer below,
which shares no code with GAP, with the repository's pi1 module, or with any package.

Our side: the ten relations, two longitudes, and four sign sheets displayed in the
paper's "Relation sheet and product fillings" subsection, transcribed literally.

Wuebben's side: the relation systems defined by two scripts from the arXiv:2608.17267v1
ancillary package, vendored verbatim in ./wuebben_anc/ (see NOTICE there).  Their
SHA-256 digests are verified before anything else runs; a mismatch aborts.  The GAP
definitions were transcribed into Python by hand; the transcription is the one thing
this script cannot check about itself, so the sources sit beside it for inspection.

  decide2.g          the (m,n) grid at (e3,e4,e5,eA,eB) in {+-1}^5      288 systems
  fixed_v_certify.g  the (m,n)=(0,0) robustness family                  8192 systems

Every system is tested for equality with each of our four sheets as a multiset of
freely reduced relators.  The script then ASSERTS the expected answer -- exactly one
literal match per sheet per family, at the recorded parameters, and no other match
of any kind -- and exits nonzero if the corpus says anything else.

Nothing is enumerated.  This says nothing about geometry or manifolds.
"""
import hashlib
import sys
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENDORED = {
    "wuebben_anc/decide2.g":         "e750ebb79ed8856388a1b598b7cd003cb096d47531066411ffe45acc2e2900b5",
    "wuebben_anc/fixed_v_certify.g": "da77de354824d023c2f1939bbe72ad3cb2466224e813c1e6e2f466f230612e37",
}
EPRINT_SHA256 = "2cdd848816994561be29541322a6c8e197366cdf1ff1825646886d97734b78b2"   # provenance only


# ---------------------------------------------------------------- free group, stdlib
# A word is a tuple of (generator, exponent) with exponent in {+1,-1}, freely reduced.
GENS = ("x", "y", "r", "s", "A", "B", "M", "N")

def reduce(letters):
    out = []
    for g, e in letters:
        if out and out[-1][0] == g and out[-1][1] == -e:
            out.pop()
        else:
            out.append((g, e))
    return tuple(out)

class W:
    __slots__ = ("w",)
    def __init__(self, w=()): self.w = reduce(w)
    def __mul__(self, o): return W(self.w + o.w)
    def inv(self): return W(tuple((g, -e) for g, e in reversed(self.w)))
    def __pow__(self, n):
        base = self if n >= 0 else self.inv()
        out = W()
        for _ in range(abs(n)): out = out * base
        return out
    def __eq__(self, o): return self.w == o.w
    def __hash__(self): return hash(self.w)
    def __repr__(self):
        return "1" if not self.w else "".join(g + ("" if e == 1 else "^-1") for g, e in self.w)

x, y, r, s, A, B, M, N = (W(((g, 1),)) for g in GENS)
inv = lambda w: w.inv()
comm = lambda u, v: u * v * inv(u) * inv(v)          # [u,v] = u v u^-1 v^-1, both papers


# ---------------------------------------------------------------- our displayed sheet
def ours(epsA, epsB):
    surface = comm(x, y) * comm(r, s)
    transport = [
        A * x * inv(A) * inv(r),                          # A x A^-1 = r
        A * y * inv(A) * inv(s),                          # A y A^-1 = s
        A * r * inv(A) * inv(x),                          # A r A^-1 = x
        A * s * inv(A) * inv(N * y),                      # A s A^-1 = N y
        B * x * inv(B) * y,                               # B x B^-1 = y^-1
        B * y * inv(B) * inv(inv(M) * y * x),             # B y B^-1 = M^-1 y x
        B * r * inv(B) * inv(r),                          # B r B^-1 = r
        B * s * inv(B) * inv(inv(r) * inv(M) * r * s),    # B s B^-1 = (r^-1 M^-1 r) s
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
    dirTbBase = inv(r) * M ** (-e5) * r * B            # "sign anti-coupled to e5"
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
        try: b.remove(w)
        except ValueError: return False
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


# ---------------------------------------------------------------- expected answer (asserted)
SIGNS = (1, -1)
def expected_decide2(epsA, epsB):
    return ("literal", 0, 0, 1, -1, -1, epsA, epsB)
def expected_fixed_v(epsA, epsB):
    return ("literal", "y1/Ax", 1, 1, 1, "r^-1", "r^-1", 1, 1, 1, -1, -1, epsA, epsB)


def verify_sources():
    print("vendored Wuebben sources (sha256, verified):")
    for rel, want in VENDORED.items():
        got = hashlib.sha256((HERE / rel).read_bytes()).hexdigest()
        status = "OK" if got == want else "MISMATCH"
        print(f"  {got}  {rel}  {status}")
        if got != want:
            print(f"FAIL: {rel} does not match the arXiv:2608.17267v1 ancillary file", file=sys.stderr)
            raise SystemExit(2)
    print(f"  {EPRINT_SHA256}  arXiv e-print 2608.17267v1 tar.gz (provenance, not vendored)")
    print()


def main():
    verify_sources()
    failures = []

    for epsA, epsB in product(SIGNS, SIGNS):
        mine = ours(epsA, epsB)
        tag = f"({'+' if epsA==1 else '-'},{'+' if epsB==1 else '-'})"
        print(f"=== our sheet {tag}: {len(mine)} relators ===")

        hits = []
        for m, n in product([-1, 0, 1], repeat=2):
            for e3, e4, e5, eA, eB in product(SIGNS, repeat=5):
                theirs = wuebben_decide2(m, n, e3, e4, e5, eA, eB)
                if same_multiset(mine, theirs):
                    hits.append(("literal", m, n, e3, e4, e5, eA, eB))
                elif same_up_to_inverse(mine, theirs):
                    hits.append(("up-to-inverse", m, n, e3, e4, e5, eA, eB))
        print(f"  decide2.g grid (288 systems): {len(hits)} match(es)")
        for h in hits:
            print(f"    {h[0]:14} m={h[1]:+d} n={h[2]:+d}  e3={h[3]:+d} e4={h[4]:+d} e5={h[5]:+d}  eA={h[6]:+d} eB={h[7]:+d}")
        if hits != [expected_decide2(epsA, epsB)]:
            failures.append(f"decide2 {tag}: expected exactly {expected_decide2(epsA, epsB)}, got {hits}")

        hits2 = []
        for section_name, section in (("y1/Ax", A * x), ("y2/Ar^-1", A * inv(r))):
            for pAs, pBy, pBs in product([1, 2], repeat=3):
                for deltaBs, deltaF in product([inv(r), x], repeat=2):
                    for eta, pF in product(SIGNS, [1, 2]):
                        for e3, e4, e5, eA, eB in product(SIGNS, repeat=5):
                            theirs = wuebben_fixed_v(pAs, pBy, pBs, deltaBs, deltaF, eta, pF,
                                                     e3, e4, e5, eA, eB, section)
                            kind = ("literal" if same_multiset(mine, theirs)
                                    else "up-to-inverse" if same_up_to_inverse(mine, theirs)
                                    else None)
                            if kind:
                                hits2.append((kind, section_name, pAs, pBy, pBs,
                                              repr(deltaBs), repr(deltaF), eta, pF, e3, e4, e5, eA, eB))
        print(f"  fixed_v_certify.g family (8192 systems): {len(hits2)} match(es)")
        for h in hits2:
            print(f"    {h[0]:14} section={h[1]:9} placements(As,By,Bs,F)=({h[2]},{h[3]},{h[4]},{h[8]})"
                  f"  deltaBs={h[5]} deltaF={h[6]} eta={h[7]:+d}"
                  f"  e3={h[9]:+d} e4={h[10]:+d} e5={h[11]:+d} eA={h[12]:+d} eB={h[13]:+d}")
        if hits2 != [expected_fixed_v(epsA, epsB)]:
            failures.append(f"fixed_v {tag}: expected exactly {expected_fixed_v(epsA, epsB)}, got {hits2}")
        print()

    print("generator dictionary: identity on (x, y, r, s, A, B, M, N); same commutator convention")
    if failures:
        print("RESULT: FAIL")
        for f in failures:
            print("  " + f)
        raise SystemExit(1)
    print("RESULT: PASS — each sheet is literally Wuebben's (m,n)=(0,0), y1/Ax, e3=+1 e4=-1 e5=-1 system, "
          "uniquely, in both families")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
