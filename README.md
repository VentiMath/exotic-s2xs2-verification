# Machine verification: the fundamental-group computation in Wuebben's exotic S²×S²

This repository documents an independent, machine-driven verification of the
fundamental-group step in

> B. J. Wuebben, *An exotic S²×S² and an exotic ℂP²#C̄P²*, arXiv:2608.17267,

which builds on Lidman–Piccirillo, arXiv:2505.14387. The author's own code and
certificates are at [bwuebben/exotic-s2xs2](https://github.com/bwuebben/exotic-s2xs2);
nothing here is derived from that repository except where explicitly cited.
This project rebuilt the geometry from scratch and checked the paper against
the rebuild.

**What this repository is:** a verification, by people and machines who are
not the paper's author, of the historically most failure-prone step in claimed
small exotic 4-manifolds — the fundamental-group computation — together with a
hypothesis audit of everything downstream of it.

**What this repository is not:** a claim on the theorem, which is Wuebben's,
or a formal proof of the entire paper.

## What is verified, from an independent triangulation

Everything below is computed from a triangulated model built independently of
the paper's coordinates, with proof-producing certificates that replay.

* **The bundle.** The genus-2 fiber, its involution with the paper's fixed
  points and curve actions, and the full surface bundle R are realized
  simplicially (f-vector [9156, 116714, 356728, 403152, 153984]) and matched
  to the paper's marked bundle by literal based monodromy action — not by
  fingerprints. The based monodromy certificate replays 17,839 elementary
  Tietze steps; an independently built second triangulation replays 34,735.
  The identification with the paper's bundle is realized by an explicit
  marked mapping-cylinder clutching over the base graph, with the relative
  monodromy comparisons checked exactly on the marked collars — the
  classification of surface bundles is no longer invoked.
* **The peripheral data.** Based meridians and longitudes for both surgery
  tori are traced as literal simplicial loops with the paper's own whiskers.
  The paper's sign-correction package (its §7.4 fix) is reproduced and
  certified, and a combinatorial sweep resolves the basing double-count
  question in the direction the paper needs. Both surgery tori are certified
  locally flat at all 1,776 of their simplex links, and the boundary the
  peripheral curves live on is an explicit half-weight normal block model
  with a global PL identification of the computed frontier: every extracted
  dual meridian is checked to be a literal normal-circle fiber, with no
  regular-neighborhood theorem invoked.
* **The eight filled groups.** Filling the triangulation-derived complement
  presentation with the certified peripheral pairs proves all four n=0 sign
  pairs, and the four adjacent half-drift systems, trivial by complete
  confluent rewriting. KBMAG is used only as an untrusted certificate
  generator: a small independent checker verifies every axiom, overlap,
  rewrite trace, and final generator-to-identity rule in the exported
  derivation DAGs, and a second checker, written independently in Ruby,
  re-verifies all 14,115 retained records without importing the Python
  implementation. All artifacts are hash-bound and replay.
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
  constant-momentum algebra of the paper's Lemma 8.2 are machine-checked, and
  its inline normalizations are rebuilt constructively: the Moser flow is the
  explicit monotone inverse of a cumulative coordinate (no ODE citation), the
  equivariant field is defined directly on the double cover with certified
  deck invariance (no covering-lift citation), the covering hypotheses are
  certified on the simplicial collar, and chart independence is argued twice
  in-project with ADK03 §2.1 / Proposition 2.2 as corroboration. A
  self-contained referee packet states the lemma's proof with each identity
  cross-referenced to the executable check.
* **The downstream chain.** The deductions after simple connectivity —
  Freedman applications, the Hambleton–Kreck classification data, the
  intersection-form calculations, minimality and symplectic Kodaira
  dimension, the square-zero torus lift, and the reuse of the
  Lidman–Piccirillo Floer argument — pass a hypothesis audit with no gap
  found; the elementary lattice and adjunction calculations are executable.

## What is not claimed

The remaining proof dependence is concentrated in named classical inputs,
applied with hypotheses that have been checked but with proofs that are
cited, not mechanized: the elementary ribbon-thickening and bistellar-trace
interpretations that read the paper's figures into complexes; the
classification of surfaces; the collapsible-3-ball and cyclic-knot-unknot
criteria behind the local-flatness certificates; simplicial
fundamental-group presentation and Tietze theory; the Kerékjártó
periodic-disk involution theorem behind Lemma 7.1's disk extension; and the
quoted Freedman–Hambleton–Kreck, symplectic Kodaira-dimension, symplectic
Thom, Rokhlin/Arf, and Heegaard Floer theorems. Surface-bundle classification,
four-dimensional smoothing, intersection-form naturality, and
derived-regular-neighborhood theory are no longer dependencies: the bundle
identification is an explicit clutching, the smooth and symplectic arguments
run entirely in the paper's already-smooth manifold, and the tubular
boundary is constructed rather than cited. Weinstein germ uniqueness is
corroborating rather than necessary — chart independence is proved
in-project between the paper's verified charts. If the framing identification (Lemma 8.2)
failed by j meridians, the machine certificates would remain correct for
their literal product-framed presentations but would no longer identify those
presentations with the paper's Lagrangian surgeries; simple connectivity, the
homeomorphism conclusions, and the exoticness argument for the claimed
manifolds would then be unproved. A completed slope-robustness scan
quantifies which discrepancies j are independently excluded: of 100
meridian-shifted refillings across both half-drift families, 82 are
certified trivial, 18 remain undecided (all perfect, all resistant to
quotient and coset-enumeration attack), and none is nontrivial. Every shift
touching only the second surgery torus is certified trivial; only shifts on
the first torus produce undecided counterfactual groups. Those 18 holdouts
are not evidence of a framing error, and they have no bearing on the j=0
proof unless the independent framing argument first fails.

The accurate one-sentence status: **the proof appears complete relative to
explicitly named standard topology theorems, with no known project-specific
gap.** That is a statement about verification depth, not a substitute for
review by symplectic and 4-manifold topologists — which this repository is
built to make cheap.

## Provenance

This verification was AI-assisted throughout, by Anthropic Claude models
(Fable 5, Opus 5) and OpenAI Codex, working under human direction. The
project keeps a commit-level provenance ledger recording which model produced
which work (see `PROVENANCE.md`); mathematical responsibility rests with the
human author. Certificates are designed to be checked, not trusted: every
asserted computation ships with a replayable artifact.

## Contents

* `docs/verification-note.md` — the verification note.
* `paper/` — the LaTeX source of the arXiv verification note.
* `verification/` — the working repository at its imported commit: the engine
  and certificates under `verification/luttinger/` (derivation-DAG
  certificates in `proof_certificates/`, rewriting systems in `direct_rws/`
  and `j_rws/`), the run transcripts under `verification/runs/`,
  referee-packet notes under `verification/notes/`, `STATUS.md` (the honest
  snapshot of what is and is not certified), `PROVENANCE.md` (the
  commit-level model ledger), and `IMPORT.md` (what was imported, what was
  removed, and why).

## Contact

John Clyde — verification@ventimath.org — [VentiMath](https://ventimath.org)

## License

MIT for everything in this repository. The paper and its contents are
copyright B. J. Wuebben; this repository does not redistribute them.
