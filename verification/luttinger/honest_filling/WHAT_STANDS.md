# What stands, whichever way pi_1(V_aud) falls (3 September 2026)

Four results survive the 2 September finding that the sealed certificates prove
the wrong group. Each is stated with the artifact that backs it and what it does
not depend on. Nothing here asserts or denies `pi_1(V_aud) = 1`.

## 1. A derived, sealed, replayable model of the construction

The marked genus-two bundle over the thickened figure-eight base, its two
surgery tori, and the complement are built as simplicial complexes and their
groups read off the triangulation (`bundle.py`, `r_run.py`, `complement.py`).

| what | artifact |
|---|---|
| complement presentation `Q` (3 generators, 78 relators), fixed hash seed, Tietze transport replayed | `sealed_transport/r_presentations.json`, `r_tietze_input.json.gz`, `r_tietze_certificate.json.gz` |
| based monodromies certified against Prop. 3.5; second, independently built triangulation | `graph_clutching_certificate.json`, `pl_flip_trace_certificate.json`, `alternative_bundle_certificate.json` |
| marked fiber realized twice, matched equivariantly | `independent_fiber_certificate.json` |
| both tori locally flat at every simplex link | `torus_local_flatness_certificate.json` |
| meridians and longitudes traced as literal simplicial loops; reproduced by a separate extractor | `independent_peripheral_certificate.json`; identities `lb_a_y1 = A x`, `lb_b_s2 = r^-1 M r B` certified in `Q` (runs 68, 69) |
| the eight honest Dehn-filling relators, common whisker, read from the boundary three-tori | `simplicial_filling/`, `honest_filling.json` |
| framing lemma: Weinstein-chart, seam and Moser identities executable | `framing_check.py`, `moser_flow_check.py`, `moser_cumulative_flow.py`, `equivariant_moser_lift.py` |

What was wrong in the sealed chain is one word shape, not the model: the
sealed beta relator paired a meridian whiskered along `A` then `s_2` with a
longitude whiskered along `s_2`. The derived relator has the common whisker.
Depends on: the triangulation and the scripts. Does not depend on: Wuebben's
text, any dictionary, any claim about `pi_1`.

## 2. The reduction: one commutator

For each of the eight honest cases `H = Q / << alpha, beta_honest >>`:

* `H = << [A, N_grid] >>` — the sealed group is `H` with one extra relation
  whose normal closure is this commutator, and the sealed certificates prove
  it trivial (`README.md`, "Two single-commutator characterizations").
* `H = << [B, M] >>` — coset enumeration on the 30 certified relations plus
  the honest fillings overflows at 200,000 cosets in every case and closes to
  index 1 the moment `[B, M] = 1` (or `M B = 1`) is added, all eight cases
  (`direct_z_variants/mb_collapse/mb_collapse.log`).
* `H = << [A, B] >>` — the base-boundary loop; case `y1_p1_p1`, 3,000,000
  cosets (`wuebben_dictionary/quotients.g`).

So `pi_1(V_aud) = 1` iff the beta base loop `B` commutes with the alpha
meridian `M` in the honest filled group, iff the alpha base loop `A` commutes
with the beta meridian `N_grid`. Decision tools return nothing either way:
Knuth–Bendix to 500,000 equations in two orderings, coset enumeration,
low-index subgroups to 7, no nonabelian simple quotient of order below
546,312, no small linear representation (`README.md`, "Decision attempts").
Depends on: `Q` and the honest relators (item 1). Does not depend on:
Wuebben's paper at all.

**The one open door.** `M` is the alpha meridian in the complement. If `M = 1`
in `Q`, then `[B, M] = 1` and every honest group is trivial. `M` is trivial in
every finite quotient of `Q` tested and nothing decides it (`README.md`,
"What is not yet certified").

## 3. Where Wuebben's sheet and the derived sheet part: one alpha meridian

Wuebben's Table 1 (arXiv:2608.17267v1) is written on loops named like ours.
Under the re-basing dictionary

    y -> M^-1 y,   s -> r^-1 M^-1 r s,   M -> B M B^-1,   N -> M^-1 N M   (x, r, A, B fixed)

his nine non-filling rows reduce to the empty word in the complement system,
i.e. they are identities of `Q` (`wuebben_dictionary/`, stage scripts and
`membership_sheet_words_500k.log` controls). His alpha filling relator is
`M_W (A x)^{eA}` with `M_W = B M B^-1`; the derived one is `M (A x)^{eA}`.
Modulo the derived relator (`A x = M^-1` for `eA = 1`) the two differ by
exactly

    M_W (A x) . (M (A x))^-1  =  B M B^-1 M^-1  =  [B, M],

and in the halted honest system both `F1_W` and `[B, M]` reduce to the same
normal form `x N^-1 B^-1 A` (`membership_sheet_words_500k.log`, also at 150k
and in the augmented 42-relation system), which is a proof of equality
whether or not the system is confluent. Hence:

> Read on the loops derived from the audit complex, Wuebben's displayed
> sheet is the honest sheet plus the single relation `[B, M] = 1`. His coset
> enumeration proves trivial exactly the group we cannot decide, with the
> undecided commutator added as a relation.

