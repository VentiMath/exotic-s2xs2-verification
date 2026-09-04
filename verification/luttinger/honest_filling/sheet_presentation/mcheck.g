Read("generation_input.g");
Q := F / rels;;
hom := GroupHomomorphismByImages(F, Q, GeneratorsOfGroup(F), GeneratorsOfGroup(Q));;
im := w -> Image(hom, w);;
words := rec( M := w_M, N := w_N, sheet_x := w_B*w_x*w_B^-1*w_y, corrected_x := w_B*w_x*w_B^-1*w_M^-1*w_y,
              drilled_printed := w_B*w_s^-1*w_r^-1*w_y*w_x*w_B^-1*(w_r^-1*w_s^-1*w_x)^-1,
              drilled_corrected := w_B*w_s^-1*w_r^-1*w_y*w_x*w_B^-1*(w_r^-1*w_s^-1*w_x*w_M)^-1 );;
for t in [ ["S3", SymmetricGroup(3)], ["S4", SymmetricGroup(4)], ["A5", AlternatingGroup(5)], ["PSL(2,7)", PSL(2,7)], ["A6", AlternatingGroup(6)], ["PSL(2,8)", PSL(2,8)], ["PSL(2,11)", PSL(2,11)], ["S5", SymmetricGroup(5)], ["S6", SymmetricGroup(6)], ["A7", AlternatingGroup(7)] ] do
  epis := GQuotients(Q, t[2]);
  out := [];
  for n in RecNames(words) do
    Add(out, Concatenation(n, " nontrivial in ", String(Number(epis, e -> not IsOne(Image(e, im(words.(n)))))), "/", String(Length(epis))));
  od;
  Print(t[1], ": ", out, "\n");
od;
QUIT;
