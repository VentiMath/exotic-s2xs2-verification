LoadPackage("ace");;
F:=FreeGroup("a","b");; a:=F.1;; b:=F.2;;
W:=function(l) local w,i; w:=One(F); for i in l do if i>0 then w:=w*GeneratorsOfGroup(F)[i]; else w:=w*GeneratorsOfGroup(F)[-i]^-1; fi; od; return w; end;;
rels:=List([[-1, -1, -2, -2, 1, 2, 2, 1, -2, -2, -2, -1, 2, 2, 1, -2, 1, 2, 2], [-2, -1, -2, -2, 1, 2, 2, 1, -2, -2, -1, 2, 2, 1, 2, 2, -1, -2, -2, -1, 2, 2, 1, -2], [-1, -2, -2, -2, -2, 1, 2, 2, 1, -2, -2, -1, 2, -1, 2, 2, 1, 2, -1, -2, -2, 1, 2, 2, 1, -2], [-2, -2, 1, -2, -1, 2, 2, 1, -2, 1, 2, 2, 2, 2, -1, -2, -2, -1, 2, 2, 2, 2, 1, -2, -1, -1, -2, -2, 1], [2, 2, 1, -2, -1, -1, -2, -2, 1, 1, 2, 2, -1, -1, -2, -2, -1, 2, 2, 1, 1, -2, -1, 2, 2, 1, 2, -1, -2, -2, -1, 2, 2, 1, -2, -2, 1, 2, -1]],W);;

Try := function(label, sgens, strat)
  local t;
  Print("START ", label, " ", strat, "\n");
  if strat = "felsch" then
    t := ACECosetTableFromGensAndRels([a,b], rels, sgens : felsch := 1, workspace := "2G", time := 900, silent);
  else
    t := ACECosetTableFromGensAndRels([a,b], rels, sgens : hard, workspace := "2G", time := 900, silent);
  fi;
  if t = fail then Print("RESULT ", label, " ", strat, " INCONCLUSIVE\n");
  else Print("RESULT ", label, " ", strat, " INDEX ", Length(t[1]), "\n"); fi;
  return t;
end;;
t := Try("<a>", [a], "felsch");
if t = fail then t := Try("<b>", [b], "felsch"); fi;
if t = fail then t := Try("trivial", [], "felsch"); fi;
if t = fail then t := Try("<a>", [a], "hard"); fi;
Print("ACE DONE\n");
QUIT;

