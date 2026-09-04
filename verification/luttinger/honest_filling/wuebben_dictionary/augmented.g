F:=FreeGroup("x","y","r","s","A","B","M","N");;
x:=F.1;; y:=F.2;; r:=F.3;; s:=F.4;; A:=F.5;; B:=F.6;; M:=F.7;; N:=F.8;;
sheet:=[(A*x*A^-1)*(r)^-1,
 (A*y*A^-1)*(s)^-1,
 (A*r*A^-1)*(x)^-1,
 (A*s*A^-1)*(N*y)^-1,
 (B*y*B^-1)*(M^-1*y*x)^-1,
 (B*r*B^-1)*(r)^-1,
 (B*s*B^-1)*(r^-1*M^-1*r*s)^-1,
 ((x)*(y)*(x)^-1*(y)^-1)*((r)*(s)*(r)^-1*(s)^-1),
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
 (B*x*B^-1)*(y^-1*M)^-1,
 B,
 ((M)*(A*x)*(M)^-1*(A*x)^-1)*(One(F))^-1,
 ((A^-1*N*A)*(r^-1*M*r*B)*(A^-1*N*A)^-1*(r^-1*M*r*B)^-1)*(One(F))^-1];;
Print("sheet relations: ", Length(sheet), "\n");
K:=r^-1*M*r;; yW:=M^-1*y;; sW:=K^-1*s;; MW:=B*M*B^-1;; NW:=M^-1*N*M;; d:=r^-1;;
wrows:=[ x*yW*x^-1*yW^-1*r*sW*r^-1*sW^-1, A*x*A^-1*r^-1, A*yW*A^-1*sW^-1, A*r*A^-1*x^-1, B*x*B^-1*yW, B*r*B^-1*r^-1, B*sW^-1*r^-1*yW*x*B^-1*x^-1*sW*r, A*sW*A^-1*(NW*yW)^-1, B*yW*B^-1*(MW^-1*yW*x)^-1, B*sW*B^-1*(d*MW^-1*d^-1*sW)^-1 ];;
cases:=rec(honest_y1_p1_p1:=[M*A*x, A^-1*N*A*r^-1*M*r*B]);;
cases.honest_y1_p1_p1:=[M*A*x, A^-1*N*A*r^-1*M*r*B];;
cases.honest_y1_p1_m1:=[M*A*x, A^-1*N*A*B^-1*r^-1*M^-1*r];;
cases.honest_y1_m1_p1:=[M*x^-1*A^-1, A^-1*N*A*r^-1*M*r*B];;
cases.honest_y1_m1_m1:=[M*x^-1*A^-1, A^-1*N*A*B^-1*r^-1*M^-1*r];;
cases.honest_y2_p1_p1:=[y^-1*M*y*y^-1*A*r^-1*y, A^-1*N*A*r^-1*M*r*B];;
cases.honest_y2_p1_m1:=[y^-1*M*y*y^-1*A*r^-1*y, A^-1*N*A*B^-1*r^-1*M^-1*r];;
cases.honest_y2_m1_p1:=[y^-1*M*y*y^-1*r*A^-1*y, A^-1*N*A*r^-1*M*r*B];;
cases.honest_y2_m1_m1:=[y^-1*M*y*y^-1*r*A^-1*y, A^-1*N*A*B^-1*r^-1*M^-1*r];;

for name in RecNames(cases) do
  fill:=cases.(name);
  t:=CosetTableFromGensAndRels(GeneratorsOfGroup(F), Concatenation(sheet, fill), [] : max:=4000000, silent:=true);
  if t=fail then Print(name, " sheet+fill: overflow\n"); else Print(name, " sheet+fill: index ", Length(t[1]), "\n"); fi;
  t:=CosetTableFromGensAndRels(GeneratorsOfGroup(F), Concatenation(sheet, wrows, fill), [] : max:=4000000, silent:=true);
  if t=fail then Print(name, " sheet+Wrows+fill: overflow\n"); else Print(name, " sheet+Wrows+fill: index ", Length(t[1]), "\n"); fi;
  t:=CosetTableFromGensAndRels(GeneratorsOfGroup(F), Concatenation(sheet, wrows, fill, [B*M*B^-1*M^-1]), [] : max:=4000000, silent:=true);
  if t=fail then Print(name, " sheet+Wrows+fill+[B,M]: overflow\n"); else Print(name, " sheet+Wrows+fill+[B,M]: index ", Length(t[1]), "\n"); fi;
od;
QUIT;

