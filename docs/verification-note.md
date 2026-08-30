# Prose companion to “A certificate-based audit of simple connectivity for an explicit model associated with Wuebben's proposed exotic S²×S² construction”

> **Known unreconciled external computation.** Wuebben's repository has stated,
> since its first visible commit and continuously since, that Lidman and
> Piccirillo report a computation of π₁(V) that disagrees with his, and that the
> disagreement is unresolved. Their published v1 never asserts π₁(V) ≠ 1 — it
> proves H₁(V) = 0 and normal generation by π₁(F) — and no relation sheet or
> nontriviality witness for the contrary computation is public. Their v1 source
> also explicitly declines to fix the surgery parametrization, while Wuebben's
> theorem is for one fixed member. The certificates below decide the presented
> groups of a sealed, hash-bound model; they do not reconcile that report.


*This is the prose companion of the arXiv note in `paper/`; the paper is the
authoritative text and carries the numbered theorems. Author: John Clyde
(VentiMath), with AI assistance disclosed in the provenance section.*

## 1. Introduction

For Wuebben's construction the theorem-critical step is the
fundamental-group computation. Wuebben (arXiv:2608.17267v1),
building on Lidman–Piccirillo (arXiv:2505.14387v1), proves that a specified
Lidman–Piccirillo piece V — a symplectic 4-manifold with the homology of
S²×D², built from a non-product genus-2 surface bundle over a once-punctured
torus by two Luttinger surgeries — is simply connected, and deduces three
theorems: (A) the symplectic double Z = V ∪_σ V is homeomorphic but not
diffeomorphic to S²×S²; (B) the quotient W = V/σ is homeomorphic to
Kawauchi's manifold B, and the pair (B, W) is distinguished by the smooth
sliceness of the figure-eight knot; (C) the Lidman–Piccirillo regluing Z'' is
a simply connected 4-manifold homeomorphic but not diffeomorphic to ℂP²#C̄P².
The proof's critical step is the triviality of the filled fundamental group
for the single specified manifold. The audit manifold uses the fixed
`(+, +)` relation sheet. The other three n=0 sign sheets are algebraic
robustness checks with no geometric identification in this note; all four
are certificate-checked as trivial. Four adjacent n=1 half-drift control
presentations — Ax replaced by the adjacent minimal representative
Ar⁻¹ = Ax(rx)⁻¹, Wuebben's n=1 member — also pass the identical
certification; they verify his one-step re-indexing and carry no logical
load for the fixed n=0 target.

This note reports a version-specific audit of the whole argument. The finite
certificate theorem is source-independent for its hash-bound presentations;
automated acceptance of the stored derivations assumes that at least one
checker conforms to the published specification. The audit-model theorem
identifies the fixed `(+, +)` presentation with an explicitly defined
manifold `V_aud`, making `V_aud`
simply connected.  The further comparison with Wuebben's intended fixed
member is conditional on Source Comparison Hypotheses D1--D14,
which separately state the marked-fiber, marked-bundle, peripheral/member,
coefficient, and smooth-surgery comparisons.  The bundle is rebuilt as a
simplicial complex, the surgery tori,
meridians, and framed longitudes are extracted combinatorially, and the
resulting filled presentations are proved trivial by complete confluent
rewriting, with every computation emitting a replayable proof certificate
checked by separately implemented Python and Ruby verifiers. Both verifiers were produced by OpenAI Codex
(GPT-5 family); independence means separate implementations, not cross-model
authorship. No independent human line-by-line audit of those checkers is
claimed. The deductions from simple connectivity to the three
theorems are then carried through as an explicit dependency chain (§7): twenty-five
external theorems are stated with their hypotheses, every hypothesis is
discharged by a named certificate or computation, every finite calculation
is executed and replayed by two checkers, and the chain ends in the three
theorems.

The conclusion, stated carefully: the four finite presentations are
certificate-checked as trivial and $\pi_1(V_{\mathrm{aud}})=1$; the
implication for Wuebben's fixed manifold is conditional on Source
Formalization D; and the three manifold conclusions are additionally
conditional on explicitly named external results. A reported contrary
computation of the same group is disclosed and not resolved; see the note
above and `runs/67`. The theorems are Wuebben's; this note claims only the
audit.

The intrinsic simple-connectivity proof uses the product-framed audit filling
and no symplectic input.  A separate theorem identifies the named product
push-offs with Lagrangian-framing classes; that theorem enters only the
conditional source bridge and downstream symplectic application.

## 2. The independent model

