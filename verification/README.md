# luttinger — combinatorial π₁ of torus complements and Luttinger surgeries

Status (updated 2026-08-29; see the root `STATUS.md` for the precise caveats):

> **Terminology in v2.1.** The manuscript now calls D1--D14 the **Source
> Comparison Hypotheses** and separates them into textual, diagrammatic, and
> smooth/framing classes. Frozen machine artifacts retain the legacy node
> name `A_source_formalization_D`; it denotes the same conjunction.

> **Known unreconciled external computation.** Wuebben's repository has stated
> since its first visible commit that Lidman and Piccirillo report a
> computation of π₁(V) disagreeing with his, and that the disagreement is
> unresolved. Their published v1 never asserts π₁(V) ≠ 1 — it proves H₁(V) = 0
> and normal generation by π₁(F) — and no relation sheet or nontriviality
> witness for the contrary computation is public. Their v1 source also
> explicitly declines to fix the surgery parametrization, so `V` names a
> manifold only after choices that Wuebben's theorem fixes and the reported
> computation may not. The certificates here decide the presented groups of a
> sealed, hash-bound model; they do not reconcile that report. See `runs/67`
> and `notes/lp_disagreement_reconciliation_2026-08-29.md`.


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
* **Both coordinate identities sealed:** Run 68 proves the literal 72-letter
  residual `lb_a_y1^-1 * geom_A * geom_x` equal to the identity in the sealed
  3-generator, 78-relator complement, without a filling relation. Independent
  Python and Ruby verifiers replay its 2,506-record ancestry DAG and 61-step
  target reduction. Run 69 proves the corresponding 113-letter beta residual
  `lb_b_s2^-1 * geom_r^-1 * geom_M * geom_r * geom_B` in 82 steps from a
  1,540-record ancestry DAG. Both verifier pairs reject altered inputs,
  forged derivations, and damaged target traces. Neither certificate contains
  a filling relation. Run 68 supersedes Run 15's nonreproducible pre-export
  evidence while preserving its conclusion.
* **Fundamental-group blocker resolved:** filling with the literal coherent
  boundary pairs certifies all eight groups (four signs, two half-drifts)
  trivial by independently checked derivation DAGs on the original
  four-generator presentations; KBMAG is only the untrusted generator. One
  unused alternate beta
  coordinate expression remains inconclusive, but no filling calculation
  depends on it. Run 35 checks the framing lemma's full inline calculus and
  isolates its remaining standard smooth-theorem inputs. Runs 43--44 and 46
  discharge chart independence and remove covering-space lifting by a direct
  equivariant Moser construction. Run 47 constructs the general relative
  Moser flow as an explicit monotone inverse, removing the separate local
  ODE theorem as well. The project does not formalize every global
  exoticness input.
* **Local flatness exhausted:** Run 48 checks the standard codimension-two
  link pair at every one of the 1,776 simplices of both surgery tori. All 296
  vertex cases include replayed collapse witnesses for an ambient `S3` link
  and an unknotted torus-link circle; all 888 edge and 592 triangle cases pass
  their finite sphere-link tests.
* **Normal frontier made explicit:** Run 49 identifies all 113,336 computed
  frontier vertices with the half-weight barycentric normal boundary by a
  global PL homeomorphism and checks all 592 dual meridians as literal normal
  circle fibers. The derived-regular-neighborhood theorem is no longer a
  dependency of the filled-presentation claim.
* **PL-to-smooth bridge rerouted:** Run 50 transports the certified marked
  tori, collars, peripheral data, and section cycles by an
  orientation-preserving homeomorphism into the underlying topological
  manifold of the audit-defined already smooth bundle `R_aud`. The source triangulation is
  never smoothed. The disjoint homologous section pair remains so in the
  target, proving square zero there and removing compatible 4D source
  smoothing and separate intersection naturality from the proof ledger.
  Comparing `R_aud` with Wuebben's intended `R` is the separate fourteen-clause
  Source Comparison Hypotheses D1--D14 boundary.
* **Relative markings made direct:** Run 51 certifies the full `c` and `e`
  collars. Alpha agrees exactly on the `c` collar; the beta twist trace avoids
  the `e` collar in all 1,536 trace cells and restricts to its literal product
  in all 3,072 collar tetrahedra. Relative isotopy extension is no longer a
  theorem input.
* **Bundle homeomorphism explicitly clutched:** Run 52 constructs the map and
  its inverse on both mapping-cylinder handles, checks their seam equations,
  and glues them on the common marked fiber. Surface-bundle classification
  and Dehn--Nielsen--Baer are now diagnostic alternatives, not dependencies.
