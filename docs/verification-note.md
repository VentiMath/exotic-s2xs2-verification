# Independent machine verification of the fundamental-group computation in Wuebben's "An exotic S²×S² and an exotic ℂP²#C̄P²"

*Draft — numbers and artifact references are finalized against the imported
certificates before any submission. Author: John Clyde (VentiMath), with
AI assistance disclosed in the provenance section.*

## 1. Introduction

Claimed constructions of small exotic 4-manifolds have historically failed in
one place: the fundamental-group computation. Wuebben (arXiv:2608.17267),
building on Lidman–Piccirillo (arXiv:2505.14387), constructs a candidate
exotic S²×S² and a candidate exotic ℂP²#C̄P² by Luttinger surgery on a
non-product genus-2 surface bundle over a genus-2 surface, and the proof's
critical step is the triviality of eight fundamental groups obtained by
filling the surgered complement.

This note reports a verification of that step that is independent of the
paper's coordinates, software, and author: the bundle is rebuilt as a
simplicial complex from the paper's marked-fiber data alone, the surgery
tori, meridians, and framed longitudes are extracted combinatorially, and the
resulting filled presentations are proved trivial by complete confluent
rewriting, with every computation emitting a replayable proof certificate
checked by a small independent verifier. The deductions downstream of simple
connectivity are audited against the hypotheses of the classification,
symplectic, and Floer-theoretic results they cite.

The conclusion, stated carefully: the proof appears complete relative to
explicitly named standard topology theorems, with no known project-specific
gap. Section 8 lists the named theorems; none of them is project-specific,
and each is applied with hypotheses that have been checked mechanically or by
direct audit.

## 2. The independent model

The genus-2 fiber is realized as a regular neighborhood of the paper's
five-chain of curves (five plumbed annular bands and two cone discs), with
the hyperelliptic-type involution realized simplicially: the fixed points,
the curve actions a↔e, b↔d, and the free half-rotation of the middle curve
are executable assertions, not assumptions. The bundle R is assembled from
simplicial mapping cylinders over a once-punctured-torus base; the two
surgery tori arise as induced subcomplexes. The assembled 4-complex passes
manifold checks down to the vertex-link level.

The identification with the paper's marked bundle is by literal based
monodromy action — the based mapping classes of both monodromies are
certified as equalities of vertex paths, transported by proof-producing
Tietze chains that replay step by step — and then by an explicit
marked mapping-cylinder clutching over the base graph: the relative
monodromy comparisons are exact on the marked collars, so the identification
is a constructed fiberwise homeomorphism into the paper's bundle rather than
an appeal to the classification of surface bundles. Everything the surgery
argument needs is transported through that map into the paper's
already-smooth manifold, where the symplectic arguments are performed; no
smoothing of the triangulation is ever chosen.

## 3. Peripheral data

Based meridians and product-framing longitudes for both tori are traced as
literal simplicial loops carrying the paper's own basing whiskers. The
paper's sign-correction package is reproduced independently, and a
combinatorial sweep of the relevant transport square resolves the basing
double-count question: the directly computed boundary longitude already
contains the geometric basing effect, exactly as the paper's corrected
convention requires.

Both surgery tori are certified locally flat at all 1,776 of their simplex
links, and the boundary carrying the peripheral curves is an explicit
half-weight normal block model with a global PL identification of the
computed frontier: every extracted dual meridian is checked to be a literal
normal-circle fiber, with no regular-neighborhood theorem invoked.

## 4. The eight filled groups

Filling the triangulation-derived complement presentation with the certified
coherent peripheral pairs yields, for all four n=0 sign pairs and the four
adjacent half-drift systems, complete confluent rewriting systems in which
every generator reduces to the identity. Knuth–Bendix completion (KBMAG) is
used only as an untrusted certificate generator: the exported derivation DAGs
are verified by an independent checker that re-validates every input-relator
axiom, inverse axiom, critical overlap, rewrite trace, and final
generator-to-identity rule. All artifacts are bound by SHA-256 and replay.

## 5. Redundancy against translation error

Because the machine certifies properties of a model, the model itself is the
residual risk. Five structurally different implementations attack it: an
independent peripheral extractor built only from the bundle; an alternative
bundle triangulation with a different subdivision; a second based-monodromy
certificate on that alternative; a simplex-level verifier of all PL flip
traces; and a second marked-fiber realization, built directly from the
abstract ribbon graph with a different vertex count, matched equivariantly to
the primary model. A single translation mistake would need to survive all of
them. What redundancy cannot exclude — a shared misreading of the paper's
conventions — is attacked separately by exact reproductions of the paper's
own displayed relations and sign tables, and by a bound interpretation
dictionary: every convention read from the paper carries the certified
computation that would fail under a rival reading, and the central entries
are cross-checked — parsed, never executed — against the author's own
committed scripts, which define the same actions, corrections, and sign
conjugators. The three entries that reading could pin only by transcription
— the ordered beta twists, the five-chain ribbon labels, and the local twist
signs — are then closed at the raw-paper level: a quarantined extractor
reads only the paper's plain text, reconstructs the five-chain, involution,
ordered twists, surgery tori, whiskers, and direction words, and a separate
process compares its frozen output with the independently built model
certificates. Reversed-order and reversed-sign mutations are distinguished,
and no paper-to-model discrepancy was found. The paper's own Lemma 7.1 is
certified rather than assumed: all 36 candidate equivariant ribbon rotations
are enumerated, exactly four survive and all normalize to one marked ribbon
with two invariant free-half-turn boundary disks, and the lemma's disk
extension reduces to the classical Kerékjártó periodic-disk involution
theorem. What remains on this axis is ordinary implementation trust — a
checker and its review both being wrong — not a declared unverified
reading.

