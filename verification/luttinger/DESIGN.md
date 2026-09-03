# DESIGN — formalizing (a)–(c) of the §8 obstruction

Goal: a machine that takes a *combinatorial* description of a symplectic
4-manifold built from a surface bundle, plus Lagrangian product tori, and
outputs the based meridian words and Lagrangian-framing push-off words, so that
the only human inputs are (i) the triangulation and (ii) one symplectic lemma
("the fibered framing is the Lagrangian framing", = paper Lemma 8.2).

Everything below is textbook PL topology; no step is a judgement call.

## 1. Model of the complement
`K` a simplicial closed 4-manifold, `T ⊂ K` a 2-dim subcomplex (torus or
disjoint union of tori) which is **full** (every simplex of K with all
vertices in T lies in T).

* **Lemma A** (Rourke–Sanderson 3.?): if T is full, |K| − |T| deformation
  retracts onto `C := K[V(K) ∖ V(T)]` (induced subcomplex). We compute
  π₁(C) by spanning tree + 2-simplices. Sizes are tiny (T⁴ on 3×3 grids:
  81 vertices, 1944 4-simplices; C has 865 generators → 4 after Tietze).
* **Lemma B**: in the first derived K', the derived neighbourhood
  `N(T) = {chains s₀<…<s_k : s₀ ∈ T}` is a regular neighbourhood, and its
  frontier `Ṅ = {chains, none in T, all meeting T}` is a triangulation of
  ∂ν(T) ≅ T³. (Fullness of T in K is what makes the *first* derived suffice.)
* **Lemma C**: `r : C' → C`, `r(b(s)) = max-order vertex of s ∖ T`, is a
  simplicial map homotopic to the retraction, hence iso on π₁. (It is the
  composite of the straight-line retraction b(s) ↦ b(s∖T) with the standard
  simplicial approximation (C)' → C of the identity.)

So: every boundary loop is built as an edge loop **in Ṅ**, pushed to C by `r`,
and read as a word in π₁(C). Basing: meridian and push-offs of the same torus
are joined to the same vertex u₀ ∈ Ṅ by paths in Ṅ; since π₁(Ṅ) = Z³ is
abelian, *any* such paths give the same based elements, and the surgery
relator μ·λ^k is then well defined. This is exactly the [BK09 §2] basing
discipline, mechanized.

## 2. The loops
* **Meridian**: for a 2-simplex σ of T, the dual 2-cell D(σ) in K' is a disc
  transverse to T at b(σ); its boundary ∂D(σ) = alternating 3-/4-simplices
  containing σ (the link circle of σ). All lie in Ṅ. That loop is μ.
* **Push-offs** (product tori α×β in a product-like chart): the loop through
  the edges {(a,b),(a,b′)} (a∈α, b′ a neighbour of b off β) is the push-off
  of α×{b} along the base normal; {(a′,b)} gives the push-off of {a}×β along
  the fiber normal. Within each square {a₀,a₁}×{b,b′} the loop is joined by a
  BFS in Ṅ. Constant normal vector along the torus ⇒ product framing.
* **Surgery**: π₁(V) = π₁(C)/⟨⟨ μ_i · λ_i^{k_i} ⟩⟩, λ_i = λ_base^p λ_fib^q, all
  four sign conventions enumerated (as the paper does).

## 3. Why this formalizes (a)–(c)
* (a) "Figure 1 is a correct drawing of the LP curves": replaced by a finite
  check. Lemma 7.1 of the paper says the marked surface is determined by the
  five-chain's intersection pattern + the involution. Input the five curves as
  edge cycles in the triangulation; the machine verifies pairwise
  intersection counts and φ₀-equivariance. No picture is read.
* (b) "crossing counts of transport annuli with the tori": never computed.
  They are consequences of the 2-skeleton of C; the machine doesn't know what a
  transport annulus is.
* (c) "Lagrangian framing": the only non-combinatorial input. The machine uses
  the fibered (product) framing; Lemma 8.2 of the paper (and the standard
  fact for products Σ×Σ) identifies it with the Lagrangian framing. That lemma
  is symplectic geometry and stays a lemma. Everything downstream of it is
  mechanical.

## 4. The bundle case (Wuebben's R) — the plan as written 22 Aug 2026
(Realized in `bundle.py` / `r_run.py`; the checks it calls for are the ones
listed in §5. Kept as the design record.)

R = genus-2 fiber F over the once-punctured torus T₀, monodromy φ₀ (half-turn
of the octagon) along α, ψ₀ = T_a T_b along β; T_α = c × α (φ₀(c)=c setwise,
half-rotation), T_β = e × β (ψ₀ = id near e).

**Base.** Don't use the cut square (the four corners are one point of T₀ and
carry incompatible triangulations unless [φ₀,ψ₀]=id as maps). Use
T₀ = disc D ∪ band₁ ∪ band₂ (thickened figure-8); tori sit over the band
cores closed through D; no corner consistency is needed.

**Fiber triangulation L.** Needs: (i) φ₀-invariant (half-turn of the octagon
is a simplicial automorphism if L is rotation-symmetric); (ii) c, e
chordless edge cycles; (iii) the five-chain a,b,c,d,e as edge cycles with the
right intersection pattern (this is the (a)-check); (iv) p and O vertices.

