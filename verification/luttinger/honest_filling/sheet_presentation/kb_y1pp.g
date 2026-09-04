F := FreeGroup("x","y","r","s","A","B","M","N");;
x:=F.1;; y:=F.2;; r:=F.3;; s:=F.4;; A:=F.5;; B:=F.6;; M:=F.7;; N:=F.8;;
cert8 := [ A*x*A^-1*r^-1, A*y*A^-1*s^-1, A*r*A^-1*x^-1, A*s*A^-1*(N*y)^-1,
           B*y*B^-1*(M^-1*y*x)^-1, B*r*B^-1*r^-1, B*s*B^-1*(r^-1*M^-1*r*s)^-1, x*y*x^-1*y^-1*r*s*r^-1*s^-1 ];;
extra := [ x*M*B*y^-1*x^-1*s*B^-1*s^-1, A*M*x^-1*A^-1*M^-1*r, x*M*A^-1*r^-1*M^-1*A, M^-1*A*r^-1*M*r*A^-1, s*B^-1*s^-1*r^-1*M*B*r ];;
fill := [ M*(A*x), A^-1*N*A*(r^-1*M*r*B) ];;
G := F / Concatenation(cert8, extra, fill);;
Print("abelian invariants: ", AbelianInvariants(G), "\n");
t := Runtime();
iso := IsomorphismFpMonoid(G);; Mon := Range(iso);;
rws := KnuthBendixRewritingSystem(Mon);;
MakeConfluent(rws);
Print("confluent: ", IsConfluent(rws), " rules: ", Length(Rules(rws)), " time ", Runtime()-t, " ms\n");
for g in GeneratorsOfGroup(G) do Print(g, " -> ", ReducedForm(rws, UnderlyingElement(Image(iso, g))), "\n"); od;
QUIT;
