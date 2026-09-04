LoadPackage("ace");;
F:=FreeGroup("a","b");; a:=F.1;; b:=F.2;;
SetInfoACELevel(3);
for ws in ["500M","1G","1500M","2G","2500M","3G","4G"] do
  Print("WS ", ws, "\n");
  t := ACECosetTableFromGensAndRels([a,b], [a^2, b^3, (a*b)^5], [] : workspace := ws, time := 30);;
  Print("  ok index=", Length(t[1]), "\n");
od;
QUIT;
