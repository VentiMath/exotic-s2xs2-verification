Read("generation_input.g");
Q := F / rels;;
hom := GroupHomomorphismByImages(F, Q, GeneratorsOfGroup(F), GeneratorsOfGroup(Q));;
cands := rec(
  sheet_BxBi_y := w_B*w_x*w_B^-1*w_y,   # sheet: B x B^-1 = y^-1
  BxBi_yi      := w_B*w_x*w_B^-1*w_y^-1,
  BixB_y       := w_B^-1*w_x*w_B*w_y,
  BixB_yi      := w_B^-1*w_x*w_B*w_y^-1,
  ctrl_ByBi    := w_B*w_y*w_B^-1*(w_M^-1*w_y*w_x)^-1,   # certified identity, control
  ctrl_AxAi    := w_A*w_x*w_A^-1*w_r^-1 );;
names := RecNames(cands);;
Print("H1(Q) = ", AbelianInvariants(Q), "\n");
ab := MaximalAbelianQuotient(Q);;
for n in names do
  Print("  abelianization image of ", n, " trivial: ", IsOne(Image(ab, Image(hom, cands.(n)))), "\n");
od;
tests := [ ["A5", AlternatingGroup(5)], ["PSL(2,7)", PSL(2,7)], ["A6", AlternatingGroup(6)], ["PSL(2,8)", PSL(2,8)],
           ["PSL(2,11)", PSL(2,11)], ["PSL(2,13)", PSL(2,13)], ["A7", AlternatingGroup(7)], ["PSL(3,3)", PSL(3,3)],
           ["S3", SymmetricGroup(3)], ["S4", SymmetricGroup(4)], ["D8", DihedralGroup(8)], ["Q8", QuaternionGroup(8)],
           ["S5", SymmetricGroup(5)], ["SL(2,3)", SL(2,3)], ["C3xS3", DirectProduct(CyclicGroup(3),SymmetricGroup(3))] ];;
for t in tests do
  epis := GQuotients(Q, t[2]);
  Print(t[1], ": ", Length(epis), " quotient(s)");
  if Length(epis) > 0 then
    for n in names do
      Print("; ", n, ":", List(epis, e -> IsOne(Image(e, Image(hom, cands.(n))))));
    od;
  fi;
  Print("\n");
od;
QUIT;
