"""Exact first-jet audit for Weinstein-chart framing independence.

The proof is in notes/lemma82_chart_independence_2026-08-26.md.  This checks
its coordinate algebra without an external symbolic package.  A
symplectomorphism germ of T^*T fixing the zero section has first jet
[I,A;0,I], A symmetric.  Fiber dilation gives [I,tA;0,I], still symplectic
and limiting to the identity, with identity action on the normal quotient.
"""

from fractions import Fraction


class Poly:
    """Tiny exact polynomial ring Q[a,b,c,t]."""

    def __init__(self, terms=()):
        self.terms = {m: Fraction(v) for m, v in dict(terms).items() if v}

    def __add__(self, other):
        other = as_poly(other)
        out = dict(self.terms)
        for monomial, value in other.terms.items():
            out[monomial] = out.get(monomial, 0) + value
            if not out[monomial]:
                del out[monomial]
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -v for m, v in self.terms.items()})

    def __sub__(self, other):
        return self + (-as_poly(other))

    def __rsub__(self, other):
        return as_poly(other) - self

    def __mul__(self, other):
        other = as_poly(other)
        out = {}
        for left, lv in self.terms.items():
            for right, rv in other.terms.items():
                monomial = tuple(x + y for x, y in zip(left, right))
                out[monomial] = out.get(monomial, 0) + lv * rv
        return Poly(out)

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.terms == as_poly(other).terms


def as_poly(value):
    if isinstance(value, Poly):
        return value
    return Poly({(0, 0, 0, 0): Fraction(value)})


def variable(index):
    monomial = [0, 0, 0, 0]
    monomial[index] = 1
    return Poly({tuple(monomial): 1})


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def multiply(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(len(right)))
             for j in range(len(right[0]))]
            for i in range(len(left))]


def equal(left, right):
    return all(left[i][j] == right[i][j]
               for i in range(len(left)) for j in range(len(left[0])))


def at_t_zero(entry):
    return Poly({m: value for m, value in entry.terms.items() if m[3] == 0})


zero, one = as_poly(0), as_poly(1)
a, b, c, t = (variable(i) for i in range(4))
I = [[one, zero], [zero, one]]
Z = [[zero, zero], [zero, zero]]
A = [[a, b], [b, c]]


def blocks(top_left, top_right, bottom_left, bottom_right):
    return [top_left[0] + top_right[0], top_left[1] + top_right[1],
            bottom_left[0] + bottom_right[0],
            bottom_left[1] + bottom_right[1]]


# Coordinates (q1,q2,p1,p2), omega = dp_i wedge dq_i.
J = blocks(Z, [[-one, zero], [zero, -one]], I, Z)
M = blocks(I, A, Z, I)
Mt = blocks(I, [[t * x for x in row] for row in A], Z, I)
Id = blocks(I, Z, Z, I)

assert equal(multiply(multiply(transpose(M), J), M), J)
print("PASS symmetric shear first jet is symplectic")
assert equal(multiply(multiply(transpose(Mt), J), Mt), J)
print("PASS fiber-dilation path [I,tA;0,I] is symplectic exactly")
assert equal([[at_t_zero(x) for x in row] for row in Mt], Id)
print("PASS dilation path limits to the identity at t=0")
assert all(M[2 + i][2 + j] == I[i][j]
           for i in range(2) for j in range(2))
print("PASS induced normal-quotient map is the identity")
print("ALL WEINSTEIN CHART-INDEPENDENCE FIRST-JET CHECKS PASSED")
