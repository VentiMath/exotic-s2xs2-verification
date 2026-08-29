# Current state (2026-08-28)

Model provenance is tracked in PROVENANCE.md; its log table is the authority
on which model produced which commits (the original "everything after 6587b7e
is Opus 5" rule is superseded there).

The original machine derivation was built in one session with Fable 5, starting from
`luttinger.tar.gz` (the inherited engine + calibrations) and DESIGN.md §4 (the
not-yet-built case: Wuebben's non-product bundle R). This file is the honest
snapshot: what is machine-certified, what is not, and where the remaining
trust boundary sits.

An auxiliary framing-discrepancy scan is complete (`runs/45`, driver
`luttinger/j_robustness.py`, verdicts `luttinger/j_robustness_results.jsonl`).
It does not alter the certified `j=0` fillings or prove Lemma 8.2; it maps
what a hypothetical framing error would do.  Run 45 originally froze 82
certified-trivial and 18 inconclusive cases.  Run 59 retries those 18 before
GAP simplification: the redundant raw relations make 13 additional cases
complete confluently, including both cases studied in Runs 39 and 41.  Their
15,973-record derivation DAGs pass both independent verifiers, giving a 95/5
tally after Run 59.  Run 60 raises the equation ceiling and certifies
`n1_y2_ap1_bm1_jap1_jbm1` with a separately double-verified 2,417-record
derivation DAG.  Run 61 independently certifies the two raised-limit `n0_y1`
completions with 2,716- and 1,636-record DAGs.  Run 62 then certifies
`n1_y2_ap1_bp1_jap1_jbp1` at `maxeqns=300000`, `tidyint=500`, with a
double-verified 1,863-record DAG.  Run 63 resolves the last case,
`n0_y1_ap1_bp1_jap1_jbp1`, by isolating the 96 relators it shares with that
`n1_y2` presentation.  The common core completes to an infinite-cyclic group:
`g1`, `g3`, and `g4` vanish, while both differing filling relators reduce to
`g2^-1`.  The `n0_y1` filling relator therefore kills the last generator.
The resulting 4,040-record ancestry certificate passes independent Python and
Ruby replay, including the exact 96/97 source comparison.  The current
repository tally is therefore **100 reported trivial (22 certificate-backed, 78 retained GAP-session verdicts), 0 inconclusive, and 0
nontrivial**.  These are auxiliary counterfactual framing shifts; the result
strengthens robustness but was never needed for the paper's `j=0` proof.

After commit `4bd40fa`, OpenAI Codex added a combinatorial basing-sweep
diagnostic (`sweep.py`, `beta_basing_sweep` in `r_run.py`).  It constructs the
§8.5 square as a 7x35 simplicial grid, checks every grid edge, and finds exactly
one interior incidence with `T_alpha`; all incidences with `T_beta` lie on the
terminal boundary.  It also propagates orientations through `K` and the tori,
computes the local intersection sign, and emits the resulting explicitly based
meridian conjugate.  Deleting the target-torus vertex stars leaves three
oriented boundary cycles of lengths 6, 34, and 34.  The terminal cycle, based
at the same local point as `lb_b`, agrees *exactly after the recorded elementary
Tietze substitutions* with the independently computed direct longitude.  This
shows that `lb_b` already contains the geometric basing effect and must not be
multiplied by an extra meridian.

## What the machine does now

Pipeline, all from the triangulation alone:

    fiber.py      genus-2 fiber L = regular nbhd of the five-chain a-b-c-d-e
                  (five plumbed 3-row annular bands) + 2 cone discs at p, O.
                  f-vector [86, 264, 176].
    layers.py     simplicial mapping cylinders, flip layers, realize_twist
                  (k monotone one-band shear rounds), build_stack.
    bundle.py     assembles K = R: alpha-annulus (Y x J) glued to the beta band
                  (flip stack St x tau).  f-vector [9156, 116714, 356728,
                  403152, 153984].  T_alpha = c x alpha, T_beta = e x beta.
    complement.py TorusComplement: C, Ndot, meridians, product-framing pushoffs.
    fast_tietze.py  occurrence-indexed, proof-producing Tietze + replay verifier.
    sweep.py      validates rectangular simplicial sweeps and torus incidences.
    r_run.py      the whole run, including the beta basing sweep -> r_cert.g -> GAP.
    group_attack.py  bounded GAP/KBMAG/ACE/quotient attacks on stable exports.
    presentation_search.py  replayable Nielsen/relator local search.

The direct section certificate in `pl_self_intersection.py` additionally
extracts the 102-vertex `p`-section and its actual 24-cycle normal link,
verifies the normal actions `I` and `-I`, and doubles it to a 138-vertex
genus-2 section. For every constant simplicial boundary rotation it builds a
disjoint normal push-off and an exact radial 3-chain. The signed intersection
list is empty, so `Gamma_hat^2=0`; see `runs/28` and
`notes/pl_self_intersection_certificate_2026-08-24.md`.

Run cost on this machine: bundle 13s, complement 14s, pi1(C) 3s
(99,863 generators / 321,702 relators), certified Tietze reduction plus full
replay to **3 gens / 78 relators** in 49s.

## Certified PASS

* **Calibration 1** (`t4_run.py`): pi1(C) = Z^2 x F_2, /<<mu>> = Z^4, surgery
  reproduces the textbook T^4 Luttinger answer. Fingerprints exact.
* **Calibration 2** (`bk_t4_test.py`): opposite signs -> tr A = 1 fingerprint,
  equal signs -> tr A = 3. Never -1/-3.
* **Fiber (= the paper's (a)-check)**: chi = -2, closed orientable, links
  circles, phi0 an involution with Fix = {p, O}, curves chordless, the
  five-chain intersection pattern, transversality, complement = 2 discs
  separating p and O. All as executable assertions in `check_fiber`.
* **Explicit based fiber generators:** `paper_bridge.py` replaces implicit
  spanning-tree basing by literal rail loops with one-edge whiskers from `p`.
  It proves `phi0(x,y)=(r,s)` as equality of vertex paths, certifies
  `[x,y][r,s]`, and proves `x,y,r` freely generate the drilled-e fiber group.
  Transporting the complete whiskered paths through the open beta stack gives
  `x->y^-1`, `y->yx`, `r->r`, `s->s`; 17,839 elementary Tietze steps replay
  successfully and the remaining surface words Dehn-reduce to the identity.
  This directly tests, and does not reproduce, the reported unbased-vs-based
  monodromy objection for the current model.  The Table 1 puncture lassos are
  still separate work.
* **First exact Table 1 comparisons:** with `M` based along the explicit
  `y_1` path, KBMAG rewrites the M2 and M3 residuals to the identity with the
  triangulation's `M^-1` convention:
  `ByB^-1=M^-1(yx)` and `BsB^-1=(r^-1M^-1r)s`.  A reduction to identity is a
  valid certificate although the full rewriting system is nonconfluent.
  The opposite signs remain inconclusive.
* **M1 membrane geometry:** an explicit 11x4 alpha-transport grid for `s`
  has no `T_alpha` hit, one `T_beta` hit of oriented sign -1, and punctured
  boundary lengths 8 and 12.  The untouched component is exactly `y^-1`.
  The 12-edge component's short detour is now proved to be the positively
  oriented, `s_2`-based dual meridian `N`: the complement of the crossing's
  closed star has f-vector `[24,90,108,42]`, reduces to the free rank-one
  meridian group, and the detour agrees with all four reachable oriented dual
  representatives; comparison with their inverses is `g^+-2`.  Every local
  Tietze step replays.  The boundary connector is the positive alpha loop
  `A^-1`; rotating to the Table 1 base corner changes the source-side meridian
  to `N=A*N_grid^-1*A^-1`.  With that word the assembled residual
  `AsA^-1*(Ny)^-1` is empty after the proof-producing full Tietze replay.
  Thus M1, M2 and M3 now form one coherent certified correction package.  See
  `runs/12`, `runs/13`, and `runs/14`.
* **The `T_alpha` filling direction:** the Section 8.4 comparison now uses the
  actual `c_y` starting corner, the literal initial segment `y_1` from `p`, a
  checked two-edge normal jog to the boundary, and the lift of `A` (the inverse
  of the displayed positive alpha loop).  Of the two half-arcs of `c`, the
  paper's `y_1` side gives `dir_base(T_alpha)=A*x` with an empty residual after
  the proof-producing Tietze pass and independent replay.  This identifies the
  paper's `n=0` section directly; see `runs/15`.
* **The `T_beta` filling direction:** starting at the actual `s_e` crossing,
  using the literal `s_2` whisker and the lift of `B`, the direct boundary
  word is positively certified as `(r^-1 M r)B`.  This is exactly the sign
  predicted from the independently certified M3 convention
  `BsB^-1=(r^-1 M^-1 r)s`; all nearby sign/order/orientation variants were
  retained as diagnostics.
* **The perfect-group blocker is resolved for all eight direct fillings.**
  Adding `M(Ax)^eA` and `N((r^-1 M r)B)^eB` directly to the
  triangulation-derived complement presentation gives, for all four sign
  pairs, complete confluent systems which rewrite every generator to the
  identity.  More strongly, exporting the literal coherent pairs
  `(M_y1,lambda_y1)`, `(M_y2,lambda_y2)`, and `(N,lambda_beta)` and filling
  without substituting coordinate formulas gives eight complete triviality
  certificates. Seven complete in one ordering and the eighth in an equivalent
  base-first order. This is not a fingerprint or coset heuristic; see
  `runs/16`--`runs/20`.
  A filling-first control on the older eight arbitrary-corner/tree-based word
  presentations remains nonconfluent in every case; this isolates their
  simultaneous peripheral conjugacies as bookkeeping rather than supplying a
  competing nontriviality result.  Reducing every coherent paper relator pair
  inside those eight nonconfluent quotients also remained inconclusive. Run 19
  now supplies the missing torus-slope permutation, and boundary-whisker
  conjugacy identifies them with the direct trivial fillings; see `runs/20`.
* **The all-eight rewriting certificates are now durable and replayable.**
  `group_attack.py direct-paper-export` saves, for every sign and half-drift
  case, the simplified presentation, KBMAG result record, and completed
  rewriting system in `luttinger/direct_rws/`. Its manifest binds the source
  presentation, generated GAP program, and all 24 case artifacts by SHA-256.
  `direct-paper-replay` verifies those digests, reloads each saved system,
  rebuilds its reducer from the stored equations, and again obtains identity
  normal forms for every generator. All eight replays pass; see `runs/21`.
* **The triangulated model is now matched globally to the paper's marked
  bundle.** `model_correspondence.py` combines the filling-five-chain test,
  literal based actions of both monodromies, the free half-rotation on `c`,
  the pointwise product restriction on `e`, a global codimension-one manifold
  check, and the two induced surgery tori. Since the punctured-torus base
  has two generator handles, Run 52 now constructs the bundle map directly
  on their mapping cylinders and checks both seam equations and inverses.
  This replaces the earlier fingerprint-only comparison without invoking
  surface-bundle classification or Dehn--Nielsen--Baer. `framing_check.py` now
  verifies the relative-Moser coefficient calculus, double-cover
  normalization, Weinstein coordinates, seam, half-drift, and
  constant-momentum assertions in Lemma 8.2; no framing discrepancy was
  found. Runs 43--44 directly discharge the needed chart-independence
  consequence by the fiber-dilation germ isotopy and an independent
  Liouville-coordinate route; ADK03 germ uniqueness is corroborating rather
  than necessary. Runs 46--47 likewise replace lifting and local-flow
  inputs. See `runs/22`, `runs/35`, `runs/43`--`44`, and
  `notes/framing_lemma_referee_packet_2026-08-25.md`.
* **The peripheral bridge is now a single conventional lemma.**  The marked
  bundle equivalence is chosen relative to `c,e`; the derived-neighborhood
  dual loops are matched to the paper's `y_1`- and `s_2`-based meridians; the
  literal push-offs use those same whiskers; and Lemma 8.2 removes any hidden
  meridian component in passing from the fibered to the Lagrangian framing.
  Therefore the direct pairs `(geom_M,lb_a_y1)` and
  `(geom_N,lb_b_s2)` impose exactly the paper's `n=0` surgery normal closure,
  independently of the unused historical coordinates and the inconclusive
  alternate `y_2` beta formula. See `runs/27` and
  `notes/peripheral_identification_lemma_2026-08-24.md`.
* **The drilled-fiber relation R3 is now certified geometrically.** A
  deterministic 31-edge loop avoids `c` vertex by vertex, represents
  `s^-1 r^-1 y x`, and together with `x,r` freely generates
  `pi1(F-nu(c))`. Transporting that literal loop through the open beta stack
  gives `r^-1 s^-1 x` after a replayed 17,839-step Tietze certificate and
  final surface Dehn reduction. Thus every additional relation imposed in
  the paper's epimorphism `G -> pi1(V)` now has an independent path-level
  geometric certificate. See `runs/23`.
* **The deductions from simple connectivity to Theorems A, B, C are a
  proof-grade dependency chain.**  `downstream_chain.py` records every
  implication from the certified `pi_1(V) = 1` to the three theorems as an
  explicit item: 25 external theorems stated with hypotheses and sources
  (Klug's Theorem 2, Hambleton's Theorem 5.1, Ho--Li's Theorem 1.1 and
  Lidman--Piccirillo's Lemmas 9 and 10 quoted verbatim), 3 hash-bound
  certificates of this repository, 15 computed facts, and 16 deduction
  steps ending in `S7_theorem_A`, `S12_theorem_B`, `S16_theorem_C`.
  `verify_downstream_chain.rb`, written independently, re-derives every
  computed fact from scratch, checks acyclicity and that each theorem
  depends on `K_pi1_V_trivial`, and verifies every evidence digest.  This
  supersedes the run-24 hypothesis audit (`downstream_audit.py`,
  `notes/downstream_theorem_audit_2026-08-23.md`), which stays as a
  historical certificate that no derived claim depends on.  See `runs/64`
  and `notes/downstream_proof_chain_2026-08-28.md`.
* **The certified inventory is enforced, not assumed.**  Both filled-group
  checkers reject a batch that verifies any case twice, and in full-inventory
  mode (the default for the Ruby driver with no paths; `--full-inventory` for
  the Python checker) require the batch to be exactly the input's eight
  fillings, one file per case slug, over a source with 4 generators, 95
  complement relators, and 2 filling relators per case.  A duplicated batch
  is a negative control in both.  `make_proof_manifest.py` refuses to write
  or check a manifest unless `proof_certificates/` holds exactly one file per
  filling.  See `runs/65`.
* **The remaining trust boundary is explicit and machine-checked.**
  `proof_ledger.py` records an acyclic dependency graph from local certificate
  files and named external inputs to the three exoticness conclusions. It
  distinguishes geometric arguments from machine certificates. The former
  KBMAG software assumption is now removed: all eight original four-generator
  filled presentations have pruned derivation DAGs, and the small independent
  checker verifies every input-relator axiom, inverse axiom, critical overlap,
  rewrite trace, equation-tidying change, and final generator-to-identity rule.
  KBMAG is used only as an untrusted certificate generator. The former top-ranked
  smooth/combinatorial bridge is now stated and proved conventionally in one
  place, with the standard PL, bundle-classification, Moser, and Weinstein
  inputs exposed. A second peripheral extractor is now complete: starting
  only from `bundle.build_bundle`, it independently reconstructs the frontier,
  orientations, dual meridians, product push-offs, retraction, and literal
  `y_1`/`s_2` lassos. It separately recovers the local `N_grid` and the
  transported paper word `A*N_grid^-1*A^-1`, with no discrepancy. Residual
  bundle-construction risk is now independently cross-checked as well: a
  separate builder, importing neither `bundle.py` nor `layers.py`, produces a
  different 64-interface triangulation with the same marked beta homology
  action and peripheral semantics. Its full based action was then certified
  independently as `x->y^-1, y->yx, r->r, s->s` by 34,735 replayed Tietze
  substitutions, so the second route is no longer limited to homology.
  A simplex-level PL verifier now checks all 128 flip cone-balls, every
  untouched product prism, all 64 slab boundaries, and all 5,718 vertex links.
  The shared marked-fiber input is now independently cross-checked too: a
  58-vertex ribbon-graph triangulation, importing no `fiber.py`, has the exact
  same canonical crossing rotations, p/O faces, and involution action as the
  primary 86-vertex plumbing, with explicit common segment subdivisions.
  Run 36 binds the finite PL applications into one integrated replay: it
  checks rotation-system thickening and every bistellar trace while
  recomputing the direct PL self-intersection certificate. Run 50 then
  removes compatible four-dimensional source smoothing and a separate
  intersection-naturality theorem from the ledger: the marked bundle
  homeomorphism transports the actual certified cycles and collars into the
  paper's already smooth target. See `runs/25`, `runs/27`--`36`, `runs/50`, and
  `notes/pl_bridge_referee_packet_2026-08-25.md`.
* **The Acorn formalization path is specified against current GitHub.**  The
  live `acornlib` baseline is pinned at `bd1e602` (2026-08-20), not the stale
  local 2025 checkout. The proof-producing certificates now exist for all
  eight filled groups; the Acorn target is an axiom-free semantic replay of
  their finite-presentation derivation DAGs. This can shrink the checker trust
  boundary further without requiring smooth 4-manifolds or Floer theory.
  See `notes/deepseek_acorn_framework_spec_2026-08-23.md`.
* **Twist realization**: the mapping torus of one realize_twist has
  H1 = Z^2, torsion-free (a T^n would show Z/n); the identity control gives
  Z^3. This caught the session's one real mathematical bug — a two-band
  symmetric shear plus core-row rotation is a *finger rotation*, homotopic to
  the identity. The fix is k monotone shear rounds of ONE side band.
* **Monodromies** (`monodromy_check.py`, output in runs/03): Y matches the
  phi-tilde model fingerprint exactly [Z^3; 1,7,29,187,671]; the beta stack at
  (dir_b, dir_a) = (1, -1) matches the hex model (psi-tilde: x -> y^-1,
  y -> yx, r,s fixed) exactly [Z^3; 1,7,17,56,86]. (1,1) does not. This is
  what fixes `build_bundle(dir_b=1, dir_a=-1)`.
* **Bundle structure**: induced T is exactly two disjoint closed tori matching
  the two vertex lists; every 3-simplex meeting T has exactly 2 cofaces.
* **Certificate section 1**: pi1(K) = pi1(C)/<<mu_a, mu_b>> has the same
  fingerprint as the Prop 3.5 model of pi1(R): `[[0,0],[1,3,7,26]]`.
* **Certificate section 2**: pi1(C) matches the author's drilled relation
  sheet fingerprint.
* **Tietze provenance**: all 99,860 elementary eliminations in the target run
  are logged and independently replayed.  Each replay step recomputes its
  substitution from a current relator in which the eliminated generator occurs
  exactly once; input/output SHA-256 digests bind the log to the presentation.
  The T4 regression deliberately corrupts a step and confirms rejection.

## The caveat on sections 1 and 2 (read this before trusting them)

Prop 3.5, pi1(K) machine, pi1(C) machine, and **all eight** drilled(e3,e4,e5)
variants print the *same* fingerprint `[[0,0],[1,3,7,26]]` (runs/01). At
IDX = 4 the invariant is not discriminating: it cannot separate the drilled
8-generator system from the filled 6-generator one, so it also cannot separate
the eight sign variants from each other. Section 1 is a genuine consistency
check but a weak one, and section 2 currently proves less than it looks like.
Raising IDX (5-6) or using a sharper invariant (e.g. the abelianization of the
index-2/3 subgroups, or GQuotients onto small groups) would make these tests
actually bite.

This caveat is now historical. It was written when sections 1 and 2 were part
of the trust chain; since then all eight original filled presentations have
independently replayed derivation-DAG triviality proofs (runs/16--21, 25), so
the non-discriminating fingerprint no longer bears on the conclusion. The
sections stay documented as the weak consistency checks they are; sharpening
them is hygiene, not a gap.

## Certificate section 3: geometric n=0 groups certified trivial

The new sweep proves combinatorially that the transported beta basing arc has
one signed crossing with `T_alpha`.  A first experiment multiplied that
meridian into `lb_b` and produced many trivial quotients, but that operation is
not justified: `lb_b` is already a directly computed boundary longitude, so
the factor may already be encoded in it.  Multiplying it again can double-count
the correction.

The code now keeps four distinct words: the direct longitude `lb_b`, the
terminal boundary traced from the punctured grid `lb_b_sweep`, the oriented
meridian diagnostic `corr_b`, and a transported reference loop.  It constructs
the oriented grid 2-chain after deleting the target-torus vertex stars and
traces all three boundary components.  The independently based terminal cycle
satisfies

    lb_b_sweep = lb_b

exactly after the same elementary Tietze substitutions used to reduce the
presentation (`longitude_residual` is the empty word).  This is the missing
geometric check: the direct surgery longitude already incorporates the basing
effect, so adding `corr_b` to it would double-count.

The separately assembled paper-coordinate-style factorization

    lb_b_sweep = corr_b * beta_reference

still does not reduce under the current elementary Tietze pass (residual length
52).  That diagnostic uses a chosen dual meridian and hand-assembled reference
whisker rather than the traced initial and puncture cycles, so it is not used as
a surgery slope.  Resolving that coordinate factorization would improve the
comparison with the paper, but it is no longer needed to identify the actual
boundary longitude.

The historical locally based presentations below all have trivial
abelianization but resisted coset enumeration.  The explicit paper bridge now
sidesteps that opaque coordinate system: it bases the alpha and beta filling
pairs along `y_1` and `s_2`, respectively, and imposes their certified words
directly in the same triangulation-derived complement.  All four `n=0` sign
pairs collapse by complete confluent rewriting.  The four adjacent `n=1`
direct-loop systems also collapse. Their alternate beta-coordinate expression
is not needed for either filling computation and remains inconclusive. The old
eight word presentations are identified by the certified slope permutation and
standard boundary-whisker conjugacy.

### Proof-certificate and group-attack follow-up

`r_run.py` now emits `r_tietze_certificate.json.gz` (99,860 verified moves),
`r_presentations.json` (the complement, all tracked paths, and all eight
fillings), and explicit geometric candidate paths for the paper's
`x,y,r,s,A,B`.  The latter use five-chain cores in an unobstructed fiber slice
and base loops through the fixed point `p`; they are intentionally called
candidates because the paper uses particular whiskers.  Of the scanned
peripheral coordinate identities, one alpha-fiber convention reduces exactly;
the others remain word-problem questions and are not asserted.

The exported filled groups simplify in GAP to 3 generators, 10--13 relators,
and total lengths 181--261.  The following bounded attacks produced no proof:

* KBMAG Knuth--Bendix on all eight: nonconfluent, no generator reduction;
* automatic-structure construction on the shortest case: word-difference
  bound exceeded;
* ACE on each cyclic-generator subgroup and the trivial subgroup of the
  shortest case: table exhaustion;
* no epimorphism of that case onto A5, PSL(2,7), A6, or PSL(2,8);
* 100,000-step Nielsen/relator searches shorten four presentations slightly
  (best total length 177) but eliminate no generator.

These are conservative negative results.  Full commands and exact outputs are
in `runs/11-proof-certificate-and-group-attacks.txt`.

### Historical uncorrected result

All eight surgeries `pi1(C)/<<mu_a . lb_a^eA, mu_b . lb_b^eB>>`:

* H1 = 0 in every case (perfect — necessary for triviality, and it is what the
  paper's homology bookkeeping predicts), but
* coset enumeration **does not close**: GAP built-in overflows at 2M and 12M;
  ACE (in the docker image, and ~1000x faster) overflows at **25M cosets**
  under both `felsch` and `hard` on the simplified 2-gen / 8-relator / total
  length 306 presentation (runs/04, runs/06).
* No nontriviality witness either: no subgroups of index <= 10 other than the
  whole group, and no epimorphisms onto A5, PSL(2,7), A6, PSL(2,8) (runs/05).

So the group is perfect, with no small-index subgroups and no small quotients —
consistent with trivial, but **not proven trivial**.

### The historical diagnostic that motivated the sweep

Scanning the slope (runs/07): multiplying the beta longitude by `mu^-1`
(i.e. using `lambda . mu^-1` in place of the machine's `lambda`) makes the
quotient collapse to trivial **instantly, by Tietze alone**, with no
enumeration at all. Same on alpha. Every `k = -1` column is trivial; every
`k = 0` and `k = +1` column overflows.

That is exactly the shape of the **pushoff-basing correction** of the paper's
§7.4 — the step Wuebben flags as "the place where the first version of [M]
erred". His derived word is

    dir_base(T_beta) = (delta M^{-eps5} delta^-1) . B,   delta = r^-1

i.e. the honest based push-off differs from the paper's naive coordinate word
by one *conjugated* meridian on the left.  This initially suggested that the
machine's constant-normal `pushoff_loop` had missed the same factor.  The new
punctured-sweep comparison rejects that inference: the machine's direct
boundary loop already agrees with the geometrically transported terminal
cycle, including whatever coordinate correction is needed.

Testing the crude version of this (runs/08) — assume
`lambda_true = lambda_machine . mu^-1` on both tori — gives:

    drift=1 (1,1) TRIVIAL   (1,-1) TRIVIAL   (-1,1) TRIVIAL   (-1,-1) overflow
    drift=2 (1,1) TRIVIAL   (1,-1) TRIVIAL   (-1,1) TRIVIAL   (-1,-1) overflow

Six of eight collapse instantly. This is now understood as a deliberately
modified, double-counted slope rather than evidence for the correct geometric
one. The surviving (-1,-1) pair resists ACE at 25M
cosets on a 2-gen presentation with no index-<=8 subgroups and no A5 quotient
(runs/09) — same inconclusive posture as before.

### Current careful conclusion

The machine reproduces the bundle, the based monodromies and corrected
transport relations, both paper-coordinate base filling directions, and the
local meridian identifications.  Filling the triangulation-derived complement
with those explicit paper words proves all four geometric `n=0` fundamental
groups trivial by complete rewriting. Directly filling with the traced `y_2`
pair proves the four adjacent groups trivial as well, without using its open
alternate beta-coordinate expression. This resolves the group-theoretic
blocker for the specified manifold and both half-drift representatives.

It does not, by itself, formalize every ingredient of the full
exotic-manifold claim. The global marked-bundle comparison and the displayed
inline calculus of Lemma 8.2 now pass, but its three isolated standard smooth
theorem inputs remain cited rather than formally proved. The deductions from
simple connectivity to Theorems A, B, C are an explicit proof-grade chain
(runs/64, notes/downstream_proof_chain_2026-08-28.md) relative to 25 named
external theorems; each is stated with its hypotheses, each hypothesis is
discharged by a named certificate, computation, or earlier step, and the
theorems themselves are cited, not reproven.

The translation risk ("the encoding is ours") is no longer a single point of
failure. The peripheral data, bundle assembly, based monodromy, PL flip
traces, and marked fiber each have a structurally independent second route:
the independent peripheral extractor, the alternative bundle triangulation
(run 31), the 34,735-step second based-monodromy certificate, the simplex-
level verifier of all 128 flip cone-balls, and the 58-vertex marked-fiber
realization matched equivariantly to the 86-vertex model (run 34). A single
translation mistake would need to survive several structurally different
implementations. What redundant implementations cannot exclude is a shared
misreading of the paper's conventions; the exact Table 1 and M1--M3
comparisons and the sign-sensitive calibrations are the checks aimed at that
layer.

Accordingly the current careful claim: the proof appears complete relative to
explicitly named standard topology theorems, with no known project-specific
gap. Lemma 8.2's former lifting, flow, and chart-independence boundaries are
closed by Runs 43--47, and Run 49 closes the derived-frontier/normal-boundary
interpretation constructively. Run 50 bypasses the former PL/smooth source
smoothing boundary by transport into the paper's already smooth target. This
is not a foundational formal proof, but every construction-specific
hypothesis currently used at the remaining theorem boundaries has a finite
certificate.

Run 54 independently reconstructs the paper-to-model dictionary without
importing or reading the existing model, correspondence code, authors'
scripts, or prior certificates. Its raw-paper result is frozen before a
separate process compares the marked five-chain, twist order and signs,
surgery tori, `y_1`/`s_2` whiskers, and direction words with Runs 34, 51, and
52 and the path-level certificates. The comparison is exact, while mutation
controls distinguish the two closest rival twist readings. No discrepancy
was found.

Run 55 then attacks Lemma 7.1 rather than assuming it. A standard-library-only
checker enumerates all 36 independent cyclic-order pairs for the abstract
five-chain. Exactly four satisfy transversality, the chain-reversing
involution, two invariant faces, and orientation preservation, and all four
normalize to one marked ribbon by orienting the curves successively. Each
face is a 10-cycle on which the involution is the free shift by five. The
remaining input is now the exact classical periodic-disk theorem of
Kerékjártó (in the modern proof of Constantin--Kolev): an
orientation-preserving order-two disk action with one fixed point is
conjugate to the half-turn. Relative to that standard two-dimensional
theorem, Lemma 7.1 is proved.

Run 56 closes the remaining source-level question by auditing the immutable
Lidman--Piccirillo `arXiv:2505.14387v1` TeX and original vector Figure 1,
without reading Wuebben or any project model. The source prose supplies the
chain-reversing involution, oriented preservation of `c`, and exactly two
fixed points. Separating the original vector drawing's solid and hidden-side
dashed layers gives one surface crossing for `ab,bc,cd,de` and zero overlap
for every nonconsecutive pair. Thus every marked input consumed by Run 55 is
present in the original source; no source-to-Wuebben discrepancy was found.

Run 57 closes the remaining single-checker/runtime boundary for the eight
filled groups. `verify_certificates.rb` is a from-scratch Ruby implementation
using only `json`, `zlib`, and other Ruby standard-library components. It
reads the original four-generator presentations and all eight compressed
proof DAGs directly, checks all 14,115 retained records, and reaches the same
eight triviality verdicts as the Python checker. Its negative controls alter
an identity root, an input-relator equation, an internal rewrite trace, and
the presentation digest; all four are rejected.

## Next steps, in order

1. **Make the large preliminary Tietze trace standalone.** The 99,859-step
   committed trace is checked while `r_run.py` reconstructs its large input,
   but that 99,863-generator input was not serialized in the committed
   package. A clean second-language replay therefore requires a deterministic
   sealed input/output bundle. This concerns the preliminary presentation
   transport, not the Run-57 triviality proofs, which start from the committed
   original four-generator filled presentations.

2. **Leave downstream foundations downstream.** Freedman classification,
   Hambleton--Kreck, symplectic Kodaira dimension, Thom, Klug/Levine, and
   Heegaard Floer inputs remain published-theorem dependencies, now with
   their hypotheses discharged item by item in the run-64 chain. Formalizing
   those theories would be a separate foundational project.

## Recently closed high-risk boundaries

* **PL-to-smooth category bridge:** Run 50 constructs the reroute
  `|K| -> R_top`: the marked bundle homeomorphism transports the certified
  tori, collars, peripheral data, and Run-28 section cycles into the paper's
  already smooth target. The source is never smoothed. The transported
  section and its push-off remain disjoint and homologous, so square zero is
  proved in the target. Compatible four-dimensional PL smoothing and a
  separate intersection-naturality theorem are removed from the ledger.
* **Relative marked monodromies:** Run 51 checks exact alpha equivariance on
  all three rows of the `c` collar and the entire beta trace on the `e`
  collar. All 1,536 beta trace cells avoid that collar and its restriction is
  exactly the 3,072-tetrahedron product. Because the paper and model use the
  same supported word `T_a o T_b`, no relative isotopy-extension theorem is
  needed.
* **Bundle classification bypassed:** Run 52 is an assembly certificate plus
  an elementary quotient argument, supported by Run 34's marked fiber map,
  Run 51's actual collar-scale checks, and the ribbon/flip interpretations.
  It records `[x,t] -> [h(x),t]` on both mapping-cylinder handles and checks
  symbolic seam and inverse equations. There is no base two-cell.
  `T_surface_bundle` and Dehn--Nielsen--Baer are no longer required, but
  Run 52 is not presented as an independent large-scale machine proof.
* **Normal boundary/frontier:** Run 48 certifies local flatness at all 1,776
  torus simplices. Run 49 then gives the explicit level-set normal block
  neighborhood `sum_T(lambda)>=1/2` and the global PL homeomorphism
  `b(s) -> (b(s intersect T)+b(s minus T))/2` from the computed derived
  frontier to its boundary. All 592 dual meridians become literal normal
  circle fibers. `T_derived_regular_neighborhood` is no longer in the proof
  ledger.
* **Lemma 8.2:** Runs 43--44 give independent chart/framing arguments; Run 46
  constructs the equivariant Moser field upstairs; Run 47 constructs its
  general flow by monotone inversion. No connected-cover lifting,
  Picard--Lindelof, or ADK03 chart-independence input remains necessary.
* **Framing-shift robustness:** Run 45 freezes the original 100-case table;
  Runs 59--62 certify 17 of its 18 original holdouts.  Run 63 resolves the
  final aligned positive-diagonal `n0_y1` case through a 96-relator common-core
  certificate: the core is infinite cyclic and the case-100 filling relator
  kills its generator.  Independent Python and Ruby verifiers replay the
  retained 4,040-record ancestry DAG.  The final tally is 100 reported
  trivial (22 certificate-backed, 78 retained GAP-session verdicts), 0 inconclusive, and 0 nontrivial. These cases do not gate the
  paper's `j=0` proof.
* **Main fundamental groups:** all eight paper fillings have independently
  replayed proof-producing triviality certificates.
* **The interpretation layer is a bound artifact:** Run 53 collects every
  convention read from the paper into one dictionary with per-entry
  discriminating witnesses, and cross-checks it — by AST parse and verbatim
  relator match, never execution — against the author's own committed
  `develop.py` and `decide.g`: his psi action, alpha swap, and M1/M2/M3
  correction shapes (with his own `delta := r^-1`) match the certified
  package at `eA=+1, eB=-1`. Three entries are declared residual: the beta
  word order (action pinned, word not), the ribbon figure transcription, and
  the local twist signs. See `runs/53` and
  `notes/interpretation_dictionary_2026-08-27.md`.
* **Run 53's three paper-reading residuals were independently attacked:**
  Run 54 quarantines a fresh extractor to the raw paper text, reconstructs
  the ordered beta word, ribbon labels, and local twist signs, and compares
  only its frozen output with Runs 34, 51, and 52. The results agree exactly;
  reverse-order and reverse-sign controls fail as they should. The remaining
  boundary at that stage was the mathematical correctness of
  the paper's own Lemma 7.1 and marked-ribbon declarations, rather than their
  transcription into this model; Run 55 addresses it next.
* **Lemma 7.1's marked-ribbon boundary is closed:** Run 55 exhausts the
  compatible rotation systems, constructs the ribbon map on vertex disks and
  bands, and verifies the two invariant free-half-turn boundary cycles. Its
  disk extension is reduced to the explicitly cited periodic-disk involution
  theorem, with the smooth branch-chart lift written out in the accompanying
  note.
* **The original Lidman--Piccirillo marked input is bound:** Run 56 checks the
  immutable v1 TeX declarations and separates the original vector Figure 1
  into labeled solid and hidden-side layers. It recovers the ordered
  five-chain, involution, oriented `c` action, and two fixed points required
  by Run 55. No Wuebben or model artifact is an input to this extraction.
* **The filled-group checker has a second implementation:** Run 57 verifies
  all 14,115 retained derivation records in Ruby without importing the Python
  checker, compiler, GAP, KBMAG, or any project group module. It also rejects
  four targeted certificate corruptions.

Optional hygiene, no longer bearing on the conclusion:

* Sharpen certificate sections 1 and 2 so the fingerprint discriminates (see
  the caveat, now historical).
* Identify the other two traced cycles in paper coordinates, certifying or
  correcting the superseded `corr_b * beta_reference` diagnostic. Its failure
  to reduce stays documented, but the direct based peripheral paths supersede
  it; it is not evidence against the proof chain.

Done since this list was first written: the downstream
Freedman/Kodaira-dimension reduction has been audited at hypothesis level
with no gap found (runs/24, notes/downstream_theorem_audit_2026-08-23.md)
and then replaced by the proof-grade chain of runs/64,
and the certificate-producing group searches reached their goal — all eight
filled groups carry complete confluent rewriting certificates verified by the
independent checker (runs/16--21, 25), so further search batteries would add
nothing to the main theorem.

## Environment notes (save yourself an hour)

* No native GAP on this machine. `colima start`, then the shim `bin/gap` runs
  `gapsystem/gap-docker` (amd64, emulated on arm64 — slow but correct). Always
  run drivers as `PATH=~/luttinger/bin:$PATH python3 r_run.py` from
  `~/luttinger/luttinger`.
* **ACE and kbmag ARE in that image** (`ace-5.3`, `kbmag-1.5.9`). ACE is worth
  ~1000x: 25M cosets in ~2 min vs GAP's built-in doing 2M in ~20 min.
* ACE's `workspace` option must be an **integer** (`workspace := 100000000`).
  A string like `"600M"` is silently ignored and you get the 250k default —
  this cost a run.
* macOS has no `timeout(1)`.
* `SimplifiedFpGroup` can return a 0-generator group; guard
  `Length(FreeGeneratorsOfFpGroup(S)) = 0` before touching `tab[1]`.
* Unreduced presentations time out under emulation. Always Tietze first.

## runs/

Raw console output, in the order produced:

    01  r_run full pipeline + the three certificate sections
    02  bundle build + structural checks
    03  monodromy fingerprint selection
    04  pilot triviality diagnostic (simplify, cyclic subgroup, 12M)
    05  nontriviality probes (low-index, GQuotients)
    06  ACE at 25M cosets, felsch and hard
    07  slope scan — the mu^-1 discovery
    08  slip-hypothesis scan, all signs and drifts
    09  ACE on the two resistant (-1,-1) quotients
    10  triangulation-derived beta basing sweep and corrected surgery scan
    11  proof-producing Tietze replay, exports, and bounded group attacks
    12  based paper generators and first Table 1 relation checks
    13  local dual-meridian N identification
    14  M1 connector and M1--M3 completion
    15  alpha filling-direction identification
    16  four paper-coordinate fillings certified trivial
    17  adjacent half-drift and relator-ordering analysis
    18  local paper-inclusion tests in historical coordinates
    19  peripheral slope permutation and opposite-side y_2 basing
    20  all eight directly traced filling groups certified trivial
    21  hashed rewriting systems and all-eight reload/replay
    22  global marked-bundle correspondence and initial framing-chart audit
    23  path-level drilled-fiber basis and R3 transport certificate
    24  downstream theorem audit
    25  explicit proof ledger
    26  Acorn framework review
    27  standalone peripheral identification lemma
    28  direct PL self-intersection certificate
    29  independent filled-group derivation certificates
    30  independent peripheral extractor
    31  alternative marked-bundle triangulation
    32  exact based monodromy in the alternative beta trace
    33  local PL flip-trace certificate
    34  independent marked-fiber realization
    35  full inline framing calculus, precise ADK03 citation, referee packet
    36  integrated PL theorem hypotheses and referee packet
    37  surface-bundle boundary audit
    38  complement-presentation boundary audit
    39  framing-shift case 1 proof-preserving compaction (310-letter target)
    40  Lemma 8.2 typeset-PDF re-audit and explicit Moser flow
    41  framing-shift case 2 frozen input and compaction (439-letter target)
    42  simplicial equivariant-lift certification (covering + deck group)
    43  Weinstein chart independence, fiber-dilation route
    44  Weinstein charts second route (Liouville-forced momenta, SL2 invariance)
    45  framing-shift robustness table, frozen (82 trivial / 18 open / 0 nontrivial)
    46  direct equivariant Moser field upstairs
    47  cumulative-coordinate Moser flow, ODE citation removed
    48  exhaustive local flatness of both surgery tori (1,776 link pairs)
    49  explicit half-weight normal block model and frontier equivalence
    50  PL-to-smooth reroute through the already-smooth target
    51  direct relative marked monodromies (c and e collars)
    52  explicit marked graph clutching (symbolic assembly)
    53  interpretation dictionary with author-code cross-check
    54  independent raw-paper dictionary reconstruction
    55  Lemma 7.1 equivariant normal form (periodic-disk reduction)
    56  original Lidman--Piccirillo source-figure audit
    57  independent Ruby verifier for all eight filled-group proof DAGs
    58  undecided scan case certified from its unsimplified presentation (83/17 current)
    59  raw-presentation certificates for 13 framing-scan holdouts (95/5 current)
    60  raised-limit certificate for n1_y2 (+,-), shift (+1,-1) (96/4 current)
    61  raised-limit certificates for two n0_y1 holdouts (98/2 current)
    62  tidyint-sensitive certificate for n1_y2 (+,+), shift (+1,+1) (99/1 current)
    63  common-core certificate for the hundredth framing case (100/0 final)
    64  downstream proof chain from Theorem D to Theorems A, B, C
    65  batch inventory checks in both filled-group checkers and the manifest generator
