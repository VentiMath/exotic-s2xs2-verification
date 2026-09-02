# generation_check.g — do the eight named loops generate pi_1(C_aud)?
#
# Q is the sealed three-generator, 78-relator presentation of the torus
# complement (Lemma "complement presentation"); w_x .. w_N are the eight
# named loops x, y, r, s, A, B, M, N as the Tietze certificate transports
# them into Q.  Coset enumeration of Q over the subgroup they generate must
# terminate with index 1.  The second enumeration shows that the six loops
# without the meridians already generate, as the relations
# A s A^-1 = N y and B y B^-1 = M^-1 y x predict.
Read("generation_input.g");
Q := F / rels;;
hom := GroupHomomorphismByImages(F, Q, GeneratorsOfGroup(F), GeneratorsOfGroup(Q));;
imgs := List([w_x, w_y, w_r, w_s, w_A, w_B, w_M, w_N], w -> Image(hom, w));;
CosetTableDefaultMaxLimit := 4000000;;
i8 := Index(Q, Subgroup(Q, imgs));;
i6 := Index(Q, Subgroup(Q, imgs{[1..6]}));;
Print("index of <x,y,r,s,A,B,M,N> in Q: ", i8, "\n");
Print("index of <x,y,r,s,A,B> in Q:     ", i6, "\n");
if i8 = 1 and i6 = 1 then Print("GENERATION CHECK PASSED\n"); else Print("GENERATION CHECK FAILED\n"); fi;

# Second check: the drilled-fiber relation is a consequence of the four
# B-transport relations and the surface relation (paper, Lemma "the relation
# sheet").  Both steps are identities in a free group, hence decidable by free
# reduction alone.  [a,b] = a b a^-1 b^-1 as in the paper.
#   (a) conjugating s^-1 r^-1 y x by B letter by letter, i.e. applying the
#       substitution subst: x -> y^-1, y -> M^-1 y x, r -> r, s -> r^-1 M^-1 r s
#       that the four B-transport relations define, gives s^-1 r^-1 y x y^-1;
#   (b) s^-1 r^-1 y x y^-1 (r^-1 s^-1 x)^-1 is an explicit conjugate of the
#       inverse of the surface relator.
FF := FreeGroup("x","y","r","s","M");;
x := FF.1;; y := FF.2;; r := FF.3;; s := FF.4;; M := FF.5;;
subst := GroupHomomorphismByImages(FF, FF, [x, y, r, s, M], [y^-1, M^-1*y*x, r, r^-1*M^-1*r*s, M]);;
lhs := Image(subst, s^-1*r^-1*y*x);;
stepA := lhs = s^-1*r^-1*y*x*y^-1;;
comm := function(a, b) return a*b*a^-1*b^-1; end;;
surface := comm(x, y) * comm(r, s);;
W := s^-1*r^-1*y*x*y^-1 * (r^-1*s^-1*x)^-1;;
g := s^-1*r^-1*comm(s, r)^-1;;
stepB := W = g * surface^-1 * g^-1;;
Print("(a) subst(s^-1 r^-1 y x) = s^-1 r^-1 y x y^-1 in the free group: ", stepA, "\n");
Print("(b) residual is a conjugate of the inverse surface relator:   ", stepB, "\n");
if stepA and stepB then Print("DERIVATION CHECK PASSED\n"); else Print("DERIVATION CHECK FAILED\n"); fi;
QUIT_GAP(0);