The audit-defined genus-2 fiber is realized as a regular neighborhood of its
five-chain of curves (five plumbed annular bands and two cone discs), with
the hyperelliptic-type involution realized simplicially: the fixed points,
the curve actions a↔e, b↔d, and the free half-rotation of the middle curve
are executable assertions, not assumptions. The bundle R is assembled from
simplicial mapping cylinders over a once-punctured-torus base; the two
surgery tori arise as induced subcomplexes. The assembled 4-complex passes
manifold checks down to the vertex-link level.

The identification with the audit's marked smooth bundle is by literal based
monodromy action — the based mapping classes of both monodromies are
certified as equalities of vertex paths, transported by proof-producing
Tietze chains whose recorded eliminations are replayed in-process by a
verifier separate from the generator (not sealed certificates) — and then by an explicit
marked mapping-cylinder clutching over the base graph: the relative
monodromy comparisons are exact on the marked collars, so the identification
is a constructed fiberwise homeomorphism into the audit-defined bundle rather than
an appeal to the classification of surface bundles. Everything the surgery
argument needs is transported through that map into the audit-defined smooth
manifold, where the symplectic arguments are performed; no smoothing of the
triangulation is ever chosen. The additional assertion that this marked
smooth bundle is Wuebben's intended bundle is the separate content of clauses
Source Comparison Hypotheses D1--D6 and D12--D14.

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

Filling the triangulation-derived complement presentation in the fixed audit
basis yields the `(+, +)` presentation of `V_aud`. Three additional n=0 sign
sheets and four adjacent half-drift systems are algebraic controls. All eight
have complete confluent rewriting systems in which every generator reduces
to the identity. Knuth–Bendix completion (KBMAG) is
used only as an untrusted certificate generator: the exported derivation DAGs
are verified by a standalone checker that re-validates every input-relator
axiom, inverse axiom, critical overlap, rewrite trace, and final
generator-to-identity rule. A second checker, separately implemented in Ruby
from the same specification,
re-verifies all retained derivation records (39,163 over the sealed presentation, 14,115 over the earlier four-generator export) without importing the
Python implementation, the compiler, GAP, or KBMAG; both accept. Both
filled-group checkers were produced by OpenAI Codex (GPT-5 family), so
“independent” means implementation-independent, not cross-model authorship
or statistically uncorrelated errors. A Claude Fable 5 session independently
reconstructed and replayed the 96-relator common-core computation behind
the last framing-scan case (§6, run 63) but did not author either checker.
Both checkers enforce the certificate inventory: no case verified twice, and
in the documented invocation exactly the eight fillings, one file per case
slug (run 65). All artifacts are bound by SHA-256 and replay.

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
signs — were then attacked at the raw-paper level: a quarantined extractor
reads only the paper's plain text, reconstructs the five-chain, involution,
ordered twists, surgery tori, whiskers, and direction words, and a separate
process compares its frozen output with the independently built model
certificates. Reversed-order and reversed-sign mutations are distinguished,
and no paper-to-model discrepancy was found: the previously identified
transcription residuals are closed relative to the paper's stated marked
data. The source itself was then audited directly rather than accepted
through the paper's restatement: a checker reading only the hash-pinned
main.tex and original vector Figure 1 of the immutable Lidman–Piccirillo
v1 arXiv source, importing no project module, confirms the ordered
five-chain a,b,c,d,e, the chain-reversing involution with c fixed with
orientation, the single consecutive crossings with all required
disjointness, and the two fixed points, in both the prose and the vector
layers. The one interpretation remaining at that boundary is the ordinary
convention that dashed arcs in a handle picture depict hidden projection
rather than extra crossings. The project-specific content of the paper's
Lemma 7.1 is certified in the same sense: all 36 candidate equivariant
ribbon rotations are enumerated, exactly four survive and all normalize to
one marked ribbon with two invariant free-half-turn boundary disks, so the
lemma's finite ribbon classification and its extension hypotheses are
machine-checked, with the Kerékjártó periodic-disk involution theorem the
remaining named input now that the source marked data are audited. Each of these checks
freezes its output as a certificate and logs its run transcript; all of it
replays directly from the repository. Beyond that boundary, what
remains is ordinary implementation trust — a checker and its review both
being wrong — not a declared unverified reading.

## 6. The framing lemma

