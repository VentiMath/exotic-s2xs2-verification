# Coset enumeration of the eight honest filled groups on the sheet loops.
# "certified": the 26 reduction-certified relations only.  "with x transport": adds B x B^-1 = y^-1,
# which is a relation-sheet identity of the paper that is NOT yet certified in Q.
# Generated from honest_filling.json; run:  gap -q -A collapse.g < /dev/null
F := FreeGroup("x","y","r","s","A","B","M","N");;
x:=F.1;; y:=F.2;; r:=F.3;; s:=F.4;; A:=F.5;; B:=F.6;; M:=F.7;; N:=F.8;;
certified := [
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
  r^-1*B^-1*M^-1*A^1*A^1*M^1*r^1*A^-1*r^1*A^-1*B^1*y^-1*x^-1
];;
xtransport := [ B*x*B^-1*y ];;
enum := function(base, fill) local tab; tab := CosetTableFromGensAndRels(GeneratorsOfGroup(F), Concatenation(base, fill), [] : max := 1000000, silent := true); if tab = fail then return "overflow"; fi; return Length(tab[1]); end;;
fill := [M^1*A^1*x^1, A^-1*N^1*A^1*r^-1*M^1*r^1*B^1];; Print("honest_y1_p1_p1: certified -> ", enum(certified, fill), ";  with x transport -> ", enum(Concatenation(certified, xtransport), fill), "\n");;
fill := [M^1*A^1*x^1, A^-1*N^1*A^1*B^-1*r^-1*M^-1*r^1];; Print("honest_y1_p1_m1: certified -> ", enum(certified, fill), ";  with x transport -> ", enum(Concatenation(certified, xtransport), fill), "\n");;
fill := [M^1*x^-1*A^-1, A^-1*N^1*A^1*r^-1*M^1*r^1*B^1];; Print("honest_y1_m1_p1: certified -> ", enum(certified, fill), ";  with x transport -> ", enum(Concatenation(certified, xtransport), fill), "\n");;
fill := [M^1*x^-1*A^-1, A^-1*N^1*A^1*B^-1*r^-1*M^-1*r^1];; Print("honest_y1_m1_m1: certified -> ", enum(certified, fill), ";  with x transport -> ", enum(Concatenation(certified, xtransport), fill), "\n");;
fill := [y^-1*M^1*y^1*y^-1*A^1*r^-1*y^1, A^-1*N^1*A^1*r^-1*M^1*r^1*B^1];; Print("honest_y2_p1_p1: certified -> ", enum(certified, fill), ";  with x transport -> ", enum(Concatenation(certified, xtransport), fill), "\n");;
fill := [y^-1*M^1*y^1*y^-1*A^1*r^-1*y^1, A^-1*N^1*A^1*B^-1*r^-1*M^-1*r^1];; Print("honest_y2_p1_m1: certified -> ", enum(certified, fill), ";  with x transport -> ", enum(Concatenation(certified, xtransport), fill), "\n");;
fill := [y^-1*M^1*y^1*y^-1*r^1*A^-1*y^1, A^-1*N^1*A^1*r^-1*M^1*r^1*B^1];; Print("honest_y2_m1_p1: certified -> ", enum(certified, fill), ";  with x transport -> ", enum(Concatenation(certified, xtransport), fill), "\n");;
fill := [y^-1*M^1*y^1*y^-1*r^1*A^-1*y^1, A^-1*N^1*A^1*B^-1*r^-1*M^-1*r^1];; Print("honest_y2_m1_m1: certified -> ", enum(certified, fill), ";  with x transport -> ", enum(Concatenation(certified, xtransport), fill), "\n");;
QUIT;
