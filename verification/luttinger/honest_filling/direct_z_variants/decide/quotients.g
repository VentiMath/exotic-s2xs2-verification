Read("double_derived.g");
iso := IsomorphismSimplifiedFpGroup(G);; H := Image(iso);;
Print("simplified: ", Length(GeneratorsOfGroup(H)), " gens, ", Length(RelatorsOfFpGroup(H)), " rels\n");
sxo := StoredExcludedOrders(H);; for i in [1..Length(sxo)] do UniteSet(sxo[i][2], [1..200]); od;
T := [ ["A5",AlternatingGroup(5)], ["L2_7",PSL(2,7)], ["A6",AlternatingGroup(6)], ["L2_8",PSL(2,8)],
       ["L2_11",PSL(2,11)], ["L2_13",PSL(2,13)], ["L2_17",PSL(2,17)], ["A7",AlternatingGroup(7)],
       ["L2_19",PSL(2,19)], ["L2_16",PSL(2,16)], ["L3_3",PSL(3,3)], ["U3_3",PSU(3,3)], ["L2_23",PSL(2,23)],
       ["L2_25",PSL(2,25)], ["M11",MathieuGroup(11)], ["L2_27",PSL(2,27)], ["L2_29",PSL(2,29)], ["L2_31",PSL(2,31)],
       ["A8",AlternatingGroup(8)] ];;
for t in T do
  t0 := Runtime();
  q := CALL_WITH_CATCH(GQuotients, [H, t[2]]);
  if q[1] and Length(q[2]) > 0 then Print(">>> NONTRIVIAL: onto ", t[1], " (", Length(q[2]), " maps)  ", Int((Runtime()-t0)/1000), "s\n");
  elif q[1] then Print("no quotient onto ", t[1], "  ", Int((Runtime()-t0)/1000), "s\n");
  else Print(t[1], " ERRORED  ", Int((Runtime()-t0)/1000), "s\n"); fi;
od;
Print("quotients done\n"); QUIT_GAP(0);
