# Part D, second pass: is M trivial in the abelianisation of some finite-index subgroup of Q
# (i.e. nontrivial in H_1 of a finite cover)?  M lies in every subgroup of index <= 5, so it
# lies in each of these; we test its image in U/[U,U].
Read("q_input.g");
hom := GroupHomomorphismByImages(F, Q, GeneratorsOfGroup(F), GeneratorsOfGroup(Q));;
Mq := Image(hom, Mw);; Bq := Image(hom, Bw);; Nq := Image(hom, Nw);;
L := LowIndexSubgroupsFpGroup(Q, 5);;
found := false;;
for U in L do
  if Index(Q, U) = 1 then continue; fi;
  iso := IsomorphismFpGroup(U);;
  UU := Range(iso);;
  ab := MaximalAbelianQuotient(UU);;
  m := Image(ab, Image(iso, Mq));; c := Image(ab, Image(iso, Comm(Bq, Mq)));; n := Image(ab, Image(iso, Nq));;
  Print("index ", Index(Q, U), "  H1(U) = ", AbelianInvariants(UU), "  M trivial in H1(U)? ", IsOne(m), "  [B,M] trivial? ", IsOne(c), "  N trivial? ", IsOne(n), "\n");
  if not IsOne(m) then found := true; Print("  ==> M IS NONTRIVIAL IN Q (survives in H_1 of an index-", Index(Q,U), " cover)\n"); fi;
od;
Print("M nontrivial in H1 of some cover to index 5: ", found, "\n");
QUIT;
