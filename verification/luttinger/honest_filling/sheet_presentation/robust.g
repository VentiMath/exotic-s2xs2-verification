F := FreeGroup("x","y","r","s","A","B","M","N");;
x:=F.1;; y:=F.2;; r:=F.3;; s:=F.4;; A:=F.5;; B:=F.6;; M:=F.7;; N:=F.8;;
names := ["AxA^-1=r","AyA^-1=s","ArA^-1=x","AsA^-1=Ny","BxB^-1=y^-1","ByB^-1=M^-1yx","BrB^-1=r","BsB^-1=r^-1M^-1rs","[x,y][r,s]"];;
sheet := [ A*x*A^-1*r^-1, A*y*A^-1*s^-1, A*r*A^-1*x^-1, A*s*A^-1*(N*y)^-1,
           B*x*B^-1*y, B*y*B^-1*(M^-1*y*x)^-1, B*r*B^-1*r^-1, B*s*B^-1*(r^-1*M^-1*r*s)^-1,
           Comm(x,y)*Comm(r,s) ];;
la := A*x;; lb := r^-1*M*r*B;;
test := function(rels, label)
  local eA, eB, tab, fill, out;
  out := [];
  for eA in [1,-1] do for eB in [1,-1] do
    fill := [ M*la^eA, A^-1*N*A*lb^eB ];
    tab := CosetTableFromGensAndRels(GeneratorsOfGroup(F), Concatenation(rels, fill), [] : max := 2000000, silent := true);
    if tab = fail then Add(out, "overflow"); else Add(out, String(Length(tab[1]))); fi;
  od; od;
  Print(label, ": indices (++,+-,-+,--) = ", out, "\n");
end;;
test(sheet, "full sheet");
for i in [1..Length(sheet)] do
  test(sheet{Difference([1..Length(sheet)],[i])}, Concatenation("drop ", names[i]));
od;
core := sheet{[1,2,3,4,6,7,8,9]};; test(core, "certified core (no BxB^-1 relation)");
QUIT;
