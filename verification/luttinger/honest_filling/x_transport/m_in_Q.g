# Part D: is the alpha meridian M nontrivial in Q = pi_1(C_aud)?
Read("q_input.g");
hom := GroupHomomorphismByImages(F, Q, GeneratorsOfGroup(F), GeneratorsOfGroup(Q));;
Mq := Image(hom, Mw);; Nq := Image(hom, Nw);; Bq := Image(hom, Bw);;
Print("AbelianInvariants(Q) = ", AbelianInvariants(Q), "\n");
ab := MaximalAbelianQuotient(Q);;
Print("image of M in Q^ab: ", Image(ab, Mq), "  trivial? ", IsOne(Image(ab, Mq)), "\n");
Print("image of N in Q^ab: ", Image(ab, Nq), "  trivial? ", IsOne(Image(ab, Nq)), "\n");
Print("image of [B,M] in Q^ab trivial? ", IsOne(Image(ab, Comm(Bq, Mq))), "\n");
# exponent-sum vectors of the sheet words (H_1 of the free group on g1,g2,g3)
expo := function(w) local v, l, i; v := [0,0,0]; l := LetterRepAssocWord(w); for i in l do v[AbsInt(i)] := v[AbsInt(i)] + SignInt(i); od; return v; end;;
for nm in ["x","y","r","s","A","B","M","N"] do Print("exponent vector of ", nm, ": ", expo(ValueGlobal(Concatenation(nm,"w"))), "\n"); od;
# relation matrix rank of Q's abelianisation
Print("exponent vectors of the 78 relators span rank: ", RankMat(List(rels, expo)), "\n");
# low-index subgroups: does M lie in each?
Print("low index subgroups of Q to index 5 ...\n");
L := LowIndexSubgroupsFpGroup(Q, 5);;
Print("  count: ", Length(L), "\n");
for U in L do
  Print("  index ", Index(Q, U), ": M in U? ", Mq in U, "   [B,M] in U? ", Comm(Bq,Mq) in U, "\n");
od;
# coset enumeration over <M>
Print("coset enumeration Q over <M> (limit 2000000): ");
tab := CosetTableFromGensAndRels(FreeGeneratorsOfFpGroup(Q), RelatorsOfFpGroup(Q), [UnderlyingElement(Mq)] : max := 2000000, silent := true);;
if tab = fail then Print("OVERFLOW\n"); else Print("index ", Length(tab[1]), "\n"); fi;
QUIT;
