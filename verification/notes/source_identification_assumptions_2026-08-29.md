# Source Formalization D for the Wuebben comparison

The finite certificate theorem and the proof that the explicitly defined
audit manifold `V_aud` is simply connected do not depend on this document.
Source Formalization D enters only when `V_aud` is compared with the fixed
`(m,n)=(0,0)` member specified in Wuebben's pinned v1 text and figures. Its
clauses are comparison assertions, not machine certificates.

The main paper gives the normative table, exact citations, and proofs. This
file is the repository ledger version of the same boundary.

## Textual and diagrammatic fiber data

- **D1 — chain labels and order.** Convention 2.1(C8), Section 7.1, and
  Figure 1 are read as the ordered five-chain `(a,b,c,d,e)` used by the
  audit. Independent extraction and ribbon tests support the transcription.
- **D2 — involution and fixed disks.** Lemma 7.1 is read as the
  chain-reversing involution exchanging `a<->e`, `b<->d`, preserving `c`,
  with the two marked complementary disks containing `p,O`. Exhaustive
  rotation-system and periodic-disk checks support the comparison; the
  marked-disk identification remains diagrammatic.
- **D3 — hidden arcs.** Dashed, hidden, or paired portions of Figure 1 are
  continued as the displayed curves and do not introduce extra crossings.
  Vector-source and planar-incidence extraction plus added-crossing mutation
  controls support this ordinary drawing convention.

## Bundle and torus data

- **D4 — twist order and sign.** Convention 2.1(C2,C5) and Sections 3.1 and
  7.2 are read as `psi_0 = T_a o T_b`, with `T_b` applied first and the
  displayed right-twist normalization. Two subdivisions and reverse-order /
  reverse-sign controls test the realization.
- **D5 — cut-square holonomy.** Convention 2.1(C4) and Section 7.3 are read
  so that the alpha base loop has `phi_0` holonomy and the beta base loop has
  `psi_0` holonomy (equivalently, upward crossing of the alpha cut applies
  `psi_0` and rightward crossing of the beta cut applies `phi_0`). The graph
  clutching map and inverse check the seams.
- **D6 — the torus subbundles.** Sections 7.2--7.3 are read as selecting the
  `c`-over-alpha and product `e`-over-beta subbundles, relative to the full
  protected collars. Collar, disjointness, and local-flatness certificates
  support the comparison; identification with the target's displayed tori
  remains a source-to-audit assertion.

## Based peripheral and member data

- **D7 — path convention and base generators.** Convention 2.1(C1,C3,C6)
  is read literally: paths compose left to right,
  `A=[bar(alpha)]^-1`, `B=[bar(beta)]^-1`, and named peripheral pairs use
  common stated whiskers.
- **D8 — meridian basings.** Section 8.3 and Table 1 are read as the audit's
  oriented `M,N`, based along `y_1,s_2` with the named correction paths.
  Two peripheral extractors and the explicit normal fibers support this.
- **D9 — alpha reference half-drift.** Section 8.4 explicitly selects the
  `y_1`-based reference word `Ax`; the complement-only 72-letter identity
  certificate and side mutations test the audit realization.
- **D10 — fixed family member and slopes.** Section 9.1 and Table 1 select
  `(m,n)=(0,0)` and the displayed F1/F2 slopes. The independent relation-
  sheet extractor agrees exactly. Settled at the level of strings (Runs 71
  and 78, `luttinger/wuebben_dictionary/`): the displayed sheet, for each of
  the four sign sheets, is literally the `(m,n)=(0,0)` system of his
  ancillary `decide2.g` at `e3=+1, e4=-1, e5=-1` and the `y1/Ax` point of
  his `fixed_v_certify.g` family, uniquely among 8,480 systems, under the
  identity map on `x,y,r,s,A,B,M,N`; the relator-by-relator diff is empty.
  What remains of D10 is not textual: whether his slopes are ours as curves
  on the tori is D12--D13.
- **D11 — convention exponents.** Convention 2.1(C7) and Remark 11.1 are
  read as making `epsilon_A,epsilon_B` relation-sheet orientation exponents,
  not four different geometric surgeries. All four sheets certify the same
  audit object under this convention identification.

## Smooth surgery data

- **D12 — smooth tori.** Section 8.7 and Lemma 8.2 are read as using the
  smooth Lagrangian tori represented by the marked curve subbundles. The
  audit supplies local-flatness, normal-frontier, and topological-to-smooth
  transport certificates; equality with the source tori remains smooth
  comparison content.
- **D13 — coefficients and framings.** Sections 2.1, 8.7, and 9 are read as
  using the Lagrangian-framing classes and coefficient/orientation
  conventions encoded by F1/F2. The Moser and Weinstein-chart calculations
  prove the corresponding statement in `V_aud`.
- **D14 — relative smooth bundle equivalence.** The comparison throughout
  Sections 7.1--8.7 is required to be represented by an orientation-
  preserving diffeomorphism relative to the two torus collars and the
  boundary marking. Explicit PL maps and collar data support this; standard
  surface smoothing and relative isotopy supply the stated upgrade once the
  source comparison is granted.

## Logical consequence and the contrary report

Under D1--D14, the relative smooth comparison carries meridians, longitude
classes, and surgery slopes, so it extends over both fillings and identifies
`V_aud` with the fixed target member. Without D1--D14 the project still
proves `pi_1(V_aud)=1`.

The contrary computation attributed to Lidman and Piccirillo is not assigned
solely to this source boundary. If it concerns the same fixed member, live
possibilities include failure of a D-clause, a defect in a displayed
geometric identification or checker, a defect in that contrary computation,
or a mismatch of members or conventions. Reconciliation requires its
presentation and dictionary.
