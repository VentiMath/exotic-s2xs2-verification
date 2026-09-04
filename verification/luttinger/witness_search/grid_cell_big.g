# grid_cell_big.g — one (n, m) cell of the displayed (+,+) sheet with a single large
# fixed coset ceiling (env GC_N, GC_M, GC_MAX), classic enumerator, silent fail on overflow.
# Written to test whether the n = -1 cells that overflow 32M cosets close at a larger table.
Read("common.g");
BreakOnError := false;;
n := Int(GAPInfo.SystemEnvironment.GC_N);; m := Int(GAPInfo.SystemEnvironment.GC_M);;
lim := Int(GAPInfo.SystemEnvironment.GC_MAX);;
G := mkG(m, n, 1, -1, -1, 1, 1);;
Print("cell (n,m)=(", n, ",", m, "), ceiling ", lim, ", ", stamp(), "\n");
t0 := Runtime();;
tab := CosetTableFromGensAndRels(FreeGeneratorsOfFpGroup(G), RelatorsOfFpGroup(G), [] : max := lim, silent := true);;
if tab = fail then Print("(n,m)=(", n, ",", m, "): overflow at ", lim, " cosets, ", Int((Runtime()-t0)/1000), "s\n");
else Print("(n,m)=(", n, ",", m, "): |G|=", Length(tab[1]), "  closed under ", lim, " cosets, ", Int((Runtime()-t0)/1000), "s\n"); fi;
QUIT_GAP(0);
