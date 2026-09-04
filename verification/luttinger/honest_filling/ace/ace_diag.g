LoadPackage("ace");;
F:=FreeGroup("a","b");; a:=F.1;; b:=F.2;;
SetInfoACELevel(3);
t := ACECosetTableFromGensAndRels([a,b], [a^2, b^3, (a*b)^5], [] : workspace := "3G", time := 30);;
Print("index=", Length(t[1]), "\n");
t := ACECosetTableFromGensAndRels([a,b], [a^2, b^3, (a*b)^5], [] : workspace := "1500M", time := 30);;
Print("index=", Length(t[1]), "\n");
QUIT;
