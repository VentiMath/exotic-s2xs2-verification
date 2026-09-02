#!/usr/bin/env python3
"""Print the relation-by-relation dictionary between the paper's displayed sheet and
Wuebben's fixed member, and the (empty) diff between them.

Companion to compare_sheets.py, which located the sheet inside Wuebben's two ancillary
families by exhaustive search and asserted the answer.  This script does the converse,
readable thing: it takes the located parameters, writes our twelve relators beside his
twelve at those parameters, names the parameter that makes each pair agree, and prints
the literal diff of the two sorted relator lists.  Standard library only; the free-group
reducer and both transcriptions are imported from compare_sheets.py, whose source hash
check runs first.  Nothing here is about manifolds.
"""
import difflib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compare_sheets as cs  # noqa: E402

x, y, r, s, A, B, M, N = cs.x, cs.y, cs.r, cs.s, cs.A, cs.B, cs.M, cs.N
inv, comm, W = cs.inv, cs.comm, cs.W

# Located parameters (compare_sheets.py asserts these are the unique match in each family).
M_, N_, E3, E4, E5 = 0, 0, 1, -1, -1
FIXED_V = dict(pAs=1, pBy=1, pBs=1, deltaBs=inv(r), deltaF=inv(r), eta=1, pF=1, section=A * x)


def sgn(e):
    return "+1" if e == 1 else "-1"


def rows(epsA, epsB):
    """(label, our name, our relator, his form as written in decide2.g, parameter, his relator)."""
    dirTaBase, dirTaFib = A * x, inv(r * x)
    dirTbBase = inv(r) * M ** (-E5) * r * B
    dirTbFib = s * inv(r) * inv(s)
    kappa3, psik3 = inv(s) * inv(r) * y * x, inv(r) * inv(s) * x
    return [
        ("R1", "[x,y][r,s] = 1", comm(x, y) * comm(r, s),
         "R0 = [x,y][r,s]", "-", comm(x, y) * comm(r, s)),
        ("R2", "A x A^-1 = r", A * x * inv(A) * inv(r),
         "A x A^-1 r^-1", "-", A * x * inv(A) * inv(r)),
        ("R3", "A y A^-1 = s", A * y * inv(A) * inv(s),
         "A y A^-1 s^-1", "-", A * y * inv(A) * inv(s)),
        ("R4", "A r A^-1 = x", A * r * inv(A) * inv(x),
         "A r A^-1 x^-1", "-", A * r * inv(A) * inv(x)),
        ("R5", "A s A^-1 = N y", A * s * inv(A) * inv(N * y),
         "A s A^-1 (N^e3 y)^-1", f"e3 = {sgn(E3)}", A * s * inv(A) * inv(N ** E3 * y)),
        ("R6", "B x B^-1 = y^-1", B * x * inv(B) * y,
         "B x B^-1 y", "-", B * x * inv(B) * y),
        ("R7", "B y B^-1 = M^-1 y x", B * y * inv(B) * inv(inv(M) * y * x),
         "B y B^-1 (M^e4 y x)^-1", f"e4 = {sgn(E4)}", B * y * inv(B) * inv(M ** E4 * y * x)),
        ("R8", "B r B^-1 = r", B * r * inv(B) * inv(r),
         "B r B^-1 r^-1", "-", B * r * inv(B) * inv(r)),
        ("R9", "B s B^-1 = (r^-1 M^-1 r) s", B * s * inv(B) * inv(inv(r) * inv(M) * r * s),
         "B s B^-1 (r^-1 M^e5 r s)^-1", f"e5 = {sgn(E5)}", B * s * inv(B) * inv(inv(r) * M ** E5 * r * s)),
        ("R10", "B (s^-1 r^-1 y x) B^-1 = r^-1 s^-1 x", B * kappa3 * inv(B) * inv(psik3),
         "B kappa3 B^-1 psik3^-1  (his R3)", "-", B * kappa3 * inv(B) * inv(psik3)),
        ("F1", f"M lambda_alpha^({sgn(epsA)}),  lambda_alpha = A x", M * (A * x) ** epsA,
         "M (dirTaBase dirTaFib^n)^eA,  dirTaBase = A x,  dirTaFib = (r x)^-1",
         f"n = {N_}, eA = {sgn(epsA)}", M * (dirTaBase * dirTaFib ** N_) ** epsA),
        ("F2", f"N lambda_beta^({sgn(epsB)}),  lambda_beta = (r^-1 M r) B", N * (inv(r) * M * r * B) ** epsB,
         "N (dirTbBase dirTbFib^m)^eB,  dirTbBase = r^-1 M^(-e5) r B,  dirTbFib = s r^-1 s^-1",
         f"m = {M_}, e5 = {sgn(E5)}, eB = {sgn(epsB)}", N * (dirTbBase * dirTbFib ** M_) ** epsB),
    ]


