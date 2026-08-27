F := FreeGroup(4);;
rels := [F.3*F.2*F.3^-1*F.2^-1,F.4^-1*F.2*F.1*F.2^-1*F.4*F.1^-1,F.1^-1*F.2*F.1*F.2^-1,F.1^-1*F.4*F.1*F.4^-1,F.1^-1*F.3*F.2*F.1*F.3^-1*F.2^-1,F.1^-1*F.3*F.2*F.3^-1*F.1*F.2^-1,F.1^-1*F.2^-1*F.1*F.4^-1*F.2*F.3*F.4*F.3^-1,F.4^-1*F.3*F.2*F.1*F.3^-1*F.2^-1*F.4*F.1^-1,F.1*F.4^-1*F.1^-1*F.4,F.3*F.1*F.3^-1*F.1^-1,F.1*F.3^-1*F.2^-1*F.4*F.1^-1*F.2*F.3*F.4^-1,F.3^-1*F.2^-1*F.4*F.1^-1*F.2*F.1*F.3*F.4^-1,F.2^-1*F.4*F.1^-1*F.2*F.3*F.4^-1*F.1*F.3^-1,F.2^-1*F.3*F.2*F.3^-1,F.3*F.2*F.1^-1*F.2^-1*F.3^-1*F.1,F.4*F.1*F.4^-1*F.1^-1,F.3*F.1^-1*F.3^-1*F.1,F.2^-1*F.1^-1*F.2*F.1,F.3*F.4^-1*F.1*F.3^-1*F.2^-1*F.4*F.1^-1*F.2,F.2^-1*F.4*F.1^-1*F.2*F.1*F.2^-1*F.1*F.4^-1*F.2*F.1^-1,F.3*F.2^-1*F.3^-1*F.1*F.2*F.1^-1,F.1^-1*F.2^-1*F.1*F.4^-1*F.2*F.1*F.2^-1*F.4*F.1^-1*F.2,F.2^-1*F.4*F.1^-1*F.2*F.1*F.3*F.1^-1*F.4^-1*F.1*F.3^-1,F.1^-1*F.2^-1*F.1*F.4^-1*F.2*F.3*F.1^-1*F.4*F.1*F.3^-1,F.3*F.1^-1*F.2^-1*F.3^-1*F.1*F.2,F.3*F.2*F.1*F.3^-1*F.1^-1*F.2^-1,F.1^-1*F.2^-1*F.1*F.4^-1*F.2*F.3*F.4*F.1^-1*F.2*F.1*F.2^-1*F.3^-1,F.4^-1*F.1*F.3^-1*F.2^-1*F.4*F.1^-1*F.2*F.3,F.1*F.3^-1*F.1^-1*F.3,F.2^-1*F.1*F.2*F.1^-1,F.2*F.3*F.4^-1*F.2^-1*F.3^-1*F.4,F.4*F.1^-1*F.3^-1*F.2^-1*F.1*F.4^-1*F.2*F.3,F.3^-1*F.2^-1*F.1*F.4^-1*F.2*F.3*F.4*F.1^-1,F.2^-1*F.4*F.1^-1*F.2*F.1*F.3*F.4^-1*F.3^-1,F.1*F.3*F.2*F.1^-1*F.2^-1*F.3^-1,F.1*F.2*F.1^-1*F.2^-1,F.2*F.1^-1*F.2^-1*F.1*F.4^-1*F.2*F.3*F.2^-1*F.3^-1*F.4,F.3^-1*F.2^-1*F.4*F.1^-1*F.2*F.1*F.2^-1*F.1^-1*F.3*F.2*F.1*F.4^-1,F.2^-1*F.4*F.1^-1*F.2*F.1*F.2^-1*F.4^-1*F.3*F.2*F.3^-1];;
G := F/rels;;
mu := F.2^-1*F.4*F.1^-1*F.2*F.1*F.4^-1;;  lf := F.3*F.2;;  lb := F.4*F.1*F.4^-1;;
fp := function(H) local L; L := LowIndexSubgroupsFpGroup(H, 4);
  return [AbelianInvariants(H), List([1..4], i -> Number(L, s -> Index(H, s) = i))]; end;;
Print("pi1(C) simplified gens: ", Length(GeneratorsOfGroup(SimplifiedFpGroup(G))), "\n");
Print("pi1(C): ", fp(G), "\n");
Z2F2 := FreeGroup(4);; Z2F2 := Z2F2/[Comm(Z2F2.1,Z2F2.2), Comm(Z2F2.1,Z2F2.3), Comm(Z2F2.1,Z2F2.4), Comm(Z2F2.2,Z2F2.3), Comm(Z2F2.2,Z2F2.4)];;
Print("Z^2xF_2: ", fp(Z2F2), "\n");
Print("pi1(C)/<<mu>>: ", fp(F/Concatenation(rels,[mu])), "\n");
Z4 := FreeGroup(4);; Z4 := Z4/List(Combinations([1..4],2), p -> Comm(Z4.(p[1]), Z4.(p[2])));;
Print("Z^4: ", fp(Z4), "\n");
for e in [1,-1] do
  Print("surgery mu*lf^", e, ": ", fp(F/Concatenation(rels,[mu*lf^e])), "\n");
  Print("surgery mu*lb^", e, ": ", fp(F/Concatenation(rels,[mu*lb^e])), "\n");
od;
Fexp := FreeGroup("x","y","a","b");; xx:=Fexp.1;;yy:=Fexp.2;;aa:=Fexp.3;;bb:=Fexp.4;;
for e in [1,-1] do
  Print("expected (dir x, k=",e,"): ", fp(Fexp/[Comm(xx,yy),Comm(aa,bb),Comm(xx,aa),Comm(yy,aa),Comm(xx,bb),Comm(yy,bb)*xx^e]), "\n");
  Print("expected (dir a, k=",e,"): ", fp(Fexp/[Comm(xx,yy),Comm(aa,bb),Comm(xx,aa),Comm(yy,aa),Comm(xx,bb),Comm(yy,bb)*aa^e]), "\n");
od;