* **Paper dictionary independently reconstructed:** Run 54 reads only the raw
  paper text, reconstructs the five-chain, involution, ordered twists, tori,
  named whiskers, and directions, and only then compares the frozen result
  with Runs 34, 51, and 52. Reversed-order and reversed-sign mutations are
  distinguished, and no paper-to-model discrepancy was found.
* **Lemma 7.1 reduced to a precise classical theorem:** Run 55 enumerates all
  36 equivariant ribbon rotations. Exactly four survive, all differing only
  by curve orientations; every one has two invariant 10-edge disk faces with
  free half-turn boundary action. The only remaining input is the published
  Kerékjártó classification of periodic disk homeomorphisms.
* **Original source figure audited:** Run 56 reads the immutable
  Lidman--Piccirillo v1 TeX and original vector Figure 1 directly. It recovers
  the ordered five-chain, chain-reversing involution, oriented `c` action,
  labels, and two fixed points required by Run 55, with no discrepancy.
* **Second certificate verifier:** Run 57 rechecks all eight filled-group
  derivation DAGs in Ruby using only its standard library. It shares no code,
  language runtime, or group implementation with the Python checker and
  independently accepts all 14,115 records. Four deliberate corruptions are
  rejected at the relevant trust boundaries.
* **Framing robustness scan closed:** Runs 59--62 certify 17 of the 18
  cases left open by the original 100-case scan. Run 63 resolves the final
  `n0_y1` aligned positive-diagonal case through its 96-relator common core
  with the neighboring `n1_y2` case. The core is infinite cyclic and the
  remaining filling relator kills its generator. Independent Python and Ruby
  replay of the retained 4,040-record ancestry DAG gives the final auxiliary
  tally: **100/100 reported trivial — 22 certificate-backed, 78 retained GAP-session verdicts — 0 inconclusive, 0 nontrivial**.
* **Downstream proof chain:** `downstream_chain.py` carries every
  implication from certified simple connectivity of the audit manifold to
  Theorems A, B, C as an explicit item — Source Comparison Hypotheses D1--D14 as one
  source-comparison assumption, 25 external theorems with hypotheses and
  sources, 3 hash-bound certificates, 15 computed facts, and 17 deduction
  steps — and
  freezes it as `downstream_chain_certificate.json`;
  `verify_downstream_chain.rb` independently recomputes every fact, checks
  the graph, and verifies the evidence digests. See `runs/64` and
  `notes/downstream_proof_chain_2026-08-28.md`; the earlier hypothesis
  audit is `runs/24`.
* **Proof artifacts:** the seeded 99,860-step raw-complex Tietze transport
  is sealed with its serialized input and replays under standalone Python
  and Ruby checkers, and the eight fillings of the resulting 3-generator
  presentation carry derivation DAGs (39,163 records) replayed by both
  filled-group checkers, so the chain from the frozen raw complex to the
  eight triviality verdicts replays end to end; see `runs/66`. The earlier
  four-generator export's eight DAGs (`runs/29`, `runs/57`) reach the same
  verdicts and are retained as superseded corroborating evidence: that
  export's transport certificate came from an unseeded run and is not
  replayable. A separate basis-free implementation also reconstructs both
  commonly based peripheral pairs directly from the marked triangulation; see
  `runs/30`. A second bundle builder, independent of the original bundle and
  layer modules, reproduces the marked beta homology action and peripheral
  semantics on a different triangulation; see `runs/31`. Its exact based-pi1
  action is independently certified in `runs/32`, and all 128 local PL flip
  traces are certified in `runs/33`. A separately triangulated ribbon-graph
  fiber has the identical equivariant marked code; see `runs/34`. Run 36
  integrates the finite hypotheses of the residual PL theorems and supplies a
  cited referee packet.

