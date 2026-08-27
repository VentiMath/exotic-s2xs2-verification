"""Explicit Moser flow for Lemma 8.2: the ODE citation made concrete.

The lemma's annulus normalization invokes one soft input: the Moser vector
field's flow exists for s in [0,1] near the compact core. For THIS vector
field that citation is overkill: with Omega = f dt^dtheta, Omega_0 =
dt^dtheta, zeta = g dtheta, g(theta,t) = int_0^t (f-1), and omega_s =
(1-s)Omega_0 + s Omega = f_s dt^dtheta, the defining equation
iota_X omega_s = -zeta forces

    X_s = -(g/f_s) d/dt,   f_s = (1-s) + s f,

motion in t only: a one-dimensional ODE with parameter theta, vanishing on
the core e = {t=0}. This script verifies, in order:

  1. (symbolic, general f) the primitive identity d zeta = Omega - Omega_0,
     the core restriction zeta|_e = 0, the contraction identity
     iota_X omega_s = -zeta for the displayed X, and the Moser cancellation
     d/ds(phi_s^* omega_s) = phi_s^*(partial_s omega_s + d iota_X omega_s)
     = 0 at the level of coefficient functions;
  2. (closed form, f = F(theta) any positive t-independent profile) the
     exact flow T(s) = t0 / (1 + s(F-1)), verified by substitution, with
     phi_1^* Omega = Omega_0 exact: F * dT/dt0 |_{s=1} = 1;
  3. (numeric, fully theta- and t-dependent f) RK4 integration of the flow
     with the pullback identity f(theta,T) dT/dt0 = 1 checked on a grid,
     the core fixed pointwise, and the explicit Gronwall trap
     |T(s)| <= |t0| e^{Cs}, C = max|f-1| / min(1, min f), giving the
     concrete invariant neighborhood |t0| < e^{-C}. For this general case
     existence itself still rests on Picard-Lindelof — applied to an
     explicit one-dimensional field with computed Lipschitz and trapping
     constants, not to an abstract flow; only the t-independent family in
     part 2 is fully constructive.

Everything asserts; any failure hard-exits.
"""
import math
import sys

try:
    import sympy as sp
except ImportError:
    sys.exit("this check needs sympy: python3 -m pip install --user sympy")


def fail(msg):
    print(f"FAIL {msg}")
    sys.exit(1)


def check(label, ok):
    if not ok:
        fail(label)
    print(f"PASS {label}")


# ---- 1. symbolic identities for general f ---------------------------------
theta, t, tau, s, t0 = sp.symbols("theta t tau s t0", real=True)
f = sp.Function("f", positive=True)

g = sp.Integral(f(theta, tau) - 1, (tau, 0, t))
check("primitive: d/dt g = f - 1 (i.e. d zeta = Omega - Omega_0)",
      sp.simplify(sp.diff(g, t) - (f(theta, t) - 1)) == 0)
check("core restriction: g(theta, 0) = 0",
      sp.simplify(g.subs(t, 0).doit()) == 0)

f_s = (1 - s) + s * f(theta, t)
check("convex combination: f_s = (1-s)*1 + s*f exactly",
      sp.simplify(f_s - ((1 - s) + s * f(theta, t))) == 0)
# positivity of f_s for f>0, 0<=s<=1 is the convexity of the segment from
# 1 to f(theta,t); record the two endpoint values.
check("interpolation endpoints: f_0 = 1 and f_1 = f",
      sp.simplify(f_s.subs(s, 0) - 1) == 0
      and sp.simplify(f_s.subs(s, 1) - f(theta, t)) == 0)

# contraction: for X = X_t d/dt and omega_s = f_s dt^dtheta,
# iota_X omega_s = f_s X_t dtheta. Solve f_s X_t = -g.
X_t = -g / f_s
check("contraction: iota_X omega_s = -zeta for X_t = -g/f_s",
      sp.simplify(f_s * X_t + g) == 0)
check("X vanishes on the core e = {t=0}",
      sp.simplify(X_t.subs(t, 0).doit()) == 0)