Geometrically the difference is one alpha meridian of basing: his meridian
`M_W` is ours transported around the beta base loop (in his derivation the
loop meets the alpha torus before the beta twist, in ours after). The
Dehn-filling relator kills the meridian that shares the longitude's whisker;
with the longitude `A x` common to both sheets, his alpha relator, read on our
loops, mixes two whiskers in the same way our sealed beta relator did.

**Traced in the complex (3 September, `x_transport/`).** Every row above is
now certified literally from the triangulation, not only by reduction of
typed words: `B x B^-1 = y^-1 M` is assembled from four pieces (the angular
squares, the radial grids over `x` and `y`, the twist band with the `e`
vertices deleted), each transported through the sealed 99,860-step Tietze
certificate and reduced to the empty word (`x_transport/certify_pieces.log`).
The radial grid over `x` meets neither torus; the grid over `y` meets the
alpha torus in exactly one vertex, and the link cycle there, with its direct
whisker, is the sealed `M` inverted. Along the inverse base loop the `x`
transport is clean, `B^-1 x B = x y`, and it is `y` that is punctured, with
correction `B^-1 M B`, the meridian conjugated by the base letter.

That is the mechanism, checkable by hand: for a fiber loop swept along a base
loop, a puncture that lies *before* the wrap contributes its meridian
conjugated by the base letter; a puncture *after* the wrap contributes it
unconjugated. Wuebben's torus meets the sweep before the wrap (his Remark 6.3,
Fig. 2); ours after the band. The two positions differ by an isotopy sliding
the torus along the beta loop through the fiber over the base point, which
fixes `x, r, A, B`, inserts a meridian into `y` and `s` (the dictionary rows),
and carries the direct-whisker meridian to itself, `M -> M`, not to
`B M B^-1`. Under that geometric map his printed x row is our certified row
(so the x row is *not* where the sheets part), his alpha filling `F1` is
exactly the derived honest filling `M A x`, and his two corrected rows `M2`,
`M3` equal ours times `[B, M^-1]` and `r^-1 [B, M^-1] r` (all quotients
reduce to the empty word, `x_transport/wuebben_rows_two_maps.log`). Under the
algebraic dictionary (`M -> B M B^-1`) his rows are identities of `Q` and his
`F1` differs from the derived filling by `[B, M]`, as above. Both readings
give the same group:

> Wuebben's eleven-relator group is the honest filled group with `[B, M] = 1`
> adjoined. The step: the meridian correction from a puncture that lies
> before the wrap was written without the conjugation by `B` that the
> transport annulus imposes.

**The beta side (same day, `x_transport/beta_side.*`, `his_fillings_enum.*`).**
With `K = r^-1 M r = A M A^-1` (certified), the only image of his beta
meridian under which his transport row `A s A^-1 = N y` becomes an identity
of `Q` is `N_W = K^-1 (A^-1 N A) K`. With it his alpha filling is the honest
one and his beta filling differs from the honest beta filling by the free
word `[K^-1, N_dir]`; his printed push-off `(r^-1 M r) B` agrees with the
isotopy image only if `[B, K] = 1`. So on our loops his beta meridian and
longitude do not share a whisker either. Coset enumeration on the 30
certified sheet relations, 3,000,000 cosets, all four sign pairs: the honest
fillings overflow; his fillings under the geometric map close to index 1,
and under the algebraic dictionary close to index 1; mixing one of his with
one of ours closes too. Under the geometric reading the collapse comes
entirely from his beta filling, so the honest group is also
`<< [K^-1, N_dir] >>`. Four commutators now each generate the honest group as
a normal closure (`[A, N_grid]`, `[B, M]`, `[A, B]`, `[K^-1, N_dir]`) and none
is decided.

> Whichever way his sheet is read on the derived loops, each of Wuebben's two
> filling relators is a meridian and a longitude carried on different
> whiskers, and his group is the honest group with one such commutator set
> to 1.

Depends on: item 1 and the reductions named. Argued, not machine-checked: the
isotopy between the two torus positions (his position is not a subcomplex of
our complex, so his configuration was realised through the inverse loop). Not
done: his beta-side row `M1` and filling `F2` under the geometric map, and
the enumeration of `Q` modulo his two fillings under that map. Still open,
and still the only thing that could reverse all of this: `M = 1` in `Q`
(Part D of `x_transport/README.md`: `M` dies in `H_1` of every cover of index
at most 5 and of the `(Z/n)^2` covers for `n = 3, 4, 5`; enumeration over
`<M>` overflows at 2,000,000 cosets).

## 4. The failure mode, named

Three words in this project entered a certificate by transcription and
proved a different group trivial: the sealed beta relator (two whiskers), the
printed x-transport row `B x B^-1 = y^-1` (certified only as `y^-1 M`), and
the boundary word of the direct double (the `A`-conjugate of the derived
class). Item 3 shows Wuebben's alpha filling has the same shape. The
remedies now in the tree: every word a certificate consumes is listed with
its provenance (`WORD_PROVENANCE.md`); no doubled presentation reaches a
certificate without passing the boundary-monodromy identity
(`direct_z_variants/seam_gate.py`); filling relators are read from the
boundary three-tori, not written (`simplicial_filling/`). Depends on: nothing
but the record.

## What none of this is

Not a proof or refutation of `pi_1(V_aud) = 1`; not a statement about
Lidman–Piccirillo's computation, which is not public; not an existence
result. The public README on `main` and the v2.4.0 release page carry the
withdrawal of the Theorem A′ headline (commit d61f1b4, 3 September).
