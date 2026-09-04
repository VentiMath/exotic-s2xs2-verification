#!/usr/bin/env python3
"""Numerical search for nontrivial SL(3,C) representations of the reduced honest groups."""
import json, random, sys
import numpy as np
SRC = "/Users/johnclyde/exotic-s2xs2-verification/verification/luttinger/honest_filling/reduced_presentations.json"
cases = json.load(open(SRC))
ONLY = sys.argv[1:] or list(cases)
N = 3
I3 = np.eye(N, dtype=complex)

def unpack(p):
    c = p[0::2] + 1j*p[1::2]
    a = c[:N*N].reshape(N,N); b = c[N*N:].reshape(N,N)
    return a, b

def residual(p, rels):
    a, b = unpack(p)
    try:
        ai, bi = np.linalg.inv(a), np.linalg.inv(b)
    except np.linalg.LinAlgError:
        return np.full(2*(2+len(rels)*N*N), 1e3)
    g = {1:a, -1:ai, 2:b, -2:bi}
    out = [np.linalg.det(a)-1, np.linalg.det(b)-1]
    for r in rels:
        M = I3
        for i in r: M = M @ g[i]
        out += list((M - I3).ravel())
    v = np.array(out)
    return np.concatenate([v.real, v.imag])

def solve(p, rels, iters=80):
    lam = 1e-3
    r = residual(p, rels); f = r @ r
    n = len(p)
    for _ in range(iters):
        J = np.empty((len(r), n)); h = 1e-7
        for k in range(n):
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
    rng = random.Random(777)
    best = []
    for start in range(60):
        p = np.array([rng.gauss(0,1) for _ in range(4*N*N)])
        p, f = solve(p, rels)
        a, b = unpack(p)
        # distance from a scalar (central) pair: image of a perfect group is perfect, so central => trivial
        dist = min(np.abs(a - w*I3).sum() + np.abs(b - w2*I3).sum() for w in np.exp(2j*np.pi*np.arange(3)/3) for w2 in np.exp(2j*np.pi*np.arange(3)/3))
        best.append((f, dist, np.trace(a), np.trace(b), np.trace(a@b)))
        if f < 1e-16 and dist > 1e-4:
            print(f"{name} start={start} NONTRIVIAL residual={f:.2e} tr(a)={np.trace(a):.6f} tr(b)={np.trace(b):.6f} tr(ab)={np.trace(a@b):.6f}", flush=True)
    best.sort(key=lambda t: t[0])
    nontriv = sorted([t for t in best if t[1] > 1e-4], key=lambda t: t[0])
    print(f"{name}: best residual overall {best[0][0]:.2e} (dist from center {best[0][1]:.2e}); best nontrivial residual {nontriv[0][0]:.2e} tr(a)={nontriv[0][2]:.4f} tr(b)={nontriv[0][3]:.4f}" if nontriv else f"{name}: all starts converged to central", flush=True)
print("SL3 SEARCH DONE", flush=True)
