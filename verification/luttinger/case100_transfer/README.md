# Case 100: common-core transfer certificate

The presentations `n0_y1_ap1_bp1_jap1_jbp1` (case 100) and
`n1_y2_ap1_bp1_jap1_jbp1` each have 97 relators.  Their last 96 relators are
identical.  Write this common core as `C`, and write the two distinct first
relators as `r0` and `r1`.

The certificate in this directory proves directly from `C` that

```
g1 = 1,  g3 = 1,  g4 = 1,  r0 = g2^-1,  r1 = g2^-1.
```

Case 100 imposes `r0 = 1`, so the fourth displayed equality gives `g2 = 1`.
All four generators of the case-100 group are therefore trivial.  The `r1`
equality is not needed for the implication; it is retained as an independent
check of the observed transfer to the already certified paired presentation.

`build_transfer_input.py` reconstructs the exact source from the two frozen
97-relator JSON files, checks the 96-relator match, and emits an uncompleted
shortlex KBMAG input with fixed limits (`tidyint=500`, `maxeqns=300000`,
`maxstates=2000000`).  `compile_transfer_certificate.py` is an untrusted
compiler: it extracts only the ancestry needed for the five displayed
equalities.  Both `verify_transfer_certificate.py` and
`verify_transfer_certificate.rb` replay that ancestry independently and
check the final group-theoretic implication.

The paired `n1` certificate is not an input to this proof.  Its extra-relator
reduction is included only as a cross-check; the case-100 conclusion uses the
common core and `r0` alone.

## Replay

From the repository root, the compact checked artifacts replay with:

```sh
python3 luttinger/case100_transfer/verify_transfer_certificate.py \
  luttinger/case100_transfer/case100_transfer.json.gz
ruby luttinger/case100_transfer/verify_transfer_certificate.rb \
  luttinger/case100_transfer/case100_transfer.json.gz
```

Both verifiers reconstruct the 96/97 comparison from the two frozen source
presentations, replay every retained equation-ancestry record, replay each
final target trace, and print `VERIFIED CASE 100 TRIVIAL`.

To regenerate the untrusted certificate, first run
`build_transfer_input.py`, run the emitted GAP program to export
`common_core_input.rws`, and then run the patched history generator and
compiler:

```sh
python3 luttinger/kbmag_history.py \
  luttinger/case100_transfer/common_core_input.rws \
  luttinger/case100_transfer/common_core.history \
  --image luttinger-kbmag-proof:4
python3 luttinger/case100_transfer/compile_transfer_certificate.py \
  luttinger/case100_transfer/common_core.history \
  luttinger/case100_transfer/case100_transfer.json.gz
```

The full history is about 93 MB and is intentionally a reproducible build
artifact rather than part of the compact certificate.  The certificate is
about 71 KB and retains the complete dependency cone needed by its targets.
