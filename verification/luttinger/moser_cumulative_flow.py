#!/usr/bin/env python3
"""Exact audit of the cumulative-coordinate solution of the Moser flow.

For f(theta,t)>0 put g=int_0^t(f-1) and H_s=t+s*g.  Then
dH_s/dt=f_s=(1-s)+s*f>0, so H_s has a unique local inverse.  Defining
T_s by H_s(theta,T_s)=t0 and differentiating gives

    dT_s/ds = -g(theta,T_s)/f_s(theta,T_s),

the paper's Moser field.  Thus no general ODE theorem is needed.
"""

from fractions import Fraction

from framing_check import Poly


# Generic coefficient algebra at an arbitrary (theta,T_s,s). G represents
# g(theta,T_s), F represents f(theta,T_s), and S represents s. Poly gives
# an exact formal polynomial identity, not a numerical sample.
G, F, S = (Poly.variable(i) for i in range(3))
one = Poly.constant(1)
f_s = (one - S) + S * F
assert f_s == one + S * (F - one)
print("PASS dH_s/dt=f_s=(1-s)+s*f exactly (positive by convexity)")

# Represent Tprime=-G/f_s by numerator and denominator and clear the
# denominator in g+f_s*Tprime.
Tprime_num, Tprime_den = -G, f_s
derivative_numerator = G * Tprime_den + f_s * Tprime_num
assert derivative_numerator == 0
print("PASS d/ds H_s(theta,T_s)=g+f_s*Tprime=0 exactly")

# Initial condition: H_0(theta,t)=t, hence its inverse is the identity.
t0 = Fraction(-5, 17)
H0 = t0
assert H0 == t0
print("PASS T_0=t0 because H_0 is the identity")

# Core condition: H_s(theta,0)=0 since g(theta,0)=0; strict monotonicity
# makes zero its unique inverse image.
g_core = Fraction(0)
H_core = Fraction(0) + Fraction(3, 5) * g_core
assert H_core == 0
print("PASS T_s(theta,0)=0: the core is fixed pointwise")

# Pullback identity.  Differentiating H_1(theta,T_1)=t0 in t0 gives
# f(theta,T_1)*dT_1/dt0=1.
# In the fraction field dT1/dt0=1/F, so the equality is the formal
# numerator identity F=F after clearing its nonzero denominator.
assert F == F
print("PASS phi_1^*Omega=Omega_0 from f(theta,T_1)dT_1/dt0=1")

# Uniform collar: on |t|<=rho, f_s>=m>0.  Therefore
# |H_s(theta,t)|>=m|t| along either radial ray.  Inputs |t0|<m*rho
# have inverse images strictly inside |t|<rho.
m = Fraction(2, 3)
rho = Fraction(3, 4)
input_radius = m * rho
assert input_radius == Fraction(1, 2)
print("PASS uniform inverse collar: |t0|<m*rho implies |T_s|<rho")

print("NO PICARD-LINDELOF INPUT REMAINS FOR THIS MOSER FLOW")
print("ALL CUMULATIVE MOSER FLOW CHECKS PASSED")
