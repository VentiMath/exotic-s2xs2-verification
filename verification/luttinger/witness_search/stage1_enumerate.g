# stage1_enumerate.g — for every case: abelianization, then coset enumeration with a
# 4,000,000-coset ceiling (ten times Wuebben's decide2 limit).  Cases that resolve are
# finished here; cases that overflow go to stage 2.
Read("common.g");
LIMIT := 4000000;;
Print("stage 1: ", Length(CASES), " cases, coset ceiling ", LIMIT, "\n");
for i in [1..Length(CASES)] do
  c := CASES[i];
  G := mkG(c.mn[1], c.mn[2], c.e[1], c.e[2], c.e[3], c.e[4], c.e[5]);
  ab := AbelianInvariants(G);
  t0 := Runtime();
  if Length(ab) > 0 then
    Print("case ", i, " ", caseLabel(c), ": H1=", ab, " NONTRIVIAL-ABELIAN\n");
  else
    tab := CosetTableFromGensAndRels(FreeGeneratorsOfFpGroup(G), RelatorsOfFpGroup(G), []
             : max := LIMIT, silent := true);
    if tab = fail then
      Print("case ", i, " ", caseLabel(c), ": H1=0  enum(", LIMIT, ") OVERFLOW  ",
            Int((Runtime()-t0)/1000), "s\n");
    else
      Print("case ", i, " ", caseLabel(c), ": H1=0  |G|=", Length(tab[1]), "  ",
            Int((Runtime()-t0)/1000), "s\n");
    fi;
  fi;
od;
Print("stage 1 done ", stamp(), "\n");
QUIT_GAP(0);
