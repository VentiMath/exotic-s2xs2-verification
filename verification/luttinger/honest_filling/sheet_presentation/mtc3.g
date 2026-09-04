Read("generation_input.g");
Q := F / rels;;
hom := GroupHomomorphismByImages(F, Q, GeneratorsOfGroup(F), GeneratorsOfGroup(Q));;
sheetimgs := List([w_x, w_y, w_r, w_s, w_A, w_B, w_M, w_N], w -> Image(hom, w));;
iso := IsomorphismFpGroupByGenerators(Q, sheetimgs, "h");;
P := Range(iso);; FP := FreeGroupOfFpGroup(P);; h := GeneratorsOfGroup(FP);;
x:=h[1];; y:=h[2];; r:=h[3];; s:=h[4];; A:=h[5];; B:=h[6];; M:=h[7];; N:=h[8];;
Prels := RelatorsOfFpGroup(P);;
certified := [ A*x*A^-1*r^-1, A*y*A^-1*s^-1, A*r*A^-1*x^-1, A*s*A^-1*(N*y)^-1,
               B*y*B^-1*(M^-1*y*x)^-1, B*r*B^-1*r^-1, B*s*B^-1*(r^-1*M^-1*r*s)^-1, Comm(x,y)*Comm(r,s) ];;
xrel := [ B*x*B^-1*y ];;
la := A*x;; lb := r^-1*M*r*B;;
run := function(label, base, beta, cap)
  local eA, eB, fill, tab, out, t;
  out := [];
  for eA in [1,-1] do for eB in [1,-1] do
    if beta = "honest" then fill := [ M*la^eA, A^-1*N*A*lb^eB ]; else fill := [ M*la^eA, N*lb^eB ]; fi;
    t := Runtime();
    tab := CosetTableFromGensAndRels(h, Concatenation(base, fill), [] : max := cap, silent := true);
    if tab = fail then Add(out, Concatenation("overflow/", String(Runtime()-t), "ms"));
    else Add(out, Concatenation("index ", String(Length(tab[1])), "/", String(Runtime()-t), "ms")); fi;
  od; od;
  Print(label, " ", beta, ": ", out, "\n");
end;;
run("P only              ", Prels, "sealed", 2000000);
run("P only              ", Prels, "honest", 2000000);
run("P + certified8      ", Concatenation(Prels, certified), "sealed", 2000000);
run("P + certified8      ", Concatenation(Prels, certified), "honest", 2000000);
run("P + certified8 + x  ", Concatenation(Prels, certified, xrel), "honest", 2000000);
Print("P relators:\n"); for rr in Prels do Print("  ", rr, "\n"); od;
QUIT;
