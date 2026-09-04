# grid_3x3.g — the (n, m) fiber-direction shift grid on the displayed (+,+) sheet,
# issue #800.  common.g's family: alpha filling M (A x . ((r x)^-1)^n)^eA, beta
# filling N (r^-1 M^-e5 r B . (s r^-1 s^-1)^m)^eB, e3=+1, e4=-1, e5=-1, eA=eB=+1.
# Each cell: coset enumeration (GAP's classic enumerator, TCENUM = GAPTCENUM) with
# fixed ceilings 4M, 16M, 32M; each attempt returns fail on overflow instead of
# entering a break loop.  Size()'s own retry ladder uses the NEWTC enumerator and,
# on the first cell, exceeded 32M cosets and dropped into a break loop (logs/grid_3x3_attempt1.log).
# NB: common.g binds r, s, x, y, A, B, M, N as free generators; do not reuse those names.
# (n,m)=(0,0) is the displayed sheet.  Memory: 32M cosets x 12 columns ~ 3 GB.
Read("common.g");
BreakOnError := false;;
LIMITS := [4000000, 16000000, 32000000];;
Print("grid 3x3 on the displayed (+,+) sheet ", stamp(), "\n");
tryEnum := function(G, lim)
  local t0, tab;
  t0 := Runtime();
  tab := CosetTableFromGensAndRels(FreeGeneratorsOfFpGroup(G), RelatorsOfFpGroup(G), [] : max := lim, silent := true);
  if tab = fail then return [fail, Int((Runtime()-t0)/1000)]; fi;
  return [Length(tab[1]), Int((Runtime()-t0)/1000)];
end;;
for n in [-1,0,1] do for m in [-1,0,1] do
  G := mkG(m, n, 1, -1, -1, 1, 1);
  ab := AbelianInvariants(G);
  done := false;
  for lim in LIMITS do
    res := tryEnum(G, lim);
    if res[1] <> fail then
      Print("(n,m)=(", n, ",", m, "): H1=", ab, "  |G|=", res[1], "  closed under ", lim, " cosets, ", res[2], "s\n");
      done := true; break;
    else
      Print("(n,m)=(", n, ",", m, "): overflow at ", lim, ", ", res[2], "s\n");
    fi;
  od;
  if not done then
    Print("(n,m)=(", n, ",", m, "): H1=", ab, "  UNDECIDED: overflow at 32000000 cosets\n");
  fi;
od; od;
Print("grid done ", stamp(), "\n");
QUIT_GAP(0);
