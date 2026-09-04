Read("double_derived.g");
for k in [2,3,4,5] do
  t0 := Runtime();
  li := CALL_WITH_CATCH(LowIndexSubgroupsFpGroup, [G, k]);
  if li[1] then Print("low-index <= ", k, ": ", Length(li[2]), " subgroup(s)  ", Int((Runtime()-t0)/1000), "s\n");
  else Print("low-index <= ", k, " ERRORED  ", Int((Runtime()-t0)/1000), "s\n"); fi;
od;
QUIT_GAP(0);
