# Relation between the v2.5.0 double W (delta_1 = A^-1B^-1AB) and the derived double D (delta_0 = AB^-1A^-1B),
# in the free group on the four base letters.  Claim: modulo the derived relation delta0_L delta0_R = 1,
#     delta1_L delta1_R  =  A_L^-1 [delta0_L^-1, u] A_L,   u = A_L A_R^-1,   [a,b] = a b a^-1 b^-1.
# Checked as an exact free-group identity after substituting delta0_R -> delta0_L^-1 (both sides are
# words in A_L, B_L, A_R, B_R; the substitution is legitimate because it only uses the derived relation).
F := FreeGroup("AL", "BL", "AR", "BR");
AL := F.1; BL := F.2; AR := F.3; BR := F.4;
d0 := function(A, B) return A*B^-1*A^-1*B; end;
d1 := function(A, B) return A^-1*B^-1*A*B; end;
Print("delta_1 = A^-1 delta_0^-1 A (same copy): ", d1(AL,BL) = AL^-1*d0(AL,BL)^-1*AL, "\n");
u := AL*AR^-1;
lhs := d1(AL,BL) * d1(AR,BR);
# rewrite delta1_R = A_R^-1 delta0_R^-1 A_R and replace delta0_R^-1 by delta0_L (the derived relation)
lhs_mod := AL^-1*d0(AL,BL)^-1*AL * AR^-1*d0(AL,BL)*AR;
comm := function(a,b) return a*b*a^-1*b^-1; end;
rhs := AL^-1 * comm(d0(AL,BL)^-1, u) * AL;
Print("delta1_L delta1_R (with delta0_R := delta0_L^-1) = A_L^-1 [delta0_L^-1, u] A_L : ", lhs_mod = rhs, "\n");
# and the substitution itself: lhs * lhs_mod^-1 = c (delta0_L delta0_R)^-1 c^-1 with c = A_L^-1 delta0_L^-1 A_L A_R^-1,
# a conjugate of the inverse of the derived relator delta0_L delta0_R.
c := AL^-1*d0(AL,BL)^-1*AL*AR^-1;
Print("lhs * lhs_mod^-1 = c (delta0_L delta0_R)^-1 c^-1 : ", lhs*lhs_mod^-1 = c*(d0(AL,BL)*d0(AR,BR))^-1*c^-1, "\n");
