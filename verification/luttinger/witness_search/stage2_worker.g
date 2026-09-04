# stage2_worker.g — one (case, target) job.  Env: WS_CASE = index into CASES,
# WS_TARGET = a name from TARGETS, or "LI7" for low-index subgroups to index 7.
# Mirrors Wuebben's phase3_worker.g, including its ExcludedOrders pre-mark: GQuotients
# probes generator orders with a hard-coded 50,000-coset enumeration that these
# presentations blow past; marking every order as already TESTED (not excluded) makes
# that probe a no-op and cannot change the set of epimorphisms found.
Read("common.g");
ci := Int(GAPInfo.SystemEnvironment.WS_CASE);;
tname := GAPInfo.SystemEnvironment.WS_TARGET;;
c := CASES[ci];;
G := mkG(c.mn[1], c.mn[2], c.e[1], c.e[2], c.e[3], c.e[4], c.e[5]);;
iso := IsomorphismSimplifiedFpGroup(G);; H := Image(iso);;
sxo := StoredExcludedOrders(H);;
for i in [1..Length(sxo)] do UniteSet(sxo[i][2], [1..200]); od;
Print("=== case ", ci, " ", caseLabel(c), " target ", tname, " ", stamp(), " ===\n");
if tname = "LI7" then
  li := CALL_WITH_CATCH(LowIndexSubgroupsFpGroup, [H, 7]);
  if li[1] = true then
    Print("  low-index<=7: ", Length(li[2]), " subgroup(s) ", stamp(), "\n");
    if Length(li[2]) > 1 then Print("  >>> NONTRIVIAL (proper low-index subgroup) <<< ", stamp(), "\n"); fi;
  else Print("  low-index<=7 ERRORED ", stamp(), "\n"); fi;
else
  T := mkTarget(tname);;
  q := CALL_WITH_CATCH(GQuotients, [H, T]);
  if q[1] = true and Length(q[2]) > 0 then
    Print("  >>> NONTRIVIAL: onto ", tname, " (", Length(q[2]), " maps) <<< ", stamp(), "\n");
  elif q[1] = true then
    Print("  no quotient onto ", tname, " ", stamp(), "\n");
  else
    Print("  ", tname, " ERRORED ", stamp(), "\n");
  fi;
fi;
Print("JOB DONE case ", ci, " target ", tname, " ", stamp(), "\n");
QUIT_GAP(0);
