# Word provenance in the load-bearing chain (2026-09-03, issue #824)

Every word a certificate consumes, where it came from, and what certifies it.
Status vocabulary: **derived** (a script builds it from the complex; script
named), **certified** (a typed word shown to be an identity by reduction to
the empty word in a named halted system, or by coset enumeration), **typed**
(transcribed from notation or a paper table; nothing certifies it yet),
**shape typed / letters derived** (the form of a relator follows a convention,
the letters inside it are derived words).  No row is "to confirm" any more.

## sealed_transport/r_presentations.json

| word(s) | status | source / check |
|---|---|---|
| 78 relators of Q (3 generators) | derived | `X.presentation(u0a)` in r_run.py on the complement of the tori, then `fast_tietze.simplify`; `r_tietze_certificate.json.gz` replayed by `verify_certificate` with the input hash pinned. Raw presentation depends on PYTHONHASHSEED; the sealed chain is the one in `sealed_transport/`. |
| geom_x, geom_y, geom_r, geom_s | derived | `paper_bridge.build_paper_loops` rails with p-whiskers, `checked_word` in r_run.py; phi_0(x,y,r,s) = (r,s,x,y) certified vertexwise (`direct_z_variants/section_complex/phi0_fiber_seams.py`). |
| geom_A, geom_B | derived | `alpha_positive`, `beta_positive` edge paths in r_run.py (`geometric_paper_candidates`), inverted. |
| geom_M | derived | `explicitly_based_meridian` in r_run.py (`geometric_paper_candidates`). |
| geom_N, geom_N_source | derived | r_run.py ~626-632: `geom_N_source = alpha_s_grid_N` (the detour meridian at the source-side corner) and `geom_N = geom_A * alpha_s_grid_N^-1 * geom_A^-1`, its transport to the corner where Table 1 starts A s A^-1; the free-word identity `A^-1 geom_N A = N_grid^-1` in honest_filling.json is this definition. |
| geom_N_candidate_0..4 | derived comparison words | r_run.py candidate enumeration preceding the definition above; not consumed as relators. |
| mu_a, lf_a, lb_a1, lb_a2, mu_b, lf_b, lb_b, corr_b, beta_reference, lb_b_sweep, sweep_residual, longitude_residual, alpha_s_* | derived | meridian / longitude / sweep constructions in r_run.py (`beta_basing_sweep`, `alpha_s_transport_sweep`). |
| coord_* (sign-convention coordinates) | derived (sign enumeration) | r_run.py; one word per sign choice. |
| table_M1/M2/M3_sign+-1 | typed for comparison only | Wuebben Table 1 rows M1-M3 in both signs (r_run.py ~711-727), compared against the audit rows; grep confirms r_run.py is the only consumer and no certificate takes them as relators. |
| fillings (8 x 2 relators) | shape typed / letters derived | Luttinger filling meridian x longitude^(+-1) with the sign and drift enumerated; letters are the tracked words above. The sealed beta filling has the mixed-whisker defect of #816. |
| paper_fillings (8 x 2) | shape typed / letters derived | F1 = M (A x)^eA, F2 = N ((r^-1 M^-e r) B)^eB in the paper's convention; letters derived. |

## honest_filling/honest_filling.json

