# decide2.g — completed presentation, re-indexed to y1/Ax on 2026-08-16.
# = phase-1 relation system + the true T_alpha transport relation R3:
#     R3:  B kappa3 B^-1 = psi(kappa3),  kappa3 = s^-1 r^-1 y x  (engine D5),
#          psi(kappa3) = r^-1 s^-1 x.
# T_beta needs no completion ({x,y,r} is a free basis of pi_1(F - nu(e)));
# stable-letter and annulus relations proved redundant; corner-region residual open.
# Adding true relations only quotients further: trivial cells provably stay trivial;
# the run's information is in the former blowup cells.
F := FreeGroup("x","y","r","s","A","B","M","N");;
x:=F.1;;y:=F.2;;r:=F.3;;s:=F.4;;A:=F.5;;B:=F.6;;M:=F.7;;N:=F.8;;
comm := function(u,v) return u*v*u^-1*v^-1; end;;
R0 := comm(x,y)*comm(r,s);;
kappa3 := s^-1*r^-1*y*x;;  psik3 := r^-1*s^-1*x;;
base := [R0, A*x*A^-1*r^-1, A*y*A^-1*s^-1, A*r*A^-1*x^-1, B*x*B^-1*y, B*r*B^-1*r^-1,
         B*kappa3*B^-1*psik3^-1];;   # R3 appended to the clean set
dirTaBase := A*x;;  dirTaFib := (r*x)^-1;;
# LOGGED FIX 2026-07-15 (paper: the pushoff-basing correction): honest
# dirTbBase, sign anti-coupled to e5.
dirTbBase := function(e5) return r^-1*M^(-e5)*r * B; end;;
dirTbFib := s*r^-1*s^-1;;
for mn in Cartesian([-1,0,1],[-1,0,1]) do
  ct := rec(triv:=0, blow:=0, h1:=0, fin:=0);
  for eA in [1,-1] do for eB in [1,-1] do
    for e3 in [1,-1] do for e4 in [1,-1] do for e5 in [1,-1] do
      rels := Concatenation(base,
        [ A*s*A^-1*(N^e3*y)^-1,
          B*y*B^-1*(M^e4*y*x)^-1,
          B*s*B^-1*(r^-1*M^e5*r*s)^-1,
          M*(dirTaBase*dirTaFib^mn[2])^eA,
          N*(dirTbBase(e5)*dirTbFib^mn[1])^eB ]);
      G := F / rels;
      ab := AbelianInvariants(G);
      if Length(ab) > 0 then ct.h1 := ct.h1 + 1;
      else
        tab := CosetTableFromGensAndRels(FreeGeneratorsOfFpGroup(G),
                 RelatorsOfFpGroup(G), [] : max := 400000, silent := true);
        if tab = fail then ct.blow := ct.blow + 1;
        elif Length(tab[1]) = 1 then ct.triv := ct.triv + 1;
        else ct.fin := ct.fin + 1;
          Print("FINITE>1 at mn=",mn," |G|=",Length(tab[1]),"\n"); fi;
      fi;
    od; od; od;
  od; od;
  Print("COMPLETE m=",mn[1]," n=",mn[2],": triv=",ct.triv," blow=",ct.blow,
        " fin=",ct.fin," h1=",ct.h1,"\n");
od;
Print("DONE\n");
QUIT_GAP(0);
