# stage1c_size.g — one case: GAP's Size() with its own retry ladder up to CosetTableDefaultMaxLimit.
Read("common.g");
CosetTableDefaultMaxLimit := 32000000;;
i := Int(GAPInfo.SystemEnvironment.WS_CASE);;
c := CASES[i];;
G := mkG(c.mn[1], c.mn[2], c.e[1], c.e[2], c.e[3], c.e[4], c.e[5]);;
t0 := Runtime();;
res := CALL_WITH_CATCH(function() return Size(G); end, []);;
if res[1] then
  Print("case ", i, " ", caseLabel(c), ": |G|=", res[2], "  ", Int((Runtime()-t0)/1000), "s  (Size ladder to 32M)\n");
else
  Print("case ", i, " ", caseLabel(c), ": Size ladder to 32M FAILED  ", Int((Runtime()-t0)/1000), "s\n");
fi;
QUIT_GAP(0);
