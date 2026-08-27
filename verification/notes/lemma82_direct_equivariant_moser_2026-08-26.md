# Lemma 8.2: direct equivariant Moser flow

The covering-space lifting theorem is unnecessary in this instance.  The
normalizing map can be constructed upstairs as a flow from the outset.

On the quotient collar write the relative-Moser vector field as

\[
 \bar X_s=a(\bar\theta,t,s)\,\partial_t,
 \qquad a=-\bar g/\bar f_s.
\]

In the paper's double-cover coordinates

\[
 q(\theta,t)=(2\theta,t),\qquad
 \tau(\theta,t)=(\theta+\pi,t),
\]

define on the original collar

\[
 X_s=a(2\theta,t,s)\,\partial_t.
\]

This is a global smooth field without making a lift choice.  Directly,
`dq(X_s)=bar X_s`.  Since the downstairs coefficient is `2pi`-periodic,

\[
 a(2(\theta+\pi),t,s)=a(2\theta+2\pi,t,s)
                       =a(2\theta,t,s),
\]

so `tau_* X_s=X_s`.  Moreover `bar g(bar theta,0)=0`, hence `X_s` vanishes
on the upstairs core.

Let `Phi_s` be its local time-dependent flow on the common collar supplied
by the relative-Moser ODE argument.  Both `Phi_s tau` and `tau Phi_s` solve
the same initial-value problem because `tau_*X_s=X_s`; uniqueness gives

\[
 \Phi_s\tau=\tau\Phi_s.
\]

Also `q Phi_s=bar Phi_s q`, by the same uniqueness argument after applying
`q`.  Thus `Phi_s` is exactly the equivariant normalization required in
Lemma 8.2.  No lifting criterion, path-lifting theorem, or uniqueness of
covering lifts is used.

Finally,

\[
 q^*(dt\wedge d\bar\theta)=2dt\wedge d\theta
                            =d(2t)\wedge d\theta,
\]

which is the paper's factor-two absorption.  The coordinate identities are
checked exactly by `luttinger/equivariant_moser_lift.py`; Run 42 separately
certifies that these coordinates describe the actual simplicial collar and
its free involution.

## Remaining analytic input

This argument deliberately does not claim to machine-prove general ODE
existence or uniqueness.  It shows that the same Picard--Lindelöf input
already used to construct the relative-Moser flow also proves equivariance.
Consequently connected-cover lifting is no longer an additional theorem in
the proof ledger.