## Files
| file | what |
|---|---|
| `complex.py` | simplicial complexes, ordered (staircase) products, grid tori, links |
| `pi1.py` | spanning-tree presentation of π₁ from the 2-skeleton; edge-path words |
| `complement.py` | `TorusComplement`: induced-complement model, derived-neighbourhood frontier Ṅ, meridian = dual-cell boundary, push-offs, retraction `r: C' → C` |
| `sweep.py` | simplicial basing-sweep and torus-incidence certificates |
| `group_attack.py` | reproducible GAP/KBMAG/ACE/finite-quotient attacks, including export and replay of certified paper-coordinate fillings |
| `direct_rws/` | eight simplified presentations, completed rewriting systems, result records, and a SHA-256 manifest |
| `proof_certificates/` | eight compressed derivation DAGs and a SHA-256 manifest for the original presentations |
| `verify_kbmag_certificate.py` | independent checker; does not import or run KBMAG; `--full-inventory` enforces the eight-case batch |
| `verify_certificates.rb` | second-language, standard-library checker for all eight filled-group derivation DAGs; enforces the eight-case batch by default |
| `sealed_transport/` | serialized raw-complex presentation (99,863 generators, 321,702 relators, 89 named tracked words), the 99,860-step Tietze certificate, the resulting 3-generator presentation of the canonical seeded run, and the eight derivation certificates of its fillings with their rewriting systems and kbprog options |
| `verify_tietze_transport.py`, `verify_tietze_transport.rb` | standalone replay of the sealed transport from those three files, with corruption controls |
| `r3_complement_audit.py` | embeds the R3 mapping-cylinder certificate at the parallel beta level in the actual two-torus complement and checks the basepoint homotopy to `B` |
| `alpha_residual/` | frozen sealed-complement source, proof certificate, compiler, and independent Python/Ruby verifiers for `lb_a_y1 = Ax` (Run 68) |
| `beta_residual/` | frozen sealed-complement source, proof certificate, compiler, and independent Python/Ruby verifiers for `lb_b_s2 = (r^-1 M r)B` (Run 69) |
| `case100_transfer/` | exact 96-relator common-core source, compact case-100 ancestry certificate, and independent Python/Ruby verifiers |
| `alpha_residual/` | frozen 72-letter alpha-longitude target in the sealed complement, compact 2,506-record ancestry certificate, and independent Python/Ruby verifiers |
| `downstream_chain.py` | the proof chain from π₁(V)=1 to Theorems A, B, C: external theorems, certificates, computed facts, deduction steps |
| `downstream_chain_certificate.json` | frozen Run-64 chain with evidence digests |
| `verify_downstream_chain.rb` | independent Ruby replay of the chain: recomputes every fact, checks the graph and the digests |
| `proof_ledger.py` | the dependency ledger of the whole verification: external theorems, machine certificates, geometric arguments, derived claims |
| `paper_bridge.py` | explicit p-whiskered octagon generators, based open-stack monodromy, and drilled-fiber R3 certificates |
| `peripheral_bridge.py` | exact torus-slope permutation and opposite-side alpha basing checks |
| `independent_peripheral_extractor.py` | separate derived-frontier, meridian, product-push-off, and literal-whisker extractor; imports none of the original peripheral machinery |
| `independent_peripheral_certificate.json` | canonical hashes and source metadata for both independently extracted pairs |
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
| `pl_theorem_audit.py` | integrated checker binding flip, ribbon, bundle, and section hypotheses to finite certificates |
| `pl_theorem_hypotheses.json` | reproducible integrated PL-boundary certificate |
| `topological_smooth_bridge.py` | verifies transport into the audit-defined already smooth target and replays square zero there |
| `topological_smooth_bridge_certificate.json` | bound Run-50 transport and section certificate |
| `relative_marking_check.py` | exact alpha-collar and supported beta-relative representative checker |
| `relative_marking_certificate.json` | reproducible Run-51 relative-monodromy certificate |
| `graph_clutching_check.py` | explicit two-handle mapping-cylinder homeomorphism and inverse checker |
| `graph_clutching_certificate.json` | reproducible Run-52 graph-clutching certificate |
| `paper_coordinate_extractor.py` | quarantined raw-paper marked-coordinate extractor |
| `paper_coordinate_certificate.json` | frozen Run-54 paper-coordinate reconstruction |
| `paper_model_dictionary_compare.py` | separate comparison against Runs 34, 51, 52, and path evidence |
| `paper_model_dictionary_comparison.json` | reproducible Run-54 comparison certificate |
| `lemma71_normal_form_check.py` | exhaustive equivariant five-chain ribbon classifier |
| `lemma71_normal_form_certificate.json` | reproducible Run-55 Lemma 7.1 certificate |
| `lp_source_figure_audit.py` | direct checker for the original Lidman--Piccirillo TeX and vector figure |
| `lp_source_figure_certificate.json` | reproducible Run-56 source-figure certificate |
| `model_correspondence.py` | global marked-bundle, monodromy, boundary, and surgery-torus correspondence audit |
| `framing_check.py` | exact relative-Moser, double-cover, coordinate, seam, and push-off calculus for the paper's framing lemma |
| `presentation_search.py` | proof-oriented Nielsen and relator-multiplication search |
| `tietze.py` | Tietze elimination (865 → 4 generators in ~3 s) |
| `t4_test.py`, `t4_run.py`, `t4_gap_tail.g` | calibration 1 |
| `bk_t4_test.py` | calibration 2 (Baldridge–Kirk) |
| `fiber.py`, `layers.py`, `bundle.py`, `r_run.py` | bundle construction and target certificate |
| `DESIGN.md` | the mathematics the code relies on |
| `paper_data.md` | Wuebben's construction and Table 1 extracted for the target run |

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
python3 verify_kbmag_certificate.py --full-inventory --negative-controls proof_certificates/*.json.gz
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
```
