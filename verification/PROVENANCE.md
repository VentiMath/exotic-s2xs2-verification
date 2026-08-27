# Provenance: which model produced which work

John is auditing this work by model. The rule is simple and the boundary is a
commit, not a date or a claim a model makes about itself.

## The boundary

    6587b7e  Machine derivation of the Luttinger surgery data for Wuebben's
             bundle R
             ^^^ everything in this commit and earlier: CLAUDE FABLE 5

Everything committed **after** 6587b7e is **Claude Opus 5**, unless a commit
says otherwise in its body.

## What Fable 5 produced (all of 6587b7e)

The engine extensions and the run: `fiber.py`, `layers.py`,
`monodromy_check.py`, `bundle.py`, `fast_tietze.py`, `r_run.py`, the generated
GAP certificates (`r_cert.g`, `r_diag*.g`, `r_scan*.g`, `r_ace*.g`), all nine
files in `runs/`, and `STATUS.md`. The inherited material — `luttinger.tar.gz`,
`complex.py`, `pi1.py`, `complement.py`, `tietze.py`, `t4_run.py`,
`bk_t4_test.py`, `author_scripts/`, `paper_data.md`, `walkthrough.txt`,
`DESIGN.md`, `README.md` — came from a prior session and the paper author, not
from Fable.

Read `STATUS.md` for what that work does and does not establish. The short
version: the bundle, the monodromies, and the relation sheet are certified; the
theorem's coset enumeration is **not** closed; two of the certificate's checks
use a fingerprint that turns out not to discriminate.

## One honest caveat about the boundary

The `/model` switch to Opus 5 reported that it saved Opus **as the default for
new sessions**. The session that wrote this file still carried a Fable 5 system
prompt, so it is genuinely ambiguous whether this file itself was written by
Fable or Opus.

This does not contaminate the record, because this file and any commit that
only touches it contain **no mathematical work** — only bookkeeping. Every
mathematical artifact is either inside 6587b7e (Fable) or in a later commit
(Opus). If precision about this one file matters later, treat it as Fable.

## How to maintain this

* When a model other than Opus 5 does substantive work, say so in that
  commit's body — a plain sentence, not a trailer. This repo keeps commit
  messages free of assistant attribution trailers.
* Add a line to the log below whenever the acting model changes.
* Do not retroactively relabel. If something was built by Fable and is later
  fixed by Opus, the fix is Opus work and the original stays Fable work.

## Log

