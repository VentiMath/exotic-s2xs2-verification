# luttinger — combinatorial π₁ of torus complements and Luttinger surgeries

Status (updated 2026-08-29; see `../STATUS.md` for the precise caveats):

> **Known unreconciled external computation.** Wuebben's repository has stated
> since its first visible commit that Lidman and Piccirillo report a
> computation of π₁(V) disagreeing with his, and that the disagreement is
> unresolved. Their published v1 never asserts π₁(V) ≠ 1 — it proves H₁(V) = 0
> and normal generation by π₁(F) — and no relation sheet or nontriviality
> witness for the contrary computation is public. Their v1 source also
> explicitly declines to fix the surgery parametrization, so `V` names a
> manifold only after choices that Wuebben's theorem fixes and the reported
> computation may not. The certificates here decide the presented groups of a
> sealed, hash-bound model; they do not reconcile that report. See `../runs/67`
> and `../notes/lp_disagreement_reconciliation_2026-08-29.md`.


* **Engine (working, calibrated):** triangulated 4-manifold `K` + full
  2-dimensional torus subcomplex `T` → presentation of π₁(K − T), based
  meridian word, based product-framing push-off words (fiber and base
  directions), all read off the *combinatorics only* — no hand-derived words.
  Surgered groups go to GAP.
* **Calibration 1** (`t4_test.py` / `t4_run.py`): `T⁴ ⊃ S¹×S¹`.
  π₁(complement) matches `Z²×F₂`, killing the meridian matches `Z⁴`,
  single surgery matches the textbook presentation. PASS.
