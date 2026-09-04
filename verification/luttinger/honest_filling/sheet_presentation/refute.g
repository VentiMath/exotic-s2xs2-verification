Read("generation_input.g");
Read("fillings_words.g");
Q := F / rels;;
hom := GroupHomomorphismByImages(F, Q, GeneratorsOfGroup(F), GeneratorsOfGroup(Q));;
tests := [ ["S3", SymmetricGroup(3)], ["S4", SymmetricGroup(4)], ["A5", AlternatingGroup(5)], ["PSL(2,7)", PSL(2,7)], ["A6", AlternatingGroup(6)],
           ["PSL(2,8)", PSL(2,8)], ["PSL(2,11)", PSL(2,11)], ["PSL(2,13)", PSL(2,13)], ["A7", AlternatingGroup(7)], ["S5", SymmetricGroup(5)],
           ["SL(2,3)", SL(2,3)], ["D8", DihedralGroup(8)], ["Q8", QuaternionGroup(8)], ["C3xS3", DirectProduct(CyclicGroup(3),SymmetricGroup(3))],
           ["S6", SymmetricGroup(6)], ["PSL(3,3)", PSL(3,3)], ["M11", MathieuGroup(11)], ["PSL(2,16)", PSL(2,16)], ["PSL(2,17)", PSL(2,17)], ["A8", AlternatingGroup(8)] ];;
for t in tests do
  epis := GQuotients(Q, t[2]);
  kh := []; ks := [];
  for name in RecNames(honest) do
    n := Number(epis, e -> IsOne(Image(e, Image(hom, honest.(name)[1]))) and IsOne(Image(e, Image(hom, honest.(name)[2]))));
    if n > 0 then Add(kh, Concatenation(name, ":", String(n))); fi;
  od;
  for name in RecNames(sealed) do
    n := Number(epis, e -> IsOne(Image(e, Image(hom, sealed.(name)[1]))) and IsOne(Image(e, Image(hom, sealed.(name)[2]))));
    if n > 0 then Add(ks, Concatenation(name, ":", String(n))); fi;
  od;
  Print(t[1], ": ", Length(epis), " epis; honest cases surviving: ", kh, "; sealed cases surviving (must be none): ", ks, "\n");
od;
QUIT;
