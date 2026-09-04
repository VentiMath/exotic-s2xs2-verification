# grid_cell_ace.g — one (n, m) cell of the displayed (+,+) sheet through ACE (GAP package
# ace-5.3 in the luttinger-kbmag-proof:local image), strategy "hard" (Felsch-heavy), a
# fixed workspace in 4-byte words (env GC_WS, e.g. 480M ~ 1.9 GB ~ 40M cosets x 12 cols).
# Env GC_STRAT selects the ACE strategy: hard (default), felsch, sims9.
# The classic GAP enumerator overflows 32M cosets on the n = -1 cells; ACE's strategy
# defines cosets differently and may close, or may not.  Env GC_N, GC_M select the cell.
Read("common.g");
LoadPackage("ace");;
n := Int(GAPInfo.SystemEnvironment.GC_N);; m := Int(GAPInfo.SystemEnvironment.GC_M);;
ws := GAPInfo.SystemEnvironment.GC_WS;;
strat := "hard";; if IsBound(GAPInfo.SystemEnvironment.GC_STRAT) then strat := GAPInfo.SystemEnvironment.GC_STRAT; fi;;
G := mkG(m, n, 1, -1, -1, 1, 1);;
Print("ACE ", strat, ", cell (n,m)=(", n, ",", m, "), workspace ", ws, " words\n");
t0 := Runtime();;
run := function()
  local fg, rl;
  fg := FreeGeneratorsOfFpGroup(G); rl := RelatorsOfFpGroup(G);
  if strat = "felsch" then return ACEStats(fg, rl, [] : felsch, workspace := EvalString(ws));
  elif strat = "sims9" then return ACEStats(fg, rl, [] : sims := 9, workspace := EvalString(ws));
  else return ACEStats(fg, rl, [] : hard, workspace := EvalString(ws)); fi;
end;;
att := CALL_WITH_CATCH(run, []);;
if att[1] then
  Print("(n,m)=(", n, ",", m, "): ACE index=", att[2].index, " activecosets=", att[2].activecosets, " maxcosets=", att[2].maxcosets, " totcosets=", att[2].totcosets, "  ", Int((Runtime()-t0)/1000), "s\n");
  if att[2].index = 1 then Print("(n,m)=(", n, ",", m, "): |G|=1 by ACE ", strat, "\n");
  elif att[2].index = 0 then Print("(n,m)=(", n, ",", m, "): ACE did not close (index 0 = overflow)\n"); fi;
else
  Print("(n,m)=(", n, ",", m, "): ACE failed: ", att[2], "\n");
fi;
QUIT_GAP(0);
