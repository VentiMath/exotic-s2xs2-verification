F := FreeGroup("x","y","r","s","A","B","M","N");;
x:=F.1;; y:=F.2;; r:=F.3;; s:=F.4;; A:=F.5;; B:=F.6;; M:=F.7;; N:=F.8;;
core := [ A*x*A^-1*r^-1, A*y*A^-1*s^-1, A*r*A^-1*x^-1, A*s*A^-1*(N*y)^-1,
          B*y*B^-1*(M^-1*y*x)^-1, B*r*B^-1*r^-1, B*s*B^-1*(r^-1*M^-1*r*s)^-1,
          Comm(x,y)*Comm(r,s) ];;
la := A*x;; lb := r^-1*M*r*B;;
for eA in [1,-1] do for eB in [1,-1] do
  fill := [ M*la^eA, A^-1*N*A*lb^eB ];
  t := Runtime();
  tab := CosetTableFromGensAndRels(GeneratorsOfGroup(F), Concatenation(core, fill), [] : max := 300000, silent := true);
  if tab = fail then Print("core(no BxB^-1) eA=", eA, " eB=", eB, ": overflow >300000 (", Runtime()-t, " ms)\n");
  else Print("core(no BxB^-1) eA=", eA, " eB=", eB, ": index ", Length(tab[1]), " (", Runtime()-t, " ms)\n"); fi;
od; od;
QUIT;
