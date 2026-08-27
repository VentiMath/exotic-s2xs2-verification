# Wuebben arXiv:2608.17267 — construction data for the target run

Fiber F: regular octagon, edge word x y x⁻¹ y⁻¹ r s r⁻¹ s⁻¹ (edges E₁..E₈, all
vertices = p). π₁(F,p) = ⟨x,y,r,s | [x,y][r,s]⟩, [u,v]=uvu⁻¹v⁻¹.
φ₀ = rotation by π: E_i → E_{i+4}; on π₁: x↔r, y↔s exactly. Fix(φ₀)={p,O}.
ψ₀ = T_a ∘ T_b (T_b first), supported in the left handle, fixes p, O and the
right handle pointwise. Based action ψ̃ = h∗id: x↦y⁻¹, y↦yx, r↦r, s↦s.
h([x,y]) = [x,y] exactly; h⁶ = conj_{[x,y]⁻¹}.
Five-chain (LP dictionary): a∼x, b∼y, e∼r, d∼s, c∼xr; [z]=[y]−[s] (unused).
c = γ ∪ ρ(γ), γ joins the y-edge pair to the s-edge pair; based word of c at
V₂ is (rx)⁻¹ (crosses E₈ then E₄).
Intersection data: c meets the y-edge once (c_y) and the s-edge once (c_s);
e meets the s-edge once (s_e); on the s-edge c_s precedes s_e; x, r miss c;
x, y, r miss e.

Base T₀: square [0,1]² minus a disc, basepoint q=(1/4,1/4); A := [ᾱ]⁻¹,
B := [β̄]⁻¹ so that BgB⁻¹ = ψ̃(g)·corr, AgA⁻¹ = φ̃(g)·corr.
T_α = c × {α-cut} (φ₀|c a free half-rotation); T_β = e × {β-cut} (product).

π₁(R) (Prop 3.5): ⟨x,y,r,s,A,B | [x,y][r,s], A g A⁻¹ = φ̃(g), B g B⁻¹ = ψ̃(g)⟩.

Derived words (§8.3–8.5; Table 1), with M the meridian of T_α based along y₁
(initial segment of y to c_y), N the meridian of T_β based along s₂, δ = r⁻¹:
  clean:     AxA⁻¹=r, AyA⁻¹=s, ArA⁻¹=x, BxB⁻¹=y⁻¹, BrB⁻¹=r
  corrected: AsA⁻¹ = N^± y,  ByB⁻¹ = M^± (yx),  BsB⁻¹ = (δ M^ε δ⁻¹) s
  R3 (invariant curve): B (s⁻¹r⁻¹yx) B⁻¹ = r⁻¹s⁻¹x
  dir_base(T_β) = (δ M^{−ε} δ⁻¹) B,   dir_fib(T_β) = s r⁻¹ s⁻¹
  dir_base(T_α) = A x,                 dir_fib(T_α) = (rx)⁻¹
  surgery relators (variant (0,0)):  M·(Ax)^{ε_A},  N·((δM^{−ε}δ⁻¹)B)^{ε_B}
Repo encoding: scripts/fixed_v_certify.g, scripts/develop.py
(github.com/bwuebben/exotic-s2xs2).  All 32 sign assignments give |G|=1.

What the target run must reproduce *from the triangulation alone*: the three
corrected relations (which relations get a meridian, with which conjugating
path), the two dir_base words (in particular the half-drift x in Ax and the
anti-coupled M-correction in dir_base(T_β)), and then |π₁(V)| = 1.
Lemma 8.2 (fibered framing = Lagrangian framing) is taken as input.
