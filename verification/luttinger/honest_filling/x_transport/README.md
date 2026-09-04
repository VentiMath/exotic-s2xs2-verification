# The x-transport row: Wuebben's whisker traced in the audit complex

Working directory (2026-09-03, issue #818; pointer on #794).

## The question, in five lines

1. Certified for the audit loops (reduction to the empty word in the sealed complement system): `B x B^-1 = y^-1 M`.
2. Printed in Wuebben's Table 1 (arXiv:2608.17267v1, row B1): `B x B^-1 = y^-1`.
3. Under the re-basing dictionary `y -> M^-1 y` (with `s -> r^-1 M^-1 r s`, `M -> B M B^-1`, `N -> M^-1 N M`) the two rows coincide, and his nine non-filling rows are identities of `Q` (`../wuebben_dictionary/`).
4. Consequence: his alpha filling `M_W (A x)` with `M_W = B M B^-1` differs from the derived `M (A x)` by exactly `[B, M]` modulo the derived relator (`../WHAT_STANDS.md` §3); `[B, M]` is undecided in the honest group.
5. To settle: is his row a true identity of `pi_1(C_aud)` for the loop he describes (change of generators), or false for every based loop realising his description (his sheet is not `pi_1` of his manifold)?

Sections below are appended as each computation finishes; every number cites a log in this directory.

## Part A: the two rows and their quotient in the sealed complement system (`residuals.py`, `residuals.log`, `residuals.json`)

System: `alpha_residual/complement_input.rws.kbprog` (49,990 rules, halted, not confluent).  A reduction to the
empty word is a proof in `Q = pi_1(C_aud)`; a nonzero residual is only a normal form.

| word (sheet letters; `sheet_generator_words_in_Q` from `honest_filling.json`) | residual |
|---|---|
| ours `B x B^-1 (y^-1 M)^-1` | **0, identity in Q** |
| his `B x B^-1 (y^-1)^-1` (printed row B1) | 27 letters |
| quotient of the two, `(B x B^-1 y)(B x B^-1 M^-1 y)^-1 = B x B^-1 M B x^-1 B^-1` | 35 letters, same normal form as `y^-1 M y` |
| `M` | 30 letters |
| his row under the dictionary `y -> M^-1 y`: `B x B^-1 (M^-1 y)` | **0** |
| `[B, M]` | 45 letters; same normal form as `F1_W F1^-1 = (B M B^-1 A x)(M A x)^-1` |
| inverse transport `B^-1 x B (x y)^-1` | **0**: `B^-1 x B = x y`, no meridian |
| inverse transport `B^-1 r B r^-1` | **0** |
| inverse transport `B^-1 y B x` | 26 letters (needs a meridian) |
| inverse transport `B^-1 s B s^-1` | 17 letters (needs a meridian) |

So the residual between the printed row and the certified row is exactly the conjugate `y^-1 M y` of the alpha
meridian (certified by common normal form), and Wuebben's alpha filling differs from the derived one by `[B, M]`
(certified by common normal form).  New here: along the *inverse* base loop the x transport is clean in our
complex (`B^-1 x B = x y`), while `y` and `s` are the ones that pick up a meridian.

## Part D: is M nontrivial in Q? (`m_in_Q.g`, `m_in_Q.log`, `m_in_Q_2.g`, `m_in_Q_2.log`)

- `AbelianInvariants(Q) = [0, 0]` (H_1 = Z^2); the exponent vectors of the 78 relators span rank 1 and kill
  the `g3` direction, so `M` (exponent vector (0,0,1)), `N` and `[B, M]` all die in `Q^ab`.
- `LowIndexSubgroupsFpGroup(Q, 5)`: 135 subgroups; `M` and `[B, M]` lie in every one of them.
- Coset enumeration of `Q` over `<M>` at 2,000,000 cosets: overflow.
- `M`, `[B, M]`, `N` are trivial in `U/[U,U]` for every subgroup `U` of index 2..5 (all `H_1(U)` free of
  rank index+1, as for a surface-like group).
- **Not decided.**  Nothing here refutes `M = 1` in `Q`; nothing proves it.  (If `M = 1` in `Q` the printed
  row holds and every honest case collapses; see the README of `honest_filling/`.)

## Part B: the literal membranes in the audit complex (`trace_x_transport.py`, `.log`, `.json`; `certify_pieces.py`, `.json`)

Geometry of the audit base (bundle.py): annulus with radii `J0 < J1 < J2`, angular copies `A0, A1, A2`
(the `phi_0` seam is `A2 -> A0`); the beta band is the twist stack (levels `0..m`) times the thickness
`t0,t1,t2`, glued with level `0` at `J2` and level `m` at `J0`, thickness `t_k` to angular copy `A_k`.
`T_alpha = c x {J1}`; `T_beta = e x (band core at t1, radial return at A1)`; base point `q = (A0, p, J2)`.
The displayed positive beta loop is `q -> (A1,J2) -> band up -> (A1,J0) -> (A1,J1) -> (A1,J2) -> q` and
`B` is its inverse.  So along the sweep that realises `B g B^-1 = psi(g)` (the positive loop, band first)
`T_alpha` is met *after* the band; along the inverse sweep (`B^-1 g B = psi^-1(g)`, radial first) it is met
*before* the band.

Pieces, each a literal object of the complex, every word transported through the sealed 99,860-step Tietze
certificate (which reproduces `Q` and all 89 sealed words) and reduced in the sealed complement system:

* `R1[x]`: the radial grid `x x {J2, J1, J0}` at `A1` is simplicial and meets neither torus.
* `R1[y]`: the radial grid `y x {J2, J1, J0}` at `A1` meets `T_alpha` in exactly one vertex,
  `(A1, c_y, J1)` with `c_y = ('b',-1,4)`, transversally with oriented sign `-1`, and misses `T_beta`.
  The meridian `ring` is the link 8-cycle of that vertex in the grid, whiskered by `y_1` at `A1`
  (the direct whisker: no band).
* `S1`: in the open twist stack with the `e`-vertices deleted (a full subcomplex of `C`), the based loops
  satisfy `x_bottom = (y^-1)_top`, `x_top = (x y)_bottom`, `y_bottom = (y x)_top` through the `p`-track,
  each certified by Tietze reduction to the empty word (so the band part of every membrane misses both tori).
* `A1`: the angular squares at `J2` between `A0` and `A1` (product cylinders) carry `x`, `y` unchanged.

Results (`certify_pieces.json`; 0 = identity in `Q`): see the table appended below once the run finishes.

### Part B results (`certify_pieces.log`; 0 = identity in Q)

| piece | result |
|---|---|
| `A1`: `x`, `y` at `(A1,J2)` equal `geom_x`, `geom_y` | 0, 0 |
| `R1[x]`: `x` at `(A1,J0)` through the radial p-track = `x` at `(A1,J2)` (no puncture) | 0 |
| `R1[y]`: `y` at `(A1,J0)` through the radial p-track = `ring . y` at `(A1,J2)` | 0 |
| `ring = geom_M^-1` (the link 8-cycle, whisker `y_1` at `A1`, is the sealed `M` inverted) | 0 |
| band, read in Q: `g` via the band = `B^-1 (g` via the radial track`) B`, `g = x, y` | 0, 0 |
| `S1` read in Q: `x` at `(A1,J2)` = (`y` via band)`^-1`; `x` via band = `geom_x geom_y` | 0, 0 |
| **assembled, our loop**: `B x B^-1 = y^-1 ring^-1 = y^-1 M` | 0 (and 44 for `y^-1 ring`) |
| **assembled, inverse loop**: `B^-1 x B = x y` | 0 |
| **inverse loop, y**: `B^-1 y B = (B^-1 M B) x^-1` | 0 |
| inverse loop, y, unconjugated: `M x^-1`, `M^-1 x^-1`, `(B^-1 M^-1 B) x^-1` | 39, 28, 42 |

So, literally in the complex: along the positive loop (band first) the `x` membrane is punctured once, at
`(A1, c_y, J1)` on the radial crossing *after* the band, where the transported loop is already `y^-1`; the
puncture meridian with its direct whisker is `M^-1` (`ring`), and the row is `B x B^-1 = y^-1 M`.  Along the
inverse loop (radial first, torus *before* the band) the `x` membrane misses `T_alpha` and the row is clean,
`B^-1 x B = x y`; there it is `y` that is punctured, before the band, and its correction is the meridian
*conjugated by the base letter*, `B^-1 M B`, not `M`.

## Part C: what Wuebben's row is, and what his sheet is (`wuebben_rows_two_maps.py`, `.log`, `.json`)

**The mechanism (checkable by hand).**  For a fiber loop `g` swept along a base loop `L` (holonomy `psi`),
the transport annulus gives `g . L . psi(g)^-1 . L^-1 = w mu^{+-1} w^-1`, where `w` runs inside the annulus
from its base corner to the puncture.  If the puncture lies *before* the wrap along `L`, `w` is the direct
whisker (fiber arc, then the short base arc); rewriting as `B g B^-1 = [corr] psi(g)` with `B = L^-1`
conjugates the correction: `corr = B (w mu w^-1)^{+-1} B^-1`.  If the puncture lies *after* the wrap,
`w = B^-1 . w_direct` and the conjugation cancels: `corr = (w_direct mu w_direct^-1)^{+-1}`.  Both cases are
certified above in our complex (the after case on the positive loop, the before case on the inverse loop).

**His configuration.**  Wuebben's `T_alpha = c x {alpha-cut}` with the sweep meeting it before the wrap
(Remark 6.3, Fig. 2: puncture `z_0 = (g cap c, wrap)` with `g` untwisted).  Ours meets it after the band.
The two are the same torus up to an isotopy that slides it forward along the beta loop through the fiber
over `q`; that isotopy fixes `x, r, A, B` (they miss `c`), inserts a meridian into `y` and `s` (which cross
`c`), and carries the direct-whisker meridian to the direct-whisker meridian.  Hence the geometric map from
his letters to ours is `y -> M^-1 y`, `s -> r^-1 M^-1 r s` (the dictionary rows) and **`M -> M`** (not
`B M B^-1`).

**Answer.**  Wuebben's printed row `B x B^-1 = y^-1` is a *true* identity of `pi_1(C)` for the loop he
describes: under the geometric map it is `B x B^-1 = (M^-1 y)^-1`, our certified row (`B1` reduces to 0
under both maps).  The discrepancy is not in the `x` row.  It is in the corrected rows: for a puncture before
the wrap the correction is `B M B^-1`, and his sheet prints `M`.  Certified:

| his row, under the geometric map (`M_W = M`) | equals in Q |
|---|---|
| `M2 (e4=-1)`: `B y_W B^-1 = M^-1 y_W x` | `[B, M^-1]` (quotient reduces to 0) |
| `M3 (e=-1)`: `B s_W B^-1 = r^-1 M^-1 r s_W` | `r^-1 [B, M^-1] r` (quotient reduces to 0) |
| the other signs | `B M^-1 B^-1 M^-1`, `r^-1 B M^-1 B^-1 M^-1 r` |
| `F1_W = M_W A x` | `M A x`, the derived honest alpha filling (quotient reduces to 0) |

and under the algebraic dictionary (`M_W = B M B^-1`): `B1`, `M2 (e4=-1)`, `M3 (e=-1)` are identities of `Q`,
while `F1_W . (M A x)^-1` has the normal form of `[B, M]`.

So there are two readings of his sheet, and both give the same group.  Read with `M` = his direct-whisker
meridian (the one his fillings intend), rows `M2`, `M3` are false in `pi_1(C)` unless `[B, M] = 1`, and his
`F1` is exactly our honest alpha filling.  Read with `M` = `B M_direct B^-1` (the only assignment that makes
his rows identities), his rows are a re-presentation of `Q`, but his `F1 = M (A x)` pairs the `B`-conjugated
meridian with the direct-whisker longitude `A x`: the mixed-whisker relator of #816 on the alpha side,
differing from the Dehn filling relator by `[B, M]`.  Either way his 11-relator group is the honest group
with `[B, M] = 1` adjoined, which is what WHAT_STANDS.md section 3 found algebraically; the geometric step
is: the correction from a puncture that lies before the wrap was written without the conjugation by `B`
that the transport annulus imposes.  (The same step on the beta side is why the audit defined
`geom_N = A N_grid^-1 A^-1`, and why the sealed beta filling had mixed whiskers, #816.)

## Beta side under the geometric map (`beta_side.py`, `.log`, `.json`)

Our alpha sweep (`A0 -> A1 -> A2 -> phi_0 -> A0`) meets `T_beta` at `A1`, *before* the `phi_0` wrap, so the
correction in `A s A^-1 = [corr] y` is the direct meridian conjugated by `A`.  r_run.py indeed sets
`N := geom_N = A . N_grid^-1 . A^-1` (`N_grid = alpha_s_grid_N`, whisker `s_2` plus the local detour); the
certified row `A s A^-1 = N y` carries the conjugation inside the letter, and the direct meridian is
`N_dir := A^-1 N A` (the honest beta filling uses it).  Wuebben's `T_beta` is also met before the `phi_0` wrap
and his `N` is the direct `s_2`-whiskered meridian; the alpha-torus isotopy of Part C inserts the `c_s`
meridian `K = r^-1 M r` into every path through `c_s`, and `s_2` passes `c_s`, so the geometric image of his
`N` is `N_W = K^-1 N_dir K`.  Certified (0 = identity in `Q`):

| statement | result |
|---|---|
| `A M A^-1 = K = r^-1 M r` (the `c_y` meridian transported around alpha is the `c_s` meridian) | 0 |
| mechanism row `A s_W A^-1 = (A N_W A^-1) y_W` with `N_W = K^-1 N_dir K`, `s_W = K^-1 s`, `y_W = M^-1 y` | **0** |
| his printed `M1`: `A s_W A^-1 = N_W y_W`, same `N_W` | 54; `M1 . [A, N_W]^-1` = **0**, so `M1 = [A, N_W]` |
| his printed `M1` with `N_W = A^-1 N A`, `N`, `K N_dir K^-1`, either sign | 41..85, no named match |
| his printed `M1` under the algebraic dictionary `N_W = M^-1 N M`, `e3 = +1` | 0 (as before) |
| `F1_W(geo) = M A x` | 0 (Part C) |
| `F2_W(geo) = N_W (r^-1 M r B)^eB` vs honest `A^-1 N A (r^-1 M r B)^eB`, `N_W = K^-1 N_dir K` | 42 = the free word `[K^-1, N_dir]` |
| `[K^-1, N_dir]`, `[B, K]`, `[A, K]`, `[K, r^-1 M r B]`, `[B, M]` in `Q` | 42, 32, 30, 40, 45 (none certified trivial) |
| `F2_W(dict)` vs honest / vs sealed `N (r^-1 M r B)^eB` | 61, 58 / 88, 82 (no named match) |

Reading.  On the beta side the same mechanism holds: his printed `M1` is, on our loops, the commutator
`[A, N_W]` of the base letter with his meridian (a puncture before the wrap, correction written without the
`A`-conjugation).  His `F1` pulls back to the honest alpha filling exactly.  His `F2` pulls back to the honest
beta filling times `[K^-1, N_dir]`; equivalently, his printed push-off word `(r^-1 M r) B` is the isotopy image
`K^-1 (r^-1 M r B) K` of the `s_2`-whiskered push-off only if `[B, K] = 1` (free-word identity in the log), so on
the beta side his meridian and his longitude no longer share a whisker on our loops.  Which conjugate of the
direct meridian is his `N` was fixed by the mechanism row reducing to 0 (only `K^-1 N_dir^{+-1} K` does).

## His sheet modulo his fillings (`his_fillings_enum.g`, `.log`)

Native GAP coset enumeration on the 30 certified sheet relations (`collapse_full.g`), 3,000,000 cosets, all four
sign pairs `(eA, eB)`; every row below is identical for the four sign pairs:

| fillings added to the 30 relations | result |
|---|---|
| honest `M (A x)^eA`, `A^-1 N A (r^-1 M r B)^eB` | overflow |
| honest + `[B, M]` | index 1 |
| his, geometric map, `N_W = A^-1 N A` (literally the honest pair) | overflow |
| his, geometric map, `N_W = K^-1 A^-1 N A K` (the certified image of his `N`) | **index 1** |
| his, geometric map, `N_W = K A^-1 N A K^-1` | index 1 |
| his, algebraic dictionary (`B M B^-1 (A x)^eA`, `M^-1 N M (r^-1 B M B^-1 r B)^eB`) | index 1 |
| dictionary `F1` + honest `F2`; honest `F1` + dictionary `F2` | index 1; index 1 |

So `Q` modulo Wuebben's two fillings is trivial under either identification of his letters, while `Q` modulo the
honest fillings overflows; each of his fillings on its own, with the other one honest, already collapses.
Under the geometric map the collapse comes entirely from the beta filling: his alpha filling is ours, and his beta
filling is ours times `[K^-1, N_dir]`, so the honest group is also the normal closure of `[K^-1, N_dir]`
(alongside `[B, M]` and `[A, N_grid]`).

## Not decided / not done

- `M = 1`, `[B, M] = 1`, `[B, K] = 1`, `[K^-1, N_dir] = 1` in `Q` are undecided (Part D and the residuals above).
  If `M = 1` in `Q` all of the above is vacuous and every honest case collapses.
- His torus position is not a subcomplex of our complex (`c` is not an edge cycle at the intermediate band
  levels), so his configuration was realised through the inverse loop and the isotopy argument, not as a
  second torus in the same complex.  The isotopy statement (Lagrangian throughout; fixes `x, r, A, B`; inserts
  `M^-1` into `y` and `K^-1` into `s` and `s_2`) is argued and consistent with every reduction above, not
  machine-checked as an isotopy.
- The reductions certify equalities in `Q`; nonzero residuals are normal forms in a halted system, not disproofs.

## Files

`residuals.py/.log/.json` (A), `q_input.g`, `m_in_Q.g/.log`, `m_in_Q_2.g/.log`, `m_in_Q_3.g/.log` (D),
`trace_x_transport.py/.log/.json`, `certify_pieces.py/.log/.json` (B), `wuebben_rows_two_maps.py/.log/.json` (C),
`beta_side.py/.log/.json` (beta side), `his_fillings_enum.g/.log` (enumerations).
Systems: `alpha_residual/complement_input.rws.kbprog` (Q), `sealed_transport/` (Tietze transport).
