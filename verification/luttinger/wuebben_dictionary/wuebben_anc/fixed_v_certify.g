# fixed_v_certify.g — direct finite certificate for the specified piece V.
#
# This is the direct group check used for the theorem. At (m,n)=(0,0), include
# the true drilled-fiber relation R3 and independently vary every local choice that
# either occurs in the derived sheet or is a useful robustness perturbation:
#   * five relation signs (e3,e4,e5,eA,eB);
#   * left/right placement of each of the three transport corrections;
#   * either c-arc conjugator (r^-1 or x) for the Bs correction;
#   * either c-arc, either meridian sign, and pre/post-B placement for the
#     based T_beta push-off correction.
# Thus 2^5 * 2^3 * 2 * (2*2*2) = 4096 relation systems are checked for the
# specified y1-side section A*x. The complete run is then repeated for the
# adjacent y2-side section A*r^-1. Every system must have trivial
# abelianization and a terminating one-coset table.
# No optional GAP package is required.

SizeScreen([200, 40]);;
F := FreeGroup("x","y","r","s","A","B","M","N");;
x := F.1;; y := F.2;; r := F.3;; s := F.4;;
A := F.5;; B := F.6;; M := F.7;; N := F.8;;
comm := function(u,v) return u*v*u^-1*v^-1; end;;

base := [
  comm(x,y)*comm(r,s),
  A*x*A^-1*r^-1, A*y*A^-1*s^-1, A*r*A^-1*x^-1,
  B*x*B^-1*y, B*r*B^-1*r^-1,
  B*(s^-1*r^-1*y*x)*B^-1*(r^-1*s^-1*x)^-1
];;

mkTransport := function(lhs, image, correction, side)
  if side = 1 then return lhs*(correction*image)^-1;
  else return lhs*(image*correction)^-1; fi;
end;;

RunFamily := function(label, dirTaBase)
  local counts, pAs, pBy, pBs, deltaBs, deltaF, eta, pF,
        e3, e4, e5, eA, eB, corrF, dirTb, rels, G, tab;
  counts := rec(total:=0, trivial:=0, overflow:=0, finite:=0, h1:=0);
  for pAs in [1,2] do for pBy in [1,2] do for pBs in [1,2] do
  for deltaBs in [r^-1,x] do
  for deltaF in [r^-1,x] do for eta in [1,-1] do for pF in [1,2] do
  for e3 in [1,-1] do for e4 in [1,-1] do for e5 in [1,-1] do
  for eA in [1,-1] do for eB in [1,-1] do
    counts.total := counts.total + 1;
    corrF := deltaF*M^eta*deltaF^-1;
    if pF = 1 then dirTb := corrF*B; else dirTb := B*corrF; fi;
    rels := Concatenation(base, [
      mkTransport(A*s*A^-1, y,   N^e3,                         pAs),
      mkTransport(B*y*B^-1, y*x, M^e4,                         pBy),
      mkTransport(B*s*B^-1, s,   deltaBs*M^e5*deltaBs^-1,      pBs),
      M*dirTaBase^eA,
      N*dirTb^eB
    ]);
    G := F/rels;
    if Length(AbelianInvariants(G)) > 0 then
      counts.h1 := counts.h1 + 1;
    else
      tab := CosetTableFromGensAndRels(FreeGeneratorsOfFpGroup(G),
               RelatorsOfFpGroup(G), [] : max := 400000, silent := true);
      if tab = fail then counts.overflow := counts.overflow + 1;
      elif Length(tab[1]) = 1 then counts.trivial := counts.trivial + 1;
      else
        counts.finite := counts.finite + 1;
        Print("FINITE>1: placements=",[pAs,pBy,pBs,pF],
              " arcs=",[deltaBs,deltaF]," signs=",[eta,e3,e4,e5,eA,eB],
              " |G|=",Length(tab[1]),"\n");
      fi;
    fi;
  od; od; od; od; od;
  od; od; od;
  od;
  od; od; od;

  Print(label, ": TOTAL=",counts.total,
        " TRIVIAL=",counts.trivial,
        " OVERFLOW=",counts.overflow,
        " FINITE>1=",counts.finite,
        " H1nonzero=",counts.h1,"\n");
end;;

RunFamily("FIXED V (y1/Ax) WITH R3", A*x);;
RunFamily("ADJACENT T_ALPHA SECTION (y2/Ar^-1) WITH R3", A*r^-1);;
QUIT_GAP(0);
