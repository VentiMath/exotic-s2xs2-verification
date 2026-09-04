Read("double_derived.g");
Print("H1 = ", AbelianInvariants(G), "\n");
CosetTableDefaultMaxLimit := 32000000;;
t0 := Runtime();;
res := CALL_WITH_CATCH(function() return Size(G); end, []);;
if res[1] then Print("|G| = ", res[2], "  ", Int((Runtime()-t0)/1000), "s\n");
else Print("Size ladder to 32M FAILED  ", Int((Runtime()-t0)/1000), "s\n"); fi;
QUIT_GAP(0);
