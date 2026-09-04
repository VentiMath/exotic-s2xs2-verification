F := FreeGroup("x","y","r","s","A","B","M","N");;
x:=F.1;; y:=F.2;; r:=F.3;; s:=F.4;; A:=F.5;; B:=F.6;; M:=F.7;; N:=F.8;;
d := r^-1;;
for e3 in [1,-1] do for e4 in [1,-1] do for e in [1,-1] do for eA in [1,-1] do for eB in [1,-1] do
  rels := [ x*y*x^-1*y^-1*r*s*r^-1*s^-1,
            A*x*A^-1*r^-1, A*y*A^-1*s^-1, A*r*A^-1*x^-1,
            B*x*B^-1*y, B*r*B^-1*r^-1,
            B*s^-1*r^-1*y*x*B^-1*x^-1*s*r,
            A*s*A^-1*(N^e3*y)^-1,
            B*y*B^-1*(M^e4*y*x)^-1,
            B*s*B^-1*(d*M^e*d^-1*s)^-1,
            M*(A*x)^eA,
            N*((d*M^(-e)*d^-1)*B)^eB ];
  t := CosetTableFromGensAndRels(GeneratorsOfGroup(F), rels, [] : max := 2000000, silent := true);
  if t = fail then Print("signs ", [e3,e4,e,eA,eB], " overflow\n");
  else Print("signs ", [e3,e4,e,eA,eB], " index ", Length(t[1]), "\n"); fi;
od; od; od; od; od;
QUIT;
