exec(open('t4_test.py').read().split('gap = P.gap_setup')[0])
from tietze import simplify, renumber
live, rels, ws = simplify(P.ngens, P.relators, [mu, lam_f, lam_b])
m, rels, (mu, lam_f, lam_b) = renumber(live, rels, ws)
print("reduced: ", m, "gens", len(rels), "relators; mu =", mu, "lf =", lam_f, "lb =", lam_b)
gw = lambda w: "One(F)" if not w else "*".join(f"F.{abs(g)}"+("^-1" if g<0 else "") for g in w)
gap = f"F := FreeGroup({m});;\nrels := [{','.join(gw(r) for r in rels)}];;\nG := F/rels;;\n"
gap += f"mu := {gw(mu)};;  lf := {gw(lam_f)};;  lb := {gw(lam_b)};;\n" + open('t4_gap_tail.g').read()
open("t4.g","w").write(gap)
out = subprocess.run(["gap","-q","t4.g"], input="", capture_output=True, text=True, timeout=600)
print(out.stdout[-4000:], out.stderr[-800:])
