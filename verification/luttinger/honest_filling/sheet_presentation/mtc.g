Read("generation_input.g");
Read("extra_words.g");
Q := F / rels;;
hom := GroupHomomorphismByImages(F, Q, GeneratorsOfGroup(F), GeneratorsOfGroup(Q));;
sheet := List([w_x, w_y, w_r, w_s, w_A, w_B, w_M, w_N], w -> Image(hom, w));;
t := Runtime();
iso := IsomorphismFpGroupByGenerators(Q, sheet, "h");;
P := Range(iso);;
Print("presentation of Q on the sheet loops: ", Length(GeneratorsOfGroup(P)), " generators, ", Length(RelatorsOfFpGroup(P)), " relators, ", Runtime()-t, " ms\n");
for pair in [["geom_M_y2", w_geom_M_y2], ["lb_a_y2", w_lb_a_y2], ["geom_M", w_geom_M], ["lb_a_y1", w_lb_a_y1], ["alpha_s_grid_N", w_alpha_s_grid_N], ["lb_b_s2", w_lb_b_s2], ["mu_b", w_mu_b], ["lb_b", w_lb_b]] do
  Print(pair[1], " = ", Image(iso, Image(hom, pair[2])), "\n");
od;
Print("relators of P:\n"); for r in RelatorsOfFpGroup(P) do Print("  ", r, "\n"); od;
QUIT;
