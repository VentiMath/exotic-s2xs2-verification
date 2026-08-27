# luttinger — combinatorial π₁ of torus complements and Luttinger surgeries

Status (updated 2026-08-25; see the root `STATUS.md` for the precise caveats):

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
  four-generator presentations; KBMAG is only the untrusted generator. One
  unused alternate beta
  coordinate expression remains inconclusive, but no filling calculation
  depends on it. Run 35 checks the framing lemma's full inline calculus and
  isolates its remaining standard smooth-theorem inputs. Runs 43--45 then
  discharge chart independence and remove covering-space lifting by a direct
  equivariant Moser construction. Run 47 constructs the general relative
  Moser flow as an explicit monotone inverse, removing the separate local
  ODE theorem as well. The project does not formalize every global
  exoticness input.
* **Downstream implications audited:** conditional on the certified
  simple-connectivity result, the covering, intersection-form, Freedman,
  Kodaira-dimension, slicing, and reglued Heegaard Floer arguments have the
  stated hypotheses.  No further gap was found; see `runs/24` and
  `notes/downstream_theorem_audit_2026-08-23.md`.
* **Proof artifacts:** the 99,860-step target Tietze reduction and all eight
  filled-group derivation DAGs are independently replayed; see `runs/10`--`18`
  and `runs/29`. A separate basis-free implementation also reconstructs both
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
| `verify_kbmag_certificate.py` | independent checker; does not import or run KBMAG |
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
| `pl_theorem_audit.py` | integrated checker binding flip, ribbon, smoothing, and section hypotheses to finite certificates |
| `pl_theorem_hypotheses.json` | reproducible integrated PL-boundary certificate |
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
python3 verify_kbmag_certificate.py proof_certificates/*.json.gz
python3 make_proof_manifest.py --check
python3 independent_peripheral_extractor.py --check --output independent_peripheral_certificate.json
python3 alternative_bundle_audit.py --check --output alternative_bundle_certificate.json
python3 alternative_based_monodromy.py --check --output alternative_based_monodromy.json.gz
python3 pl_flip_trace.py --check --output pl_flip_trace_certificate.json
python3 independent_fiber_audit.py --check --output independent_fiber_certificate.json
python3 framing_check.py
python3 pl_theorem_audit.py --check --output pl_theorem_hypotheses.json
```
