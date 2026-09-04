F := FreeGroup("x","y","r","s","A","B","M","N");;
x:=F.1;; y:=F.2;; r:=F.3;; s:=F.4;; A:=F.5;; B:=F.6;; M:=F.7;; N:=F.8;;
relations := [
  A^1*x^1*A^-1*r^-1,
  A^1*y^1*A^-1*s^-1,
  A^1*r^1*A^-1*x^-1,
  A^1*s^1*A^-1*y^-1*N^-1,
  B^1*y^1*B^-1*x^-1*y^-1*M^1,
  B^1*r^1*B^-1*r^-1,
  B^1*s^1*B^-1*s^-1*r^-1*M^1*r^1,
  x^1*y^1*x^-1*y^-1*r^1*s^1*r^-1*s^-1,
  A^-1*r^1*A^1*x^-1,
  s^1*A^1*y^-1*A^-1,
  B^1*r^-1*B^-1*r^1,
  A^1*M^1*x^-1*A^-1*M^-1*r^1,
  x^1*M^1*A^-1*r^-1*M^-1*A^1,
  M^-1*A^1*r^-1*M^1*r^1*A^-1,
  M^1*B^1*y^1*B^-1*x^-1*y^-1,
  s^1*B^-1*s^-1*r^-1*M^1*B^1*r^1,
  x^1*M^1*B^1*y^-1*x^-1*s^1*B^-1*s^-1,
  r^-1*B^1*A^1*x^1*r^1*A^-1*y^1*B^-1*x^-1,
  y^1*B^-1*x^-1*B^1*x^1*A^1*y^-1*x^-1*A^-1*r^1*s^1,
  s^1*r^1*s^-1*r^-1*N^-1*A^1*s^1*A^-1*x^1*y^-1*x^-1,
  s^1*r^-1*s^-1*r^-1*A^1*x^1*y^1*x^1*y^-1*x^-1*A^-1*r^1,
  x^1*y^1*x^1*y^-1*x^-1*r^-1*A^1*x^1*y^1*x^1*y^-1*x^-1*r^-1*A^-1,
  r^1*s^1*A^1*B^-1*x^-1*A^-1*M^-1*y^1*r^1*A^1*B^1*A^-1*s^-1*r^-1*y^-1,
  M^1*B^1*A^1*x^1*y^1*x^1*y^-1*x^-1*A^-1*B^-1*M^-1*A^-1*x^1*y^1*x^-1*y^-1*x^-1*A^1,
  r^-1*A^1*x^1*y^1*x^1*y^-1*x^-1*r^-1*y^1*x^1*y^-1*x^-1*A^-1*y^1*B^-1*x^1*B^1*y^-1*x^1*y^-1*x^-1,
  r^-1*B^-1*M^-1*A^1*A^1*M^1*r^1*A^-1*r^1*A^-1*B^1*y^-1*x^-1,
  B^1*x^1*B^-1*M^-1*y^1,
  B^1*s^-1*r^-1*y^1*x^1*B^-1*M^-1*x^-1*s^1*r^1,
  M^1*A^1*x^1*M^-1*x^-1*A^-1,
  A^-1*N^1*A^1*r^-1*M^1*r^1*B^1*A^-1*N^-1*A^1*B^-1*r^-1*M^-1*r^1
];;
out := "";;
G := F / Concatenation(relations, [M^1*A^1*x^1, A^-1*N^1*A^1*r^-1*M^1*r^1*B^1]);; P := PresentationFpGroup(G);; TzOptions(P).printLevel := 0;; TzInitGeneratorImages(P);; TzGoGo(P);; TzGoGo(P);;
H := FpGroupPresentation(P);; rels := List(RelatorsOfFpGroup(H), r -> LetterRepAssocWord(r));;
imgs := List(TzImagesOldGens(P), w -> LetterRepAssocWord(w));; pre := List(TzPreImagesNewGens(P), w -> LetterRepAssocWord(w));;
AppendTo("reduced_presentations.txt", "honest_y1_p1_p1|", Length(GeneratorsOfGroup(H)), "|", rels, "|", imgs, "|", pre, "\n");;
G := F / Concatenation(relations, [M^1*A^1*x^1, A^-1*N^1*A^1*B^-1*r^-1*M^-1*r^1]);; P := PresentationFpGroup(G);; TzOptions(P).printLevel := 0;; TzInitGeneratorImages(P);; TzGoGo(P);; TzGoGo(P);;
H := FpGroupPresentation(P);; rels := List(RelatorsOfFpGroup(H), r -> LetterRepAssocWord(r));;
imgs := List(TzImagesOldGens(P), w -> LetterRepAssocWord(w));; pre := List(TzPreImagesNewGens(P), w -> LetterRepAssocWord(w));;
AppendTo("reduced_presentations.txt", "honest_y1_p1_m1|", Length(GeneratorsOfGroup(H)), "|", rels, "|", imgs, "|", pre, "\n");;
G := F / Concatenation(relations, [M^1*x^-1*A^-1, A^-1*N^1*A^1*r^-1*M^1*r^1*B^1]);; P := PresentationFpGroup(G);; TzOptions(P).printLevel := 0;; TzInitGeneratorImages(P);; TzGoGo(P);; TzGoGo(P);;
H := FpGroupPresentation(P);; rels := List(RelatorsOfFpGroup(H), r -> LetterRepAssocWord(r));;
imgs := List(TzImagesOldGens(P), w -> LetterRepAssocWord(w));; pre := List(TzPreImagesNewGens(P), w -> LetterRepAssocWord(w));;
AppendTo("reduced_presentations.txt", "honest_y1_m1_p1|", Length(GeneratorsOfGroup(H)), "|", rels, "|", imgs, "|", pre, "\n");;
G := F / Concatenation(relations, [M^1*x^-1*A^-1, A^-1*N^1*A^1*B^-1*r^-1*M^-1*r^1]);; P := PresentationFpGroup(G);; TzOptions(P).printLevel := 0;; TzInitGeneratorImages(P);; TzGoGo(P);; TzGoGo(P);;
H := FpGroupPresentation(P);; rels := List(RelatorsOfFpGroup(H), r -> LetterRepAssocWord(r));;
imgs := List(TzImagesOldGens(P), w -> LetterRepAssocWord(w));; pre := List(TzPreImagesNewGens(P), w -> LetterRepAssocWord(w));;
AppendTo("reduced_presentations.txt", "honest_y1_m1_m1|", Length(GeneratorsOfGroup(H)), "|", rels, "|", imgs, "|", pre, "\n");;
G := F / Concatenation(relations, [y^-1*M^1*y^1*y^-1*A^1*r^-1*y^1, A^-1*N^1*A^1*r^-1*M^1*r^1*B^1]);; P := PresentationFpGroup(G);; TzOptions(P).printLevel := 0;; TzInitGeneratorImages(P);; TzGoGo(P);; TzGoGo(P);;
H := FpGroupPresentation(P);; rels := List(RelatorsOfFpGroup(H), r -> LetterRepAssocWord(r));;
imgs := List(TzImagesOldGens(P), w -> LetterRepAssocWord(w));; pre := List(TzPreImagesNewGens(P), w -> LetterRepAssocWord(w));;
AppendTo("reduced_presentations.txt", "honest_y2_p1_p1|", Length(GeneratorsOfGroup(H)), "|", rels, "|", imgs, "|", pre, "\n");;
G := F / Concatenation(relations, [y^-1*M^1*y^1*y^-1*A^1*r^-1*y^1, A^-1*N^1*A^1*B^-1*r^-1*M^-1*r^1]);; P := PresentationFpGroup(G);; TzOptions(P).printLevel := 0;; TzInitGeneratorImages(P);; TzGoGo(P);; TzGoGo(P);;
H := FpGroupPresentation(P);; rels := List(RelatorsOfFpGroup(H), r -> LetterRepAssocWord(r));;
imgs := List(TzImagesOldGens(P), w -> LetterRepAssocWord(w));; pre := List(TzPreImagesNewGens(P), w -> LetterRepAssocWord(w));;
AppendTo("reduced_presentations.txt", "honest_y2_p1_m1|", Length(GeneratorsOfGroup(H)), "|", rels, "|", imgs, "|", pre, "\n");;
G := F / Concatenation(relations, [y^-1*M^1*y^1*y^-1*r^1*A^-1*y^1, A^-1*N^1*A^1*r^-1*M^1*r^1*B^1]);; P := PresentationFpGroup(G);; TzOptions(P).printLevel := 0;; TzInitGeneratorImages(P);; TzGoGo(P);; TzGoGo(P);;
H := FpGroupPresentation(P);; rels := List(RelatorsOfFpGroup(H), r -> LetterRepAssocWord(r));;
imgs := List(TzImagesOldGens(P), w -> LetterRepAssocWord(w));; pre := List(TzPreImagesNewGens(P), w -> LetterRepAssocWord(w));;
AppendTo("reduced_presentations.txt", "honest_y2_m1_p1|", Length(GeneratorsOfGroup(H)), "|", rels, "|", imgs, "|", pre, "\n");;
G := F / Concatenation(relations, [y^-1*M^1*y^1*y^-1*r^1*A^-1*y^1, A^-1*N^1*A^1*B^-1*r^-1*M^-1*r^1]);; P := PresentationFpGroup(G);; TzOptions(P).printLevel := 0;; TzInitGeneratorImages(P);; TzGoGo(P);; TzGoGo(P);;
H := FpGroupPresentation(P);; rels := List(RelatorsOfFpGroup(H), r -> LetterRepAssocWord(r));;
imgs := List(TzImagesOldGens(P), w -> LetterRepAssocWord(w));; pre := List(TzPreImagesNewGens(P), w -> LetterRepAssocWord(w));;
AppendTo("reduced_presentations.txt", "honest_y2_m1_m1|", Length(GeneratorsOfGroup(H)), "|", rels, "|", imgs, "|", pre, "\n");;
QUIT;
