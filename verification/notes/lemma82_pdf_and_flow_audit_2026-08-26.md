# Lemma 8.2: typeset-PDF re-audit and explicit Moser flow (2026-08-26)

Two closures of residue in the framing lemma's verification, both run 40.

## 1. Typography re-audit against the actual PDF

Motivation: the one apparent error ever seen in Lemma 8.2 — the Moser sign
problem — was an artifact of plain-text extraction (subscripts scrambled).
Every audit until now worked from that extraction. This pass re-checked each
displayed formula of §8.7 against the typeset PDF taken from the author's
repository (`papers/exotic-s2xs2-and-cp2.pdf`, printed pages 20–23), read as
rendered pages.

All displays match the formulas as machine-checked:

* Weinstein chart data: coordinates `(Θ₁,Θ₂;P₁,P₂)`,
  `ω = dP₁∧dΘ₁ + dP₂∧dΘ₂`, `T = {P = 0}`.
* T_β chart: base annulus `(θ₂,u)`, Thurston form
  `ω = dt∧dθ₁ + K du∧dθ₂`, canonical for `(θ₁,θ₂; t, Ku)`,
  `T_β = {t = u = 0}`.
* T_α chart: quotient of `A_c×[0,2π]×(−1,1)` by
  `(θ₁,t,2π,u) ∼ (θ₁+π,t,0,u)`; coordinate change
  `Θ₁ = θ₁ − θ₂/2, Θ₂ = θ₂, P₁ = t, P₂ = t/2 + Ku`; deck identification
  `Θ₁ ↦ Θ₁ + 2π`; push-off momenta `(t₀, t₀/2)` and `(0, Ku₀)`.
* Moser data: `Ω = f dt∧dθ₁`, `Ω₀ = dt∧dθ₁`,
  `g(θ₁,t) = ∫₀ᵗ (f(θ₁,τ)−1) dτ`, `ζ = g dθ₁`, `dζ = Ω − Ω₀`, `ζ|_e = 0`,
  `ω_s = (1−s)Ω₀ + sΩ`, `ι_{X_s}ω_s = −ζ`,
  `d/ds φ_s*ω_s = φ_s*(d ι_{X_s}ω_s + dζ) = 0`.
* Equivariant Moser: quotient annulus, connected double cover, `Ω = π*Ω̄`,
  the lift criterion (identity on π₁), the deck-transformation argument, the
  pulled-back form `2 dt∧dθ₁` and the factor-2 absorption.
* Table 1 (printed page 23): F1 `M(Ax)^{ε_A} = 1` and
  F2 `N((r⁻¹M^{−ε}r)B)^{ε_B} = 1` match the certified direct filling words
  (with ε = −1 fixed by M3, F2's correction is `(r⁻¹Mr)B` as certified).

No discrepancy of any kind. The extraction-artifact channel is closed: the
audits' restored subscripts were all correct.

## 2. Explicit Moser flow (`moser_flow_check.py`)

The lemma's annulus normalization cited one soft analytic input: existence
of the Moser vector field's flow for s ∈ [0,1] near the compact core. For
this vector field the citation is now replaced by the flow itself. Since
`ι_X ω_s = −ζ` with `ω_s = f_s dt∧dθ₁` forces `X_s = −(g/f_s) ∂_t`, the
flow is a one-dimensional ODE in t with θ₁ a parameter. The script
verifies, all asserting:

* symbolically for a general positive `f(θ,t)`: the primitive identity, the
  core restriction, the contraction identity, vanishing of X on the core,
  and the Moser cancellation `∂_s ω_s + d ι_X ω_s = 0`;
* in closed form for every t-independent profile `f = F(θ) > 0`: the flow
  is exactly `T(s) = t₀/(1 + s(F−1))`, verified by substitution, with
  `φ₁*Ω = Ω₀` holding exactly (`F · ∂T/∂t₀ = 1`);
* numerically for a fully θ- and t-dependent profile: RK4 trajectories fix
  the core pointwise, satisfy the pullback identity
  `f(θ,T)·∂T/∂t₀ = 1` to residual 8.3e-11, and obey the explicit Grönwall
  trap `|T(s)| ≤ |t₀| e^{Cs}` with `C = max|f−1| / min(1, min f)` —
  giving the concrete invariant neighborhood `|t₀| < e^{−C}` (0.584 for
  the test profile). For general f, existence itself remains
  Picard–Lindelöf — applied to an explicit one-dimensional field with
  computed Lipschitz and trapping constants; the t-independent family is
  the fully constructive case.

## Remaining residue after run 40

Subsequent runs shrink this boundary further. Runs 43--44 discharge the
chart-independence statement by two routes. Run 46 constructs the Moser
field directly upstairs and proves its deck invariance, eliminating the
connected-cover lifting theorem. The remaining conventional input for this
normalization was Picard–Lindelöf existence and uniqueness for the explicit
one-dimensional field. Run 47 subsequently removes that citation too by
constructing the general flow as the unique inverse of the strictly
increasing cumulative coordinate `H_s=t+s integral_0^t(f-1)`.