| Boundary | Model | Scope |
|---|---|---|
| through 6587b7e | Claude Fable 5 | initial build; see STATUS.md |
| 4bd40fa | Claude Opus 5 | provenance bookkeeping only |
| 661e810 | OpenAI Codex (GPT-5 family) | oriented beta and alpha-s sweeps; proof-producing Tietze replay; explicit p-whiskered paper generators and based monodromy; local N-meridian identification; M1--M3; explicit y_1/y_2/s_2 peripheral pairs; presentation exports and group attacks; complete KBMAG triviality certificates for all eight directly traced fillings; peripheral slope and conjugacy bridge; hashed rewriting-system export and all-eight replay; global marked-bundle correspondence and framing-chart audit; path-level drilled-fiber basis and R3 transport; downstream classification, exoticness, slicing, and Floer-hypothesis audit; explicit proof-dependency ledger and risk register (runs/10--25); live-GitHub acornlib capability audit and DeepSeek certificate-framework specification |
| after 661e810 | Claude Fable 5 | model switched back to Fable (2026-08-24); the "after 6587b7e is Opus" rule above is superseded by this log |
| after dad49cf | OpenAI Codex (GPT-5 family) | standalone expert-facing peripheral identification lemma; proof-ledger integration; explicit separation of the direct `n=0` pairs from obsolete and inconclusive coordinate diagnostics |
| after 8f9046b | Claude Fable 5 | bookkeeping only: STATUS.md de-staled (superseded provenance rule removed; completed downstream audit recorded in the conclusion; next-steps list rewritten around the Lemma 8.2 residue and its blast radius) |
| ca32aa1 | OpenAI Codex (GPT-5 family) | independent 58-vertex marked-fiber realization and equivariant match to the 86-vertex model (run 34) |
| after ca32aa1 | Claude Fable 5 | bookkeeping only: 8857689 adopts the runs-29--34 reassessment into STATUS.md. Correction to that commit's body: the reassessment text it incorporates was authored by OpenAI Codex and relayed by John, not authored by John. All substantive input to this repo remains Claude models and OpenAI Codex, plus the user-relayed community reactions recorded in notes/community_reactions_2026-08-23.md |
| 311c46f..c9975ec | OpenAI Codex (GPT-5 family) | framing-lemma calculus closure, PL/surface-bundle/complement theorem-boundary packets, framing-shift case 1 search (runs 35--39); Fable's interleaved outreach/bookkeeping commits (3e68c6b, ff814c7) say so in their bodies |
| 23692dd | Claude Fable 5 | run 40: explicit Moser flow retiring the framing lemma's ODE input; typeset-PDF re-audit of every section 8.7 display; also the untracked j-robustness scan drivers and results (commit pending with the table freeze) |
| 4e0ade6..a665d73 | mixed, per commit body | provenance rows (Fable 4e0ade6), framing-shift case 2 analysis (Codex 5860acb), run-number collision fix at 40/41 (Fable 6cca005 and a665d73) |
| 2ec9ed3 | Claude Fable 5 | run 42: simplicial certification of the equivariant lift's covering hypotheses and deck group |
| 9276f22 | OpenAI Codex (GPT-5 family) | run 43: Weinstein chart independence via fiber dilation / Alexander trick, demoting ADK03 to corroboration |
| aad6105 | Claude Fable 5 | run 44: second Weinstein route (Liouville-forced momenta, opposite-shear chart, SL2 invariance); softens run 40's "no ODE citation remains" overstatement and declares the sympy dependency |
| a7a1db4 | OpenAI Codex (GPT-5 family) | runs 46--47: direct equivariant Moser field constructed upstairs (retiring the connected-cover lifting citation) and the cumulative-coordinate flow construction removing the Picard--Lindelof citation |
| 5da551d | Claude Fable 5 | run 45: framing-shift robustness table frozen — 100 cases, 82 certified trivial, 18 inconclusive, 0 nontrivial; all beta-only shifts certified; scan driver, verdict log, GAP programs, and rewriting systems committed |
| 1bc4caf | Claude Fable 5 | records the run 45 freeze in STATUS and PROVENANCE and finalizes the outreach draft |
| 972f7df | OpenAI Codex (GPT-5 family) | run 48: exhaustive local flatness of both surgery tori — 1,776 link pairs classified with replayed collapse witnesses |
| 2bda20f | OpenAI Codex (GPT-5 family) | run 49: explicit half-weight normal block model and the global PL frontier equivalence; T_derived_regular_neighborhood removed |
| 8e8a929 | OpenAI Codex (GPT-5 family) | run 50: PL-to-smooth reroute through the already-smooth target; smoothing and intersection-naturality nodes removed |
| 8e5d7e9 | OpenAI Codex (GPT-5 family) | run 51: direct relative marked monodromies, exact on the c collar with the full beta trace product on the e collar |
| b4af95d | OpenAI Codex (GPT-5 family) | run 52: explicit marked graph clutching; T_surface_bundle removed, assembly certificate symbolic |
| 44baf93 | OpenAI Codex (GPT-5 family) | addresses the independent replay review: 82/18 correction, seam-convention repair with a guarding test, honest run-52 weighting, ledger edges, doubled-bundle extension, restored attack surface |
| e57a71d | Claude Fable 5 | run 53: interpretation dictionary bound with per-entry witnesses and the non-executing author-code cross-check; three residual entries declared |

A separate Claude Fable 5 window is independently building an alternative
fiber realization (handle model: two 4x4 grid tori joined by an annulus,
psi0 realized as a linear order-6 rotation with 6 edge flips) from the
pre-bundle tarball state. As of 661e810 none of that work has landed in this
repo — fiber.py here is still the five-chain plumbing model. If that work is
ever imported, it must come in as a clearly labeled alternative module on its
own commit, not as an overwrite of the five-chain files, because the entire
certificate chain in runs/ depends on the five-chain complex.

The later Codex `alternative_bundle.py` is not that Fable handle model. It
retains the certified five-chain fiber and independently rebuilds the bundle
assembly with a different subdivision; Run 31 states its exact independence
boundary.

Likewise, the later Codex `independent_fiber.py` is not the unlanded Fable
two-grid-torus model. It constructs a 58-vertex surface directly from the
abstract five-chain ribbon graph by vertex disks and edge bands; Run 34 gives
its provenance and exact comparison boundary.