* **Calibration 2** (`bk_t4_test.py`): Baldridge–Kirk double surgery on two
  disjoint Lagrangian tori in `T⁴` (the paper's own Appendix B.1 test).
  Output group = `(Z²⋊_A Z)×Z` with `tr A = 1` for opposite signs and
  `tr A = 3` for equal signs, through index 6; the `tr A = −1, −3` groups
  are never produced. PASS — this is sign- and basing-sensitive.
* **Bundle and based paper bridge built:** the non-product bundle `R`, both
  surgery tori, and the complement are constructed combinatorially. Explicit
  p-whiskered generators reproduce the based monodromies. Oriented punctured
  sweeps and local-star calculations certify M1--M3 and the `N` meridian. The
  paper basings give `dir_base(T_alpha)=Ax` and
  `dir_base(T_beta)=(r^-1 M r)B`.
* **Fundamental-group blocker resolved:** filling with the literal coherent
  boundary pairs certifies all eight groups (four signs, two half-drifts)
  trivial by independently checked derivation DAGs on the original
  four-generator presentations. KBMAG is only an untrusted proof generator;
  the checker replays the relator axioms, overlaps, rewrite paths, tidying
  changes, and eight one-letter identity rules. One unused alternate beta
  coordinate expression remains inconclusive, but no filling calculation
  depends on it. Run 35 checks the framing lemma's full inline calculus and
  isolates its remaining standard smooth-theorem inputs; it does not
  formalize those theorems or every global exoticness input.
* **Proof artifacts:** the seeded 99,860-step raw-complex Tietze transport
  is sealed with its serialized input in `sealed_transport/` and replays
  under standalone Python and Ruby checkers, and the eight fillings of the
  resulting 3-generator presentation carry derivation DAGs (39,163 records)
  replayed by both filled-group checkers; see `../runs/66`. The earlier
  four-generator export's eight DAGs (`../runs/29`, `../runs/57`) reach the
  same verdicts and are retained as superseded corroborating evidence: that
  export's transport certificate came from an unseeded run and is not
  replayable. Run 57 independently checks the same
  14,115 DAG records in Ruby, sharing neither code nor runtime with the Python
  verifier. A separate basis-free implementation
  reconstructs both commonly based peripheral pairs directly from the marked
  triangulation; see `../runs/30`. A second bundle builder, independent of the
  original bundle and layer modules, reproduces the marked beta homology action
  and peripheral semantics on a different triangulation; see `../runs/31`.
  Its exact based-pi1 action is independently certified in `../runs/32`.
  All 128 local PL flip traces are certified in `../runs/33`.
  A separately triangulated ribbon-graph fiber has the identical equivariant
  marked code; see `../runs/34`. Run 36 integrates the finite hypotheses of
  the residual PL theorems and supplies a cited referee packet.
* **Auxiliary framing-shift scan closed:** Runs 59--62 certify 17 of the 18
  cases left open by the original 100-case scan. Run 63 resolves the final
  `n0_y1` aligned positive-diagonal case through the 96 relators it shares
  with the neighboring `n1_y2` presentation. The common core is infinite
  cyclic and the case-100 filling relator kills its generator. Independent
  Python and Ruby replay of the retained 4,040-record ancestry DAG gives the
  final tally: **100/100 reported trivial — 22 certificate-backed, 78 retained GAP-session verdicts — 0 inconclusive, 0 nontrivial**.
  These stress-test hypothetical framing errors and are not inputs to the
  paper's certified `j=0` groups; see `../runs/59`--`../runs/63`.

## Files
| file | what |
|---|---|
| `complex.py` | simplicial complexes, ordered (staircase) products, grid tori, links |
| `pi1.py` | spanning-tree presentation of π₁ from the 2-skeleton; edge-path words |
| `complement.py` | `TorusComplement`: induced-complement model, derived-neighbourhood frontier Ṅ, meridian = dual-cell boundary, push-offs, retraction `r: C' → C` |
| `sweep.py` | simplicial basing-sweep and torus-incidence certificates |
| `group_attack.py` | reproducible GAP/KBMAG/ACE/finite-quotient attacks, including export and replay of certified paper-coordinate fillings |
| `direct_rws/` | eight simplified presentations, completed rewriting systems, result records, and a SHA-256 manifest |
| `CERTIFICATE_SPEC.md` | normative mathematical grammar and soundness proof for `luttinger-kbmag-proof-v1` |
| `proof_certificates/` | eight compressed, separately checked derivation DAGs plus SHA-256 manifest |
| `verify_kbmag_certificate.py` | small checker for the derivation DAGs; does not import or run KBMAG |
| `verify_certificates.rb` | separate Ruby/standard-library checker for the same eight DAGs, with corruption controls |
| `sealed_transport/` | serialized raw-complex presentation, 99,860-step Tietze certificate, 3-generator result of the canonical seeded run, and the derivation certificates of its eight fillings (`proof_certificates/`, `raw_proof_inputs/`, `kbprog_options.json`) |
| `verify_tietze_transport.py`, `verify_tietze_transport.rb` | standalone replay of the sealed transport, with corruption controls |
| `r3_complement_audit.py` | embeds the R3 mapping-cylinder certificate at the parallel beta level in the actual two-torus complement and checks the basepoint homotopy to `B` |
| `compile_kbmag_certificate.py` | untrusted history compiler and dependency-cone pruner |
| `kbmag-proof/` | minimal KBMAG logging patch used only to generate complete histories |
| `case100_transfer/` | exact 96-relator common-core source, compact case-100 ancestry certificate, and independent Python/Ruby verifiers |
| `presentation_search.py` | proof-oriented Nielsen and relator-multiplication search |
| `case1_compact_attack.py` | replayable named-word/Nielsen/Tietze search for the hardest auxiliary framing-shift case |
| `case2_compact_attack.py` | exact compact export and replayable attack for the adjacent `j_alpha=+2` framing-shift case |
| `paper_bridge.py` | explicit p-whiskered octagon generators, based open-stack monodromy, and drilled-fiber R3 certificates |
| `peripheral_bridge.py` | exact torus-slope permutation and opposite-side alpha basing checks |
| `independent_peripheral_extractor.py` | separate derived-frontier, meridian, product-push-off, and literal-whisker extractor |
| `independent_peripheral_certificate.json` | canonical path hashes and source metadata for the independent extraction |
| `alternative_bundle.py` | independent marked-bundle builder with a different 64-interface beta triangulation |
| `alternative_bundle_audit.py` | structural, marked-homology, and peripheral comparison for the alternative bundle |
| `alternative_bundle_certificate.json` | reproducible certificate for the alternative construction and comparison |
| `alternative_based_monodromy.py` | exact based-pi1 proof generator and replay checker for the alternative beta trace |
| `alternative_based_monodromy.json.gz` | 34,735-step Tietze and terminal Dehn certificate for the alternative trace |
| `pl_flip_trace.py` | simplex-level checker for all flip cone-balls, untouched prisms, slabs, and vertex links |
| `pl_flip_trace_certificate.json` | reproducible local and global PL certificate for the alternative trace |
| `independent_fiber.py` | separate vertex-disk/edge-band realization of the marked genus-2 fiber; does not import `fiber.py` |
| `independent_fiber_audit.py` | canonical equivariant ribbon-code comparison and common-subdivision certificate |
| `independent_fiber_certificate.json` | reproducible marked-fiber equivalence certificate |
| `pl_theorem_audit.py` | integrated checker binding flip, ribbon, smoothing, and section hypotheses to finite certificates |
| `pl_theorem_hypotheses.json` | reproducible integrated PL-boundary certificate |
| `model_correspondence.py` | global marked-bundle, monodromy, boundary, and surgery-torus correspondence audit |
| `framing_check.py` | exact relative-Moser, double-cover, coordinate, seam, and push-off calculus for the paper's framing lemma |
| `weinstein_chart_independence.py` | exact first-jet audit for the self-contained Weinstein-chart framing-independence argument |
| `pl_self_intersection.py` | extracted fixed-point section, doubled PL normal neighborhood, and explicit square-zero push-off |
| `downstream_audit.py` | finite Euler, rank-two lattice, square-zero, cover-genus, and adjunction checks for Theorem 1.2 |
| `proof_ledger.py` | checks the dependency graph while keeping source assumptions, cited theorems, geometric arguments, software trust, and machine certificates distinct |
| `publication_semantics_check.py` | regression-checks Theorem B's sliceness polarity and the $V_{aud}$ versus Wuebben scope boundary against the manuscript, supplement, and downstream certificate |
| `tietze.py` | Tietze elimination (865 → 4 generators in ~3 s) |
| `t4_test.py`, `t4_run.py`, `t4_gap_tail.g` | calibration 1 |
| `bk_t4_test.py` | calibration 2 (Baldridge–Kirk) |
| `fiber.py`, `layers.py`, `bundle.py`, `r_run.py` | bundle construction and target certificate |
| `DESIGN.md` | the mathematics the code relies on |
| `paper_data.md` | Wuebben's construction and Table 1 extracted for the target run |

`group_attack.py word --name NAME` and `word-all` test exported tracked words
in the complement group; identity reductions are positive certificates, while
nonempty output from a nonconfluent rewriting system is reported as
inconclusive.

## Run
```
apt-get install gap-core gap-libs      # GAP 4.x
python3 t4_run.py                      # ~30 s incl. GAP
python3 bk_t4_test.py                  # ~1–2 min incl. GAP (LowIndex to 6)
python3 group_attack.py paper-kb-all   # all eight paper-coordinate fillings
python3 group_attack.py paper-kb-hard  # alternate ordering for the default-hard case
python3 group_attack.py direct-paper-kb-all   # eight literal peripheral fillings
python3 group_attack.py direct-paper-kb-hard  # alternate ordering for one holdout
python3 group_attack.py direct-paper-export   # durable completed systems + hashes
python3 group_attack.py direct-paper-replay   # verify hashes, reload, and replay all eight
python3 verify_kbmag_certificate.py proof_certificates/*.json.gz
ruby verify_certificates.rb --negative-controls
python3 verify_tietze_transport.py --negative-controls
ruby verify_tietze_transport.rb --negative-controls
python3 verify_kbmag_certificate.py --input sealed_transport/r_presentations.json --full-inventory --expect-generators 3 --expect-relators 78 --negative-controls sealed_transport/proof_certificates/*.json.gz
ruby verify_certificates.rb --root sealed_transport --full-inventory --expect-generators 3 --expect-relators 78 --negative-controls
python3 make_proof_manifest.py --check
python3 independent_peripheral_extractor.py --check --output independent_peripheral_certificate.json
python3 alternative_bundle_audit.py --check --output alternative_bundle_certificate.json
python3 alternative_based_monodromy.py --check --output alternative_based_monodromy.json.gz
python3 pl_flip_trace.py --check --output pl_flip_trace_certificate.json
python3 independent_fiber_audit.py --check --output independent_fiber_certificate.json
python3 framing_check.py
python3 pl_theorem_audit.py --check --output pl_theorem_hypotheses.json
python3 downstream_chain.py --check
ruby verify_downstream_chain.rb
python3 proof_ledger.py
python3 publication_semantics_check.py
```