Luttinger surgery is performed with respect to the Lagrangian framing; the
paper's Lemma 8.2 identifies it with the fibered framing used by the
combinatorial longitudes. The lemma's displayed Weinstein-chart, seam, and
constant-momentum algebra are checked by exact-rational Python programs, and
its inline analytic normalizations have been rebuilt constructively rather
than cited. The Moser
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
excluded. The scan comprises 96 shifted cases — twelve nonzero shifts, the
eight axis shifts of magnitude at most 2 and the four diagonal shifts
(±1,±1), a cross-and-diagonal sample rather than a full grid, across all
four sign pairs and both half-drift families — plus four zero-shift
controls that re-derive the paper's own n=0 fillings through the same
pipeline. The scan reports all 100 trivial, but only 22 are backed by
independently replayed derivation certificates; the other 78 retain GAP
session verdicts. No nontriviality witness was found at any stage. The
evidence is of two levels. The original pipeline,
which simplifies each presentation before completion, decided 82 at the
level of a GAP session (40 by Tietze collapse, 42 by complete confluent
rewriting) and exported no certificates from those runs. The 18 it left
open, every one involving a shift on the first torus, carry independently
replayed derivation-DAG certificates: 17 from confluent completion of the
unsimplified 97-relator presentation, whose redundant relators are what make
completion tractable, some only at raised equation limits (runs 58–62); and
the last from a certified reduction through the 96 relators it shares with
its neighboring presentation, whose common core is infinite cyclic with the
omitted relator reducing to its generator (run 63). The full verdict table
and search history are reported with the artifacts. Within the scanned
range, no framing error would have produced a nontrivial group; the scan
bears on the j=0 proof only if the independent framing argument of §6 first
fails.

## 7. From simple connectivity to the three theorems

The deductions from π₁(V) = 1 to Theorems A, B, C are carried through as an
explicit dependency chain, itself a machine artifact
(`verification/luttinger/downstream_chain.py`, run 64). Every item is one of
four kinds: an external theorem, stated with its hypotheses and source (25
items; Klug's Theorem 2, Hambleton's Theorem 5.1, Ho–Li's Theorem 1.1, and
Lidman–Piccirillo's Lemmas 9 and 10 quoted verbatim); a certificate of this
repository, bound by SHA-256 (3 items: π₁(V) = 1 through the proof manifest
and its two checker runs; the section's self-intersection Γ̂·Γ̂ = 0 from
run 28; the framing identification of runs 35, 43, 46, 47); a computed fact
executed by the script (15 items); or a deduction step from earlier items
(16 steps, ending in the three theorems). Both the Python chain builder and
the separately implemented Ruby checker were produced by Claude Fable 5;
independence here is implementation independence, not cross-model authorship.
The Ruby checker re-derives every computed fact from scratch, checks that every
citation resolves and that the graph is acyclic, verifies that each theorem
depends on the certified π₁(V) = 1, and checks every evidence digest. The
chain in prose, with the quoted statements and the proofs of the sixteen
steps, is `verification/notes/downstream_proof_chain_2026-08-28.md`; the
computational supplement gives the complete proposition-by-proposition chain.

In outline: π₁(V) = 1 with χ(V) = 2 gives H₂(V) = ℤ⟨F⟩, F·F = 0, and V spin
by Wu's formula; van Kampen gives π₁(Z) = π₁(Z'') = 1 (this is where the
stronger statement π₁(V) = 1, rather than π₁(Z) = 1, is needed, since the
regluing twists the amalgam). In Z, the certified Γ̂·Γ̂ = 0 with F·F = 0 and
F·Γ̂ = 1 makes (F, Γ̂) a basis of the hyperbolic form by the index formula,
so Z is spin because its form is even, and Freedman gives Z ≅ S²×S²
topologically. Z carries the Thurston-type form of the closed bundle
R ∪_σ R, with the surgery tori Lagrangian and the surgeries the certified
Luttinger surgeries; R ∪_σ R is aspherical, hence minimal with κ ≠ −∞,
Ho–Li carries κ ≠ −∞ through the surgeries, and a diffeomorphism to
S²×S² — made orientation-preserving by a reflection of one factor — would
pull back a form with κ = −∞, contradicting Li's independence of κ from
the form. That is Theorem A. For Theorem B, the covering sequence gives
π₁(W) = ℤ/2, χ(W) = 2 gives b₂(W) = 0, Lidman–Piccirillo's Lemma 7 gives W
spin, and Hambleton–Kreck gives W ≅ B; the symplectic k-fold covers of F and
Γ̂ with the symplectic Thom theorem show no nonzero square-zero class of Z
contains a torus; and a slice disk for 4₁ in W is either characteristic in
W − B⁴ — where Klug's theorem with σ = [D]² = 0 forces Arf(4₁) = 0, but
Δ(−1) = −5 ≡ 3 mod 8 gives Arf(4₁) = 1 — or caps to a square-zero torus
nonzero mod 2 that lifts to Z, contradicting the previous step. For Theorem
C, Novikov additivity and the odd square of Γ'' give the form
⟨1⟩ ⊕ ⟨−1⟩ by an explicit change of basis valid for every parity witness,
Freedman gives Z'' ≅ ℂP²#C̄P², and Lidman–Piccirillo's Lemmas 9 and 10 give a
nonvanishing mixed invariant along the square-zero line of F, whereas both
square-zero lines of ℂP²#C̄P² split over S²×S¹ with vanishing mixed
invariants.

