#!/usr/bin/env python3
"""Numerical search for nontrivial SL(2,C) representations of the reduced honest groups.
A nontrivial solution (a,b) != (I,I) with tiny residual is evidence the group is nontrivial."""
import json, random, sys, cmath
import numpy as np

SRC = "/Users/johnclyde/exotic-s2xs2-verification/verification/luttinger/honest_filling/reduced_presentations.json"
cases = json.load(open(SRC))
ONLY = sys.argv[1:] or list(cases)

def mul(X, Y):
    return (X[0]*Y[0]+X[1]*Y[2], X[0]*Y[1]+X[1]*Y[3], X[2]*Y[0]+X[3]*Y[2], X[2]*Y[1]+X[3]*Y[3])
def inv(X):  # adjugate / det
    dt = X[0]*X[3]-X[1]*X[2]
    return (X[3]/dt, -X[1]/dt, -X[2]/dt, X[0]/dt)
I2 = (1+0j, 0j, 0j, 1+0j)

def residual(p, rels):
    a = (complex(p[0],p[1]), complex(p[2],p[3]), complex(p[4],p[5]), complex(p[6],p[7]))
    b = (complex(p[8],p[9]), complex(p[10],p[11]), complex(p[12],p[13]), complex(p[14],p[15]))
    ai, bi = inv(a), inv(b)
    g = {1:a, -1:ai, 2:b, -2:bi}
    out = [a[0]*a[3]-a[1]*a[2]-1, b[0]*b[3]-b[1]*b[2]-1]
    for r in rels:
        M = I2
        for i in r: M = mul(M, g[i])
        out += [M[0]-1, M[1], M[2], M[3]-1]
    v = np.array(out)
    return np.concatenate([v.real, v.imag])

def solve(p, rels, iters=80):
    lam = 1e-3
    r = residual(p, rels); f = r @ r
    for _ in range(iters):
        J = np.empty((len(r), 16))
        h = 1e-7
        for k in range(16):
            q = p.copy(); q[k] += h
            J[:, k] = (residual(q, rels) - r) / h
        A = J.T @ J; gvec = J.T @ r
        while True:
            try:
                step = np.linalg.solve(A + lam*np.diag(np.diag(A)+1e-12), -gvec)
            except np.linalg.LinAlgError:
                lam *= 10; continue
            pn = p + step; rn = residual(pn, rels); fn = rn @ rn
            if fn < f:
                p, r, f = pn, rn, fn; lam = max(lam/3, 1e-12); break
            lam *= 10
            if lam > 1e8: return p, f
        if f < 1e-28: break
    return p, f

for name in ONLY:
    rels = cases[name]["relators"]
    rng = random.Random(12345)
    best = []
    for start in range(120):
        p = np.array([rng.gauss(0,1) for _ in range(16)])
        p, f = solve(p, rels)
        a = (complex(p[0],p[1]), complex(p[2],p[3]), complex(p[4],p[5]), complex(p[6],p[7]))
        b = (complex(p[8],p[9]), complex(p[10],p[11]), complex(p[12],p[13]), complex(p[14],p[15]))
        dist = sum(abs(a[i]-I2[i]) for i in range(4)) + sum(abs(b[i]-I2[i]) for i in range(4))
        distneg = sum(abs(a[i]+I2[i]) for i in range(4)) + sum(abs(b[i]+I2[i]) for i in range(4))
        tra, trb, trab = a[0]+a[3], b[0]+b[3], mul(a,b)[0]+mul(a,b)[3]
        best.append((f, dist, distneg, tra, trb, trab))
        if f < 1e-16 and dist > 1e-4 and distneg > 1e-4:
            print(f"{name} start={start} NONTRIVIAL residual={f:.2e} tr(a)={tra:.6f} tr(b)={trb:.6f} tr(ab)={trab:.6f}", flush=True)
    best.sort(key=lambda t: t[0])
    nontriv = [t for t in best if t[1] > 1e-4 and t[2] > 1e-4]
    nontriv.sort(key=lambda t: t[0])
    print(f"{name}: best residual overall {best[0][0]:.2e} (dist from I {best[0][1]:.2e}); best nontrivial residual {nontriv[0][0]:.2e} tr(a)={nontriv[0][3]:.4f} tr(b)={nontriv[0][4]:.4f} tr(ab)={nontriv[0][5]:.4f}" if nontriv else f"{name}: all starts converged to trivial", flush=True)
print("SL2 SEARCH DONE", flush=True)
