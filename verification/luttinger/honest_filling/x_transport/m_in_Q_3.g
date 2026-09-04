# Part D, third pass: M in H_1 of the (Z/n)^2 abelian covers, n = 3 (index 9) and n = 4 (index 16).
Read("q_input.g");
hom := GroupHomomorphismByImages(F, Q, GeneratorsOfGroup(F), GeneratorsOfGroup(Q));;
Mq := Image(hom, Mw);; Bq := Image(hom, Bw);;
ab := MaximalAbelianQuotient(Q);; Ab := Range(ab);;
for n in [3, 4, 5] do
  modn := NaturalHomomorphismByNormalSubgroup(Ab, Subgroup(Ab, List(GeneratorsOfGroup(Ab), g -> g^n)));;
  U := Kernel(ab * modn);;
  Print("n = ", n, ": index ", Index(Q, U), "\n");
  iso := IsomorphismFpGroup(U);; UU := Range(iso);; abU := MaximalAbelianQuotient(UU);;
  Print("   H1(U) = ", AbelianInvariants(UU), "\n");
  Print("   M trivial in H1(U)? ", IsOne(Image(abU, Image(iso, Mq))), "   [B,M] trivial? ", IsOne(Image(abU, Image(iso, Comm(Bq, Mq)))), "\n");
od;
QUIT;
