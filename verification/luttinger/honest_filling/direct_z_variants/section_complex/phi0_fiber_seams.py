"""Certify the four fiber seams of the double as literal based paths in the audit fiber:
sigma_aud acts on the fiber over q by phi_0, and the seams are x_L = r_R, y_L = s_R, r_L = x_R, s_L = y_R.
paper_bridge.build_paper_loops already asserts phi_0(x) = r and phi_0(y) = s vertexwise; here the other two
directions and phi_0^2 = id on every fiber vertex are checked the same way."""
import sys, os
sys.path.insert(0, os.path.expanduser('~/luttinger/direct-z-integration/verification/luttinger'))
from fiber import build_fiber
from paper_bridge import build_paper_loops
F = build_fiber(); phi0 = F['phi0']; L = F['L']
loops = build_paper_loops(F)
verts = {v for s in L.simplices[0] for v in s}
inv = all(phi0[phi0[v]] == v for v in verts)
print('phi_0 is an involution on all', len(verts), 'fiber vertices:', inv)
print('phi_0 fixes p:', phi0['p'] == 'p')
for a, b in (('x', 'r'), ('y', 's'), ('r', 'x'), ('s', 'y')):
    ok = [phi0[v] for v in loops[a]] == loops[b]
    print(f'phi_0({a}) = {b} as literal based edge paths (length {len(loops[a])-1}):', ok)