## 6. The framing lemma

Luttinger surgery is performed with respect to the Lagrangian framing; the
paper's Lemma 8.2 identifies it with the fibered framing used by the
combinatorial longitudes. The lemma's displayed Weinstein-chart, seam, and
constant-momentum algebra are machine-checked, and its inline analytic
normalizations have been rebuilt constructively rather than cited. The Moser
flow is produced as the explicit monotone inverse of a cumulative coordinate,
so no ODE existence theorem is invoked; the equivariant step defines the
Moser field directly on the double cover with certified projection, deck
invariance, and factor-two normalization, so no covering-lift theorem is
invoked; and the covering hypotheses themselves — free involution, genuine
2:1 simplicial covering, deck group exactly {id, φ₀}, core winding number
two — are certified on the actual simplicial collar. Chart independence is
argued twice within the project: a fiber-dilation isotopy takes any
chart-transition germ to the identity relative to the zero section, and a
construction-side proof shows the paper's charts are forced by pairing the
Liouville primitive with the well-defined angle frames, with every integral
angle-basis change preserving constant momentum and the one symplectic move
that could add meridian components — the closed-1-form shift — excluded by
the zero-section condition. ADK03 §2.1 and Proposition 2.2 stand as
corroboration. After this program, no standard input to the lemma remains
cited rather than mechanized: the only form of Weinstein germ uniqueness
the argument uses — independence of the constant-momentum push-off between
the paper's displayed charts — is the statement proved above.

The lemma's exact logical load: if the identification failed by j meridians,
the machine certificates would remain correct for the product-framed
presentations they literally describe, but would no longer identify those
presentations with the paper's surgeries; simple connectivity, the Freedman
conclusions, and the exoticness argument for the claimed manifolds would
become unproved. A completed slope-robustness scan — refilling the
complement with the meridian-shifted longitudes and running the same
certification pipeline — quantifies which discrepancies j are independently
excluded. Of 100 shifted cases across both half-drift families, 82 are
certified trivial (40 by proof-producing Tietze collapse, 42 by complete
confluent rewriting), 18 remain undecided, and none is nontrivial. The
undecided groups are all perfect, admit no quotient onto the six smallest
nonabelian simple groups, have no proper subgroup of index at most 8, and
resist coset enumeration to a 12.5M-coset ceiling. Every shift touching
only the second surgery torus is certified trivial in both families; all
undecided cases involve a shift on the first torus. The full verdict table
is reported with the artifacts.

## 7. The downstream audit

Conditional on the certified simple connectivity, the deductions of the
paper's main theorem pass a hypothesis audit: the covering exact sequence and
Hambleton–Kreck classification data; the even and odd rank-two intersection
form calculations feeding Freedman's classification; minimality and
symplectic Kodaira dimension (two independent routes); the symplectic Thom
genus bound behind the no-torus lemma; the lifted-torus and Rokhlin/Arf steps
of the slicing argument; and the reuse of the Lidman–Piccirillo relative
Floer argument, including why the stronger π₁ statement is the one the
regluing needs. The elementary lattice, Euler, cover-genus, and adjunction
computations are executable.

## 8. Trust boundary

The named standard inputs, applied with checked hypotheses and cited proofs:
the elementary ribbon-thickening and bistellar-trace interpretations that
read the paper's figures into complexes; the classification of surfaces; the
collapsible-3-ball and cyclic-knot-unknot criteria behind the local-flatness
certificates; simplicial fundamental-group presentation and Tietze theory;
the Kerékjártó periodic-disk involution theorem behind Lemma 7.1's disk
extension; Freedman's simply connected classification with the Hambleton–Kreck
finite-cyclic classification; symplectic Kodaira dimension and minimality
(via the audited ADK / Ho–Li Luttinger-surgery constructions); the
symplectic Thom theorem; the Rokhlin/Arf input of the slicing argument; and
the Ozsváth–Szabó / Lidman–Piccirillo Floer machinery. This note does not
reprove them.

Formerly listed inputs that are no longer dependencies: surface-bundle
classification (replaced by the explicit clutching of §2); four-dimensional
smoothing and intersection naturality (the smooth arguments run entirely in
the paper's already-smooth manifold, and the section's square is computed
there from transported disjoint homologous cycles); derived-regular-
neighborhood theory (the tubular boundary is constructed — see §3); and
Weinstein germ uniqueness (chart independence is proved between the paper's
verified charts — see §6; ADK03 remains corroboration).

## 9. Provenance and method

The verification was AI-assisted throughout (Anthropic Claude Fable 5 and
Opus 5; OpenAI Codex), under human direction and with commit-level model
provenance. Cross-model review was adversarial by design, and several
load-bearing corrections in the record came from one model refuting the
other's assessment. Mathematical responsibility rests with the human author.
Every asserted computation ships with a replayable certificate; no claim in
this note depends on trusting a model.

## 10. Data availability

All code, certificates, run logs, and the provenance ledger:
https://github.com/VentiMath/exotic-s2xs2-verification. The paper's own
code: https://github.com/bwuebben/exotic-s2xs2.
