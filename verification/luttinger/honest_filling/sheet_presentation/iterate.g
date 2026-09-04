CosetTableDefaultMaxLimit := 6000000;;
F:=FreeGroup("a","b");;
W:=function(l) local w,i; w:=One(F); for i in l do if i>0 then w:=w*GeneratorsOfGroup(F)[i]; else w:=w*GeneratorsOfGroup(F)[-i]^-1; fi; od; return w; end;;
G:=F/List([[-1, -1, -2, -2, 1, 2, 2, 1, -2, -2, -2, -1, 2, 2, 1, -2, 1, 2, 2], [-2, -1, -2, -2, 1, 2, 2, 1, -2, -2, -1, 2, 2, 1, 2, 2, -1, -2, -2, -1, 2, 2, 1, -2], [-1, -2, -2, -2, -2, 1, 2, 2, 1, -2, -2, -1, 2, -1, 2, 2, 1, 2, -1, -2, -2, 1, 2, 2, 1, -2], [-2, -2, 1, -2, -1, 2, 2, 1, -2, 1, 2, 2, 2, 2, -1, -2, -2, -1, 2, 2, 2, 2, 1, -2, -1, -1, -2, -2, 1], [2, 2, 1, -2, -1, -1, -2, -2, 1, 1, 2, 2, -1, -1, -2, -2, -1, 2, 2, 1, 1, -2, -1, 2, 2, 1, 2, -1, -2, -2, -1, 2, 2, 1, -2, -2, 1, 2, -1]],W);;

PStatus := function(G, tag)
  local r; r := RelatorsOfFpGroup(G);
  Print(tag, " ngens=", Length(GeneratorsOfGroup(G)), " nrels=", Length(r), " total=", Sum(r, Length), " ab=", AbelianInvariants(G), "\n");
end;;
PowerRound := function(G)
  local gens, fgens, rels, n, j, k, cand, t, iso, H, P, H2, tag;
  gens := GeneratorsOfGroup(G); fgens := FreeGeneratorsOfFpGroup(G); rels := RelatorsOfFpGroup(G); n := Length(gens);
  for k in [2,3] do
    for j in [1..n] do
      cand := ShallowCopy(fgens); cand[j] := fgens[j]^k;
      t := CosetTableFromGensAndRels(fgens, rels, cand : max := 6000000, silent := true);
      if t <> fail then
        tag := Concatenation("  sub gen", String(j), "^", String(k));
        Print(tag, " index=", Length(t[1]), "\n");
        if Length(t[1]) = 1 then
          iso := IsomorphismFpGroupByGenerators(G, List([1..n], i -> gens[1]^0 * ElementOfFpGroup(FamilyObj(gens[1]), cand[i])), "c");
          H := Range(iso);
          P := PresentationFpGroup(H); TzOptions(P).printLevel := 0; TzGoGo(P);
          H2 := FpGroupPresentation(P);
          PStatus(H2, Concatenation("  -> after MTC on ", tag, " + TzGoGo:"));
          return H2;
        fi;
      else
        Print("  sub gen", j, "^", k, " overflow\n");
      fi;
    od;
  od;
  return fail;
end;;
PStatus(G, "round0");
for rnd in [1..8] do
  H := PowerRound(G);
  if H = fail then Print("no completing candidate at rnd ", rnd, "\n"); break; fi;
  G := H;
  PStatus(G, Concatenation("rnd", String(rnd)));
  if Length(GeneratorsOfGroup(G)) = 0 then Print("TRIVIAL\n"); break; fi;
  if Length(GeneratorsOfGroup(G)) = 1 then Print("CYCLIC rels=", RelatorsOfFpGroup(G), "\n"); break; fi;
od;
QUIT;

