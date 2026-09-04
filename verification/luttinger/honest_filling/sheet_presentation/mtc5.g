Read("generation_input.g");
Q := F / rels;;
hom := GroupHomomorphismByImages(F, Q, GeneratorsOfGroup(F), GeneratorsOfGroup(Q));;
sheetimgs := List([w_x, w_y, w_r, w_s, w_A, w_B, w_M, w_N], w -> Image(hom, w));;
iso := IsomorphismFpGroupByGenerators(Q, sheetimgs, "h");;
P := Range(iso);; FP := FreeGroupOfFpGroup(P);; h := GeneratorsOfGroup(FP);;
x:=h[1];; y:=h[2];; r:=h[3];; s:=h[4];; A:=h[5];; B:=h[6];; M:=h[7];; N:=h[8];;
Prels := RelatorsOfFpGroup(P);;
certified := [ A*x*A^-1*r^-1, A*y*A^-1*s^-1, A*r*A^-1*x^-1, A*s*A^-1*(N*y)^-1,
               B*y*B^-1*(M^-1*y*x)^-1, B*r*B^-1*r^-1, B*s*B^-1*(r^-1*M^-1*r*s)^-1, x*y*x^-1*y^-1*r*s*r^-1*s^-1 ];;
lb := r^-1*M*r*B;;
alphas := rec( y1 := [M, A*x], y2 := [y^-1*M*y, y^-1*A*r^-1*y] );;
enum := function(base, pkg, beta, eA, eB, cap)
  local alpha, fill, tab;
  alpha := alphas.(pkg);
  if beta = "honest" then fill := [ alpha[1]*alpha[2]^eA, A^-1*N*A*lb^eB ]; else fill := [ alpha[1]*alpha[2]^eA, N*lb^eB ]; fi;
  tab := CosetTableFromGensAndRels(h, Concatenation(base, fill), [] : max := cap, silent := true);
  if tab = fail then return "overflow"; fi; return Length(tab[1]);
end;;
for pkg in ["y1", "y2"] do for beta in ["sealed", "honest"] do
  Print("P+cert8 ", pkg, " ", beta, ": ", List([[1,1],[1,-1],[-1,1],[-1,-1]], e -> enum(Concatenation(Prels, certified), pkg, beta, e[1], e[2], 2000000)), "\n");
od; od;
# minimal subsets of P relators (greedy removal) that keep all eight honest cases collapsing
allok := function(base) local pkg, e; for pkg in ["y1","y2"] do for e in [[1,1],[1,-1],[-1,1],[-1,-1]] do if enum(base, pkg, "honest", e[1], e[2], 300000) <> 1 then return false; fi; od; od; return true; end;;
need := ShallowCopy(Prels);;
for i in [Length(Prels), Length(Prels)-1 .. 1] do
  trial := Filtered(need, rr -> rr <> Prels[i]);
  if allok(Concatenation(trial, certified)) then need := trial; fi;
od;
Print("minimal P relators needed (", Length(need), "):\n"); for rr in need do Print("  ", rr, "\n"); od;
# can any certified relation be dropped too?
need2 := ShallowCopy(certified);;
for i in [Length(certified), Length(certified)-1 .. 1] do
  trial := Filtered(need2, rr -> rr <> certified[i]);
  if allok(Concatenation(need, trial)) then need2 := trial; fi;
od;
Print("certified sheet relations still needed (", Length(need2), "):\n"); for rr in need2 do Print("  ", rr, "\n"); od;
Print("final check all eight honest cases with minimal set: ", allok(Concatenation(need, need2)), "\n");
PrintTo("needed_relators.txt", Concatenation(List(need, String), List(need2, String)));
QUIT;
