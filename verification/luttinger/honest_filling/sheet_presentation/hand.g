F := FreeGroup("x","y","r","s","A","B","M","N");;
x:=F.1;; y:=F.2;; r:=F.3;; s:=F.4;; A:=F.5;; B:=F.6;; M:=F.7;; N:=F.8;;
sheet := [ A*x*A^-1*r^-1, A*y*A^-1*s^-1, A*r*A^-1*x^-1, A*s*A^-1*(N*y)^-1,
           B*x*B^-1*y, B*y*B^-1*(M^-1*y*x)^-1, B*r*B^-1*r^-1, B*s*B^-1*(r^-1*M^-1*r*s)^-1,
           Comm(x,y)*Comm(r,s) ];;
la := A*x;; lb := r^-1*M*r*B;;
Print("sheet group abelian invariants: ", AbelianInvariants(F/sheet), "\n");
for kind in ["sealed", "honest"] do
  for eA in [1,-1] do
    for eB in [1,-1] do
      if kind = "sealed" then fill := [ M*la^eA, N*lb^eB ];
      else fill := [ M*la^eA, A^-1*N*A*lb^eB ]; fi;
      rels := Concatenation(sheet, fill);
      t := Runtime();
      tab := CosetTableFromGensAndRels(GeneratorsOfGroup(F), rels, [] : max := 4000000, silent := true);
      if tab = fail then
        Print(kind, " eA=", eA, " eB=", eB, ": overflow (>4e6 cosets) after ", Runtime()-t, " ms\n");
      else
        Print(kind, " eA=", eA, " eB=", eB, ": index ", Length(tab[1]), " (", Runtime()-t, " ms); abelian invariants ", AbelianInvariants(F/rels), "\n");
      fi;
    od;
  od;
od;
QUIT;
