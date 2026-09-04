Read("generation_input.g");
Read("extra_words.g");
Q := F / rels;;
hom := GroupHomomorphismByImages(F, Q, GeneratorsOfGroup(F), GeneratorsOfGroup(Q));;
sheet := List([w_x, w_y, w_r, w_s, w_A, w_B, w_M, w_N], w -> Image(hom, w));;
iso := IsomorphismFpGroupByGenerators(Q, sheet, "h");;
P := Range(iso);;
FP := FreeGroupOfFpGroup(P);;
Print("P: ", Length(GeneratorsOfGroup(P)), " gens, ", Length(RelatorsOfFpGroup(P)), " relators, lengths ", List(RelatorsOfFpGroup(P), Length), "\n");
rw := w -> UnderlyingElement(Image(iso, Image(hom, w)));;
W := rec();;
for pair in [["geom_M_y2", w_geom_M_y2], ["lb_a_y2", w_lb_a_y2], ["geom_M", w_geom_M], ["lb_a_y1", w_lb_a_y1], ["Ngrid", w_alpha_s_grid_N], ["lbs2", w_lb_b_s2], ["geom_N", w_geom_N]] do
  W.(pair[1]) := rw(pair[2]);
  Print(pair[1], ": length ", Length(W.(pair[1])), "\n");
od;
# sanity: the sheet generators map to themselves, and A^-1 geom_N A = Ngrid^-1
hh := GeneratorsOfGroup(FP);;
Print("A^-1 geom_N A * Ngrid = 1 in FP? ", IsOne(hh[5]^-1*W.geom_N*hh[5]*W.Ngrid), "\n");
run := function(label, pkg, beta)
  local eA, eB, fill, tab, out, t, alpha;
  if pkg = "y1" then alpha := [W.geom_M, W.lb_a_y1]; else alpha := [W.geom_M_y2, W.lb_a_y2]; fi;
  out := [];
  for eA in [1,-1] do for eB in [1,-1] do
    if beta = "honest" then fill := [ alpha[1]*alpha[2]^eA, W.Ngrid^-1*W.lbs2^eB ];
    else fill := [ alpha[1]*alpha[2]^eA, W.geom_N*W.lbs2^eB ]; fi;
    t := Runtime();
    tab := CosetTableFromGensAndRels(hh, Concatenation(RelatorsOfFpGroup(P), fill), [] : max := 2000000, silent := true);
    if tab = fail then Add(out, Concatenation("overflow/", String(Runtime()-t), "ms"));
    else Add(out, Concatenation("index ", String(Length(tab[1])), "/", String(Runtime()-t), "ms")); fi;
  od; od;
  Print(label, " ", pkg, " ", beta, ": ", out, "\n");
end;;
run("P(Q on sheet loops)", "y1", "sealed");
run("P(Q on sheet loops)", "y1", "honest");
run("P(Q on sheet loops)", "y2", "sealed");
run("P(Q on sheet loops)", "y2", "honest");
PrintTo("P_relators.txt", List(RelatorsOfFpGroup(P), r -> String(r)));
PrintTo("P_words.txt", rec(geom_M_y2 := String(W.geom_M_y2), lb_a_y2 := String(W.lb_a_y2), geom_M := String(W.geom_M), lb_a_y1 := String(W.lb_a_y1), Ngrid := String(W.Ngrid), lbs2 := String(W.lbs2), geom_N := String(W.geom_N)));
QUIT;
