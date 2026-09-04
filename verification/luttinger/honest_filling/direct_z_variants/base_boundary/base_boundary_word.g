# The audit base complex (bundle.py docstring + r_run.py geometric_paper_candidates):
#   annulus  a(i,j): angular copy i in {0,1,2} (edge 2->0 is the phi0 edge), radius j in {0,1,2};
#   band     s(l,k): stack level l in {0,1,2}, thickness k in {0,1,2};
#   feet     s(0,k) = a(k,2), s(2,k) = a(k,0).
# Loops based at q = a(0,2):
#   alpha_positive = a(0,2) a(1,2) a(2,2) a(0,2);   A = its inverse (r_run.py: geom_A = reversed)
#   beta_positive  = a(0,2) a(1,2) s(1,1) a(1,0) a(1,1) a(1,2) a(0,2);   B = its inverse
#   boundary       = the free edges: phi0 edge at J2, band side k=2, phi0 edge at J0, band side k=0.
# Edge-path group via a free group on oriented edges, relators = 2-cell boundaries.
verts := [];
for i in [0..2] do for j in [0..2] do Add(verts, ["a",i,j]); od; od;
for k in [0..2] do Add(verts, ["s",1,k]); od;
name := function(v)
  if v[1] = "s" and v[2] = 0 then return ["a", v[3], 2]; fi;
  if v[1] = "s" and v[2] = 2 then return ["a", v[3], 0]; fi;
  return v;
end;
edges := [];
addE := function(u, v) local e; e := [name(u), name(v)];
  if not (e in edges or Reversed(e) in edges) then Add(edges, e); fi; end;
for j in [0..2] do for i in [0..2] do addE(["a",i,j], ["a",(i+1) mod 3, j]); od; od;
for i in [0..2] do for j in [0..1] do addE(["a",i,j], ["a",i,j+1]); od; od;
for k in [0..2] do for l in [0..1] do addE(["s",l,k], ["s",l+1,k]); od; od;
for k in [0..1] do addE(["s",1,k], ["s",1,k+1]); od;
faces := [];
for i in [0..2] do for j in [0..1] do
  Add(faces, [["a",i,j], ["a",(i+1) mod 3,j], ["a",(i+1) mod 3,j+1], ["a",i,j+1]]); od; od;
for l in [0..1] do for k in [0..1] do
  Add(faces, [["s",l,k], ["s",l+1,k], ["s",l+1,k+1], ["s",l,k+1]]); od; od;
Print("V=", Length(verts), " E=", Length(edges), " F=", Length(faces),
      " chi=", Length(verts)-Length(edges)+Length(faces), "\n");
F := FreeGroup(Length(edges));
g := GeneratorsOfGroup(F);
edgeElt := function(u, v) local e, p;
  e := [name(u), name(v)]; p := Position(edges, e);
  if p <> fail then return g[p]; fi;
  p := Position(edges, Reversed(e)); return g[p]^-1; end;
pathElt := function(path) local w, t;
  w := One(F);
  for t in [1..Length(path)-1] do w := w * edgeElt(path[t], path[t+1]); od;
  return w; end;
rels := List(faces, f -> pathElt(Concatenation(f, [f[1]])));
# boundary edges: those in exactly one face
count := List(edges, e -> 0);
for f in faces do for t in [1..4] do
  e := [name(f[t]), name(f[(t mod 4)+1])];
  p := Position(edges, e); if p = fail then p := Position(edges, Reversed(e)); fi;
  count[p] := count[p] + 1; od; od;
Print("boundary edges: ", Filtered([1..Length(edges)], p -> count[p] = 1), "\n");
Print("  ", List(Filtered([1..Length(edges)], p -> count[p] = 1), p -> edges[p]), "\n");
# a maximal tree: kill all edges from a BFS tree rooted at q
q := ["a",0,2];
tree := []; seen := [q]; queue := [q];
while Length(queue) > 0 do
  u := Remove(queue, 1);
  for e in edges do
    if e[1] = u and not e[2] in seen then Add(tree, e); Add(seen, e[2]); Add(queue, e[2]); fi;
    if e[2] = u and not e[1] in seen then Add(tree, e); Add(seen, e[1]); Add(queue, e[1]); fi;
  od;
od;
Append(rels, List(tree, e -> g[Position(edges, e)]));
G := F / rels;
iso := IsomorphismSimplifiedFpGroup(G);
H := Range(iso);
Print("pi_1(base) simplified: ", Length(GeneratorsOfGroup(H)), " generators, ",
      Length(RelatorsOfFpGroup(H)), " relators\n");
img := w -> Image(iso, Image(EpimorphismFromFreeGroup(G), w));
# hmm: map F -> G is the natural one
toG := GroupHomomorphismByImages(F, G, g, GeneratorsOfGroup(G));
img := w -> Image(iso, Image(toG, w));
alphaP := img(pathElt([["a",0,2],["a",1,2],["a",2,2],["a",0,2]]));
betaP  := img(pathElt([["a",0,2],["a",1,2],["s",1,1],["a",1,0],["a",1,1],["a",1,2],["a",0,2]]));
bdry   := img(pathElt([["a",0,2],["a",2,2],["s",1,2],["a",2,0],["a",0,0],["s",1,0],["a",0,2]]));
A := alphaP^-1;  B := betaP^-1;
Print("alpha_positive = ", alphaP, "\nbeta_positive  = ", betaP, "\nboundary       = ", bdry, "\n");
cands := rec(AiBiAB := A^-1*B^-1*A*B, BiABAi := B^-1*A*B*A^-1, ABAiBi := A*B*A^-1*B^-1, BAiBiA := B*A^-1*B^-1*A,
             BiAiBA := B^-1*A^-1*B*A, AiBABi := A^-1*B*A*B^-1, BABiAi := B*A*B^-1*A^-1, ABiAiB := A*B^-1*A^-1*B);
for n in RecNames(cands) do
  if cands.(n) = bdry then Print("boundary loop based at q  =  ", n, "  (in A, B)\n"); fi;
  if cands.(n) = bdry^-1 then Print("boundary loop based at q  =  (", n, ")^-1  (in A, B)\n"); fi;
od;
Print("A,B generate pi_1(base): ", Index(H, Subgroup(H, [A, B])) = 1, "\n");