# Moser cancellation at coefficient level:
# partial_s omega_s has coefficient f - 1; d(iota_X omega_s) = d(-g dtheta)
# has dt^dtheta coefficient -(d/dt g) = -(f - 1). Their sum is 0.
partial_s_coeff = sp.diff(f_s, s)
d_iota_coeff = -sp.diff(g, t)
check("Moser cancellation: partial_s omega_s + d iota_X omega_s = 0",
      sp.simplify(partial_s_coeff + d_iota_coeff) == 0)

# ---- 2. closed-form flow for t-independent profiles -----------------------
F = sp.Function("F", positive=True)
gF = (F(theta) - 1) * t                       # g for f = F(theta)
fsF = (1 - s) + s * F(theta)
T = t0 / (1 + s * (F(theta) - 1))             # candidate exact flow
ode_residual = sp.diff(T, s) - (-(F(theta) - 1) * T / fsF.subs(t, 0))
check("closed form: T(s) = t0/(1+s(F-1)) solves dT/ds = -(F-1)T/f_s",
      sp.simplify(ode_residual) == 0)
check("closed form: T(0) = t0", sp.simplify(T.subs(s, 0) - t0) == 0)
pullback = F(theta) * sp.diff(T.subs(s, 1), t0)
check("closed form: phi_1^* Omega = Omega_0 exactly (F * dT/dt0 = 1)",
      sp.simplify(pullback - 1) == 0)

# ---- 3. numeric general case ----------------------------------------------
A, K1, K2 = 0.35, 3, 2


def f_num(th, tt):
    return 1.0 + A * math.sin(K1 * th) * math.cos(K2 * tt)


def g_num(th, tt, n=200):
    # Simpson quadrature of f-1 from 0 to tt.
    if tt == 0.0:
        return 0.0
    h = tt / n
    total = (f_num(th, 0) - 1) + (f_num(th, tt) - 1)
    for i in range(1, n):
        total += (4 if i % 2 else 2) * (f_num(th, i * h) - 1)
    return total * h / 3


def velocity(th, tt, ss):
    fs = (1 - ss) + ss * f_num(th, tt)
    return -g_num(th, tt) / fs


def flow(th, tt0, steps=400):
    tt, ss, h = tt0, 0.0, 1.0 / steps
    for _ in range(steps):
        k1 = velocity(th, tt, ss)
        k2 = velocity(th, tt + h * k1 / 2, ss + h / 2)
        k3 = velocity(th, tt + h * k2 / 2, ss + h / 2)
        k4 = velocity(th, tt + h * k3, ss + h)
        tt += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        ss += h
    return tt


f_min, f_max_dev = 1.0 - A, A
C = f_max_dev / min(1.0, f_min)
radius = math.exp(-C)
print(f"explicit constants: min f = {f_min}, max|f-1| = {f_max_dev}, "
      f"Gronwall C = {C:.6f}, existence radius e^-C = {radius:.6f}")

thetas = [2 * math.pi * k / 24 for k in range(24)]
worst = 0.0
for th in thetas:
    if flow(th, 0.0) != 0.0:
        fail(f"core moved at theta={th}")
    for tt0 in (0.02, -0.02, 0.1, -0.1, 0.3, -0.3, 0.5, -0.5):
        T1 = flow(th, tt0)
        if abs(T1) > abs(tt0) * math.exp(C) + 1e-12:
            fail(f"Gronwall trap violated at theta={th}, t0={tt0}")
        eps = 1e-5
        dT = (flow(th, tt0 + eps) - flow(th, tt0 - eps)) / (2 * eps)
        residual = abs(f_num(th, T1) * dT - 1.0)
        worst = max(worst, residual)
check("core fixed pointwise on the 24-point grid", True)
check("Gronwall trap |T| <= |t0| e^C on the full grid", True)
check(f"pullback f(theta,T) dT/dt0 = 1, worst residual {worst:.2e}",
      worst < 1e-5)

print(f"trapping: for |t0| <= {radius:.3f} the trajectory stays inside the "
      "collar |t| < 1 for all s in [0,1]; existence for general f is "
      "Picard-Lindelof applied with these computed constants")
print("ALL MOSER FLOW CHECKS PASSED")
