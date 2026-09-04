Read("generation_input.g");
Read("extra_words.g");
# Q~ : Q's generators plus the eight sheet loops as defined generators.
FF := FreeGroup("g1","g2","g3","x","y","r","s","A","B","M","N");;
gens := GeneratorsOfGroup(FF);;
toFF := GroupHomomorphismByImages(F, FF, GeneratorsOfGroup(F), gens{[1,2,3]});;
img := w -> Image(toFF, w);;
x:=FF.4;; y:=FF.5;; r:=FF.6;; s:=FF.7;; A:=FF.8;; B:=FF.9;; M:=FF.10;; N:=FF.11;;
Qrels := List(rels, img);;
defs := [ x^-1*img(w_x), y^-1*img(w_y), r^-1*img(w_r), s^-1*img(w_s), A^-1*img(w_A), B^-1*img(w_B), M^-1*img(w_M), N^-1*img(w_N) ];;
certified := [ A*x*A^-1*r^-1, A*y*A^-1*s^-1, A*r*A^-1*x^-1, A*s*A^-1*(N*y)^-1,
               B*y*B^-1*(M^-1*y*x)^-1, B*r*B^-1*r^-1, B*s*B^-1*(r^-1*M^-1*r*s)^-1, Comm(x,y)*Comm(r,s) ];;
xrel := [ B*x*B^-1*y ];;
Ngrid := img(w_alpha_s_grid_N);; lbs2 := img(w_lb_b_s2);;
alpha := rec( y1 := [img(w_geom_M), img(w_lb_a_y1)], y2 := [img(w_geom_M_y2), img(w_lb_a_y2)] );;
run := function(label, base, pkg, kind, cap)
  local eA, eB, fill, tab, out, t;
  out := [];
  for eA in [1,-1] do for eB in [1,-1] do
    if kind = "honest" then fill := [ alpha.(pkg)[1]*alpha.(pkg)[2]^eA, Ngrid^-1*lbs2^eB ];
    else fill := [ alpha.(pkg)[1]*alpha.(pkg)[2]^eA, img(w_geom_N)*lbs2^eB ]; fi;
    t := Runtime();
    tab := CosetTableFromGensAndRels(gens, Concatenation(base, fill), [] : max := cap, silent := true);
    if tab = fail then Add(out, Concatenation("overflow/", String(Runtime()-t), "ms"));
    else Add(out, Concatenation("index ", String(Length(tab[1])), "/", String(Runtime()-t), "ms")); fi;
  od; od;
  Print(label, " ", pkg, " ", kind, ": ", out, "\n");
end;;
base0 := Concatenation(Qrels, defs);;
base1 := Concatenation(base0, certified);;
base2 := Concatenation(base1, xrel);;
run("Q+defs+certified+xrel", base2, "y1", "sealed", 1000000);
run("Q+defs+certified+xrel", base2, "y1", "honest", 1000000);
run("Q+defs+certified      ", base1, "y1", "honest", 1000000);
run("Q+defs+certified+xrel", base2, "y2", "honest", 1000000);
run("Q+defs+certified      ", base1, "y2", "honest", 1000000);
run("Q+defs only           ", base0, "y1", "honest", 1000000);
QUIT;