**Monodromy ψ₀ without coordinates (recommended).** Realize T_a T_b as a
sequence of edge flips L = L₀ → L₁ → … → L_m followed by a simplicial
relabeling L_m ≅ L. A Dehn twist about an edge cycle of length k in a
collar is a standard flip sequence. Each flip gives a simplicial cobordism
F×[i,i+1]: ordinary staircase prisms over untouched triangles, and over the
flipped quadrilateral Q the ball Q×[0,1] coned from one new interior vertex
(boundary = 2 bottom + 2 top triangles + 4 vertical squares with diagonals
matching the neighbouring prisms). Stack the layers; this is F×[0,1] with
bottom L and top ψ₀⁻¹L, as a genuine simplicial complex. Band₂ = that stack
× I (staircase). Band₁ = L×[0,1]×I glued by φ₀. D = L × (triangulated disc).
Glue along L × (arcs of ∂D) — consistent if one global vertex order is used.

**Verification built in.** Compute π₁(R) from the triangulation and check it
against Prop. 3.5 (`⟨x,y,r,s,A,B | [x,y][r,s], AgA⁻¹=φ̃(g), BgB⁻¹=ψ̃(g)⟩`)
by fingerprints — this certifies the flip sequence realizes the right *based*
automorphism, not just the right mapping class. Then run `TorusComplement` on
T_α ∪ T_β, take the meridians and the push-offs
(dir_base, dir_fib per torus), impose μ·dir^{±1}, and compare with Table 1 /
`fixed_v_certify.g`. The machine's relators for the monodromies will be its
own (generators = non-tree edges); comparison is by group fingerprints and by
the explicit isomorphism to Prop. 3.5 obtained from the tree.

Keeping T_α, T_β **full**: c and e chordless; the band-core paths chordless
in the base; the cone vertices of flip layers are never in a torus, so no
spurious spanned simplices; check `K.is_full(T)` (the code asserts it).

**Size.** L with ~30 vertices, ~20 flips, base with ~30 vertices: K has
~10⁵ 4-simplices. `complex.product` is naive Python; expect to rewrite the
product and `is_full` with indexed lookups. Python Tietze handles 10⁴
generators; GAP takes the rest.

## 5. Honest scope (revised 2026-09-03)
The original §5 (22 Aug) predates the bundle build and is superseded.

* **Done by machine.** The marked bundle R over the thickened figure-8
  base (`bundle.py`, `r_run.py`), its fundamental group and the two-torus
  complement, all from the triangulation. The based monodromies are certified
  against Prop. 3.5 by replayed Tietze transports, and again on an
  independently built second triangulation (`alternative_bundle.py`); the
  marked fiber has a second, import-free realization matched equivariantly
  (`independent_fiber.py`). Both tori are certified locally flat at every
  simplex link. Meridians and longitudes are traced as literal simplicial
  loops with named whiskers and reproduced by a separate extractor
  (`independent_peripheral_extractor.py`). The complement's presentation is
  sealed with a fixed hash seed. Filling that presentation with the sealed
  peripheral words gives eight groups that are trivial by complete confluent
  rewriting, each certificate replayed by two checkers.
* **The framing lemma (8.2) is a written lemma with executable identities,
  not a certificate.** Its Weinstein-chart, seam, and constant-momentum
  algebra are checked exactly (`framing_check.py`); the Moser flow is
  constructed rather than cited (`moser_flow_check.py`,
  `moser_cumulative_flow.py`); the equivariant lift is built on the
  simplicial collar (`equivariant_moser_lift.py`); chart independence is
  argued twice in-project, with Weinstein germ uniqueness as corroboration
  only. What is not mechanized is the lemma's content as symplectic
  geometry: that the fibered framing *is* the Lagrangian framing is still
  read from the argument, with each identity in it executable.
* **Open, and the current boundary of what is proved (found 2 Sep 2026;
  `honest_filling/README.md`).** The sealed filling relators are not Dehn
  filling relators of the tori as based: the beta relator pairs a meridian
  whiskered along `A` then `s_2` with a longitude whiskered along `s_2`
  alone. The honest filled group differs from the certified one by the
  single commutator `[A, N_grid]`, and it is undecided: Knuth–Bendix to
  500,000 equations, coset enumeration, low-index subgroups, finite
  quotients to order 604,800 and small linear representations all return
  nothing either way. So the machine route derives the complement, the
  seams, and the peripheral words, and proves the *sealed* presentations
  trivial; it does not establish that pi_1 of the filled manifold is
  trivial. Two further rows are open: the printed transport
  `B x B^-1 = y^-1` is certified only as `y^-1 M`, with `M` undecided in the
  complement; and the direct double's boundary word, now derived from the
  complex (`direct_z_variants/`), gives a doubled presentation that does not
  collapse at 500,000 equations. The doubling involution and the descent of
  the symplectic form to the double are defined from audit data (runs
  72–73); the double's fundamental group is not known.
* **Cited, not mechanized (unchanged in kind).** Simplicial
  fundamental-group and Tietze theory, the classification of surfaces, the
  local-flatness criteria, Kerékjártó's periodic-disk theorem, and the
  downstream chain's named theorems; see the repository README, "What is
  not claimed".
