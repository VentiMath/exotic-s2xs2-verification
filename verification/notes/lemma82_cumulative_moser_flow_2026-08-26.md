# Lemma 8.2: constructive cumulative-coordinate Moser flow

The relative-Moser flow in Lemma 8.2 does not require a general local ODE
existence theorem. For

\[
 \Omega=f(\theta,t)\,dt\wedge d\theta,\qquad f>0,
\]

set

\[
 g(\theta,t)=\int_0^t(f(\theta,u)-1)\,du,
 \quad f_s=(1-s)+sf,
 \quad H_s(\theta,t)=t+s g(\theta,t).
\]

Then

\[
 \partial_tH_s=1+s(f-1)=f_s>0.
\]

For each `theta` and `s`, `H_s` is therefore strictly increasing in `t`.
On a sufficiently small common collar it has a unique inverse in the radial
variable. Define `T_s` by

\[
 H_s(\theta,T_s(\theta,t_0))=t_0.
\]

At `s=0`, `H_0=t`, so `T_0=t_0`. Differentiating at fixed `theta,t_0`
gives

\[
 0=g(\theta,T_s)+f_s(\theta,T_s)\partial_sT_s,
\]

hence

\[
 \partial_sT_s=-g(\theta,T_s)/f_s(\theta,T_s),
\]

exactly the vector field derived in Run 40. Also `H_s(theta,0)=0`, so strict
monotonicity gives `T_s(theta,0)=0`: the core is fixed pointwise.

At `s=1`, differentiating `H_1(theta,T_1)=t_0` with respect to `t_0`
gives

\[
 f(\theta,T_1)\partial_{t_0}T_1=1,
\]

which is precisely `phi_1^* Omega=Omega_0`.

The construction is uniform near the compact core. If `f_s>=m>0` on
`|t|<=rho` for all `theta,s`, monotonicity and integration give
`|H_s(theta,+/-rho)|>=m rho`. Thus every `|t_0|<m rho` has a unique inverse
`|T_s|<rho` for the whole interval `s in [0,1]`. Smooth dependence follows
directly because `partial_t H_s=f_s` never vanishes.

The coefficient identities and the uniform-collar inequality are checked
exactly by `luttinger/moser_cumulative_flow.py`. This replaces the
Picard--Lindelöf entry in the proof ledger with an explicit monotone inverse.
It still uses ordinary one-variable calculus, but no abstract flow-existence
theorem remains at this point.