| word(s) | status | source / check |
|---|---|---|
| sheet rows AxA^-1=r, AyA^-1=s, ArA^-1=x, AsA^-1=Ny, ByB^-1=M^-1yx, BrB^-1=r, BsB^-1=r^-1M^-1rs, [x,y][r,s]=1 | certified | transcribed from the relation sheet, each reduced to the empty word in the complement system (`reduction_status_in_complement_system`, residual 0). |
| BxB^-1 = y^-1 (as printed) | typed, NOT certified | `x_transport_relation_uncertified`; the certified form is BxB^-1 = y^-1 M. Issue #818. |
| BxB^-1 = y^-1 M, B(s^-1 r^-1 y x)B^-1 = r^-1 s^-1 x M, [M, Ax] = 1, [A^-1 N A, r^-1 M r B] = 1 | certified | reduction in the complement system (`xMBy^-1x^-1sB^-1s^-1=1`, `lb_a_y1 = A x`, `lb_b_s2 = r^-1 M r B` all residual 0). |
| derived_01 .. derived_19 | derived, then certified | relators of the GAP presentation of Q on the eight sheet loops (`IsomorphismFpGroupByGenerators`, `sheet_presentation/mtc3.g`, log `mtc3.log`), each substituted into Q letters and reduced to the empty word in the complement system (`sheet_presentation/certify_P_relators.py` -> `certified_P_relators.json`), deduplicated against the sheet rows. |
| identities lb_a_y1 = A x, lb_b_s2 = r^-1 M r B, geom_M_y2 = y^-1 M y, lb_a_y2 = y^-1 A r^-1 y | certified | reduction in the complement system, residual 0. |
| case fillings alpha = M A x, beta = A^-1 N A r^-1 M r B (and the sign variants) | shape typed / letters certified | common-whisker filling of each torus: meridian times the certified longitude identity; four sign cases times two packages. |
| sheet_generator_words_in_Q | derived | the tracked geom words. |
| free-word identity A^-1 geom_N A = N_grid^-1 | certified (free group) | flag in the JSON. |

## Wuebben comparison (honest_filling/wuebben_dictionary/)

| word(s) | status | source / check |
|---|---|---|
| dictionary y -> M^-1 y, s -> r^-1 M^-1 r s, M -> B M B^-1, N -> M^-1 N M | typed hypothesis, then certified | all nine non-filling Wuebben rows reduce to 1 in Q_aud under it (stage scripts, logs). |
| Wuebben fillings F1_W, F2_W under the dictionary | typed; NOT in <<F_aud>> unless the honest group is trivial | residuals persist at 150k and 500k in the 30-relation system (`membership_sheet_words_500k.log`) and in the augmented 42-relation system halted at 500k, non-confluent (`membership_sheet_words_aug500k.log`, `kbmag/honest_y1_p1_p1_aug.rws.kbprog`). Settled by enumeration instead (`x_transport/his_fillings_enum.g`, `.log`): Q modulo his two fillings is trivial under either identification of his letters (geometric map or dictionary), while Q modulo the honest fillings overflows at 3,000,000 cosets. Under the geometric map his alpha filling is ours and his beta filling is ours times `[K^-1, N_dir]` (K = r^-1 M r), so his group is the honest group with one commutator set to 1 (`x_transport/README.md`, "Beta side"). Not a defect in our chain; the difference is a whisker choice on his beta torus. |
| Wuebben Table 1 rows, 4096 conventions | typed from arXiv:2608.17267 | reproduced trivial 32/32 (his group), not consumed by our certificates. |

## Direct double (direct_z, v2.5.0 RC, and direct_z_variants/)

| word(s) | status | source / check |
|---|---|---|
| 2 x (78 relators + 2 fillings) | derived / shape typed as above | `build_direct_z_q.py` from the sealed transport. |
| four fiber seams x_L = r_R, y_L = s_R, r_L = x_R, s_L = y_R | certified | literal based paths under phi_0 (`section_complex/phi0_fiber_seams.py`). |
| boundary word, v2.5.0: A^-1 B^-1 A B | typed; fails the seam gate | `seam_gate.py` G2 residuals on r, s; it is the A-conjugate of the boundary class. |
| boundary word, derived: A B^-1 A^-1 B | derived in the section of the real complex, twice | `section_complex/extract_section.py` + `section_boundary_word.g` (this tree) and the other agent's `direct_z/derive_boundary_inclusion.py` -> `boundary_inclusion.json` with a 140-step Tietze certificate (RC tree, 2026-09-03 08:55); the two based boundary inclusions agree letter for letter (#821). Agrees with the hand model and passes the seam gate. |
| relation form delta_L delta_R = 1 | derived from sigma_aud (section circle reversed) | Lemma sigma-aud(i), (iv); gate G3. |

## Actions

Typed and uncertified words that a certificate consumed: the printed
x-transport row (#818; the certified form is `B x B^-1 = y^-1 M`) and the
v2.5.0 boundary word (#820/#821; the derived word is `A B^-1 A^-1 B`).
Wuebben's fillings are not in <<F_aud>> unless the honest group is trivial;
his group is ours plus one commutator (`x_transport/`).  Everything else
consumed by a certificate is derived or certified, with the producing script
or the reducing system named.
