# stage1b_enumerate.g — re-run stage 1 on the "ours" cases with a 16,000,000-coset ceiling
# (four times the stage-1 ceiling), since case 1 and case 5 collapse only beyond 4,000,000.
Read("common.g");
LIMIT := 16000000;;
idx := List(SplitString(GAPInfo.SystemEnvironment.WS_CASES, ","), Int);;
for i in idx do
  c := CASES[i];
  G := mkG(c.mn[1], c.mn[2], c.e[1], c.e[2], c.e[3], c.e[4], c.e[5]);
  t0 := Runtime();
  tab := CosetTableFromGensAndRels(FreeGeneratorsOfFpGroup(G), RelatorsOfFpGroup(G), []
           : max := LIMIT, silent := true);
  if tab = fail then
    Print("case ", i, " ", caseLabel(c), ": enum(", LIMIT, ") OVERFLOW  ", Int((Runtime()-t0)/1000), "s\n");
  else
    Print("case ", i, " ", caseLabel(c), ": |G|=", Length(tab[1]), "  ", Int((Runtime()-t0)/1000), "s\n");
  fi;
od;
Print("stage 1b done ", stamp(), "\n");
QUIT_GAP(0);
