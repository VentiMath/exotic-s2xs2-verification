# An exotic S²×S² from a certificate-checked surface-bundle surgery manifold

This repository contains the manuscript, supplement, and proof artifacts for
an explicit marked surface-bundle surgery manifold `V_aud` and its double.
Its primary, source-independent result (Theorem A′) is

> `Z_aud = V_aud ∪_{σ_aud} V_aud` is a closed symplectic 4-manifold that is
> homeomorphic but not diffeomorphic to `S²×S²`,

resting on

> `pi_1(V_aud) = 1`, with `chi(V_aud)=2`, `H_2(V_aud)=Z`, spinness, a
> primitive square-zero genus-two fiber, a relative section, and a symplectic
> structure,

an intrinsic boundary involution `σ_aud`, the descent of the symplectic form
to the double, and published theorems (Freedman; Auroux–Donaldson–Katzarkov;
Ho–Li; Li) whose hypotheses are discharged in the text.

The construction was motivated by

> B. J. Wuebben, *An exotic S²×S² and an exotic ℂP²#C̄P²*, arXiv:2608.17267v1,

which builds on Lidman–Piccirillo, arXiv:2505.14387v1.  The comparison
`V_aud ≅ V` is not a theorem of the manuscript and no theorem depends on it.
The supplement preserves an open fourteen-clause attribution checklist for
that comparison and the historical transfer chain.  Wuebben's own code and certificates are at
[bwuebben/exotic-s2xs2](https://github.com/bwuebben/exotic-s2xs2); nothing
here is derived from that repository except where explicitly cited.

**What this repository is:** a version-specific, certificate-checked
computer-assisted topology project.  Its finite theorem is that four
explicit, manifest-bound presentations are
trivial under the published certificate specification; automated acceptance
of the stored derivations assumes that at least one checker conforms to that
specification.  A separate audit-model theorem identifies the fixed
`(+, +)` presentation with the explicitly defined manifold `V_aud`, which is
therefore simply connected and has the intrinsic topology listed above; the
other three sign sheets are algebraic robustness checks.  The main paper then
proves Theorem A′ about the double `Z_aud`; it does not assert anything about
Wuebben's own manifolds.

The proof that `pi_1(V_aud)=1` uses only the product-framed filling.  The
separate product-to-Lagrangian framing theorem is not an input to simple
connectivity; it proves the source-independent symplecticity of `V_aud` and
would also be relevant to any future source comparison.

Legacy machine artifacts retain the identifier `A_source_formalization_D`
and the earlier phrase “Source Formalization D.” In v2.1 these names denote
exactly the conjunction of the open source-comparison checklist D1--D14; the rename
does not change the frozen dependency node or its digest.

The immutable v2.4.0 verification snapshot is archived at
[doi:10.5281/zenodo.22254457](https://doi.org/10.5281/zenodo.22254457);
[doi:10.5281/zenodo.22169753](https://doi.org/10.5281/zenodo.22169753) is the
concept DOI for the newest archived version.

**v2.4.0 release.** The newest public immutable release is:
[releases/tag/v2.4.0](https://github.com/VentiMath/exotic-s2xs2-verification/releases/tag/v2.4.0),
archived under version DOI
[10.5281/zenodo.22254457](https://doi.org/10.5281/zenodo.22254457). Run
`python3 paper/check_release_sync.py` to verify the release's hashes, counts,
terminology, bound manifests, and the pinned `verification/` tree object; the
gate rebuilds the deterministic arXiv archive itself, so it runs from a clean
clone. The release URL and both DOIs resolve from a logged-out browser.
The v2.4.0 proof manifest has SHA-256
`e8118b489a1b365c002a1931839fb419ab0f456aaecf724f2acf979612c9b5b9` and
binds 48 files, including the revised checkers and the audit-manifold
invariant checker.  The `verification/` tree object is
`650069254d921c218c6fa50fc359c0f128ef7ddb`, the existence-chain certificate has SHA-256
`197c9944ab5fcbb95a3ab767f786ab9bbc0ab002bdea4d64723dfa870fb78357`, and the attribution-chain certificate has SHA-256
`73257b9ea0883255bb15c70f77f551526eec1714a866ab9e645cfe374528e8ca`.

**What this repository is not:** a verification or refutation of Wuebben's
fixed manifold; a proof of his Theorems B and C (the quotient and the
regluing, which need a free boundary involution and are outside the
existence route); or a substitute for independent human review of one
certificate checker, the PL conversion, the symplectic framing argument, and
the descent of the form to the double.

**Bounded external-review packets.** The remaining reviews are specified in
[`verification/luttinger/CHECKER_AUDIT_GUIDE.md`](verification/luttinger/CHECKER_AUDIT_GUIDE.md)
and
[`verification/notes/EXTERNAL_REVIEW_GUIDE.md`](verification/notes/EXTERNAL_REVIEW_GUIDE.md).
The first maps every certificate-specification obligation to both checker
implementations and supplies adversarial replay commands. The second separates
the PL/peripheral review needed for simple connectivity from the symplectic
review needed for the framing theorem. Neither file claims that an external
review has occurred.

**Known unreconciled external computation.** Wuebben's repository has stated,
since its first visible commit and continuously since, that Lidman and
Piccirillo report a computation of π₁(V) that disagrees with his, and that the
disagreement is unresolved. This must be read alongside everything below.
What the public record contains: their published v1 never asserts π₁(V) ≠ 1 —
it proves H₁(V) = 0 and that π₁(V) is normally generated by π₁(F) — and no
relation sheet, generator dictionary, or nontriviality witness for the contrary
computation is public anywhere we can find. Their v1 source also carries an
explicit footnote declining to fix the surgery parametrization ("since we
parametrized the surgery tori somewhat arbitrarily, V is not well-defined per
se"), while Wuebben's theorem is for one fixed member V′₀,₀. So the two
reported outcomes are not known to concern the same manifold — and not known
to concern different ones either. The certificates in this repository decide
the presented groups of a sealed, hash-bound model; **they do not reconcile
that report, and nothing here should be read as claiming they do.** This
project recorded the report on 2026-08-23 and did not carry it into its
status file, ledger, and manuscript until 2026-08-29; that omission is
documented in [`verification/runs/67-r3-complement-and-lp-disagreement.txt`](verification/runs/67-r3-complement-and-lp-disagreement.txt)
and [`verification/notes/lp_disagreement_reconciliation_2026-08-29.md`](verification/notes/lp_disagreement_reconciliation_2026-08-29.md).

## What is verified, from an independent triangulation

Everything below is computed from a triangulated model built independently of
the paper's coordinates, with proof-producing certificates that replay.

* **The bundle.** The genus-2 fiber, its involution, marked points and curve
  actions, and the full audit bundle `R_aud` are realized simplicially
  (f-vector [9156, 116714, 356728, 403152, 153984]) and matched to its marked
  smooth definition by literal based monodromy action — not by fingerprints.
  The based monodromy certificate replays 17,839 elementary
  Tietze steps; an independently built second triangulation replays 34,735.
  This internal identification is realized by an explicit
  marked mapping-cylinder clutching over the base graph, with the relative
  monodromy comparisons checked exactly on the marked collars — the
  classification of surface bundles is no longer invoked. Comparing this
  marked object with Wuebben's bundle is the separate open comparison in
  clauses D1--D6.
* **The peripheral data.** Based meridians and longitudes for both surgery
  tori are traced as literal simplicial loops with the audit's named whiskers.
  The alpha coordinate identity `lb_a_y1 = A x` is additionally certified in
  the sealed complement itself by a 2,506-record ancestry DAG, independently
  replayed in Python and Ruby (run 68); the beta identity
  `lb_b_s2 = (r^-1 M r) B` has an analogous 1,540-record certificate (run 69).
  No filling relation is used in either proof.
  The paper's sign-correction package (its §8.3 corrected relations and §8.5
  push-off basing correction) is reproduced and
  certified, and a combinatorial sweep resolves the basing double-count
  question in the direction the paper needs. Both surgery tori are certified
  locally flat at all 1,776 of their simplex links, and the boundary the
  peripheral curves live on is an explicit half-weight normal block model
  with a global PL identification of the computed frontier: every extracted
  dual meridian is checked to be a literal normal-circle fiber, with no
  regular-neighborhood theorem invoked.
* **The eight filled groups.** The audit manifold uses the fixed n=0 `(+, +)`
  filling. The other three n=0 sign pairs are algebraic relation sheets; no
  geometric identification is claimed for them. Filling the
  triangulation-derived complement presentation proves the fixed sheet,
  those three robustness sheets, and four adjacent half-drift controls
  trivial by complete
  confluent rewriting. KBMAG is used only as an untrusted certificate
  generator: separate Python and Ruby checkers produced by OpenAI Codex
  (GPT-5 family) verify every axiom, overlap, rewrite trace, and final
  generator-to-identity rule in the exported derivation DAGs. They share no
  implementation code but do share the certificate specification and model
  family: independence here means implementation independence, not cross-model
  authorship or statistically uncorrelated errors. A Claude Fable 5 session
  independently reconstructed and replayed the 96-relator common-core
  computation behind the last framing-scan case (run 63); it did not author
  either checker. No independent human line-by-line checker
  audit is claimed. Both checkers enforce the certificate inventory — no
  case verified twice, and in the documented invocation exactly the eight
  fillings, one file per case slug (run 65). All artifacts are hash-bound
  and replay.
* **Intrinsic audit-manifold invariants.** From simple connectivity,
  connected boundary, Euler characteristic `2`, a surviving fiber, and the
  fixed-point section, the manuscript proves
  `H_0(V_aud)=H_2(V_aud)=Z`, all other integral homology groups zero,
  spinness, and a primitive square-zero genus-two generator.  The framing
  theorem then identifies the two fillings as Luttinger surgeries and gives
  a symplectic structure preserving a disjoint fiber.  The finite arithmetic
  and the slope-family negative control replay with
  `python3 verification/luttinger/audit_manifold_invariants.py`.
* **Redundant second routes.** A translation mistake would have to survive
  several structurally different implementations: an independent peripheral
  extractor, an alternative bundle triangulation, the second based-monodromy
  certificate, a simplex-level verifier of all 128 PL flip traces, and a
  58-vertex marked-fiber realization matched equivariantly to the primary
  86-vertex model. What redundancy cannot exclude — a shared misreading of
  the paper's conventions — is attacked by a bound interpretation
  dictionary: every convention read from the paper carries its
  discriminating certified witness, and the central entries are
  cross-checked, by parsing and never executing, against the author's own
  committed scripts, which define the same actions, corrections, and sign
  conjugators. The three entries run 53 could pin only by transcription —
  the ordered beta twists, the five-chain ribbon labels, and the local twist
  signs — were then attacked at the raw-paper level: a quarantined
  extractor reads only the paper's text, reconstructs the five-chain,
  involution, ordered twists, tori, whiskers, and direction words, and a
  separate process compares its frozen output with the independently built
  model certificates. Reversed-order and reversed-sign mutations are
  distinguished, and no paper-to-model discrepancy was found: the
  transcription residuals are closed relative to the paper's stated marked
  data. The original Lidman–Piccirillo v1 source was then audited directly
  — hash-pinned main.tex and vector Figure 1, no project module imported —
  confirming the ordered five-chain, the chain-reversing involution with c
  fixed with orientation, the consecutive crossings and disjointness, and
  the two fixed points, in both prose and vector layers; the one remaining
  interpretation there is the ordinary dashed-arc hidden-projection
  convention. Lemma 7.1's finite ribbon classification and extension
  hypotheses are certified — all 36 candidate equivariant ribbon rotations
  enumerated, exactly four surviving, all normalizing to one marked ribbon
  — with the classical Kerékjártó periodic-disk theorem the remaining
  named input.
* **The framing lemma's analysis.** The displayed Weinstein-chart, seam, and
  constant-momentum algebra of the paper's Lemma 8.2 are checked by
  exact-rational Python programs, and
  its inline normalizations are rebuilt constructively: the Moser flow is the
  explicit monotone inverse of a cumulative coordinate (no ODE citation), the
  equivariant field is defined directly on the double cover with certified
  deck invariance (no covering-lift citation), the covering hypotheses are
  certified on the simplicial collar, and chart independence is argued twice
  in-project with ADK03 §2.1 / Proposition 2.2 as corroboration. A
  self-contained referee packet states the lemma's proof with each identity
  cross-referenced to the executable check.
* **The existence chain.** `verification/luttinger/downstream_chain.py`
  (run 74) carries every implication from certified π₁(V_aud)=1 to
  Theorem A′ — `Z_aud = V_aud ∪_{σ_aud} V_aud` is a closed symplectic
  4-manifold homeomorphic but not diffeomorphic to `S²×S²` — as an explicit
  item: 9 external theorems, 4 hash-bound certificates, 3 hash-bound written
  proofs (`paper/sigma_aud.tex`, `paper/symplectic_double.tex`, the split
  form of `paper/main.tex`), 5 computed facts, 7 deduction steps, and no
  assumption. Both its checkers fail if an assumption is added, if any item
  names Lidman–Piccirillo, Wuebben, or D1--D14, or if the conclusion stops
  resting on the certified π₁, the certified σ_aud, and the descent lemma.
* **The historical transfer chain (attribution only).** The conditional
  deductions from simple connectivity of Wuebben's `V` to the three proposed
  theorems are preserved unchanged as an explicit dependency chain
  (`verification/luttinger/attribution/wuebben_transfer_chain.py`, run 64): Source
  Formalization D as one explicit comparison assumption, 25 external
  theorems stated with their hypotheses and sources (Klug's relative
  Rochlin theorem, Hambleton's classification statement, Ho–Li's Kodaira
  invariance, and Lidman–Piccirillo's Floer lemmas quoted verbatim), 3
  hash-bound certificates of this repository (π₁(V_aud)=1, the section's
  self-intersection Γ̂·Γ̂=0, the framing identification), 15 computed
  facts (Euler characteristics and Betti numbers, the hyperbolic and odd
  intersection-form bases, cover genera, adjunction, Arf(4₁)=1 two ways,
  the instantiated Klug formula, the Hambleton–Kreck invariant tuple), and
  17 deduction steps ending in Theorems A, B, and C. The first step is the
  source-comparison sufficiency argument from V_aud to Wuebben's V; no certificate itself is
  described as proving that source comparison. Both the Python chain
  builder and the separately implemented Ruby checker were produced by Claude
  Fable 5; this is implementation independence, not cross-model authorship.
  The Ruby checker re-derives every computed fact from scratch, checks the
  graph is acyclic and that each theorem depends on both the certified
  π₁(V_aud)=1 and the open source-comparison checklist D1--D14, and verifies every evidence digest. The dependency ledger
  (`proof_ledger.py`) binds the whole verification — 33 named external
  theorems, 37 machine certificates, 12 geometric arguments, one explicit
  source-assumption node, and 21 derived claims — with every evidence file
  hashed. The first four counts describe the compact downstream chain; the
  larger figures describe the project-wide ledger, so they are not competing
  tallies. The chain is
  written out in prose in
  `verification/notes/downstream_proof_chain_2026-08-28.md` and in the
  mathematical and computational supplement.

## What is not claimed

The remaining proof dependence has two different kinds.  First, Source
Comparison Hypotheses D1--D14 comprise textual, diagrammatic, and
smooth/framing assumptions about marked-fiber, marked-bundle,
peripheral/member, coefficient, and smooth-surgery fidelity.
Their independent extractors and mutation controls are evidence for exact
mathematical interpretations, not certificates that a diagram denotes the
audit object.
Second, named classical inputs are applied with checked hypotheses but cited
rather than mechanized: elementary ribbon thickening and bistellar traces; the
classification of surfaces; the collapsible-3-ball and cyclic-knot-unknot
criteria behind the local-flatness certificates; simplicial
fundamental-group presentation and Tietze theory; the Kerékjártó
periodic-disk involution theorem behind Lemma 7.1's disk extension; and the
twenty-five external theorems of the downstream chain — Freedman's and the
Hambleton–Kreck classifications, Thurston's symplectic form on surface
bundles, Luttinger surgery, symplectic Kodaira dimension (Li) and its
invariance under Luttinger surgery (Ho–Li), the symplectic Thom theorem and
the symplectic cover construction, Klug's relative Rochlin theorem with
Levine's Arf criterion, Palais's ball isotopy, Kawauchi's manifold B, and
Lidman–Piccirillo's constructions and Floer lemmas (with the Ozsváth–Szabó
theorems behind them), together with the elementary algebraic topology the
chain names (van Kampen, the covering sequence, duality and universal
coefficients, the lattice index formula, Wu's formula, Novikov additivity,
asphericity, adjunction). Inside the audit-defined object,
surface-bundle classification, four-dimensional smoothing, intersection-form naturality, and
derived-regular-neighborhood theory are no longer dependencies: the bundle
identification is an explicit clutching, the smooth and symplectic arguments
run entirely in the audit-defined smooth manifold, and the tubular
boundary is constructed rather than cited. Weinstein germ uniqueness is
corroborating rather than necessary — chart independence is proved
in-project between the audit's verified charts. The comparison of those
objects and charts with Wuebben's ones remains the open source-comparison checklist D1--D14. If the
framing identification (Lemma 8.2)
failed by j meridians, the machine certificates would remain correct for
their literal product-framed presentations but would no longer identify those
presentations with the paper's Lagrangian surgeries; simple connectivity, the
homeomorphism conclusions, and the exoticness argument for the claimed
manifolds would then be unproved. A completed slope-robustness scan
quantifies which discrepancies j are independently excluded: 96
meridian-shifted refillings (twelve nonzero shifts, a cross-and-diagonal
sample rather than a full grid, across four sign pairs and both half-drift
families) plus four zero-shift controls. The completed scan reports all 100
trivial and none nontrivial, but 22 are certificate-backed while the other 78
retain only GAP session verdicts. The original pipeline decided 82 at the
level of a GAP session; the 18 it left open, every one a shift on the first
surgery torus, carry
independently replayed derivation-DAG certificates (runs 58–63), the last
by a certified reduction through the 96 relators it shares with its
neighbor. Within the scanned range, no framing error would have produced a
nontrivial group; the scan bears on the j=0 proof only if the independent
framing argument first fails.

The accurate one-sentence status: **the finite presentations are certified
trivial and the audit-defined `V_aud` is simply connected; the implication for
Wuebben's fixed manifold is conditional on the open source-comparison checklist D1--D14; and the three manifold
conclusions are additionally conditional on named external results** — with the reported contrary
computation of π₁(V) disclosed above and not resolved. That is a statement
about verification depth, not a substitute for review by symplectic and
4-manifold topologists — which this repository is built to make cheaper.

## Provenance

This verification was AI-assisted throughout, by Anthropic Claude models
(Fable 5, Opus 5) and OpenAI Codex, working under human direction. The
project keeps a commit-level provenance ledger recording which model produced
which work (see `PROVENANCE.md`); mathematical responsibility rests with the
human author. Certificates are designed to be checked, not trusted: every
asserted computation ships with a replayable artifact.

## Contents

* `paper/` — the LaTeX source of the main audit and its computational
  supplement.
* `TARGET.md` — immutable target-paper versions and SHA-256 digests.
* `verification/` — the working repository at its imported commit: the engine
  and certificates under `verification/luttinger/` (derivation-DAG
  certificates in `proof_certificates/`, rewriting systems in `direct_rws/`,
  the downstream proof chain in `downstream_chain.py` with
  its certificate and Ruby checker), the run transcripts under
  `verification/runs/`,
  referee-packet notes under `verification/notes/`, `STATUS.md` (current
  status, evidence, and limitations), and `IMPORT.md` (what was imported, what was
  removed, and why).

## Contact

John Clyde — verification@ventimath.org — [VentiMath](https://ventimath.org)

## License

Everything authored for this repository, including the verification note, is
licensed under the MIT License. Wuebben's target paper remains copyright its
author and is linked, not redistributed.