def main():
    cs.verify_sources()
    print("generator dictionary (ours -> Wuebben's): x->x  y->y  r->r  s->s  A->A  B->B  M->M  N->N")
    print("commutator convention in both: [u,v] = u v u^-1 v^-1;  loops compose left to right in both")
    print(f"located member: (m,n) = ({M_},{N_});  relation signs e3={sgn(E3)} e4={sgn(E4)} e5={sgn(E5)};"
          "  (eA,eB) = (eps_A,eps_B)")
    print()

    bad = 0
    for epsA, epsB in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        tag = f"({'+' if epsA==1 else '-'},{'+' if epsB==1 else '-'})"
        table = rows(epsA, epsB)
        mine = cs.ours(epsA, epsB)
        his = cs.wuebben_decide2(M_, N_, E3, E4, E5, epsA, epsB)
        his_fixed = cs.wuebben_fixed_v(FIXED_V["pAs"], FIXED_V["pBy"], FIXED_V["pBs"], FIXED_V["deltaBs"],
                                       FIXED_V["deltaF"], FIXED_V["eta"], FIXED_V["pF"],
                                       E3, E4, E5, epsA, epsB, FIXED_V["section"])
        print(f"=== sheet {tag}: relation by relation ===")
        print(f"  {'':4} {'ours':46} {'reduced relator':22} {'Wuebben decide2.g form':84} {'parameter':28} equal")
        for label, name, mine_w, his_form, param, his_w in table:
            eq = mine_w == his_w
            bad += not eq
            print(f"  {label:4} {name:46} {mine_w!r:22} {his_form:84} {param:28} {'yes' if eq else 'NO'}")
        # The row-by-row words must also reproduce both transcribed systems as multisets.
        row_words = [t[2] for t in table]
        ok1 = cs.same_multiset(row_words, mine)
        ok2 = cs.same_multiset(row_words, his)
        ok3 = cs.same_multiset(row_words, his_fixed)
        bad += (not ok1) + (not ok2) + (not ok3)
        print(f"  rows reproduce ours(): {ok1};  decide2.g at ({M_},{N_}): {ok2};  fixed_v_certify.g at the located point: {ok3}")
        a = sorted(repr(w) for w in mine)
        b = sorted(repr(w) for w in his)
        diff = list(difflib.unified_diff(a, b, "ours", "wuebben_decide2(0,0)", lineterm="", n=0))
        print(f"  unified diff of sorted relator lists: {'EMPTY' if not diff else chr(10).join(diff)}")
        bad += bool(diff)
        print()

    print("Wuebben's shift family in these letters (decide2.g):")
    print("  lambda_alpha(n) = A x . ((r x)^-1)^n")
    print("  lambda_beta(m)  = (r^-1 M r) B . (s r^-1 s^-1)^m        (at e5 = -1)")
    print("  V_aud's longitudes are the n = 0 and m = 0 members; no offset.")
    print("  Note: an outside 2026-09-01 grid shifted lambda_beta by r^m instead of (s r^-1 s^-1)^m;")
    print("  those are different words away from m = 0 and agree with his only at m = 0.")
    print()
    print("fixed_v_certify.g point: section y1/Ax; corrections for (As, By, Bs, F) all left-placed;")
    print("  deltaBs = deltaF = r^-1; eta = +1; beta correction before B.")
    print()
    if bad:
        print("RESULT: FAIL")
        raise SystemExit(1)
    print("RESULT: PASS - twelve of twelve relators agree letter for letter in all four sheets; the diff is empty")


if __name__ == "__main__":
    main()
