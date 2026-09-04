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
enum := function(fill) local tab; tab := CosetTableFromGensAndRels(GeneratorsOfGroup(F), Concatenation(relations, fill), [] : max := 2000000, silent := true); if tab = fail then return "overflow"; fi; return Length(tab[1]); end;;
Print("honest_y1_p1_p1: honest -> ", enum([M^1*A^1*x^1, A^-1*N^1*A^1*r^-1*M^1*r^1*B^1]), ";  sealed -> ", enum([M^1*A^1*x^1, N*(r^-1*M*r*B)^1]), "\n");;
Print("honest_y1_p1_m1: honest -> ", enum([M^1*A^1*x^1, A^-1*N^1*A^1*B^-1*r^-1*M^-1*r^1]), ";  sealed -> ", enum([M^1*A^1*x^1, N*(r^-1*M*r*B)^-1]), "\n");;
Print("honest_y1_m1_p1: honest -> ", enum([M^1*x^-1*A^-1, A^-1*N^1*A^1*r^-1*M^1*r^1*B^1]), ";  sealed -> ", enum([M^1*x^-1*A^-1, N*(r^-1*M*r*B)^1]), "\n");;
Print("honest_y1_m1_m1: honest -> ", enum([M^1*x^-1*A^-1, A^-1*N^1*A^1*B^-1*r^-1*M^-1*r^1]), ";  sealed -> ", enum([M^1*x^-1*A^-1, N*(r^-1*M*r*B)^-1]), "\n");;
Print("honest_y2_p1_p1: honest -> ", enum([y^-1*M^1*y^1*y^-1*A^1*r^-1*y^1, A^-1*N^1*A^1*r^-1*M^1*r^1*B^1]), ";  sealed -> ", enum([y^-1*M^1*y^1*y^-1*A^1*r^-1*y^1, N*(r^-1*M*r*B)^1]), "\n");;
Print("honest_y2_p1_m1: honest -> ", enum([y^-1*M^1*y^1*y^-1*A^1*r^-1*y^1, A^-1*N^1*A^1*B^-1*r^-1*M^-1*r^1]), ";  sealed -> ", enum([y^-1*M^1*y^1*y^-1*A^1*r^-1*y^1, N*(r^-1*M*r*B)^-1]), "\n");;
Print("honest_y2_m1_p1: honest -> ", enum([y^-1*M^1*y^1*y^-1*r^1*A^-1*y^1, A^-1*N^1*A^1*r^-1*M^1*r^1*B^1]), ";  sealed -> ", enum([y^-1*M^1*y^1*y^-1*r^1*A^-1*y^1, N*(r^-1*M*r*B)^1]), "\n");;
Print("honest_y2_m1_m1: honest -> ", enum([y^-1*M^1*y^1*y^-1*r^1*A^-1*y^1, A^-1*N^1*A^1*B^-1*r^-1*M^-1*r^1]), ";  sealed -> ", enum([y^-1*M^1*y^1*y^-1*r^1*A^-1*y^1, N*(r^-1*M*r*B)^-1]), "\n");;
QUIT;
