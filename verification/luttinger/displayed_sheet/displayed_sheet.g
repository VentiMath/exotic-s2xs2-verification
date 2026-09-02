# Coset enumeration of the DISPLAYED relation sheet (paper, "Relation sheet
# and product fillings"), independent of the sealed 78-relator presentation Q.
#
# Generators: fiber x, y, r, s ; base A, B ; meridians M, N.
# Words are transcribed literally from the paper.  [a,b] = a b a^-1 b^-1,
# matching the surface word x y x^-1 y^-1 r s r^-1 s^-1 in the paper.
#
# Runs, in order:
#   1. the ten displayed relations + fillings, all four sign sheets (eps_A, eps_B)
#   2. the same four sheets WITHOUT the drilled-fiber relation (feeds the
#      redundancy question raised separately; not needed for triviality)
#   3. negative controls: one filling only -> H_1 must be Z, never trivial
#
# This script asserts nothing about which sheet is pi_1 of a geometric object.

F := FreeGroup("x","y","r","s","A","B","M","N");;
x := F.1;; y := F.2;; r := F.3;; s := F.4;;
A := F.5;; B := F.6;; M := F.7;; N := F.8;;

surface  := x*y*x^-1*y^-1 * r*s*r^-1*s^-1;;
transport := [
  A*x*A^-1 * r^-1,                       # A x A^-1 = r
  A*y*A^-1 * s^-1,                       # A y A^-1 = s
  A*r*A^-1 * x^-1,                       # A r A^-1 = x
  A*s*A^-1 * (N*y)^-1,                   # A s A^-1 = N y
  B*x*B^-1 * y,                          # B x B^-1 = y^-1
  B*y*B^-1 * (M^-1*y*x)^-1,              # B y B^-1 = M^-1 y x
  B*r*B^-1 * r^-1,                       # B r B^-1 = r
  B*s*B^-1 * (r^-1*M^-1*r*s)^-1          # B s B^-1 = (r^-1 M^-1 r) s
];;
drilled  := B*(s^-1*r^-1*y*x)*B^-1 * (r^-1*s^-1*x)^-1;;   # drilled-fiber relation

lambda_alpha := A*x;;
lambda_beta  := (r^-1*M*r)*B;;

base_rels := Concatenation([surface], transport, [drilled]);;
base_rels_no_drilled := Concatenation([surface], transport);;

# Bound the enumeration so a genuinely hard case fails loudly instead of hanging.
CosetTableDefaultMaxLimit := 2000000;;

sign_name := function(e) if e = 1 then return "+"; else return "-"; fi; end;;

RunSheet := function(label, rels, eA, eB)
  local G, t0, t1, sz, ab, ms;
  G := F / Concatenation(rels, [ M*lambda_alpha^eA, N*lambda_beta^eB ]);
  t0 := NanosecondsSinceEpoch();
  sz := Size(G);
  t1 := NanosecondsSinceEpoch();
  ab := AbelianInvariants(G);
  ms := Int((t1 - t0) / 1000000);
  Print(label, " sheet (", sign_name(eA), ",", sign_name(eB), ")",
        "  relators=", Length(rels)+2,
        "  |G|=", sz, "  H1=", ab, "  coset-enum ", ms, " ms\n");
  return sz;
end;;

all_trivial := true;;

Print("=== 1. ten displayed relations + two fillings ===\n");
for eA in [1,-1] do for eB in [1,-1] do
  if RunSheet("full", base_rels, eA, eB) <> 1 then all_trivial := false; fi;
od; od;

Print("=== 2. same, WITHOUT the drilled-fiber relation ===\n");
for eA in [1,-1] do for eB in [1,-1] do
  if RunSheet("no-drilled", base_rels_no_drilled, eA, eB) <> 1 then all_trivial := false; fi;
od; od;

Print("=== 3. negative controls: single filling, H_1 must be infinite cyclic ===\n");
Ga := F / Concatenation(base_rels, [ M*lambda_alpha ]);;
Gb := F / Concatenation(base_rels, [ N*lambda_beta ]);;
Print("alpha filling only:  H1=", AbelianInvariants(Ga), "\n");
Print("beta  filling only:  H1=", AbelianInvariants(Gb), "\n");
controls_ok := AbelianInvariants(Ga) = [0] and AbelianInvariants(Gb) = [0];;

Print("=== summary ===\n");
Print("GAP ", GAPInfo.Version, "\n");
Print("all eight filled sheets trivial: ", all_trivial, "\n");
Print("single-filling controls infinite cyclic: ", controls_ok, "\n");
Print("RESULT: ", all_trivial and controls_ok, "\n");
QUIT;