Three points where the chain's route differs from the paper's: H₁(V) = 0 is
taken from the certificate rather than from the surgery relations; the form
of Z is identified from the certified Γ̂·Γ̂ = 0, so Z is spin by evenness and
the spin quotient is not needed for Theorem A; and the sliceness dichotomy
is taken over ℤ/2 throughout, which is what makes the null-homologous case
exactly Klug's characteristic case and the lifted torus nonzero integrally.

## 8. Trust boundary

The source comparison is conditional on Source Comparison Hypotheses D1--D14, whose
fourteen clauses are not treated as standard theorems or machine
certificates. They separate marked-fiber, marked-bundle, peripheral/member,
coefficient, and smooth-surgery fidelity and bind each reading to a target
location. Independent extraction and mutation controls are evidence for the
readings, not proofs of what another author's prose and figures intend.

The named standard inputs behind the audit-model theorem, applied with
checked hypotheses and cited proofs, are elementary ribbon thickening and
bistellar traces; the classification of
surfaces; the collapsible-3-ball and cyclic-knot-unknot criteria behind the
local-flatness certificates; simplicial fundamental-group presentation and
Tietze theory; the Kerékjártó periodic-disk involution theorem behind
Lemma 7.1's disk extension; and ADK03 as corroboration of the framing
identification.

The named inputs behind the downstream chain are its twenty-five external
theorems, each stated in the chain with its hypotheses: Seifert–van Kampen;
the covering exact sequence; Poincaré–Lefschetz duality with universal
coefficients and the Euler characteristic; the lattice index formula; Wu's
formula; Novikov additivity; asphericity of bundles; the adjunction
formula; Palais's ball isotopy; Freedman's classification; the
Hambleton–Kreck classification (Hambleton 2008, Theorem 5.1); Thurston's
symplectic form on surface bundles; Luttinger surgery (Luttinger, ADK);
symplectic Kodaira dimension (Li 2006) and Ho–Li's invariance theorem; the
symplectic Thom theorem (Ozsváth–Szabó 2000) and the symplectic cover
construction (after Stipsicz–Szabó); Klug's relative Rochlin theorem and
Levine's Arf criterion; the slice-disk/0-trace embedding; Lidman–Piccirillo's
constructions (their Lemmas 4, 6, 7, the regluing of their Theorem 2) and
Floer lemmas (their Lemmas 9 and 10, with Ozsváth–Szabó 2004, 2006 behind
them); and Kawauchi's manifold B. This note does not
reprove them.  The source-reading evidence is recorded separately from these
general mathematical inputs.

Formerly listed inputs that are no longer dependencies inside the audit
model: surface-bundle
classification (replaced by the explicit clutching of §2); four-dimensional
smoothing and intersection naturality (the smooth arguments run entirely in
the audit-defined smooth manifold, and the section's square is computed
there from transported disjoint homologous cycles); derived-regular-
neighborhood theory (the tubular boundary is constructed — see §3); and
Weinstein germ uniqueness (chart independence is proved between the audit's
verified charts — see §6; ADK03 remains corroboration). Source Comparison
Hypotheses D1--D14 remain the separate source-comparison boundary.

## 9. Provenance and method

The verification was AI-assisted throughout (Anthropic Claude Fable 5 and
Opus 5; OpenAI Codex), under human direction and with commit-level model
provenance. Cross-model review was adversarial by design, and several
decisive corrections in the record came from one model refuting the
other's assessment. Mathematical responsibility rests with the human author.
Every asserted computation ships with a replayable certificate. No claim in
this note depends on accepting a model's prose as evidence, but automated
acceptance of the certificates does depend on checker conformance to the
published specification; no independent human line-by-line code audit is
claimed.

## 10. Data availability

The exact target is Wuebben arXiv:2608.17267v1 (18 August 2026), PDF SHA-256
`16a6cef4998699f76ee508e062f8192cf80eeb478b7e077bfa35ccc25350186a`;
`TARGET.md` records this and the Lidman–Piccirillo v1 digest. All code,
certificates, run logs, and the provenance ledger:
https://github.com/VentiMath/exotic-s2xs2-verification, pinned in the
tagged release v2.0.1 (the paper's Data and reproducibility section records
the commit and the SHA-256 of the proof manifest and of the downstream-chain
certificate). The v2.1.0 manuscript and this companion remain release
candidates until the matching tag and archival DOI are created. The paper's
own code: https://github.com/bwuebben/exotic-s2xs2.
