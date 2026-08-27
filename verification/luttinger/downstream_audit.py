#!/usr/bin/env python3
"""Finite algebra checks used in the downstream 4-manifold audit.

This does not formalize Freedman theory, symplectic Kodaira dimension, or
Heegaard Floer theory.  It checks the elementary numerical and lattice claims
to which those theorems are applied in Theorem 1.2 of arXiv:2608.17267.
"""

from itertools import product


def square(form, v):
    return sum(v[i] * form[i][j] * v[j] for i in range(2) for j in range(2))


def pairing(form, u, v):
    return sum(u[i] * form[i][j] * v[j] for i in range(2) for j in range(2))


def check_even_section_forms():
    """[[0,1],[1,2n]] is integrally hyperbolic."""
    for n in range(-20, 21):
        q = ((0, 1), (1, 2 * n))
        f, g0 = (1, 0), (-n, 1)  # g0 = Gamma - n F
        assert square(q, f) == 0
        assert square(q, g0) == 0
        assert pairing(q, f, g0) == 1


def check_odd_section_forms():
    """[[0,1],[1,2n+1]] is integrally <1>+<-1>."""
    for n in range(-20, 21):
        q = ((0, 1), (1, 2 * n + 1))
        e = (-n, 1)       # Gamma - n F, square +1
        d = (n + 1, -1)   # F - e, square -1
        assert square(q, e) == 1
        assert square(q, d) == -1
        assert pairing(q, e, d) == 0


def check_square_zero_axes():
    """In H, a nonzero square-zero vector lies on one coordinate axis."""
    h = ((0, 1), (1, 0))
    for a, b in product(range(-50, 51), repeat=2):
        if (a, b) != (0, 0) and square(h, (a, b)) == 0:
            assert a == 0 or b == 0


def check_numerics():
    # Closed, simply connected Z with chi=4 has b2=2.
    chi_z, b1_z = 4, 0
    b2_z = chi_z - 2 + 2 * b1_z
    assert b2_z == 2

    # An unbranched k-cover of a genus-2 surface has genus k+1.
    for k in range(1, 101):
        chi_cover = k * (2 - 2 * 2)
        genus = 1 - chi_cover // 2
        assert genus == k + 1

    # Adjunction for a symplectic genus-2, square-zero fiber.
    genus_f, f_square = 2, 0
    canonical_pairing = 2 * genus_f - 2 - f_square
    assert canonical_pairing == 2


def main():
    check_even_section_forms()
    check_odd_section_forms()
    check_square_zero_axes()
    check_numerics()
    print("PASS: downstream Euler, lattice, square-zero, cover-genus, and adjunction checks")


if __name__ == "__main__":
    main()
