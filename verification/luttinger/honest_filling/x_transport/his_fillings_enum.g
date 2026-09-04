F := FreeGroup("x","y","r","s","A","B","M","N");;
x:=F.1;; y:=F.2;; r:=F.3;; s:=F.4;; A:=F.5;; B:=F.6;; M:=F.7;; N:=F.8;;
relations := [
  A^1*x^1*A^-1*r^-1,
  A^1*y^1*A^-1*s^-1,
  A^1*r^1*A^-1*x^-1,
  A^1*s^1*A^-1*y^-1*N^-1,
  B^1*y^1*B^-1*x^-1*y^-1*M^1,
  B^1*r^1*B^-1*r^-1,
  B^1*s^1*B^-1*s^-1*r^-1*M^1*r^1,
  x^1*y^1*x^-1*y^-1*r^1*s^1*r^-1*s^-1,
  A^-1*r^1*A^1*x^-1,
  s^1*A^1*y^-1*A^-1,
  B^1*r^-1*B^-1*r^1,
  A^1*M^1*x^-1*A^-1*M^-1*r^1,
  x^1*M^1*A^-1*r^-1*M^-1*A^1,
  M^-1*A^1*r^-1*M^1*r^1*A^-1,
  M^1*B^1*y^1*B^-1*x^-1*y^-1,
  s^1*B^-1*s^-1*r^-1*M^1*B^1*r^1,
  x^1*M^1*B^1*y^-1*x^-1*s^1*B^-1*s^-1,
  r^-1*B^1*A^1*x^1*r^1*A^-1*y^1*B^-1*x^-1,
  y^1*B^-1*x^-1*B^1*x^1*A^1*y^-1*x^-1*A^-1*r^1*s^1,
  s^1*r^1*s^-1*r^-1*N^-1*A^1*s^1*A^-1*x^1*y^-1*x^-1,
  s^1*r^-1*s^-1*r^-1*A^1*x^1*y^1*x^1*y^-1*x^-1*A^-1*r^1,
  x^1*y^1*x^1*y^-1*x^-1*r^-1*A^1*x^1*y^1*x^1*y^-1*x^-1*r^-1*A^-1,
  r^1*s^1*A^1*B^-1*x^-1*A^-1*M^-1*y^1*r^1*A^1*B^1*A^-1*s^-1*r^-1*y^-1,
  M^1*B^1*A^1*x^1*y^1*x^1*y^-1*x^-1*A^-1*B^-1*M^-1*A^-1*x^1*y^1*x^-1*y^-1*x^-1*A^1,
  r^-1*A^1*x^1*y^1*x^1*y^-1*x^-1*r^-1*y^1*x^1*y^-1*x^-1*A^-1*y^1*B^-1*x^1*B^1*y^-1*x^1*y^-1*x^-1,
  r^-1*B^-1*M^-1*A^1*A^1*M^1*r^1*A^-1*r^1*A^-1*B^1*y^-1*x^-1,
  B^1*x^1*B^-1*M^-1*y^1,
  B^1*s^-1*r^-1*y^1*x^1*B^-1*M^-1*x^-1*s^1*r^1,
  M^1*A^1*x^1*M^-1*x^-1*A^-1,
  A^-1*N^1*A^1*r^-1*M^1*r^1*B^1*A^-1*N^-1*A^1*B^-1*r^-1*M^-1*r^1
];;
# His sheet modulo his fillings: Q on the 30 certified sheet relations, plus Wuebben's two fillings under the
# geometric map (M_W = M, N_W = K^-1 (A^-1 N A) K or A^-1 N A, y,s re-based) and under the algebraic dictionary
# (M_W = B M B^-1, N_W = M^-1 N M), all four sign pairs, 3,000,000 cosets.  Controls: honest, honest + [B,M].
K := r^-1*M*r;;
enum := function(fill) local tab; tab := CosetTableFromGensAndRels(GeneratorsOfGroup(F), Concatenation(relations, fill), [] : max := 3000000, silent := true); if tab = fail then return "overflow"; fi; return Concatenation("index ", String(Length(tab[1]))); end;;
lam := r^-1*M*r*B;;
for eA in [1,-1] do for eB in [1,-1] do
  Print("signs (", eA, ",", eB, ")\n");
  Print("  honest:                          ", enum([M*(A*x)^eA, A^-1*N*A*lam^eB]), "\n");
  Print("  honest + [B,M]:                  ", enum([M*(A*x)^eA, A^-1*N*A*lam^eB, B*M*B^-1*M^-1]), "\n");
  Print("  geometric, N_W = A^-1 N A:       ", enum([M*(A*x)^eA, A^-1*N*A*lam^eB]), "  (identical to honest)\n");
  Print("  geometric, N_W = K^-1 A^-1 N A K:", enum([M*(A*x)^eA, K^-1*A^-1*N*A*K*lam^eB]), "\n");
  Print("  geometric, N_W = K A^-1 N A K^-1:", enum([M*(A*x)^eA, K*A^-1*N*A*K^-1*lam^eB]), "\n");
  Print("  algebraic dictionary:            ", enum([B*M*B^-1*(A*x)^eA, M^-1*N*M*(r^-1*B*M*B^-1*r*B)^eB]), "\n");
  Print("  dictionary F1 only + honest F2:  ", enum([B*M*B^-1*(A*x)^eA, A^-1*N*A*lam^eB]), "\n");
  Print("  honest F1 + dictionary F2:       ", enum([M*(A*x)^eA, M^-1*N*M*(r^-1*B*M*B^-1*r*B)^eB]), "\n");
od; od;
QUIT;
