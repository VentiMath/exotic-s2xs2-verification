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
 (B*s^-1*r^-1*y*x*B^-1)*(r^-1*s^-1*x*M)^-1,
 ((M)*(A*x)*(M)^-1*(A*x)^-1)*(One(F))^-1,
 ((A^-1*N*A)*(r^-1*M*r*B)*(A^-1*N*A)^-1*(r^-1*M*r*B)^-1)*(One(F))^-1];;
Print("sheet relations: ", Length(sheet), "\n");
K:=r^-1*M*r;; yW:=M^-1*y;; sW:=K^-1*s;; MW:=B*M*B^-1;; NW:=M^-1*N*M;; d:=r^-1;;
wrows:=[ x*yW*x^-1*yW^-1*r*sW*r^-1*sW^-1, A*x*A^-1*r^-1, A*yW*A^-1*sW^-1, A*r*A^-1*x^-1, B*x*B^-1*yW, B*r*B^-1*r^-1, B*sW^-1*r^-1*yW*x*B^-1*x^-1*sW*r, A*sW*A^-1*(NW*yW)^-1, B*yW*B^-1*(MW^-1*yW*x)^-1, B*sW*B^-1*(d*MW^-1*d^-1*sW)^-1 ];;
cases:=rec();;
cases.honest_y1_p1_p1:=[M*A*x, A^-1*N*A*r^-1*M*r*B];;
cases.honest_y1_p1_m1:=[M*A*x, A^-1*N*A*B^-1*r^-1*M^-1*r];;
cases.honest_y1_m1_p1:=[M*x^-1*A^-1, A^-1*N*A*r^-1*M*r*B];;
cases.honest_y1_m1_m1:=[M*x^-1*A^-1, A^-1*N*A*B^-1*r^-1*M^-1*r];;
cases.honest_y2_p1_p1:=[y^-1*M*y*y^-1*A*r^-1*y, A^-1*N*A*r^-1*M*r*B];;
cases.honest_y2_p1_m1:=[y^-1*M*y*y^-1*A*r^-1*y, A^-1*N*A*B^-1*r^-1*M^-1*r];;
cases.honest_y2_m1_p1:=[y^-1*M*y*y^-1*r*A^-1*y, A^-1*N*A*r^-1*M*r*B];;
cases.honest_y2_m1_m1:=[y^-1*M*y*y^-1*r*A^-1*y, A^-1*N*A*B^-1*r^-1*M^-1*r];;


c := B*M*B^-1*M^-1;;   # [B,M]
Ngrid := A^-1*N^-1*A;;  # N_grid = A^-1 geom_N^-1 A  (free-word identity A^-1 geom_N A = N_grid^-1)
c2 := A*Ngrid*A^-1*Ngrid^-1;;  # [A, N_grid]
fill := cases.honest_y1_p1_p1;;
base := Concatenation(sheet, fill);;
Try := function(label, extra)
  local t;
  t := CosetTableFromGensAndRels(GeneratorsOfGroup(F), Concatenation(base, extra), [] : max := 3000000, silent := true);
  if t = fail then Print(label, ": overflow\n"); else Print(label, ": index ", Length(t[1]), "\n"); fi;
end;;
Try("+[A,N_grid]", [c2]);
Try("+[B,M]", [c]);
for k in [2..6] do Try(Concatenation("+[B,M]^", String(k)), [c^k]); od;
Try("+[[B,M],B]", [c*B*c^-1*B^-1]);
Try("+[[B,M],M]", [c*M*c^-1*M^-1]);
Try("+[[B,M],A]", [c*A*c^-1*A^-1]);
Try("+[[B,M],x]", [c*x*c^-1*x^-1]);
Try("+[[B,M],[A,N_grid]]", [c*c2*c^-1*c2^-1]);
Try("+[B,M]=[A,N_grid]", [c*c2^-1]);
Try("+[B,M]=[A,N_grid]^-1", [c*c2]);
Try("+[B,M]^2=[A,N_grid]", [c^2*c2^-1]);
Try("+B commutes with Ax", [B*A*x*B^-1*x^-1*A^-1]);
Try("+A commutes with r^-1MrB (lb_b_s2)", [A*r^-1*M*r*B*A^-1*B^-1*r^-1*M^-1*r]);
Try("+[A,B]", [A*B*A^-1*B^-1]);
Try("+[A,B]^2", [(A*B*A^-1*B^-1)^2]);
Try("+[x,M]", [x*M*x^-1*M^-1]);
Try("+[B,N]", [B*N*B^-1*N^-1]);
Try("+[A,M]", [A*M*A^-1*M^-1]);
Try("+[A,N]", [A*N*A^-1*N^-1]);
Try("+[M,N]", [M*N*M^-1*N^-1]);
Try("+M^2", [M^2]);
Try("+M^3", [M^3]);
Try("+A^2", [A^2]);
Try("+B^2", [B^2]);
QUIT;
