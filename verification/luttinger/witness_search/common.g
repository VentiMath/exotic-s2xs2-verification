# common.g — shared definitions for the witness search (Run 72).
#
# The relation systems are Wuebben's CURRENT-coordinate family exactly as defined in
# his decide2.g (arXiv:2608.17267v1 anc; vendored and hash-verified under
# ../wuebben_dictionary/wuebben_anc/), including the 2026-07-15 push-off correction
# to the beta longitude.  At (m,n)=(0,0), e3=+1, e4=-1, e5=-1 this is the paper's
# displayed sheet (Run 71).  Everything else is a neighbour of it.
F := FreeGroup("x","y","r","s","A","B","M","N");;
x:=F.1;;y:=F.2;;r:=F.3;;s:=F.4;;A:=F.5;;B:=F.6;;M:=F.7;;N:=F.8;;
comm := function(u,v) return u*v*u^-1*v^-1; end;;
R0 := comm(x,y)*comm(r,s);;
kappa3 := s^-1*r^-1*y*x;;  psik3 := r^-1*s^-1*x;;
base := [R0, A*x*A^-1*r^-1, A*y*A^-1*s^-1, A*r*A^-1*x^-1, B*x*B^-1*y, B*r*B^-1*r^-1,
         B*kappa3*B^-1*psik3^-1];;
dirTaBase := A*x;;  dirTaFib := (r*x)^-1;;
dirTbBase := function(e5) return r^-1*M^(-e5)*r * B; end;;
dirTbFib := s*r^-1*s^-1;;
mkG := function(m, n, e3, e4, e5, eA, eB)
  return F / Concatenation(base,
    [ A*s*A^-1*(N^e3*y)^-1,
      B*y*B^-1*(M^e4*y*x)^-1,
      B*s*B^-1*(r^-1*M^e5*r*s)^-1,
      M*(dirTaBase*dirTaFib^n)^eA,
      N*(dirTbBase(e5)*dirTbFib^m)^eB ]);
end;;

# Cases.  The n = -1 column is where Wuebben's own decide2 log shows every one of
# his 32 sign systems overflowing at 400,000 cosets, for each m.  Two sign families:
#   "ours"    e3=+1 e4=-1 e5=-1, the paper's signs, with (eA,eB) over {+-1}^2;
#   "wuebben" the four patterns his 56-hour phase-2/3 search used (old coordinate).
CASES := [];;
for m in [-1,0,1] do
  for eA in [1,-1] do for eB in [1,-1] do
    Add(CASES, rec(fam:="ours", mn:=[m,-1], e:=[1,-1,-1,eA,eB]));
  od; od;
od;
for m in [-1,0,1] do
  for e in [[1,1,1,1,1],[-1,-1,-1,-1,-1],[1,-1,1,-1,1],[-1,1,-1,1,-1]] do
    Add(CASES, rec(fam:="wuebben", mn:=[m,-1], e:=e));
  od;
od;
caseLabel := function(c)
  return Concatenation(c.fam, " (", String(c.mn[1]), ",", String(c.mn[2]), ") e=", String(c.e));
end;;
stamp := function() return Concatenation("[", String(Int(Runtime()/1000)), "s]"); end;;

# Every nonabelian simple group of order < 10^5, ascending (L2(59) = 102660 is next).
# Since H1 = 0 for every case (checked in stage 1), a nontrivial finite quotient of
# order <= 10^5 exists iff one of these is a quotient.
TARGETS := [ "A5","L2_7","A6","L2_8","L2_11","L2_13","L2_17","A7","L2_19","L2_16",
             "L3_3","U3_3","L2_23","L2_25","M11","L2_27","L2_29","L2_31","A8","L3_4",
             "L2_37","U4_2","Sz_8","L2_32","L2_41","L2_43","L2_47","L2_49","U3_4",
             "L2_53","M12" ];;
mkTarget := function(name)
  local q;
  if name = "A5"  then return AlternatingGroup(5);
  elif name = "A6" then return AlternatingGroup(6);
  elif name = "A7" then return AlternatingGroup(7);
  elif name = "A8" then return AlternatingGroup(8);
  elif name = "M11" then return MathieuGroup(11);
  elif name = "M12" then return MathieuGroup(12);
  elif name = "L3_3" then return PSL(3,3);
  elif name = "L3_4" then return PSL(3,4);
  elif name = "U3_3" then return PSU(3,3);
  elif name = "U3_4" then return PSU(3,4);
  elif name = "U4_2" then return PSU(4,2);
  elif name = "Sz_8" then return Image(IsomorphismPermGroup(SuzukiGroup(8)));
  elif name{[1..3]} = "L2_" then
    q := Int(name{[4..Length(name)]}); return PSL(2,q);
  fi;
  Error("unknown target ", name);
end;;
